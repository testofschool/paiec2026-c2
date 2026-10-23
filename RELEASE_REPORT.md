# C2 public release report

Local reproduction and package acceptance: PASS. Both splits ran once in the same fresh virtual environment. The default complete comparison reported 25 PASS, 0 FAIL and 0 BLOCKED. The registered ZIP was rebuilt exactly; the official default full checker exited 0. Protected originals and numerical sources remain unchanged. Final byte inventory and final full-tree scrub are detached records beside this release directory, so they can bind the completed report without a self-referential digest.

2026-10-22 local packaging status: The 25-check PASS above describes the historical 2026-10-10 numerical reproduction. Direct user approval limited the release_preflight.py repair to two helper defects. Before installation, the retained pre-v10.7 copy reproduced exit 1 with exactly seven findings (P1, P2, P3, P3, P4, P5, P6); after installation, the complete v10.7 preflight with the final identified PDF passed with exit 0. Scientific sources, registered expectations, tolerances, and ZIP bytes remain unchanged. GitHub publication, the selected Codabench submission ID, and external uploads remain human actions; no external publication or submission occurred in this work.

Report assembled at 2026-10-10T14:35:26.723246+09:00. This is a local release package. Local numbers are not hidden-test scores. No external publication or submission occurred.

## Start and immutable registration

The start trigger was `c2e/REPORT.md`, created at 2026-10-10T13:39:58.371983+09:00 after a terminal dependency-hash mismatch before Step 0. Its SHA256 is `9a86fc11335d332ba1826bb91d3116fbe8b15cf9957185925d2a4469cf5d87b8`. C2E coverage and all five experiment gates remained UNRUN; no failed coverage value is inferred. The public target is C2. The report condition preceded the approved 2026-10-21 00:00 KST time cutoff.

Release registration was written at 2026-10-10T13:40:53.491716+09:00, before any release rerun. `verification/release_start.json` SHA256: `85d1f7e816c3fcc9d81496c314dc019a0b2309756fb4a709d50061ba6ae357a4`. It records 0 release reruns before registration.

All split2 expected values were read at full precision from the existing frozen `c2d2/summary.json`, SHA256 `15504d62061413e8ab560b92d8b98b8cbb16f7afa3ee20db7f44e4ec4684c90a`. They were never taken from this rerun. `verification/expected_values.json` was frozen before rerunning, SHA256 `63011992452eeec465fef451d0024a50f1e11060836df6b4da072c5be92a7132`. The tolerance remains 1e-6; all package hashes remain exact.

## Approved deviations and qualifications

The specification mistakenly gave split2 expected values rounded to five decimal places; they were corrected to the raw values in the frozen summary.json with author approval on 2026-10-10.

The author corrected the scrub specification on 2026-10-10 by removing P006/P007 from the unconditional blacklist. This is a specification correction, not an exception. The remaining private-path/account patterns and credentials remain forbidden. Original prior and registered ZIP bytes are unchanged. The single required code-writing/review disclosure appears exactly in README; its two literal names are not repeated elsewhere outside the prior. The final scope proof is in `verification/scrub_conflicts.json`.

The author approved CPython 3.10.11, numpy 2.2.6, pandas 2.3.3, pyarrow 24.0.0 and scipy 1.15.3 as the one reproduction lock on 2026-10-10. (a) Split2 producing library versions have no recorded binding and remain UNVERIFIABLE; this lock comes from the existing report's version record. (b) Split3 was produced in a different recorded environment in `c2b0/offline_dependency.json`: Python 3.12.14, numpy 2.5.3, pandas 3.0.6, pyarrow 25.0.1 and scipy 1.18.1. Restored historical package records failed integrity verification and were not used as a verified runtime. Both new splits used the one approved lock and passed unchanged tolerances. No second environment was added.

The historical ZIP is reconstructed using the immutable original fitted prior and member metadata. Fresh training separately recomputes six fold priors, variance parameters and an all-public prior from public tables; that fresh JSON is retained externally and is not substituted into the historical hash target. A direct historical producing-builder process receipt was unavailable; actual new exact-byte reproduction provides the package comparison evidence.

The official checker runs in its default full mode and exercises prediction. Its optional acquisition helper returns without execution when `labeling.py` is absent; the registered four-member ZIP has no such module. Optional acquisition-hook execution is therefore SKIPPED/N/A, not claimed as tested. The registered split evaluations still execute their original acquisition simulation. No extra experiment or archive member was added.

