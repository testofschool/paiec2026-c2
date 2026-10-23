"""Join immutable prior identifier keys to hash-validated public subject rows."""
import argparse
from collections import Counter
import hashlib
import io
import json
import math
import os
from pathlib import Path
import stat
import sys


ROOT = Path(os.path.abspath(Path(__file__).parents[1]))
PRIOR_SHA256 = "ebea4e925fa97a84d47ececce94b2c9bfc769020711500dfa83e0fbf1d1b1ff9"
MANIFEST_SHA256 = "09d46c62efb511713af315e167322492d599cd768a72aa9baa7c6ab7dca75eba"
RESIDENCY_SHA256 = "6063788832c8164c821963b8defd34957becd848aa5a52d35b2b68b088be3ad5"
FROZEN_MODEL_SHA256 = "1d84ecb67c8b772a3719078bf2ca067d2bb0802ba36489e45181d4886bd4dcc6"
FIELDS = ("normalized_name", "harness", "reasoning_effort", "harness_version",
          "subject_features_extra")
PATTERNS = {
    "pattern_1": "".join(map(chr, (67, 108, 97, 117, 100, 101))),
    "pattern_2": "".join(map(chr, (67, 111, 100, 101, 120))),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key in an authoritative input")
        result[key] = value
    return result


def parse(data):
    return json.loads(data, object_pairs_hook=no_duplicate_keys)


def bootstrap_file(path):
    """Guard the first helper read without relying on that helper or traversal."""
    path = Path(os.path.abspath(path))
    current = Path(path.anchor)
    for index, part in enumerate(path.parts[1:]):
        current = current / part
        info = current.lstat()
        if getattr(info, "st_flags", 0) & 0x40000000 or stat.S_ISLNK(info.st_mode):
            raise ValueError("Bootstrap source must be resident without symbolic links")
        if index < len(path.parts) - 2 and not stat.S_ISDIR(info.st_mode):
            raise ValueError("Bootstrap parent must be a local directory")
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError("Bootstrap source must be a regular local file")
    return path


def matching_strings(prior):
    """Collect every matching JSON key or string value without saving its text."""
    records = []

    def inspect(text, path, location, member_index=None):
        literal = {label: text.count(token) for label, token in PATTERNS.items()}
        folded = {label: text.casefold().count(token.casefold())
                  for label, token in PATTERNS.items()}
        if not any(folded.values()):
            return
        role = None
        if location == "dictionary_key" and path in [("a_full",), ("a_name",)]:
            role = ("subject_configuration_identifier" if path[0] == "a_full"
                    else "normalized_model_name_identifier")
        records.append({"container": path, "location": location,
                        "source_member_index": member_index,
                        "string_sha256": sha(text.encode()), "text": text,
                        "literal_hits": literal, "casefold_hits": folded,
                        "role": role})

    def walk(value, path=()):
        if isinstance(value, dict):
            for index, (key, child) in enumerate(value.items()):
                inspect(key, path, "dictionary_key", index)
                walk(child, path + (key,))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, path + (index,))
        elif isinstance(value, str):
            inspect(value, path[:-1], "string_value")

    walk(prior)
    return records


