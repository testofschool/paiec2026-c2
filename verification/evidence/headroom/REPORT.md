# PAIEC leaderboard anchors and item-axis headroom

Generated 2026-10-09T04:40:25.160227+09:00 (KST). Measurement only; no method adoption.

## Result and interpretation

The saved public-pool run scores **13,023 raw subject–benchmark pairs** across **145 scored benchmarks**, with six held-out benchmark folds. The comparator ALC is **0.201469**. The table below is numerical local evidence. Official hidden-set scores, leaderboard scale conversion and formative-feedback noise remain **UNMEASURED**.

The user supplied a 2026-10-09 01:5x KST phase-29785 snapshot with leader 0.1172, runner-up 0.1483, third 0.1496 and organizer entry 0.1801, 33 visible entries and 145 participants. That leaderboard snapshot was not independently refreshed in this run. None of those values is established to share the scale of this local simulation. The organizer entry's method is unknown. Four human anchor submissions—official mean ×2 and frozen v2 ×2—are still needed to measure the scale relationship and noise. No Codabench submission or Git push occurred.

Oracle A is the exact floor for probabilities constant within each scored pair on this evaluation subset. Oracle B is a fitted, regularized 2PL diagnostic using unavailable evaluation labels. It is not a universal item-method ceiling or a proved minimum Brier. Finite optimizer convergence and regularization limit its interpretation. Feasible C and D are predefined probes; no new model, blend, calibration or hyperparameter was selected from these held-out results. No conclusion about reaching or missing official first place follows from local numbers alone.

**Oracle B convergence: 17/145 fitted benchmarks have unsuccessful optimizer termination flags.** All fitted scores, including failed termination cases, remain in the numerical table. B is a finite fitted oracle proxy; its score is not a validated universal item-axis ceiling.

## Authority and protocol

The [current official rules](https://aimslab.stanford.edu/competition) and current hosted configuration govern the competition. The [pinned official baseline](https://github.com/aims-foundations/paiec_baseline/tree/82d330ddcdb16016a3ae9e048db7e588ba2c6a39) supplies the anchor and interface. The outdated FAQ is excluded. The live rule verification and source/code distinctions are recorded in [headroom/protocol_audit.md](<$PAIEC_SOURCE_ROOT/headroom/protocol_audit.md>) and [headroom/spec_output_audit.md](<$PAIEC_SOURCE_ROOT/headroom/spec_output_audit.md>). This report does not claim an additional live rules audit.

Eligibility requires at least 80 distinct items in a raw subject–benchmark pair. Each raw pair receives floor-half acquisition items and the remaining evaluation items; all repeat responses to an item stay on the same side. Acquisition is a nested random item order at budgets 0, 1, 3, 7, 15 and 31. ALC weights are 0.1, 0.2, 0.2, 0.2, 0.2 and 0.1. Evaluation Brier includes every recorded evaluation response; pair scores are averaged equally. Acquisition reveals the first binary response after stable sorting by subject_id, item_id and trial (minimum trial order). This is a disclosed convention; chronological order is not established, and equivalence to hosted trial selection is unverified.

Fold assignment is `SHA256('fold:' + benchmark)[:8] mod 6`; each benchmark RNG is `default_rng(int(SHA256('split:' + benchmark)[:8], 16))`. These retain the frozen harness's fold/seed convention. Raw subjects are processed in sorted order and receive separate random permutations. New pair-specific RNG draws mean the item trajectories differ from the old shared benchmark split. The prior old CV 0.2025 is not reproduced by this changed protocol.

Benchmark-cluster percentile intervals resample scored benchmarks with replacement, retain all equally weighted raw pair differences in each sampled cluster, and use 2,000 replicates, seed 0, and the 2.5th/97.5th percentiles. Positive `Δ = frozen − method` means improvement. Intervals describe public benchmark heterogeneity; they do not estimate hidden-feedback noise.

## Inputs and provenance

Dataset `aims-foundations/measurement-db@54074453da7b9911be0f48e4c560be547bc84d21` is the public training corpus. The exact 163 local slugs match the pinned eligibility manifest. Preparation retained 68,631,488 binary responses, 31,750,924 raw subject–item cells and 3,679,304 item target records. Of 163 source benchmarks, 145 contain scored eligible pairs. No hidden data were inspected, and no inference API, remote embedding service or LLM was called.

Preserved benchmark/subject/response inputs: **489/489 digest checks PASS**, 2,064,539,922 bytes; errors: 0. The full source-table audit is [headroom/required_inputs_integrity.json](<$PAIEC_SOURCE_ROOT/headroom/required_inputs_integrity.json>). Full individual input hashes appear in the appendices.

### Protected frozen artifacts

| Artifact | Captured SHA256 | Bytes |
| --- | --- | --- |
| `irt_shrink/model.py` | `1d84ecb67c8b772a3719078bf2ca067d2bb0802ba36489e45181d4886bd4dcc6` | 7,275 |
| `irt_shrink/train_prior.py` | `6403fc88dc879aaaa32eab883f31655c69bc392a3f82f4b7daec6bb68f2c9322` | 6,489 |
| `irt_shrink/lobo_eval.py` | `3f29cd9b1f2a3034f42867c8f3eebb291325c9597c92d2e3ce1294b03549e197` | 7,428 |
| `irt_shrink/prior.json` | `1cc7b5a59223fc8d61e2e805c40063b672dcbce9043206720b30e42c5d66da55` | 4,356,693 |
| `irt_shrink/dist/irt_shrink.zip` | `6e7f6a4668a9b485e25350e889881c0b630e9d48ad25829ac80a0f0e5d9f2368` | 382,470 |

These are captured baseline hashes, not by themselves post-execution preservation checks. The frozen predictor is read-only; the local comparator runs its original algorithms with training-fold-only replicas of the prior. Literal all-public `prior.json` is recorded as a submission artifact and is not used for primary LOBO scoring because it would leak held-out public labels.

## T0 — anchors

Status: **PASS**. Fresh official clone at `82d330ddcdb16016a3ae9e048db7e588ba2c6a39`. Frozen ZIP prefix match: `True`. Anchor files are ready for human submission.

| Artifact | SHA256 | Bytes |
| --- | --- | --- |
| [empirical_mean_zip](<$PAIEC_SOURCE_ROOT/headroom/anchor_source/dist/empirical_mean.zip>) | `568323afb144fc02c9e3ba597f99c1e077bc09c7b67af58e9b9576ec584ef20c` | 1,935 |
| [frozen_irt_zip](<$PAIEC_SOURCE_ROOT/irt_shrink/dist/irt_shrink.zip>) | `6e7f6a4668a9b485e25350e889881c0b630e9d48ad25829ac80a0f0e5d9f2368` | 382,470 |
| [mean_model](<$PAIEC_SOURCE_ROOT/headroom/anchor_source/empirical_mean/model.py>) | `1e570641dd9b981baae988779b904ae58ad610a99bd44fb861647c60c93e935e` | 1,617 |
| [mean_readme](<$PAIEC_SOURCE_ROOT/headroom/anchor_source/empirical_mean/README.md>) | `c2766b1b069e408b61db56170e2ab96148ea3e8dcccb39c073298f8b1bdf3ed1` | 1,996 |
| [build_script](<$PAIEC_SOURCE_ROOT/headroom/anchor_source/tools/build_mean_zip.py>) | `cbea151a7a31cc5a78f293780211ce3c86f1c47062df7a2d99a8883362645a5f` | 907 |
| [checker](<$PAIEC_SOURCE_ROOT/headroom/anchor_source/check_submission_zip.py>) | `abe3cae05f4b18450b36edca60faef8a39bdf21821f30ff195c3cc45e177c646` | 27,121 |

```text
$ python3 tools/build_mean_zip.py
Wrote $PAIEC_SOURCE_ROOT/headroom/anchor_source/dist/empirical_mean.zip (1,935 bytes)
exit_code=0
```

```text
$ python3 check_submission_zip.py dist/empirical_mean.zip
OK: dist/empirical_mean.zip looks like a valid submission ZIP.
exit_code=0
```

## T1 — item inventory

**163/163 files**, **3,015,939,651 bytes**, **4,922,461 item-table rows**. Missing slugs: `[]`. All pinned remote digests verified. 29 verified existing files were hardlinked, saving 203,704,421 duplicate bytes; 134 unique completed files were directly downloaded with TLS verification (2,812,235,230 target bytes). Total retry-inclusive network bytes are UNMEASURED. Trace downloads: 0; response downloads: 0.

Each item's schema, row count, source URL and full digest are in [headroom/T1.json](<$PAIEC_SOURCE_ROOT/headroom/T1.json>); the compact inventory is [headroom/T1_items_inventory.tsv](<$PAIEC_SOURCE_ROOT/headroom/T1_items_inventory.tsv>). The public table's `content` field aliases to interface `item_content`. Identifier, grading criterion and verifier columns are not TF-IDF predictors.

## T2 — numerical results

All rows share the same pair splits and scoring cells. ALC and Brier are equally weighted pair means; lower is better. Fold wins compare each method's fold mean with the comparator.

The T2 probe labels differ from the initial strategy-axis labels: feasible T2 C maps to strategic axis A (cross-pair IRT), and feasible T2 D maps to strategic axis B (item text). Strategic axis C (acquisition policy) and axis D (pretrained LLM featurizer) were UNRUN in this specification.

| Method | ALC | B0 | B1 | B3 | B7 | B15 | B31 | Fold wins / 6 | ΔALC | 95% CI (frozen − method) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Frozen algorithm, fold-refit prior | 0.201469 | 0.249014 | 0.215340 | 0.201441 | 0.191050 | 0.184793 | 0.180429 | reference | 0.000000 | reference |
| A — oracle pair rate | 0.173856 | 0.173856 | 0.173856 | 0.173856 | 0.173856 | 0.173856 | 0.173856 | 6 | 0.027613 | [0.023685, 0.031163] |
| B — full-response 2PL oracle | 0.085897 | 0.085897 | 0.085897 | 0.085897 | 0.085897 | 0.085897 | 0.085897 | 6 | 0.115572 | [0.109405, 0.123869] |
| C — feasible cross-pair 1PL | 0.187020 | 0.266949 | 0.215283 | 0.191911 | 0.170799 | 0.154057 | 0.139154 | 3 | 0.014449 | [-0.003478, 0.026743] |
| D — static TF-IDF + prior | 0.379247 | 0.379247 | 0.379247 | 0.379247 | 0.379247 | 0.379247 | 0.379247 | 0 | -0.177778 | [-0.260601, -0.113260] |

### Local curves and benchmark-cluster intervals

These standalone figures show local per-budget scores and the local ALC difference intervals. They add no leaderboard-scale calibration or reach claim.

![Local PAIEC headroom curves and intervals](<$PAIEC_SOURCE_ROOT/headroom/headroom_curves.png>)

[headroom/headroom_curves.png](<$PAIEC_SOURCE_ROOT/headroom/headroom_curves.png>)

[headroom/headroom_curves.svg](<$PAIEC_SOURCE_ROOT/headroom/headroom_curves.svg>)

**Oracle B convergence: 17/145 fitted benchmarks have unsuccessful optimizer termination flags.** All fitted scores, including failed termination cases, remain in the numerical table. B is a finite fitted oracle proxy; its score is not a validated universal item-axis ceiling.

### First-place reach gate — HOLD

| Measured probe | Final local ALC | User-supplied official target | Scale calibration | Reach verdict |
| --- | --- | --- | --- | --- |
| Frozen algorithm, fold-refit prior | 0.201469 | 0.1172 | UNMEASURED | HOLD |
| A — oracle pair rate | 0.173856 | 0.1172 | UNMEASURED | HOLD |
| B — full-response 2PL oracle | 0.085897 | 0.1172 | UNMEASURED | HOLD |
| C — feasible cross-pair 1PL | 0.187020 | 0.1172 | UNMEASURED | HOLD |
| D — static TF-IDF + prior | 0.379247 | 0.1172 | UNMEASURED | HOLD |

The rank-rarity reference is 1/33 = **3.03%** of visible scored leaderboard entries. The 145 registered participants are not the scored-entry denominator and do not replace 33 in this calculation. This ratio is descriptive; it is not a measured probability of winning.

Official feedback noise is **UNMEASURED**, which requires the reach gate to remain **HOLD**. No axis is selected or adopted in this measurement run. C measures this particular content/features-proxy 1PL implementation under dense public-pool evidence; D measures this particular static TF-IDF/ridge/ability combination. Either implementation's weak or negative result would not reject the whole cross-pair or item-text axis. Full-run numbers above supersede partial-fold observations; an early fold alone establishes no full-run performance conclusion.

### D's explicit differences

D B0 Brier: **0.379247** versus frozen B0 **0.249014**; `frozen_B0 − D_B0 = -0.130234`. `frozen_ALC − D_ALC = -0.177778`, 95% benchmark-cluster CI [-0.260601, -0.113260]. D does not adapt after acquiring labels; its probabilities remain fixed, so its ALC equals its B0 Brier. No optional B0-only hybrid or blend was adopted.

### Overall same-item reuse

| Budget | Raw evaluation cell fraction | Raw pair mean | Visible-proxy pair mean |
| --- | --- | --- | --- |
| B0 | 0.000000 | 0.000000 | 0.000000 |
| B1 | 0.075871 | 0.354245 | 0.355736 |
| B3 | 0.104611 | 0.445368 | 0.448363 |
| B7 | 0.144503 | 0.557995 | 0.562739 |
| B15 | 0.197822 | 0.687584 | 0.694212 |
| B31 | 0.264632 | 0.804723 | 0.812515 |

Raw cell fraction counts distinct evaluation `(subject, item)` cells whose raw item ID is acquired by another raw subject. A pair's own acquisition/evaluation item sets are disjoint. Raw pair mean gives each pair equal weight; visible-proxy pair mean counts the content/features key actually available to C. These denominators differ; repeat trials do not inflate reuse.

### Fold 0 — 1,480 pairs, 25 scored benchmarks

| Method | ALC | B0 | B1 | B3 | B7 | B15 | B31 | ALC win | ΔALC | 95% CI (frozen − method) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Frozen algorithm, fold-refit prior | 0.182532 | 0.230991 | 0.190441 | 0.181976 | 0.173640 | 0.168756 | 0.164707 | reference | 0.000000 | reference |
| A — oracle pair rate | 0.158812 | 0.158812 | 0.158812 | 0.158812 | 0.158812 | 0.158812 | 0.158812 | 1 | 0.023721 | [0.020954, 0.032728] |
| B — full-response 2PL oracle | 0.056927 | 0.056927 | 0.056927 | 0.056927 | 0.056927 | 0.056927 | 0.056927 | 1 | 0.125606 | [0.084734, 0.137955] |
| C — feasible cross-pair 1PL | 0.179378 | 0.239814 | 0.194020 | 0.183243 | 0.169461 | 0.158065 | 0.144382 | 1 | 0.003155 | [-0.007832, 0.006245] |
| D — static TF-IDF + prior | 0.588270 | 0.588270 | 0.588270 | 0.588270 | 0.588270 | 0.588270 | 0.588270 | 0 | -0.405737 | [-0.478419, -0.101163] |

D B0 delta: `-0.357279`; D ALC delta: `-0.405737`.

| Budget | Raw evaluation cell fraction | Raw pair mean | Visible-proxy pair mean |
| --- | --- | --- | --- |
| B0 | 0.000000 | 0.000000 | 0.000000 |
| B1 | 0.011190 | 0.032148 | 0.032482 |
| B3 | 0.032450 | 0.090963 | 0.091613 |
| B7 | 0.070415 | 0.193586 | 0.195019 |
| B15 | 0.133345 | 0.353354 | 0.355630 |
| B31 | 0.218992 | 0.552372 | 0.554670 |

### Fold 1 — 4,852 pairs, 19 scored benchmarks

| Method | ALC | B0 | B1 | B3 | B7 | B15 | B31 | ALC win | ΔALC | 95% CI (frozen − method) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Frozen algorithm, fold-refit prior | 0.195066 | 0.264690 | 0.213317 | 0.192433 | 0.180287 | 0.172772 | 0.168353 | reference | 0.000000 | reference |
| A — oracle pair rate | 0.162825 | 0.162825 | 0.162825 | 0.162825 | 0.162825 | 0.162825 | 0.162825 | 1 | 0.032241 | [0.019027, 0.033475] |
| B — full-response 2PL oracle | 0.085569 | 0.085569 | 0.085569 | 0.085569 | 0.085569 | 0.085569 | 0.085569 | 1 | 0.109497 | [0.096199, 0.129129] |
| C — feasible cross-pair 1PL | 0.160338 | 0.282491 | 0.196176 | 0.160181 | 0.133937 | 0.116958 | 0.106383 | 1 | 0.034728 | [-0.004575, 0.038763] |
| D — static TF-IDF + prior | 0.392862 | 0.392862 | 0.392862 | 0.392862 | 0.392862 | 0.392862 | 0.392862 | 0 | -0.197796 | [-0.219502, -0.169250] |

D B0 delta: `-0.128172`; D ALC delta: `-0.197796`.

| Budget | Raw evaluation cell fraction | Raw pair mean | Visible-proxy pair mean |
| --- | --- | --- | --- |
| B0 | 0.000000 | 0.000000 | 0.000000 |
| B1 | 0.178769 | 0.829874 | 0.829979 |
| B3 | 0.199016 | 0.875351 | 0.875568 |
| B7 | 0.223127 | 0.891639 | 0.892114 |
| B15 | 0.262751 | 0.904868 | 0.905647 |
| B31 | 0.325473 | 0.922575 | 0.923556 |

### Fold 2 — 3,905 pairs, 21 scored benchmarks

| Method | ALC | B0 | B1 | B3 | B7 | B15 | B31 | ALC win | ΔALC | 95% CI (frozen − method) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Frozen algorithm, fold-refit prior | 0.202640 | 0.222349 | 0.219146 | 0.206660 | 0.195063 | 0.188831 | 0.184648 | reference | 0.000000 | reference |
| A — oracle pair rate | 0.177589 | 0.177589 | 0.177589 | 0.177589 | 0.177589 | 0.177589 | 0.177589 | 1 | 0.025051 | [0.024347, 0.033211] |
| B — full-response 2PL oracle | 0.084101 | 0.084101 | 0.084101 | 0.084101 | 0.084101 | 0.084101 | 0.084101 | 1 | 0.118539 | [0.105655, 0.130398] |
| C — feasible cross-pair 1PL | 0.196455 | 0.232063 | 0.225433 | 0.207198 | 0.187382 | 0.170585 | 0.151287 | 1 | 0.006185 | [-0.011342, 0.007310] |
| D — static TF-IDF + prior | 0.312629 | 0.312629 | 0.312629 | 0.312629 | 0.312629 | 0.312629 | 0.312629 | 0 | -0.109989 | [-0.281106, -0.092739] |

D B0 delta: `-0.090280`; D ALC delta: `-0.109989`.

| Budget | Raw evaluation cell fraction | Raw pair mean | Visible-proxy pair mean |
| --- | --- | --- | --- |
| B0 | 0.000000 | 0.000000 | 0.000000 |
| B1 | 0.040062 | 0.079126 | 0.079156 |
| B3 | 0.103374 | 0.215708 | 0.215784 |
| B7 | 0.187031 | 0.422257 | 0.422439 |
| B15 | 0.274776 | 0.671498 | 0.671853 |
| B31 | 0.349854 | 0.877014 | 0.877612 |

### Fold 3 — 1,201 pairs, 27 scored benchmarks

| Method | ALC | B0 | B1 | B3 | B7 | B15 | B31 | ALC win | ΔALC | 95% CI (frozen − method) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Frozen algorithm, fold-refit prior | 0.227665 | 0.277371 | 0.234192 | 0.226672 | 0.218772 | 0.215222 | 0.209560 | reference | 0.000000 | reference |
| A — oracle pair rate | 0.200827 | 0.200827 | 0.200827 | 0.200827 | 0.200827 | 0.200827 | 0.200827 | 1 | 0.026837 | [0.024019, 0.032127] |
| B — full-response 2PL oracle | 0.100642 | 0.100642 | 0.100642 | 0.100642 | 0.100642 | 0.100642 | 0.100642 | 1 | 0.127023 | [0.106481, 0.151792] |
| C — feasible cross-pair 1PL | 0.233065 | 0.320208 | 0.254387 | 0.238955 | 0.220337 | 0.200743 | 0.181601 | 0 | -0.005401 | [-0.013350, 0.004472] |
| D — static TF-IDF + prior | 0.338092 | 0.338092 | 0.338092 | 0.338092 | 0.338092 | 0.338092 | 0.338092 | 0 | -0.110427 | [-0.201740, -0.075620] |

D B0 delta: `-0.060721`; D ALC delta: `-0.110427`.

| Budget | Raw evaluation cell fraction | Raw pair mean | Visible-proxy pair mean |
| --- | --- | --- | --- |
| B0 | 0.000000 | 0.000000 | 0.000000 |
| B1 | 0.011384 | 0.056144 | 0.068136 |
| B3 | 0.030884 | 0.147497 | 0.172613 |
| B7 | 0.060066 | 0.273667 | 0.312154 |
| B15 | 0.099750 | 0.423418 | 0.478525 |
| B31 | 0.146845 | 0.564764 | 0.632081 |

### Fold 4 — 1,033 pairs, 30 scored benchmarks

| Method | ALC | B0 | B1 | B3 | B7 | B15 | B31 | ALC win | ΔALC | 95% CI (frozen − method) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Frozen algorithm, fold-refit prior | 0.229517 | 0.266810 | 0.233957 | 0.228498 | 0.224232 | 0.219495 | 0.215993 | reference | 0.000000 | reference |
| A — oracle pair rate | 0.207717 | 0.207717 | 0.207717 | 0.207717 | 0.207717 | 0.207717 | 0.207717 | 1 | 0.021800 | [0.017536, 0.026471] |
| B — full-response 2PL oracle | 0.115327 | 0.115327 | 0.115327 | 0.115327 | 0.115327 | 0.115327 | 0.115327 | 1 | 0.114190 | [0.098543, 0.143176] |
| C — feasible cross-pair 1PL | 0.230266 | 0.298732 | 0.256270 | 0.239860 | 0.220043 | 0.197085 | 0.177416 | 0 | -0.000749 | [-0.007781, 0.008511] |
| D — static TF-IDF + prior | 0.369419 | 0.369419 | 0.369419 | 0.369419 | 0.369419 | 0.369419 | 0.369419 | 0 | -0.139902 | [-0.232013, -0.085785] |

D B0 delta: `-0.102609`; D ALC delta: `-0.139902`.

| Budget | Raw evaluation cell fraction | Raw pair mean | Visible-proxy pair mean |
| --- | --- | --- | --- |
| B0 | 0.000000 | 0.000000 | 0.000000 |
| B1 | 0.055291 | 0.122336 | 0.126058 |
| B3 | 0.141509 | 0.304867 | 0.310997 |
| B7 | 0.255925 | 0.531778 | 0.541393 |
| B15 | 0.365344 | 0.726773 | 0.736951 |
| B31 | 0.443343 | 0.857335 | 0.865041 |

### Fold 5 — 552 pairs, 23 scored benchmarks

| Method | ALC | B0 | B1 | B3 | B7 | B15 | B31 | ALC win | ΔALC | 95% CI (frozen − method) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Frozen algorithm, fold-refit prior | 0.190760 | 0.253176 | 0.197101 | 0.190367 | 0.181527 | 0.173741 | 0.168949 | reference | 0.000000 | reference |
| A — oracle pair rate | 0.162698 | 0.162698 | 0.162698 | 0.162698 | 0.162698 | 0.162698 | 0.162698 | 1 | 0.028062 | [0.024246, 0.032605] |
| B — full-response 2PL oracle | 0.092003 | 0.092003 | 0.092003 | 0.092003 | 0.092003 | 0.092003 | 0.092003 | 1 | 0.098757 | [0.079712, 0.134312] |
| C — feasible cross-pair 1PL | 0.194197 | 0.274536 | 0.206647 | 0.193825 | 0.181156 | 0.170394 | 0.163388 | 0 | -0.003437 | [-0.007562, 0.001721] |
| D — static TF-IDF + prior | 0.278364 | 0.278364 | 0.278364 | 0.278364 | 0.278364 | 0.278364 | 0.278364 | 0 | -0.087604 | [-0.165941, -0.048499] |

D B0 delta: `-0.025188`; D ALC delta: `-0.087604`.

| Budget | Raw evaluation cell fraction | Raw pair mean | Visible-proxy pair mean |
| --- | --- | --- | --- |
| B0 | 0.000000 | 0.000000 | 0.000000 |
| B1 | 0.007945 | 0.065956 | 0.066053 |
| B3 | 0.021796 | 0.151790 | 0.152145 |
| B7 | 0.044928 | 0.230277 | 0.231163 |
| B15 | 0.084423 | 0.289038 | 0.290993 |
| B31 | 0.153939 | 0.357645 | 0.361579 |

## Estimators and predefined choices

A predicts the true evaluation-half response mean of each raw pair at every budget. B fits all available binary held-out-benchmark responses, including evaluation labels and subjects below scoring eligibility. Its logit is `d + a_i θ_s + offset_i`, algebraically `a_i(θ_s − b_i)`. Oracle θ prior centers use full-response pair logits clipped to [0.01,0.99] with variance 4; item offsets have variance 1, benchmark intercept prior variance 4, and log-discrimination variance 1 with discrimination bounded to [0.1,5]. All are predefined.

C fits MAP 1PL using only one acquired label at minimum trial order per budgeted item from all eligible pairs in the held-out benchmark. Eight-field visible subject dictionaries define ability states. Item keys hash supplied content + item_features + an empty interactors field, within benchmark; raw item IDs are not extra prediction features. Response-level interactors are intentionally ignored. The ability prior uses the original full/name/provider/global fallback: `mean_lam × ability_mean`, variance `tau2 + mean_lam² × ability_variance`. Item offsets have variance 1; intercept prior uses `mu_d, s2_d`. B0 uses only those priors. Unseen items after acquisition use the fitted benchmark intercept.

D targets the logit of each item's mean of subject-specific correct rates (each subject's repeat trials first averaged), clipped to [0.0001,0.9999]. Word TF-IDF uses unigrams/bigrams and at most 50,000 features. Vocabulary, IDF and ridge target fitting use only the five training folds. Ridge alpha=1, LSQR tolerance=1e-4 and max_iter=2000 are fixed. Prediction is `sigmoid(ability_mean + predicted_item_easiness)` with no additional held-out-selected ability scale, blend or calibration. D scores the same static probabilities at all six budgets. Training counts and fitted solver iterations are in [headroom/text_fits.json](<$PAIEC_SOURCE_ROOT/headroom/text_fits.json>).

D tokenizes the supplied serialized `content` string without prompt-only extraction. Markup, code and serialized field names can therefore contribute textual features. A narrow read-only input inspection is in [headroom/D_content_scope_review.json](<$PAIEC_SOURCE_ROOT/headroom/D_content_scope_review.json>); its sampled findings and scope limits are separated from predictive conclusions below.

### Canonical D fit metadata

| Fold | Training items | Test items | Features | Training nnz | LSQR iterations | Alpha |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 3,367,460 | 311,844 | 50000 | 607,082,904 | [269] | 1.0 |
| 1 | 3,178,717 | 500,587 | 50000 | 484,010,567 | [253] | 1.0 |
| 2 | 3,337,703 | 341,601 | 50000 | 603,750,668 | [278] | 1.0 |
| 3 | 2,725,063 | 954,241 | 50000 | 468,974,370 | [255] | 1.0 |
| 4 | 2,732,199 | 947,105 | 50000 | 475,418,109 | [256] | 1.0 |
| 5 | 3,055,378 | 623,926 | 50000 | 597,941,915 | [281] | 1.0 |

### Completed D checkpoint provenance

Text workers publish a complete per-fold CSV and fit JSON atomically before TEXT_DONE. The marker records row count and both SHA256 digests. The writer rechecks those digests, CSV rows and equality with the canonical six-fold text_fits.json metadata. A retained legacy fold is adopted only after its complete CSV passes the same checkpoint validation. These are completeness/integrity checks, not scientific quality claims.

| Fold | CSV rows | CSV SHA256 | Fit SHA256 | Marker/canonical match |
| --- | --- | --- | --- | --- |
| 0 | 1480 | `e369f15e8010dfe0605a1ec524c607ba4d5f23e4ed01fcd59d78082dca75f2f7` | `d4ed8a41e931f94128c16254132310d8c2d67bb24a90d52cf87ef24d18920ba8` | matching |
| 1 | 4852 | `291dababaaaf3a1551455048dcdd134d2ca6430e455f60f0e1816a5f85969222` | `a59edd725202148fb6e4f2a2cfce592df85ddb0ae34c272ea5baa49ae5142eff` | matching |
| 2 | 3905 | `14d66dded94f18c98f5ed86d1b8d9159b49ba8732294908a23f7a4ff81006781` | `6e77e91452282713cec334e4f60ab6200da81c51ccfa67e24e21a603bfde2a84` | matching |
| 3 | 1201 | `149a3f30df1c0f28bf86a51153ae9cfa8dffc0886fd3d330dba9906dafab4486` | `dbe8219be67ff3180db5326c255bd5e50a960b6a76b827fdcad23a22768cb7f7` | matching |
| 4 | 1033 | `4e1894789d3d483fb08df122e74f5d23ed3e96a2e888c42d17f4856ecf1f274e` | `d26410acec7b7afd6ad3dfe8b4a21c15b54159cec8cc70140a0aaed198345ff3` | matching |
| 5 | 552 | `2bac27f3e874029821180518c61e1a06b19eddf8fdf475f2ee52d86fe9afc61a` | `0b6ff09ebf8099f8f6d753625aa72cff80dbd37d1c627de4962c34a23c6ccafb` | matching |

The frozen comparator pools acquired labels by its original five-field configuration key and uses its unchanged ability fallback, benchmark fit and posterior predictive probability. Raw IDs still define separate scored pairs. Six priors are refitted from training-fold sufficient statistics using the frozen equations; fixture replication is evidence of those equations, not a claim that public item trajectories equal the old harness.

### Engineering changes preserving the predefined estimator

Default TF-IDF builds the full unselected-vocabulary sparse matrix before applying max_features. The completed path instead uses two training-only passes: Counter term frequencies from the same analyzer; sorted feature names and float32 frequency argsort for the intended 50,000-feature selection; then a fixed selected vocabulary with IDF still learned from the training fold. Word unigrams/bigrams, ridge alpha and estimator parameters remain unchanged. The independent tied-frequency, Unicode, under-cap and actual-50,000-cap equivalence fixtures are recorded below. They verify those fixtures, not a full-corpus default-versus-optimized comparison that was never completed.

The corpus retains numeric item IDs/targets, approximately 300 MB, and a generator reads one benchmark's item text per pass in the original benchmark/item order. It uses the same cleaning and target joins, replacing the roughly 15 GB resident text corpus without changing document order or training/test partition membership. A-C and D subject lookup were changed from repeated whole-table filtering to one groupby lookup, reducing O(subjects × cells) preprocessing. Completed A-C fold 0 and the completed afrimedqa checkpoint were retained on restart. Split/scoring masks and estimator definitions were preserved. The engineering source versions changed; definitions and hash lineage are recorded in [headroom/MEASUREMENT_PLAN.json](<$PAIEC_SOURCE_ROOT/headroom/MEASUREMENT_PLAN.json>). The failed default-vocabulary, resident-corpus and extra fold-5 attempts produced no completed D performance result. The later-interrupted streaming process PID 59515 retained its completed fold-0 result.

## Fit convergence and limits

Oracle B and C use L-BFGS-B, maxiter=500, ftol=1e-9, gtol=1e-5, maxcor=10. `success` is the optimizer's termination flag; it does not establish a global optimum. No failed fit is silently excluded from the reported scores.

| Fit/state | Total | Success flags | Failures | Max iterations | Max \|gradient\| | Failing benchmarks |
| --- | --- | --- | --- | --- | --- | --- |
| B full-response 2PL | 145 | 128 | 17 | 500 | 2275.67550775 | adaptivestep, afrieval, alignment_faking, babilong, bridging_gap, cruxeval, helm_afr, kmmlu, llm_uncertainty_bench, mmbench_v11, mmlu, mmlupro, monkey_power_laws, pku_saferlhf, sgrades, sib200, tensortrust |
| C B0 prior only | 145 | 145 | 0 | 0 | 0.00000000 | none |
| C B1 1PL | 145 | 145 | 0 | 55 | 0.02133810 | none |
| C B3 1PL | 145 | 145 | 0 | 64 | 0.17980152 | none |
| C B7 1PL | 145 | 145 | 0 | 81 | 0.07836666 | none |
| C B15 1PL | 145 | 145 | 0 | 97 | 0.33799526 | none |
| C B31 1PL | 145 | 145 | 0 | 174 | 2.52743224 | none |

### Every nonconverged fit

| Fold | Benchmark | Method | Budget | Iterations | Max \|gradient\| | Termination |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | afrieval | B | full | 500 | 5.85368112 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 0 | monkey_power_laws | B | full | 500 | 2275.67550775 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 1 | alignment_faking | B | full | 500 | 114.84260147 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 1 | cruxeval | B | full | 500 | 68.31398139 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 1 | llm_uncertainty_bench | B | full | 500 | 261.31735533 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 1 | mmbench_v11 | B | full | 500 | 305.72143311 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 1 | pku_saferlhf | B | full | 500 | 2.88614581 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 2 | helm_afr | B | full | 500 | 15.78668772 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 2 | mmlupro | B | full | 500 | 27.43146669 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 2 | sib200 | B | full | 500 | 2.59753976 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 3 | adaptivestep | B | full | 500 | 1.46551104 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 3 | babilong | B | full | 500 | 1025.67442387 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 3 | bridging_gap | B | full | 500 | 1184.58293045 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 3 | sgrades | B | full | 500 | 19.80532649 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 4 | tensortrust | B | full | 500 | 2.85232348 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 5 | kmmlu | B | full | 500 | 25.65991879 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |
| 5 | mmlu | B | full | 500 | 20.62874425 | STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT |

B0 C records are prior states and are not optimization calls. A-C diagnostic files are preserved separately for every fold. Convergence limitations especially qualify Oracle B's headroom interpretation. A comparison with an oracle score does not eliminate untested item-aware approaches.

## Validation and preservation

Implementation fixture checks: [headroom/independent_validation.json](<$PAIEC_SOURCE_ROOT/headroom/independent_validation.json>). These checks cover frozen-interface equivalence, gradients, acquisition/evaluation separation, visible-state pooling, evaluation-outcome perturbations, prior-equation replication and identical D/A-C split RNG consumption. They are implementation checks rather than public-pool quality or hidden-set performance measurements.

