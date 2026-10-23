# C2B0 one-shot calibration report

Inputs and immutable SHA-256:

```json
{
  "c2/model.py": "14ed10f59580da8d25deb41eb4cf5d945b94f31aacf7e995f2cccc424e2756d8",
  "irt_shrink/model.py": "1d84ecb67c8b772a3719078bf2ca067d2bb0802ba36489e45181d4886bd4dcc6",
  "c2d2/provisional_packages/C2_r1.zip": "70ff16e31d76195fc07c487a446c0a17f3f2fd63f234d81035f05e9f7e6ae31d",
  "headroom/pair_stats.csv": "74ed5d32c9f5714702384e43f79c7e0c58626ab186d5a48ca902a77aaa1f0ca6",
  "c2d2/evaluate.py": "e58ea02c8b494db458e3403b7ae8a899bc99d5fdbf8e28c3dccb94cb028c71ce",
  "headroom/measure.py": "a2ed788351ff1029a72f3d4bfe6adc7a41b97b9c6c10c050a12cd705d4bb8248"
}
```

| Method | ALC | B0 | B1 | B3 | B7 | B15 | B31 |
|---|---|---|---|---|---|---|---|
| C2 | 0.1848401766 | 0.2488973551 | 0.2080542620 | 0.1882908100 | 0.1717180728 | 0.1582704372 | 0.1468372469 |
| C2B0 | 0.1879808620 | 0.2803042089 | 0.2080542620 | 0.1882908100 | 0.1717180728 | 0.1582704372 | 0.1468372469 |

B0 benchmark-cluster bootstrap 95% CI (C2 − C2B0): [-0.07898230948549159, 0.008787343865300959]; 2,000 reps, seed 0. Fold wins: 3/6. Maximum prediction delta at positive budgets: 0.0.

Fitted parameters and gate results:

```json
{
  "metrics": {
    "C2": {
      "ALC": 0.18484017662654537,
      "B0": 0.24889735512042896,
      "B1": 0.20805426200103744,
      "B3": 0.18829081004539874,
      "B7": 0.17171807282148555,
      "B15": 0.15827043724025494,
      "B31": 0.1468372469286715
    },
    "C2B0": {
      "ALC": 0.1879808620045337,
      "B0": 0.2803042089003121,
      "B1": 0.20805426200103744,
      "B3": 0.18829081004539874,
      "B7": 0.17171807282148555,
      "B15": 0.15827043724025494,
      "B31": 0.1468372469286715
    }
  },
  "b0_ci": [
    -0.07898230948549159,
    0.008787343865300959
  ],
  "fold_wins": 3,
  "max_abs_prediction_delta": 0.0,
  "calibrations": {
    "0": {
      "alpha": 0.10230401944587193,
      "beta": 0.13874669688628155,
      "lambda": 1,
      "pairs": 11543,
      "responses": 16395999,
      "gradient_max": 0.006842260550039822,
      "optimizer_message": "Desired error not necessarily achieved due to precision loss."
    },
    "1": {
      "alpha": -0.6481015183006615,
      "beta": 1.730764591167715,
      "lambda": 1,
      "pairs": 8171,
      "responses": 27999528,
      "gradient_max": 2.493366757505555e-08,
      "optimizer_message": "Optimization terminated successfully."
    },
    "2": {
      "alpha": -0.7770508006742042,
      "beta": 0.3419749309034935,
      "lambda": 1,
      "pairs": 9118,
      "responses": 32805279,
      "gradient_max": 1.2829603236563791e-05,
      "optimizer_message": "Desired error not necessarily achieved due to precision loss."
    },
    "3": {
      "alpha": -0.8299658243361699,
      "beta": 0.3092088727084918,
      "lambda": 1,
      "pairs": 11822,
      "responses": 29488018,
      "gradient_max": 0.0010057432061222338,
      "optimizer_message": "Desired error not necessarily achieved due to precision loss."
    },
    "4": {
      "alpha": -0.803397449699185,
      "beta": 0.6100088951026402,
      "lambda": 1,
      "pairs": 11990,
      "responses": 32833680,
      "gradient_max": 8.05124924407874e-06,
      "optimizer_message": "Desired error not necessarily achieved due to precision loss."
    },
    "5": {
      "alpha": -0.762762376049263,
      "beta": 0.43012063122168254,
      "lambda": 1,
      "pairs": 12471,
      "responses": 31856376,
      "gradient_max": 0.0014507471934981364,
      "optimizer_message": "Desired error not necessarily achieved due to precision loss."
    }
  },
  "pairs": 13023,
  "benchmarks": 145,
  "gates": {
    "b0_ci": false,
    "positive_budget_invariant": true,
    "alc_not_worse": false,
    "fold_wins": false,
    "original_runtime_fixture": true
  },
  "accepted": false,
  "full_pool_calibration": {
    "alpha": -0.7406468630658717,
    "beta": 0.5313381570252843,
    "lambda": 1,
    "pairs": 13023,
    "responses": 34275776,
    "gradient_max": 0.0031696317607791125,
    "optimizer_message": "Desired error not necessarily achieved due to precision loss."
  }
}
```

Gate 5, author-specified B0 recipe with fitted full-pool coefficients:

