"""Cross-pair item offsets on the unchanged frozen logistic predictor.

The runtime uses only the standard library. ``set_prior`` must receive the
training-only offset variance, either explicitly or in prior['c2']. Inputs to
``predict`` are frozen within a checkpoint, as in the frozen model: reuse of
the same label sequence is accelerated by a 64-entry sample fingerprint. A
new sequence is always fully fingerprinted. Replace the sequence (or call
``clear_cache``) after an in-place change outside the sample. The sample and
the full fingerprint include complete normalized content and item features.

``build_state`` and ``predict_from_state`` give evaluators an explicit immutable
checkpoint API. Only evidence from another full subject configuration in the
target benchmark is used to estimate the target item's offset. The frozen
pair logits are held fixed throughout that one-dimensional MAP fit.
"""

import hashlib
import json
import math
import os
import types
from collections import OrderedDict


_HERE = os.path.dirname(os.path.abspath(__file__))
_FROZEN_PATH = os.path.join(os.path.dirname(_HERE), "irt_shrink", "model.py")
if not os.path.exists(_FROZEN_PATH):
    # Packaged artifacts contain an unchanged copy beside this entry point.
    _FROZEN_PATH = os.path.join(_HERE, "frozen_model.py")

# Execute source without import loaders, which cannot create frozen bytecode.
frozen = types.ModuleType("paiec_c2_frozen")
frozen.__file__ = _FROZEN_PATH
with open(_FROZEN_PATH, "rb") as _handle:
    exec(compile(_handle.read(), _FROZEN_PATH, "exec"), frozen.__dict__)

FIELDS = frozen.FIELDS
subject_keys = frozen.subject_keys
_PRIOR = None
_SIGMA2 = None
_TEXT_PRIOR = None
_BASE_SCALE = 1.0
_CACHE = OrderedDict()
_QUICK = OrderedDict()
_CACHE_MAX = 8


def clean(value):
    """Same textual normalization as headroom.clean, including missing NaN."""
    if value is None or isinstance(value, float) and math.isnan(value):
        return ""
    return str(value).strip()


def item_key(item):
    """Visible key specified for C2: normalized content plus item features."""
    item = item or {}
    return clean(item.get("item_content")), clean(item.get("item_features"))


def clear_cache():
    _CACHE.clear()
    _QUICK.clear()


def set_prior(prior, sigma_delta2=None, text_prior=None, base_scale=1.0):
    """Install frozen prior and training-only C2/D2 configuration.

    ``text_prior(item)`` returns the calibrated offset prior mean b*e.
    ``base_scale`` is calibration coefficient a; C2 alone keeps it at 1.
    """
    global _PRIOR, _SIGMA2, _TEXT_PRIOR, _BASE_SCALE
    if sigma_delta2 is None:
        sigma_delta2 = prior.get("c2", {}).get("sigma_delta2")
    if sigma_delta2 is None:
        raise ValueError("C2 requires a training-only sigma_delta2")
    sigma_delta2 = float(sigma_delta2)
    if not math.isfinite(sigma_delta2) or sigma_delta2 < 0:
        raise ValueError("sigma_delta2 must be finite and nonnegative")
    base_scale = float(base_scale)
    if not math.isfinite(base_scale):
        raise ValueError("base_scale must be finite")
    _PRIOR, _SIGMA2, _TEXT_PRIOR, _BASE_SCALE = prior, sigma_delta2, text_prior, base_scale
    clear_cache()


def load_prior(path=None):
    if path is not None or _PRIOR is None:
        with open(path or os.path.join(_HERE, "prior.json")) as handle:
            prior = json.load(handle)
        set_prior(prior)
    return _PRIOR


def frozen_moments(prior, fit, subject):
    """Raw frozen mean and Laplace variance, with its exact arithmetic order."""
    full, name, provider = subject_keys(subject)
    d, lam, cov, post = fit
    am, av = frozen.ability(prior, full, name, provider)
    if full in post:
        r, vr = post[full]
    else:
        r, vr = 0.0, prior["hyper"]["tau2"] + lam * lam * av
    mean = d + lam * am + r
    var = cov[0] + 2.0 * am * cov[1] + am * am * cov[2] + vr
    return mean, var