```json
{
  "frozen_interface": {
    "cases": 30,
    "budgets": [
      0,
      1,
      3,
      7,
      15,
      31
    ],
    "fallbacks": [
      "full",
      "name",
      "provider",
      "global"
    ],
    "max_abs_error": 0.0,
    "pass": true
  },
  "gradient_checks": [
    {
      "model": "1PL",
      "parameters": 8,
      "epsilon": 1e-06,
      "max_abs_error": 1.3263161680043822e-09,
      "pass": true
    },
    {
      "model": "2PL",
      "parameters": 12,
      "epsilon": 1e-06,
      "max_abs_error": 2.056773834580028e-09,
      "pass": true
    }
  ],
  "fixture_protocol": {
    "raw_subjects": 3,
    "feasible_visible_subjects": 2,
    "oracle_raw_items": 200,
    "evaluation_items_per_pair": 50,
    "b0_reuse_zero": true,
    "disjoint_subject_all_reuse_zero": true,
    "nested_reuse_monotone": true,
    "oracle_static": true,
    "text_static": true,
    "feasible_C_labels_unchanged_when_eval_outcomes_flipped": true,
    "oracle_labels_change_when_eval_outcomes_flipped": true,
    "fit_success_count": 6,
    "fit_total": 6,
    "pass": true
  },
  "prior_replication": {
    "fixture": "irt_shrink/synth/data",
    "responses": 504954,
    "benchmarks": 36,
    "entire_prior_equal": true,
    "max_absolute_error": 0.0,
    "pass": true
  },
  "wall_seconds": 0.23738554120063782,
  "all_pass": true,
  "D_split_rng": {
    "raw_subject_item_counts": {
      "sA": 81,
      "sB": 100,
      "sC": 121,
      "sD": 270
    },
    "evaluation_cells": 287,
    "masks_identical": true,
    "rng_state_identical_after_each_subject": true,
    "max_score_abs_error": 0.0,
    "pass": true
  },
  "public_streamed_prior_replication": {
    "scope": "full public streamed sufficient stats versus frozen all-public prior artifact",
    "stats_equal": true,
    "hyper_max_abs_error": 2.956523914576792e-12,
    "ability_max_abs_errors": {
      "a_full": 8.19677659080753e-12,
      "a_name": 8.179013022413528e-12,
      "a_provider": 5.256017843180416e-12,
      "a_global": 8.903988657493755e-14
    },
    "keys_equal": {
      "a_full": true,
      "a_name": true,
      "a_provider": true
    },
    "pass": true
  },
  "two_pass_tfidf": {
    "cases": [
      {
        "case": "small_ties_unicode",
        "documents": 7,
        "cap": 5,
        "features": 5,
        "dtype": "float32",
        "vocabulary_equal": true,
        "idf_max_abs_error": 0.0,
        "X_max_abs_error": 0.0,
        "X_test_max_abs_error": 0.0,
        "ridge_prediction_max_abs_error": 0.0,
        "ridge_iterations_base": [
          3
        ],
        "ridge_iterations_fixed": [
          3
        ],
        "pass": true
      },
      {
        "case": "under_cap",
        "documents": 4,
        "cap": 50000,
        "features": 13,
        "dtype": "float32",
        "vocabulary_equal": true,
        "idf_max_abs_error": 0.0,
        "X_max_abs_error": 0.0,
        "X_test_max_abs_error": 0.0,
        "ridge_prediction_max_abs_error": 0.0,
        "ridge_iterations_base": [
          1
        ],
        "ridge_iterations_fixed": [
          1
        ],
        "pass": true
      },
      {
        "case": "actual_50000_cap_many_ties",
        "documents": 30,
        "cap": 50000,
        "features": 50000,
        "dtype": "float32",
        "vocabulary_equal": true,
        "idf_max_abs_error": 0.0,
        "X_max_abs_error": 0.0,
        "X_test_max_abs_error": 0.0,
        "ridge_prediction_max_abs_error": 0.0,
        "ridge_iterations_base": [
          3
        ],
        "ridge_iterations_fixed": [
          3
        ],
        "pass": true
      }
    ],
    "all_pass": true,
    "tolerance": 1e-06,
    "scope": "same sklearn float32 word1-2gram top-feature selection incl ties; numeric roundoff tolerance"
  },
  "streamed_document_order": {
    "cases": [
      {
        "heldout_fold": 0,
        "partition": "train",
        "documents": 6,
        "equal": true,
        "document_sequence_sha256": "ba174f4869e059608877765d8275de5f6a2d103be66540b9527e4be10edfa08e"
      },
      {
        "heldout_fold": 0,
        "partition": "test",
        "documents": 3,
        "equal": true,
        "document_sequence_sha256": "efca56bfeb21e0ff0b0c56188ca55757197f203dfb5aa0c5737d2b54b72f995d"
      },
      {
        "heldout_fold": 1,
        "partition": "train",
        "documents": 6,
        "equal": true,
        "document_sequence_sha256": "d76f59e46e85e6dceca4243bdbc2c75811989e3ad05685d1d9d520e0068c679c"
      },
      {
        "heldout_fold": 1,
        "partition": "test",
        "documents": 3,
        "equal": true,
        "document_sequence_sha256": "5f292b90e011451d85d428bf83e021ab0ea1fbbc6403b9b0418719583e151140"
      },
      {
        "heldout_fold": 2,
        "partition": "train",
        "documents": 6,
        "equal": true,
        "document_sequence_sha256": "aae7e940e85b0ffc5186308a327764f299d03cbce7f67ed7f0d794c1bb43ce34"
      },
      {
        "heldout_fold": 2,
        "partition": "test",
        "documents": 3,
        "equal": true,
        "document_sequence_sha256": "f2019a1c5e5d44a17506f233b97c39d2293ab65c6b01803d0e7ccbbc937b28a4"
      }
    ],
    "all_pass": true,
    "source_documents_function_sha256": "038fb92688c848862ad7941ee17924fc46cc2b88306d20fe0d118eabb00b8baf",
    "scope": "exact current streamed documents function vs former resident left-merge, unsorted source rows, preserved target order, None and whitespace cleaning"
  }
}
```

### Two-pass TF-IDF equivalence fixtures

Recorded all-pass flag: `True`. This is fixture-level algorithm-equivalence evidence, separate from D's final scores.

| Fixture | Documents | Feature cap | Vocabulary equal | Max IDF error | Max training-X error | Max test-X error | Max ridge-prediction error | Pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| small_ties_unicode | 7 | 5 | True | 0.0000000000 | 0.0000000000 | 0.0000000000 | 0.0000000000 | True |
| under_cap | 4 | 50000 | True | 0.0000000000 | 0.0000000000 | 0.0000000000 | 0.0000000000 | True |
| actual_50000_cap_many_ties | 30 | 50000 | True | 0.0000000000 | 0.0000000000 | 0.0000000000 | 0.0000000000 | True |

### Saved measurement definitions and source lineage

[headroom/MEASUREMENT_PLAN.json](<$PAIEC_SOURCE_ROOT/headroom/MEASUREMENT_PLAN.json>)

Original estimator definitions were recorded before the first completed benchmark metrics. Subsequent source versions reflect engineering/resource changes; original algorithm parameters were retained. Recorded provenance follows:

```json
{
  "recorded_at_kst": "2026-10-09T02:19:12.527390+09:00",
  "script_sha256": "09db8a05c79bdec41eb43bffa81babbc7a02879205958ab9ef03bfeb1c2766a2",
  "scope": "public-pool A-D measurement; no adoption/tuning/submission",
  "budgets": [
    0,
    1,
    3,
    7,
    15,
    31
  ],
  "weights": [
    0.1,
    0.2,
    0.2,
    0.2,
    0.2,
    0.1
  ],
  "folds": "lobo_eval.fold_of SHA256 fold:bench modulo6",
  "split_seed": "lobo_eval._h(split:bench), successive per-raw-subject exact half and acquisition order permutations",
  "trial": "earliest recorded trial after stable subject/item/trial sorting; official trial selection not specified",
  "C": {
    "family": "1PL MAP",
    "theta_mean": "mean_lam*a prior fallback",
    "theta_var": "tau2+mean_lam^2*a_var",
    "d_prior": "N(mu_d,s2_d)",
    "item_offset_prior": "N(0,1)",
    "visible_item_features": "content+item_features, normalized; ignores response interactors"
  },
  "B": {
    "family": "2PL MAP oracle on all heldout-benchmark binary responses",
    "theta_prior_variance": 4,
    "intercept_prior_variance": 4,
    "offset_variance": 1,
    "log_discrimination_variance": 1,
    "a_bounds": [
      0.1,
      5
    ]
  },
  "optimizer": {
    "method": "L-BFGS-B",
    "maxiter": 500,
    "ftol": 1e-09,
    "gtol": 1e-05
  },
  "D": {
    "ngram": [
      1,
      2
    ],
    "max_features": 50000,
    "ridge_alpha": 1,
    "solver": "lsqr",
    "tol": 0.0001,
    "maxiter": 2000,
    "item_target": "logit of mean per-subject item rate; clip 1e-4",
    "probability": "sigmoid(a_prior_mean + predicted item easiness)",
    "budgets": "static across all budgets, ALC=B0"
  },
  "comparison": "frozen v2 algorithm with fold-refit priors, identical acquisition/evaluation cells",
  "anchor_target": "0.1172 user-provided board snapshot; hidden/local scale and noise UNMEASURED",
  "final_script_sha256": "a2ed788351ff1029a72f3d4bfe6adc7a41b97b9c6c10c050a12cd705d4bb8248",
  "implementation_refinements": [
    "Group subject rows once instead of repeated full-table filtering; same cells and RNG consumption.",
    "Two-pass exact training term counts then the same sorted feature and float32 argsort top-50000 selection; fixed-vocabulary TF-IDF fits training IDF.",
    "Stream document text one benchmark at a time in identical original order instead of retaining all corpus text.",
    "Resume completed A-C benchmark/fold checkpoints; no completed scores discarded.",
    "Publish atomic per-fold D CSV/fit artifacts and hash-validated completion markers; final D workers cover folds 0,1,2 and 3,4,5. An extra dedicated fold-5 attempt was interrupted during term counting for disk/swap pressure, produced no completed scores, and is recorded separately. Preserve completed checkpoints and merge only after all six D fits/text markers and A-C completion markers are validated. No estimators or parameters changed."
  ],
  "two_pass_equivalence_evidence": "independent_validation.json",
  "model_parameters_changed": false,
  "orchestration_validation_evidence": "orchestration_validation.json",
  "D_worker_schedule": {
    "main_resume": [
      0,
      1,
      2
    ],
    "secondary": [
      3,
      4,
      5
    ],
    "extra_dedicated_fold5_attempt": {
      "pid": 67761,
      "session_id": 83137,
      "status": "INTERRUPTED",
      "evidence": "text_5_interrupted.json"
    },
    "coordination": "Final two workers cover disjoint folds0,1,2 and3,4,5; dedicatedfold5 will not be restarted."
  }
}
```

### Orchestration implementation evidence

The isolated checkpoint smoke fixtures and independent source review are distinct evidence. The fixtures execute legacy-adoption, complete-marker acceptance, partial-CSV rejection and changed-hash rejection in a temporary directory. The separate review inspects source and those fixture outputs; it explicitly does not rerun the entire numerical science suite. Neither establishes predictive quality or hidden performance.

[headroom/orchestration_validation.json](<$PAIEC_SOURCE_ROOT/headroom/orchestration_validation.json>)

```json
{
  "recorded_at_kst": "2026-10-09T02:52:02.933243+09:00",
  "script": "headroom/measure.py",
  "script_sha256": "a2ed788351ff1029a72f3d4bfe6adc7a41b97b9c6c10c050a12cd705d4bb8248",
  "status": "PASS",
  "checks": {
    "syntax": "AST parse of the patched source completed.",
    "legacy_backfill": "Complete isolated legacy fold CSV and text_fits list were adopted into individual fit and TEXT_DONE artifacts.",
    "checkpoint_validation": "Adopted completion marker validated its fold, expected benchmark pair counts, finite probability-range Brier scores, CSV hash, and fit hash.",
    "partial_csv_rejected": "Replacing the isolated complete CSV with an incomplete CSV raised ValueError.",
    "changed_hash_rejected": "Changing an isolated score while preserving row counts raised ValueError because its marker hash no longer matched."
  },
  "fixture_scope": "Isolated TemporaryDirectory under headroom; no production score artifacts used or changed.",
  "fixture_outputs": "Removed when the test context exited.",
  "estimator_or_parameter_changes": false
}
```

[headroom/orchestration_independent_review.json](<$PAIEC_SOURCE_ROOT/headroom/orchestration_independent_review.json>)

```json
{
  "recorded_at_kst": "2026-10-09T03:01:09.293476+09:00",
  "kind": "independent source review",
  "scope": "Latest subset-text-worker and assembly orchestration; source inspection plus inspection of orchestration_validation.json. This review did not rerun the entire numerical fixture suite.",
  "script": "headroom/measure.py",
  "script_sha256": "a2ed788351ff1029a72f3d4bfe6adc7a41b97b9c6c10c050a12cd705d4bb8248",
  "status": "PASS",
  "checks": {
    "fold_isolation": "The selected execution folds alter worker scheduling only. Each selected fold trains on the entire corpus with corpus.fold != fold and tests on corpus.fold == fold.",
    "estimator_equivalence": "TF-IDF parameters, deterministic two-pass vocabulary selection, Ridge parameters, text target definitions, prior lookup, and D scoring are unchanged by the orchestration refactor.",
    "document_and_split_order": "documents(partition) still preserves benchmark sort=False and target item order; D consumes the per-subject acquisition-order permutation so its evaluation cells match simulate.",
    "atomic_publication": "Per-fold text CSV and fit JSON are atomically published before TEXT_DONE. The marker records expected row count and both artifact SHA256 values.",
    "checkpoint_acceptance": "Completion requires expected per-benchmark pair counts, no duplicate benchmark/subject rows, finite Brier scores in [0,1], matching fit.fold, and matching marker counts/hashes.",
    "legacy_adoption": "Only the resumed assembler adopts complete legacy fold CSV/list metadata. Standalone text workers do not backfill. Legacy adoption validates the complete CSV before publishing its fit and marker.",
    "assembly": "Assembler waits for all six AC_DONE and TEXT_DONE markers and per-fold fit JSON, revalidates text checkpoints, and uses a one-to-one benchmark/subject merge with equal coverage before final aggregation.",
    "reviewed_smoke_evidence": "orchestration_validation.json records isolated syntax, legacy adoption, valid checkpoint, incomplete CSV rejection, and changed-hash rejection checks with PASS."
  },
  "operational_condition": "The original legacy text process must be stopped after its complete fold checkpoint is saved and before the resumed assembler adopts it; parent has scheduled this sequence.",
  "estimator_or_parameter_changes": false,
  "production_artifacts_modified_by_review": false
}
```

### D0 sanity review

A poor first-fold D score triggered an independent target/prior/sign sanity review. This checks the recorded implementation without refitting or changing estimator parameters. A first-fold observation is not a full-run D conclusion; the canonical six-fold table supplies the final comparison.

[headroom/D0_sanity_review.json](<$PAIEC_SOURCE_ROOT/headroom/D0_sanity_review.json>)

```json
{
  "recorded_at_kst": "2026-10-09T03:27:47.303349+09:00",
  "kind": "Independent read-only D fold0 sanity review",
  "status": "PASS_WITH_NO_IMPLEMENTATION_ERROR_FOUND_IN_CHECKED_SCOPE",
  "no_new_fits": true,
  "scope": "Independent raw binary response calculation on five real training benchmarks; real fold0 eligible-subject prior quantiles; saved target distribution and saved score arithmetic; source sign/index review. Does not recreate unavailable per-item Ridge predictions or refit the model.",
  "source_sha256": "a2ed788351ff1029a72f3d4bfe6adc7a41b97b9c6c10c050a12cd705d4bb8248",
  "target_checks": [
    {
      "benchmark": "algotune",
      "fold": 4,
      "binary_responses_used": 2772,
      "raw_subject_item_cells": 2772,
      "items": 154,
      "subject_mean_rate_max_abs_error": 0.0,
      "clipped_logit_max_abs_error": 0.0,
      "subject_counts_identical": true,
      "status": "PASS",
      "inputs_sha256": {
        "responses": "66454f671fb545f99d012d212dcd82156c2943fced9c5be82318fc674142097f",
        "subjects": "7e8fd95d157c3d49d0ab4956a570a4d6a234c8ec7f49104af472a22d08286cf4",
        "stored_targets": "0b491d2141b7226724b682117caf51355265dac9e22b9b29d80fd570b2d4ca8d"
      },
      "subject_item_cells_with_multiple_recorded_trials": 0
    },
    {
      "benchmark": "beavertails",
      "fold": 3,
      "binary_responses_used": 1680,
      "raw_subject_item_cells": 1680,
      "items": 420,
      "subject_mean_rate_max_abs_error": 0.0,
      "clipped_logit_max_abs_error": 0.0,
      "subject_counts_identical": true,
      "status": "PASS",
      "inputs_sha256": {
        "responses": "7367901e99aadfde4e9c6ad444413fbb97cabdb097bfb8454793817dad67c158",
        "subjects": "2fa69259ea06562298346133c9a0ee65a6b2c3082e09142b232233ce1ade53c7",
        "stored_targets": "4c71543dbf7e7b2b5279d19696979feab886c8356a6b5daf2a80d55251ed40fe"
      },
      "subject_item_cells_with_multiple_recorded_trials": 0
    },
    {
      "benchmark": "financebench",
      "fold": 3,
      "binary_responses_used": 2400,
      "raw_subject_item_cells": 2400,
      "items": 150,
      "subject_mean_rate_max_abs_error": 0.0,
      "clipped_logit_max_abs_error": 0.0,
      "subject_counts_identical": true,
      "status": "PASS",
      "inputs_sha256": {
        "responses": "1b7c8eb6d6498c45b1a27cd6ade8b968842399c20b10077dd6f7847ebd912a16",
        "subjects": "60043d9fcc3b17908defaa203db95c2ca09330e83f9a39709212e83c20264b31",
        "stored_targets": "dab67da0689c2341bda4cf828d8727905453de316a05b6c390936c77d42f0185"
      },
      "subject_item_cells_with_multiple_recorded_trials": 0
    },
    {
      "benchmark": "jailbreakbench",
      "fold": 5,
      "binary_responses_used": 3074,
      "raw_subject_item_cells": 3074,
      "items": 2001,
      "subject_mean_rate_max_abs_error": 0.0,
      "clipped_logit_max_abs_error": 0.0,
      "subject_counts_identical": true,
      "status": "PASS",
      "inputs_sha256": {
        "responses": "dcc5bb3b227497752ac3f03a85eacb18b247e4b9e3bc6ba8dcef1c3a7ee033a5",
        "subjects": "5a1961e2dbec840d2413a700bf7c0379b8c6d62471fca45bc3e64ddd95583de6",
        "stored_targets": "8318b4fb8ba0cb492d38496b7e98704f8a4d6cfe9c0666b78d9d2ebd114ff5e9"
      },
      "subject_item_cells_with_multiple_recorded_trials": 0
    },
    {
      "benchmark": "naep_llm_students",
      "fold": 3,
      "binary_responses_used": 53680,
      "raw_subject_item_cells": 5368,
      "items": 488,
      "subject_mean_rate_max_abs_error": 2.220446049250313e-16,
      "clipped_logit_max_abs_error": 2.220446049250313e-15,
      "subject_counts_identical": true,
      "status": "PASS",
      "inputs_sha256": {
        "responses": "a3c8132fc2a3a9e489d5e74184ce04d7e300b2429fb0ded9e480f04dce4842e7",
        "subjects": "35fba2d648b2af2e88746d03616c9e9c3048cf18b1fcf9accf663b55cd279a16",
        "stored_targets": "1a506d5a0a5e426a335c7cb26277c034fb52fc8d1fc7d3024c55ac6080e5be0e"
      },
      "subject_item_cells_with_multiple_recorded_trials": 5368
    }
  ],
  "ability_stats": {
    "eligible_pairs": 1480,
    "ability_quantiles": {
      "0": -1.8284041736244097,
      "0.01": -1.060604623634885,
      "0.05": -0.7233650888469351,
      "0.25": 0.0,
      "0.5": 0.0,
      "0.75": 0.0,
      "0.95": 0.0,
      "0.99": 0.5271745574741826,
      "1": 1.6839211582911087
    },
    "ability_variance_quantiles": {
      "0": 0.000575093371351391,
      "0.01": 0.007136035078768159,
      "0.05": 0.08016555808328063,
      "0.25": 1.0147004527964367,
      "0.5": 1.0147004527964367,
      "0.75": 1.0147004527964367,
      "0.95": 1.0147004527964367,
      "0.99": 1.0147004527964367,
      "1": 1.2348003432189536
    },
    "fallback_counts": {
      "global": 1217,
      "name": 211,
      "provider": 33,
      "full": 19
    },
    "prior_hyper": {
      "mu_d": 1.1286794941864602,
      "s2_d": 4.306337769132878,
      "s2_l": 1.0059990472134202,
      "tau2": 0.05,
      "mean_lam": 2.103878309449079
    },
    "prior_sha256": "2606f1c20ce98cc6817c936d84ee8a543d0702caca606534dfc238596455c65b",
    "per_benchmark_ability": {
      "afrieval": {
        "pairs": 948,
        "quantiles": {
          "0": 0.0,
          "0.01": 0.0,
          "0.05": 0.0,
          "0.25": 0.0,
          "0.5": 0.0,
          "0.75": 0.0,
          "0.95": 0.0,
          "0.99": 0.0,
          "1": 0.0
        }
      },
      "agentic_review_perturbation": {
        "pairs": 3,
        "quantiles": {
          "0": -0.3949533318350444,
          "0.01": -0.3949533318350444,
          "0.05": -0.3949533318350444,
          "0.25": -0.3949533318350444,
          "0.5": -0.3949533318350444,
          "0.75": -0.3949533318350444,
          "0.95": -0.3949533318350444,
          "0.99": -0.3949533318350444,
          "1": -0.3949533318350444
        }
      },
      "agi_elo": {
        "pairs": 20,
        "quantiles": {
          "0": -1.8284041736244097,
          "0.01": -1.7784194969430505,
          "0.05": -1.578480790217614,
          "0.25": -0.9970985769516405,
          "0.5": -0.5866167151654309,
          "0.75": 0.0,
          "0.95": 0.0,
          "0.99": 0.0,
          "1": 0.0
        }
      },
      "averimatec": {
        "pairs": 1,
        "quantiles": {
          "0": 0.0,
          "0.01": 0.0,
          "0.05": 0.0,
          "0.25": 0.0,
          "0.5": 0.0,
          "0.75": 0.0,
          "0.95": 0.0,
          "0.99": 0.0,
          "1": 0.0
        }
      },
      "ceval": {
        "pairs": 11,
        "quantiles": {
          "0": -0.7370494172103386,
          "0.01": -0.6633444754893048,
          "0.05": -0.3685247086051693,
          "0.25": 0.0,
          "0.5": 0.0,
          "0.75": 0.0,
          "0.95": 0.0,
          "0.99": 0.0,
          "1": 0.0
        }
      },
      "clasheval": {
        "pairs": 6,
        "quantiles": {
          "0": -1.3091093857839602,
          "0.01": -1.303087553970668,
          "0.05": -1.2790002267175002,
          "0.25": -1.1231055754619055,
          "0.5": -0.7435403265597167,
          "0.75": -0.32561449549839155,
          "0.95": 0.5161412658878941,
          "0.99": 0.7197150596506566,
          "1": 0.7706085080913471
        }
      },
      "edu_circuit_hw": {
        "pairs": 6,
        "quantiles": {
          "0": -0.815486269867141,
          "0.01": -0.8115644272343009,
          "0.05": -0.7958770567029404,
          "0.25": -0.7370494172103386,
          "0.5": -0.658859547298104,
          "0.75": -0.5239125154366011,
          "0.95": -0.2728090160440574,
          "0.99": -0.21089316393486948,
          "1": -0.19541420090757258
        }
      },
      "egoschema": {
        "pairs": 11,
        "quantiles": {
          "0": -0.7303661398688226,
          "0.01": -0.7033539563002501,
          "0.05": -0.5953052220259601,
          "0.25": -0.44737324039301996,
          "0.5": -0.43450217660294216,
          "0.75": -0.43450217660294216,
          "0.95": -0.43450217660294216,
          "0.99": -0.43450217660294216,
          "1": -0.43450217660294216
        }
      },
      "elicitation_game": {
        "pairs": 13,
        "quantiles": {
          "0": 0.0,
          "0.01": 0.0,
          "0.05": 0.0,
          "0.25": 0.0,
          "0.5": 0.0,
          "0.75": 0.0,
          "0.95": 0.0,
          "0.99": 0.0,
          "1": 0.0
        }
      },
      "engdesign": {
        "pairs": 12,
        "quantiles": {
          "0": -0.815486269867141,
          "0.01": -0.8102990240782918,
          "0.05": -0.7895500409228948,
          "0.25": -0.5834469142203883,
          "0.5": -0.5117885005846182,
          "0.75": -0.47009990399740265,
          "0.95": -0.4062005843604975,
          "0.99": -0.38562991081108877,
          "1": -0.38048724242373666
        }
      },
      "enginemt_qa": {
        "pairs": 1,
        "quantiles": {
          "0": 0.0,
          "0.01": 0.0,
          "0.05": 0.0,
          "0.25": 0.0,
          "0.5": 0.0,
          "0.75": 0.0,
          "0.95": 0.0,
          "0.99": 0.0,
          "1": 0.0
        }
      },
      "helm_bbq": {
        "pairs": 81,
        "quantiles": {
          "0": -1.5653269279330457,
          "0.01": -1.3312524576949756,
          "0.05": -1.029421923104802,
          "0.25": -0.7915649339061158,
          "0.5": -0.5401301022450292,
          "0.75": -0.3395641491213735,
          "0.95": 0.5271745574741826,
          "0.99": 1.0084081542364205,
          "1": 1.6839211582911087
        }
      },
      "legal_rag_bench": {
        "pairs": 6,
        "quantiles": {
          "0": -0.48598033309204397,
          "0.01": -0.48598033309204397,
          "0.05": -0.48598033309204397,
          "0.25": -0.48598033309204397,
          "0.5": -0.36719514800202313,
          "0.75": -0.24840996291200232,
          "0.95": -0.24840996291200232,
          "0.99": -0.24840996291200232,
          "1": -0.24840996291200232
        }
      },
      "legalbench": {
        "pairs": 31,
        "quantiles": {
          "0": -1.3261514364159674,
          "0.01": -1.3261514364159674,
          "0.05": -1.206019533382408,
          "0.25": -0.7975180582771899,
          "0.5": -0.43450217660294216,
          "0.75": 0.0,
          "0.95": 0.5851465039744709,
          "0.99": 0.8598531307477203,
          "1": 0.8598531307477203
        }
      },
      "lingoly": {
        "pairs": 11,
        "quantiles": {
          "0": 0.0,
          "0.01": 0.0,
          "0.05": 0.0,
          "0.25": 0.0,
          "0.5": 0.0,
          "0.75": 0.0,
          "0.95": 0.0,
          "0.99": 0.0,
          "1": 0.0
        }
      },
      "medhelm_race_based_med": {
        "pairs": 13,
        "quantiles": {
          "0": -1.0343719996599086,
          "0.01": -1.0312378601137089,
          "0.05": -1.0187013019289104,
          "0.25": -0.7981291748696464,
          "0.5": -0.6846173305537054,
          "0.75": -0.1746929847219488,
          "0.95": -0.033256626409378764,
          "0.99": 0.02976803618455558,
          "1": 0.045524201833039284
        }
      },
      "monkey_power_laws": {
        "pairs": 13,
        "quantiles": {
          "0": -0.9651473402661821,
          "0.01": -0.9372656713878555,
          "0.05": -0.825738995874549,
          "0.25": -0.6335482200043776,
          "0.5": 0.0,
          "0.75": 0.0,
          "0.95": 0.0,
          "0.99": 0.0,
          "1": 0.0
        }
      },
      "mtbbench": {
        "pairs": 25,
        "quantiles": {
          "0": 0.0,
          "0.01": 0.0,
          "0.05": 0.0,
          "0.25": 0.0,
          "0.5": 0.0,
          "0.75": 0.0,
          "0.95": 0.0,
          "0.99": 0.0,
          "1": 0.0
        }
      },
      "multi_swebench": {
        "pairs": 82,
        "quantiles": {
          "0": -0.9658510904273091,
          "0.01": -0.9658510904273091,
          "0.05": -0.9658510904273091,
          "0.25": -0.5802771132753457,
          "0.5": -0.4921566252684735,
          "0.75": -0.3964929414197704,
          "0.95": 0.8395299032227453,
          "0.99": 1.1925600344006677,
          "1": 1.1925600344006677
        }
      },
      "openbiorq": {
        "pairs": 11,
        "quantiles": {
          "0": -0.7370494172103386,
          "0.01": -0.7305638511912188,
          "0.05": -0.7046215871147395,
          "0.25": -0.5416203296969075,
          "0.5": -0.47776315787196066,
          "0.75": -0.2515107479452749,
          "0.95": -0.172171456913496,
          "0.99": -0.172171456913496,
          "1": -0.172171456913496
        }
      },
      "perfcodebench": {
        "pairs": 20,
        "quantiles": {
          "0": 0.0,
          "0.01": 0.0,
          "0.05": 0.0,
          "0.25": 0.0,
          "0.5": 0.0,
          "0.75": 0.0,
          "0.95": 0.0,
          "0.99": 0.0,
          "1": 0.0
        }
      },
      "pxplore": {
        "pairs": 14,
        "quantiles": {
          "0": 0.0,
          "0.01": 0.0,
          "0.05": 0.0,
          "0.25": 0.0,
          "0.5": 0.0,
          "0.75": 0.0,
          "0.95": 0.0,
          "0.99": 0.0,
          "1": 0.0
        }
      },
      "swe_together": {
        "pairs": 20,
        "quantiles": {
          "0": 0.0,
          "0.01": 0.0,
          "0.05": 0.0,
          "0.25": 0.0,
          "0.5": 0.0,
          "0.75": 0.0,
          "0.95": 0.0,
          "0.99": 0.0,
          "1": 0.0
        }
      },
      "visual_riddles": {
        "pairs": 8,
        "quantiles": {
          "0": 0.0,
          "0.01": 0.0,
          "0.05": 0.0,
          "0.25": 0.0,
          "0.5": 0.0,
          "0.75": 0.0,
          "0.95": 0.0,
          "0.99": 0.0,
          "1": 0.0
        }
      },
      "wmt_mqm": {
        "pairs": 113,
        "quantiles": {
          "0": 0.0,
          "0.01": 0.0,
          "0.05": 0.0,
          "0.25": 0.0,
          "0.5": 0.0,
          "0.75": 0.0,
          "0.95": 0.0,
          "0.99": 0.0,
          "1": 0.0
        }
      }
    }
  },
  "training_target_stats": {
    "training_items": 3367460,
    "rate_quantiles": {
      "0": 0.0,
      "0.01": 0.0,
      "0.05": 0.0,
      "0.25": 0.0,
      "0.5": 0.45454545454545453,
      "0.75": 1.0,
      "0.95": 1.0,
      "0.99": 1.0,
      "1": 1.0
    },
    "easiness_quantiles": {
      "0": -9.21024036697585,
      "0.01": -9.21024036697585,
      "0.05": -9.21024036697585,
      "0.25": -9.21024036697585,
      "0.5": -0.18232155679395468,
      "0.75": 9.21024036697596,
      "0.95": 9.21024036697596,
      "0.99": 9.21024036697596,
      "1": 9.21024036697596
    },
    "exact_zero_rate_items": 1340264,
    "exact_one_rate_items": 1090093,
    "exact_zero_or_one_fraction": 0.7217181495845534,
    "single_subject_item_fraction": 0.5555002880509345,
    "mean_rate": 0.4711558986556889,
    "mean_easiness": -0.6410394660206422,
    "item_count_dominance_top10": [
      {
        "bench": "tensortrust",
        "items": 570791,
        "exact_zero_rate": 482059,
        "exact_one_rate": 87111,
        "single_subject_items": 568649,
        "mean_easiness": -6.373029821820409,
        "mean_rate": 0.15399550747599977,
        "training_item_fraction": 0.1695019391470129
      },
      {
        "bench": "babilong",
        "items": 526202,
        "exact_zero_rate": 193542,
        "exact_one_rate": 139193,
        "single_subject_items": 195969,
        "mean_easiness": -0.9491937308917107,
        "mean_rate": 0.44922795870155435,
        "training_item_fraction": 0.15626080191004496
      },
      {
        "bench": "llmail_inject",
        "items": 207043,
        "exact_zero_rate": 204969,
        "exact_one_rate": 754,
        "single_subject_items": 197057,
        "mean_easiness": -9.08983622422672,
        "mean_rate": 0.005875508362194955,
        "training_item_fraction": 0.0614834326168685
      },
      {
        "bench": "bbq",
        "items": 204093,
        "exact_zero_rate": 49347,
        "exact_one_rate": 119489,
        "single_subject_items": 145679,
        "mean_easiness": 3.199897459008363,
        "mean_rate": 0.6797011656450735,
        "training_item_fraction": 0.060607401424218846
      },
      {
        "bench": "interchangeable_token_embeddings",
        "items": 199893,
        "exact_zero_rate": 2088,
        "exact_one_rate": 176916,
        "single_subject_items": 55,
        "mean_easiness": 8.05534912617087,
        "mean_rate": 0.9373039576173253,
        "training_item_fraction": 0.0593601705736668
      },
      {
        "bench": "llm_bp_tag",
        "items": 152139,
        "exact_zero_rate": 55640,
        "exact_one_rate": 96124,
        "single_subject_items": 152139,
        "mean_easiness": 2.4510560168648694,
        "mean_rate": 0.6330952839375182,
        "training_item_fraction": 0.04517915580289001
      },
      {
        "bench": "llm_uncertainty_bench",
        "items": 149793,
        "exact_zero_rate": 845,
        "exact_one_rate": 0,
        "single_subject_items": 0,
        "mean_easiness": 0.10844743991866974,
        "mean_rate": 0.5367104643623888,
        "training_item_fraction": 0.044482488284938795
      },
      {
        "bench": "ood_prediction",
        "items": 142805,
        "exact_zero_rate": 69918,
        "exact_one_rate": 72887,
        "single_subject_items": 142805,
        "mean_easiness": 0.19148631805300467,
        "mean_rate": 0.510395294282413,
        "training_item_fraction": 0.04240733371740125
      },
      {
        "bench": "bridging_gap",
        "items": 132418,
        "exact_zero_rate": 5081,
        "exact_one_rate": 10224,
        "single_subject_items": 0,
        "mean_easiness": 0.45581900965876176,
        "mean_rate": 0.5374596450683382,
        "training_item_fraction": 0.0393228130400955
      },
      {
        "bench": "tumlu",
        "items": 128016,
        "exact_zero_rate": 52245,
        "exact_one_rate": 72868,
        "single_subject_items": 120090,
        "mean_easiness": 1.4841671968716554,
        "mean_rate": 0.5806485126859143,
        "training_item_fraction": 0.03801559632482643
      }
    ],
    "aggregation_note": "Each training item is one Ridge target row, regardless of its benchmark or number of contributing raw subjects."
  },
  "saved_score_checks": {
    "pairs": 1480,
    "D_alc": 0.588269892134917,
    "D_b0": 0.588269892134917,
    "frozen_alc": 0.18253248468861683,
    "frozen_b0": 0.23099109384520541,
    "frozen_b0_minus_D_b0": -0.35727879828971154,
    "D_pair_score_quantiles": {
      "0": 0.0005687005947101,
      "0.01": 0.05865237977075697,
      "0.05": 0.12723069774401774,
      "0.25": 0.42467388980542026,
      "0.5": 0.6757764096668583,
      "0.75": 0.7519815378606306,
      "0.95": 0.8175831559711719,
      "0.99": 0.8382409380730611,
      "1": 0.853025322107479
    },
    "D_static_across_all_budgets_exact": true,
    "input_sha256": {
      "D_scores": "e369f15e8010dfe0605a1ec524c607ba4d5f23e4ed01fcd59d78082dca75f2f7",
      "AC_scores": "297ac203f2f2265914d830c821b3af9f224cda8ef9de8f4ccd7b676ec1c5c9d9",
      "D_fit_metadata": "d4ed8a41e931f94128c16254132310d8c2d67bb24a90d52cf87ef24d18920ba8"
    }
  },
  "source_checks": {
    "target_definition": "Verified real data: per raw subject/item trial mean, then equal mean over raw subjects for each item, then logit clipping [1e-4,1-1e-4].",
    "sign": "The regressor predicts item easiness e, and D computes expit(am + e). This equals sigma(theta - b) with b = -e. No accidental sign reversal found.",
    "item_prediction_alignment": "Training/test labels and documents use the same numeric corpus order; pred is assigned positionally to test.copy(), then per-benchmark pred_e is keyed by item_id. Response item_id maps to that keyed Series. Previous independent streamed-document fixture and D RNG-consumption fixture passed.",
    "heldout_fold_visibility": "Fold0 vocabulary, IDF, regression targets use only corpus.fold != 0; prior is fold_prior_0.json. Fold0 responses are only used for scoring.",
    "budget_static": "Saved D_ALC and all budget columns are exactly equal for all 1480 pairs, matching the intentionally B0-only text estimator."
  },
  "implementation_error_found": false,
  "limitations": [
    "The trained Ridge coefficient/vectorizer state and per-item fold0 predicted easiness were not saved, so this review cannot independently inspect the actual prediction distribution or recompute D scores from saved model parameters. No refit was performed.",
    "Passing these input/source checks does not prove every possible implementation path is error-free."
  ],
  "hypotheses_separate_from_verified_checks": [
    "Very large clipped target magnitudes and item-count imbalance may produce overconfident text extrapolation across benchmarks. The target distribution is verified, but the causal explanation for fold0 score is not established.",
    "The standardized subject ability prior plus directly regressed aggregate item easiness may generalize poorly when heldout subjects/benchmarks differ in ability composition; no alternative estimator was tested."
  ]
}
```