```json
{
  "recipe": "author-specified B0 stress fixture; DESIGN.md fixed before fitting",
  "seed": 0,
  "first_a_name_keys": 300,
  "evidence_subjects": 2000,
  "target_subjects": 2000,
  "labels": 62000,
  "predictions": 2000,
  "zero_own_target_pair_labels": true,
  "full_pool_calibration": {
    "alpha": -0.7406468630658717,
    "beta": 0.5313381570252843,
    "lambda": 1,
    "pairs": 13023,
    "responses": 34275776,
    "gradient_max": 0.0031696317607791125,
    "optimizer_message": "Desired error not necessarily achieved due to precision loss."
  },
  "wall_seconds": 0.2393159579951316,
  "peak_rss_bytes": 80773120,
  "prediction_min": 0.30431793479371044,
  "prediction_max": 0.30646212893419583,
  "shape_and_b0_pass": true,
  "runtime_pass": true,
  "rss_pass": true,
  "prediction_range_pass": true,
  "pass": true,
  "input_sha256": {
    "prior.json": "a6d4d375f713408dc60ef966de92bfe8bd6d0941d70f713c3516b24ad589a443",
    "calibration_full.json": "532bdd0fc317db41d7da75f76c92bc7a775070052b979a0578bdb1b971f47163",
    "model.py": "dcda36b45da82dd6ad4ac2aa4b2d2a139fd29ca5fd3714ac17ff239e55d6d49f",
    "frozen_model.py": "1d84ecb67c8b772a3719078bf2ca067d2bb0802ba36489e45181d4886bd4dcc6",
    "DESIGN.md": "fad14aff19c1797f10120696f042e0d895eeff9903e8f5a520caee044f5b8a1e"
  },
  "evidence_sha256": "35cb2139cc8b92930ed0973ae361ea66674deb66b9dc75c49b5572156891aaa5",
  "test_only_identity_calibration": false
}
```
Deviations: model, fitting, split and gates 1–4 unchanged. Fixture details fixed before outcomes under AUTHOR_RESUME_20261009.md; original byte identity requirement withdrawn by the author. Hidden data, submission and git push were not used. Local numbers are not hidden-test scores.

패키지 설치 한정 네트워크 1회, 저자 승인

Dependency versions and artifact hashes: `offline_dependency.json`.

Historical supplemental validation, superseded for gate 5 and excluded from its evidence: five B0 behavior checks passed. Reconstructed stress: 0.384990 s, 71.73 MiB peak RSS, prediction range [0.3878821133, 0.5397092164]. Test-only identity coefficients; not full-pool fitted values. This does not establish original-fixture identity.

Six outer training priors were recomputed from training-only cached sufficient statistics. Maximum numeric difference from the supplied immutable priors: 3.828604100419852e-12. This diagnostic is not an acceptance gate. Actual C2/C2B0 evaluation uses the supplied priors unchanged, and its positive-budget prediction invariant remains 1e-12.

Actual author-resumed execution: `PYTHONDONTWRITEBYTECODE=1 c2b0/.venv/bin/python c2b0/run.py` (terminal exit 0). Locally cached SciPy is added automatically. Source/input/output checkpoint fingerprints reject stale or modified artifacts. All five gates must pass before packaging.


## Final gate decision and independent verification

| Gate | Decision | Evidence |
|---|---|---|
| 1 B0 improvement CI lower bound > 0 | FAIL | -0.0789823095 |
| 2 B1/3/7/15/31 prediction difference ≤ 1e-12 | PASS | Maximum difference 0 |
| 3 ALC no worse | FAIL | 0.1848401766 → 0.1879808620 |
| 4 At least 5/6 B0 fold wins | FAIL | 3/6 |
| 5 Author recipe, fitted full-pool coefficients | PASS | 0.239316 s; 80,773,120 bytes RSS; predictions [0.3043179348, 0.3064621289] |

C2B0 is rejected by the registered criteria. No ZIP was created and no package checker was invoked, because the all-five-gates prerequisite failed. No post-outcome model, coefficient, weighting, split or gate changes were made.

Independent artifact verification passed over 13,023 pairs and 145 eligible benchmarks: B0 score recomputation maximum error 3.33e-16, 870 nested training exclusions audited, relative ridge-gradient maximum 4.17e-10, bootstrap/fold/ALC/gate decisions independently reproduced, protected input hashes unchanged. See independent_validation.json and independent_validation.log. The optimizer precision-loss messages are retained verbatim; the independently checked stationary gradients satisfy the pre-fixed convergence tolerance.

Operational deviation: attempt 1 exited with local TimeoutError errno 60 while hashing an input after 135 prepared benchmarks. Its log and exception were preserved. Only after confirming terminal exit, the unchanged command was restarted and reused source/input/output-validated checkpoints. The resumed execution completed with exit 0. See run_attempt1_timeout.log and failure_attempt1_timeout.json.

Requested discovery commands and raw outputs are recorded in discovery_outputs.md. The broad find was terminated at the author’s explicit request: ps confirmed PID 17696, kill 17696 succeeded, subsequent ps showed the PID absent (exit 1). The original pipeline ended with empty stdout. This interrupted search is not evidence that PyArrow is absent.
