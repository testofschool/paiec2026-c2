# PAIEC 2026 C2

Status: registration-machine (Apple M1 Max, 2026-10-10) fresh reproduction: 25 checks passed, 0 failed, 0 blocked. A 2026-10-22 fresh copy on other hardware (Apple M5 Max) rebuilt the ZIP, model and frozen predictor byte-exactly, reproduced frozen ALC and C2 B0 within 3e-11, and showed cross-machine variation of up to 2.8e-5 on the three refit-dependent C2 metrics (split2 C2 ALC, split3 C2 ALC, split3 C2 B31; details in REPRODUCTION_NOTE.md). The 1e-6 gate in compare_expected.py is the author's same-machine exactness check; a rerun on different hardware should expect differences of that order.

Requirements: CPython 3.10.11, requirements.lock (8 pins), PAIEC_PUBLIC_DATA_DIR (measurement-db public tables, 5,080,479,573 bytes), PAIEC_CHECKER_DIR, ≥ 13 GiB RAM (peak RSS 12.76 GB observed).

LLM coding assistants (Claude, Codex) were used for code writing and review; all numbers come from the scripts in this repository.

Method (six lines):
1. Use the frozen subject/benchmark prior and predictor without numerical changes.
2. Fit item offsets from acquisition observations of other full subject configurations.
3. Shrink offsets with the variance fitted on the other five benchmark folds.
4. Keep six deterministic outer folds and the original split2/split3 seeds.
5. Evaluate budgets 0, 1, 3, 7, 15, 31 on the disjoint evaluation half.
6. Average pair-level Brier curves over 13,023 pairs in 145 benchmarks.

Local numbers are not hidden-test scores.

