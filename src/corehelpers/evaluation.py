"""Copied C2 numerical evaluation functions for both registered seeds."""
import sys
sys.dont_write_bytecode = True
import hashlib
import time
import numpy as np
import pandas as pd
from scipy.special import expit
from c2 import model as c2
from corehelpers import measure as source
BUDGETS = source.BUDGETS
WEIGHTS = source.WEIGHTS

def split_seed(benchmark):
    return int(hashlib.sha256(("split2:" + benchmark).encode()).hexdigest()[:8], 16)


def partition_cells(cells, benchmark):
    """Use headroom's exact-half raw subject split and identical RNG consumption."""
    eligible = sorted(cells.groupby("subject_id").size().loc[lambda x: x >= 80].index)
    by_subject = {sid: group for sid, group in cells.groupby("subject_id", sort=False)}
    rng, parts = np.random.default_rng(split_seed(benchmark)), {}
    for sid in eligible:
        sub = by_subject[sid].sort_values("item_id", kind="mergesort")
        mask = rng.permutation(len(sub)) < len(sub) // 2
        acquired = sub[mask].iloc[rng.permutation(int(mask.sum()))]
        evaluation = sub[~mask]
        if len(acquired) != len(sub) // 2 or len(acquired) < max(BUDGETS):
            raise ValueError("invalid acquisition split: " + str(sid))
        if set(acquired.item_id).intersection(evaluation.item_id):
            raise ValueError("acquisition/evaluation item overlap: " + str(sid))
        parts[sid] = acquired, evaluation
    return eligible, parts


def candidate_probabilities(subject, keys, state, text_e=None, a=1.0, b=0.0):
    """Vectorized base probabilities, replacing only visible item-offset positions.

    C2 receives text_e=None. C2+D2 receives per-item text predictions and the
    unchanged training calibration. Each distinct visible key is fitted once
    for its actual target exclusion; source logits use the same coefficient a.
    """
    full, name, provider = c2.subject_keys(subject)
    mean, var = c2.frozen_moments(state["prior"], state["fit"], subject)
    if text_e is None:
        frozen_p = c2.frozen.predictive(state["prior"], state["fit"], full, name, provider)
        probabilities = np.full(len(keys), np.clip(frozen_p, 1e-4, 1 - 1e-4))
        base_mean, base_var = mean, var
        a = 1.0
    else:
        text_e = np.asarray(text_e, dtype=float)
        if text_e.shape != (len(keys),) or not np.isfinite(text_e).all():
            raise ValueError("missing or nonfinite evaluation text predictions")
        base_mean, base_var = float(a) * mean, float(a) ** 2 * var
        probabilities = np.clip(expit((base_mean + b * text_e) /
            np.sqrt(1 + np.pi * max(base_var, 0) / 8)), 1e-4, 1 - 1e-4)
    positions = {}
    for pos, key in enumerate(keys):
        if key in state["item_counts"]:
            positions.setdefault(key, []).append(pos)
    for key, indices in positions.items():
        prior_mean = 0.0 if text_e is None else float(b) * float(text_e[indices[0]])
        if text_e is not None and not np.allclose(text_e[indices], text_e[indices[0]], rtol=0, atol=1e-12):
            raise ValueError("identical visible item key has inconsistent text predictions")
        item = {"benchmark_id": state["benchmark"], "item_content": key[0], "item_features": key[1]}
        delta, delta_var, present = c2.posterior_offset(state, item, full, prior_mean, mean_scale=a)
        if present:
            probabilities[indices] = c2._probability(base_mean + delta, base_var + delta_var)
    return probabilities


