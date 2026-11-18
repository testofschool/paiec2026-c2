"""Shared split2 replay for sparse-cap scores and response-weighted reliability."""
import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from corehelpers import evaluation as ev, measure, protocol
from corehelpers.io import atomic_json, read_json, validate_inventory


def records(run):
    measure.DATA = run / "data"
    inventory = validate_inventory(read_json(run / "artifacts" / "prepared.json"), measure.DATA)
    return [r for r in inventory if r["eligible_pairs"]]


def load_benchmark(run, record):
    bench, fold = record["bench"], record["fold"]
    folder = run / "artifacts"
    prior = read_json(folder / f"fold_prior_{fold}.json")
    config = read_json(folder / f"fold_{fold}_config.json")
    assert config["fold"] == fold
    variance = config["sigma_delta2"]
    ev.c2.set_prior(prior, variance)
    subjects, cells = measure.read_bench(bench)
    table = measure.item_table(bench)
    keys = pd.Series(list(zip(table.item_content, table.item_features)), index=table.index)
    if not set(cells.item_id).issubset(keys.index):
        raise ValueError(f"Missing item metadata for {bench}")
    return prior, variance, subjects, cells, keys


def select_subjects(bench, cells):
    counts = cells.groupby("subject_id").size()
    eligible = counts[counts >= protocol.MIN_ITEMS].index
    return sorted(eligible, key=lambda sid: hashlib.sha256(f"cap:{bench}|{sid}".encode()).hexdigest())


def score(bench, prior, variance, subjects, cells, keys, *, beta15=False, observe=None, score_partitions=None):
    eligible, parts = ev.partition_cells(cells, bench)
    rows, evaluate, acquisitions = {}, {}, {}
    for sid in eligible:
        train, test = parts[sid]
        meta = subjects.loc[sid].to_dict()
        k, n = test.k.to_numpy(float), test.n.to_numpy(float)
        evaluate[sid] = meta, test.item_id.map(keys).to_numpy(), k, n
        rows[sid] = {"bench": bench, "fold": protocol.fold_of(bench), "subject_id": sid,
                     "n_eval": int(n.sum())}
        acquisitions[sid] = []
        for record in train.iloc[:max(protocol.BUDGETS)].itertuples(index=False):
            content, features = keys.at[record.item_id]
            item = {"benchmark_id": bench, "item_content": content, "item_features": features}
            acquisitions[sid].append(((meta, item), int(record.first)))
    for budget in protocol.BUDGETS:
        labeled = [label for sid in eligible for label in acquisitions[sid][:budget]]
        state = ev.c2.build_state(prior, labeled, bench, variance)
        for sid in eligible:
            meta, evaluation_keys, k, n = evaluate[sid]
            frozen = np.clip(ev.c2.frozen.predictive(prior, state["fit"], *ev.c2.subject_keys(meta)),
                             1e-4, 1 - 1e-4)
            c2 = ev.candidate_probabilities(meta, evaluation_keys, state)
            row = rows[sid]
            row[f"frozen_b{budget}"] = measure.brier(frozen, k, n)
            row[f"C2_b{budget}"] = measure.brier(c2, k, n)
            if beta15:
                successes = sum(label for _, label in acquisitions[sid][:budget])
                row[f"beta15_b{budget}"] = measure.brier((1.5 + successes) / (3 + budget), k, n)
            if observe is not None:
                observe(budget, frozen, c2, k, n)
    frame = pd.DataFrame(list(rows.values()))
    for method in (("frozen", "C2", "beta15") if beta15 else ("frozen", "C2")):
        frame[f"{method}_alc"] = sum(w * frame[f"{method}_b{b}"]
                                     for w, b in zip(protocol.WEIGHTS, protocol.BUDGETS))
    if score_partitions is not None:
        extra = pd.DataFrame(score_partitions(bench, subjects, parts))
        join = ["bench", "subject_id"]
        if set(map(tuple, extra[join].values)) != set(map(tuple, frame[join].values)):
            raise ValueError(f"Baseline scorer used different pairs for {bench}")
        overlap = sorted(set(frame.columns) & set(extra.columns) - set(join))
        for col in overlap:
            left = frame.set_index(join)[col].sort_index()
            right = extra.set_index(join)[col].sort_index()
            if not np.array_equal(left.values, right.values):
                raise ValueError(f"Baseline and replay field differs: {bench} {col}")
        frame = frame.merge(extra.drop(columns=overlap), on=join, validate="one_to_one")
    return frame


def bindings(run):
    folder = run / "artifacts"
    paths = [folder / "prepared.json", folder / "training_receipt.json",
             *(folder / f"fold_prior_{f}.json" for f in range(protocol.N_FOLDS)),
             *(folder / f"fold_{f}_config.json" for f in range(protocol.N_FOLDS))]
    return {"inputs": {p.name: measure.sha(p) for p in paths},
            "cell_scoring_sha256": measure.sha(Path(__file__)),
            "registered_evaluator_sha256": measure.sha(Path(ev.__file__))}
