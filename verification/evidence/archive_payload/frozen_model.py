"""Hierarchical logistic shrinkage predictor for PAIEC (stdlib only).

For a target (subject, item) the Brier-optimal prediction without item-level
evidence is the posterior mean of the pair success rate pi_sb. We model

    logit(pi_sb) = d_b + lam_b * a_s + r_sb

a_s    subject ability, estimated offline on the public training pool
       (prior.json); unseen subjects fall back to name -> provider -> global.
d_b    unknown benchmark offset,  prior N(mu_d, s2_d) learned from training.
lam_b  unknown benchmark slope,   prior N(mean_lam, s2_l) learned from training.
r_sb   pair deviation,            prior N(0, tau2) learned from training.

At each call the supplied labels for the target's benchmark_id (all subjects
present) update (d_b, lam_b, r_sb) by MAP with a Laplace variance; the
prediction is the probit-approximated posterior mean of sigmoid(z).
Fits are cached per evidence fingerprint, so repeated calls are cheap.
v2 (2026-10-08): damped inner Newton step for r_sb (|step| <= 1, 30 iters).
"""

import json
import math
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
PRIOR_FILE = "prior.json"
FIELDS = ("normalized_name", "harness", "reasoning_effort", "harness_version",
          "subject_features_extra")

_PRIOR = None
_CACHE = {}
_CACHE_MAX = 256


def _s(value):
    return "" if value is None else str(value).strip()


def subject_keys(subject):
    """(full configuration key, model name, provider)."""
    subject = subject or {}
    full = "|".join(_s(subject.get(f)) for f in FIELDS)
    return full, _s(subject.get("normalized_name")), _s(subject.get("provider"))


def load_prior(path=None):
    global _PRIOR
    if path is not None:
        with open(path) as handle:
            _PRIOR = json.load(handle)
    elif _PRIOR is None:
        with open(os.path.join(_HERE, PRIOR_FILE)) as handle:
            _PRIOR = json.load(handle)
    return _PRIOR


def set_prior(prior):
    """Install an in-memory prior (used by cross-validation)."""
    global _PRIOR
    _PRIOR = prior
    _CACHE.clear()
    _QUICK.clear()


def ability(prior, full, name, provider):
    """Prior mean and variance of a_s via the fallback hierarchy."""
    if name and full in prior["a_full"]:
        return prior["a_full"][full]
    if name and name in prior["a_name"]:
        return prior["a_name"][name]
    if provider and provider in prior["a_provider"]:
        return prior["a_provider"][provider]
    return prior["a_global"]


def _sig(z):
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def fit_benchmark(prior, groups, iters=40):
    """MAP of (d, lam, r_s) given groups {key: (k, n, a_mean, a_var)}.

    Returns d, lam, the 2x2 covariance of (d, lam), and {key: (r, var_r)}.
    """
    h = prior["hyper"]
    mu_d, s2_d, s2_l, tau2 = h["mu_d"], h["s2_d"], h["s2_l"], h["tau2"]
    mu_l = h.get("mean_lam", 1.0)
    d, lam = mu_d, mu_l
    r = {key: 0.0 for key in groups}
    cov = (s2_d, 0.0, s2_l)
    for _ in range(iters):
        # 1) pair deviations given (d, lam)
        for key, (k, n, am, av) in groups.items():
            t2 = tau2 + lam * lam * av
            rk = r[key]
            for _ in range(30):
                p = _sig(d + lam * am + rk)
                g = k - n * p - rk / t2
                hh = n * p * (1.0 - p) + 1.0 / t2
                # Damped Newton: an undamped step overshoots once p saturates
                # (hh -> 1/t2) and then oscillates; v1 produced |r| ~ 40 for
                # name-fallback subjects with many labels.
                step = max(-1.0, min(1.0, g / hh))
                rk += step
                if abs(step) < 1e-8:
                    break
            r[key] = rk
        # 2) benchmark (d, lam) given r: one damped 2-D Newton step
        gd = -(d - mu_d) / s2_d
        gl = -(lam - mu_l) / s2_l
        hdd, hdl, hll = 1.0 / s2_d, 0.0, 1.0 / s2_l
        for key, (k, n, am, av) in groups.items():
            p = _sig(d + lam * am + r[key])
            res, w = k - n * p, n * p * (1.0 - p)
            gd += res
            gl += res * am
            hdd += w
            hdl += w * am
            hll += w * am * am
        det = hdd * hll - hdl * hdl
        if det <= 0:
            break
        dd = (hll * gd - hdl * gl) / det
        dl = (hdd * gl - hdl * gd) / det
        scale = min(1.0, 2.0 / max(abs(dd), abs(dl), 1e-12))
        d += scale * dd
        lam += scale * dl
        cov = (hll / det, -hdl / det, hdd / det)
        if max(abs(dd), abs(dl)) < 1e-7:
            break
    post = {}
    for key, (k, n, am, av) in groups.items():
        t2 = tau2 + lam * lam * av
        p = _sig(d + lam * am + r[key])
        post[key] = (r[key], 1.0 / (n * p * (1.0 - p) + 1.0 / t2))
    return d, lam, cov, post


