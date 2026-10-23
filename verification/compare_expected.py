"""Compare existing reproduction receipts against the immutable registration."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import stat
import sys

PINNED_EXPECTED_SHA256 = "63011992452eeec465fef451d0024a50f1e11060836df6b4da072c5be92a7132"
PINNED_TOLERANCE = 1e-6
EXPECTED_COVERAGE = {"benchmarks": 145, "pairs": 13023}
METRICS = {
    "split2": ("C2_ALC", "frozen_ALC", "C2_B0"),
    "split3": ("C2_ALC", "C2_B0", "C2_B31"),
}
PACKAGE_PATHS = {
    "model.py": "src/c2/model.py",
    "frozen_model.py": "src/irt_shrink/model.py",
    "C2_r1.zip": "dist/C2_r1.zip",
}


class DuplicateJSONKey(ValueError):
    """An ambiguous object cannot be used as a verification receipt."""


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateJSONKey("duplicate object key")
        value[key] = item
    return value


def resident_bytes(path):
    try:
        info = path.stat()
    except FileNotFoundError:
        return None, "BLOCKED", "missing_input"
    except OSError:
        return None, "BLOCKED", "metadata_unavailable"
    if getattr(info, "st_flags", 0) & 0x40000000:
        return None, "BLOCKED", "dataless_input"
    if not stat.S_ISREG(info.st_mode):
        return None, "FAIL", "input_not_regular_file"
    try:
        return path.read_bytes(), "PASS", None
    except OSError:
        return None, "BLOCKED", "content_unavailable"


def resident_json(path):
    data, status, reason = resident_bytes(path)
    if data is None:
        return None, None, status, reason
    digest = hashlib.sha256(data).hexdigest()
    try:
        value = json.loads(data, object_pairs_hook=unique_object)
    except DuplicateJSONKey:
        return None, digest, "FAIL", "duplicate_json_key"
    except (ValueError, UnicodeDecodeError):
        return None, digest, "FAIL", "invalid_json"
    if not isinstance(value, dict):
        return None, digest, "FAIL", "json_root_not_object"
    return value, digest, "PASS", None


def compare_number(expected, actual, tolerance):
    if actual is None:
        return "BLOCKED", None, "missing_metric"
    if isinstance(actual, bool) or not isinstance(actual, (int, float)):
        return "FAIL", None, "metric_not_numeric"
    if not math.isfinite(actual):
        return "FAIL", None, "metric_not_finite"
    difference = abs(actual - expected)
    return ("PASS" if difference <= tolerance else "FAIL"), difference, None


def selected_splits(split):
    if split == "both":
        return tuple(METRICS)
    if split in METRICS:
        return (split,)
    raise ValueError("invalid selected split")


def compare_metrics(expected, observed, tolerance, split="both"):
    checks = []
    for split in selected_splits(split):
        keys = METRICS[split]
        stage = observed.get(split) if isinstance(observed, dict) else None
        complete = isinstance(stage, dict) and stage.get("status") == "COMPLETE"
        values = stage.get("metrics", {}) if complete else {}
        values = values if isinstance(values, dict) else {}
        for key in keys:
            want = expected[split][key]
            actual = values.get(key)
            status, delta, reason = compare_number(want, actual, tolerance)
            if not complete:
                reason = "stage_not_complete"
            display_actual = actual
            if isinstance(actual, float) and not math.isfinite(actual):
                display_actual = str(actual)
            elif actual is not None and (isinstance(actual, bool) or not isinstance(actual, (int, float))):
                display_actual = {"invalid_type": type(actual).__name__}
            checks.append({"id": split + "." + key, "status": status,
                           "expected": want, "actual": display_actual,
                           "absolute_difference": delta, "tolerance": tolerance,
                           "reason": reason})
        coverage = stage.get("coverage", {}) if complete else {}
        coverage = coverage if isinstance(coverage, dict) else {}
        for key, want in EXPECTED_COVERAGE.items():
            actual = coverage.get(key)
            status = "BLOCKED" if actual is None else (
                "PASS" if type(actual) is int and actual == want else "FAIL")
            checks.append({"id": split + ".coverage." + key, "status": status,
                           "expected": want, "actual": actual,
                           "reason": "missing_coverage" if actual is None else None})
    return checks


def merge_results(receipts, split="both"):
    merged, checks = {}, []
    names = selected_splits(split)
    for index, receipt in enumerate(receipts):
        if receipt is None:
            continue
        for split in names:
            if split not in receipt:
                continue
            stage = receipt[split]
            if not isinstance(stage, dict):
                checks.append({"id": "observed." + split + ".shape", "status": "FAIL",
                               "reason": "split_not_object"})
                continue
            if split in merged:
                same = merged[split] == stage
                checks.append({"id": "observed." + split + ".duplicate." + str(index),
                               "status": "PASS" if same else "FAIL",
                               "reason": "identical_duplicate" if same else "conflicting_duplicate"})
            else:
                merged[split] = stage
    return merged, checks


def evaluate(root, observed_paths, expected_path, registration_path, package_paths,
             split="both", metrics_only=False):
    checks = []
    expected, digest, status, reason = resident_json(expected_path)
    checks.append({"id": "registration.expected_file", "status": status,
                   "actual": digest, "reason": reason})
    if expected is None:
        return finish(checks, split, metrics_only)
    checks.append({"id": "registration.expected_sha256",
                   "status": "PASS" if digest == PINNED_EXPECTED_SHA256 else "FAIL",
                   "expected": PINNED_EXPECTED_SHA256, "actual": digest})
    registration, registration_digest, status, reason = resident_json(registration_path)
    checks.append({"id": "registration.start_file", "status": status,
                   "actual": registration_digest, "reason": reason})
    if registration is None or digest != PINNED_EXPECTED_SHA256:
        return finish(checks, split, metrics_only)
    recorded = registration.get("expected_values_sha256")
    checks.append({"id": "registration.start_expected_sha256",
                   "status": "PASS" if recorded == digest else "FAIL",
                   "expected": digest, "actual": recorded})
    for key, want in (("release_target", "C2"), ("release_reruns_before_registration", 0)):
        actual = registration.get(key)
        checks.append({"id": "registration." + key,
                       "status": "BLOCKED" if actual is None else (
                           "PASS" if actual == want and type(actual) is type(want) else "FAIL"),
                       "expected": want, "actual": actual})
    tolerance = expected.get("tolerance")
    checks.append({"id": "registration.tolerance",
                   "status": "PASS" if type(tolerance) in (int, float) and tolerance == PINNED_TOLERANCE else "FAIL",
                   "expected": PINNED_TOLERANCE, "actual": tolerance})
    checks.append({"id": "registration.hash_tolerance",
                   "status": "PASS" if expected.get("hash_tolerance") == "exact" else "FAIL",
                   "expected": "exact", "actual": expected.get("hash_tolerance")})
    receipts = []
    for index, observed_path in enumerate(observed_paths):
        observed, observed_digest, status, reason = resident_json(observed_path)
        checks.append({"id": "observed.file." + str(index), "status": status,
                       "actual": observed_digest, "reason": reason})
        receipts.append(observed)
        if observed is not None:
            checks.append({"id": "observed.schema_version." + str(index),
                           "status": "PASS" if type(observed.get("schema_version")) is int and observed["schema_version"] == 1 else "FAIL",
                           "expected": 1, "actual": observed.get("schema_version")})
    observed, merge_checks = merge_results(receipts, split)
    checks.extend(merge_checks)
    checks.extend(compare_metrics(expected, observed, PINNED_TOLERANCE, split))
    if not metrics_only:
        for name, relative in package_paths.items():
            path = root / relative
            data, status, reason = resident_bytes(path)
            actual = None if data is None else hashlib.sha256(data).hexdigest()
            want = expected["package_sha256"][name]
            if actual is not None:
                status = "PASS" if actual == want else "FAIL"
            checks.append({"id": "package." + name, "status": status,
                           "expected": want, "actual": actual, "reason": reason})
    return finish(checks, split, metrics_only)


def finish(checks, split="both", metrics_only=False):
    counts = {s: sum(c["status"] == s for c in checks) for s in ("PASS", "FAIL", "BLOCKED")}
    status = "FAIL" if counts["FAIL"] else "BLOCKED" if counts["BLOCKED"] else "PASS"
    scope = ("full_both_splits_and_package" if split == "both" and not metrics_only else
             split + "_metrics_only" if metrics_only else split + "_metrics_and_package")
    return {"schema_version": 1, "status": status, "counts": counts,
            "staged_scope": scope, "selected_splits": list(selected_splits(split)),
            "package_checks": "EXCLUDED" if metrics_only else "REQUIRED",
            "full_acceptance_check": split == "both" and not metrics_only,
            "checks": checks, "experiment_reruns": 0}


def raw_text(result):
    lines = ["status=" + result["status"], "staged_scope=" + result["staged_scope"],
             "package_checks=" + result["package_checks"],
             " ".join(k + "=" + str(v) for k, v in result["counts"].items())]
    for check in result["checks"]:
        line = check["status"] + " " + check["id"]
        for key in ("expected", "actual", "absolute_difference", "tolerance", "reason"):
            if key in check and check[key] is not None:
                line += " " + key + "=" + str(check[key])
        lines.append(line)
    return "\n".join(lines) + "\n"


def self_test():
    assert compare_number(0.2, None, 1e-6)[0] == "BLOCKED"
    assert compare_number(0.2, 0.2 + 0.5e-6, 1e-6)[0] == "PASS"
    assert compare_number(0.2, 0.2 + 2e-6, 1e-6)[0] == "FAIL"
    assert compare_number(0.2, float("nan"), 1e-6)[0] == "FAIL"
    assert compare_number(0.2, True, 1e-6)[0] == "FAIL"
    expected = {split: {key: 0.2 for key in keys} for split, keys in METRICS.items()}
    partial = {"split2": {"status": "PARTIAL", "metrics": expected["split2"], "coverage": EXPECTED_COVERAGE}}
    assert all(c["status"] == "BLOCKED" for c in compare_metrics(expected, partial, 1e-6))
    full = {split: {"status": "COMPLETE", "metrics": dict(expected[split]), "coverage": dict(EXPECTED_COVERAGE)} for split in METRICS}
    assert all(c["status"] == "PASS" for c in compare_metrics(expected, full, 1e-6))
    full["split3"]["coverage"]["pairs"] = 13022
    assert finish(compare_metrics(expected, full, 1e-6))["status"] == "FAIL"
    full["split3"]["metrics"]["C2_B0"] = float("nan")
    json.dumps(compare_metrics(expected, full, 1e-6), allow_nan=False)
    class DatalessPath:
        def stat(self):
            return type("Info", (), {"st_flags": 0x40000000})()
        def read_bytes(self):
            raise AssertionError("dataless content must not be read")
    assert resident_bytes(DatalessPath())[1:] == ("BLOCKED", "dataless_input")
    merged, duplicate_checks = merge_results([{"split2": {"status": "COMPLETE"}}, {"split3": {"status": "COMPLETE"}}])
    assert set(merged) == set(METRICS) and not duplicate_checks
    assert merge_results([{"split2": {"status": "COMPLETE"}}, {"split2": {"status": "COMPLETE"}}])[1][0]["status"] == "PASS"
    assert merge_results([{"split2": {"status": "COMPLETE"}}, {"split2": {"status": "UNRUN"}}])[1][0]["status"] == "FAIL"
    class JSONBytesPath:
        def __init__(self, data):
            self.data = data
        def stat(self):
            return type("Info", (), {"st_flags": 0, "st_mode": stat.S_IFREG})()
        def read_bytes(self):
            return self.data
    ambiguous = [b'{"split2": {"status": "UNRUN"}, "split2": {"status": "COMPLETE"}}',
                 b'{"split2": {"metrics": {"C2_B0": 0, "C2_B0": 1}}}',
                 b'{"split2": {"coverage": {"pairs": 0, "pairs": 13023}}}',
                 b'{"split2": {"status": "UNRUN", "status": "COMPLETE"}}',
                 b'{"split2": {"metrics": {"C2_B0": 0, "C2_\\u00420": 1}}}']
    for data in ambiguous:
        value, digest, status, reason = resident_json(JSONBytesPath(data))
        assert value is None and status == "FAIL" and reason == "duplicate_json_key"
        assert digest == hashlib.sha256(data).hexdigest()
    value, _, status, _ = resident_json(JSONBytesPath(b'{"split2": {"status": "COMPLETE"}}'))
    assert status == "PASS" and value["split2"]["status"] == "COMPLETE"
    valid = {split: {"status": "COMPLETE", "metrics": dict(expected[split]),
                    "coverage": dict(EXPECTED_COVERAGE)} for split in METRICS}
    bad_two = json.loads(json.dumps(valid))
    bad_two["split2"]["metrics"]["C2_ALC"] = 0.2 + 2e-6
    bad_three = json.loads(json.dumps(valid))
    bad_three["split3"]["metrics"]["C2_B31"] = 0.2 + 2e-6
    bad_coverage = json.loads(json.dumps(valid))
    bad_coverage["split2"]["coverage"]["pairs"] = 13022
    stage_cases = [
        ("split2", {"split2": valid["split2"]}, "PASS"),
        ("split3", {"split3": valid["split3"]}, "PASS"),
        ("both", {"split2": valid["split2"]}, "BLOCKED"),
        ("split2", {"split3": valid["split3"]}, "BLOCKED"),
        ("split3", {"split2": valid["split2"]}, "BLOCKED"),
        ("split2", bad_two, "FAIL"),
        ("split3", bad_three, "FAIL"),
        ("split2", bad_coverage, "FAIL"),
        ("split2", bad_three, "PASS"),
    ]
    for split, observed, want in stage_cases:
        result = finish(compare_metrics(expected, observed, 1e-6, split), split, True)
        assert result["status"] == want and result["package_checks"] == "EXCLUDED"
        assert result["staged_scope"] == split + "_metrics_only"
        assert not result["full_acceptance_check"]
    pinned_path = Path(__file__).with_name("expected_values.json")
    pinned, _, status, _ = resident_json(pinned_path)
    assert status == "PASS"
    registration = JSONBytesPath(json.dumps({"expected_values_sha256": PINNED_EXPECTED_SHA256,
        "release_target": "C2", "release_reruns_before_registration": 0}).encode())
    observed = JSONBytesPath(json.dumps({"schema_version": 1, "split2": {
        "status": "COMPLETE", "metrics": pinned["split2"], "coverage": EXPECTED_COVERAGE}}).encode())
    class NoPackageRoot:
        def __truediv__(self, relative):
            raise AssertionError("package check attempted")
    staged = evaluate(NoPackageRoot(), [observed], pinned_path, registration, PACKAGE_PATHS,
                      split="split2", metrics_only=True)
    assert staged["status"] == "PASS" and staged["staged_scope"] == "split2_metrics_only"
    assert not any(check["id"].startswith("package.") for check in staged["checks"])
    try:
        evaluate(NoPackageRoot(), [observed], pinned_path, registration, PACKAGE_PATHS)
    except AssertionError as error:
        assert str(error) == "package check attempted"
    else:
        raise AssertionError("default full comparison omitted required package checks")
    print("SELF_TEST PASS 30")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--observed", default="output/results.json")
    parser.add_argument("--results", action="append", help="Repeat for separate existing split receipts")
    parser.add_argument("--expected", default="verification/expected_values.json")
    parser.add_argument("--registration", default="verification/release_start.json")
    parser.add_argument("--model", default=PACKAGE_PATHS["model.py"])
    parser.add_argument("--frozen-model", default=PACKAGE_PATHS["frozen_model.py"])
    parser.add_argument("--zip", default=PACKAGE_PATHS["C2_r1.zip"])
    parser.add_argument("--split", choices=("split2", "split3", "both"), default="both")
    parser.add_argument("--metrics-only", action="store_true",
                        help="Explicit staged metrics check; excludes package verification")
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--text-output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    root = args.root.resolve()
    observed_paths = [root / path for path in (args.results or [args.observed])]
    result = evaluate(root, observed_paths, root / args.expected,
                      root / args.registration, {"model.py": args.model,
                      "frozen_model.py": args.frozen_model, "C2_r1.zip": args.zip},
                      split=args.split, metrics_only=args.metrics_only)
    text = raw_text(result)
    print(text, end="")
    if args.json_output:
        args.json_output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    if args.text_output:
        args.text_output.write_text(text)
    return {"PASS": 0, "FAIL": 1, "BLOCKED": 2}[result["status"]]


if __name__ == "__main__":
    sys.exit(main())
