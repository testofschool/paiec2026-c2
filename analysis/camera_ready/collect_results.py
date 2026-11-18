"""Assemble v21 measurements from scored files, historical receipts and the official comparison."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
EVIDENCE = REPO / "verification/evidence/camera_ready"

def read(path):
    return json.loads(path.read_bytes())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def relative(path):
    return path.relative_to(REPO).as_posix()

def file_time(path):
    return dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).isoformat()

def collect(run):
    registered=read(REPO / "verification/expected_values.json")
    actual=read(run / "eval_split2/results.json")["split2"]
    official=read(run / "compare_split2.json")
    checks={key:dict(expected=value, actual=actual["metrics"][key],
                     absolute_difference=abs(value-actual["metrics"][key]))
            for key,value in registered["split2"].items()}
    tol=registered["tolerance"]
    status="PASS" if official["status"]=="PASS" and all(x["absolute_difference"]<=tol for x in checks.values()) else "FAIL"
    repro=dict(status=status, checks=checks, tolerance=tol, coverage=actual["coverage"],
               compare_split2_sha256=sha(run/"compare_split2.json"), split2_results_sha256=sha(run/"eval_split2/results.json"))
    def row(script, source, outcome, values, inputs=None, **extra):
        source=EVIDENCE/source
        code=HERE/script
        return dict(status=outcome, values=values, script=relative(code), script_sha256=sha(code),
                    evidence=relative(source), inputs={relative(source):sha(source), **(inputs or {})},
                    repro_gate=status, measured_at=file_time(source), **extra)
    def result(name):
        return read(EVIDENCE/name)
    inv=result("inventory.json")
    expected_counts=dict(inventory_benchmarks=163, benchmarks_any_pair_n_ge_5=158, benchmarks_positive_eligible_pairs=145)
    counts_match=all(inv[k]==v for k,v in expected_counts.items())
    sparse=result("sparse_caps.json")
    reliab=result("reliability.json")
    base=result("baselines.json")
    receipts=result("c2e_receipts.json")
    m1=result("measurement_definitions.json")
    deps={relative(HERE/n):sha(HERE/n) for n in ("reliability.py","cell_scoring.py")}
    common={**reliab["inputs"],**deps}
    measurements={
        "M0":row("baselines.py","inventory.json","MATCH" if counts_match else "MISMATCH",
                 {k:v for k,v in inv.items() if k!="inputs"},inv["inputs"],expected=expected_counts),
        "M1":row("source_audit.py","measurement_definitions.json",m1["status"],m1["values"],m1["inputs"],note=m1["note"]),
        "M2":row("baselines.py","baselines.json",base["M2"]["status"],base["M2"]["values"],
                 {**common,"official_model_sha256":base["official_model"]["sha256"]},adapter_gate=base["adapter_gate"],
                 reference_displayed=base["M2"]["reference_displayed"], reference_absolute_differences=base["M2"]["reference_absolute_differences"]),
        "M3":row("sparse_caps.py","sparse_caps.json","MEASURED",sparse["caps"],{**sparse["inputs"],
                 "cell_scoring_sha256":sparse["cell_scoring_sha256"],"sparse_plan_sha256":sparse["sparse_plan_sha256"]},
                 design_check=sparse["design_check"],reference_v14=sparse["reference_v14"]),
        "M5":row("reliability.py","reliability.json","MEASURED",reliab["reliability"],common,
                 wrapper_gate=reliab["wrapper_gate"], response_count=reliab["evaluation_responses_per_method_budget"]),
        "M6":row("baselines.py","baselines.json",base["M6"]["status"],base["M6"]["values"],common,
                 adapter_gate=base["adapter_gate"])}
    measurements["M4"]=row("c2e_receipts.py","c2e_receipts.json",receipts["status"],
                           receipts.get("values",receipts))
    for key in ("M2", "M6"):
        measurements[key]["inputs"].update(base["benchmark_sum_evidence"])
    mismatched=[k for k,v in base["M2"]["reference_absolute_differences"].items() if v>base["M2"]["tolerance"]]
    if mismatched:
        measurements["M2"]["reuse_submitted_row"]={"status":"DEPENDS_ON_MISMATCH","fields":mismatched}
    records={key:measurements[key] for key in sorted(measurements)}
    source_checks=result("source_preregistration.json")["checks"]
    base_commit=next(r["actual"] for r in source_checks if r["name"]=="origin/main")
    output=dict(schema_version=1,base_commit=base_commit,repro_gate=repro,measurements=records)
    (HERE/"RESULTS_v21.json").write_text(json.dumps(output,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run",required=True,type=Path)
    collect(parser.parse_args().run)