The official checker is supplied independently, rather than copied under the release's MIT license. Its revision and source hashes are pinned. Only the generated temporary ZIP path was normalized in the published checker text; the external raw log SHA256 is retained in `verification/official_checker.json`.

Individual virtualenv/package-install durations and peak memory were not separately measured. Complete elapsed fresh-run intervals and actual measured stage durations are recorded below. The training interval includes observation lag; it is not claimed to be exact process-only CPU time. A detached complete inventory covers this report's own hash and size; putting that digest inside the same report would be self-referential.

## Fresh-copy execution and environment

A new external temporary directory and copied repository were created; a new isolated virtual environment was installed once. CPython/runtime imports verified the approved five versions, with no inherited system site-packages. `verification/fresh_runtime.json` and `verification/installation.log` preserve the evidence. Installation used only the eight exact entries in `requirements.lock`. No retry occurred.

Offline preparation copied and verified 652 resident public files, totaling 5,080,479,573 bytes, from measurement-db revision `54074453da7b9911be0f48e4c560be547bc84d21`. It took 19.810293374583125 seconds. No dataset network retrieval or redistribution of data tables occurred. The user-side authorized-access download prerequisite is documented separately in README. All generated raw tables, per-pair CSVs, fold artifacts and raw run logs remain outside this source release.

All scientific Python sources, shell wrappers and lock bytes in the delivered tree match the tested fresh copy and initial source snapshot: 28 registered paths. Documentation and measured evidence were finalized after execution. `verification/post_run_integrity.json` records that binding, plus the six protected original files and immutable expectation/prior copies. No original was edited.

Environment variables used the fresh external run directory and its interpreter; inherited `PYTHONPATH` and `PYTHONHOME` were unset. The supplied resident public-data root and official checker root were set separately. Each shell wrapper set numerical threads to 1 and kept bytecode outside the repository. Actual commands and exit states follow; paths use the documented environment variable names for portability.

| Command actually executed | Start KST | End KST | Wall seconds | Exit |
|---|---|---|---:|---:|
| `python3.10 -m venv "$PAIEC_RUN_DIR/venv"` | not separately recorded | not separately recorded | UNMEASURED | 0 |
| `"$PAIEC_PYTHON" -m pip --disable-pip-version-check install --only-binary=:all: -r requirements.lock` | not separately recorded | not separately recorded | UNMEASURED | 0 |
| `./scripts/prepare_data.sh "$PAIEC_PUBLIC_DATA_DIR"` | 2026-10-10T14:07:39.681551+09:00 | not separately recorded | 19.810293374583125 | 0 |
| `"$PAIEC_PYTHON" -B verification/verify_identifier_sources.py --data "$PAIEC_RUN_DIR/data" --out "$PAIEC_RUN_DIR/identifier_sources.json"` | 2026-10-10T14:08:21.919819+09:00 | not separately recorded | UNMEASURED | 0 |
| `./scripts/train_prior.sh` | 2026-10-10T14:08:46.625354+09:00 | 2026-10-10T14:19:38.859582+09:00 | 652.234228 | 0 |
| `./scripts/evaluate_split2.sh` | 2026-10-10T14:19:38.926690+09:00 | 2026-10-10T14:24:05.853218+09:00 | 266.92500645900145 | 0 |
| `"$PAIEC_PYTHON" -B verification/compare_expected.py --split split2 --metrics-only --results "$PAIEC_RUN_DIR"/eval_split2/results.json --json-output "$PAIEC_RUN_DIR"/compare_split2.json --text-output "$PAIEC_RUN_DIR"/compare_split2.txt` | 2026-10-10T14:24:10.486657+09:00 | 2026-10-10T14:24:10.528008+09:00 | 0.040899042040109634 | 0 |
| `./scripts/evaluate_split3.sh` | 2026-10-10T14:24:18.876184+09:00 | 2026-10-10T14:28:48.373661+09:00 | 269.4959771670401 | 0 |
| `"$PAIEC_PYTHON" -B verification/compare_expected.py --split split3 --metrics-only --results "$PAIEC_RUN_DIR"/eval_split3/results.json --json-output "$PAIEC_RUN_DIR"/compare_split3.json --text-output "$PAIEC_RUN_DIR"/compare_split3.txt` | 2026-10-10T14:28:51.470208+09:00 | 2026-10-10T14:28:51.518080+09:00 | 0.04741662507876754 | 0 |
| `./scripts/build_zip.sh` | 2026-10-10T14:28:58.388241+09:00 | 2026-10-10T14:28:59.099235+09:00 | 0.7097270409576595 | 0 |
| `./scripts/official_checker.sh` | 2026-10-10T14:29:02.073528+09:00 | 2026-10-10T14:29:02.835882+09:00 | 0.7611449593678117 | 0 |
| `"$PAIEC_PYTHON" -B verification/compare_expected.py --results "$PAIEC_RUN_DIR"/eval_split2/results.json --results "$PAIEC_RUN_DIR"/eval_split3/results.json --zip "$PAIEC_RUN_DIR"/dist/C2_r1.zip --json-output "$PAIEC_RUN_DIR"/compare_final.json --text-output "$PAIEC_RUN_DIR"/compare_final.txt` | 2026-10-10T14:29:09.937239+09:00 | 2026-10-10T14:29:09.986882+09:00 | 0.048953416757285595 | 0 |

