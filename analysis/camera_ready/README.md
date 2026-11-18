# Reproducing the v21 analyses

Use the parent release's README to prepare the 652 registered tables, fit the six priors, run the split2 evaluation and write its `compare_split2.json` with `verification/compare_expected.py --split split2 --metrics-only --results "$PAIEC_RUN_DIR/eval_split2/results.json" --json-output "$PAIEC_RUN_DIR/compare_split2.json"`. The v21 study uses the resulting training receipt and artifacts. The eight package versions for scoring are in the release's `requirements.lock`.

From the repository root, after those stages finish, the following commands regenerate the data-dependent evidence under `verification/evidence/camera_ready/`. Set `PAIEC_V14_ARCHIVE` to the v14 evidence archive to include its historical comparison. Omitting the option records that the reference was unavailable.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
analysis_dir=analysis/camera_ready
"$PAIEC_PYTHON" -B "$analysis_dir/baselines.py" inventory --run "$PAIEC_RUN_DIR"
"$PAIEC_PYTHON" -B "$analysis_dir/sparse_caps.py" --run "$PAIEC_RUN_DIR" --v14-archive "$PAIEC_V14_ARCHIVE"
"$PAIEC_PYTHON" -B "$analysis_dir/reliability.py" --run "$PAIEC_RUN_DIR" --with-baselines --scores-only
"$PAIEC_PYTHON" -B "$analysis_dir/baselines.py" summarize --run "$PAIEC_RUN_DIR"
"$PAIEC_PYTHON" -B "$analysis_dir/verify_scores.py" --run "$PAIEC_RUN_DIR"
"$PAIEC_PYTHON" -B "$analysis_dir/collect_results.py" --run "$PAIEC_RUN_DIR"
```

Generate the figure with a separate Python environment containing the scoring dependencies and Matplotlib. This run used Matplotlib 3.10.8.

```sh
"$PAIEC_PLOT_PYTHON" -B "$analysis_dir/reliability.py" --plot-only --run "$PAIEC_RUN_DIR"
```

The official empirical-mean predictor is included with its license. Its source revision and byte digest appear in `baselines.json`. M2 and M6 use the same acquisition and evaluation partitions as the calibration replay. M3 applies the subject cap first and then partitions the retained subjects using the published split2 procedure. Each cap therefore compares the methods on common cells, while changing the cap can also change a retained subject's cells. The v14 cap results use that archive's own protocol.

M1 has no measurement definition. The source audit and historical receipt inventory record the supplied documents and archives available at execution time. The v21 handoff archive includes `out/T0.json` with search coverage and `out/T7.json` with the base and local analysis commits. Use `out/FILES.json` to verify individual archive entries.

For the original directory layout (the clone in `repo/`, with sibling directories `run/` and `out/`), `run_split2.py` wraps the official commands with macOS RSS and wall-time recording. `render_report.py` creates the report after the local commit audit. `package_results.py` rebuilds and checks the patch, inventories the archived files, reads every archive member back and writes the outer SHA-256 file. Those packaging steps use the execution logs and before-run hashes retained alongside the clone.