### D content input scope review

This read-only inspection consumed the first two content cells from each of four named benchmarks, eight cells in total, and saved schema/field names/types/lengths rather than prompts or assets. No recognized data URI or long base64-like run was found in those eight cells. The sample is not random or representative; corpus-wide prevalence remains UNMEASURED. The two sampled mind2web strings were serialized JSON containing candidate_node_ids, cleaned_html and query, with 90,960 and 273,632 characters; their cleaned_html fields contained 83,433 and 255,662 characters. These observations limit what raw TF-IDF features mean. They neither establish a cause of D's score nor reject the item-text axis. No fit or score was changed.

[headroom/D_content_scope_review.json](<$PAIEC_SOURCE_ROOT/headroom/D_content_scope_review.json>)

```json
{
  "recorded_at_kst": "2026-10-09T04:09:00.878874+09:00",
  "kind": "Read-only public item-content scope inspection",
  "status": "INSPECTED_NARROW_SCOPE",
  "scope": "At most the first two content cells from each of four named public benchmarks. Only schema, field names, type categories, and string/payload lengths are retained; no prompts or assets are emitted.",
  "no_fits_or_score_changes": true,
  "no_new_corpus_pass": true,
  "benchmarks": [
    {
      "benchmark": "mind2web",
      "path": "paiec_baseline/payload/data/mind2web/items.parquet",
      "parquet_content_type": "string",
      "file_bytes": 522164413,
      "metadata_rows": 17153,
      "metadata_row_groups": 2,
      "inspection_api": "ParquetFile.iter_batches(batch_size=1, columns=['content']); next() called no more than twice",
      "inspected_cells": 2,
      "samples": [
        {
          "cell_index_from_file_start": 0,
          "is_null": false,
          "content_chars": 90960,
          "content_utf8_bytes": 90960,
          "content_encoding": "JSON serialized in string",
          "parsed_root_type": "dict",
          "json_field_names": [
            "candidate_node_ids",
            "cleaned_html",
            "query"
          ],
          "value_type_counts": {
            "dict": 1,
            "str": 456,
            "list": 1
          },
          "structural_content_type_counts": {},
          "max_container_depth": 2,
          "decoded_string_leaf_chars_total": 85414,
          "known_data_uri_media_payloads": 0,
          "known_data_uri_mime_types": {},
          "known_data_uri_payload_chars_total": 0,
          "known_data_uri_payload_fraction_of_raw_content_chars": 0.0,
          "long_base64_like_run_chars_total": 0,
          "long_base64_like_run_fraction_of_raw_content_chars": 0.0,
          "markup_string_leaf_chars_total": 83433,
          "other_string_leaf_chars_excluding_known_media": 85414,
          "leaf_string_path_summary": {
            "$.candidate_node_ids[]": {
              "strings": 454,
              "string_chars": 1816,
              "known_media_payload_chars": 0,
              "base64_like_run_chars": 0,
              "longest_base64_like_run_chars": 0,
              "markup_string_chars": 0
            },
            "$.cleaned_html": {
              "strings": 1,
              "string_chars": 83433,
              "known_media_payload_chars": 0,
              "base64_like_run_chars": 0,
              "longest_base64_like_run_chars": 0,
              "markup_string_chars": 83433
            },
            "$.query": {
              "strings": 1,
              "string_chars": 165,
              "known_media_payload_chars": 0,
              "base64_like_run_chars": 0,
              "longest_base64_like_run_chars": 0,
              "markup_string_chars": 0
            }
          },
          "interpretation": "No evidence of base64 dominance in this inspected cell; markup/code/ordinary text may still dominate."
        },
        {
          "cell_index_from_file_start": 1,
          "is_null": false,
          "content_chars": 273632,
          "content_utf8_bytes": 273632,
          "content_encoding": "JSON serialized in string",
          "parsed_root_type": "dict",
          "json_field_names": [
            "candidate_node_ids",
            "cleaned_html",
            "query"
          ],
          "value_type_counts": {
            "dict": 1,
            "str": 896,
            "list": 1
          },
          "structural_content_type_counts": {},
          "max_container_depth": 2,
          "decoded_string_leaf_chars_total": 260353,
          "known_data_uri_media_payloads": 0,
          "known_data_uri_mime_types": {},
          "known_data_uri_payload_chars_total": 0,
          "known_data_uri_payload_fraction_of_raw_content_chars": 0.0,
          "long_base64_like_run_chars_total": 0,
          "long_base64_like_run_fraction_of_raw_content_chars": 0.0,
          "markup_string_leaf_chars_total": 255662,
          "other_string_leaf_chars_excluding_known_media": 260353,
          "leaf_string_path_summary": {
            "$.candidate_node_ids[]": {
              "strings": 894,
              "string_chars": 4470,
              "known_media_payload_chars": 0,
              "base64_like_run_chars": 0,
              "longest_base64_like_run_chars": 0,
              "markup_string_chars": 0
            },
            "$.cleaned_html": {
              "strings": 1,
              "string_chars": 255662,
              "known_media_payload_chars": 0,
              "base64_like_run_chars": 0,
              "longest_base64_like_run_chars": 0,
              "markup_string_chars": 255662
            },
            "$.query": {
              "strings": 1,
              "string_chars": 221,
              "known_media_payload_chars": 0,
              "base64_like_run_chars": 0,
              "longest_base64_like_run_chars": 0,
              "markup_string_chars": 0
            }
          },
          "interpretation": "No evidence of base64 dominance in this inspected cell; markup/code/ordinary text may still dominate."
        }
      ]
    },
    {
      "benchmark": "naturalreasoning",
      "path": "paiec_baseline/payload/data/naturalreasoning/items.parquet",
      "parquet_content_type": "string",
      "file_bytes": 379249825,
      "metadata_rows": 1145824,
      "metadata_row_groups": 115,
      "inspection_api": "ParquetFile.iter_batches(batch_size=1, columns=['content']); next() called no more than twice",
      "inspected_cells": 2,
      "samples": [
        {
          "cell_index_from_file_start": 0,
          "is_null": false,
          "content_chars": 256,
          "content_utf8_bytes": 256,
          "content_encoding": "plain string or non-JSON serialized string",
          "parsed_root_type": "str",
          "json_field_names": [],
          "value_type_counts": {
            "str": 1
          },
          "structural_content_type_counts": {},
          "max_container_depth": 0,
          "decoded_string_leaf_chars_total": 256,
          "known_data_uri_media_payloads": 0,
          "known_data_uri_mime_types": {},
          "known_data_uri_payload_chars_total": 0,
          "known_data_uri_payload_fraction_of_raw_content_chars": 0.0,
          "long_base64_like_run_chars_total": 0,
          "long_base64_like_run_fraction_of_raw_content_chars": 0.0,
          "markup_string_leaf_chars_total": 0,
          "other_string_leaf_chars_excluding_known_media": 256,
          "leaf_string_path_summary": {
            "$": {
              "strings": 1,
              "string_chars": 256,
              "known_media_payload_chars": 0,
              "base64_like_run_chars": 0,
              "longest_base64_like_run_chars": 0,
              "markup_string_chars": 0
            }
          },
          "interpretation": "No evidence of base64 dominance in this inspected cell; markup/code/ordinary text may still dominate."
        },
        {
          "cell_index_from_file_start": 1,
          "is_null": false,
          "content_chars": 383,
          "content_utf8_bytes": 383,
          "content_encoding": "plain string or non-JSON serialized string",
          "parsed_root_type": "str",
          "json_field_names": [],
          "value_type_counts": {
            "str": 1
          },
          "structural_content_type_counts": {},
          "max_container_depth": 0,
          "decoded_string_leaf_chars_total": 383,
          "known_data_uri_media_payloads": 0,
          "known_data_uri_mime_types": {},
          "known_data_uri_payload_chars_total": 0,
          "known_data_uri_payload_fraction_of_raw_content_chars": 0.0,
          "long_base64_like_run_chars_total": 0,
          "long_base64_like_run_fraction_of_raw_content_chars": 0.0,
          "markup_string_leaf_chars_total": 0,
          "other_string_leaf_chars_excluding_known_media": 383,
          "leaf_string_path_summary": {
            "$": {
              "strings": 1,
              "string_chars": 383,
              "known_media_payload_chars": 0,
              "base64_like_run_chars": 0,
              "longest_base64_like_run_chars": 0,
              "markup_string_chars": 0
            }
          },
          "interpretation": "No evidence of base64 dominance in this inspected cell; markup/code/ordinary text may still dominate."
        }
      ]
    },
    {
      "benchmark": "robust_reasoning_benchmark",
      "path": "paiec_baseline/payload/data/robust_reasoning_benchmark/items.parquet",
      "parquet_content_type": "string",
      "file_bytes": 282596765,
      "metadata_rows": 4895,
      "metadata_row_groups": 1,
      "inspection_api": "ParquetFile.iter_batches(batch_size=1, columns=['content']); next() called no more than twice",
      "inspected_cells": 2,
      "samples": [
        {
          "cell_index_from_file_start": 0,
          "is_null": false,
          "content_chars": 641,
          "content_utf8_bytes": 641,
          "content_encoding": "plain string or non-JSON serialized string",
          "parsed_root_type": "str",
          "json_field_names": [],
          "value_type_counts": {
            "str": 1
          },
          "structural_content_type_counts": {},
          "max_container_depth": 0,
          "decoded_string_leaf_chars_total": 641,
          "known_data_uri_media_payloads": 0,
          "known_data_uri_mime_types": {},
          "known_data_uri_payload_chars_total": 0,
          "known_data_uri_payload_fraction_of_raw_content_chars": 0.0,
          "long_base64_like_run_chars_total": 0,
          "long_base64_like_run_fraction_of_raw_content_chars": 0.0,
          "markup_string_leaf_chars_total": 0,
          "other_string_leaf_chars_excluding_known_media": 641,
          "leaf_string_path_summary": {
            "$": {
              "strings": 1,
              "string_chars": 641,
              "known_media_payload_chars": 0,
              "base64_like_run_chars": 0,
              "longest_base64_like_run_chars": 0,
              "markup_string_chars": 0
            }
          },
          "interpretation": "No evidence of base64 dominance in this inspected cell; markup/code/ordinary text may still dominate."
        },
        {
          "cell_index_from_file_start": 1,
          "is_null": false,
          "content_chars": 435,
          "content_utf8_bytes": 435,
          "content_encoding": "plain string or non-JSON serialized string",
          "parsed_root_type": "str",
          "json_field_names": [],
          "value_type_counts": {
            "str": 1
          },
          "structural_content_type_counts": {},
          "max_container_depth": 0,
          "decoded_string_leaf_chars_total": 435,
          "known_data_uri_media_payloads": 0,
          "known_data_uri_mime_types": {},
          "known_data_uri_payload_chars_total": 0,
          "known_data_uri_payload_fraction_of_raw_content_chars": 0.0,
          "long_base64_like_run_chars_total": 0,
          "long_base64_like_run_fraction_of_raw_content_chars": 0.0,
          "markup_string_leaf_chars_total": 0,
          "other_string_leaf_chars_excluding_known_media": 435,
          "leaf_string_path_summary": {
            "$": {
              "strings": 1,
              "string_chars": 435,
              "known_media_payload_chars": 0,
              "base64_like_run_chars": 0,
              "longest_base64_like_run_chars": 0,
              "markup_string_chars": 0
            }
          },
          "interpretation": "No evidence of base64 dominance in this inspected cell; markup/code/ordinary text may still dominate."
        }
      ]
    },
    {
      "benchmark": "swe_smith",
      "path": "paiec_baseline/payload/data/swe_smith/items.parquet",
      "parquet_content_type": "string",
      "file_bytes": 244658364,
      "metadata_rows": 15616,
      "metadata_row_groups": 2,
      "inspection_api": "ParquetFile.iter_batches(batch_size=1, columns=['content']); next() called no more than twice",
      "inspected_cells": 2,
      "samples": [
        {
          "cell_index_from_file_start": 0,
          "is_null": false,
          "content_chars": 1517,
          "content_utf8_bytes": 1517,
          "content_encoding": "plain string or non-JSON serialized string",
          "parsed_root_type": "str",
          "json_field_names": [],
          "value_type_counts": {
            "str": 1
          },
          "structural_content_type_counts": {},
          "max_container_depth": 0,
          "decoded_string_leaf_chars_total": 1517,
          "known_data_uri_media_payloads": 0,
          "known_data_uri_mime_types": {},
          "known_data_uri_payload_chars_total": 0,
          "known_data_uri_payload_fraction_of_raw_content_chars": 0.0,
          "long_base64_like_run_chars_total": 0,
          "long_base64_like_run_fraction_of_raw_content_chars": 0.0,
          "markup_string_leaf_chars_total": 0,
          "other_string_leaf_chars_excluding_known_media": 1517,
          "leaf_string_path_summary": {
            "$": {
              "strings": 1,
              "string_chars": 1517,
              "known_media_payload_chars": 0,
              "base64_like_run_chars": 0,
              "longest_base64_like_run_chars": 0,
              "markup_string_chars": 0
            }
          },
          "interpretation": "No evidence of base64 dominance in this inspected cell; markup/code/ordinary text may still dominate."
        },
        {
          "cell_index_from_file_start": 1,
          "is_null": false,
          "content_chars": 1839,
          "content_utf8_bytes": 1839,
          "content_encoding": "plain string or non-JSON serialized string",
          "parsed_root_type": "str",
          "json_field_names": [],
          "value_type_counts": {
            "str": 1
          },
          "structural_content_type_counts": {},
          "max_container_depth": 0,
          "decoded_string_leaf_chars_total": 1839,
          "known_data_uri_media_payloads": 0,
          "known_data_uri_mime_types": {},
          "known_data_uri_payload_chars_total": 0,
          "known_data_uri_payload_fraction_of_raw_content_chars": 0.0,
          "long_base64_like_run_chars_total": 0,
          "long_base64_like_run_fraction_of_raw_content_chars": 0.0,
          "markup_string_leaf_chars_total": 0,
          "other_string_leaf_chars_excluding_known_media": 1839,
          "leaf_string_path_summary": {
            "$": {
              "strings": 1,
              "string_chars": 1839,
              "known_media_payload_chars": 0,
              "base64_like_run_chars": 0,
              "longest_base64_like_run_chars": 0,
              "markup_string_chars": 0
            }
          },
          "interpretation": "No evidence of base64 dominance in this inspected cell; markup/code/ordinary text may still dominate."
        }
      ]
    }
  ],
  "remaining_unmeasured": [
    "The remaining rows of each file are UNMEASURED by this inspection. The first two cells are not a random or representative sample.",
    "Corpus-wide base64/media/markup prevalence is UNMEASURED.",
    "The TF-IDF vocabulary entries selected from these particular cells, their fitted weights, and their effects on D scores are UNMEASURED.",
    "Arrow may internally decompress a row group while producing one-row batches; inspection consumes only two content cell values per benchmark."
  ],
  "interpretation_limits": [
    "Long alphanumeric/base64-like runs are a heuristic unless they occur in a recognized data MIME URI. They can include long ordinary identifiers.",
    "Markup and source code are textual inputs, but raw serialized content may give TF-IDF features a different meaning from natural-language item difficulty.",
    "This scope check does not reject the item-text axis or establish the cause of D performance."
  ]
}
```

### Final numerical audit

[headroom/numerical_validation.json](<$PAIEC_SOURCE_ROOT/headroom/numerical_validation.json>)

```json
{
  "all_pass": true,
  "checks": {
    "unique_raw_pairs": true,
    "all_eligible_pairs": true,
    "benchmark_pair_counts": true,
    "fold_hash": true,
    "positive_evaluation": true,
    "frozen_finite_and_bounds": true,
    "frozen_weights": true,
    "frozen_equal_pair_mean": true,
    "frozen_budget_means": true,
    "frozen_ALC_delta": true,
    "frozen_B0_delta": true,
    "frozen_fold0_means": true,
    "frozen_fold1_means": true,
    "frozen_fold2_means": true,
    "frozen_fold3_means": true,
    "frozen_fold4_means": true,
    "frozen_fold5_means": true,
    "A_finite_and_bounds": true,
    "A_weights": true,
    "A_equal_pair_mean": true,
    "A_budget_means": true,
    "A_ALC_delta": true,
    "A_B0_delta": true,
    "A_fold0_means": true,
    "A_fold1_means": true,
    "A_fold2_means": true,
    "A_fold3_means": true,
    "A_fold4_means": true,
    "A_fold5_means": true,
    "A_cluster_ci": true,
    "A_fold_wins": true,
    "A_fold0_ci": true,
    "A_fold1_ci": true,
    "A_fold2_ci": true,
    "A_fold3_ci": true,
    "A_fold4_ci": true,
    "A_fold5_ci": true,
    "B_finite_and_bounds": true,
    "B_weights": true,
    "B_equal_pair_mean": true,
    "B_budget_means": true,
    "B_ALC_delta": true,
    "B_B0_delta": true,
    "B_fold0_means": true,
    "B_fold1_means": true,
    "B_fold2_means": true,
    "B_fold3_means": true,
    "B_fold4_means": true,
    "B_fold5_means": true,
    "B_cluster_ci": true,
    "B_fold_wins": true,
    "B_fold0_ci": true,
    "B_fold1_ci": true,
    "B_fold2_ci": true,
    "B_fold3_ci": true,
    "B_fold4_ci": true,
    "B_fold5_ci": true,
    "C_finite_and_bounds": true,
    "C_weights": true,
    "C_equal_pair_mean": true,
    "C_budget_means": true,
    "C_ALC_delta": true,
    "C_B0_delta": true,
    "C_fold0_means": true,
    "C_fold1_means": true,
    "C_fold2_means": true,
    "C_fold3_means": true,
    "C_fold4_means": true,
    "C_fold5_means": true,
    "C_cluster_ci": true,
    "C_fold_wins": true,
    "C_fold0_ci": true,
    "C_fold1_ci": true,
    "C_fold2_ci": true,
    "C_fold3_ci": true,
    "C_fold4_ci": true,
    "C_fold5_ci": true,
    "D_finite_and_bounds": true,
    "D_weights": true,
    "D_equal_pair_mean": true,
    "D_budget_means": true,
    "D_ALC_delta": true,
    "D_B0_delta": true,
    "D_fold0_means": true,
    "D_fold1_means": true,
    "D_fold2_means": true,
    "D_fold3_means": true,
    "D_fold4_means": true,
    "D_fold5_means": true,
    "D_cluster_ci": true,
    "D_fold_wins": true,
    "D_fold0_ci": true,
    "D_fold1_ci": true,
    "D_fold2_ci": true,
    "D_fold3_ci": true,
    "D_fold4_ci": true,
    "D_fold5_ci": true,
    "A_static_curve": true,
    "B_static_curve": true,
    "D_static_curve": true,
    "A_pair_constant_floor": true,
    "reuse_B0_zero": true,
    "reuse_nested_and_bounds": true,
    "reuse_overall_B0_summary": true,
    "reuse_overall_B1_summary": true,
    "reuse_overall_B3_summary": true,
    "reuse_overall_B7_summary": true,
    "reuse_overall_B15_summary": true,
    "reuse_overall_B31_summary": true,
    "reuse_0_B0_summary": true,
    "reuse_0_B1_summary": true,
    "reuse_0_B3_summary": true,
    "reuse_0_B7_summary": true,
    "reuse_0_B15_summary": true,
    "reuse_0_B31_summary": true,
    "reuse_1_B0_summary": true,
    "reuse_1_B1_summary": true,
    "reuse_1_B3_summary": true,
    "reuse_1_B7_summary": true,
    "reuse_1_B15_summary": true,
    "reuse_1_B31_summary": true,
    "reuse_2_B0_summary": true,
    "reuse_2_B1_summary": true,
    "reuse_2_B3_summary": true,
    "reuse_2_B7_summary": true,
    "reuse_2_B15_summary": true,
    "reuse_2_B31_summary": true,
    "reuse_3_B0_summary": true,
    "reuse_3_B1_summary": true,
    "reuse_3_B3_summary": true,
    "reuse_3_B7_summary": true,
    "reuse_3_B15_summary": true,
    "reuse_3_B31_summary": true,
    "reuse_4_B0_summary": true,
    "reuse_4_B1_summary": true,
    "reuse_4_B3_summary": true,
    "reuse_4_B7_summary": true,
    "reuse_4_B15_summary": true,
    "reuse_4_B31_summary": true,
    "reuse_5_B0_summary": true,
    "reuse_5_B1_summary": true,
    "reuse_5_B3_summary": true,
    "reuse_5_B7_summary": true,
    "reuse_5_B15_summary": true,
    "reuse_5_B31_summary": true,
    "D_independent_process_pairing": true
  },
  "checks_count": 146,
  "serialization_note": "The first final-audit attempt reached JSON serialization but failed on NumPy Boolean flags. Flags now use native bool; calculations and measured scores are unchanged. The same final inputs were audited again.",
  "final_summary_sha256": "6df88cb6c15b78c16159cab9c6c796e9036dd79eb971a94a90e9ed769f987b4e",
  "pairs_sha256": "4acb2f8cdce30e03a1243120b89eb68921daa14ba3a31510d9ce2225d5620826",
  "validator_sha256": "617cf27b13239a3c2ac17ca4629218601789267d52dd7afca2c95e65ee674f92",
  "maximum_errors": {
    "frozen_ALC": 1.6653345369377348e-16,
    "A_ALC": 1.3877787807814457e-16,
    "A_CI": 0.0,
    "A_fold0_CI": 6.938893903907228e-18,
    "A_fold1_CI": 3.469446951953614e-18,
    "A_fold2_CI": 6.938893903907228e-18,
    "A_fold3_CI": 6.938893903907228e-18,
    "A_fold4_CI": 1.0408340855860843e-17,
    "A_fold5_CI": 0.0,
    "B_ALC": 1.3877787807814457e-16,
    "B_CI": 0.0,
    "B_fold0_CI": 0.0,
    "B_fold1_CI": 2.7755575615628914e-17,
    "B_fold2_CI": 2.7755575615628914e-17,
    "B_fold3_CI": 0.0,
    "B_fold4_CI": 2.7755575615628914e-17,
    "B_fold5_CI": 4.163336342344337e-17,
    "C_ALC": 1.6653345369377348e-16,
    "C_CI": 3.469446951953614e-18,
    "C_fold0_CI": 1.734723475976807e-18,
    "C_fold1_CI": 6.938893903907228e-18,
    "C_fold2_CI": 1.734723475976807e-18,
    "C_fold3_CI": 1.734723475976807e-18,
    "C_fold4_CI": 8.673617379884035e-19,
    "C_fold5_CI": 8.673617379884035e-19,
    "D_ALC": 2.220446049250313e-16,
    "D_CI": 0.0,
    "D_fold0_CI": 0.0,
    "D_fold1_CI": 0.0,
    "D_fold2_CI": 5.551115123125783e-17,
    "D_fold3_CI": 2.7755575615628914e-17,
    "D_fold4_CI": 2.7755575615628914e-17,
    "D_fold5_CI": 6.938893903907228e-18
  },
  "pairs": 13023,
  "benchmarks": 145,
  "bootstrap_repetitions": 2000,
  "bootstrap_seed": 0,
  "wall_seconds": 0.7855215407907963
}
```

The first final-audit attempt completed its calculations but failed while serializing NumPy boolean check values to JSON. The helper converted check values to native booleans and was rerun; the saved measurement scores were unchanged. That first attempt did not produce a completed validation artifact. Its separate wall duration is UNMEASURED; the final audit's timer covers the successful rerun.

### Protected files after execution

[headroom/frozen_integrity_after.json](<$PAIEC_SOURCE_ROOT/headroom/frozen_integrity_after.json>)

```json
{
  "status": "PASS",
  "all_pass": true,
  "checked_at_kst": "2026-10-09T04:38:12.122081+09:00",
  "scope": "Protected content, sizes, mtimes and packaged/runtime identity after final summary",
  "baseline_manifest": "$PAIEC_SOURCE_ROOT/headroom/frozen_integrity_before.json",
  "baseline_manifest_sha256": "ec10120e0c4a0a6bfc75b47d834fba1dc7b87aaaedf3fe5f905878b805588fe3",
  "final_summary_sha256": "6df88cb6c15b78c16159cab9c6c796e9036dd79eb971a94a90e9ed769f987b4e",
  "files_expected": 5,
  "files_checked": 5,
  "files_passed": 5,
  "required_zip_prefix_matches": true,
  "zip_members": [
    {
      "member": "model.py",
      "sha256": "1d84ecb67c8b772a3719078bf2ca067d2bb0802ba36489e45181d4886bd4dcc6",
      "bytes": 7275,
      "baseline_sha256_matches": true,
      "local_same_bytes": true
    },
    {
      "member": "prior.json",
      "sha256": "1cc7b5a59223fc8d61e2e805c40063b672dcbce9043206720b30e42c5d66da55",
      "bytes": 4356693,
      "baseline_sha256_matches": true,
      "local_same_bytes": true
    },
    {
      "member": "README.md",
      "sha256": "e6cf7533bc5b39ec15d85213584c1831431f93c03ea3036fbdffa5d54110455e",
      "bytes": 637,
      "baseline_sha256_matches": true,
      "local_same_bytes": true
    }
  ],
  "errors": [],
  "wall_seconds": 0.01495808269828558,
  "files": [
    {
      "relative_path": "irt_shrink/model.py",
      "expected_sha256": "1d84ecb67c8b772a3719078bf2ca067d2bb0802ba36489e45181d4886bd4dcc6",
      "expected_bytes": 7275,
      "expected_mtime_ns": 1791474611422539670,
      "status": "PASS",
      "sha256": "1d84ecb67c8b772a3719078bf2ca067d2bb0802ba36489e45181d4886bd4dcc6",
      "bytes": 7275,
      "mtime_ns": 1791474611422539670,
      "content_unchanged": true,
      "size_unchanged": true,
      "mtime_unchanged": true
    },
    {
      "relative_path": "irt_shrink/train_prior.py",
      "expected_sha256": "6403fc88dc879aaaa32eab883f31655c69bc392a3f82f4b7daec6bb68f2c9322",
      "expected_bytes": 6489,
      "expected_mtime_ns": 1791460436149199899,
      "status": "PASS",
      "sha256": "6403fc88dc879aaaa32eab883f31655c69bc392a3f82f4b7daec6bb68f2c9322",
      "bytes": 6489,
      "mtime_ns": 1791460436149199899,
      "content_unchanged": true,
      "size_unchanged": true,
      "mtime_unchanged": true
    },
    {
      "relative_path": "irt_shrink/lobo_eval.py",
      "expected_sha256": "3f29cd9b1f2a3034f42867c8f3eebb291325c9597c92d2e3ce1294b03549e197",
      "expected_bytes": 7428,
      "expected_mtime_ns": 1791474611423483107,
      "status": "PASS",
      "sha256": "3f29cd9b1f2a3034f42867c8f3eebb291325c9597c92d2e3ce1294b03549e197",
      "bytes": 7428,
      "mtime_ns": 1791474611423483107,
      "content_unchanged": true,
      "size_unchanged": true,
      "mtime_unchanged": true
    },
    {
      "relative_path": "irt_shrink/prior.json",
      "expected_sha256": "1cc7b5a59223fc8d61e2e805c40063b672dcbce9043206720b30e42c5d66da55",
      "expected_bytes": 4356693,
      "expected_mtime_ns": 1791463170637661238,
      "status": "PASS",
      "sha256": "1cc7b5a59223fc8d61e2e805c40063b672dcbce9043206720b30e42c5d66da55",
      "bytes": 4356693,
      "mtime_ns": 1791463170637661238,
      "content_unchanged": true,
      "size_unchanged": true,
      "mtime_unchanged": true
    },
    {
      "relative_path": "irt_shrink/dist/irt_shrink.zip",
      "expected_sha256": "6e7f6a4668a9b485e25350e889881c0b630e9d48ad25829ac80a0f0e5d9f2368",
      "expected_bytes": 382470,
      "expected_mtime_ns": 1791474647246592275,
      "status": "PASS",
      "sha256": "6e7f6a4668a9b485e25350e889881c0b630e9d48ad25829ac80a0f0e5d9f2368",
      "bytes": 382470,
      "mtime_ns": 1791474647246592275,
      "content_unchanged": true,
      "size_unchanged": true,
      "mtime_unchanged": true
    }
  ]
}
```

## Wall times and execution deviations

| Stage | Recorded wall seconds | Scope |
| --- | --- | --- |
| Overall observed elapsed | 9248.094 | Recorded T0 reproduction start through this report timestamp; includes concurrent work, retries and checks |
| T0 clone | 0.870 | Fresh clone tool call |
| T0 reproduction | 0.140 | Build/check/hash |
| T1 | 273.244 | First task-created item file or hardlink creation to final target verification, including download retries; excludes metadata preflight |
| T2 preparation | 136.799 | Successful binary-target/prior preparation |
| T2 resumed D + assembly | 4425.058 | Resumed assembler text stages, parallel-worker waits and summary only; initial/interrupted D attempts excluded |
| Initial streaming D process | 3146.000 | Streaming D process elapsed through retained fold 0 checkpoint; SIGINT after complete fold 0 CSV and fit metadata, before any completed fold 1 output; includes imports/counting/fit/scoring; excludes earlier failed D attempts. Process elapsed from ps, not a perf-counter stage timer. |
| Interrupted extra D fold-5 worker | 385.083 | Log creation through last write only; no completed fold; not precise process/perf-counter elapsed |
| Fixture validation | 0.237 | Implementation fixtures only |
| Final numerical audit | 0.786 | Successful saved final audit only; first serialization-failed attempt excluded |
| Protected files after execution | 0.015 | Final protected-source/ZIP verification |
| Source input audit | 2.296 | 489 preserved-table digests |
| Initial A-C segment before SIGINT | ~706; exact duration UNMEASURED | Approximately 11m46s; completed fold 0 and afrimedqa checkpoint retained |
| ac_wall_0_1_2_3_4_5.json | 3192.870 | Resumed A-C segment only; initial segment excluded; concurrent with D, not total A-C elapsed |
| text_wall_0_1_2.json | 4033.476 | Post-resume D segment only; requested=[0, 1, 2]; executed=[1, 2]; skipped=[0]; per-fold seconds={'1': 2181.6062644999474, '2': 1849.7931564999744}; parallel costs do not sum to elapsed |
| text_wall_3_4_5.json | 6222.535 | Post-resume D segment only; requested=[3, 4, 5]; executed=[3, 4, 5]; skipped=[]; per-fold seconds={'3': 2664.5497364168987, '4': 2141.080066249706, '5': 1414.7117699170485}; parallel costs do not sum to elapsed |

Overall observed elapsed is computed directly from `2026-10-09T02:06:17.065886+09:00` to `2026-10-09T04:40:25.160227+09:00`, without summing concurrent track timers. Its scope includes all work since the recorded anchor-build start; the root execution and initial clone may have started earlier. The initial A-C segment's approximately 706 seconds are separate from the resumed ac_wall JSON timers; those JSON values must not be interpreted as the whole A-C runtime.

D was distributed among resumed text workers, including requested subsets 0/1/2, 3/4/5 and a dedicated fold-5 worker. Actual executed/skipped lists are taken from every text_wall_*.json file above; completed hash-validated folds are skipped instead of being adopted twice. These are orchestration records, not additional scientific methods. The initial streaming worker (PID 59515) had reached approximately 3.2 million training-document counts after about 20 minutes at an observation before any D score completed. Its process elapsed through the eventual retained fold-0 checkpoint, when available, is recorded separately in text_initial_segment.json at one-second ps resolution, followed by SIGINT after fold 0 was saved and before any completed fold-1 output. The process had already entered the next Counter pass. This includes its successful retained fold-0 fit, excludes previous failed attempts, and is not a perf-counter stage timer. Resumed text_wall JSON files cover only their worker segments. They are not complete D cost estimates and are not summed with one another or with concurrent A-C stages. Canonical text_fits.json and the six validated markers, rather than worker process state, establish final fold completeness.