The initial `cp -R . "$PAIEC_RUN_DIR/repository"` copied the release into a new temporary directory before virtualenv creation. Runtime import verification and public-identifier join were additional read-only prerequisites. The source-copy snapshot is `verification/fresh_copy_snapshot.json`. Both staged metrics-only gates exclude package checks explicitly; the default final comparison requires both splits and all three package hashes.

Hardware: Apple M1 Max, 10 logical CPUs, 64 GiB RAM; one numerical thread. Fresh-directory creation to final comparison: 1505.031802 seconds (about 25.1 minutes), including setup and observation gaps. Offline preparation start to final comparison: 1290.305331 seconds (about 21.5 minutes), excluding package installation. Prior-training observed interval: 652.234228 seconds. Split2: 266.92500645900145 seconds. Split3: 269.4959771670401 seconds. ZIP build: 0.7097270409576595 seconds. Official checker: 0.7611449593678117 seconds. See `verification/run_timing.json` for timing qualifications and exact stage records.

One fresh-copy test, one package-installation session, one prior-training invocation, one split2 invocation, one split3 invocation, one ZIP build and one official checker invocation occurred. No automatic retry, new experiment, model download, remote creation, push or competition submission occurred in the release work. C2E is separate and remains stopped.

## Numerical results

Both completed evaluations contain 145 eligible benchmarks and 13,023 unique raw subject/benchmark pairs. All finite MAP estimates remain in variance pooling, including the three nonconverged maxiter-500 fits (`babilong`, `bridging_gap`, `monkey_power_laws`): 163 fits, 160 optimizer successes. No convergence filter or increased iteration limit was substituted.

| Split | Metric | Registered | Fresh observed | Absolute difference | Decision |
|---|---|---:|---:|---:|---|
| split2 | C2_ALC | 0.18487910654403214 | 0.18487910654403214 | 0.0 | PASS |
| split2 | frozen_ALC | 0.2015333932758017 | 0.20153339327580172 | 2.7755575615628914e-17 | PASS |
| split2 | C2_B0 | 0.24893649649887992 | 0.24893649649887994 | 2.7755575615628914e-17 | PASS |
| split3 | C2_ALC | 0.1848401766 | 0.18484017662654537 | 2.6545377007636262e-11 | PASS |
| split3 | C2_B0 | 0.2488973551 | 0.24889735512042893 | 2.042893632037135e-11 | PASS |
| split3 | C2_B31 | 0.1468372469 | 0.1468372469286715 | 2.8671509610944668e-11 | PASS |

Maximum metric difference: 2.8671509610944668e-11. Each staged comparison was 15 PASS, 0 FAIL and 0 BLOCKED. The split2 gate ended at 14:24:10.528008 KST before split3 began at 14:24:18.876184 KST; the split3 gate preceded package building. Exact full raw comparison output is pasted without modification:

```text
status=PASS
staged_scope=full_both_splits_and_package
package_checks=REQUIRED
PASS=25 FAIL=0 BLOCKED=0
PASS registration.expected_file actual=63011992452eeec465fef451d0024a50f1e11060836df6b4da072c5be92a7132
PASS registration.expected_sha256 expected=63011992452eeec465fef451d0024a50f1e11060836df6b4da072c5be92a7132 actual=63011992452eeec465fef451d0024a50f1e11060836df6b4da072c5be92a7132
PASS registration.start_file actual=85d1f7e816c3fcc9d81496c314dc019a0b2309756fb4a709d50061ba6ae357a4
PASS registration.start_expected_sha256 expected=63011992452eeec465fef451d0024a50f1e11060836df6b4da072c5be92a7132 actual=63011992452eeec465fef451d0024a50f1e11060836df6b4da072c5be92a7132
PASS registration.release_target expected=C2 actual=C2
PASS registration.release_reruns_before_registration expected=0 actual=0
PASS registration.tolerance expected=1e-06 actual=1e-06
PASS registration.hash_tolerance expected=exact actual=exact
PASS observed.file.0 actual=0bab18b3b4117844ed5ac6814f7c9a413ed77309e605369849c8062da61f8c83
PASS observed.schema_version.0 expected=1 actual=1
PASS observed.file.1 actual=1d5c4f029ef325e8221a62d9ad42196b5e350416c78ad72cbffd86049d787790
PASS observed.schema_version.1 expected=1 actual=1
PASS split2.C2_ALC expected=0.18487910654403214 actual=0.18487910654403214 absolute_difference=0.0 tolerance=1e-06
PASS split2.frozen_ALC expected=0.2015333932758017 actual=0.20153339327580172 absolute_difference=2.7755575615628914e-17 tolerance=1e-06
PASS split2.C2_B0 expected=0.24893649649887992 actual=0.24893649649887994 absolute_difference=2.7755575615628914e-17 tolerance=1e-06
PASS split2.coverage.benchmarks expected=145 actual=145
PASS split2.coverage.pairs expected=13023 actual=13023
PASS split3.C2_ALC expected=0.1848401766 actual=0.18484017662654537 absolute_difference=2.6545377007636262e-11 tolerance=1e-06
PASS split3.C2_B0 expected=0.2488973551 actual=0.24889735512042893 absolute_difference=2.042893632037135e-11 tolerance=1e-06
PASS split3.C2_B31 expected=0.1468372469 actual=0.1468372469286715 absolute_difference=2.8671509610944668e-11 tolerance=1e-06
PASS split3.coverage.benchmarks expected=145 actual=145
PASS split3.coverage.pairs expected=13023 actual=13023
PASS package.model.py expected=14ed10f59580da8d25deb41eb4cf5d945b94f31aacf7e995f2cccc424e2756d8 actual=14ed10f59580da8d25deb41eb4cf5d945b94f31aacf7e995f2cccc424e2756d8
PASS package.frozen_model.py expected=1d84ecb67c8b772a3719078bf2ca067d2bb0802ba36489e45181d4886bd4dcc6 actual=1d84ecb67c8b772a3719078bf2ca067d2bb0802ba36489e45181d4886bd4dcc6
PASS package.C2_r1.zip expected=70ff16e31d76195fc07c487a446c0a17f3f2fd63f234d81035f05e9f7e6ae31d actual=70ff16e31d76195fc07c487a446c0a17f3f2fd63f234d81035f05e9f7e6ae31d

```

## Numerical source and integrity evidence

`src/c2/model.py`, `src/irt_shrink/model.py` and `src/irt_shrink/train_prior.py` are exact byte copies. Original numerical functions/constants, target and 1PL fitting statements, item-weighted variance pooling, fixed optimizer options and split3 seed expression remain unchanged in the extracted helpers. Only portable CLI/path/output/provenance/residency handling surrounds these blocks. `verification/source_diffs.txt` records 30 zero-change byte/text/AST comparisons; `src/source_manifest.json` and `verification/integration_review.json` provide their source bindings.

The verification utilities passed their isolated synthetic checks before this reproduction: comparator 30 PASS; scrub scanner 47 PASS; receipt/CLI provenance guards 16 PASS. These are verification checks, not additional scientific experiments. Actual numerical reproduction and static source equivalence are reported separately.

Independent read-only execution review verified the input/source/artifact bindings, completed score checkpoints, registered numerical differences, stage chronology and ZIP member metadata. All 652 input hashes, 17 scientific sources and 14 evaluation artifact bindings remain consistent. `verification/independent_execution_review.json` and `verification/post_run_integrity.json` preserve the final review. The six named protected originals retain their pre-run exact full hashes and sizes.

## Package and privacy evidence

