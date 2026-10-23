"""Fit prior.json from the public training payload (development machine only).

    python train_prior.py --data ../paiec_baseline/payload/data --out prior.json

The payload comes from paiec_baseline/tools/prepare_data.py --no-embeddings.
Model (on the pair success-rate logit scale):
    z_sb = d_b + lam_b * a_s + r_sb,   r_sb ~ N(0, tau2)
Fitted by weighted alternating least squares on empirical logits, then
normalised so that a has mean 0 and SD 1 across subject configurations.
"""

import argparse
import glob
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import FIELDS  # noqa: E402

MIN_PAIR_N = 5


def _clean(series):
    return series.astype(object).where(series.notna(), "").astype(str).str.strip()


def load_payload(data_dir):
    """Long table: bench, full, name, provider, item_id, trial, y (binary only)."""
    frames = []
    for bench_file in sorted(glob.glob(os.path.join(data_dir, "*", "benchmarks.parquet"))):
        bdir = os.path.dirname(bench_file)
        meta = pd.read_parquet(bench_file).iloc[0]
        if meta.get("response_type") != "binary" or meta.get("granularity") != "item":
            continue
        resp_path = os.path.join(bdir, "response.parquet")
        if not os.path.exists(resp_path):
            resp_path = os.path.join(bdir, "responses.parquet")
        if not os.path.exists(resp_path):
            continue
        resp = pd.read_parquet(resp_path, columns=["subject_id", "item_id", "trial", "response"])
        resp = resp[resp["response"].isin([0.0, 1.0])]
        if resp.empty:
            continue
        subj = pd.read_parquet(os.path.join(bdir, "subjects.parquet"))
        for col in FIELDS + ("provider",):
            subj[col] = _clean(subj[col]) if col in subj else ""
        subj["full"] = subj[list(FIELDS)].agg("|".join, axis=1)
        resp = resp.merge(subj[["subject_id", "full", "normalized_name", "provider"]],
                          on="subject_id", how="inner")
        resp = resp.rename(columns={"normalized_name": "name"})
        resp["bench"] = os.path.basename(bdir)
        resp["y"] = resp["response"].astype(np.int8)
        frames.append(resp[["bench", "full", "name", "provider", "item_id", "trial", "y"]])
    if not frames:
        raise SystemExit(f"no eligible benchmarks under {data_dir}")
    out = pd.concat(frames, ignore_index=True)
    for col in ("bench", "full", "name", "provider", "item_id"):
        out[col] = out[col].astype("category")
    return out


def fit_prior(df, n_iter=200):
    pairs = (df.groupby(["bench", "full"], sort=False, observed=True)
               .agg(k=("y", "sum"), n=("y", "size"), name=("name", "first"),
                    provider=("provider", "first")).reset_index())
    for col in ("bench", "full", "name", "provider"):
        pairs[col] = pairs[col].astype(str)
    pairs = pairs[pairs["n"] >= MIN_PAIR_N].reset_index(drop=True)
    k, n = pairs["k"].to_numpy(float), pairs["n"].to_numpy(float)
    z = np.log((k + 0.5) / (n - k + 0.5))
    v = 1.0 / (k + 0.5) + 1.0 / (n - k + 0.5)
    bi, bench_names = pd.factorize(pairs["bench"])
    si, subj_names = pd.factorize(pairs["full"])
    B, S = len(bench_names), len(subj_names)

    d = np.bincount(bi, z, B) / np.bincount(bi, minlength=B)
    lam = np.ones(B)
    a = np.zeros(S)
    tau2 = 0.5
    ridge_a, ridge_l = 1.0, 4.0
    for it in range(n_iter):
        w = 1.0 / (v + tau2)
        # subjects
        num = np.bincount(si, w * lam[bi] * (z - d[bi]), S)
        den = np.bincount(si, w * lam[bi] ** 2, S) + 1.0 / ridge_a
        a_new = num / den
        # benchmarks: weighted LS of z on [1, a] with ridge on lam toward 1
        x = a_new[si]
        sw = np.bincount(bi, w, B)
        sx = np.bincount(bi, w * x, B)
        sxx = np.bincount(bi, w * x * x, B) + 1.0 / ridge_l
        sy = np.bincount(bi, w * z, B)
        sxy = np.bincount(bi, w * x * z, B) + 1.0 / ridge_l
        det = sw * sxx - sx * sx
        lam_new = (sw * sxy - sx * sy) / det
        d_new = (sy - lam_new * sx) / sw
        # normalise a ~ mean 0, sd 1
        m, sd = a_new.mean(), a_new.std() or 1.0
        a_new = (a_new - m) / sd
        d_new = d_new + lam_new * m
        lam_new = lam_new * sd
        resid = z - d_new[bi] - lam_new[bi] * a_new[si]
        tau2_new = max(0.05, float(np.average(resid ** 2 - v, weights=1.0 / (v + tau2))))
        delta = max(np.abs(a_new - a).max(), np.abs(d_new - d).max(), abs(tau2_new - tau2))
        a, d, lam, tau2 = a_new, d_new, lam_new, tau2_new
        if delta < 1e-6:
            break

    w = 1.0 / (v + tau2)
    a_var = 1.0 / (np.bincount(si, w * lam[bi] ** 2, S) + 1.0)
    full_tab = pd.DataFrame({"full": subj_names, "a": a, "va": a_var})
    first = pairs.drop_duplicates("full").set_index("full")
    full_tab["name"] = first.loc[full_tab["full"], "name"].to_numpy()
    full_tab["provider"] = first.loc[full_tab["full"], "provider"].to_numpy()

    def pooled(groupcol, min_count):
        out = {}
        for key, g in full_tab[full_tab[groupcol] != ""].groupby(groupcol):
            if len(g) < min_count:
                continue
            between = float(g["a"].var(ddof=0)) if len(g) > 1 else 0.0
            out[key] = [float(g["a"].mean()), float(between + g["va"].mean())]
        return out

    a_var_global = float(full_tab["a"].var(ddof=0) + full_tab["va"].mean())
    prior = {
        "version": 1,
        "hyper": {"mu_d": float(d.mean()), "s2_d": float(max(d.var(), 0.05)),
                  "s2_l": float(max(lam.var(), 0.01)), "tau2": float(tau2),
                  "mean_lam": float(lam.mean())},
        "a_full": {r.full: [float(r.a), float(r.va)] for r in full_tab.itertuples()},
        "a_name": pooled("name", 1),
        "a_provider": pooled("provider", 3),
        "a_global": [0.0, a_var_global],
        "stats": {"benchmarks": int(B), "subject_configs": int(S), "pairs": int(len(pairs)),
                  "responses": int(len(df))},
    }
    return prior


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", default="prior.json")
    args = ap.parse_args()
    prior = fit_prior(load_payload(args.data))
    with open(args.out, "w") as handle:
        json.dump(prior, handle, separators=(",", ":"))
    print(json.dumps({"hyper": prior["hyper"], "stats": prior["stats"]}, indent=1))


if __name__ == "__main__":
    main()