def clean(value):
    # Same null/float-NaN/string normalization used by the producing table reader.
    return "" if value is None or (isinstance(value, float) and math.isnan(value)) else str(value).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    # Execute only this hash-pinned standard-library helper; no bytecode cache use.
    helper_path = ROOT / "src/resident_files.py"
    helper_bytes = bootstrap_file(helper_path).read_bytes()
    if sha(helper_bytes) != RESIDENCY_SHA256:
        raise ValueError("Local residency helper source changed")
    helper = {"__name__": "identifier_residency_helper"}
    exec(compile(helper_bytes, "resident_files.py", "exec"), helper)
    local_file, local_path = helper["local_file"], helper["local_path"]

    prior_path = local_file(ROOT / "src/archive_payload/prior.json")
    prior_bytes = prior_path.read_bytes()
    if sha(prior_bytes) != PRIOR_SHA256:
        raise ValueError("Immutable prior bytes changed")
    frozen = local_file(ROOT / "src/irt_shrink/model.py").read_bytes()
    if sha(frozen) != FROZEN_MODEL_SHA256:
        raise ValueError("Frozen identifier construction source changed")
    manifest_bytes = local_file(ROOT / "verification/public_input_manifest.json").read_bytes()
    if sha(manifest_bytes) != MANIFEST_SHA256:
        raise ValueError("Public input manifest changed")
    manifest, prior = parse(manifest_bytes), parse(prior_bytes)
    records = matching_strings(prior)
    if len(records) != 2629 or any(record["role"] is None for record in records):
        raise ValueError("Prior contains an unexpected identifier location")
    total_literal = Counter()
    total_folded = Counter()
    for record in records:
        total_literal.update(record["literal_hits"])
        total_folded.update(record["casefold_hits"])
    if dict(total_literal) != {"pattern_1": 2538, "pattern_2": 6}:
        raise ValueError("Prior literal occurrence count changed")
    if dict(total_folded) != {"pattern_1": 2911, "pattern_2": 44}:
        raise ValueError("Prior casefold occurrence count changed")

    source = local_path(args.data)
    output = local_path(args.out, missing_ok=True)
    if output.exists() or output == ROOT or ROOT in output.parents:
        raise ValueError("Use a fresh verification output outside the source release")
    if output == source or source in output.parents:
        raise ValueError("Keep verification output outside the public input directory")
    subject_files = []
    for entry in manifest["files"]:
        relative = Path(entry["path"])
        if len(relative.parts) != 2 or relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Unsafe public input manifest path")
        if relative.name != "subjects.parquet":
            continue
        path = local_file(source / relative)
        raw = path.read_bytes()
        if len(raw) != entry["size_bytes"] or sha(raw) != entry["sha256"]:
            raise ValueError("Public subject table hash mismatch: " + relative.as_posix())
        subject_files.append((entry, path))
    if len(subject_files) != 163:
        raise ValueError("Public subject table coverage differs from the fixed inventory")

    # This import is deliberately deferred until all authoritative byte checks pass.
    # Run this script only in the separately verified fresh reproduction environment.
    import pandas as pd

    targets = {(record["container"][0], record["text"]): record for record in records}
    joined = {key: [] for key in targets}
    row_count = 0
    for entry, path in subject_files:
        table_bytes = local_file(path).read_bytes()
        if len(table_bytes) != entry["size_bytes"] or sha(table_bytes) != entry["sha256"]:
            raise ValueError("Public subject table changed after admission")
        table = pd.read_parquet(io.BytesIO(table_bytes))
        columns = {field: (table[field].map(clean) if field in table else [""] * len(table))
                   for field in FIELDS}
        for row_index, values in enumerate(zip(*(columns[field] for field in FIELDS))):
            row_count += 1
            full, name = "|".join(values), values[0]
            for key in [("a_full", full), ("a_name", name)]:
                if key in joined:
                    joined[key].append({"path": entry["path"], "row_index": row_index})
    unmatched = []
    evidence = []
    for key, record in targets.items():
        item = {"container_json_pointer": "/" + key[0],
                "source_member_index": record["source_member_index"],
                "key_sha256": record["string_sha256"], "role": record["role"],
                "literal_hits": record["literal_hits"], "casefold_hits": record["casefold_hits"],
                "public_rows": joined[key], "public_row_count": len(joined[key])}
        evidence.append(item)
        if not joined[key]:
            unmatched.append({"container_json_pointer": item["container_json_pointer"],
                              "key_sha256": item["key_sha256"]})
    checked_files = [{"path": entry["path"], "sha256": entry["sha256"],
                      "size_bytes": entry["size_bytes"]} for entry, _ in subject_files]
    result = {"schema_version": 1, "status": "PASS" if not unmatched else "FAIL",
              "scope": "Exact string metadata membership; no response reads, fitting, or prediction",
              "prior_sha256": PRIOR_SHA256, "public_input_manifest_sha256": MANIFEST_SHA256,
              "frozen_model_sha256": FROZEN_MODEL_SHA256,
              "verifier_sha256": sha(local_file(Path(__file__)).read_bytes()),
              "runtime": {"python": sys.version.split()[0], "pandas": pd.__version__},
              "identifier_records": len(records), "literal_hits": dict(total_literal),
              "casefold_hits": dict(total_folded), "checked_subject_files": checked_files,
              "subject_rows_read": row_count, "unmatched_identifiers": unmatched,
              "matching_identifiers": evidence, "raw_identifier_strings_saved": False,
              "qualification": "Composite identifiers retain all public subject metadata fields, including descriptive identity notes; membership does not assert the resolved identity of an uncertain model."}
    if sha(local_file(prior_path).read_bytes()) != PRIOR_SHA256:
        raise ValueError("Immutable prior changed during verification")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "identifier_records": len(records),
                      "unmatched_identifiers": len(unmatched), "output_sha256": sha(output.read_bytes())}))
    return 0 if not unmatched else 1


if __name__ == "__main__":
    sys.exit(main())