def _probability(mean, var):
    p = frozen._sig(mean / math.sqrt(1.0 + math.pi * max(var, 0.0) / 8.0))
    return float(min(max(p, 1e-4), 1.0 - 1e-4))


def fit_item_offset(counts, frozen_means, sigma_delta2, prior_mean=0.0, mean_scale=1.0):
    """MAP and Laplace variance from {full: (k,n)} with fixed pair logits.

    The strictly concave log posterior has a unique optimum for positive
    sigma_delta2. Damped Newton steps avoid saturation-induced overshoot.
    """
    sigma_delta2, prior_mean = float(sigma_delta2), float(prior_mean)
    if sigma_delta2 <= 0:
        return prior_mean, 0.0
    precision = 1.0 / sigma_delta2
    rows = [(float(k), int(n), mean_scale * frozen_means[full])
            for full, (k, n) in counts.items() if n]
    delta = prior_mean
    for _ in range(80):
        gradient = -(delta - prior_mean) * precision
        hessian = precision
        for k, n, mean in rows:
            p = frozen._sig(mean + delta)
            gradient += k - n * p
            hessian += n * p * (1.0 - p)
        step = max(-1.0, min(1.0, gradient / hessian))
        delta += step
        if abs(step) < 1e-10:
            break
    hessian = precision
    for k, n, mean in rows:
        p = frozen._sig(mean + delta)
        hessian += n * p * (1.0 - p)
    return delta, 1.0 / hessian


def _record(subject, item, label):
    full, name, provider = subject_keys(subject)
    return (full, name, provider, frozen._s((item or {}).get("benchmark_id")),
            item_key(item), 1 if label == 1 else 0)