def predictive(prior, fit, full, name, provider):
    d, lam, cov, post = fit
    am, av = ability(prior, full, name, provider)
    if full in post:
        r, vr = post[full]
    else:
        r, vr = 0.0, prior["hyper"]["tau2"] + lam * lam * av
    mean = d + lam * am + r
    var = cov[0] + 2.0 * am * cov[1] + am * am * cov[2] + vr
    return _sig(mean / math.sqrt(1.0 + math.pi * max(var, 0.0) / 8.0))


def build_groups(prior, labeled, benchmark):
    groups = {}
    meta = {}
    for entry in labeled or ():
        (subject, item), label = entry
        if benchmark and _s((item or {}).get("benchmark_id")) != benchmark:
            continue
        full, name, provider = subject_keys(subject)
        k, n = groups.get(full, (0, 0))
        groups[full] = (k + (1 if label == 1 else 0), n + 1)
        meta[full] = (name, provider)
    out = {}
    for full, (k, n) in groups.items():
        am, av = ability(prior, full, *meta[full])
        out[full] = (k, n, am, av)
    return out


def _quick_key(labeled, benchmark):
    """O(1)-ish fingerprint: evidence is frozen within a checkpoint and nested
    across budgets, so length plus an evenly spaced sample identifies it."""
    n = len(labeled) if labeled else 0
    if n == 0:
        return (benchmark, 0)
    step = max(1, n // 64)
    sample = []
    for i in list(range(0, n, step)) + [n - 1]:
        (subject, item), label = labeled[i]
        sample.append((subject_keys(subject)[0], _s((item or {}).get("benchmark_id")),
                       _s((item or {}).get("item_content"))[:64], label))
    return (benchmark, n, hash(tuple(sample)))


_QUICK = {}


def predict(input, labeled=None):
    subject, item = input
    prior = load_prior()
    benchmark = _s((item or {}).get("benchmark_id"))
    quick = _quick_key(labeled, benchmark)
    fit = _QUICK.get(quick)
    if fit is None:
        groups = build_groups(prior, labeled, benchmark)
        fingerprint = (benchmark, tuple(sorted((key, v[0], v[1]) for key, v in groups.items())))
        fit = _CACHE.get(fingerprint)
        if fit is None:
            fit = fit_benchmark(prior, groups)
            if len(_CACHE) >= _CACHE_MAX:
                _CACHE.clear()
            _CACHE[fingerprint] = fit
        if len(_QUICK) >= _CACHE_MAX:
            _QUICK.clear()
        _QUICK[quick] = fit
    full, name, provider = subject_keys(subject)
    p = predictive(prior, fit, full, name, provider)
    return float(min(max(p, 1e-4), 1.0 - 1e-4))
