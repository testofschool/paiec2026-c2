# Fresh-copy reproduction receipts (2026-10-22)

| Machine | Key | Expected | Observed | Absolute difference | Verdict (1e-6) |
|---|---|---:|---:|---:|---|
| Apple M5 Max | split2.C2_ALC | 0.18487910654403214 | 0.18489647409719684 | 1.7367553164698846e-05 | FAIL |
| Apple M5 Max | split2.frozen_ALC | 0.2015333932758017 | 0.20153339327580172 | 2.7755575615628914e-17 | PASS |
| Apple M5 Max | split2.C2_B0 | 0.24893649649887992 | 0.24893649649887994 | 2.7755575615628914e-17 | PASS |
| Apple M5 Max | split3.C2_ALC | 0.1848401766 | 0.1848574271066814 | 1.725050668141548e-05 | FAIL |
| Apple M5 Max | split3.C2_B0 | 0.2488973551 | 0.24889735512042893 | 2.042893632037135e-11 | PASS |
| Apple M5 Max | split3.C2_B31 | 0.1468372469 | 0.14686523602787088 | 2.7989127870886588e-05 | FAIL |
| Apple M1 Max | split2.C2_ALC | 0.18487910654403214 | not run (SSH host key verification failed) | — | not run |
| Apple M1 Max | split2.frozen_ALC | 0.2015333932758017 | not run (SSH host key verification failed) | — | not run |
| Apple M1 Max | split2.C2_B0 | 0.24893649649887992 | not run (SSH host key verification failed) | — | not run |
| Apple M1 Max | split3.C2_ALC | 0.1848401766 | not run (SSH host key verification failed) | — | not run |
| Apple M1 Max | split3.C2_B0 | 0.2488973551 | not run (SSH host key verification failed) | — | not run |
| Apple M1 Max | split3.C2_B31 | 0.1468372469 | not run (SSH host key verification failed) | — | not run |

| Machine | ZIP exact SHA | Official checker | model.py exact | frozen_model.py exact | Stage wall sum (s) | Peak RSS (bytes) | pip freeze |
|---|---|---|---|---|---:|---:|---|
| Apple M5 Max | True (`70ff16e31d76195fc07c487a446c0a17f3f2fd63f234d81035f05e9f7e6ae31d`) | exit 0 | True | True | 605.385213 (v10.3 + continuation; continuation 128.859786) | 12758138880 | numpy==2.2.6<br>pandas==2.3.3<br>pyarrow==24.0.0<br>python-dateutil==2.9.0.post0<br>pytz==2025.2<br>scipy==1.15.3<br>six==1.17.0<br>tzdata==2025.2 |
| Apple M1 Max | not run (SSH host key verification failed) | not run | not run | not run | not run | not run | not run |

Registered expected values were produced on an Apple M1 Max (2026-10-10). On 2026-10-22 a fresh copy on Apple M5 Max reproduced frozen ALC and C2 B0 to an absolute difference of 2.7755575615628914e-17 and C2 split2 ALC within 1.7367553164698846e-05 (tolerance 1e-6: FAIL); on the M1 Max the rerun was not run because SSH returned `Host key verification failed.` The reported four-decimal figures are unchanged in the existing report files; the fresh split3 C2 ALC and C2 B31 round to 0.1849 and 0.1469, respectively. The refitted and original prior JSON bytes differ; the largest absolute difference among common numeric keys is 0.002074751416940246 at `/c2/sigma_delta2`.

| Machine | Stage | Exit | Wall seconds | Peak RSS bytes |
|---|---|---:|---:|---:|
| Apple M5 Max | a1_01_venv | 0 | 2.016411 | 117587968 |
| Apple M5 Max | a1_02_pip_install | 0 | 9.070824 | 194887680 |
| Apple M5 Max | a1_03_prepare | 0 | 6.039703 | 58589184 |
| Apple M5 Max | a1_04_identifier | 0 | 12.107733 | 153600000 |
| Apple M5 Max | a1_05_train | 0 | 315.489041 | 8154005504 |
| Apple M5 Max | a1_06_split2 | 0 | 130.787591 | 12758138880 |
| Apple M5 Max | a1_07_compare_split2 | 1 | 1.014125 | 17842176 |
| Apple M5 Max | split3 | 0 | 127.688765 | 12338987008 |
| Apple M5 Max | compare_split3 | 1 | 0.039317 | 17776640 |
| Apple M5 Max | build_zip | 0 | 0.513138 | 28147712 |
| Apple M5 Max | official_checker | 0 | 0.591686 | 64749568 |
| Apple M5 Max | compare_final | 1 | 0.026880 | 18169856 |

The M5 continuation reused the v10.3 training and split2 outputs, without retraining. Compare failures did not stop the remaining stages. Registered package sources, expected values, requirements and comparison code were unchanged. No push was performed.

Prior byte comparison:

- `$PAIEC_PUBLIC_DATA_DIR`: 4727204 bytes, SHA256 `d145c1f738c2c3937db9eeef6ec2268cb67376e6444fb7b24ff2c2a1240438c5`.
- `$PAIEC_PUBLIC_DATA_DIR`: 4356734 bytes, SHA256 `ebea4e925fa97a84d47ececce94b2c9bfc769020711500dfa83e0fbf1d1b1ff9`.

Receipt files: `p2probe/v10_4/M5_FULL.json`, `STUDIO_FULL.json`, `PRIOR_DIFF.json`; per-stage KST ISO start/end timestamps, unique logs and package member hashes are recorded in M5_FULL.json.