Public inputs are obtained by the organizer using their own authorized access
to [measurement-db](https://huggingface.co/datasets/aims-foundations/measurement-db),
dataset revision `54074453da7b9911be0f48e4c560be547bc84d21`.
The release contains metadata, file digests and fitted model parameters, with
no redistributed data tables or credentials. An organizer with an installed
Hugging Face CLI can obtain the tables separately:

```sh
hf download aims-foundations/measurement-db --repo-type dataset \
  --revision 54074453da7b9911be0f48e4c560be547bc84d21 \
  --include '*/formatted_tables/benchmarks.parquet' \
            '*/formatted_tables/subjects.parquet' \
            '*/formatted_tables/items.parquet' \
            '*/formatted_tables/responses.parquet' \
  --local-dir "$PAIEC_PUBLIC_DATA_DIR"
```

This retrieval is a separate user-side prerequisite. The local acceptance
run uses existing resident public tables entirely offline. Preparation accepts
either the public `formatted_tables` layout or a flattened benchmark layout,
checks all 652 registered table hashes, and normalizes `responses.parquet` to
`response.parquet`. Only the 163 registered binary/item benchmarks are copied.

The official checker is supplied independently from
[the organizer's baseline](https://github.com/aims-foundations/paiec_baseline),
revision `82d330ddcdb16016a3ae9e048db7e588ba2c6a39`.
Set `PAIEC_CHECKER_DIR` to its local directory. The command verifies the exact
checker and helper digests before running its default full mode. The prediction
smoke test executes; the optional acquisition hook is skipped because the
registered archive contains no `labeling.py`. That separately supplied code is
not included under this release's MIT license.

Exact sequence from the
root of this repository, with CPython 3.10.11 available as
`python3.10`. Set `PAIEC_PUBLIC_DATA_DIR` and `PAIEC_CHECKER_DIR` to the local
prerequisites first. All generated files remain in an external run directory.

```sh
set -eu
export PAIEC_RUN_DIR="$(mktemp -d)"
cp -R . "$PAIEC_RUN_DIR/repository"
cd "$PAIEC_RUN_DIR/repository"
python3.10 -m venv "$PAIEC_RUN_DIR/venv"
export PAIEC_PYTHON="$PAIEC_RUN_DIR/venv/bin/python"
export PYTHONDONTWRITEBYTECODE=1
"$PAIEC_PYTHON" -m pip --disable-pip-version-check install --only-binary=:all: -r requirements.lock
./scripts/prepare_data.sh "$PAIEC_PUBLIC_DATA_DIR"
"$PAIEC_PYTHON" -B verification/verify_identifier_sources.py \
  --data "$PAIEC_RUN_DIR/data" --out "$PAIEC_RUN_DIR/identifier_sources.json"
./scripts/train_prior.sh
./scripts/evaluate_split2.sh
"$PAIEC_PYTHON" -B verification/compare_expected.py \
  --split split2 --metrics-only --results "$PAIEC_RUN_DIR/eval_split2/results.json"
./scripts/evaluate_split3.sh
"$PAIEC_PYTHON" -B verification/compare_expected.py \
  --split split3 --metrics-only --results "$PAIEC_RUN_DIR/eval_split3/results.json"
./scripts/build_zip.sh
./scripts/official_checker.sh
"$PAIEC_PYTHON" -B verification/compare_expected.py \
  --results "$PAIEC_RUN_DIR/eval_split2/results.json" \
  --results "$PAIEC_RUN_DIR/eval_split3/results.json" \
  --zip "$PAIEC_RUN_DIR/dist/C2_r1.zip"
"$PAIEC_PYTHON" -B verification/scrub_scan.py --root .
```

Use a fresh external directory for each stage sequence; the commands refuse
existing output directories. No automatic rerun or installation retry is part
of this procedure. Package installation is the sole network operation in the
local fresh-environment acceptance run.
Stop immediately on a failed split metric check. Both splits use this one
environment; changing the tolerance, expected values or environment is not part
of the procedure. Staged metric checks exclude package checks; the final default
comparison requires both splits and all three exact package hashes.

Measured on an Apple M1 Max with 64 GiB memory and one numerical thread: about
21.5 minutes from offline preparation to the final comparison, excluding package
installation and initial copying. Split2 took 266.925 seconds and split3 took
269.496 seconds. Allow approximately 20–30 minutes on comparable hardware once
prerequisites are available. Public inputs
occupy 5,080,479,573 bytes; allow at least 8 GiB additional free space for
training and intermediates, plus space for the virtual environment.

| Split | Metric | Registered expected value |
|---|---|---:|
| split2 | C2 ALC | 0.18487910654403214 |
| split2 | frozen ALC | 0.2015333932758017 |
| split2 | C2 B0 | 0.24893649649887992 |
| split3 | C2 ALC | 0.1848401766 |
| split3 | C2 B0 | 0.2488973551 |
| split3 | C2 B31 | 0.1468372469 |

Absolute tolerance is 1e-6. Model, frozen predictor and archival ZIP hashes
must match exactly. `verification/expected_values.json` was registered before
any release rerun; its SHA256 is
`63011992452eeec465fef451d0024a50f1e11060836df6b4da072c5be92a7132`.

Training recomputes the six outer-fold priors and variance fits from public
tables. Evaluation uses those fresh artifacts, without copying cached scores.
ZIP building reproduces the historical registered package using its original
fitted prior bytes and original member metadata. A newly refitted prior is
retained separately in the external artifacts directory; its JSON bytes are
not substituted into the historical hash comparison.
The fitted prior retains the public subject/model identifier keys verified
against the registered subject tables. Removing the two name patterns from
the scrub specification leaves private-path, account and credential checks active.

Exact copies and extracted numerical functions are listed in
`src/source_manifest.json`; privacy, data provenance and environment limitations
are recorded in `verification/`. A local package build is not an external
submission or publication.

## Entry notes

`frozen_model.py` is `src/irt_shrink/model.py` bundled unchanged and exec-loaded by `model.py`; its own `predict` is not the entry point.
The cache applies only to the same `labeled` object, and a new copy triggers refitting (approximately 8 ms/call at 775 labels).
Labels must be integer 0/1 and `benchmark_id` must be nonempty; other inputs silently reduce performance.
Extract the ZIP into an empty directory to load the bundled `frozen_model.py`, because `../irt_shrink/model.py` takes precedence.