The original streaming worker log is preserved separately as [headroom/text_initial_segment.log](<$PAIEC_SOURCE_ROOT/headroom/text_initial_segment.log>); resumed measure.log has a separate process scope. The initial log and process-elapsed ledger are cost/provenance evidence, while the retained complete fold-0 CSV and fit metadata are the scientific result artifacts.

The extra dedicated fold-5 attempt (PID 67761) was interrupted with SIGINT for observed disk/swap pressure, before any selected sparse matrix or complete CSV/fit/marker existed. Its log lifetime was approximately 385 seconds, not a precise successful-process timer. No completed scores were discarded, no estimator parameters changed, and the existing 3/4/5 worker retained responsibility for fold 5. The cost-only evidence is [headroom/text_5_interrupted.json](<$PAIEC_SOURCE_ROOT/headroom/text_5_interrupted.json>) and [headroom/text_5.log](<$PAIEC_SOURCE_ROOT/headroom/text_5.log>). Execution snapshots showed about 121–140 MiB available disk and 18.84 GB swap usage around interruption, then about 2.1 GiB disk availability while reported swap usage remained 18.84 GB. No files were deleted for that recovery. The cause of the observed disk recovery is UNMEASURED; these observations do not prove causality. No further parallel D worker was launched after this interruption.

Concurrent stage times are not summed. The first failed preparation duration is UNMEASURED; its exception was observed in execution outputs, while prepare.log was overwritten by the successful rerun. An initial text-preprocessing attempt was interrupted after approximately two minutes to run A-C and D concurrently; it produced no completed result metrics, and its log was also overwritten by the rerun. Those setup/retry costs are distinct from the successful stage timers.

A later default-vocabulary TF-IDF attempt was interrupted after approximately 11–12 minutes before any D result completed. The process sample recorded physical footprint 18.3G and peak 18.7G; execution outputs observed roughly 550 MB free disk. A further resident-text-corpus attempt was interrupted after approximately one minute with about 20 GB RSS, also before any D result. Exact interrupted-attempt wall durations are UNMEASURED; successful-stage timers exclude these attempts. [headroom/text_default_interrupted.log](<$PAIEC_SOURCE_ROOT/headroom/text_default_interrupted.log>), [headroom/text_sample.txt](<$PAIEC_SOURCE_ROOT/headroom/text_sample.txt>) and [headroom/text_resident_corpus_interrupted.log](<$PAIEC_SOURCE_ROOT/headroom/text_resident_corpus_interrupted.log>) are cost/resource diagnostics, not completed method-score evidence. The optimized numeric corpus and benchmark-text generator address the resident-text overhead; feature selection is addressed by the two-pass Counter implementation described above.

A later one-second sample of the original streaming D process is preserved in [headroom/text_streaming_sample.txt](<$PAIEC_SOURCE_ROOT/headroom/text_streaming_sample.txt>). It reported 6.3G physical footprint and 11.8G peak-to-that-sample, with tokenizer/regex work prominent in the captured stack. These are sampled resource observations. Final peak footprint, complete worker runtime and any performance prognosis are not inferred from this sample.

All additional text_streaming_sample*.txt snapshots are hashed in the evidence table. Each physical-footprint value and peak value belongs to that sampling time, not to the final maximum over the run.

A post-completion resource-sampling request against PID 66699 returned 'no longer running'. It created no sample artifact and did not affect any fit or score. Its diagnostic wall duration is UNMEASURED; no sampling retry was needed.

The shell's `python` command was unavailable, so T0 used `python3` (Python 3.10.11). The measurement environment required scikit-learn installation in the isolated headroom environment. No protected predictor source was modified for installation or measurement.

Report interpreter: `$PAIEC_SOURCE_ROOT/headroom/.venv/bin/python`, Python `3.10.11`. Versions below describe the interpreter generating this report and should not be mistaken for independent environment provenance if a different interpreter is used:

| Package | Version |
| --- | --- |
| numpy | 2.2.6 |
| pandas | 2.3.3 |
| scipy | 1.15.3 |
| scikit-learn | 1.7.2 |
| pyarrow | 24.0.0 |

- Raw scoring units are 13,023 subject-ID pairs versus 12,972 old five-field configuration pairs. Eight colliding old keys collapse 51 additional raw IDs; the raw pairs now retain their equal score weights while the frozen predictor retains its original grouping.
- The per-pair split replaces the old shared item split. Fold hashes and benchmark RNG seeds match, but new subject-specific draws and acquisition counts change trajectories.
- Training-fold-refitted priors replace a literal all-public prior in primary LOBO to avoid held-out-label leakage. Original prior.json remains the frozen submission artifact.
- D is static at all budgets. Easiness smoothing, raw ability scale, ridge settings, C's variance presets and Oracle B's regularization were fixed without held-out optimization.
- Earliest recorded acquisition trial is a local convention; hosted selection equivalence is UNVERIFIED. Evaluation still includes every recorded binary response.
- C uses a content/features identity proxy and ignores response interactors. The source audit found 228,320 nonempty-interactor response rows in 6 of 163 tables: advprompter, emoji_attack, haiid, harmbench, jailbreakbench, tau2_bench.
- Full-public-pool acquisition reveals budget-limited labels from all eligible pairs. This can provide much denser evidence than hosted formative feedback's at-most-1,000 unique subject–item sample. Reuse and feasible-C scores are not forecasts under that sparse cap.
- Verified existing item files were hardlinked. Anonymous HF requests initially returned 401; existing local credentials were used only in process memory, never printed or saved.
- ENOSPC interrupted downloads/preparation despite reported free space. Completed items were preserved; only the task-created incomplete mind2web partial was discarded before retrying with one worker and a 300 MiB guard. All 163 final items completed locally.
- R2 fallback status was BLOCKED: API code 10042, Please enable R2 through the Cloudflare Dashboard.. Bucket created: False; objects uploaded: 0; public access: False; Worker deployed: False. Local completion resolved the storage dependency; no remote item fallback was used.
- Headroom files, downloaded public item tables and reviewable anchors are measurement outputs. No predictor change, submission, push, new production model or first-place claim is implied.

## Evidence hashes

SHA256 values below are computed when this report is generated. Individual dataset hashes in the appendices are the verified recorded values; no credential material is included.

| Evidence | SHA256 | Bytes |
| --- | --- | --- |
| [headroom/write_report.py](<$PAIEC_SOURCE_ROOT/headroom/write_report.py>) | `00edf998a7f606dfceab1f283a0a4cade3b343147a3cc2e13159b6a56f45983d` | 56,305 |
| [headroom/measure.py](<$PAIEC_SOURCE_ROOT/headroom/measure.py>) | `a2ed788351ff1029a72f3d4bfe6adc7a41b97b9c6c10c050a12cd705d4bb8248` | 31,319 |
| [headroom/T0.json](<$PAIEC_SOURCE_ROOT/headroom/T0.json>) | `5e51ba962c2f35d5ef4854378ea91bd2691460f3c26f45b80ba6883ccfef608f` | 3,053 |
| [headroom/T1.json](<$PAIEC_SOURCE_ROOT/headroom/T1.json>) | `c70cabe314a763bd373db6d24c71b7aaf6536eec9fc0976f28aa2d737bec9eb5` | 410,128 |
| [headroom/T1_items_inventory.tsv](<$PAIEC_SOURCE_ROOT/headroom/T1_items_inventory.tsv>) | `d47a68596592a17654027b9b19bf6da2f540b793415ec09df5526225f246a100` | 43,017 |
| [headroom/prepared.json](<$PAIEC_SOURCE_ROOT/headroom/prepared.json>) | `eb54323c439a4f68e8735788eb13a08c39836235fcff39e4c81b316174ca8697` | 25,317 |
| [headroom/pair_stats.csv](<$PAIEC_SOURCE_ROOT/headroom/pair_stats.csv>) | `74ed5d32c9f5714702384e43f79c7e0c58626ab186d5a48ca902a77aaa1f0ca6` | 4,406,392 |
| [headroom/text_fits.json](<$PAIEC_SOURCE_ROOT/headroom/text_fits.json>) | `79d1d41fb2707f2e12762c55496ba9c332ddf819ea2fb9c2e1758f0995530f43` | 1,562 |
| [headroom/summary.json](<$PAIEC_SOURCE_ROOT/headroom/summary.json>) | `6df88cb6c15b78c16159cab9c6c796e9036dd79eb971a94a90e9ed769f987b4e` | 24,018 |
| [headroom/pairs.csv](<$PAIEC_SOURCE_ROOT/headroom/pairs.csv>) | `4acb2f8cdce30e03a1243120b89eb68921daa14ba3a31510d9ce2225d5620826` | 14,519,039 |
| [headroom/independent_validation.json](<$PAIEC_SOURCE_ROOT/headroom/independent_validation.json>) | `87575bc309666b194bb0ac9ea60c8a8b20afc12d41d24bb3ba6c5e292bb84faa` | 5,475 |
| [headroom/numerical_validation.json](<$PAIEC_SOURCE_ROOT/headroom/numerical_validation.json>) | `e4f84d56551dd416b5b29bb3a98f05a209c070a9bbdd12cf52db8bbd57a35ee4` | 6,146 |
| [headroom/required_inputs_integrity.json](<$PAIEC_SOURCE_ROOT/headroom/required_inputs_integrity.json>) | `7b09329e088a819026b6a8f74645e8fe96f0f613009ebdf434ef524a02f04c5f` | 184,107 |
| [headroom/interactors_inventory.json](<$PAIEC_SOURCE_ROOT/headroom/interactors_inventory.json>) | `06acaad7430af8d31f69f096f308a3f5fb47a82600597b58a14e4db29e4894db` | 19,551 |
| [headroom/frozen_integrity_before.json](<$PAIEC_SOURCE_ROOT/headroom/frozen_integrity_before.json>) | `ec10120e0c4a0a6bfc75b47d834fba1dc7b87aaaedf3fe5f905878b805588fe3` | 2,374 |
| [headroom/frozen_integrity_after.json](<$PAIEC_SOURCE_ROOT/headroom/frozen_integrity_after.json>) | `6d6b74469703e5caa8e4a9c50231ac14ab2d982c2d12b3c1526760a55e07ed7e` | 3,888 |
| [headroom/R2.json](<$PAIEC_SOURCE_ROOT/headroom/R2.json>) | `481314fcc8471ff13fdb669dea0dcd7ad4faf67e39647aff1fe9b610eb182d37` | 926 |
| [headroom/protocol_audit.md](<$PAIEC_SOURCE_ROOT/headroom/protocol_audit.md>) | `86d24d17e4a18d0efe7231d786cb20bcc585845e526ba1e6e735980b59884930` | 12,699 |
| [headroom/spec_output_audit.md](<$PAIEC_SOURCE_ROOT/headroom/spec_output_audit.md>) | `093b885940f6f40f1e9c6f22ffe64d7974f60654a5b169b9f58c514c5926c792` | 3,354 |
| [headroom/orchestration_validation.json](<$PAIEC_SOURCE_ROOT/headroom/orchestration_validation.json>) | `e82c2c554d80d2ec9b33b72cf4101ed84e83c8de3afbc7eee53e59dbd120f772` | 1,065 |
| [headroom/orchestration_independent_review.json](<$PAIEC_SOURCE_ROOT/headroom/orchestration_independent_review.json>) | `94736c5e025aadc63393d79f4a55ccfcf9b457d808b326cf877ebbcf483c69bb` | 2,392 |
| [headroom/D0_sanity_review.json](<$PAIEC_SOURCE_ROOT/headroom/D0_sanity_review.json>) | `a1abe2703188de76eb4390be1bb4ecc840c49f2ff34077a0659ed4fbbc95b7ac` | 21,138 |
| [headroom/D_content_scope_review.json](<$PAIEC_SOURCE_ROOT/headroom/D_content_scope_review.json>) | `0365b744228c2530cd2f8f47916f4b1b17b4c039bd8e3c80f106af951014623c` | 15,905 |
| [headroom/validate_numbers.py](<$PAIEC_SOURCE_ROOT/headroom/validate_numbers.py>) | `617cf27b13239a3c2ac17ca4629218601789267d52dd7afca2c95e65ee674f92` | 6,627 |
| [headroom/check_frozen_integrity.py](<$PAIEC_SOURCE_ROOT/headroom/check_frozen_integrity.py>) | `f3bc3d31fb44ea976b16fd371263bf97b11ebedf640bdf5485633304be98b6f3` | 4,899 |
| [headroom/plot_summary.py](<$PAIEC_SOURCE_ROOT/headroom/plot_summary.py>) | `24efecb459d72330c3a829ba9303c4ce96a1f0ef380b954170fd634502aa1a13` | 8,195 |
| [headroom/headroom_curves.png](<$PAIEC_SOURCE_ROOT/headroom/headroom_curves.png>) | `2f6221bdd8d7845279bb64f4e2db4aff3a0e2c9cbea07194abfc177b8fd408b2` | 197,851 |
| [headroom/headroom_curves.svg](<$PAIEC_SOURCE_ROOT/headroom/headroom_curves.svg>) | `11c99e442d838e34ca8771e1a4d9247ac805e4d6535526351950946291ee1b8e` | 32,034 |
| [headroom/MEASUREMENT_PLAN.json](<$PAIEC_SOURCE_ROOT/headroom/MEASUREMENT_PLAN.json>) | `1f015a4a385ac632e5eaebbf22c1f731514a739e1a4cd8f1ad51d9e15a7b9168` | 3,498 |
| [headroom/text_default_interrupted.log](<$PAIEC_SOURCE_ROOT/headroom/text_default_interrupted.log>) | `4c3f7e90b9de6fcd07e92f9079abcc9fe030fedf3eac5247a4fd56d7e79de078` | 1,244 |
| [headroom/text_sample.txt](<$PAIEC_SOURCE_ROOT/headroom/text_sample.txt>) | `4d1522be93f3869121c494d5f99aef2457c865387e7309979d6c8cf4633eee28` | 170,898 |
| [headroom/text_sample_command.log](<$PAIEC_SOURCE_ROOT/headroom/text_sample_command.log>) | `8b710281293a691309adaebb9417cbd21f514013cd1acaa7ddde41460337c308` | 199 |
| [headroom/text_resident_corpus_interrupted.log](<$PAIEC_SOURCE_ROOT/headroom/text_resident_corpus_interrupted.log>) | `6b125fa605055ca40a99202358352cac54cdc094a86304f5af1350f9ef2dcaeb` | 794 |
| [headroom/text_initial_segment.json](<$PAIEC_SOURCE_ROOT/headroom/text_initial_segment.json>) | `48d528198d07650bee55549652ccd0df738e8a42c19b5223acd44acc60ea9d43` | 857 |
| [headroom/text_initial_segment.log](<$PAIEC_SOURCE_ROOT/headroom/text_initial_segment.log>) | `0fc093ca4868f4265b2a55b2edf9e1fd7f40532749a157e5acd809a2fc493ede` | 3,962 |
| [headroom/text_5_interrupted.json](<$PAIEC_SOURCE_ROOT/headroom/text_5_interrupted.json>) | `7d81b773113f4c6c2eff4b8f2c59198b69fa6014f6ccd209721cc32073f265c4` | 1,593 |
| [headroom/text_5.log](<$PAIEC_SOURCE_ROOT/headroom/text_5.log>) | `29d24a8475852c2a58a81621c0791256bf15b5aaa20e00cef212510f1540f893` | 1,703 |
| [headroom/measure.log](<$PAIEC_SOURCE_ROOT/headroom/measure.log>) | `637b6724d65eb23a5b62590a36bda0361e95278e94e37844f27fab0d02219da1` | 9,422 |
| [headroom/text_3_4_5.log](<$PAIEC_SOURCE_ROOT/headroom/text_3_4_5.log>) | `6006e8728eebebc85afd281f7fa07677f522e5aaaeb46c321dc34192e1339521` | 8,419 |
| [headroom/text_stream_sample_command.log](<$PAIEC_SOURCE_ROOT/headroom/text_stream_sample_command.log>) | `2f3044b3d438984a48cccaa9c05c4ae37dccc5d5e7f508efed621d39420ba58f` | 206 |
| [headroom/text_streaming_sample.txt](<$PAIEC_SOURCE_ROOT/headroom/text_streaming_sample.txt>) | `dddd79d56058dfc0a3411717acee43b71a5bbd0a563971907dfcafaced3794c9` | 188,633 |
| [headroom/text_streaming_sample_2.txt](<$PAIEC_SOURCE_ROOT/headroom/text_streaming_sample_2.txt>) | `57800b1c045cd542100b87c2f0129e945c848ddd7de141a3e5b2407231e48feb` | 179,292 |
| [headroom/fold_prior_0.json](<$PAIEC_SOURCE_ROOT/headroom/fold_prior_0.json>) | `2606f1c20ce98cc6817c936d84ee8a543d0702caca606534dfc238596455c65b` | 3,525,244 |
| [headroom/fold_prior_1.json](<$PAIEC_SOURCE_ROOT/headroom/fold_prior_1.json>) | `dddc95a481ddf6bbd78bc6df9ac36309a069712e1780ebe38efdaf59b00d1a3b` | 2,982,561 |
| [headroom/fold_prior_2.json](<$PAIEC_SOURCE_ROOT/headroom/fold_prior_2.json>) | `a8ad23dfdfe5bd53676c2449e147bb166276590f0363176614533bc50e4b33ea` | 3,143,471 |
| [headroom/fold_prior_3.json](<$PAIEC_SOURCE_ROOT/headroom/fold_prior_3.json>) | `59b7177fa961d7267fa4572a5416e7dd4c2acb7bac6fcec2265092e02c3cdd9b` | 3,837,504 |
| [headroom/fold_prior_4.json](<$PAIEC_SOURCE_ROOT/headroom/fold_prior_4.json>) | `c2a5ee61fcbeb5b898a56e71d058b308f376f7d1ab4ee269583397cc27d4b680` | 4,143,858 |
| [headroom/fold_prior_5.json](<$PAIEC_SOURCE_ROOT/headroom/fold_prior_5.json>) | `e9a4b5c14adf641021c408b49e9ed4e0f2a7a4fe36165948f0c4aa999a9cec44` | 4,257,920 |
| [headroom/ac_wall_0_1_2_3_4_5.json](<$PAIEC_SOURCE_ROOT/headroom/ac_wall_0_1_2_3_4_5.json>) | `3b68bac91027904765afd1831437bd79065f680915c64f79b245ba5f3819efa4` | 65 |
| [headroom/text_wall_0_1_2.json](<$PAIEC_SOURCE_ROOT/headroom/text_wall_0_1_2.json>) | `43168b59e703aea08c2b63f3ba5bc261976185d7cb1052e2b7673a7942a2e6db` | 225 |
| [headroom/text_wall_3_4_5.json](<$PAIEC_SOURCE_ROOT/headroom/text_wall_3_4_5.json>) | `e11109e5af99635b8c3963ea8ebaa9f3b5eb97ea3a787104bc3fab406d0a05c3` | 251 |
| [headroom/results/fold_0_fits.json](<$PAIEC_SOURCE_ROOT/headroom/results/fold_0_fits.json>) | `1dac89f17791daeb461a2b27d6a6e86af41f5e3f64e03b800789842c968bd618` | 54,809 |
| [headroom/results/fold_1_fits.json](<$PAIEC_SOURCE_ROOT/headroom/results/fold_1_fits.json>) | `402c94a635214ab14e11201ada8ce42c84930d03f59831269961bcf47aface00` | 41,965 |
| [headroom/results/fold_2_fits.json](<$PAIEC_SOURCE_ROOT/headroom/results/fold_2_fits.json>) | `d3c25365e443db3b21df0adaf88449aba0feef8418f837234dbbc6b60a7e97b8` | 45,873 |
| [headroom/results/fold_3_fits.json](<$PAIEC_SOURCE_ROOT/headroom/results/fold_3_fits.json>) | `c239288a9bdae3d884952798a2c05d8df65bf5961c7610ab090ffe94a2596113` | 58,950 |
| [headroom/results/fold_4_fits.json](<$PAIEC_SOURCE_ROOT/headroom/results/fold_4_fits.json>) | `2fcdc28f7375c2400f6e609deaccce57658d46df1de69b2f363ef405e3910a1b` | 65,686 |
| [headroom/results/fold_5_fits.json](<$PAIEC_SOURCE_ROOT/headroom/results/fold_5_fits.json>) | `34111a20ab3aaacd93651004505e1984647db96b81fdf2a31ed842dd31ce832e` | 50,235 |
| [headroom/results/fold_0_combined.csv](<$PAIEC_SOURCE_ROOT/headroom/results/fold_0_combined.csv>) | `37eac29c38bb799f354166ba36efae42f718502e07aba48954ae3999e699bbf9` | 1,685,161 |
| [headroom/results/fold_1_combined.csv](<$PAIEC_SOURCE_ROOT/headroom/results/fold_1_combined.csv>) | `3063052d6dceca5a8437ab101a926837541b8881ef0117d4e06551e5fd67ec23` | 5,016,156 |
| [headroom/results/fold_2_combined.csv](<$PAIEC_SOURCE_ROOT/headroom/results/fold_2_combined.csv>) | `fa4f019882b8e45619cc00b75780a4f800aa05f199e1e4c923898ff341600d66` | 4,519,071 |
| [headroom/results/fold_3_combined.csv](<$PAIEC_SOURCE_ROOT/headroom/results/fold_3_combined.csv>) | `8e8caea7e24df6b43f7ba2b3626c10411952c39a34c2549574fd95771f71243a` | 1,475,778 |
| [headroom/results/fold_4_combined.csv](<$PAIEC_SOURCE_ROOT/headroom/results/fold_4_combined.csv>) | `6a0394a63480b15e57fe61a825ec346ad9a8216c25eaee4a96f1df3b4eea387a` | 1,166,100 |
| [headroom/results/fold_5_combined.csv](<$PAIEC_SOURCE_ROOT/headroom/results/fold_5_combined.csv>) | `7208b9fd70a2cdc33a000b5b22c2ac18cfcd20abb4a63d7f03a9bd1a0b567fd7` | 659,276 |
| [headroom/results/fold_0_text.csv](<$PAIEC_SOURCE_ROOT/headroom/results/fold_0_text.csv>) | `e369f15e8010dfe0605a1ec524c607ba4d5f23e4ed01fcd59d78082dca75f2f7` | 237,235 |
| [headroom/results/fold_1_text.csv](<$PAIEC_SOURCE_ROOT/headroom/results/fold_1_text.csv>) | `291dababaaaf3a1551455048dcdd134d2ca6430e455f60f0e1816a5f85969222` | 829,343 |
| [headroom/results/fold_2_text.csv](<$PAIEC_SOURCE_ROOT/headroom/results/fold_2_text.csv>) | `14d66dded94f18c98f5ed86d1b8d9159b49ba8732294908a23f7a4ff81006781` | 629,260 |
| [headroom/results/fold_3_text.csv](<$PAIEC_SOURCE_ROOT/headroom/results/fold_3_text.csv>) | `149a3f30df1c0f28bf86a51153ae9cfa8dffc0886fd3d330dba9906dafab4486` | 197,977 |
| [headroom/results/fold_4_text.csv](<$PAIEC_SOURCE_ROOT/headroom/results/fold_4_text.csv>) | `4e1894789d3d483fb08df122e74f5d23ed3e96a2e888c42d17f4856ecf1f274e` | 170,823 |
| [headroom/results/fold_5_text.csv](<$PAIEC_SOURCE_ROOT/headroom/results/fold_5_text.csv>) | `2bac27f3e874029821180518c61e1a06b19eddf8fdf475f2ee52d86fe9afc61a` | 89,823 |
| [headroom/results/fold_0_textfit.json](<$PAIEC_SOURCE_ROOT/headroom/results/fold_0_textfit.json>) | `d4ed8a41e931f94128c16254132310d8c2d67bb24a90d52cf87ef24d18920ba8` | 226 |
| [headroom/results/fold_1_textfit.json](<$PAIEC_SOURCE_ROOT/headroom/results/fold_1_textfit.json>) | `a59edd725202148fb6e4f2a2cfce592df85ddb0ae34c272ea5baa49ae5142eff` | 226 |
| [headroom/results/fold_2_textfit.json](<$PAIEC_SOURCE_ROOT/headroom/results/fold_2_textfit.json>) | `6e77e91452282713cec334e4f60ab6200da81c51ccfa67e24e21a603bfde2a84` | 226 |
| [headroom/results/fold_3_textfit.json](<$PAIEC_SOURCE_ROOT/headroom/results/fold_3_textfit.json>) | `dbe8219be67ff3180db5326c255bd5e50a960b6a76b827fdcad23a22768cb7f7` | 226 |
| [headroom/results/fold_4_textfit.json](<$PAIEC_SOURCE_ROOT/headroom/results/fold_4_textfit.json>) | `d26410acec7b7afd6ad3dfe8b4a21c15b54159cec8cc70140a0aaed198345ff3` | 226 |
| [headroom/results/fold_5_textfit.json](<$PAIEC_SOURCE_ROOT/headroom/results/fold_5_textfit.json>) | `0b6ff09ebf8099f8f6d753625aa72cff80dbd37d1c627de4962c34a23c6ccafb` | 226 |
| [headroom/results/fold_0_TEXT_DONE](<$PAIEC_SOURCE_ROOT/headroom/results/fold_0_TEXT_DONE>) | `68929e8ef346db48ef1c825c8bc4c0419efacc704e4456c23b17fd21898386a5` | 199 |
| [headroom/results/fold_1_TEXT_DONE](<$PAIEC_SOURCE_ROOT/headroom/results/fold_1_TEXT_DONE>) | `2349c0e6062daee4d428a4fa2300c8e6e0c027f9486c6f0626ff23f9e719f78e` | 199 |
| [headroom/results/fold_2_TEXT_DONE](<$PAIEC_SOURCE_ROOT/headroom/results/fold_2_TEXT_DONE>) | `0be890f0a47e52efd303f70f01baa9efc2255fba725c660814a04882d7a1fa9c` | 199 |
| [headroom/results/fold_3_TEXT_DONE](<$PAIEC_SOURCE_ROOT/headroom/results/fold_3_TEXT_DONE>) | `70421e89996dc2318ee2a8934f275768bc1e314407c1dc99274bd96bac744ff5` | 199 |
| [headroom/results/fold_4_TEXT_DONE](<$PAIEC_SOURCE_ROOT/headroom/results/fold_4_TEXT_DONE>) | `d1ee23017ef15b5ea0e5d77e8522e873859c6f96a3f716002b236c225ed76b52` | 199 |
| [headroom/results/fold_5_TEXT_DONE](<$PAIEC_SOURCE_ROOT/headroom/results/fold_5_TEXT_DONE>) | `0db029b8f4ac36c2783ce06ac5402b0da024cd9353cc627f3797e63412f1495e` | 198 |
| [headroom/targets/abstract_reason.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/abstract_reason.parquet>) | `1e69cf0f253618b4abafff3077f9e28dcf6ed57a4a22ad0df3f9d9a1a4c991a3` | 167,049 |
| [headroom/targets/adaptivestep.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/adaptivestep.parquet>) | `a039e2acad7f620fe9c62b63e49a080e539ddbabce760d2d12912b38d64b355c` | 77,785 |
| [headroom/targets/advprompter.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/advprompter.parquet>) | `ebbd4947b0e0f94dbf4826a8bbf4ad27466e179285dec092edce0eded5ee2625` | 3,874 |
| [headroom/targets/aegis.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/aegis.parquet>) | `eec7a30d3880fc1298d0876b39fc6879e213c223178b569383e16f25f6fca163` | 212,479 |
| [headroom/targets/afrieval.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/afrieval.parquet>) | `e6726344b77186e76ff466d66bf066f8b965ce6ac96c00cb02738d1adb295b3f` | 697,050 |
| [headroom/targets/afrimedqa.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/afrimedqa.parquet>) | `888252ef2bb777e89008db0ccb742273b0397cd1c2ea5df360e7eb86d40de7a7` | 780,761 |
| [headroom/targets/agentic_review_perturbation.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/agentic_review_perturbation.parquet>) | `b1e5222cf99263a34ad6fd437015ee717ae2ab4bb4e51e855feccb420616a34b` | 4,954 |
| [headroom/targets/agi_elo.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/agi_elo.parquet>) | `c5715c6a199ca880e3a34608872426f01760f23b9c4bc4ee66eadfb8fa4894b8` | 273,341 |
| [headroom/targets/ai2d_test.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/ai2d_test.parquet>) | `55e0d2b118f50805238aa45f816a037afa1d9f06effc4556316fbcb7e3a18902` | 70,884 |
| [headroom/targets/aider.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/aider.parquet>) | `1185a2d9900bb85b9dcff50c768ca1e89c87f805399778bebbbd8f01394cc571` | 3,802 |
| [headroom/targets/algotune.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/algotune.parquet>) | `0b491d2141b7226724b682117caf51355265dac9e22b9b29d80fd570b2d4ca8d` | 6,180 |
| [headroom/targets/alignment_faking.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/alignment_faking.parquet>) | `cf439d7739041ea176bfb002f40709bc546512c2173563adb1610106bb055fdf` | 52,626 |
| [headroom/targets/alpha_sql.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/alpha_sql.parquet>) | `445ae4ac59403b2a2da86227e6ae285b208c7839ca4816c518a2da02cf0d082d` | 31,192 |
| [headroom/targets/appworld.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/appworld.parquet>) | `828c374d7f64757aff1eff93e112fb4af67cf384fb533de8d84140c96bf92bc9` | 14,445 |
| [headroom/targets/auditing_sabotage_bench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/auditing_sabotage_bench.parquet>) | `904cf293b7a14c38904aa6fb83fd7fd9249411192a3c84aab14208352ea7d9b5` | 4,835 |
| [headroom/targets/averimatec.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/averimatec.parquet>) | `27cfafa78a35d52a21dbe5725b81a68cdb0f1b6554fddd24018646bf97b4f745` | 5,779 |
| [headroom/targets/babilong.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/babilong.parquet>) | `71ec883725abf8b422d83f5f7ecc56c25a3061f749f41b7f671695f6bcac274e` | 8,873,124 |
| [headroom/targets/bbq.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/bbq.parquet>) | `b7398dd513d75b2e71afdfde51e93534bb65a8afea3c67ff2a1eec3ea14a3481` | 3,352,397 |
| [headroom/targets/beavertails.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/beavertails.parquet>) | `4c71543dbf7e7b2b5279d19696979feab886c8356a6b5daf2a80d55251ed40fe` | 10,961 |
| [headroom/targets/benger.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/benger.parquet>) | `3f80b3605904fef44f695373eafaf56e1bf3b63c2a8512a4c67d51af487e5fc3` | 18,879 |
| [headroom/targets/bertaqa.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/bertaqa.parquet>) | `11d1640917a957bcd1c7bf9584d179014df95ee3cba9207b61d916d8bc3d4192` | 941,484 |
| [headroom/targets/bird_sql.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/bird_sql.parquet>) | `d97617fec027c63ecf0934889a4efd9b2eee3bf631823c5da6297b04c0edd168` | 10,689 |
| [headroom/targets/brace.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/brace.parquet>) | `8349fd00fdbc8b63a3cf4d9e65fb1e16757f5aefda2d3fd18a7292faa1e64430` | 240,761 |
| [headroom/targets/braveguard.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/braveguard.parquet>) | `5b4f81b3e4631ce3400cde46831872cfb8f8316a97251a60245fbdd4c95c1f12` | 12,887 |
| [headroom/targets/bridging_gap.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/bridging_gap.parquet>) | `a25b5980bb12041693f617f11a08ae18302c69aa604b445df392a90300077b97` | 2,551,520 |
| [headroom/targets/causal_axioms.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/causal_axioms.parquet>) | `e9f8769a7ea818a0299d3e0498a46a203d5b637a31291268de5ef7863fe0799a` | 86,085 |
| [headroom/targets/cellverse.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/cellverse.parquet>) | `aa7155a68064bb8a9d4a6b1a62f7a820c71aa71324bcdf94c25c1ebd682f28c1` | 16,847 |
| [headroom/targets/ceval.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/ceval.parquet>) | `d8fe01998972e64c4778c151476b147e11ff053409beb31530890ed854e851d2` | 28,956 |
| [headroom/targets/chartmuseum.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/chartmuseum.parquet>) | `2aad97a4a2e5363b222084ae97979ab565ac2050021d178850c0c531433ac5c5` | 2,291 |
| [headroom/targets/chi_bench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/chi_bench.parquet>) | `fe092f5c2c6b61c4116772062b2b89a64f50888877470af77e3315332f61e827` | 19,050 |
| [headroom/targets/clasheval.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/clasheval.parquet>) | `7c02e4d37d5f9688907fbaddd6e52ceb486f06e29f9edd81f3e2a4566fa905ed` | 236,541 |
| [headroom/targets/cmmlu.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/cmmlu.parquet>) | `aa8ea6253c69942cbda931abb6fcbea4ea8233b2dde71fa03233fcb10b29ebf2` | 442,948 |
| [headroom/targets/confagents.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/confagents.parquet>) | `cb3b5355ea0e61e7ebc54b7f8d63ad144c46a49de55260616848004c39a4f1dc` | 3,217 |
| [headroom/targets/critic_discernment_game.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/critic_discernment_game.parquet>) | `071e4fc55ad8147ae72238476e13735e122dc7b84cd3a04d0483eb6cf1594a02` | 37,123 |
| [headroom/targets/crow.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/crow.parquet>) | `9935c4e2798bdd720c6f20b5bacebe6fc53c33b81b78a43303d6a56e64e13432` | 36,666 |
| [headroom/targets/cruxeval.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/cruxeval.parquet>) | `42379c1d9e2fefd593c6002ee256fed54a45b18d09cbab5026c1beb6a254a1b2` | 95,295 |
| [headroom/targets/dave.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/dave.parquet>) | `2a06b6e8ee1b7d73cca3df697365f6e589d94eb0453201f96150becf63472614` | 77,967 |
| [headroom/targets/dbpa.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/dbpa.parquet>) | `2c7a7f0d5f33c0bd0880421c64a9792f9047c57eb351d8571dd4a8506a0663e0` | 4,201 |
| [headroom/targets/devbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/devbench.parquet>) | `25ab3568da2e66e581f7f180bfbfb9918a7af51fa515e365c7a44b7987efcbe8` | 8,443 |
| [headroom/targets/disco.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/disco.parquet>) | `887c6214ccd8b981a5a313a41bc15c515bed377907b451278652258a637d5665` | 512,669 |
| [headroom/targets/editbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/editbench.parquet>) | `c70d7841f11d6a0d44b2346ec0da44e53742a25476c76ce43821ad1739bf2a44` | 14,853 |
| [headroom/targets/edu_circuit_hw.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/edu_circuit_hw.parquet>) | `653db001f842cd1dc7acab7b8605d4572c848e3194f2e1802ebfa791c180fda5` | 13,149 |
| [headroom/targets/egoschema.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/egoschema.parquet>) | `d083f9f77a1a0e574c09a55f8bc3360d31a81f8241e64005ac3f7adb310b41a7` | 86,667 |
| [headroom/targets/ehrflowbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/ehrflowbench.parquet>) | `347cea13de4ef3424c5e4775a5ab21e3602245200cc9d91dfcfc7a04e0887416` | 3,342 |
| [headroom/targets/elicitation_game.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/elicitation_game.parquet>) | `eab3f596b9bcb0f73a50d1ecbdf361a3a36b9b8adfaf7f982e7b296051b06d88` | 59,797 |
| [headroom/targets/emoji_attack.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/emoji_attack.parquet>) | `5764b091a179a11775fca900eb8222dd0bfcebda645e94a0860b64b5d5f03077` | 293,773 |
| [headroom/targets/engdesign.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/engdesign.parquet>) | `8f1b485121678709d27f7eb13c81edfcc553c03794549672d379de2dab15c059` | 5,742 |
| [headroom/targets/enginemt_qa.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/enginemt_qa.parquet>) | `9b04d9e010d08540b56d5da60c0220a909bb28d4f562f320b7d196c0fb2c7c9e` | 15,482 |
| [headroom/targets/erbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/erbench.parquet>) | `0842f1fc6703ebf864488bbd29ad21b1aae3c15462e2207f4100042fa9ca2c8b` | 618,562 |
| [headroom/targets/evouna.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/evouna.parquet>) | `56c5058c1738ed650f9226ad028d24c45bb12bfe7240e7abdbd8750097da9729` | 100,987 |
| [headroom/targets/exploitgym.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/exploitgym.parquet>) | `c2270da831ba455aebbc24f56d46d38553c101b306d2e7402297f7173a28f401` | 35,894 |
| [headroom/targets/faithcot.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/faithcot.parquet>) | `516099fe67751c7374f9c76e2a4dc16da9c9a0255153f4a8f8956cdc2631bb38` | 16,261 |
| [headroom/targets/felm.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/felm.parquet>) | `fcefd43ae44fafb5d461888377f6f39ebbf348443f6ea60db273add91152a21d` | 83,439 |
| [headroom/targets/fewshot_ttt_bbh.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/fewshot_ttt_bbh.parquet>) | `5023366dd1b6e6426fa5a888ff07297f65cbda4a202fd5a6ed1a749e2f5ea766` | 29,004 |
| [headroom/targets/financebench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/financebench.parquet>) | `dab67da0689c2341bda4cf828d8727905453de316a05b6c390936c77d42f0185` | 5,993 |
| [headroom/targets/finegrain_t2i.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/finegrain_t2i.parquet>) | `e35341f171f19dbc7a7538eeb6a4981a2e30290e8d62d018a1db71da70ca9645` | 16,814 |
| [headroom/targets/haiid.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/haiid.parquet>) | `0668b9b90d82fe21c6e1a68a40e277650d739e24c31b0e37c1776dcf84d484d7` | 8,157 |
| [headroom/targets/hallusionbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/hallusionbench.parquet>) | `75e4070746f96d34d9128993796b1b5a0ac9294ac43f8a6bfa7542394c634fb1` | 27,466 |
| [headroom/targets/harmbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/harmbench.parquet>) | `9be11e51f3d22206bab99b61bd4df9c3dc3f8aaecb2f261922fc286c783d01fe` | 1,133,167 |
| [headroom/targets/healthadminbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/healthadminbench.parquet>) | `cf783ef8e34c492dfb29692be15875fb556aee09206a8f72418fc2dd457c25ff` | 13,850 |
| [headroom/targets/helm_afr.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/helm_afr.parquet>) | `53d49b67641f90337966ec6982ebb4234b9f39697f025a83934f43f1fc8d8bb2` | 1,343,016 |
| [headroom/targets/helm_bbq.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/helm_bbq.parquet>) | `0b267db367646d89bc534b5cbec87156a04a3aa2005ae2ac899469cd0316cc83` | 42,694 |
| [headroom/targets/helm_thaiexam.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/helm_thaiexam.parquet>) | `98d94ea10ab24cfab0561fd582bb5f089c3613c4e5876d1455a7c4782fcfc0a7` | 14,675 |
| [headroom/targets/hle.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/hle.parquet>) | `56771bcb2a3f5825b577582abf34324875dc17a4d0953f548dd5af3d2dc54715` | 47,595 |
| [headroom/targets/icpc2_code_selector.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/icpc2_code_selector.parquet>) | `2da7e204440af64b10e4f45e1bc45c2c9a5e22fbf3ac4739b99684da2f0b9e30` | 47,966 |
| [headroom/targets/igakuqa.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/igakuqa.parquet>) | `df2fad221098434ee1cb7ebfdab9a606e44a5b05935cacc6cf6bc29b0975ce6b` | 58,232 |
| [headroom/targets/igakuqa119.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/igakuqa119.parquet>) | `11aa45b2a55a51ff5095092c9eeb4a70465e792cb548ca7fafe42c413d6764e6` | 10,388 |
| [headroom/targets/ikp.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/ikp.parquet>) | `bb252961479d83fd5bc58a7ea86c4064ac3f4a062696a35163ba06f5a24dcd15` | 44,049 |
| [headroom/targets/imagenet_hard.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/imagenet_hard.parquet>) | `4bf79370099c665c9d365e285e2fc568ac7375a048bd0a41ad1b52a9e78bdc7e` | 143,580 |
| [headroom/targets/ineqmath.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/ineqmath.parquet>) | `2aad97a4a2e5363b222084ae97979ab565ac2050021d178850c0c531433ac5c5` | 2,291 |
| [headroom/targets/interchangeable_token_embeddings.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/interchangeable_token_embeddings.parquet>) | `0ec4545b63c9378b5ce9c789bbd9567946953a7ba34434e6312d14022cefe9bf` | 3,182,307 |
| [headroom/targets/jailbreakbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/jailbreakbench.parquet>) | `8318b4fb8ba0cb492d38496b7e98704f8a4d6cfe9c0666b78d9d2ebd114ff5e9` | 40,995 |
| [headroom/targets/judgetuning.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/judgetuning.parquet>) | `7dc9d7385d8006fe13d9b8ec8eaff73c87819452649b40b04358332eb8a90271` | 59,085 |
| [headroom/targets/kernelbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/kernelbench.parquet>) | `b17dc36af933cf53c25e0f2dc2ecf09757b9a7625298f1be5a64763cfa0c0bc5` | 11,542 |
| [headroom/targets/kmmlu.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/kmmlu.parquet>) | `9ce765b9bbb3a1c128a325ff3ef19dc3395cbb5ca05ba427b15f1ab3f63d9e42` | 706,211 |
| [headroom/targets/kormedmcqa.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/kormedmcqa.parquet>) | `6bc2299281ebc54a3d6e35c9d13629a61b55eb9bd848132c5e5e0ac15a2751c4` | 60,884 |
| [headroom/targets/legal_rag_bench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/legal_rag_bench.parquet>) | `b0af4faf88780ec4628e5df12f5b9b75731a1302a024ca833e3dbcaf0b5e4f4f` | 8,703 |
| [headroom/targets/legalbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/legalbench.parquet>) | `2553b75922e809b8710456b94f4dbf0fedc3b81274ad6bbf9434fd2d3a816635` | 189,310 |
| [headroom/targets/lingoly.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/lingoly.parquet>) | `2e969d843c60eb87fa55fb3e7a69f86fb441fef3f46c2f79e786d0488f893d0e` | 234,539 |
| [headroom/targets/live_agent_risk.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/live_agent_risk.parquet>) | `d1ee19710a621f9986df6a48ef8a86ca1c65c362238620df77ea411c83d9f36b` | 4,344 |
| [headroom/targets/liveaopsbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/liveaopsbench.parquet>) | `a0162199870d414a5164e0320aa1c2cfb7b2640f90972af151c7574e26d58437` | 103,667 |
| [headroom/targets/llm_bp_tag.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/llm_bp_tag.parquet>) | `1b1c74124d255985d3edea7b4f9f8c1b9e3fd70ab6832ffc9f03297ec76f05d0` | 2,505,318 |
| [headroom/targets/llm_uncertainty_bench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/llm_uncertainty_bench.parquet>) | `dfe253ed0a5c9ea768feaba4c91756dadabb6759999aa0063797ab67e96c0429` | 2,597,110 |
| [headroom/targets/llmail_inject.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/llmail_inject.parquet>) | `c4cc43718f57f1bf660c01988b83bb25fcfff5946b23d5679de3bc735817339d` | 3,261,739 |
| [headroom/targets/llms_lean_formalization.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/llms_lean_formalization.parquet>) | `8a5e27ff8ecad8ed7830ba4c9da478af845ce2daf636c6b65d0ef6f59aacafc5` | 18,128 |
| [headroom/targets/mathconstraint.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/mathconstraint.parquet>) | `befcc5a8dc96eb1158bf30becb578ca1d3396a2c3d44559895a9f9ac768217cc` | 13,500 |
| [headroom/targets/mathvista_mini.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/mathvista_mini.parquet>) | `44ad9f9359cac2d5aaacad69818de99a2e55ff8f082c8f403dab2d590ad1444e` | 33,885 |
| [headroom/targets/medhelm_ehr_sql.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/medhelm_ehr_sql.parquet>) | `2b434b078d79acbf5d1ff588029bc1a855bd7ff06329decb109223c5811ca7eb` | 22,247 |
| [headroom/targets/medhelm_head_qa.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/medhelm_head_qa.parquet>) | `8a30b4464d76b900919df37d89f5b655d2d5f5cc132b1af37853ecf62074d09e` | 22,258 |
| [headroom/targets/medhelm_med_mcqa.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/medhelm_med_mcqa.parquet>) | `b43ea95808c5874d799a7d8ed6b6ad993be88e1969a3eaa725930a47171ef58f` | 22,236 |
| [headroom/targets/medhelm_med_qa.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/medhelm_med_qa.parquet>) | `c2ed0e9e9fa3ada981add60eabde6477ca0930f562717b0b9731d5ee238f9c14` | 22,260 |
| [headroom/targets/medhelm_medbullets.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/medhelm_medbullets.parquet>) | `869fc1a3b15783650d6ddf42bce64051706460ed5ec7ff5f13174ccb1b304357` | 8,878 |
| [headroom/targets/medhelm_medcalc_bench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/medhelm_medcalc_bench.parquet>) | `d3a11dc596a3912250c1d69dae33788f8ca0908c954601d082483d34f25824e2` | 22,155 |
| [headroom/targets/medhelm_medec.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/medhelm_medec.parquet>) | `4a2ea6f703a24dda26c66032875008ea65092135737ce5cce7a7f195cadce92b` | 14,658 |
| [headroom/targets/medhelm_medhallu.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/medhelm_medhallu.parquet>) | `b28bfb85d7656acd6b082b783bce7757ff2d4dc6758e7a347b6913c2df3a323c` | 41,213 |
| [headroom/targets/medhelm_pubmed_qa.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/medhelm_pubmed_qa.parquet>) | `172c748787993c350e8cdef11af689b534d8c4da109c4558f69ef6fb0c2cb561` | 32,047 |
| [headroom/targets/medhelm_race_based_med.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/medhelm_race_based_med.parquet>) | `30847bd7b22a7bb9eed02373dc59d5d440876dc463d2630e510bb37b3679253c` | 6,315 |
| [headroom/targets/mind2web.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/mind2web.parquet>) | `4b89bb903e274346e5f0ffee2f2c643f63dea0dfcae7bbdddcd8948d7d74d6f9` | 311,091 |
| [headroom/targets/mj_bench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/mj_bench.parquet>) | `7d071d1e2f2f206d4a416c4785d84aed3a756edb186d5e537d6fbf15e7358914` | 315,049 |
| [headroom/targets/mmbench_v11.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/mmbench_v11.parquet>) | `4956ed110c091ca3e10f9bb7836e6792485e26dfad784c765887e8428ec9e5e0` | 355,886 |
| [headroom/targets/mmlu.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/mmlu.parquet>) | `d6fc153b9d2c2d468825e3a95514c226933ae77498414251c80916be4ca3ce87` | 276,174 |
| [headroom/targets/mmlupro.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/mmlupro.parquet>) | `379dacfd06c99ef4773969ed223e9bcafd4ad2ab5c5e4649a034f1b6844e8108` | 306,621 |
| [headroom/targets/mmmu_dev_val.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/mmmu_dev_val.parquet>) | `2aad97a4a2e5363b222084ae97979ab565ac2050021d178850c0c531433ac5c5` | 2,291 |
| [headroom/targets/monkey_power_laws.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/monkey_power_laws.parquet>) | `97981318885d6bf009578041aba7b10be8d68baecf2397b9f97ead4a88180702` | 19,680 |
| [headroom/targets/morphkv.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/morphkv.parquet>) | `7786cffeba497e69ddf3a1fd775c505c9049090c4bd5dec986f0cc02336fa9e8` | 13,916 |
| [headroom/targets/mtbbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/mtbbench.parquet>) | `9ac5b4b0d8d1359561597f51e222084b441d0af15ed3142181acac03da5c0fb9` | 14,588 |
| [headroom/targets/multi_swebench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/multi_swebench.parquet>) | `82123d02385fdc892aa9e026969c764b4d5d1aee80ff856a0cadd87405373758` | 50,930 |
| [headroom/targets/mypcbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/mypcbench.parquet>) | `4bc36b6b575f645a34096854583b524fa6beb59d44f51b27abfba394fc854482` | 5,138 |
| [headroom/targets/naep_llm_students.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/naep_llm_students.parquet>) | `1a506d5a0a5e426a335c7cb26277c034fb52fc8d1fc7d3024c55ac6080e5be0e` | 13,835 |
| [headroom/targets/naturalreasoning.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/naturalreasoning.parquet>) | `2aad97a4a2e5363b222084ae97979ab565ac2050021d178850c0c531433ac5c5` | 2,291 |
| [headroom/targets/naturebench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/naturebench.parquet>) | `870845492618e02bf69f0d23b7e0219b4c5952b9dd3bd08a647c6532c407eeae` | 6,822 |
| [headroom/targets/nester.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/nester.parquet>) | `18a44834f559397a6b27888cd8d02b820fd9043ea615c02a2c198c58d2e3c3d2` | 9,665 |
| [headroom/targets/nyu_ctf_bench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/nyu_ctf_bench.parquet>) | `83de2866a0efb2643f104315c68102a19c00e9e4eeb4eee6d8457bbb5eb5fd5a` | 10,886 |
| [headroom/targets/ood_prediction.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/ood_prediction.parquet>) | `84c65ead31ee95bc143ae3370521427c4520db08cf926a1496cd71f5cdfea8d3` | 2,304,910 |
| [headroom/targets/openbiorq.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/openbiorq.parquet>) | `b34d46417ea0794e01d586e46dc35f70d5dcb1cbaa506ea5016e6edceaa4cfe0` | 16,039 |
| [headroom/targets/os_harm.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/os_harm.parquet>) | `caeafaf0a18277d4661e890c6094230a3f24e4fa4741abfaeea5420f90fc764b` | 13,056 |
| [headroom/targets/perfcodebench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/perfcodebench.parquet>) | `2b3b1302fd031e00b08bb419a4bd52c25e864d13606fc8c08c34c01a35924667` | 41,663 |
| [headroom/targets/perumedqa.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/perumedqa.parquet>) | `ee71ef9f230978a6b5085ab2f7b86736adece2d67ce3c690c793a498b3b4d76f` | 166,416 |
| [headroom/targets/pku_saferlhf.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/pku_saferlhf.parquet>) | `3a7f90c6cb43cfeab953a6e8d7dfc693fed951e9efe05b148cb2974c141526e0` | 762,554 |
| [headroom/targets/planbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/planbench.parquet>) | `9b0c8c15ccad87cc33b6e7a7e26703bac76442102327d1a87bd8b57f56197c43` | 217,725 |
| [headroom/targets/proofaug.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/proofaug.parquet>) | `4453ddc06faa516084243452d5ff451e375fd0922c184bfc28cfbdb9a9943eaa` | 7,460 |
| [headroom/targets/prox.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/prox.parquet>) | `c1d6300d1413e8a4d31f4cb7d5598e056c713fea3e7a088db86262eb65267177` | 222,484 |
| [headroom/targets/pxplore.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/pxplore.parquet>) | `a26cafdae2c7bd584dadaae80a31198420860454df9c1eea87b820dff00ffd9d` | 18,944 |
| [headroom/targets/radar.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/radar.parquet>) | `734c22760ced2a1cb4d2ca2c29e0466fc180e26ab5fb46490e4791c7fc0f0aba` | 2,897 |
| [headroom/targets/real_webagents.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/real_webagents.parquet>) | `7ecbdb6d9e728be7953276bd05541fbe82a9fbd6448247466a6c9c9916e3f3bc` | 9,491 |
| [headroom/targets/realtimeqa.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/realtimeqa.parquet>) | `3b10ff13ce200169bfbc68facd23ab42a95a082a9f708dc6ac0dca537e02f4f0` | 157,411 |
| [headroom/targets/reliancescope.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/reliancescope.parquet>) | `95035fb5dfd0eaabd951f42297d1e667909922a92b66253e3d68ff24efd50464` | 25,723 |
| [headroom/targets/researchcodebench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/researchcodebench.parquet>) | `b7ea00701203d39d55abd4bb3ddf2e7f3cf8e32216e7fd23c9f20098d79a31d1` | 7,691 |
| [headroom/targets/revolve.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/revolve.parquet>) | `cf09c6810e26f5124b8ad159ad2dda112692c75ce19657cc1f666ca34eb5ec86` | 9,063 |
| [headroom/targets/risebench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/risebench.parquet>) | `924ed62c98ddfaf8da104b705a43dfe9df7ed591674fdd3aa7e61521b26e9ab9` | 24,525 |
| [headroom/targets/robust_reasoning_benchmark.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/robust_reasoning_benchmark.parquet>) | `8629600b458e919eedf10f9d93c8b11de96782d1a69f731baad7cef8af0ab62e` | 105,316 |
| [headroom/targets/safeagentbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/safeagentbench.parquet>) | `20655a8f2d75f90cc552e1a337af0fe87edaf1a26e9739da226984d529353ad4` | 15,842 |
| [headroom/targets/scbench_long.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/scbench_long.parquet>) | `69755fbc8d225c3591a2f8590296a1919f2a5e736d5a8db7d54274771b0ffb13` | 3,004 |
| [headroom/targets/sgrades.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/sgrades.parquet>) | `79c51304230c7672387225e5a3d94d91dcb69fde20e9fca57e077ca98a5bd6e2` | 491,536 |
| [headroom/targets/sib200.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/sib200.parquet>) | `be01355ca882d3d2b7e09942ea478d79634642cf1146bec8443f14529bf653f2` | 808,096 |
| [headroom/targets/sketchjudge.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/sketchjudge.parquet>) | `005ee669fd5318e9f13db2629ee88fed0e975150ae276abd40edb2a60701b8fb` | 81,630 |
| [headroom/targets/software_world_models.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/software_world_models.parquet>) | `08d3c78625fe8be096b63fc289c216fa67f22e97d52d3d0560e4cfc688fa0621` | 11,634 |
| [headroom/targets/statqa.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/statqa.parquet>) | `2297fe398e20516de713eb732469513d6ec17cec69f87d02d7668a7ca7c548c8` | 26,343 |
| [headroom/targets/subjective_qa.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/subjective_qa.parquet>) | `0ce3b0fb8d7203648f1d9a6176287bc9212b285184f13066c5cedfb511cb555b` | 203,500 |
| [headroom/targets/sugarcrepe.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/sugarcrepe.parquet>) | `855e1bab856bec5560961a9491c95eee11777f74b7c3f22d1b54ecb46e7d4b11` | 271,442 |
| [headroom/targets/sustainable_food.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/sustainable_food.parquet>) | `35a2943fea4fb9ac0a5ab2cb932032e98a48be387a93be4b804ff015ed8c9dc2` | 12,560 |
| [headroom/targets/swe_rebench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/swe_rebench.parquet>) | `24c463784bf84b6e60b8ab09e4075127575588cc24c83aee0613636cb4fe6052` | 126,734 |
| [headroom/targets/swe_smith.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/swe_smith.parquet>) | `b87becf9e2b65e200df3ec81e4e9c5da2fb06363c093336d74944bc28e241c70` | 292,874 |
| [headroom/targets/swe_together.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/swe_together.parquet>) | `7e0d143464d3c117dbe15a3f6d4e5a4c9d17666853b5886d79ff11383d2cad77` | 5,501 |
| [headroom/targets/swebench_live.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/swebench_live.parquet>) | `b8333f3422421fe9c29bdf39bb8eccb1cbeafdfffe6d60fbfe76af368be6b891` | 35,071 |
| [headroom/targets/swepolybench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/swepolybench.parquet>) | `3313777034a7269b77480ba3a47454995fc5a78df02b2f518445b70441f4c951` | 13,789 |
| [headroom/targets/tau2_bench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/tau2_bench.parquet>) | `459d29c21e6bf4e1c0e26e322aefa9fee628d413a1b0b7d677f1440c9532be72` | 51,886 |
| [headroom/targets/taubench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/taubench.parquet>) | `dc64248aba7a4805e6a2d2f3b69087a055985fd23752a4f705a849a7d20d9687` | 7,800 |
| [headroom/targets/tensortrust.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/tensortrust.parquet>) | `8a0117b817957ac803d95abfdbe69fc9fc7cbae1b8eaf7c0b8382a75d9730f30` | 8,799,481 |
| [headroom/targets/truthfulqa_mc.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/truthfulqa_mc.parquet>) | `c31f11825e5284454238a0275ad999e01fe7d4b7f2b1d1a82d721b253c7ba93f` | 21,240 |
| [headroom/targets/tulu_human_eval.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/tulu_human_eval.parquet>) | `27aaf2281a00efd3865149cebaeef13025fd75e112c41cefeafcb01dad0510de` | 23,061 |
| [headroom/targets/tumlu.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/tumlu.parquet>) | `0fff55060e0afe705c55f41b465aa88129a87fe5cb16b8c97e6e56c7e6977e7d` | 2,141,175 |
| [headroom/targets/txbench_pp.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/txbench_pp.parquet>) | `533923017d9955fd481322c9872a7465b9575cbd64aa16ba00525787d75458c5` | 3,263 |
| [headroom/targets/visual_memory.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/visual_memory.parquet>) | `3bfac620da0ff6c280278c55e6df188f3a9eb83a0199a20a9c2ad8d10cb19834` | 867,321 |
| [headroom/targets/visual_riddles.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/visual_riddles.parquet>) | `934250933992d921b5925c4c14492b1a02dff818d10d07674b654f8fcee07053` | 18,564 |
| [headroom/targets/visualwebarena.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/visualwebarena.parquet>) | `ddcfaf5a581142a36425eb0350880c69f5cd6502c0596b233d929dd5c89efc16` | 6,737 |
| [headroom/targets/vl_rewardbench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/vl_rewardbench.parquet>) | `40a3d177075d4dbd6dae975288f566a0d6ae74bceceb38f868589f087fe8d467` | 44,477 |
| [headroom/targets/weavebench.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/weavebench.parquet>) | `de8927d0c53e33f7bc240c6df856533e48529217d325df13aa9ad11087cc1e53` | 5,069 |
| [headroom/targets/wikihow_agent.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/wikihow_agent.parquet>) | `bcdb1ae682de757324aaf2743ede54ea63f34f83b78cee202ac95582bd7e92a9` | 265,016 |
| [headroom/targets/wmt_mqm.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/wmt_mqm.parquet>) | `3894ebdc2d5d0e639175a20e16900f031198a6227779dd971f0e9e966d3341ef` | 3,528,744 |
| [headroom/targets/workarena.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/workarena.parquet>) | `26c4bcc1565446ca26dad65f0da1be28c8db0aaa342c292626f81ccec0715ea0` | 10,335 |
| [headroom/targets/workbench_revisited.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/workbench_revisited.parquet>) | `be1b194a381e2ba2587c0daaebc6378a15392eff9c5126209e4a4223bd14eedf` | 16,710 |
| [headroom/targets/worldcentralbanks.parquet](<$PAIEC_SOURCE_ROOT/headroom/targets/worldcentralbanks.parquet>) | `4bcfedfad3a16b3696d9e437d83ae56e3d2cbfb5bbcf6eb216255f0404195cc7` | 2,091,316 |
| [run_logs/hf_full_table_inventory.json](<$PAIEC_SOURCE_ROOT/run_logs/hf_full_table_inventory.json>) | `f8731c9b2eace07fe66e0d514d5eee7ef2a0e36f62cf9bcca23953796e29bfc2` | 410,207 |
| [run_logs/hf_complete_eligibility.json](<$PAIEC_SOURCE_ROOT/run_logs/hf_complete_eligibility.json>) | `abf0a5a0cdf57423cf0fe45c5b828132158bf8e660cac6d5b05a6d459b99624a` | 452,597 |
| [run_logs/required_tables_preservation.json](<$PAIEC_SOURCE_ROOT/run_logs/required_tables_preservation.json>) | `c38b1219bcc69cad17fd8bbe8da743eddf19d6726d45eedd78333587c5609088` | 307,452 |