The new ZIP has four original members in original order, fixed 1980 timestamps, original modes and compression semantics. Size is 386,770 bytes; SHA256 `70ff16e31d76195fc07c487a446c0a17f3f2fd63f234d81035f05e9f7e6ae31d`. Original model and frozen predictor hashes are exact, as the raw comparison shows. The archived prior SHA256 is `ebea4e925fa97a84d47ececce94b2c9bfc769020711500dfa83e0fbf1d1b1ff9` in both the source payload and delivered ZIP. `dist/C2_r1.zip` is a byte-exact copy of the new tested build.

All 2,544 literal prior hits (P006: 2,538; P007: 6) occur only in `a_full`/`a_name` dictionary keys, including public composite identity metadata. There are no matching JSON string values or non-identifier fields. Case-insensitive counts are 2,955 (2,911/44); these use the same public-key context. The immutable ZIP prior is byte-identical and duplicates this same audited content. All 2,629 matching identifiers join to hash-verified public subject rows across 163 tables, with 0 unmatched. No public identifier bytes were removed or encoded to hide them. Outside the prior, only the single exact author-mandated README disclosure remains; all other occurrences are 0.

The corrected post-execution scrub reports PASS: 0 forbidden hits, 0 blocked inputs, 0 errors, 76 resident files and 4 ZIP members scanned at that snapshot. Allowed author-name hit: pattern P900, `LICENSE`, content offset 32, count 1. Its full receipt is `verification/scrub_after_execution.json`. It predates final report/evidence assembly, so the final exact-tree scan is recorded separately in the detached sibling `paiec2026-c2.scrub.json`; that scan covers the completed report and every final file. It must report PASS with 0 forbidden hits and 0 blocked inputs before delivery.

Historical `verification/compare_preflight.*`, `verification/scrub_preflight.json`, `verification/packaging_review.json` and `verification/protected_integrity.json` preserve their earlier preparation snapshots. Their missing-output BLOCKED, old-policy FAIL or pre-approval HOLD values are superseded by the fresh full comparison, author correction, final integrity and final scrub records; they are not current acceptance outcomes. The privacy specification correction is explicitly retained rather than silently erasing its original conflict evidence.

## Complete file inventory

The detached sibling `paiec2026-c2.manifest.json` records the actual SHA256 and byte size of EVERY final release file, including `RELEASE_REPORT.md`, and binds the final scrub snapshot. Its own SHA256 and byte size are delivered separately. This avoids claiming an impossible self-contained hash of a file inside itself. The table below records all other final release files; this report's actual bytes/hash are in the detached inventory. No subsequent edit is allowed without recapturing the final inventory and scrub.

