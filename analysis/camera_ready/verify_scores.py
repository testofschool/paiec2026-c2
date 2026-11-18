"""Check the replay against the registered output for every split2 pair and budget."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "verification/evidence/camera_ready"
BUDGETS = (0, 1, 3, 7, 15, 31)
WEIGHTS = (0.1, 0.2, 0.2, 0.2, 0.2, 0.1)

def read_scores(path):
    frame = pd.read_csv(path, dtype={"bench": str, "subject_id": str}, keep_default_na=False)
    if frame.duplicated(["bench", "subject_id"]).any():
        raise ValueError("Duplicate evaluation pair")
    return frame.set_index(["bench", "subject_id"]).sort_index()

def check(run):
    original = read_scores(run / "eval_split2/split2/scores.csv")
    replay_paths = sorted((run / "camera_ready_m5").glob("*/scores.csv"))
    replay = pd.concat([read_scores(p) for p in replay_paths]).sort_index()
    assert original.index.equals(replay.index)
    cols = [method+"_"+suffix for method in ("C2","frozen")
            for suffix in ("alc", *("b"+str(b) for b in BUDGETS))]
    pair_abs = (original[cols] - replay[cols]).abs()
    assert np.isfinite(pair_abs).all().all()
    assert (original.n_eval == replay.n_eval).all()
    max_diff = pair_abs.max().to_dict()
    counts = original.groupby(level="bench").size()
    stats = json.loads((EVIDENCE / "sparse_caps.json").read_bytes())
    caps = {}
    for cap, result in stats["caps"].items():
        expected = int(counts.clip(upper=int(cap)).sum())
        assert result["pairs"]==expected
        for method in result["methods"].values():
            weighted = sum(w*method["Brier"][str(b)] for w,b in zip(WEIGHTS,BUDGETS))
            assert abs(weighted - method["ALC"]) < 1e-12
        caps[cap] = expected
    rel = json.loads((EVIDENCE / "reliability.json").read_bytes())
    n = int(original.n_eval.sum())
    for method in rel["reliability"].values():
        for r in method.values():
            bins=r["bins"]
            assert len(bins)==10 and sum(b["responses"] for b in bins)==n
            assert all(b["lower"]==i/10 and b["upper"]==(i+1)/10 for i,b in enumerate(bins))
            assert all((b["lower"]-1e-12 <= b["mean_prediction"] <= b["upper"]+1e-12
                        and 0 <= b["observed_rate"] <= 1) if b["responses"] else (
                        b["mean_prediction"] is None and b["observed_rate"] is None) for b in bins)
            ece = sum(b["responses"]*abs(b["mean_prediction"]-b["observed_rate"]) for b in bins if b["responses"])/n
            assert abs(ece-r["ECE"]) < 1e-12
    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()
    gate={"status":"PASS" if max(max_diff.values())<=1e-9 else "FAIL",
          "pairs":len(original),"benchmarks":len(counts),"responses_per_method_budget":n,
          "pair_fields_compared":cols,"max_absolute_difference_by_field":max_diff,"pair_tolerance":1e-9,
          "cap_population_expected_from_full_split":caps,"weighted_sparse_ALCs_checked":True,
          "all_six_reliability_totals_and_ECE_verified":True,
          "official_pair_table_sha256":sha(run/"eval_split2/split2/scores.csv"),
          "validation_script_sha256":sha(Path(__file__))}
    (EVIDENCE/"score_verification.json").write_text(json.dumps(gate,indent=2)+"\n")
    print(json.dumps(gate,indent=2))
if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run",type=Path,required=True)
    check(p.parse_args().run)