def _sample_key(labeled, benchmark):
    n = len(labeled) if labeled is not None else 0
    if not n:
        return benchmark, 0, ()
    step = max(1, n // 64)
    indices = list(range(0, n, step))
    if indices[-1] != n - 1:
        indices.append(n - 1)
    return benchmark, n, tuple(_record(*labeled[i][0], labeled[i][1]) for i in indices)


def build_state(prior, labeled, benchmark, sigma_delta2=None):
    """Build one checkpoint with a full semantic evidence fingerprint.

    No labels from evaluation inputs are read here. A benchmark's frozen fit
    sees its revealed labels; item bins preserve full subject keys for the
    later leave-target-pair-out calculation.
    """
    if sigma_delta2 is None:
        sigma_delta2 = _SIGMA2
    if sigma_delta2 is None:
        sigma_delta2 = prior.get("c2", {}).get("sigma_delta2")
    if sigma_delta2 is None:
        raise ValueError("C2 requires a training-only sigma_delta2")
    sigma_delta2 = float(sigma_delta2)
    if not math.isfinite(sigma_delta2) or sigma_delta2 < 0:
        raise ValueError("sigma_delta2 must be finite and nonnegative")
    benchmark = frozen._s(benchmark)
    stats, meta, item_counts = {}, {}, {}
    digest = hashlib.sha256()
    for entry in labeled or ():
        (subject, item), label = entry
        full, name, provider, bench, key, y = _record(subject, item, label)
        if benchmark and bench != benchmark:
            continue
        encoded = json.dumps((full, name, provider, bench, key, y),
                             ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
        k, n = stats.get(full, (0, 0))
        stats[full] = k + y, n + 1
        meta[full] = name, provider
        by_pair = item_counts.setdefault(key, {})
        k, n = by_pair.get(full, (0, 0))
        by_pair[full] = k + y, n + 1
    groups = {full: (k, n, *frozen.ability(prior, full, *meta[full]))
              for full, (k, n) in stats.items()}
    fit = frozen.fit_benchmark(prior, groups)
    means = {}
    for full, (name, provider) in meta.items():
        am, av = frozen.ability(prior, full, name, provider)
        means[full] = fit[0] + fit[1] * am + fit[3][full][0]
    return {"prior": prior, "benchmark": benchmark, "fit": fit,
            "frozen_means": means, "item_counts": item_counts,
            "sigma_delta2": float(sigma_delta2), "offset_cache": {},
            "fingerprint": (benchmark, digest.hexdigest()),
            "evidence_count": sum(n for k, n in stats.values())}


def posterior_offset(state, item, target_full, prior_mean=0.0, mean_scale=1.0):
    """Return (offset, variance, has_other_pair_evidence).

    No evidence is a structural fallback, so its additional variance is zero
    even when sigma_delta2 is positive. For C2 this preserves frozen exactly.
    With a text prior it preserves the calibrated D2 no-evidence prediction.
    """
    key = item_key(item)
    prior_mean, mean_scale = float(prior_mean), float(mean_scale)
    if not math.isfinite(prior_mean) or not math.isfinite(mean_scale):
        raise ValueError("offset prior mean and source scale must be finite")
    by_pair = state["item_counts"].get(key, {})
    # All target pairs absent from this item have identical offset evidence.
    # Share their posterior rather than refitting once per evaluation subject.
    excluded = target_full if target_full in by_pair else None
    cache_key = key, excluded, prior_mean, mean_scale
    cached = state["offset_cache"].get(cache_key)
    if cached is not None:
        return cached
    counts = {full: count for full, count in by_pair.items()
              if full != target_full}
    if not counts:
        result = prior_mean, 0.0, False
    else:
        delta, var = fit_item_offset(counts, state["frozen_means"],
                                     state["sigma_delta2"], prior_mean, mean_scale)
        result = delta, var, True
    state["offset_cache"][cache_key] = result
    return result


def predict_from_state(subject, item, state, prior_mean=0.0, base_mean=None, base_var=None,
                       offset_mean_scale=1.0):
    """Predict C2 or calibrated C2+D2 from a prepared immutable checkpoint."""
    full, name, provider = subject_keys(subject)
    delta, delta_var, has_evidence = posterior_offset(state, item, full, prior_mean,
                                                     offset_mean_scale)
    if base_mean is None and base_var is None and not has_evidence and prior_mean == 0:
        p = frozen.predictive(state["prior"], state["fit"], full, name, provider)
        return float(min(max(p, 1e-4), 1.0 - 1e-4))
    mean, var = frozen_moments(state["prior"], state["fit"], subject)
    return _probability((mean if base_mean is None else base_mean) + delta,
                        (var if base_var is None else base_var) + delta_var)


def _checkpoint(prior, labeled, benchmark):
    quick = _sample_key(labeled, benchmark)
    identity = id(labeled), benchmark
    cached = _QUICK.get(identity)
    if cached is not None and cached[0] is labeled and cached[1] == quick:
        _QUICK.move_to_end(identity)
        return cached[2]
    state = build_state(prior, labeled, benchmark)
    fingerprint = state["fingerprint"]
    existing = _CACHE.get(fingerprint)
    if existing is not None:
        state = existing
    _CACHE[fingerprint] = state
    _CACHE.move_to_end(fingerprint)
    while len(_CACHE) > _CACHE_MAX:
        _CACHE.popitem(last=False)
    _QUICK[identity] = labeled, quick, state
    _QUICK.move_to_end(identity)
    while len(_QUICK) > _CACHE_MAX:
        _QUICK.popitem(last=False)
    return state


def predict(input, labeled=None):
    subject, item = input
    prior = load_prior()
    benchmark = frozen._s((item or {}).get("benchmark_id"))
    state = _checkpoint(prior, labeled, benchmark)
    prior_mean = 0.0 if _TEXT_PRIOR is None else float(_TEXT_PRIOR(item))
    if _BASE_SCALE == 1.0:
        return predict_from_state(subject, item, state, prior_mean)
    mean, var = frozen_moments(prior, state["fit"], subject)
    return predict_from_state(subject, item, state, prior_mean,
                              _BASE_SCALE * mean, _BASE_SCALE ** 2 * var, _BASE_SCALE)