| File | Bytes | SHA256 |
|---|---:|---|
| `.gitignore` | 52 | `1ea9320ca3593d399057f005509a8d080ba61e4e98498cd5a4df221245e180cb` |
| `LICENSE` | 1070 | `79ce570e0403b5ae1c401f829ff1f56d96f1cdae1999cc40a0651c5fce6d1c68` |
| `README.md` | 7745 | `307dde810d443552a84e3d7b79d848858edc7b0c4aca2f6a467709cf37697d71` |
| `REPRODUCTION_NOTE.md` | 4300 | `9f05e3cd6386a6cbdd8117d5485206fd92afb315d04cbe0dd97f035494d74e4f` |
| `dist/C2_r1.zip` | 386770 | `70ff16e31d76195fc07c487a446c0a17f3f2fd63f234d81035f05e9f7e6ae31d` |
| `requirements.lock` | 368 | `189c35a0d8be6a25aab409b838926af9334d5bfef7594d5c9fa36737fb0d63e9` |
| `scripts/_common.sh` | 413 | `a5b78f17276c66d8c8b77e13ab7c92b79c12e52e76504ae3d9a5b543c0df3486` |
| `scripts/build_zip.sh` | 131 | `af7ef4ab1e59df8d28a8adad42035d433f3c6ba360f80391f1e31865af8ad03d` |
| `scripts/evaluate_split2.sh` | 210 | `08b1942f6da643d64fc06c3ecca6bcceaa8b02f8496478a05edd4af67b29ac85` |
| `scripts/evaluate_split3.sh` | 210 | `1eb5ca9a5da0b2fd7ab119ccdb31e128102c55d4d507735d8ac516ba4e8a7176` |
| `scripts/official_checker.sh` | 256 | `7cb62105099370846bcd8d8743436f1368b6d67521b084b9fafd022adf033025` |
| `scripts/prepare_data.sh` | 220 | `59f7d851b063d9ea604f510552ed1e2c5a92e88c8d831f375f40f999f9e8dd5d` |
| `scripts/train_prior.sh` | 151 | `a702a9fc8053b5b3ab6b7fbd235df1c8e9cb02b226d61d14ee5dca302a4be707` |
| `src/archive_payload/README.md` | 1111 | `84932dd52a371b94c12c1f33b9355968aeba4bc2bb48f479582f19347af6bb03` |
| `src/archive_payload/prior.json` | 4356734 | `ebea4e925fa97a84d47ececce94b2c9bfc769020711500dfa83e0fbf1d1b1ff9` |
| `src/build_zip.py` | 2593 | `d6941dc4f93733747e2bbc93d19fe5b1f15db71a9232a0d31163c73ec6776613` |
| `src/c2/__init__.py` | 35 | `bc625fa33c75b0506bc408af31591edd614b0b5f927605b05318069b4fbc245b` |
| `src/c2/model.py` | 11717 | `14ed10f59580da8d25deb41eb4cf5d945b94f31aacf7e995f2cccc424e2756d8` |
| `src/check_official.py` | 1528 | `67b96d0862cc2f8d352b5b9e8e4a7e6fc51a8460eec34c704902ee79e4417a54` |
| `src/corehelpers/__init__.py` | 35 | `bc625fa33c75b0506bc408af31591edd614b0b5f927605b05318069b4fbc245b` |
| `src/corehelpers/evaluation.py` | 9032 | `9cc9a87a993a47781f0de82c339820e712d8f1922c751b2574afdb553b1cab2a` |
| `src/corehelpers/io.py` | 3476 | `f95f91a95ce5a6bf7966106b6417726d00200a89f654b4d44fc5460cef50c172` |
| `src/corehelpers/measure.py` | 9717 | `0cfc9bb8076746697e96daed7833d52ac505b4b351029de650d9e1a2e2248694` |
| `src/corehelpers/protocol.py` | 308 | `e665df810d118115acfb98e7debdbbc3140191e983823bf46ef05d0acdcf4d1b` |
| `src/corehelpers/split3.py` | 145 | `6f27be76e9266bb4e6baf979eb31f1675a1dcc5fc26f98f093ec36c61e3124a0` |
| `src/evaluate.py` | 6885 | `3eec74a22d550b2ccdc25bd2fa97de36a0df55974f263d7e5923511f10e56f70` |
| `src/irt_shrink/__init__.py` | 35 | `bc625fa33c75b0506bc408af31591edd614b0b5f927605b05318069b4fbc245b` |
| `src/irt_shrink/model.py` | 7275 | `1d84ecb67c8b772a3719078bf2ca067d2bb0802ba36489e45181d4886bd4dcc6` |
| `src/irt_shrink/train_prior.py` | 6489 | `6403fc88dc879aaaa32eab883f31655c69bc392a3f82f4b7daec6bb68f2c9322` |
| `src/prepare_data.py` | 3977 | `42733a2b0a3450e3e9d3252752da69e8790dabd7f0ceff25dd6b63d88f40bc42` |
| `src/resident_files.py` | 1633 | `6063788832c8164c821963b8defd34957becd848aa5a52d35b2b68b088be3ad5` |
| `src/source_manifest.json` | 18352 | `555f778566467e4469e0b9b4e0422dd2fd11115f74b393cf0959564594379a0f` |
| `src/train.py` | 6418 | `882355181802192656ee902d9324c1c79cda5330ae63f10484ce750c3fb17622` |
| `verification/archive_payload_manifest.json` | 803 | `f4a89cd195b5b2b1537930fdf588e1a572d981389d0b13fd737f125750c524f5` |
| `verification/author_corrections.json` | 3850 | `babcb37c90de36dd6acdde6cf94d0e77d8f29472b7918b54c28066d1a6c50277` |
| `verification/compare_expected.py` | 17869 | `a3ce076cfffeb8949f3ba8dc2d9c067d3e35d23fa5726cc0238e29e097e2e94c` |
| `verification/compare_final.json` | 5068 | `706dc47ada242c55838322acf097d7f84a3acf5b4c5d4d8b00911501534bf6ec` |
| `verification/compare_final.txt` | 2704 | `56c2a69627541fb1a4680580c2bcc48e6c73c39bde2129922163d146404948bc` |
| `verification/compare_preflight.json` | 4404 | `6cea3c5e5223022cbf4f6b64dc47d8a204f7b7be526101769b61b06ef68c097c` |
| `verification/compare_preflight.txt` | 2186 | `42504cd7cc70b27d165e066af69fec0fbc2fbb1e2ec974094ef56c12ba14119a` |
| `verification/compare_split2.json` | 2979 | `3e12336a9159f45d72b5e8a1023bd71131f7479150a79ef8bc1b06574d7d907e` |
| `verification/compare_split2.txt` | 1550 | `ae6b01f412a75bb26b76139165177ae123b8d710ff32a4bd7a36bb7db027b1f6` |
| `verification/compare_split3.json` | 2972 | `f9ed364e9e3e4af6a5271d8146db972204399c0a8f85e16e2536e6058d6e1dbb` |
| `verification/compare_split3.txt` | 1543 | `909563e1e3f7ea40b1ad29acb678494b9cdc1403a0401d92076a40f115f8ef34` |
| `verification/data_provenance.json` | 8718 | `182080ce9ff958b784a120fa98a5a781db2940317d2837f1298daf5fcddb6450` |
| `verification/environment_provenance.json` | 14506 | `51cfa28aac3ef495b426697e7e229c8897a631d22ab50780f0c1c9325377571a` |
| `verification/evidence/MANIFEST.json` | 8295 | `47852cb135fafc4321c4d8e993ee4d1475f758fad5742806c461f37864010dd1` |
| `verification/evidence/archive_payload/frozen_model.py` | 7275 | `1d84ecb67c8b772a3719078bf2ca067d2bb0802ba36489e45181d4886bd4dcc6` |
| `verification/evidence/c2b0/REPORT.md` | 9010 | `cd2986617574a74a42a8de2183dd2485ed54991dd168f299717d791a6eb1951c` |
| `verification/evidence/c2d2/summary.json` | 211927 | `68c3773c96ff48b4ba50c3c74e5f1c5cdc84f9eb39b0ba77acc5590d271c3c68` |
| `verification/evidence/c2d2/test_c2.py` | 11080 | `1ed8d74438ae4aa851593493bd4c2fef144714dc02ed1924c4d3590b1afb26a0` |
| `verification/evidence/c2e/lex/LEXICAL_LOCK_20261010_v2.json` | 7190 | `e277469698a4c770b491fd8fc7e0c00d627789687c8035cb5be280395910fbad` |
| `verification/evidence/c2e/lex/outer_pair_deltas.csv` | 209864 | `40320f2b1dc2ca5583788371fc84457ef6bf3e99a5bde395a880541361b18720` |
| `verification/evidence/c2e/lex/outer_partial.csv` | 1733 | `69013d35812c6ccd11ac24f3a716fb4cef15265b53e337b81947d429ecabb8bd` |
| `verification/evidence/headroom/REPORT.md` | 228337 | `467389e3efce84710ee13864094c9c8409ed1bf768d20ec3015802dd9d64fb1d` |
| `verification/expected_values.json` | 1326 | `63011992452eeec465fef451d0024a50f1e11060836df6b4da072c5be92a7132` |
| `verification/fresh_copy_snapshot.json` | 8538 | `69d78113ae50fd00010f520ff17b86af6481fb6de1f1125f24e149a553d8fa9f` |
| `verification/fresh_run_commands.json` | 5271 | `9ac9fa6930bac6309a7c580b8ed61d1c1f68299cca86ab201032bac4429304eb` |
| `verification/fresh_runtime.json` | 238 | `a513ec9fd4323a081887c7b62df9c148fdf91399ea5b693a4b7a927798be6590` |
| `verification/fresh_training_summary.json` | 9331 | `9bff02f89ef569b899a57004a4ba81d13e32b0ba9de6584389f43e48261c7197` |
| `verification/hardware.json` | 273 | `62e40a53cfab3fa6002dbd3281eb1ddc0ba32950be0edfa163f1417f6d5b2206` |
| `verification/identifier_audit.json` | 3507912 | `88fc9004f63275b3299766f4d420f83ed47e9e9447101b6c77ded5b0460edfc1` |
| `verification/identifier_sources.json` | 1736190 | `18a38bed327dfe066a870b7ddcf3ae3a47c550f37b91897d237bda4982e68eb6` |
| `verification/independent_execution_review.json` | 11173 | `3427534615e548455903a8cf9d71e5a4fc2071e45873bd6e47c319004b2251fe` |
| `verification/installation.log` | 2089 | `3ebf93dfff459730f7100d63f3b606168f505d24f5633722398993bef9b60307` |
| `verification/integration_review.json` | 15212 | `d9357b58cef97fb075263c44088488c285076bbfd17d6b2011d3e9df06525e48` |
| `verification/official_checker.json` | 1300 | `88505b541cd7f2c64ddaf023b3b4514f72899bbb543992e2144f41eee59a3847` |
| `verification/official_checker.txt` | 69 | `855fd6df56763baef973c6b47dc602702ad163e1d66f43e22bb32f8a58b667fa` |
| `verification/offline_data_receipt.json` | 279 | `ab7d81297fa4697033c08dd4ec69f5bd958f2646fbb8d4d76d822d20878f2dbf` |
| `verification/packaging_review.json` | 6280 | `7476600c144e3946f8360d9876a4c81e651a7cc461d47a787741bc396f10f9ce` |
| `verification/post_run_integrity.json` | 31863 | `5801f4202bc11c5c4bb28527aba6688712458a1eb698bddd7bea4149ce83d500` |
| `verification/preparation_timing.json` | 394 | `a24f58ac5965bbf7fe6c6cec66826e20bf0991d3d46614138f6e90622137d727` |
| `verification/protected_integrity.json` | 1694 | `cbd681681d1d4660da47d553872fe0a6c140483f172028fcf0b63c52e9eeabbc` |
| `verification/public_input_manifest.json` | 124965 | `09d46c62efb511713af315e167322492d599cd768a72aa9baa7c6ab7dca75eba` |
| `verification/release_preflight.py` | 5876 | `6cb4d23025ed09892d5551538911b8099798432b4382964cab50cc015efc4e65` |
| `verification/release_start.json` | 660 | `85d1f7e816c3fcc9d81496c314dc019a0b2309756fb4a709d50061ba6ae357a4` |
| `verification/release_status.json` | 15054 | `d4fe15a9ba41b1f6e5013a9f3b28d00b7fe4e833df336d4a450726e2bdb793cd` |
| `verification/run_timing.json` | 5296 | `a0d46547578edf87583c61fb264da4f6b6cbb661d439880f477245a3a295ccfe` |
| `verification/scrub_after_execution.json` | 8623 | `3fb26dcafb309e1552e5bf6a9883a4b115a6607baf4aae95abe929ffc2845339` |
| `verification/scrub_conflicts.json` | 648521 | `eb3c2eb7fcf7112170671011c7f17a99b266bf4b316069f64f769957150adbf5` |
| `verification/scrub_policy_correction.json` | 3373 | `cf63a4c9e096c7ec8f8f4b6381c7691c4a2b396ef0b193ff8223591a2abe311c` |
| `verification/scrub_preflight.json` | 22735 | `cf183040ed1cd810579394ef7b09ed95db8e022e50c85ec924860b45229628f0` |
| `verification/scrub_scan.py` | 17683 | `48198285d80f1aa526846f89781e5278cc3d4a42754c097af186c8861c7399bc` |
| `verification/source_diffs.txt` | 3169 | `0c874c4e8b3e6c63f9621e3864aa658e9caa069b2f1885a1fb4de519198c31e0` |
| `verification/split2_results.json` | 278 | `0bab18b3b4117844ed5ac6814f7c9a413ed77309e605369849c8062da61f8c83` |
| `verification/split3_results.json` | 273 | `1d5c4f029ef325e8221a62d9ad42196b5e350416c78ad72cbffd86049d787790` |
| `verification/training_receipt.json` | 71863 | `68dc379e59e9ec1f4e9a4edfc0c9b869accd79692208b100673c49c543350dfe` |
| `verification/verification_review.json` | 6243 | `cc5fcdd753d7c9385a5ee15c30085606dcfc450777d959b6b10ac99a6378847a` |
| `verification/verify_identifier_sources.py` | 10476 | `065f3ff8a445f38683a1ec1683d7e83cc15b78c0e395cf5266cd172317a8f174` |
| `verification/zip_build.json` | 143 | `5b1f17e5b532cccd7c316fcf2a82f3e00ef7c7610709d12018aa4ef81887d533` |
| `RELEASE_REPORT.md` | See detached final manifest | See detached final manifest |