## Appendix — all downloaded/reused item input hashes

| Slug | Bytes | Rows | SHA256 | Provenance |
| --- | --- | --- | --- | --- |
| abstract_reason | 10,549,040 | 9,089 | `bf97f9bff6a6a44a48bba688fd402705888dac81b313135f262262fba44a35d7` | verified_local_hardlink |
| adaptivestep | 1,576,068 | 4,525 | `eee9a48a089fd94d5e6b6af33eb4b704f5413e073b400852bb1dff885924fcfe` | verified_local_hardlink |
| advprompter | 29,301 | 50 | `48d6bc3ea9d5ab52608a508833103680e9cd01a2517f7f84941bed9e90656528` | verified_local_hardlink |
| aegis | 1,381,796 | 11,500 | `a84bf5bfeac873848f908dfaa3568db5853c5dcfe7d19143f9c710dc781c04f9` | verified_local_hardlink |
| afrieval | 7,142,460 | 35,205 | `ffb1e4847221e003de23a539687e75da0d438cbc3b9c481b3131384646c0c618` | verified_local_hardlink |
| afrimedqa | 19,710,846 | 42,494 | `487d3b61c4a001a901583c0ecd9c144cf13a430bb01ff1f34ecfc9fcd418d99e` | verified_local_hardlink |
| agentic_review_perturbation | 407,068 | 105 | `1ec9fc3b6a75e84ac70b5fedc88c2b26cfc9c6c4e3daaa1fc9dcc5dd1f7c7362` | verified_local_hardlink |
| agi_elo | 4,329,974 | 13,953 | `edc7856fab159be49e6f609f1bed5c88a55c79406b2aee421b975ea19d3d3d74` | verified_local_hardlink |
| ai2d_test | 572,124 | 3,088 | `d76abbef5670284060151add2958d355d3e597efe79ca43a99c303be3d4aff93` | verified_local_hardlink |
| aider | 143,161 | 26 | `fc547256d7b7ca7d4fc7e4ebe690c586ebf71f82da822c2a847544559ff7fc01` | verified_local_hardlink |
| algotune | 508,732 | 154 | `b089d8f29fef971f02f45885ecb0a23cb9e9e1dcf249099e1b619f3799611a4c` | verified_local_hardlink |
| alignment_faking | 2,821,008 | 1,464 | `07422da21d2cb296b9ba1d8737a5e1ac8c76d51f5beff9602221f06aa5786204` | verified_local_hardlink |
| alpha_sql | 927,621 | 1,534 | `df83ad39d0b91054ba9f70de59b4393afec9e8b1b5ec989af54b5571be86d3a9` | verified_local_hardlink |
| appworld | 253,157 | 585 | `016ed101f006d6ce8d2dc43dd82f1ceacc53c0a5b28a8e63752a7049588f6729` | verified_local_hardlink |
| auditing_sabotage_bench | 1,128,733 | 68 | `cc6fea1982af20ec867388d56ff96bf92271217c968a591894f92d02ea165850` | verified_local_hardlink |
| averimatec | 57,957 | 152 | `67f63eadd557caf439bcd2a1be7311d40ed164de998539ca421205c3132c5e24` | verified_local_hardlink |
| babilong | 45,079,999 | 526,202 | `6cffcbd3d0ef436103c416d909251103d632c8d81a85a5eeaa9297f884489c9b` | verified_local_hardlink |
| bbq | 28,377,321 | 204,201 | `0d2c57557872899c7e31e5e974bca0d0667f4ff42a904889a236104e8e2d0248` | verified_local_hardlink |
| beavertails | 37,975 | 420 | `68130bd4335f2b1ac3a825a0ff4c001dc75694e77043772c425c9dce77847805` | verified_local_hardlink |
| benger | 4,376,647 | 760 | `b3633d6de0d12c53d448b5cb7e256f6d1e581a2e221ec642d60a58ccd02bfd1f` | verified_local_hardlink |
| bertaqa | 25,596,401 | 51,760 | `5bab19ecdfd45fe4fcb3bc937edd39768f219004a685739b278d51422198da36` | verified_local_hardlink |
| bird_sql | 318,389 | 360 | `d4ff41c32631b47583127e0df84a78d9dc90bb16fb430284d9beb6e7a8898f7c` | verified_local_hardlink |
| brace | 1,771,588 | 12,631 | `6d35500bec530cbc6e7b007306210e6e0afbaf2a0b1e28403904f236ce0cd41c` | verified_local_hardlink |
| braveguard | 2,454,942 | 536 | `989bb7524e922b6c6d4b44282c49966baa7705a9f30aa429382b4be4a2adda1c` | verified_local_hardlink |
| bridging_gap | 39,912,899 | 132,418 | `b17b683bc1685c46d5d63a0f8075108e30ff6ed5a321253d5a63e46c30f6885f` | verified_local_hardlink |
| causal_axioms | 391,141 | 4,500 | `3a2f09b6de15a40b2d28c80183bceba582d7b42417216af6674eee7ea9c79d96` | verified_local_hardlink |
| cellverse | 924,840 | 748 | `ccc9382ccaf846ad4a6ea3a8ec3c69c6a4bb31733e7307758817efebef030653` | verified_local_hardlink |
| ceval | 2,844,461 | 13,951 | `ef2e9ae4d8602732883393f2cd2e63912dfe0cf363d3efc8dede2913a9908b50` | verified_local_hardlink |
| chartmuseum | 78,772 | 162 | `6821b69c99cce7b456a989022a4ce92cf4ac57aab6c529a9b48ad4f01aa8b092` | verified_local_hardlink |
| chi_bench | 138,236 | 775 | `f5fb3e40b978fef937b5583de3ed87b25f73ffe9df2a55603c63b302aae7b99d` | direct_tls_download |
| clasheval | 16,245,691 | 12,495 | `e8f76477ac36d0a6e01dc824c54ae8c9bc658f7da9a8b1cd5765ff15583bdaab` | direct_tls_download |
| cmmlu | 4,483,659 | 23,160 | `5137af93b3b45e04334abc559233fe3a08a962928c38cfc35cfc564cb4605e25` | direct_tls_download |
| confagents | 20,722 | 16 | `3741ff58939ff871310f11fca9ae551288fea23b3bd3ef1ded12cf0bbbd72572` | direct_tls_download |
| critic_discernment_game | 782,128 | 1,819 | `fce47cc9d0796c053fc4afded25bb495ffa2b16508a7d8fe2495d62c7fc89cce` | direct_tls_download |
| crow | 404,832 | 1,984 | `b6a800a97db0914d5486214f61033e89a0e3cb8b08e33004db96c33b9602ea10` | direct_tls_download |
| cruxeval | 964,730 | 4,000 | `b06e3093a6beb8c56a48ee4bcef5cd54914e138880d7f6ce6fec7b19686b2f0e` | direct_tls_download |
| dave | 785,003 | 3,922 | `54cc772ed45f6d41506c27f13fc1fc35f0c68e592edefeb0c68c50cc358993a6` | direct_tls_download |
| dbpa | 19,340 | 59 | `3958d664938b90677a0e666bc61de4b49a5dd4bea8cd1f1f566782412c94b5d8` | direct_tls_download |
| devbench | 113,778 | 271 | `74f78cd2de8db38ed2d07865697647c3dee7daaa01790313fb9b17a44f6dc407` | direct_tls_download |
| disco | 6,228,981 | 28,000 | `1fb6cb920fac31be39cd17837743f4dfba46387f29f656345e2f479282d2b2a0` | direct_tls_download |
| editbench | 6,347,667 | 540 | `cd23e864e60c01c5b8a2d99c4d0602596d6c8a4ea98b47a06052f0ca16230333` | direct_tls_download |
| edu_circuit_hw | 298,119 | 513 | `c0d6795a744baa698f30aca23ce1780cf84cddee9b7da7c1f83233e795962fae` | direct_tls_download |
| egoschema | 16,308,632 | 4,500 | `4d85eced53d1dd077c14868de86234de28a383b94d1113197f5126126f052213` | direct_tls_download |
| ehrflowbench | 179,411 | 20 | `0fdcb88e18d9e35be508a844bc0ba108da40d493b38ea2a42c24eb5a878c656d` | direct_tls_download |
| elicitation_game | 192,607 | 2,960 | `7dab9c3a16ab21fbc590324b59e04613d445edfa7a87a3e669cb121fa11bb642` | direct_tls_download |
| emoji_attack | 11,779,653 | 15,153 | `c07276b4bb790253b57bd17becb4f41b3ee720ad27b829206b899444ac262bfd` | direct_tls_download |
| engdesign | 407,975 | 101 | `768b6622ec26d8194b28a01262134551a0576bcffbdc74339373613e773d7a2c` | direct_tls_download |
| enginemt_qa | 95,476 | 676 | `2c08add9c99a655809d32fda9f1c108d8e38477fa74436d677e8ca561f072fe4` | direct_tls_download |
| erbench | 2,099,744 | 32,163 | `0f8a66afdf4b0e99dd0c4d5c0d88016415c8f21c54c9cb19b949ad8de468a3ca` | direct_tls_download |
| evouna | 801,505 | 5,609 | `f069964c69fc10a87851ee83a9bad21a507b417a73ffdd78d6195aac016864b4` | direct_tls_download |
| exploitgym | 2,996,559 | 1,737 | `863f4c084b5b7ed4bb8752e06122bc5794388e130a78f4a4d99a54fcb09e7a0a` | direct_tls_download |
| faithcot | 146,385 | 687 | `31314cb162c3ac4cd417e3ea69f174a334f5ef0bc067df9208bef49cf694a387` | direct_tls_download |
| felm | 201,456 | 4,412 | `13ec8d1ba82121efb9e0a58acc96b068c7e0516947ec4cef86e0297e78f7afeb` | direct_tls_download |
| fewshot_ttt_bbh | 238,642 | 1,310 | `bd64ceff79edb58d23a1c7fcfed6d8607a708281129b1c59c8c3be6bc0c1c3ea` | direct_tls_download |
| financebench | 43,586 | 150 | `b86240e2c5ad2c985bd7cb571618e66f5d99f6aedad035ab08f4c8f3a810cba5` | direct_tls_download |
| finegrain_t2i | 98,175 | 760 | `e692ef1f35f0493c04efe6743a98c6d4461c08df78ca02224baf68f72dbc9eb0` | direct_tls_download |
| haiid | 37,956 | 152 | `6ceca26301c575e0ee9fd3079864a4faea9c7d9868d42b32b334a90b2e9a2af4` | direct_tls_download |
| hallusionbench | 126,047 | 1,205 | `5eb07f0e6fdedbecae69fc1d2fe618c587925b216673eba30eb86ffe6eb59f21` | direct_tls_download |
| harmbench | 22,025,185 | 62,160 | `83179e4cd4d679cb98d63f297fd7510532b5b4d0007025d9db6527e69911b49c` | direct_tls_download |
| healthadminbench | 308,412 | 540 | `cfd65f829c75382a2b0b14bd64bc613fea051905d64337d8354c2b21af76cbf1` | direct_tls_download |
| helm_afr | 18,227,291 | 72,223 | `746ca65792055395ffbb396243bc3b9ed0137391ff317ef74cbf37a719d22e00` | direct_tls_download |
| helm_bbq | 412,602 | 2,000 | `5c7fa671a16d03d0e685c5198ef6e92629192271cbc78ac167c6c1887f3b2718` | direct_tls_download |
| helm_thaiexam | 537,835 | 565 | `a9ec4112788f16183e8728f52f92afb3fb1336ad81df32df335ae29672404d5d` | direct_tls_download |
| hle | 1,098,973 | 2,249 | `b560db001b69e74c1aaa26c0eef009d20dfae3231009da474a55d793411b09f1` | direct_tls_download |
| icpc2_code_selector | 3,246,435 | 2,175 | `9d063333450063c1ea93c9bc98280813c824cd0d263e0fb2bb866a97627956ec` | direct_tls_download |
| igakuqa | 1,307,550 | 2,942 | `88e77727baa8657ce76ccc273748caf2730f85e486c578fb0a377991ee8aa191` | direct_tls_download |
| igakuqa119 | 288,022 | 400 | `47fab238b463e64c315b3df12fed6e423622b63912bb1d38a22d3840f2306bd3` | direct_tls_download |
| ikp | 121,423 | 1,400 | `9ea2edca9784cbc6f3b72604090b85fc3171cc504bc1ec28b84d1fe6455136c5` | direct_tls_download |
| imagenet_hard | 1,635,016 | 7,496 | `1c1a45055fe36aad47cfb907b6fcb0aff6b3d839d9c3d3d3f32e21c7d277d46f` | direct_tls_download |
| ineqmath | 404,961 | 1,000 | `6b6fb28e47618584168a387628866d72d0640a643b895291d032093630425ebf` | direct_tls_download |
| interchangeable_token_embeddings | 18,303,028 | 199,978 | `60bdf81a71c1e6c34403a25c50fa3b2656eac7311dd76470461a7cc2c98bbe7a` | direct_tls_download |
| jailbreakbench | 297,945 | 2,001 | `7a1e5c66c8056b0c615e032978ef5eb9d383137a87aac081ac6c4739c54fd477` | direct_tls_download |
| judgetuning | 7,081,877 | 3,000 | `a01d40d398bd065ef8317697a47cbb27d7e13bab6c71a7d275336b2f2be53fe7` | direct_tls_download |
| kernelbench | 119,307 | 250 | `16018528e9fdc6d7afcf73ee15bbfc588bff412c16ffb948cf10e804a6bdb7d3` | direct_tls_download |
| kmmlu | 7,298,644 | 35,015 | `ba91ea948bcdd7527666e9eaf5b8a66a339e11f8aca5b15b223d5e285c6aa18c` | direct_tls_download |
| kormedmcqa | 834,597 | 3,009 | `606c84b30b2d3317a2042c841c9f2b72331d9fa0d739f96f9c7c62b3e1e8d16f` | direct_tls_download |
| legal_rag_bench | 78,071 | 300 | `f81665c3635a2ba5f83381ec5f85122367123c7a1c705841c03287574579db02` | direct_tls_download |
| legalbench | 33,112,788 | 9,393 | `5eeef327491fbf0b982b2ede6e7ebc3a57df4d38857c86ce56a9e5c6265e3771` | direct_tls_download |
| lingoly | 6,819,987 | 12,463 | `1e540755959ea0ea0ed032600888bb03cac6a4a046bf6da28b52c379f626355a` | direct_tls_download |
| live_agent_risk | 36,543 | 73 | `6d59450d0a88b0122a17c998640b5238af8483d2733396729790598351d58de1` | direct_tls_download |
| liveaopsbench | 1,069,445 | 5,323 | `c70cd52d4da2fcde0df5e4d51421440f6202e073faa77d582ce63b461ec61aab` | direct_tls_download |
| llm_bp_tag | 51,373,685 | 152,139 | `f62b7a2235ac2d671b028956a21421c3dd26ffc9e42a2ee1db701acad6ffa14e` | direct_tls_download |
| llm_uncertainty_bench | 185,532,357 | 149,793 | `082b37735a4ee4fc634c4741791092eb6f8c0c9c5ce22dcf113f60cc91a2d2a9` | direct_tls_download |
| llmail_inject | 136,504,346 | 207,291 | `c09cfe4a56641f1e70e348a67d902efe012ab0f0b034eb670fdc6de0efd23cdb` | direct_tls_download |
| llms_lean_formalization | 522,309 | 588 | `83975121dbadbee324de243fd01071b571e08d1808add81f5e3c360511e07c59` | direct_tls_download |
| mathconstraint | 216,194 | 504 | `0fa7dfb3f226f589c8a289ef40df271c526c5fa0e8a4e8e8e751176848506721` | direct_tls_download |
| mathvista_mini | 274,317 | 1,000 | `85fd39a1b18654bdaf29f557ceff3feafd846175cd40216de5320635a5660278` | direct_tls_download |
| medhelm_ehr_sql | 451,094 | 1,000 | `73c799fcac4543462caaf643bcd15a7bf2ee0d589ee6f50c1be559b96d681b0b` | direct_tls_download |
| medhelm_head_qa | 339,640 | 1,000 | `73c8f4cba81343097120f557316a2ff1b55b5005a1142642d9c9f5725813005e` | direct_tls_download |
| medhelm_med_mcqa | 221,975 | 1,000 | `c5cb52a6ae7acb3999ef8b2e2a4f9b15ffae02824d65b7d4877cb0ce8ed0df2d` | direct_tls_download |
| medhelm_med_qa | 596,901 | 1,000 | `6dda5aef865667dc91d8feca968c3ebc753db929f0538625e392e89d504fafad` | direct_tls_download |
| medhelm_medbullets | 209,403 | 298 | `54b17226ef81655508f49d081e3142eac60c6cb805c2f959d9c99fe568a16fab` | direct_tls_download |
| medhelm_medcalc_bench | 1,341,826 | 992 | `d6be49b18be83fe296a4ea23af2c691884fc4da18a5a9af15e8dde6e747bb4fa` | direct_tls_download |
| medhelm_medec | 274,812 | 597 | `6ff9a11f62ba530f03811d888832528908c8ffd124b3d96cf25d3c953ed0c85e` | direct_tls_download |
| medhelm_medhallu | 1,927,430 | 2,000 | `5db64b4ed27c3109d9865e2aa3d1a3de6eb1e63dedc988025ef1cf47ed96015e` | direct_tls_download |
| medhelm_pubmed_qa | 1,302,832 | 1,500 | `b7d41c5b5f3ef35c7d21f0c97090bb6613db921fff104d00b9cb837db9db0173` | direct_tls_download |
| medhelm_race_based_med | 134,459 | 167 | `8ff383624a4619ed6afee683c7ba7e2dc51f4740952e7634c21ca856990ae3e4` | direct_tls_download |
| mind2web | 522,164,413 | 17,153 | `ca4813c9fc3307910fdb9321ced12196615ff2afeecb7228eecb22c1bea3fa5e` | direct_tls_download |
| mj_bench | 5,853,312 | 26,564 | `52852f870b47b606e37ab4bf7806ad2b4ca93683f72b5bf4af72a3957cd7349d` | direct_tls_download |
| mmbench_v11 | 2,176,586 | 12,175 | `b86c098eb22376627bfd1fb5eb17eec37fa5cce1793fc990595badd0abb7fbb3` | direct_tls_download |
| mmlu | 8,397,018 | 14,015 | `3ed1d85dc3cb852eaa1ed352320cbbd4285d07d76a9fadcc48abbb40ee093b1a` | direct_tls_download |
| mmlupro | 5,263,166 | 14,226 | `0260255dad59a3ace57dc87d4b86044290623d4279384b47fb751fce92992370` | direct_tls_download |
| mmmu_dev_val | 351,718 | 1,050 | `ac201c3f787f07b1ef042e9f39257f568073fb8ca1fe90ec78459817ebb3250b` | direct_tls_download |
| monkey_power_laws | 1,068,636 | 525 | `f3d6c37ca172d3453d6ed6e1a9279447ba13f397bd34afcaf86ac32ebbc99e86` | direct_tls_download |
| morphkv | 74,626 | 537 | `04279a6b5d2d4e787704c48d081b98ff770bcac2b3098a3100e86b537a395067` | direct_tls_download |
| mtbbench | 606,021 | 573 | `11d91be9f0726d5663e1f947e7253dbbe4470124e3de7e76f27d1be7a1ec263e` | direct_tls_download |
| multi_swebench | 59,055,510 | 2,127 | `21cc67f8c5811cfff671ae0dae34056aadd1f876918c64fce4a4a3b3a28c27b0` | direct_tls_download |
| mypcbench | 35,464 | 118 | `fb75886fd90eaa87e954216f1175a7c7c8d1260cf126c7fa134a1d2d968efe0f` | direct_tls_download |
| naep_llm_students | 475,569 | 488 | `f1823d0fd6b9d79d3563b334fa4774031382b0868aa2bad218385b5ae4d797bc` | direct_tls_download |
| naturalreasoning | 379,249,825 | 1,145,824 | `d74365d88e2da1eea0749d1ceaed6575cf026835153ccd799249ed96d6a506ab` | direct_tls_download |
| naturebench | 329,489 | 181 | `3c98ff662edef6d19b5c12fb404c2251006fadba42586ef264ca7a6dbd77f4c8` | direct_tls_download |
| nester | 44,019 | 356 | `005833a08a5ff70217831b88042907f790ef5eb1957277ed8805b8918693bdc7` | direct_tls_download |
| nyu_ctf_bench | 116,852 | 400 | `4c3156ae8e7226554ca1b241a87846b7d2c8b43275232f436ab335c6538a060f` | direct_tls_download |
| ood_prediction | 25,782,472 | 142,805 | `f40114366935329e79832451c312d13d8847547919d910fd5c4bea0854c80436` | direct_tls_download |
| openbiorq | 2,117,263 | 657 | `3ced52663a715af78cac94204528b9648204e00a64871e826e0b7f8339921c87` | direct_tls_download |
| os_harm | 76,284 | 512 | `3daf3b9b273538fa23633777c446667d802c4dd9de49787243a6cb035ecd585f` | direct_tls_download |
| perfcodebench | 1,181,957 | 1,854 | `f879a5f3d076e0a9bfa299c99857bd18318d2823f541888ae8a042ace1abb4de` | direct_tls_download |
| perumedqa | 1,852,747 | 8,259 | `00d71a689de53769c89badd0daaed837a0181b1ac558d0caa86bf94876043961` | direct_tls_download |
| pku_saferlhf | 4,661,620 | 39,994 | `5d02020e2e6489e342966e80112a18716b11176b5c9432da846d08ca9d881efa` | direct_tls_download |
| planbench | 4,501,756 | 11,076 | `e9d2dabdb376cdc9d5d9dafd58e8951c5eef5785e87f83742f4a43f1d8b0cd60` | direct_tls_download |
| proofaug | 67,262 | 244 | `e04e5b6bb51307f8cc6ae294e2d251a856276e858c066d8c87ea948c9f7d234b` | direct_tls_download |
| prox | 1,909,958 | 12,052 | `242f47fc58488c328856bd9096038b9c9d0e79470dba707a5582cf104e8e9924` | direct_tls_download |
| pxplore | 1,523,346 | 787 | `ec6af81935c6bedad707cae0c28cfcbb543763e21b697b486de223c9c07f7b19` | direct_tls_download |
| radar | 17,581 | 1 | `b51abb29d3b386d53035e83b39e0b59b982d6a86b5e83d3908f628214ebb3b69` | direct_tls_download |
| real_webagents | 48,588 | 233 | `5908db1f903c608e00911d50ca7ec0fa0e1b5bf4a09365d4ad52e0e1fde8f136` | direct_tls_download |
| realtimeqa | 1,350,861 | 7,954 | `cf195a933ec29d837aa9074fe19bce1a03e507d79abcb5bffe6d17ebf7572506` | direct_tls_download |
| reliancescope | 5,607,400 | 1,200 | `3ee78b9d92ab0bb2aaa237f6505ab78f92ad513d08844326a59bafe8309e13d9` | direct_tls_download |
| researchcodebench | 8,928,605 | 212 | `3aee135afa6b206cbce8867beca681811d95579db34a0c0eed1822d8c6b01268` | direct_tls_download |
| revolve | 121,763 | 310 | `5df01d17a693882f92d2ae3b13a5ec1484857cc019bf09622190c6823a5f8fad` | direct_tls_download |
| risebench | 171,703 | 1,080 | `4ae5b84d003982fb8857a5efada1950c6ebf684a5a2208292dcea2d04da356df` | direct_tls_download |
| robust_reasoning_benchmark | 282,596,765 | 4,895 | `20f450dd137e77f5321fd2e198b8e709d80d2f1093045af1464f894c54232587` | direct_tls_download |
| safeagentbench | 58,212 | 665 | `93b8b6dfaa39dbb14da77254bedb090d4bc9fdf34d6343aa6f78bba6321b4cf6` | direct_tls_download |
| scbench_long | 37,625 | 4 | `465341911124b933ceeab906e3aa6e09d8849bac53d336ab9fcd9be8e8f20cc9` | direct_tls_download |
| sgrades | 19,500,725 | 40,509 | `8cba11c6d0771894ebd09366018dc4b92dd9dc2b9f97ea471e43dc5ae865a6c1` | direct_tls_download |
| sib200 | 13,238,260 | 83,640 | `65192519f170ac87b103f19e2f6dcd5d5af975def51d7d44a1bb3865c6e6ff97` | direct_tls_download |
| sketchjudge | 1,094,006 | 4,053 | `c035fcc4750cd1aaadff57d2c6338394e967101f21b98aa1551e4b1be3f1d0c5` | direct_tls_download |
| software_world_models | 29,751,858 | 434 | `6e106b0605e877fb7e13f65ed68fdb840f5c36e710c03edea30a59edf3fac7db` | direct_tls_download |
| statqa | 696,538 | 1,183 | `56d495ac71c3c741ce45b78d309bfa3d4654042df276db64f94c1e9a08554691` | direct_tls_download |
| subjective_qa | 7,750,739 | 10,921 | `7f882b006454dc4e55c9ecedf43d0055299fa76fdf011ff1497d1822fc6af992` | direct_tls_download |
| sugarcrepe | 2,590,871 | 15,024 | `14c56c7747f70efa8137d3c6faf69d20cac74d9fb637050281dfae5a8c3aa3fd` | direct_tls_download |
| sustainable_food | 297,038 | 500 | `84a82a6bff8d5572e3c5987eb0ea187a3cee0896a3deb3701dcc90aa7c593789` | direct_tls_download |
| swe_rebench | 39,763,649 | 6,306 | `78fd183af256d62c7947a74ee714018d2eb3cce13191fa2d5f2f4593df8e3c5b` | direct_tls_download |
| swe_smith | 244,658,364 | 15,616 | `b1c15996050e2d2740ad1082bd7da0b9e5e0736408e70678396508b7ac1b4803` | direct_tls_download |
| swe_together | 1,431,405 | 109 | `36d03a25f2d2619538de42d3ee74a9ffef85244bf75879cd8da5a3b9e7858076` | direct_tls_download |
| swebench_live | 158,410,512 | 2,202 | `1bd5cbdfeee8b7a046643da1c99666609b0c3ffcbb9b4ac65c25231a69b901fb` | direct_tls_download |
| swepolybench | 5,777,467 | 547 | `5858931cb1dfff3ed4ba7df62c556ee5014ac48dc898acaf9ed3ada0221e4185` | direct_tls_download |
| tau2_bench | 8,084,868 | 2,388 | `fe6c77d369d041a0a1c1d8ea76c07091fb4b7ea415fee6008618f77a5a9b438a` | direct_tls_download |
| taubench | 85,082 | 201 | `a532e73d595f69d38c84060ec73085003bdd61848bb194fdd6a0a9ff5afc4b44` | direct_tls_download |
| tensortrust | 237,325,576 | 570,791 | `22f04d7d081dcba56095b50c747641345286db6fc840eda4aa61eeaa5fe81054` | direct_tls_download |
| truthfulqa_mc | 258,185 | 817 | `b47d549ab5ffd657eea9ea2dc8992e656f86a86d9a24762d96a6b2d5644e4449` | direct_tls_download |
| tulu_human_eval | 89,911 | 1,028 | `bd3f3436f86a8585b75613c864375b372f0d2d91bd74bf2cea3e8167a28c454c` | direct_tls_download |
| tumlu | 58,958,276 | 133,944 | `88430aa633d24dc613e7567d7916f12ef7926600bcc545458b17c61d22ff6ea9` | direct_tls_download |
| txbench_pp | 28,333 | 12 | `e64647ebcd45311043696e296e6327829d951ac245bebd49c612bd5b9d1db85f` | direct_tls_download |
| visual_memory | 7,029,297 | 47,500 | `3c5474934bfd9949f7b1aae9c931b992c1c4b5fd717ec4f01e8386dd5e1fd04b` | direct_tls_download |
| visual_riddles | 264,977 | 793 | `d557d3f898f2266040e27424c52d93426f352eb67eb7f1a667f525b1c00b7f1b` | direct_tls_download |
| visualwebarena | 63,193 | 200 | `eec6afa8ecff597b7e4250a36fe58d3aa274c731c7dd2d77b04485aa0f386d98` | direct_tls_download |
| vl_rewardbench | 1,222,169 | 1,532 | `17785ac86ed515b204366b74ef6555174fa35dd98470cdf16dff9690079d7522` | direct_tls_download |
| weavebench | 1,478,425 | 114 | `9a91c7c104cbafcfc7512b1b52cf368ef89111d49176ef98b7d95d32155cbef1` | direct_tls_download |
| wikihow_agent | 18,085,920 | 14,287 | `a66c8b21ee90a1236ebf764312cefb1b1ce4c232a989cfbc33c4138e545e9342` | direct_tls_download |
| wmt_mqm | 10,484,526 | 207,090 | `e994f8b0eb27482039ad8c1a08aa1e47081f0cf1e949ad8716d2d3f2acc6f334` | direct_tls_download |
| workarena | 86,657 | 385 | `6e7224da6cd8589c87be19a505048b84710a412ab7fce495ecc31ec171dc4def` | direct_tls_download |
| workbench_revisited | 100,968 | 690 | `b64b841a2d1d0985a7129b293c7343457f7cca2e182dd8da9f2c4d406030e744` | direct_tls_download |
| worldcentralbanks | 37,275,231 | 119,925 | `22a1db8a94797d9c542ee79dfe33fdbfd26776d8f05f7cae4e07ff87e9ed9aa0` | direct_tls_download |

