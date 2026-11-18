"""Run the registered macOS split2 sequence and record wall time and peak RSS."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


def main():
    repo = Path(__file__).resolve().parents[2]
    base = repo.parent
    run = Path(os.environ.get("PAIEC_RUN_DIR", base / "run")).resolve()
    python = str(Path(os.environ.get("PAIEC_PYTHON", run / "venv/bin/python")).absolute())
    data = Path(os.environ["PAIEC_PUBLIC_DATA_DIR"]).resolve()
    out = base / "out"
    logs = out / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    if any((run / name).exists() for name in ("data", "artifacts", "eval_split2")):
        raise SystemExit("Use a fresh run directory")
    env = {**os.environ, "PAIEC_PYTHON": python, "PAIEC_RUN_DIR": str(run),
           "PYTHONDONTWRITEBYTECODE": "1"}
    stages = [
        ("prepare", ["./scripts/prepare_data.sh", str(data)]),
        ("identifiers", [python, "-B", "verification/verify_identifier_sources.py",
                         "--data", str(run / "data"), "--out", str(run / "identifier_sources.json")]),
        ("train", ["./scripts/train_prior.sh"]),
        ("evaluate", ["./scripts/evaluate_split2.sh"]),
        ("compare", [python, "-B", "verification/compare_expected.py", "--split", "split2",
                     "--metrics-only", "--results", str(run / "eval_split2/results.json"),
                     "--json-output", str(run / "compare_split2.json"),
                     "--text-output", str(run / "compare_split2.txt")])]
    records = []
    for stage, command in stages:
        log = logs / (stage + ".log")
        started = time.monotonic()
        with log.open("w") as stream:
            proc = subprocess.run(["/usr/bin/time", "-l", *command], cwd=repo, env=env,
                                  stdout=stream, stderr=subprocess.STDOUT)
        elapsed = time.monotonic() - started
        rss = re.search(r"(\d+)\s+maximum resident set size", log.read_text(errors="replace"))
        portable = [a.replace(str(data), "$PAIEC_PUBLIC_DATA_DIR").replace(python, "$PAIEC_PYTHON")
                    .replace(str(run), "$PAIEC_RUN_DIR") for a in command]
        records.append(dict(stage=stage, command=portable, exit=proc.returncode,
                            wall_seconds=elapsed, peak_rss_bytes=int(rss[1]) if rss else None))
        (out / "T1_stages.json").write_text(json.dumps(records, indent=2) + "\n")
        if proc.returncode:
            return proc.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
