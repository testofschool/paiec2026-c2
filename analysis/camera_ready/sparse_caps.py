"""Replay split2 after restricting eligible subjects as prespecified in sparse_plan.json."""
import argparse
import gc
import json
import hashlib
import tarfile
from pathlib import Path

import numpy as np
import pandas as pd
from cell_scoring import (ROOT, atomic_json, bindings, ev, load_benchmark, measure, protocol,
                          records, score, select_subjects)

HERE = Path(__file__).resolve().parent
OUTPUT = ROOT / "verification/evidence/camera_ready"


def comparison(frame, comparator):
    d = frame.assign(delta=frame[f"{comparator}_alc"] - frame.C2_alc)
    clusters = d.groupby("bench", sort=True).delta.agg(["sum", "count"])
    ids = np.random.default_rng(0).integers(len(clusters), size=(2000, len(clusters)))
    draws = clusters["sum"].to_numpy()[ids].sum(axis=1) / clusters["count"].to_numpy()[ids].sum(axis=1)
    folds = d.groupby("fold").delta.mean()
    return {"direction": f"{comparator} minus C2", "difference": float(d.delta.mean()),
            "ci95": np.percentile(draws, [2.5, 97.5]).tolist(),
            "fold_mean_differences": {str(f): float(x) for f, x in folds.items()},
            "C2_fold_wins": int((folds > 0).sum()), "ties": int((folds == 0).sum())}


def summarize(frame):
    methods = {m: {"ALC": float(frame[f"{m}_alc"].mean()),
                   "Brier": {str(b): float(frame[f"{m}_b{b}"].mean()) for b in protocol.BUDGETS}}
               for m in ("frozen", "C2", "beta15")}
    return {"pairs": len(frame), "benchmarks": frame.bench.nunique(), "methods": methods,
            "comparisons": {m: comparison(frame, m) for m in ("frozen", "beta15")}}


def run_analysis(run, reference):
    plan = json.loads((HERE / "sparse_plan.json").read_text())
    plan_sha = measure.sha(HERE / "sparse_plan.json")
    if json.loads((HERE / "sparse_plan_receipt.json").read_text())["sha256"] != plan_sha:
        raise ValueError("Sparse plan hash differs from its receipt")
    caps = plan["caps"]
    all_rows = {cap: [] for cap in caps}
    for record in records(run):
        bench = record["bench"]
        prior, variance, subjects, cells, keys = load_benchmark(run, record)
        ranked = select_subjects(bench, cells)
        assert len(ranked) == record["eligible_pairs"]
        previous = None
        for cap in caps:
            keep = ranked[:cap]
            if previous is None or len(previous) != len(keep):
                frame = score(bench, prior, variance, subjects, cells[cells.subject_id.isin(keep)],
                              keys, beta15=True)
                assert set(frame.subject_id) == set(keep)
                previous = frame
            all_rows[cap].append(previous)
        print(bench, len(ranked), flush=True)
        ev.c2.clear_cache()
        del subjects, cells, keys, prior
        gc.collect()
    output = {str(cap): summarize(pd.concat(frames, ignore_index=True)) for cap, frames in all_rows.items()}
    diff = abs(output["1"]["methods"]["frozen"]["ALC"] - output["1"]["methods"]["C2"]["ALC"])
    result = {"caps": output, "design_check": {"status": "PASS" if diff <= 1e-12 else "FAIL",
                                              "absolute_difference": diff, "tolerance": 1e-12},
              "reference_v14": reference, "sparse_plan_sha256": plan_sha, **bindings(run)}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    atomic_json(OUTPUT / "sparse_caps.json", result)


def read_v14(path):
    member = "PAIEC_v14_evidence/v14/paired_sparse_audit/results.json"
    with tarfile.open(path, "r:*") as archive:
        raw = archive.extractfile(member).read()
    original = json.loads(raw)
    return {"archive": path.name, "archive_sha256": measure.sha(path),
            "member": member, "member_sha256": hashlib.sha256(raw).hexdigest(),
            "comparison": "Descriptive reference only; device and selection protocol differ.",
            "caps": {str(r["cap"]): {"pairs": r["pairs"], "C2_ALC": r["methods"]["C2"]["alc"]}
                     for r in original["results"] if r["cap"] in (1, 2, 8)}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--v14-archive", type=Path, help="Original v14 evidence archive")
    args = parser.parse_args()
    reference = read_v14(args.v14_archive) if args.v14_archive else "NOT_FOUND"
    run_analysis(args.run, reference)
