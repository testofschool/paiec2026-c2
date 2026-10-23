"""Copied public-data preparation and numerical fitting functions."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import os
import time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit, logit
from irt_shrink import model
from corehelpers import protocol as lobo_eval

HERE = Path(__file__).resolve().parents[1]
DATA = HERE
BUDGETS = lobo_eval.BUDGETS

WEIGHTS = lobo_eval.WEIGHTS

SUBJECT_FIELDS = ("normalized_name", "provider", "release_date", "access_date",
                  "harness", "harness_version", "reasoning_effort", "subject_features_extra")

ITEM_FIELDS = ("item_content", "item_features", "interactors")


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 ** 2), b""):
            h.update(block)
    return h.hexdigest()


def clean(value):
    return "" if value is None or (isinstance(value, float) and np.isnan(value)) else str(value).strip()


def read_bench(bench):
    d = DATA / bench
    subjects = pd.read_parquet(d / "subjects.parquet")
    for c in SUBJECT_FIELDS:
        subjects[c] = subjects[c].map(clean) if c in subjects else ""
    subjects["subject_id"] = subjects["subject_id"].astype(str)
    subjects["full"] = subjects[list(model.FIELDS)].agg("|".join, axis=1)
    subjects["visible"] = subjects[list(SUBJECT_FIELDS)].apply(
        lambda r: json.dumps(list(r), ensure_ascii=False, separators=(",", ":")), axis=1)
    subjects = subjects.set_index("subject_id")
    path = d / "response.parquet"
    if not path.exists():
        path = d / "responses.parquet"
    r = pd.read_parquet(path, columns=["subject_id", "item_id", "trial", "response"])
    r = r[r.response.isin([0., 1.])].copy()
    r["subject_id"] = r.subject_id.astype(str)
    r["item_id"] = r.item_id.astype(str)
    r = r[r.subject_id.isin(subjects.index)]
    # Stable earliest-recorded-trial convention, disclosed in the report.
    r = r.sort_values(["subject_id", "item_id", "trial"], kind="mergesort")
    cells = r.groupby(["subject_id", "item_id"], sort=True, observed=True).agg(
        k=("response", "sum"), n=("response", "size"), first=("response", "first")).reset_index()
    return subjects, cells


def fit_prior_stats(pairs, response_count, n_iter=200):
    """Same sufficient-statistic equations as frozen train_prior.fit_prior."""
    pairs = pairs[pairs.n >= 5].reset_index(drop=True)
    k, n = pairs.k.to_numpy(float), pairs.n.to_numpy(float)
    z = np.log((k + .5) / (n - k + .5))
    v = 1 / (k + .5) + 1 / (n - k + .5)
    bi, benches = pd.factorize(pairs.bench)
    si, names = pd.factorize(pairs.full)
    B, S = len(benches), len(names)
    d = np.bincount(bi, z, B) / np.bincount(bi, minlength=B)
    lam, a, tau2 = np.ones(B), np.zeros(S), .5
    for _ in range(n_iter):
        w = 1 / (v + tau2)
        an = np.bincount(si, w * lam[bi] * (z - d[bi]), S) / (
            np.bincount(si, w * lam[bi] ** 2, S) + 1)
        x = an[si]
        sw, sx = np.bincount(bi, w, B), np.bincount(bi, w * x, B)
        sxx = np.bincount(bi, w * x * x, B) + .25
        sy, sxy = np.bincount(bi, w * z, B), np.bincount(bi, w * x * z, B) + .25
        ln = (sw * sxy - sx * sy) / (sw * sxx - sx * sx)
        dn = (sy - ln * sx) / sw
        m, sd = an.mean(), an.std() or 1.
        an = (an - m) / sd
        dn, ln = dn + ln * m, ln * sd
        residual = z - dn[bi] - ln[bi] * an[si]
        tn = max(.05, float(np.average(residual ** 2 - v, weights=1 / (v + tau2))))
        delta = max(abs(an - a).max(), abs(dn - d).max(), abs(tn - tau2))
        a, d, lam, tau2 = an, dn, ln, tn
        if delta < 1e-6:
            break
    w = 1 / (v + tau2)
    va = 1 / (np.bincount(si, w * lam[bi] ** 2, S) + 1)
    tab = pd.DataFrame({"full": names, "a": a, "va": va})
    first = pairs.drop_duplicates("full").set_index("full")
    for field in ("name", "provider"):
        tab[field] = first.loc[tab.full, field].to_numpy()
    def pooled(field, minimum):
        return {key: [float(g.a.mean()), float(g.a.var(ddof=0) + g.va.mean())]
                for key, g in tab[tab[field] != ""].groupby(field) if len(g) >= minimum}
    return {"version": 1, "hyper": {"mu_d": float(d.mean()), "s2_d": float(max(d.var(), .05)),
        "s2_l": float(max(lam.var(), .01)), "tau2": float(tau2), "mean_lam": float(lam.mean())},
        "a_full": {r.full: [float(r.a), float(r.va)] for r in tab.itertuples()},
        "a_name": pooled("name", 1), "a_provider": pooled("provider", 3),
        "a_global": [0., float(tab.a.var(ddof=0) + tab.va.mean())],
        "stats": {"benchmarks": B, "subject_configs": S, "pairs": len(pairs), "responses": int(response_count)}}


def prepare():
    start = time.perf_counter()
    (HERE / "targets").mkdir(exist_ok=True)
    records, inventory = [], []
    for i, path in enumerate(sorted(DATA.glob("*/benchmarks.parquet"))):
        bench = path.parent.name
        meta = pd.read_parquet(path).iloc[0]
        if meta.get("response_type") != "binary" or meta.get("granularity") != "item":
            continue
        subjects, cells = read_bench(bench)
        c = cells.copy()
        c["full"] = c.subject_id.map(subjects.full)
        pairs = c.groupby("full", sort=False).agg(k=("k", "sum"), n=("n", "sum")).reset_index()
        lookup = subjects.drop_duplicates("full").set_index("full")
        pairs["name"] = pairs.full.map(lookup.normalized_name)
        pairs["provider"] = pairs.full.map(lookup.provider)
        pairs["bench"], pairs["fold"] = bench, lobo_eval.fold_of(bench)
        records.append(pairs)
        cells["rate"] = cells.k / cells.n
        targets = cells.groupby("item_id", sort=True).agg(rate=("rate", "mean"), subjects=("subject_id", "size")).reset_index()
        targets["easiness"] = logit(np.clip(targets.rate, 1e-4, 1 - 1e-4))
        targets.to_parquet(HERE / "targets" / f"{bench}.parquet", index=False)
        counts = cells.groupby("subject_id").size()
        inventory.append({"bench": bench, "fold": lobo_eval.fold_of(bench), "responses": int(cells.n.sum()),
            "cells": len(cells), "items": len(targets), "eligible_pairs": int((counts >= 80).sum())})
        if i % 10 == 0:
            print(f"prepare {i}: {bench} cells={len(cells)} items={len(targets)}", flush=True)
    pairs = pd.concat(records, ignore_index=True)
    pairs.to_csv(HERE / "pair_stats.csv", index=False)
    for fold in range(6):
        p = pairs[pairs.fold != fold]
        prior = fit_prior_stats(p, p.n.sum())
        (HERE / f"fold_prior_{fold}.json").write_text(json.dumps(prior, separators=(",", ":")))
    out = {"benchmarks": inventory, "pairs": int(sum(r["eligible_pairs"] for r in inventory)),
           "wall_seconds": time.perf_counter() - start}
    (HERE / "prepared.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({"pairs": out["pairs"], "items": sum(x["items"] for x in inventory), "wall": out["wall_seconds"]}), flush=True)


def fit_irt(si, ii, k, n, theta_mean, theta_var, I, two=False, dmean=0., dvar=1.):
    """Deterministic MAP 1PL / regularized 2PL (oracle uses full outcomes)."""
    S = len(theta_mean)
    initial = np.r_[theta_mean, np.zeros(I), dmean, np.zeros(I) if two else []]
    def objective(x):
        theta, offset, d = x[:S], x[S:S+I], x[S+I]
        a = np.exp(x[S+I+1:]) if two else np.ones(I)
        z = d + a[ii] * theta[si] + offset[ii]
        residual = n * expit(z) - k
        value = np.sum(n * np.logaddexp(0, z) - k * z)
        value += .5 * np.sum((theta - theta_mean) ** 2 / theta_var) + .5 * np.sum(offset ** 2)
        value += .5 * (d - dmean) ** 2 / dvar
        gt = np.bincount(si, residual * a[ii], minlength=S) + (theta - theta_mean) / theta_var
        ge = np.bincount(ii, residual, minlength=I) + offset
        gd = residual.sum() + (d - dmean) / dvar
        grad = np.r_[gt, ge, gd]
        if two:
            la = x[S+I+1:]
            value += .5 * np.sum(la ** 2)
            ga = np.bincount(ii, residual * a[ii] * theta[si], minlength=I) + la
            grad = np.r_[grad, ga]
        return float(value), grad
    bounds = [(None, None)] * (S + I + 1) + ([(np.log(.1), np.log(5.))] * I if two else [])
    result = minimize(objective, initial, jac=True, method="L-BFGS-B", bounds=bounds,
                      options={"maxiter": 500, "ftol": 1e-9, "gtol": 1e-5, "maxcor": 10})
    x = result.x
    a = np.exp(x[S+I+1:]) if two else np.ones(I)
    return x[:S], x[S:S+I] + x[S+I], a, {
        "success": bool(result.success), "message": str(result.message), "iterations": result.nit,
        "objective": float(result.fun), "gradient_max": float(abs(result.jac).max()), "intercept": float(x[S+I])}


def brier(p, k, n):
    return float(np.sum(n * p * p - 2 * k * p + k) / n.sum())


def item_table(bench):
    t = pd.read_parquet(DATA / bench / "items.parquet")
    if "item_content" not in t and "content" in t:
        t = t.rename(columns={"content": "item_content"})
    t["item_id"] = t.item_id.astype(str)
    if t.item_id.duplicated().any():
        raise ValueError(f"duplicate item IDs in {bench}")
    for c in ITEM_FIELDS:
        t[c] = t[c].map(clean) if c in t else ""
    t["visible"] = t[list(ITEM_FIELDS)].apply(
        lambda row: hashlib.sha256(json.dumps(list(row), ensure_ascii=False, separators=(",", ":")).encode()).hexdigest(), axis=1)
    return t.set_index("item_id")


def atomic_text(path, value):
    """Publish a complete artifact before any completion marker is visible."""
    path = Path(path)
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    temporary.write_text(value)
    temporary.replace(path)