## Appendix — all preserved benchmark/subject/response input hashes

| Input | Bytes | SHA256 | Recorded integrity result |
| --- | --- | --- | --- |
| abstract_reason/benchmarks.parquet | 17,092 | `8e2c91805dc91ad86b6710aabf71085156e438a43ed7846b9fcb47d0643c0824` | PASS |
| abstract_reason/subjects.parquet | 6,495 | `040593fa9128e3108866d269b440d11d4565569e196c7686782dfa34a35f7d17` | PASS |
| abstract_reason/response.parquet | 346,118 | `59893c65449b1223ab6a71ba139e63149786d7660ad64c3f3a34dcacaedddfcc` | PASS |
| adaptivestep/benchmarks.parquet | 17,623 | `0fb51bc5fb75ea72935f35a00ab98da56b3ed847678e60ad9178738ee884f07e` | PASS |
| adaptivestep/subjects.parquet | 6,565 | `32d6e7b49e34b05c83d9bb5cb0c175cf4e717a42f1a40809465d89e175b19065` | PASS |
| adaptivestep/response.parquet | 18,906,610 | `fcc7a28f9e30327cf2af9804b453c87a02ed225cc121f21de8f39bf1ef9dd90f` | PASS |
| advprompter/benchmarks.parquet | 17,275 | `a0d1a827722261553fd74d0ba11aad7edff82b43aa3b6948664253061993eb75` | PASS |
| advprompter/subjects.parquet | 6,622 | `0394b0c10f9d573383fc4f4d7df2a919f671941788a1356a9bac75bacd837051` | PASS |
| advprompter/response.parquet | 8,478 | `0211545a16febe197ed45877be2d68f4c07626ef88e627f2dc538fe9c273cfa6` | PASS |
| aegis/benchmarks.parquet | 18,113 | `1451963030814e81990d1a6dcefde6cf27a91a63006aa0d1e405cec9fcad6b54` | PASS |
| aegis/subjects.parquet | 7,636 | `7be08182aab9a9922e2a125e5b00343a9e14a100c7cec564da65957e941b2348` | PASS |
| aegis/response.parquet | 439,109 | `924bb0387b0a90b7d2a09248230e5b75326fc939bc925030f87b23874db4da23` | PASS |
| afrieval/benchmarks.parquet | 17,608 | `d4bbb04d1bad19b5d938700ee66849c0f7b0d64e451e3a050fa7064b20264cc6` | PASS |
| afrieval/subjects.parquet | 43,949 | `82d0098f307c00012ddda7b14f9848224475f1eccf2758c0338799c90345e818` | PASS |
| afrieval/response.parquet | 32,763,498 | `9ef4f721f4fe2d105eaa68c5d895a11e98bff849b20ff8409ac7d103e53482c5` | PASS |
| afrimedqa/benchmarks.parquet | 16,603 | `94ee26a8e60e1ca707193962a2723b0dd36fbb577857ebb4ceb521044d41a40f` | PASS |
| afrimedqa/subjects.parquet | 8,931 | `09b8bd0426537c59192cdeaac1a5f597f0711661a907ced9bc9c882b488d237c` | PASS |
| afrimedqa/response.parquet | 10,809,179 | `c8e24b3c79de1a7160a2b43fa77bc61f953db6aeaa1d91b32280d5f65e1c3c64` | PASS |
| agentic_review_perturbation/benchmarks.parquet | 17,334 | `282ccb7ff0a6aafc0efb8774bd9ff2a9dc842f1318ac274bcab8e2b81bd52bf0` | PASS |
| agentic_review_perturbation/subjects.parquet | 6,849 | `12254c0aea7d5ae93af6648a1b08107bb63486fb6093f2dc9b40d8cfc6c5eb93` | PASS |
| agentic_review_perturbation/response.parquet | 13,673 | `e4ff1e47348981f9e32c2d919d0e85a87aa1a28e55a0b2d3aaed61d3c58295de` | PASS |
| agi_elo/benchmarks.parquet | 16,625 | `c7859745ee6d7eaed727afbbc39f97f7fa10afd90b6fe4a68deec0d7a8f66949` | PASS |
| agi_elo/subjects.parquet | 7,996 | `33a7ee8739d9d05acf1de17069c3791ab92b828edaccc3973fd04d80fcfbb3f5` | PASS |
| agi_elo/response.parquet | 10,391,446 | `e10fdd1ce2c39483dc5c878394e3b9f3561cecd2f2480e773b6a0996b867a0f7` | PASS |
| ai2d_test/benchmarks.parquet | 17,367 | `3701e5ef546cfd7cb54f1f185bb81b27a24de49322b87e81d6066d27a0be80f9` | PASS |
| ai2d_test/subjects.parquet | 21,544 | `1e6d74a9d3de04a7f796be107de1421541186d4e22d008c07a1c33af51a27b88` | PASS |
| ai2d_test/response.parquet | 19,856,672 | `dc0853abdefe687251f6118c2c17f5cb4b982fe315e34b0709477205ff08234f` | PASS |
| aider/benchmarks.parquet | 18,138 | `1d61fae1e56920ebb7509ae3f6f657f2dacb83d31db7cad0b4bc44f96e4d5474` | PASS |
| aider/subjects.parquet | 9,756 | `1b8a0fa1836de42102779358e156c54999e8f936d4aec6339819265120e5f77d` | PASS |
| aider/response.parquet | 106,716 | `9e3e6e231242d33053373d635919d6c3aaaa74694d988ecf1ade333ae2369100` | PASS |
| algotune/benchmarks.parquet | 17,522 | `b037f4938d32844f5df1c3f86cca701e167da568d3605e8e3c4e3c9e2ff0a83b` | PASS |
| algotune/subjects.parquet | 7,988 | `7e8fd95d157c3d49d0ab4956a570a4d6a234c8ec7f49104af472a22d08286cf4` | PASS |
| algotune/response.parquet | 60,286 | `66454f671fb545f99d012d212dcd82156c2943fced9c5be82318fc674142097f` | PASS |
| alignment_faking/benchmarks.parquet | 17,775 | `35ea703afc682a9400758cf6042c92213aec4fcc315f39c38a9fa618bd38cb5b` | PASS |
| alignment_faking/subjects.parquet | 148,183 | `777921d21feb3301cd5b295b0f2b408f6515c0c8d447b5b938367998dfae5c7c` | PASS |
| alignment_faking/response.parquet | 42,954,219 | `944469057d9c5499e5d24ee00804b3652a217d7cf5fbffa8d20f747e3cb1769b` | PASS |
| alpha_sql/benchmarks.parquet | 17,205 | `1908074ff2a68572c6fd9b3f0dffe4e35d4a5bc8a9b62709938d7866ecc1de13` | PASS |
| alpha_sql/subjects.parquet | 7,458 | `17c199cf2b0b3c356812965d0f7b7545579aa728bd23634b4eaf05ea88ac9ba5` | PASS |
| alpha_sql/response.parquet | 62,474 | `772a7fd827e50a4d89504c4605a2b5e2b917dc30ff1d8385d7072ff691cce609` | PASS |
| appworld/benchmarks.parquet | 17,262 | `d0aa40dd5d3e1652d99e58645475620ad4c564005bdc6ff454b11cdd08ad5145` | PASS |
| appworld/subjects.parquet | 7,506 | `39700cd3eca5efea9ca4e29dacb9a30372a99b35fc22a45157b7853e84dc730d` | PASS |
| appworld/response.parquet | 229,064 | `a15f0c5f85d435d9fa90ee17b9e2cf303e9439dd2b85e0f151534173e21f1f14` | PASS |
| auditing_sabotage_bench/benchmarks.parquet | 17,268 | `286e5634304815b9373c65eba0e322a69587002b27296d896b4513f0d9958e32` | PASS |
| auditing_sabotage_bench/subjects.parquet | 8,905 | `55836cf422f6ac0fc6c07fd6e644702f526a751c88f7339b26ad3612e7a92053` | PASS |
| auditing_sabotage_bench/response.parquet | 42,946 | `5c4ba281202a468c4b930eaa67a0640defe269ab14a8f97d8fb58c6fbac1de88` | PASS |
| averimatec/benchmarks.parquet | 17,410 | `6117952f9cba359b8e78ababf96d52bd5ff51ddad6e19807fe02e6ae3f90957e` | PASS |
| averimatec/subjects.parquet | 7,456 | `d6da6a09cdd230081b872b7086b201c582f3aa00cdb19103dd302bb77b30962b` | PASS |
| averimatec/response.parquet | 11,136 | `af1d2805e3505d9a489357c1a875f761c85585c7b58c6df880f86f6852bc226c` | PASS |
| babilong/benchmarks.parquet | 17,101 | `2ec32907221928244079fb0087e7061f11810b6b435b8e4d581e5d120be8b74a` | PASS |
| babilong/subjects.parquet | 14,429 | `7057ebdae4d4d646975820e22f70a0750260b11a25c984038ddf35682b348928` | PASS |
| babilong/response.parquet | 75,589,828 | `4239cdb64fbd26be2b7bfd4ba4b7c1f806658b9080126c797913b36bdfaf6efd` | PASS |
| bbq/benchmarks.parquet | 16,461 | `b3cedc9a7b1a469df95631cb8386d5186742d2e9e4055d765f496da5f3041e6f` | PASS |
| bbq/subjects.parquet | 7,161 | `63c7fa4d4e0de201f7d6277f178aaf97aab2f610e0aeed74197cc475a29c0905` | PASS |
| bbq/response.parquet | 14,243,974 | `4b1ad142c0652475e807369f87d94f1d19d07a2e1d1b5b3c357f270faa3256d0` | PASS |
| beavertails/benchmarks.parquet | 16,896 | `be264ef70fffb88b150cbc25f0066668bc3091cfccde9e429cd7a4493ebac64d` | PASS |
| beavertails/subjects.parquet | 6,977 | `2fa69259ea06562298346133c9a0ee65a6b2c3082e09142b232233ce1ade53c7` | PASS |
| beavertails/response.parquet | 45,008 | `7367901e99aadfde4e9c6ad444413fbb97cabdb097bfb8454793817dad67c158` | PASS |
| benger/benchmarks.parquet | 17,338 | `42f33c2e4e6c4d75e9b5a75a32f4bfb07da58a5583bd9473f89d0faca8c07941` | PASS |
| benger/subjects.parquet | 9,088 | `eed8ff929c05f66a464262dae1eadf279313a8770605ba346414a1a2f2581745` | PASS |
| benger/response.parquet | 208,497 | `ef3e19ea78134dfe20d1a86bf3559531ae33292a2611c52a79414b7dec7f41b4` | PASS |
| bertaqa/benchmarks.parquet | 16,888 | `f7a577a4ba050be0a4150d33dc903bdfe677b8c682831c550a9a6fd9a85a8a45` | PASS |
| bertaqa/subjects.parquet | 7,282 | `0ded33a6193ca7c496e188630d163ed62f2c89dd49a85e5ceb55eb88789bac07` | PASS |
| bertaqa/response.parquet | 2,143,408 | `bdd7c044e384ea1db7c9a234076ae024db39f3f7691fb52caabd5761b910c80e` | PASS |
| bird_sql/benchmarks.parquet | 17,107 | `099a9b3c37f70fd2d67288ad8627d5c574cdc1744d7d8ad68e380a495c320505` | PASS |
| bird_sql/subjects.parquet | 13,394 | `5344027c99a304c6de848191ea82d481635d425454661886013a2656d3be0a65` | PASS |
| bird_sql/response.parquet | 857,770 | `a6d47ab7cb8b5f654b9ffcf8653890c8272cf2094696b7917ed97e9ed2e73493` | PASS |
| brace/benchmarks.parquet | 17,693 | `6d8bc0fd3b6d5b2477d05a3545da036cf903ecc9ba9d80ac63347a39fc185972` | PASS |
| brace/subjects.parquet | 7,527 | `a6f226083f72cb3035ad4404cae7afbfbb325fda415fcd402349b569d7f79837` | PASS |
| brace/response.parquet | 5,785,374 | `f87ba5941185ef220f3c08b127382dff114fb03eba0bb9a0b83a157765c28620` | PASS |
| braveguard/benchmarks.parquet | 16,968 | `c5a246335adbcc31b038b5e2f73853dc4eaa57046ee3499db6ea1948504ff5c4` | PASS |
| braveguard/subjects.parquet | 11,066 | `c243045788bc088eecd4e0e9cb5e83778cd543464fb67a7783a8993edf1ec9ba` | PASS |
| braveguard/response.parquet | 25,755 | `2080ecfc8c8152d5e1fb6383b0a0ff916e15b2cb9cff55568a73acc1a35e823c` | PASS |
| bridging_gap/benchmarks.parquet | 18,023 | `3b2e1b1f84a53d26a6d0837d67c42b96578092cd5aec01c78a805fbae994ff4a` | PASS |
| bridging_gap/subjects.parquet | 30,341 | `2d1c9bc7043a70e7264fb45ad7330de2c144f9eceefac3b3fc4763c18ac3204c` | PASS |
| bridging_gap/response.parquet | 165,534,304 | `552362a9d2f2d02ad95e19e942580bad2861f76be152837e4b985ef10c1dffd4` | PASS |
| causal_axioms/benchmarks.parquet | 17,319 | `f519d6071af070255f0823e4add40d2f3d76f7d1f21e04e9f419de035c240bb4` | PASS |
| causal_axioms/subjects.parquet | 6,747 | `20c3d793a848a80c824702a8b8b1075a763854c1091fa634157fc24e84cbd386` | PASS |
| causal_axioms/response.parquet | 265,395 | `743ff26e695e7e297723a0ae90d9ef26b188e0bb104d3f7deee98daafe4980b7` | PASS |
| cellverse/benchmarks.parquet | 16,547 | `97443ed363c9e12511aec20ca6a0bf9686ced36e71cf98ad875834c56b6db1ea` | PASS |
| cellverse/subjects.parquet | 6,536 | `8f44dc8c4573a3c6034c030f9cec7e3362820eb5c4f2abfcbaacbb1641b6b6ae` | PASS |
| cellverse/response.parquet | 33,360 | `b3876e4bf8949da97607b37df8df063358d611b749d285e3227f31e5bb389d23` | PASS |
| ceval/benchmarks.parquet | 17,331 | `9549a56280fab9aeaf4bda4cff05d5d1cb41c80799ba963e93225fe9d5607b05` | PASS |
| ceval/subjects.parquet | 7,290 | `57f1e1c2ffd32b44ddb5b31f277a5b56b16309f42fc3e43e7188eb636da5f001` | PASS |
| ceval/response.parquet | 351,210 | `306c1a7b5b16b5286ea0d5f4d7ce53909936f1bf06d81b856ba8d4cbd37c3c28` | PASS |
| chartmuseum/benchmarks.parquet | 17,023 | `c9281342bc27c923b59f43ad3f5f22e5c6a40dd742d7443685ba82ad0e0c38d6` | PASS |
| chartmuseum/subjects.parquet | 6,706 | `35ae33016ee275604fd833664527e0482ca840fa1fc16592f1d937ea0e5a205f` | PASS |
| chartmuseum/response.parquet | 11,489 | `3b8378afd4a93809d2c4539fe1b229be0677dc67072597904fa82aeccf49ec85` | PASS |
| chi_bench/benchmarks.parquet | 16,656 | `9b33fd1eb63a82772332aa547b568797c2326948e94791e66294ad5d2d764fca` | PASS |
| chi_bench/subjects.parquet | 15,053 | `33e9c443ca7df64687771c9f3e0224b9e98cd31b2a322057003f15e2649be4cf` | PASS |
| chi_bench/response.parquet | 176,015 | `eec0c23474da86e5a1c5272235c9f1240716e18b0ee5c9ff53b300c2e6513ac9` | PASS |
| clasheval/benchmarks.parquet | 16,919 | `8662dfe73488de294c81d46eaa63de47637308c660b4dac24e9798706be32688` | PASS |
| clasheval/subjects.parquet | 6,867 | `72803e2a70db2c8ddff9162383991d7773d4cda6fde15b5e0c78e5e420f5d1ad` | PASS |
| clasheval/response.parquet | 2,701,083 | `968ec1c89c5b3ebb2ae082bd000848baaf36bd9428b5a42ca19f239daddd21d3` | PASS |
| cmmlu/benchmarks.parquet | 17,735 | `d315214ca30ccf7a9345ec56252876c483e13745e6f61095c5f96038fba17753` | PASS |
| cmmlu/subjects.parquet | 8,344 | `51c514405ab377e8ba4fb29dfb7b62a44273062505f9f1b0c04eaeda1e87d311` | PASS |
| cmmlu/response.parquet | 5,633,594 | `b42a1cfbb7a6973c483d42ac455fc6840d77e1ab0620b16c7195b5fc791d65d6` | PASS |
| confagents/benchmarks.parquet | 17,090 | `2cff83d0a2280f1f884d66e80698a348f8e460b0f896299ceebd3403617a36e8` | PASS |
| confagents/subjects.parquet | 6,568 | `0cfdecaf8f3b274637b06bd0c1e5c14d0c675751232c55ca724c8854f96b3f6e` | PASS |
| confagents/response.parquet | 7,018 | `8c470b8deebcdae873597494fe2dbde44da4d2a8b330bdfeb249d8a125a4cc0c` | PASS |
| critic_discernment_game/benchmarks.parquet | 16,849 | `e87272019e8f6e7652f9e5800b4b75933d461bd5ee443a40dc27e2808af0d654` | PASS |
| critic_discernment_game/subjects.parquet | 7,628 | `376d495dca55855b281306a65f0f886bf97260d71144d1aa4a887bb7504c5689` | PASS |
| critic_discernment_game/response.parquet | 182,548 | `0f2ee09b83d840730145cf10a98dcedaeaf655245551549fd7ecc2faac25e676` | PASS |
| crow/benchmarks.parquet | 16,333 | `abb60bd8a857488aa5851af0e5a3c100abe635eaa5ae793fc21d5ef0b8d6bf5e` | PASS |
| crow/subjects.parquet | 11,068 | `e66c66a5e481380108f7b0a4d19983e30cd9e63612dea0abcb13f08ab9d266ee` | PASS |
| crow/response.parquet | 163,547 | `5e8e07b74ce40bd731d0a37bcb5b7aa381bc9719538d508676401c1288d4b6ed` | PASS |
| cruxeval/benchmarks.parquet | 16,528 | `a7fc2360f43593f6bca435554c40920da0c5a41070e3e89fe07237238bfc0d0f` | PASS |
| cruxeval/subjects.parquet | 8,658 | `7dbe35df7cde9123f35a00f1e5f0790142657c660ddc87302be3ddbddc2def83` | PASS |
| cruxeval/response.parquet | 20,809,388 | `f777c5280cc1cc8963a76a13b8bada16b2a68f207d03fb77e4f03ea3b459aa6c` | PASS |
| dave/benchmarks.parquet | 17,672 | `6a6b2c92c3124e2012eab2924e403b45ab4be8c49350be8ee53f4ac3f8fc3e5a` | PASS |
| dave/subjects.parquet | 7,126 | `449ba6631cea24863649baaec9c20869d808c6616449f94a535f8fe55941d56d` | PASS |
| dave/response.parquet | 458,974 | `e674d6d5e555c130b51d87905d77c02d23847e250c4703fc62c9225911f721ec` | PASS |
| dbpa/benchmarks.parquet | 17,337 | `5a810e5ad53beb078cf6010fbf0ce1167e816fbf35217a0964871849ce1b519d` | PASS |
| dbpa/subjects.parquet | 8,024 | `030c8f5eac9c7c808427c6fe2010ed8a70ed8015c1063872632fe82d5a7258ea` | PASS |
| dbpa/response.parquet | 15,192 | `b617d2ed40b82a55a3d0ea68fd035f6fd8a7b02943abd967dda261954981aef3` | PASS |
| devbench/benchmarks.parquet | 18,212 | `52fcf1e7c4f2eefb0d6d3fead86864c79ef1ec39c30f88da3273a5ea500c4f74` | PASS |
| devbench/subjects.parquet | 7,608 | `ceb38afb741d0ff421ea63a91ac8641598150e33f190008d905ab9f10065eb04` | PASS |
| devbench/response.parquet | 108,551 | `10c7a198606929c5863b8b9ae1d81c93e639a082eb89df42bc14c0328d00c4eb` | PASS |
| disco/benchmarks.parquet | 17,480 | `caf40e3a1124238c58e9fdf7fc337f4b98695d14d34e3b59377cc0e5d31cd289` | PASS |
| disco/subjects.parquet | 7,947 | `cb253aa39eafc703236628e9adc9fd9dae3b4c690c953eea51fd17a1cc761da0` | PASS |
| disco/response.parquet | 3,009,568 | `fab86f87ca3b506642f64fe71f88818000c690c810edd7f832c23d844d9263c7` | PASS |
| editbench/benchmarks.parquet | 17,666 | `835a23344276f43582c930cba439492bd5bb15f5c45f1b883436ba537b1bdded` | PASS |
| editbench/subjects.parquet | 9,394 | `455dbf129e6becc190935a7fd763f3c55b2f2905174fe2765f19be4125f1e953` | PASS |
| editbench/response.parquet | 477,995 | `10e60a511a5d3276a5eb83598c61a6a9340c49db0ee8b15ca8e2dd95db02a250` | PASS |
| edu_circuit_hw/benchmarks.parquet | 17,833 | `5c848e8700d262f523132457279327b9d7180f4574947be0c205fc71bde1bb72` | PASS |
| edu_circuit_hw/subjects.parquet | 8,051 | `c2f3a4bfe6d99e23e51552c17437c555a446174c9d397a0f7a1a1f701f95dd99` | PASS |
| edu_circuit_hw/response.parquet | 74,414 | `8f8b58b100e4a26e00fe661b494f4c488d88926ec3257169cd38a5d20bedd4b8` | PASS |
| egoschema/benchmarks.parquet | 17,745 | `1d51e1a8fac5bff8576bc2fef9eca0d2868403e0a3900e2ff3b75832c3eddaf7` | PASS |
| egoschema/subjects.parquet | 9,035 | `fbf5394185f2899f14a92a61739b6ef2558ecc6864c619be77812d06620513ad` | PASS |
| egoschema/response.parquet | 193,441 | `9f54c18b4582f91d6e9d1e98c715224216c9f7f4aa2e616ae2a28f1c72375d89` | PASS |
| ehrflowbench/benchmarks.parquet | 17,984 | `ea66cb57961e6cad458c807b513113c81bb6e80e6fb5613edb37a1221b65de8e` | PASS |
| ehrflowbench/subjects.parquet | 7,796 | `bbcb17b519a65cb76422b46875383e4e30b746f13adeac5fe6dd09ec7a03aa31` | PASS |
| ehrflowbench/response.parquet | 9,078 | `d601ee7de8e8876093cc50898ddb0873762733bad02490d25a3cb860234bdabe` | PASS |
| elicitation_game/benchmarks.parquet | 17,399 | `112ad8d8abaced649732c0bbd32fe112b4fb2ff80eb1dfb00a44ae5a03aac9eb` | PASS |
| elicitation_game/subjects.parquet | 7,819 | `a08c09715513137aa3f1618ffe2485479eaf77604a825cf930183a2a551f55b0` | PASS |
| elicitation_game/response.parquet | 359,332 | `5d40a39fd9ac88a9fe36deba1842f8753fc141436e8413dfe3c0e1d4fb717199` | PASS |
| emoji_attack/benchmarks.parquet | 17,887 | `2bfc2e27ded4e28d21962d0a21f7af6fafa98f75b70b570ca89027dd72490f3a` | PASS |
| emoji_attack/subjects.parquet | 7,412 | `e2de920a0eef05b3cb38f9ec2c270ee713f82516a0ba44d953d122d81de59cf8` | PASS |
| emoji_attack/response.parquet | 1,561,567 | `1ec13073970586996d5b60a406322c57cd98f78668789d2b22b88dd97b65beb7` | PASS |
| engdesign/benchmarks.parquet | 16,783 | `5380263e49f5b5626101d23a9d0fcca655fe82c0228f1646e3caf1e27e1c74c7` | PASS |
| engdesign/subjects.parquet | 7,482 | `dcdbd9dbbb8aadfe0bbefb0ce41c9c7401cfa62e3a180e5d5c80fc486ff34c14` | PASS |
| engdesign/response.parquet | 110,006 | `64c2da202f93afee5e36971cd2cd5bf199d84500e097d385c3d819f5b373b22e` | PASS |
| enginemt_qa/benchmarks.parquet | 16,931 | `dac0241add6b073c8b564ebd3b97159213a0528adc3f36bb49b75095bceb6668` | PASS |
| enginemt_qa/subjects.parquet | 7,238 | `f23f828e1caefe6304fc706bfe5965fc295b9bff667788b8f5ba32ee086b6be2` | PASS |
| enginemt_qa/response.parquet | 30,930 | `713f043fd52959f9960bf83e032aeb282afdb91a462547e9e7e4c837496a1690` | PASS |
| erbench/benchmarks.parquet | 17,167 | `ede9961b8218947d7d900e0c4a92d5347e42dfecd9d1dfdd183fec6c3d5ee5fe` | PASS |
| erbench/subjects.parquet | 6,753 | `9646f275559c214fa08d451c22d87b4deae46e71b1fdc5f16673823c717e3a28` | PASS |
| erbench/response.parquet | 7,991,324 | `bd056ba26743f1b898f220b92442e27afd30fef506d537f79ff29021eb266533` | PASS |
| evouna/benchmarks.parquet | 17,185 | `f5bb9fbbb8af883641b1e63311bd0a4ac1c6258707621bf90770b62259aee334` | PASS |
| evouna/subjects.parquet | 6,788 | `e9e85658e70bcbef579820833472c0d676255c82814dc7a91199b4ac168ae5ab` | PASS |
| evouna/response.parquet | 850,921 | `84f25faf0c32fc2234d5c78f648842909d57c3643cf2e485634a0b41275c5768` | PASS |
| exploitgym/benchmarks.parquet | 18,359 | `2446c8fc8a23b170836bd6ce143d9b78022e289833820cc6e8bb2308a45591ed` | PASS |
| exploitgym/subjects.parquet | 7,397 | `210e0183f1b715fcd15ca166efd2bf7af44b715119c6143e582b98e4311b4cf5` | PASS |
| exploitgym/response.parquet | 161,460 | `5fa390ac69db3749ddd866732d045bc43a241ad622b9a8c1db4696c15598dd24` | PASS |
| faithcot/benchmarks.parquet | 17,619 | `a9a4bcafe10d8a20fa9a5042559fea7f417096b7e5afe83a3aa3ac433f495c63` | PASS |
| faithcot/subjects.parquet | 7,155 | `b642644cec1a6435c418c96422029e106edb9170a703a9875ce1f5348c04a99f` | PASS |
| faithcot/response.parquet | 69,907 | `21b6fcf9a49f6d8995b8db797e8f581325204c1dad0b26390b7c2cc1ce7689ed` | PASS |
| felm/benchmarks.parquet | 17,280 | `7348b698be0a71751eba1be4a53f59b83f0eed4b05233e182495a6348b279c3c` | PASS |
| felm/subjects.parquet | 6,969 | `b3011b707d1310b72202bf6159456c5c55d9118619bf4624a933c1e18d83bab9` | PASS |
| felm/response.parquet | 169,982 | `f2550fa7f57da53729dd5fd7c22504e57dcefc4f4829595564a6a58088c1d9b5` | PASS |
| fewshot_ttt_bbh/benchmarks.parquet | 17,170 | `712991a976b78d5c84a9b90c9164b9af02fdf6af0d51d42b607bb146aebd26a3` | PASS |
| fewshot_ttt_bbh/subjects.parquet | 7,659 | `9fc0a8e1914cff8aeed6ee2e51400a10ef5828ba16b740452cd0e779e5d2d676` | PASS |
| fewshot_ttt_bbh/response.parquet | 176,995 | `2a4700833ff4e94941cf415c90e3885ee13906c41a29c9525a4f50f7c0eceb27` | PASS |
| financebench/benchmarks.parquet | 18,178 | `a127d4ffbc51e48989b49ef375ca5354dc4bfb88fa117e2e5fad12dc14c4d5c9` | PASS |
| financebench/subjects.parquet | 8,210 | `60043d9fcc3b17908defaa203db95c2ca09330e83f9a39709212e83c20264b31` | PASS |
| financebench/response.parquet | 53,892 | `1b7c8eb6d6498c45b1a27cd6ade8b968842399c20b10077dd6f7847ebd912a16` | PASS |
| finegrain_t2i/benchmarks.parquet | 17,461 | `1456031ae5e80a0cdc64bf52077fbd4cd2e4edad6aed499bdc9946af2b678458` | PASS |
| finegrain_t2i/subjects.parquet | 8,735 | `eb80739a6969639e841073f065cad2b463d38fbfa4553d4e19a553750a663573` | PASS |
| finegrain_t2i/response.parquet | 283,869 | `a7137836a2db3f901eac277af7451424ee21c82b277363a01550b40289092f53` | PASS |
| haiid/benchmarks.parquet | 17,356 | `895f251455fdd8e5150583835c969c7516aecb22494e75a7f80062dbdb4f9657` | PASS |
| haiid/subjects.parquet | 131,671 | `cf61dfde246a2051f4393c6f3b639dce7ec83b09ea95bbe81c0aae2968500459` | PASS |
| haiid/response.parquet | 2,347,899 | `7146c9514de7a71cb05e7582675fc64d82b7a5bc6cee53cac4de007fdba20b3d` | PASS |
| hallusionbench/benchmarks.parquet | 17,508 | `b95bb7c8105def1e36a5c736922e4211885098ea497ca65357c9cde6391d48f6` | PASS |
| hallusionbench/subjects.parquet | 24,893 | `04a05bab45d628214d43c1c140882e029ce0bdff8ca7952ce19d56af5504b5be` | PASS |
| hallusionbench/response.parquet | 5,272,228 | `c8c4280ac954a05e4f629d5cfb0d56fa80594906666443b98fbfd24e4cf78d10` | PASS |
| harmbench/benchmarks.parquet | 17,474 | `ac34f3f9a963623e76525af5cf57f53f935932dd4024bb085cc47e674d1825bb` | PASS |
| harmbench/subjects.parquet | 9,413 | `9720ecc81bf53ad35bffdf3fc8203d46de769eb3891d323f1533981a8818c9e2` | PASS |
| harmbench/response.parquet | 3,210,981 | `d52a1b761cbebddc1800977c8bfbb18d9842a46e63483288286341ba36031ffc` | PASS |
| healthadminbench/benchmarks.parquet | 16,931 | `bdbc50d38d2ddeea38b5ebbf4fe1ea4149a04da7a374b30ebf37de2669cc1b66` | PASS |
| healthadminbench/subjects.parquet | 8,407 | `449ab0222acab63cbc43db30bbb25968dda748533311d7336022aea9ef5924ac` | PASS |
| healthadminbench/response.parquet | 155,946 | `4165643d92f54ae14ca9a62d84bf9b9ba238041f19948d91eab82a9f4d12e432` | PASS |
| helm_afr/benchmarks.parquet | 16,560 | `f2576dc38fceebbcddb15fbb9d49f61baa64f2da08708a884b9dc4dad7b87be6` | PASS |
| helm_afr/subjects.parquet | 10,751 | `a5d1c1072438fcb5ca3163bba203b6fae1cc3beaf22c67a351a9db11bd496323` | PASS |
| helm_afr/response.parquet | 18,477,493 | `b4d83673944f49446548f53f1d17ad507c0cef4c08ae80719eba0eef8425d3b8` | PASS |
| helm_bbq/benchmarks.parquet | 16,778 | `d9d89a646cd7f2bd0333fbfaf316366333832e052dfd2879ec33f8354c07b731` | PASS |
| helm_bbq/subjects.parquet | 16,169 | `3c5a4fdc7572f361d499262533e9204918b0caa0e320aa958f341c6693263cb1` | PASS |
| helm_bbq/response.parquet | 1,726,527 | `4256e22ffeae7362a56efa6740361a990a399a46fdb4ec4c2849af0c2a16634c` | PASS |
| helm_thaiexam/benchmarks.parquet | 16,577 | `7917c3c13732bad95932accfcf1cbdc6cf42bb28f0697f26ed830f29638f6c52` | PASS |
| helm_thaiexam/subjects.parquet | 12,814 | `94fe8b31ee79719dd95db6cce83460c90c1be06da6d171926bc306c215cb0f98` | PASS |
| helm_thaiexam/response.parquet | 489,008 | `0aa989d87516b30adc32b0b8e2701f146b2cefafcdf52f933127d2292f4a4eb0` | PASS |
| hle/benchmarks.parquet | 17,528 | `7b4814c0a4d04e8e5b83aa290c66ad1923ee974cb6294a0bf82ea32771ff6af7` | PASS |
| hle/subjects.parquet | 10,457 | `b4983ea42c740932df6e500be72b2b986076525466711cafd6c8181633e66b1b` | PASS |
| hle/response.parquet | 330,211 | `9edcb3b07cd766d792b66be0d4596d2cb791005e7866349ff30a5006e7e7cb88` | PASS |
| icpc2_code_selector/benchmarks.parquet | 17,947 | `fda749d3b53a6f9f8594ac79d0eacc2fb279fc9eae406b3f781d9fef9310574a` | PASS |
| icpc2_code_selector/subjects.parquet | 8,458 | `791b1e21cdfc3cd03e2c63b6bd771de4d229252d0e54063e931e5f5caadda9a3` | PASS |
| icpc2_code_selector/response.parquet | 1,656,217 | `4994e1c41b1d7d977a98aed04c012d69cf9e8d36cf5ec43235aa8fd2ab402df3` | PASS |
| igakuqa/benchmarks.parquet | 17,467 | `06b289015167256c0a4dd077cea45f905eafca054120b7552cf71ca34fd22838` | PASS |
| igakuqa/subjects.parquet | 18,541 | `b33aa0d42f6f777bd5a5cca79dda78dbd3393703cf6f85c299c5f2b0038defaf` | PASS |
| igakuqa/response.parquet | 249,283 | `b42b00775e04c088607c2d39613c388b66dc7b40384026d9d0f3722a6af32780` | PASS |
| igakuqa119/benchmarks.parquet | 17,478 | `393155019511995b5dfebfc2ccdc38c45146e534f7b26bdb5a57e4687e18ca9d` | PASS |
| igakuqa119/subjects.parquet | 7,846 | `8775872382cd88c7511f41781c15b8453931f25891942c9f594fdb8db599acba` | PASS |
| igakuqa119/response.parquet | 20,616 | `163be31cbd1d517116bdd4953905a0e2455f1b0d63449335608b495feff8dc9a` | PASS |
| ikp/benchmarks.parquet | 17,603 | `249423399160b2a15123e47028fab17a1e1e7e95e52024edcacaa77df1d02415` | PASS |
| ikp/subjects.parquet | 14,486 | `07a6c1ccb44d0133d03430cb71b461a50dab161c9352c8882033e52f06e25ed1` | PASS |
| ikp/response.parquet | 5,974,722 | `12096ea71e0cd77bc846a9e4ab61ba424ea44642fe099db9a21b866eb8b18ec5` | PASS |
| imagenet_hard/benchmarks.parquet | 17,571 | `38aef2a6699b039b71ac2ee7259e3d37ce120fd443b91c0ea8864ae945340644` | PASS |
| imagenet_hard/subjects.parquet | 8,210 | `4bd35e8a31fce6817b7840cd7cfa9ad1f76fe9f6e7c667e3b47c28ff46f9abe6` | PASS |
| imagenet_hard/response.parquet | 3,802,961 | `d8628e6d659ac22fe0c20066932ab26a9dd12d60ff7980c105078c6a16be04f6` | PASS |
| ineqmath/benchmarks.parquet | 17,325 | `88160c02785d32324125d719c26a5d5b27a4bd404971a47e335d82460a6853b3` | PASS |
| ineqmath/subjects.parquet | 7,659 | `eb7e6137182f5e6104d510e3e27c1ed914b79df3284674edc80d99111e8a77f0` | PASS |
| ineqmath/response.parquet | 42,611 | `a10fcbd8b77e5b530007a64328e7c5b36fd7c044d7cd095586330c2e72b4de65` | PASS |
| interchangeable_token_embeddings/benchmarks.parquet | 17,798 | `9c8e35898668af32f005d508aab5f44cb67f3fb1ff97fb37873418c8eb560a4a` | PASS |
| interchangeable_token_embeddings/subjects.parquet | 12,279 | `a5575ffa9a30ee910f08d11dea10c37b425ecc30580392b41f9bc46a327d0356` | PASS |
| interchangeable_token_embeddings/response.parquet | 14,998,112 | `6154f3deeff885c7905a778145f697cc7002c45c36db9c98ef0d6c746ba735ba` | PASS |
| jailbreakbench/benchmarks.parquet | 17,071 | `9beec47e8a5597574f66899b3b42d136b70af6ed280583a3882e18956ef4dc5d` | PASS |
| jailbreakbench/subjects.parquet | 8,386 | `5a1961e2dbec840d2413a700bf7c0379b8c6d62471fca45bc3e64ddd95583de6` | PASS |
| jailbreakbench/response.parquet | 101,736 | `dcc5bb3b227497752ac3f03a85eacb18b247e4b9e3bc6ba8dcef1c3a7ee033a5` | PASS |
| judgetuning/benchmarks.parquet | 17,043 | `13ff0bd571b1bd950ba3d45689487ae376dfa612e5547ba3a22a856f9c5c35f5` | PASS |
| judgetuning/subjects.parquet | 9,318 | `025fc7dfc7a8495f1f910efe56a656f648ba7ea8f48d5dd25739114b43c3fe18` | PASS |
| judgetuning/response.parquet | 535,541 | `2c6269288e4165581fe93d6e2743492bda08e4b8722cbe8e139df52799598b47` | PASS |
| kernelbench/benchmarks.parquet | 17,515 | `b38ab178dba516718ee813805f59841d7866d555d6e3f275057b7936ac1df807` | PASS |
| kernelbench/subjects.parquet | 8,222 | `2b19bd5732597eeabbe62b0e49bfdc1c9b7e6934a928289af71e012140e80ae1` | PASS |
| kernelbench/response.parquet | 1,448,378 | `370d11acf9126faf2732ea469a510f4120046b7a56cc6951a02dbe3f6ae8eb7e` | PASS |
| kmmlu/benchmarks.parquet | 17,173 | `cd6d980d6ec1804103dc8f90a29b5d758152859ae02262e3af45e9984ffadd56` | PASS |
| kmmlu/subjects.parquet | 8,778 | `5b9bc4a4732ef25ee9b9fcefa57b34fc1b6a836a5b168336ea4ce0d651a2ae82` | PASS |
| kmmlu/response.parquet | 37,931,803 | `08dcb425a44dc84cfcf2d7b104cce8013f456460f2e8224b02f18cc1f52acab3` | PASS |
| kormedmcqa/benchmarks.parquet | 17,022 | `70ae5fce05628876b456c857f7e47cee53b36ecb7fa799b34fc4108f59393d13` | PASS |
| kormedmcqa/subjects.parquet | 7,542 | `7257cc1c6b61a56f3a45e38f6ebea5341fd9d39dc6058af5674a141208f99435` | PASS |
| kormedmcqa/response.parquet | 570,951 | `1f38d754fa1b34e2102b4013acbbc393c773b882a2e3c370815e9c89697f7fbb` | PASS |
| legal_rag_bench/benchmarks.parquet | 17,043 | `eb0bb0ea6a274020f804c10731cb25d32431b78fdf97f99fb798c9db52966eae` | PASS |
| legal_rag_bench/subjects.parquet | 7,373 | `6bf11748378f184577deac90e3bd4c88ea8fa7da5b7c993214a7268389acf2ce` | PASS |
| legal_rag_bench/response.parquet | 44,969 | `552edb5de0f9114bdf5540ff6f5ff8219aa498714ff8bf05eb080e94709c037d` | PASS |
| legalbench/benchmarks.parquet | 16,729 | `a27fe51634b8551daada0a520fd20ebc41c9e8942207fbd0588c767248620322` | PASS |
| legalbench/subjects.parquet | 11,115 | `a4c50baa3fe15097d95e582ac06dea90f05285f7a362c47cec2a2772a1cdaa94` | PASS |
| legalbench/response.parquet | 1,522,897 | `9a84b4513e44dc32acdf7f4900ef7390c40e20a973127a55d1f4b89e59aecd31` | PASS |
| lingoly/benchmarks.parquet | 17,286 | `4ac8cf2388c084390f23765b7d5fdcd386b7a46806c51f3150d47b58be9c7ac1` | PASS |
| lingoly/subjects.parquet | 7,807 | `bdfd7de79e215f8975955fb04947666054ef15b104475a4b36f8fb0d4fd5c560` | PASS |
| lingoly/response.parquet | 777,661 | `eacc0ddc9caded2ea8335c78bc9388fede7f59c11dd85fe2c14f0c9f93c8887f` | PASS |
| live_agent_risk/benchmarks.parquet | 17,592 | `39022e3cf33412b4ff953c46a4a7096a0d4f19f56567ab84bb1a83c28bcdf010` | PASS |
| live_agent_risk/subjects.parquet | 10,430 | `ee0d884d73c20cb61eece818d2fddfae7707c00037cde16aba89631d43ea0bb1` | PASS |
| live_agent_risk/response.parquet | 16,265 | `5285c8daa2cb580acb9911e96f7f192d685b0d310ca9950f5d5285c591fe3a22` | PASS |
| liveaopsbench/benchmarks.parquet | 17,226 | `2e67162e9195704f11c8c67d4825bd099ccfb82d1db135b750883fc92fea1bb6` | PASS |
| liveaopsbench/subjects.parquet | 7,824 | `e7904875393dc9f45c914cf517e221a15cacda1b088682b3e16db0bad41db17b` | PASS |
| liveaopsbench/response.parquet | 2,042,344 | `04c17bca06e188c5e32bc75975090334ac864408bbd7937a34dea48ff1ae4dcb` | PASS |
| llm_bp_tag/benchmarks.parquet | 16,949 | `1f0c75717c5823daf221e5242a8c4feb18b9d7f2443e4eb0c2d999cd060a5249` | PASS |
| llm_bp_tag/subjects.parquet | 7,564 | `97e39ca6defe6110c629b16328d7ede11664886d52292c1b869e850b5d5c51e5` | PASS |
| llm_bp_tag/response.parquet | 5,896,346 | `d8e72d48cd7f44e1d32c7c3d9e61dfada1995cff9b53fbbe287d2cee116f915a` | PASS |
| llm_uncertainty_bench/benchmarks.parquet | 17,366 | `932dd5c679c43121066ed94b3168722bfdcd198b8666d3ec5819284c3370b8c6` | PASS |
| llm_uncertainty_bench/subjects.parquet | 13,866 | `46e0c8e33fbcf1fa436e5e589115342547387285b436d191327f43ac309ace6e` | PASS |
| llm_uncertainty_bench/response.parquet | 191,334,518 | `8bad9f47b9ba470831b9aec9e6d36c42f229200cf3308ab1696f539ffe96816e` | PASS |
| llmail_inject/benchmarks.parquet | 17,861 | `ec0d1e8de14f936255e0db45f4d7c2e378e67e146c0ec0035ceeb8d8c417d9aa` | PASS |
| llmail_inject/subjects.parquet | 8,244 | `335fd9c6cc70444555946971f3d0ad30b3f227375f84baa3215a780071fdd391` | PASS |
| llmail_inject/response.parquet | 14,287,879 | `ed5df30de0b889884d2317e2692057a92fcf43384940e315dfb18c4792e850a0` | PASS |
| llms_lean_formalization/benchmarks.parquet | 17,851 | `f78611ea3a0f56d6c2f7f61bb08ce9d447f0a238f1568b86f723af985d96e9aa` | PASS |
| llms_lean_formalization/subjects.parquet | 12,197 | `eb38de41ab0214643e1b797c5c43201da3c7ea7df4c41df1c3f32b7d732b2cb9` | PASS |
| llms_lean_formalization/response.parquet | 1,312,750 | `673f78a26e7448e05cd6adac13660419e4ce0b1df434c091ced0533ce4647270` | PASS |
| mathconstraint/benchmarks.parquet | 16,736 | `cc381281133008ce4ae2fa9c8b1a33fffeb049a326969197e57688fb7cfdb091` | PASS |
| mathconstraint/subjects.parquet | 7,467 | `b517aad0bb1fd6562809aacfc0a53cdb4854a1f824b967d5c6dd3fe7ed90cdf2` | PASS |
| mathconstraint/response.parquet | 260,653 | `6a88ec3bbb763a38904ddfadf4945888683ac00df174c9bb8e21bec0968c3a8e` | PASS |
| mathvista_mini/benchmarks.parquet | 17,798 | `8672d0481563d7277a30df6ff90d4d0a8d2b679830b37c3da543329bcf8b99cc` | PASS |
| mathvista_mini/subjects.parquet | 19,248 | `76ba546a61da459cc4a1efad05978f30a336814825aa8b8db38e485eb5a0121f` | PASS |
| mathvista_mini/response.parquet | 5,950,545 | `8c6c644c1a31d2da33d0a37f463dd0ae768589c5a863e444a739a6ef98334ec1` | PASS |
| medhelm_ehr_sql/benchmarks.parquet | 16,809 | `2a60ab42bbc1aa70e75a3a8806aac73f555efb92cc387d401e6dcc7de297d6ef` | PASS |
| medhelm_ehr_sql/subjects.parquet | 9,929 | `f1e360850f5c2799a6aeafff27bbe7e1e9292ccac2a9d43c97867efe0edbeb57` | PASS |
| medhelm_ehr_sql/response.parquet | 287,916 | `2afacd8f709aa74cf796dbcfbbdcfb0834d4fc84836a5d3a50624b9e9b4cbf4d` | PASS |
| medhelm_head_qa/benchmarks.parquet | 16,771 | `64e703864149a32a83d8606b777579f8d90ab381d9ddd7abbff2445807c96858` | PASS |
| medhelm_head_qa/subjects.parquet | 10,033 | `73e18c691217b6c3aabe0ae2f28c88ace968a3796c18cb5d918eb24dcfd8820a` | PASS |
| medhelm_head_qa/response.parquet | 287,961 | `c2d33781739a29f9b6bca280b146c37dba35f5f0941d58e28f97aef2dba8160d` | PASS |
| medhelm_med_mcqa/benchmarks.parquet | 16,688 | `5ebcd06bc091a8d47628e592ac60ae14ceaecdc7e364d04228d2c4da1e7f1f4a` | PASS |
| medhelm_med_mcqa/subjects.parquet | 9,999 | `80a312a683442106d7d464bd538b763dab8ce912284da480b7ec3e639360e53a` | PASS |
| medhelm_med_mcqa/response.parquet | 288,382 | `3246d509fbcf5e063a273e1461a39b5ba48d0c61c90b72f1f690949e5ba3cb6a` | PASS |
| medhelm_med_qa/benchmarks.parquet | 16,673 | `9833c690fc73757d29c76e9f200f6cda7bf79ada61390598ea10e6e6eabe8aac` | PASS |
| medhelm_med_qa/subjects.parquet | 9,999 | `80a312a683442106d7d464bd538b763dab8ce912284da480b7ec3e639360e53a` | PASS |
| medhelm_med_qa/response.parquet | 288,248 | `2819b08122ed45a785d9fc91b03b1236d229dbe513d1c47e74ae20d927515514` | PASS |
| medhelm_medbullets/benchmarks.parquet | 16,713 | `4043a387ec9c8d0674c6276f5c08c2e79b69d75d5f1357e27c1a4e1e146db25b` | PASS |
| medhelm_medbullets/subjects.parquet | 9,999 | `80a312a683442106d7d464bd538b763dab8ce912284da480b7ec3e639360e53a` | PASS |
| medhelm_medbullets/response.parquet | 86,514 | `9cda3770e38b6212b4515c4dde816e39ba36d80d8cbedd38db02415f60e7c7d8` | PASS |
| medhelm_medcalc_bench/benchmarks.parquet | 16,904 | `ac8080ca5de2b91b6ec479b1e09ff9070d21329819ef0db47c08a7bf781e3521` | PASS |
| medhelm_medcalc_bench/subjects.parquet | 9,928 | `a80fc0c652d0d4c4774b139c9c68fa5c01462027a425f5cbecd57f56691c2e0a` | PASS |
| medhelm_medcalc_bench/response.parquet | 288,090 | `45a7af2fe75a38d670bc073e5f117f920bd4fa48fba14ebc8e0352803d4bba14` | PASS |
| medhelm_medec/benchmarks.parquet | 16,770 | `bc05c98278f84ae2fab7759ccf53a1c8186f391c9f4c91d8427444900a9e6e90` | PASS |
| medhelm_medec/subjects.parquet | 9,939 | `b637b10f63ae6377b63151b0b157c7955f44b62dcf23d76e3cf4dc9da48a1b5e` | PASS |
| medhelm_medec/response.parquet | 169,825 | `8216a29c48ab8008d0686b3ec1bab1736bf4d75bc630c3db318a4322f54d5573` | PASS |
| medhelm_medhallu/benchmarks.parquet | 16,735 | `f81fe9f6cd501e5146f4029c1ed3ce152caf2997edf5ebc6ba40a84e04ae9ba7` | PASS |
| medhelm_medhallu/subjects.parquet | 9,898 | `f4b306addcb0b699281b0e33f6651f48d9ae4195f77081f65a976cb8de47197d` | PASS |
| medhelm_medhallu/response.parquet | 325,086 | `0cbc143133d9a7612f877dd2230b8fa4e6f5dbe0d435d5606b772a49af81c3d3` | PASS |
| medhelm_pubmed_qa/benchmarks.parquet | 16,736 | `8de2c35a15c75e79d9a3a9e0fbf98a4ead53bc0a792415a384ff466351619d46` | PASS |
| medhelm_pubmed_qa/subjects.parquet | 10,006 | `759de1f9b9cc0a84ba6afd6c555e8af02d25fec4cc851f10a852e556991a101d` | PASS |
| medhelm_pubmed_qa/response.parquet | 261,973 | `fbd0358fe63ccfd89bf59dddfff7e468bc0a50a247bdb315382c2ed83fcfd603` | PASS |
| medhelm_race_based_med/benchmarks.parquet | 16,803 | `dd94d1f4b6f8ec466306b87c64a71200a858178bfca84e381cab205cd3fb1aea` | PASS |
| medhelm_race_based_med/subjects.parquet | 9,999 | `80a312a683442106d7d464bd538b763dab8ce912284da480b7ec3e639360e53a` | PASS |
| medhelm_race_based_med/response.parquet | 49,585 | `147380c2408282141c247f475b76655b5ae0bba5d61a96e6f6c200626b64054b` | PASS |
| mind2web/benchmarks.parquet | 17,136 | `bd7939b2c13363baec95cc2637beb7dd06825f8020853834ff4e1cad15a8fa43` | PASS |
| mind2web/subjects.parquet | 8,222 | `22e6486a5a00fb1407027a17141472e35aa6bb2b89ee7a28b8b882bd2567daf1` | PASS |
| mind2web/response.parquet | 646,382 | `0d3e54f0296751afadbf742fb8c3b32698298d946580d07b87e7bb281206140e` | PASS |
| mj_bench/benchmarks.parquet | 18,181 | `7e886edf1fabf2a8bdbcb0f9b8229a32a998c2be50884a5765c4953c497de057` | PASS |
| mj_bench/subjects.parquet | 11,485 | `62b6e9162d31ffaaed60be9d613bbc19b7e0928546f78a3d43e68463ed43f0b7` | PASS |
| mj_bench/response.parquet | 5,508,387 | `7ea952f662b532bb14ce6ee6b2f851d4b8f815a595ae8cc9f34ea82efbbc5252` | PASS |
| mmbench_v11/benchmarks.parquet | 17,835 | `9c0a4bb498ea44c30b093aba031a5f220122b1cc5736d7761d38f17c823af5cf` | PASS |
| mmbench_v11/subjects.parquet | 19,441 | `3389995ea2ef4be2a28893404108ca013fd235864bf34d9ce7eb587ee0c22025` | PASS |
| mmbench_v11/response.parquet | 122,366,043 | `71aaa4635008c26178d252a13c0467fe42211444e6842a8b1e6b5097e599ac21` | PASS |
| mmlu/benchmarks.parquet | 18,197 | `4ccab7366b683608dd1a364cd41d42819ef0f61c216358301a19ec2398172059` | PASS |
| mmlu/subjects.parquet | 28,499 | `e8daab04e0b649e7b4fec0d287a6747382e755835c2282c0d8a0c7286b4af781` | PASS |
| mmlu/response.parquet | 78,907,187 | `c4f823de0671b6275d96c6ee7121ddb6b098f7ea9d94b1bcba12127f798b327e` | PASS |
| mmlupro/benchmarks.parquet | 16,644 | `50918c56640a6168daf7e816c9b8006c4f065779efcaee5c5f38b9d2a8b6dd7b` | PASS |
| mmlupro/subjects.parquet | 9,943 | `5599d2c63e3f598115e3403460923a45ec672869b14145c74985030cd9109559` | PASS |
| mmlupro/response.parquet | 21,145,564 | `271532b41394e8b4ab1afef648afae16279f6df52f697d75b23979d884cbcdd0` | PASS |
| mmmu_dev_val/benchmarks.parquet | 16,829 | `b9e4dcc5fe1decacf394b75b5943a298e1a6709ddd3be0f37bc5d4d0d28569c0` | PASS |
| mmmu_dev_val/subjects.parquet | 21,507 | `442e7115b52a269c2466e4a8cb696ca3394ba4f8f57c96b5a7cbde61808b5f7d` | PASS |
| mmmu_dev_val/response.parquet | 5,689,676 | `86e49d879857da01b43e15791e5cbc920e0407d189d6d00b36544a775d919873` | PASS |
| monkey_power_laws/benchmarks.parquet | 17,901 | `7b3c22497c53293194fe09d0b34adf8c2e0753ca9ee09035a491492be8c9dd5f` | PASS |
| monkey_power_laws/subjects.parquet | 7,637 | `3efdaea2a5c0925e33f2bd3821ba45ddf35f77f100f73ca02bb554d15bfb7d29` | PASS |
| monkey_power_laws/response.parquet | 708,257,822 | `0894d5c6a1072fc511e83208f7cde0dae67bcd1fbead422daf727e6a3a9bc198` | PASS |
| morphkv/benchmarks.parquet | 16,981 | `6d5e632c9f024672141f904d672dc49e5b6da7a35bd954d70f7cf02eefedd8d1` | PASS |
| morphkv/subjects.parquet | 7,070 | `5640d191f89d5e1b45fa3d88148c0abf1235b39b11d19d17e33f95bd0a2bf141` | PASS |
| morphkv/response.parquet | 95,569 | `16e6859d1762b46fcc7caa5b2ab84fb4c9768effd20126d5ae49934653957a97` | PASS |
| mtbbench/benchmarks.parquet | 18,244 | `e3f65fb3ef0396ae85f64f330718991aad947dfd6dcae782ba0731087f56f76f` | PASS |
| mtbbench/subjects.parquet | 12,703 | `1e1d2957a10a159096d861d9501f739917e36de2cf9459ef0725835eb6e4725a` | PASS |
| mtbbench/response.parquet | 194,301 | `c986af96ba5da3357f62b96c2d281463a87e3905bdf2f299fbeb658a3e2e5fe3` | PASS |
| multi_swebench/benchmarks.parquet | 17,027 | `ad1c8d39f85ff0e1a2fc82c7293a6d4f3751d912e46cbf2c6bbb193b1d9c6416` | PASS |
| multi_swebench/subjects.parquet | 9,456 | `06eca4d34e9201ff58c62923a7d76dc315cb9748b308aab21e43e111e3faac49` | PASS |
| multi_swebench/response.parquet | 1,222,393 | `3925964852cede82d958b828f7eaa5f3cc2923a7b8f0e63e783b78a44c028f60` | PASS |
| mypcbench/benchmarks.parquet | 17,040 | `e1e7a652f6bce7b271cf8151a6b6a80c29eba2f32e4226d44cf74bfa5e03565d` | PASS |
| mypcbench/subjects.parquet | 8,272 | `8f01d6d796a0bf8b2067f8b785b0b8f926b497abb9fe7d5ec3ac63878db2b398` | PASS |
| mypcbench/response.parquet | 10,085 | `9bb25104f485f272397ee8891cb01e959c0a7dcb7a19536f587c93f949dacb73` | PASS |
| naep_llm_students/benchmarks.parquet | 17,470 | `dc46c105b90e440cecb3427e96f44f40566e38b09be5906cea852e0a2b07c7de` | PASS |
| naep_llm_students/subjects.parquet | 8,896 | `35fba2d648b2af2e88746d03616c9e9c3048cf18b1fcf9accf663b55cd279a16` | PASS |
| naep_llm_students/response.parquet | 1,044,375 | `a3c8132fc2a3a9e489d5e74184ce04d7e300b2429fb0ded9e480f04dce4842e7` | PASS |
| naturalreasoning/benchmarks.parquet | 17,122 | `796418e2c2b21ede1348a276c83f08bec3bd10da4611a1bc3c65189bd672c5c6` | PASS |
| naturalreasoning/subjects.parquet | 7,384 | `b71c24bf173a0314b5fae4336407a6bf63bc0443d4955eae546ab553aaac892d` | PASS |
| naturalreasoning/response.parquet | 42,828,850 | `451f2e0c7ab61516e5500455d0bd73340fbda8f811a566918e831acaee1e13fa` | PASS |
| naturebench/benchmarks.parquet | 18,162 | `1080a181467eb2ef7372d650fd606da4c0544bd2d9599e817e50077458f8be69` | PASS |
| naturebench/subjects.parquet | 10,729 | `75110f163992470b90e65d2fb7b8870ce21af343f8e80555ab104270f5225220` | PASS |
| naturebench/response.parquet | 48,340 | `8b760ea2cebb80f8865034321c94ba3f72f610b3d30cdd1dd69e3f9981c1a061` | PASS |
| nester/benchmarks.parquet | 18,154 | `919b11294d51b3fa4d230164ca45d881976e2b51b73c6ea7933273e5795f51e8` | PASS |
| nester/subjects.parquet | 6,562 | `ef3acc2dd1d9d5e910b4eacda0e07e1d03618b980c86f9ed765484e2653b78db` | PASS |
| nester/response.parquet | 34,020 | `31a9d074e6cf0565454781b6e357535e34ad4e3f6901419688c09c832f6a2f80` | PASS |
| nyu_ctf_bench/benchmarks.parquet | 18,947 | `9af54bf98c7fbc8bf6b3de9ff22bc9d2bd1e2a8d9212f2d6a66c426c6448f43f` | PASS |
| nyu_ctf_bench/subjects.parquet | 9,117 | `ad54e3722664f8b1de1ada80b0bb85130b77f7f8e742f445f7a30f2f2555c14f` | PASS |
| nyu_ctf_bench/response.parquet | 70,828 | `62a53d8cbd70091355014da9091d8d34b19627b69229c213b6c662cfc63999ca` | PASS |
| ood_prediction/benchmarks.parquet | 18,519 | `2daf5b4d1f066737c27a02256afae1f20f09243c36e67489bde2e39a6ad4ea63` | PASS |
| ood_prediction/subjects.parquet | 6,980 | `8128a355c112bc14e7dca90f8432bee5d35ee94b9f83b422714f1b7d33e086ff` | PASS |
| ood_prediction/response.parquet | 5,345,154 | `f552c632ad73dee1d2b3592713e146b5993b7c658068a42ee2f3e14736943edc` | PASS |
| openbiorq/benchmarks.parquet | 17,067 | `0b891659f2651e2f52e35674d0500e0e75f0c5b30ee9bd6e6130b3f03c008b6c` | PASS |
| openbiorq/subjects.parquet | 7,231 | `26fc8590381459a435407e1a048eaf0a72ef32025e07f772a3e3984b8f682f69` | PASS |
| openbiorq/response.parquet | 156,179 | `c50d2442172e20d2b47c621e20f2a616e189800ca8a3f73bc27d9824bd2bef92` | PASS |
| os_harm/benchmarks.parquet | 16,969 | `3ad03e01871641f3e8323f677a894b47014c6bdaebb3939a1d5381d6ad608e21` | PASS |
| os_harm/subjects.parquet | 8,724 | `b8fda69b1aafb29851a1d2454665028b8b3c388cd31978388bd46aa93b50eb98` | PASS |
| os_harm/response.parquet | 48,620 | `7bafb8213a9ef31cd28335cf602e0e7b6a40b64ae6200bda3bd7b7088c1c89fe` | PASS |
| perfcodebench/benchmarks.parquet | 18,393 | `54f9c555ee4dde8bc6737a8172fc37f8e4c503c8dab2cd8f8435c6b79c595fbb` | PASS |
| perfcodebench/subjects.parquet | 8,094 | `f0bce7bc0c69d5690ba150a149dce5021d05d923a2c5f5e2bd1815d61d210f7c` | PASS |
| perfcodebench/response.parquet | 503,788 | `3832b5437dbb9b0e0c675f833aec120241f661ae5d6d6c17b1e73f155d85da3c` | PASS |
| perumedqa/benchmarks.parquet | 16,975 | `9e4dd84bb70847e7738987a9968c6dd43c33adffd1985d85de81db9f90544c7d` | PASS |
| perumedqa/subjects.parquet | 8,297 | `8a2d656a048a0b42bf708fef0fc3f20b1fdeafb509ff42d8380ec678498c55df` | PASS |
| perumedqa/response.parquet | 3,221,439 | `db36f1448811c83367a84e47afdad423e1d6a1ddecf78d277c53e6a1b7f5ced6` | PASS |
| pku_saferlhf/benchmarks.parquet | 16,914 | `46197caae11bb4b2ae820fba42fb9a0e3eee95b852fbcc2032e49a01bce1500c` | PASS |
| pku_saferlhf/subjects.parquet | 6,999 | `43c2c9f8a97a10f27b9dfb4399590415e9b1cd0d91dc60b3ce7126572acfa218` | PASS |
| pku_saferlhf/response.parquet | 7,169,572 | `bd87014be2fb02df801e7deed00ffe7b7450422b777f7e0cbbe8d4618c5ad426` | PASS |
| planbench/benchmarks.parquet | 17,458 | `49e7562706f81237255948562a7ee0adac98a1436c7ad23df6afbc602b8fbb7b` | PASS |
| planbench/subjects.parquet | 9,985 | `2fed4ba31ec62021b1353bc96b4895a7311051714405ef76f3cdf0ca0895c34d` | PASS |
| planbench/response.parquet | 991,707 | `1c55e47e516fa73cf90d6b966261e23b38013fcec3c346b33526c9435b2bb31d` | PASS |
| proofaug/benchmarks.parquet | 16,922 | `b175d54161db06ed5cd4f309957925cbec1266bac52240e9f2e9bf97830ce249` | PASS |
| proofaug/subjects.parquet | 7,005 | `e07eac2cc3f552054c8782c5d42eb1f26e2b4cfb679c21b183092a589239e0d8` | PASS |
| proofaug/response.parquet | 15,019 | `fd33ff0a05de9e5e41452b2c09cacfee7fb3c298c4a6744e6b61fd2b5ad2f75b` | PASS |
| prox/benchmarks.parquet | 18,245 | `76dc2ebc6cf73a89a68269adbadc8bc3d6512121ebcadc035a64e5ee7ff5c362` | PASS |
| prox/subjects.parquet | 7,261 | `cccdd7ea2308deafbb4f6ff3836cdc05f6ecbce1cb9245b212ebeacc68031fe6` | PASS |
| prox/response.parquet | 912,445 | `a7bf0acc124f72c04d955c2b59d11bc719b17d08c0b0f12d5542fd2e5b87038a` | PASS |
| pxplore/benchmarks.parquet | 17,987 | `8d681679eb319a2bdcb495226d1d236134e8abc2b32e47ced3355aa945c12ddc` | PASS |
| pxplore/subjects.parquet | 7,343 | `210d6bb15b3a9caacaf74ed1eff695171cd5c747effa75e1c13ac87bd34d52c6` | PASS |
| pxplore/response.parquet | 99,248 | `987c53eea4d4ea2a4a0627e2d3d9b192327f8cd617819daf373b1d659b1b6472` | PASS |
| radar/benchmarks.parquet | 16,419 | `11ec81b4c22052b829dc56a7748fe476edd9c1e6db12b1a304a524c8f944dfbd` | PASS |
| radar/subjects.parquet | 8,232 | `314b4e66be4c4af32a9667c423729bcce20e979f5e38ff7f819fd456186b46c1` | PASS |
| radar/response.parquet | 5,551 | `49832c5d09fd9966da476d4a26f6197a93658c36c0dc0767a04da596b225ea51` | PASS |
| real_webagents/benchmarks.parquet | 16,703 | `747b4a61dabe1fbc9f212dfff3cb7afb3a0b7480e6da1eb5e001ea30d60b0c9a` | PASS |
| real_webagents/subjects.parquet | 8,365 | `e563ff232af0d2241220e9857cdc65c64b67b9301aae594677a60ff3308e7fa5` | PASS |
| real_webagents/response.parquet | 94,908 | `56d1fca0b984a30701f165f550e979d96c71b79af3b11a482e4eba5771065213` | PASS |
| realtimeqa/benchmarks.parquet | 17,194 | `bb38e6b1f8c0d5fea13abc9d946536d5cf11ea504160d4e59321ab436ad5f757` | PASS |
| realtimeqa/subjects.parquet | 12,362 | `6bcea8fdbdace3ee914af06a80b87254213ec28e0895528cc798165657c7e54e` | PASS |
| realtimeqa/response.parquet | 1,411,647 | `1589fe0172011f1798f5195b1e69f70b90aba33f780ccc0b2b7955a11fbdd05b` | PASS |
| reliancescope/benchmarks.parquet | 16,872 | `80b8a933464f59244da3ef6fcde75385829c27c7d04d18275f2c80049d00d6db` | PASS |
| reliancescope/subjects.parquet | 7,902 | `46a502e6d9634370c9c2c8f6e833318a0dbba5cdbf4abc3b35e570b104b602cc` | PASS |
| reliancescope/response.parquet | 165,377 | `14eb1128f0db5c493ca5fba86e3edb6cc63c7ccdb70bf9f88f00a3a8ab275642` | PASS |
| researchcodebench/benchmarks.parquet | 16,499 | `935efcdc5dac86f2f292f0cd8c772600595dc09cf81adff20bb43e271c21ae30` | PASS |
| researchcodebench/subjects.parquet | 8,321 | `c8dbb5ac589749270ddea2be6e456ea22b991d5ffc5107fd80d0865a77e94b3a` | PASS |
| researchcodebench/response.parquet | 137,904 | `318c067d86f35dd057e6b4d33114d4ae46447c9ef91e1b4bddba7667fc8c0375` | PASS |
| revolve/benchmarks.parquet | 17,672 | `6b5073f1c9024b4a3f0d64d1c9a018d8a79b800a6d9b4327fcd97a84de80ba22` | PASS |
| revolve/subjects.parquet | 6,675 | `b2212c286372635109f3142ebdea8f87a93d2c6495f0e4219b7c1c97605dbaf9` | PASS |
| revolve/response.parquet | 71,162 | `62fbe077d85714da804c8431c740308f17b6c8ec6f7fa5db5b735a60c32e041b` | PASS |
| risebench/benchmarks.parquet | 17,323 | `3bb42b531dd6cbde2d5de655c22653beed61fbc982cf9146c2119af32513be6d` | PASS |
| risebench/subjects.parquet | 7,989 | `41d2413f24849972c2b743a8b71447e3964e6aa2510fd11bcec39d9d412fadc8` | PASS |
| risebench/response.parquet | 181,955 | `ff701de91d37e147f119d63fc957995edaa4d3d60ccf87dd80ff3a20b709fd7b` | PASS |
| robust_reasoning_benchmark/benchmarks.parquet | 17,561 | `677de3cea6dc2b0aa1a4c23edf106fd1af84d1d9ede52f90463393955acbeb06` | PASS |
| robust_reasoning_benchmark/subjects.parquet | 9,206 | `35deef273ce3c5289401733e13f4e0b6f18b593f86397486f9fa1c9857c33a26` | PASS |
| robust_reasoning_benchmark/response.parquet | 2,910,990 | `fd3e1c0477ae05f897859ecaeab61b4175047d09dfa269cb8213916af1eb5ae2` | PASS |
| safeagentbench/benchmarks.parquet | 17,791 | `746508f56f0f9e3d6b360587a450e839e0993be4cb93dfa2f1bb1a56924e92f9` | PASS |
| safeagentbench/subjects.parquet | 8,113 | `4553d128c585982778407b67fc3bc5a5ded8d6fd49515adc6ac8748ea141c40b` | PASS |
| safeagentbench/response.parquet | 103,463 | `18225c61b6117a3466d0bb0de335ae9fa6fafe19b14fe39858eec2de4a404f6a` | PASS |
| scbench_long/benchmarks.parquet | 17,244 | `48d655925cf7d8d2e0f14780d510446ca0c3ccd4f1d9390bf7419117171b0ab8` | PASS |
| scbench_long/subjects.parquet | 8,567 | `2573aeadecda36589eecdedf5e02f865bc1ed79eb69877e3770ec6d923c51fec` | PASS |
| scbench_long/response.parquet | 12,720 | `97c0c8979041812e21c903258a3f6b0984e2ae9fc39408741ba4c46f2d160b5f` | PASS |
| sgrades/benchmarks.parquet | 17,119 | `662517f83bfd5fc4688253f546f0a9ce0178a0021d26acec5dd5503c88b184bf` | PASS |
| sgrades/subjects.parquet | 13,019 | `af3db37f5148494985506a10f917eedd7a4a48f36c68f47841b98ab166be4c27` | PASS |
| sgrades/response.parquet | 51,267,924 | `1e258beabfefa796288a08c63c78aa317c23803cb2fc6adc6a6cc9a336a60775` | PASS |
| sib200/benchmarks.parquet | 17,260 | `7fcc035ffc96b56f4f43f7387bbf878f257a2dc0ca2feb9faa819f67c5de7086` | PASS |
| sib200/subjects.parquet | 119,932 | `76ab598df13d4622f9f26e42ee756950dcb9e600ada93e5ba56c058a483c43de` | PASS |
| sib200/response.parquet | 17,139,097 | `451de6e16bce2081c599ee4434e59ca4df78c937c2aea3b779d3ef03f39a2fe7` | PASS |
| sketchjudge/benchmarks.parquet | 18,697 | `7c60d3de580f8b02d1a9418786077c1ca48f0e8e5a4efba375113acb4b97ed4f` | PASS |
| sketchjudge/subjects.parquet | 10,267 | `76bc4341b25f75ddd285bdde143e2a41044d78def51822f8436b7d1aa54511cf` | PASS |
| sketchjudge/response.parquet | 934,241 | `f9ab23a38f20fbd78d2abef0c1dc6a3113801b71032ce373ab2cb0105bd707a0` | PASS |
| software_world_models/benchmarks.parquet | 17,100 | `89377c95a7a4713178419ad42625e34e1336905cd657d952090b0445fa1c2daf` | PASS |
| software_world_models/subjects.parquet | 7,761 | `63046d8b91f66b8093ff341b82607df759aa351bdf81399d306b3d4e411f89fc` | PASS |
| software_world_models/response.parquet | 167,512 | `4d7772b9594ccdf4c0ef3f5358ecaf2bc5bd39a392e0970d33875324be72ae4d` | PASS |
| statqa/benchmarks.parquet | 18,768 | `f86fde7a597216027eed6b8f9bb614db5092eb90c725a041cdd5e3d990707314` | PASS |
| statqa/subjects.parquet | 9,893 | `f2ef9f0fffd3ed524f16dfe4bdb6e9f7e4841edc07db4f6124df8453eb0af6ed` | PASS |
| statqa/response.parquet | 1,208,767 | `e4132481cc3d73f0b9846d1a2184f2dd5ee794abca7049251b863739b6fb4521` | PASS |
| subjective_qa/benchmarks.parquet | 16,857 | `8f090bb8298082c69775df0f3e569463894d878064b20ed07bf13c0908830ac3` | PASS |
| subjective_qa/subjects.parquet | 8,269 | `be915fa6be3f75d1df963309ae23a48b5e2bf8421b7e5a7991d774d9e3d1b614` | PASS |
| subjective_qa/response.parquet | 531,545 | `f0cd3cfc0d5407838c2e7ce28ad8c0b1d057efb07bc5fa8e0d40839362330d40` | PASS |
| sugarcrepe/benchmarks.parquet | 19,911 | `bd35571a886c46e1e233c1d7df9ba4855910aa10c828fd49a017c3feb9733f69` | PASS |
| sugarcrepe/subjects.parquet | 6,624 | `7fd81e99929b17cbd8e85680ea3da1cd94a70b4959c8e733b91d8c638e4d05f9` | PASS |
| sugarcrepe/response.parquet | 567,485 | `006dfd5e849c5ec86b17beb834a9d347c039a3328ab27134a90ef45e9b8fae8b` | PASS |
| sustainable_food/benchmarks.parquet | 17,203 | `8b1b3c0ed55c6038637a30e779060f88407106e05b10ea130d58b71176e965d8` | PASS |
| sustainable_food/subjects.parquet | 7,656 | `c836af5328d88a9bd707ffaa142a499812d42d18ce16754565ceb7a62086ef9c` | PASS |
| sustainable_food/response.parquet | 71,483 | `8a4fb288bdcb5289d2bb83a0f73d337756f8c0f9fa634e4886856c2ba6ad3f04` | PASS |
| swe_rebench/benchmarks.parquet | 18,096 | `76f02f3de1d9a94806eb08aa04e32119c2cbfe9c04bdf2c30792bd3b7639f821` | PASS |
| swe_rebench/subjects.parquet | 6,747 | `4f2f5f3481c2394acb74f2905a51dd12d4191c946f44dc48bf2ff1ebcee448ad` | PASS |
| swe_rebench/response.parquet | 1,994,128 | `097bb00e2a69a5ba92907e02b7e6b451bf520e5076fb905fb442fb4ffd51f39f` | PASS |
| swe_smith/benchmarks.parquet | 16,366 | `f21bc0a7d26e18fd152afbd6981efeeb338abc585e709c6151dba90e107447e8` | PASS |
| swe_smith/subjects.parquet | 6,794 | `d89118121fdef1c009acf5faffda9e5a6d2f3ce513b00407bd33c491c343eb4f` | PASS |
| swe_smith/response.parquet | 1,703,296 | `910eddf51ce753274c4a366871eb2a1b21668e9cbc6bc367bd99cf985fdd3894` | PASS |
| swe_together/benchmarks.parquet | 17,081 | `a92063cb39ed42570339f81cd4fbaae7da5e444949fb6d2adc661fc2a38a9afe` | PASS |
| swe_together/subjects.parquet | 8,193 | `176f0b6981dbe0d3183a1af6467730b7c81aa4210fd9237c03421ce8a74bd28d` | PASS |
| swe_together/response.parquet | 91,130 | `b0ec3a12f6f9762674f4292453823fd76ea4ad95ae934fe64e8ac9c0b42f8cc6` | PASS |
| swebench_live/benchmarks.parquet | 17,970 | `e2c1e384aab39fdd607907c28aa34ff23978e671deed43407e5eaa5ad6a1b808` | PASS |
| swebench_live/subjects.parquet | 12,059 | `6bf7f9430efd6ac2b63f6201f090012368e8e87c5438b4fa63e54f07c5243a53` | PASS |
| swebench_live/response.parquet | 356,917 | `eff9fa5a50047917c0ca2ede8369e017ab41cc4cb2944766aa59df1ecb398034` | PASS |
| swepolybench/benchmarks.parquet | 17,369 | `27b9be4d20ffffa110ef3979e8e42f7dffa2f57a53c9f50382f665bc4c28271e` | PASS |
| swepolybench/subjects.parquet | 8,273 | `4135982ddcbd1d245ef9446ce7ecb1e80f6a480e3f3cfcc842112d26eb3cf87f` | PASS |
| swepolybench/response.parquet | 52,216 | `a9084aeeafa54a62c86c43e9ec45c57d4d8eb848fb635dc2890b342d2dbd1cae` | PASS |
| tau2_bench/benchmarks.parquet | 16,891 | `385680f2cb3b14aeebac40a1289935789ff0b1cf9e19bf0f924c8b4f8d1cb618` | PASS |
| tau2_bench/subjects.parquet | 12,735 | `ffc5e6a51d192d268474618f0c767c382672ef090fadfe1e781e21a6e2eac587` | PASS |
| tau2_bench/response.parquet | 544,938 | `9f72ea3e5a25161f5e0304a7f6ab4e67f2ad733229747f44d88dac0cf95e2376` | PASS |
| taubench/benchmarks.parquet | 17,406 | `97b0df180f57c189a1c3c6ea995cb7b3a64069cfb9d89202e64a45111aa8e496` | PASS |
| taubench/subjects.parquet | 12,955 | `3b1f8eede9c84a63540ea24a93e8c654d8fd766357975896f221ecab7bdd78cf` | PASS |
| taubench/response.parquet | 193,234 | `55a421a56723edaebe488d50afeb1bd16e9751cc666467653dcb2c7e71697b02` | PASS |
| tensortrust/benchmarks.parquet | 16,748 | `5c29deefa4478e66a2bd3fa098c1915ff405d0841bc71583209811ea4e476261` | PASS |
| tensortrust/subjects.parquet | 7,026 | `8a3e3ce00847cff1ae0a4b32ae169de5a228512969c29a9837c920957df6cc44` | PASS |
| tensortrust/response.parquet | 24,624,915 | `ab41541a7a5c514a1eb5211361107a1551180c1df8e464def4cad0d785af0e30` | PASS |
| truthfulqa_mc/benchmarks.parquet | 17,765 | `32368320935fb91da785d2e50ab3bb20fbc7c0b04b8989417c3daf8590fe0c2f` | PASS |
| truthfulqa_mc/subjects.parquet | 28,499 | `e8daab04e0b649e7b4fec0d287a6747382e755835c2282c0d8a0c7286b4af781` | PASS |
| truthfulqa_mc/response.parquet | 2,586,569 | `57bbf6b3bf12e82b439fc69cb2fd59a0f11706b4cebb863d0d541e49b27a2870` | PASS |
| tulu_human_eval/benchmarks.parquet | 18,266 | `89f14427678fe8bd26b7462bd8ea6c64059041a24541034a9caf6fb63830f8ed` | PASS |
| tulu_human_eval/subjects.parquet | 7,900 | `601015b071a379c615d8d17bf3d0339c55ba812cd981764bdf3db51598436ea9` | PASS |
| tulu_human_eval/response.parquet | 84,217 | `fef37e3470543ac1342befa3530e7d6431cfef65cba35eb683effa32ae6cbd26` | PASS |
| tumlu/benchmarks.parquet | 17,652 | `f441b14cd77561fa04d1c1202e7e9c0a920922910abe82cbc52dcbad67d59c81` | PASS |
| tumlu/subjects.parquet | 10,006 | `783651c5383909fab6fc9feb2a417c4aff967ee44dd874b0b96ff2b23f57d386` | PASS |
| tumlu/response.parquet | 6,650,075 | `c2def46d6b124d564db98bd734ffe87b7aae93af3c9e710f422aad53b8cffa65` | PASS |
| txbench_pp/benchmarks.parquet | 18,531 | `8e26d12afcb963a793e2d19ccefed8e54762fe93228041a8f1a11a04ece40ab3` | PASS |
| txbench_pp/subjects.parquet | 8,319 | `2c5493ef7953947e7ef8defe9a34cdb7e8496497cfa6c44e7b67c90028a22433` | PASS |
| txbench_pp/response.parquet | 16,851 | `e3d66094e48d024d9fc013a2da3c6017410482b8f02b834cdc4ae4d883ae1fa1` | PASS |
| visual_memory/benchmarks.parquet | 17,740 | `276193c3c565e185be018cc811d2ad5b7f7f6250fc99e7c93e7a509bb07590a9` | PASS |
| visual_memory/subjects.parquet | 7,108 | `438137267aa8b0dbbb41c03801d055e6967ff821542132bd09f8fe9e3b97c008` | PASS |
| visual_memory/response.parquet | 8,799,837 | `a5222032ae6f3bc63d06f2396f94e2dfc63aa0d73159075c8c44085b5fb39c6b` | PASS |
| visual_riddles/benchmarks.parquet | 18,236 | `c33dce72f542b99af332c674c76dec10ca2b4f8035a13a094711025bd5f83c6a` | PASS |
| visual_riddles/subjects.parquet | 7,874 | `7e999562146bd43aa89f2d0397f1cf9208fd6ee3cdcaf0edf487dcd76df80480` | PASS |
| visual_riddles/response.parquet | 82,018 | `9377374e64ad60d3241d414df72260dc77f5942c73118f7e2f5079c015931fd8` | PASS |
| visualwebarena/benchmarks.parquet | 18,171 | `aab3686ba54cffba88a9d7951ab72a5615923e8b609fb94a1c885de1d4c6d4ea` | PASS |
| visualwebarena/subjects.parquet | 13,626 | `d8f75234b9e4117654c4050edcf775f77b742c0d6eb27e425c3a1e012ff4249b` | PASS |
| visualwebarena/response.parquet | 20,607 | `45690bdd395c7cdf95b75b6441064929539fcaf5d05ec144ba10f5cb464cdfd4` | PASS |
| vl_rewardbench/benchmarks.parquet | 16,445 | `2a155cb678f52ec79bf67913139d028d9025daf9189c37e6425b1ad4bcd01106` | PASS |
| vl_rewardbench/subjects.parquet | 7,365 | `c8cb4d7cde1ef9c99d12b013f2f850917fd3be56b9cc2d37518b0f08b0c406b3` | PASS |
| vl_rewardbench/response.parquet | 2,605,842 | `97ae8a3339b5eea2049019fd8aecfc82df69e5a85eb8acac046703836bbf462d` | PASS |
| weavebench/benchmarks.parquet | 17,525 | `66b4d9c7c6c50b01c22c22a046b8f8e7ddb67ed1cfa78171b466937cc4fb2085` | PASS |
| weavebench/subjects.parquet | 7,188 | `f8655051124a4b3aa639144589a724165ccd25bed0b421d1347ee519b44ae13f` | PASS |
| weavebench/response.parquet | 10,122 | `1397ba490ad0d2f4ddb5cff947dce87130e4dd6522fa3532aa37bc848a1bc8c7` | PASS |
| wikihow_agent/benchmarks.parquet | 16,419 | `69e46113f85b9d88730dafe004228ade3d96d09b21d0960b17f77e8bdb69eaef` | PASS |
| wikihow_agent/subjects.parquet | 10,501 | `ca3ff701d611288387b453054ff4ee077101afadd597d0dbbfd1fb0938b88996` | PASS |
| wikihow_agent/response.parquet | 6,418,919 | `1a2d1741c90962cb9cd642fcea6f61278ace2074bf66a99ff256a96bade639d8` | PASS |
| wmt_mqm/benchmarks.parquet | 17,022 | `0d981524abdfc1ac5501e601e7384057ff95f47f6ef404faa09ff8799398d8b8` | PASS |
| wmt_mqm/subjects.parquet | 13,525 | `992903e45fe345138fe118c72180cffef73410a3b6cb9fdeaa7f0ccd31e2e8e1` | PASS |
| wmt_mqm/response.parquet | 135,527,858 | `e131b88a9774bfa2506344e1a49271d3f6587873086f357602a50d5de856dd7b` | PASS |
| workarena/benchmarks.parquet | 18,161 | `98096cefd6f1df3499e1fd6222dd5fa06c773c5ae0c0e121027390e9eb97b03a` | PASS |
| workarena/subjects.parquet | 19,265 | `87f88a783f77a352f4690b923b6ac9ba461b28bc609e05bb557a1b291a8f91f1` | PASS |
| workarena/response.parquet | 21,894 | `938f16332824703433fec48ae2cc1fb1beb9d9f199d057110085d185b41c0a3c` | PASS |
| workbench_revisited/benchmarks.parquet | 18,115 | `a8b826f6a2dc3fc6e33a72597b544889e8106e01aa50070b71a3add0f45d5469` | PASS |
| workbench_revisited/subjects.parquet | 7,748 | `9ae8e4f16e212e28bd556dc8b36aa1a745c4da65addd403b39c9abbc5447c3af` | PASS |
| workbench_revisited/response.parquet | 336,781 | `5b06ab5cfb5762f5e8f59e788d609867ddb4b35827cdbdc5412971f606d0f2f3` | PASS |
| worldcentralbanks/benchmarks.parquet | 17,021 | `a4aa3edd51d1d19ca6fab5512b91e1706df0a92ed7207b8eac32300d67bee67a` | PASS |
| worldcentralbanks/subjects.parquet | 8,370 | `cdc872cb4ee7f9faa744aa93065f8df3c9b500b09a013c0157ca8a48ca61fa8b` | PASS |
| worldcentralbanks/response.parquet | 10,418,569 | `0f7fbd80f776f63323db167267107765d3e304f4a89d262cd51473ef73912887` | PASS |