def simulate_benchmark(benchmark, prior, sigma_delta2, stage="c2", text_e=None,
                       calibration=None, subjects=None, cells=None, table=None):
    """Return complete per-raw-subject score rows and checkpoint diagnostics."""
    if stage not in ("c2", "text"):
        raise ValueError("unknown evaluation stage")
    if subjects is None or cells is None:
        subjects, cells = source.read_bench(benchmark)
    if table is None:
        table = source.item_table(benchmark)
    if not set(cells.item_id).issubset(table.index):
        raise ValueError("response items missing from item table: " + benchmark)
    eligible, parts = partition_cells(cells, benchmark)
    if not eligible:
        return pd.DataFrame(), {"benchmark": benchmark, "pairs": 0, "budgets": []}
    if stage == "text":
        if text_e is None or calibration is None:
            raise ValueError("text stage requires predictions and calibration")
        if not text_e.index.is_unique or not set(cells.item_id).issubset(text_e.index):
            raise ValueError("text predictions omit or duplicate response items: " + benchmark)
        a, b = float(calibration["a"]), float(calibration["b"])
        if not np.isfinite([a, b]).all():
            raise ValueError("nonfinite training calibration")
    else:
        a, b = 1.0, 0.0
    keys_by_id = pd.Series(list(zip(table.item_content, table.item_features)), index=table.index)
    subject_dict = {sid: subjects.loc[sid].to_dict() for sid in eligible}
    items_for_labels = {}
    rows, evaluations = {}, {}
    for sid in eligible:
        acquired, ev = parts[sid]
        meta = subjects.loc[sid]
        rows[sid] = {"bench": benchmark, "fold": source.lobo_eval.fold_of(benchmark),
                     "subject_id": sid, "full": meta.full,
                     "n_eval": int(ev.n.sum()), "n_eval_items": len(ev)}
        k, n = ev.k.to_numpy(float), ev.n.to_numpy(float)
        evaluations[sid] = (k, n, ev.item_id.map(keys_by_id).to_numpy(),
                            None if stage == "c2" else ev.item_id.map(text_e).to_numpy(float))
        if stage == "c2":
            oracle_score = source.brier(k.sum() / n.sum(), k, n)
            for budget in BUDGETS:
                rows[sid][f"A_b{budget}"] = oracle_score
        for item_id in acquired.iloc[:max(BUDGETS)].item_id:
            if item_id not in items_for_labels:
                content, features = keys_by_id.loc[item_id]
                items_for_labels[item_id] = {"benchmark_id": benchmark,
                    "item_content": content, "item_features": features}
    diagnostics = {"benchmark": benchmark, "pairs": len(eligible), "budgets": []}
    for budget in BUDGETS:
        started = time.perf_counter()
        labeled = []
        for sid in eligible:
            for record in parts[sid][0].iloc[:budget].itertuples(index=False):
                labeled.append(((subject_dict[sid], items_for_labels[record.item_id]), int(record.first)))
        state = c2.build_state(prior, labeled, benchmark, sigma_delta2)
        for sid in eligible:
            meta = subject_dict[sid]
            k, n, keys, e = evaluations[sid]
            frozen_p = c2.frozen.predictive(prior, state["fit"], *c2.subject_keys(meta))
            frozen_p = np.clip(frozen_p, 1e-4, 1 - 1e-4)
            rows[sid][f"frozen_b{budget}"] = source.brier(frozen_p, k, n)
            candidate_p = candidate_probabilities(meta, keys, state, e, a, b)
            if stage == "c2":
                rows[sid][f"C2_b{budget}"] = source.brier(candidate_p, k, n)
            else:
                mean, var = c2.frozen_moments(prior, state["fit"], meta)
                d2_p = np.clip(expit((a * mean + b * e) /
                    np.sqrt(1 + np.pi * max(a * a * var, 0) / 8)), 1e-4, 1 - 1e-4)
                rows[sid][f"D2_b{budget}"] = source.brier(d2_p, k, n)
                rows[sid][f"C2D2_b{budget}"] = source.brier(candidate_p, k, n)
        diagnostics["budgets"].append({"budget": budget, "revealed_labels": len(labeled),
            "visible_item_keys": len(state["item_counts"]), "posterior_fits": len(state["offset_cache"]),
            "evidence_fingerprint": state["fingerprint"][1], "wall_seconds": time.perf_counter() - started})
    tags = ("frozen", "A", "C2") if stage == "c2" else ("frozen", "D2", "C2D2")
    for row in rows.values():
        for tag in tags:
            row[f"{tag}_alc"] = sum(w * row[f"{tag}_b{budget}"] for w, budget in zip(WEIGHTS, BUDGETS))
    return pd.DataFrame(list(rows.values())), diagnostics


def validate_frame(frame, record, stage):
    if len(frame) != record["eligible_pairs"] or frame.duplicated(["bench", "subject_id"]).any():
        raise ValueError("incomplete/duplicate benchmark score rows: " + record["bench"])
    if (frame.bench != record["bench"]).any() or (frame.fold != record["fold"]).any():
        raise ValueError("benchmark/fold mismatch in score checkpoint")
    tags = ("frozen", "A", "C2") if stage == "c2" else ("frozen", "D2", "C2D2")
    columns = [f"{tag}_b{budget}" for tag in tags for budget in BUDGETS] + [f"{tag}_alc" for tag in tags]
    values = frame[columns].to_numpy(float)
    if not np.isfinite(values).all() or (values < -1e-12).any() or (values > 1 + 1e-12).any():
        raise ValueError("invalid score values in checkpoint")
    for tag in tags:
        expected = sum(w * frame[f"{tag}_b{budget}"] for w, budget in zip(WEIGHTS, BUDGETS))
        if not np.allclose(frame[f"{tag}_alc"], expected, rtol=0, atol=1e-12):
            raise ValueError("ALC does not match budget scores")
