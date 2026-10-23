"""C2 nesting, exclusion, numerical posterior, and cache regression tests.

Run from PAIEC2026: PYTHONDONTWRITEBYTECODE=1 python -m unittest c2d2.test_c2 -v
"""

import copy
import hashlib
import importlib.util
import math
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("c2_under_test", ROOT / "c2/model.py")
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)


def subject(name, harness="one"):
    return {"normalized_name": name, "harness": harness, "provider": "provider"}


def item(content="shared", features="kind", benchmark="bench"):
    return {"item_content": content, "item_features": features, "benchmark_id": benchmark}


def label(subject_meta, item_meta, y):
    return (subject_meta, item_meta), y


class C2Tests(unittest.TestCase):
    def setUp(self):
        self.target, self.other = subject("target"), subject("other")
        self.prior = {
            "a_full": {c2.subject_keys(self.target)[0]: [0.5, 0.2],
                       c2.subject_keys(self.other)[0]: [-0.4, 0.3]},
            "a_name": {"target": [0.2, 0.5]},
            "a_provider": {"provider": [0.1, 0.6]},
            "a_global": [0.0, 0.7],
            "hyper": {"mu_d": -0.1, "s2_d": 0.6, "s2_l": 0.3,
                      "mean_lam": 1.0, "tau2": 0.8}}
        c2.set_prior(self.prior, sigma_delta2=1.5)

    def frozen_prediction(self, s, i, labels):
        groups = c2.frozen.build_groups(self.prior, labels, c2.clean(i["benchmark_id"]))
        fit = c2.frozen.fit_benchmark(self.prior, groups)
        p = c2.frozen.predictive(self.prior, fit, *c2.subject_keys(s))
        return min(max(p, 1e-4), 1 - 1e-4)

    def assert_nested(self, s, i, labels):
        actual, expected = c2.predict((s, i), labels), self.frozen_prediction(s, i, labels)
        self.assertLessEqual(abs(actual - expected), 1e-12)
        self.assertEqual(actual, expected)

    def test_b0_exact_invariant_across_fallbacks(self):
        for s in (self.target, subject("target", "new-harness"),
                  subject("unknown"), {"normalized_name": "global"}):
            for i in (item(), item("new"), item("shared", "different")):
                with self.subTest(subject=s, item=i):
                    self.assert_nested(s, i, [])

    def test_no_other_pair_evidence_exact_with_own_labels(self):
        i = item()
        labels = [label(self.target, i, 1), label(self.target, i, 0),
                  label(self.other, item("unrelated"), 1)]
        self.assert_nested(self.target, i, labels)

    def test_other_benchmark_never_supplies_item_evidence(self):
        labels = [label(self.other, item(benchmark="different"), 1)]
        self.assert_nested(self.target, item(), labels)
        state = c2.build_state(self.prior, labels, "bench")
        self.assertEqual(state["evidence_count"], 0)
        self.assertEqual(state["item_counts"], {})

    def test_exclude_entire_full_target_configuration(self):
        i = item()
        labels = [label(self.target, i, 1)] * 10 + [label(self.other, i, 0)] * 3
        state = c2.build_state(self.prior, labels, "bench")
        target_full, other_full = c2.subject_keys(self.target)[0], c2.subject_keys(self.other)[0]
        expected = c2.fit_item_offset({other_full: (0, 3)}, state["frozen_means"], 1.5)
        actual = c2.posterior_offset(state, i, target_full)
        self.assertEqual(actual, (*expected, True))
        self.assertLess(actual[0], 0)

    def test_same_model_name_different_configuration_is_other_pair(self):
        i, other_config = item(), subject("target", "different-harness")
        state = c2.build_state(self.prior, [label(other_config, i, 1)], "bench")
        delta, variance, present = c2.posterior_offset(state, i, c2.subject_keys(self.target)[0])
        self.assertTrue(present)
        self.assertGreater(delta, 0)
        self.assertGreater(variance, 0)

    def test_content_and_features_both_define_item_key(self):
        labels = [label(self.other, item("a" * 80 + "tail-one", "kind"), 1)]
        for candidate in (item("a" * 80 + "tail-two", "kind"),
                          item("a" * 80 + "tail-one", "other-kind")):
            self.assert_nested(self.target, candidate, labels)
        i = item("  a  ", " kind ")
        self.assertEqual(c2.item_key(i), c2.item_key(item("a", "kind")))
        self.assertEqual(c2.item_key({"item_content": None, "item_features": float("nan")}), ("", ""))

    def test_interactors_are_not_part_of_explicit_spec_key(self):
        left, right = item(), item()
        left["interactors"], right["interactors"] = "one", "two"
        self.assertEqual(c2.item_key(left), c2.item_key(right))

    def test_map_stationarity_and_laplace_variance_fixed_logits(self):
        counts = {"one": (3, 10), "two": (18, 20), "three": (0, 4)}
        means = {"one": -1.2, "two": 0.8, "three": 2.3}
        sigma2, prior_mean = 0.7, -0.2
        delta, var = c2.fit_item_offset(counts, means, sigma2, prior_mean)
        gradient = -(delta - prior_mean) / sigma2
        precision = 1 / sigma2
        for full, (k, n) in counts.items():
            p = c2.frozen._sig(means[full] + delta)
            gradient += k - n * p
            precision += n * p * (1 - p)
        self.assertLess(abs(gradient), 1e-8)
        self.assertAlmostEqual(var, 1 / precision, places=14)
        self.assertGreater(var, 0)
        self.assertLess(var, sigma2)
        self.assertEqual(means, {"one": -1.2, "two": 0.8, "three": 2.3})

    def test_prediction_adds_frozen_and_offset_variance(self):
        i, labels = item(), [label(self.other, item(), 1)] * 4
        state = c2.build_state(self.prior, labels, "bench")
        mean, var = c2.frozen_moments(self.prior, state["fit"], self.target)
        delta, delta_var, present = c2.posterior_offset(state, i, c2.subject_keys(self.target)[0])
        self.assertTrue(present)
        expected = c2.frozen._sig((mean + delta) / math.sqrt(1 + math.pi * (var + delta_var) / 8))
        self.assertEqual(c2.predict_from_state(self.target, i, state), expected)

    def test_no_evidence_bypasses_offset_prior_variance(self):
        state = c2.build_state(self.prior, [], "bench", sigma_delta2=1000)
        self.assertEqual(c2.posterior_offset(state, item(), c2.subject_keys(self.target)[0]), (0, 0, False))
        self.assertEqual(c2.predict_from_state(self.target, item(), state),
                         self.frozen_prediction(self.target, item(), []))

    def test_combined_no_evidence_is_calibrated_d2(self):
        a, b_e = 0.65, 0.3
        state = c2.build_state(self.prior, [], "bench")
        mean, var = c2.frozen_moments(self.prior, state["fit"], self.target)
        expected = c2.frozen._sig((a * mean + b_e) / math.sqrt(1 + math.pi * a * a * var / 8))
        actual = c2.predict_from_state(self.target, item(), state, b_e, a * mean, a * a * var)
        self.assertEqual(actual, expected)
        c2.set_prior(self.prior, 1.5, text_prior=lambda i: b_e, base_scale=a)
        self.assertEqual(c2.predict((self.target, item()), []), expected)

    def test_combined_scales_source_and_target_likelihood_consistently(self):
        a, b_e = 0.65, 0.3
        i, labels = item(), [label(self.other, item(), 1)] * 4
        state = c2.build_state(self.prior, labels, "bench")
        target_full, other_full = c2.subject_keys(self.target)[0], c2.subject_keys(self.other)[0]
        scaled_means = {full: a * z for full, z in state["frozen_means"].items()}
        expected_offset = c2.fit_item_offset({other_full: (4, 4)}, scaled_means, 1.5, b_e)
        actual_offset = c2.posterior_offset(state, i, target_full, b_e, mean_scale=a)
        self.assertEqual(actual_offset, (*expected_offset, True))
        raw_offset = c2.posterior_offset(state, i, target_full, b_e)
        self.assertNotEqual(raw_offset, actual_offset)
        mean, var = c2.frozen_moments(self.prior, state["fit"], self.target)
        expected = c2._probability(a * mean + expected_offset[0], a * a * var + expected_offset[1])
        c2.set_prior(self.prior, 1.5, text_prior=lambda j: b_e, base_scale=a)
        self.assertEqual(c2.predict((self.target, i), labels), expected)
        self.assertEqual(c2.predict_from_state(self.target, i, state, b_e, a * mean, a * a * var,
                                               offset_mean_scale=a), expected)

    def test_targets_absent_from_item_share_cached_posterior(self):
        i = item()
        state = c2.build_state(self.prior, [label(self.other, i, 1)], "bench")
        first = c2.posterior_offset(state, i, c2.subject_keys(self.target)[0])
        second = c2.posterior_offset(state, i, c2.subject_keys(subject("unseen"))[0])
        self.assertEqual(first, second)
        self.assertEqual(len(state["offset_cache"]), 1)

    def test_distinct_sequences_full_fingerprint_unsampled_changes(self):
        i = item()
        labels = [label(self.other, item("unrelated"), 0) for _ in range(200)]
        labels[1] = label(self.other, i, 1)  # outside n//64 sampled positions
        first = c2.predict((self.target, i), labels)
        replacement = copy.deepcopy(labels)
        replacement[1] = label(self.other, item("unrelated", "different"), 1)
        second = c2.predict((self.target, i), replacement)
        self.assertNotEqual(first, second)
        self.assertEqual(second, self.frozen_prediction(self.target, i, replacement))
        self.assertEqual(len(c2._CACHE), 2)

    def test_sampled_inplace_content_features_and_labels_invalidate(self):
        labels = [label(self.other, item(), 1)]
        original = c2.predict((self.target, item()), labels)
        self.assertEqual(c2.predict((self.target, item()), labels), original)
        labels[0][0][1]["item_features"] = "different"
        changed = c2.predict((self.target, item()), labels)
        self.assertNotEqual(changed, original)
        self.assertEqual(changed, self.frozen_prediction(self.target, item(), labels))
        labels[0] = label(self.other, item(), 0)
        self.assertNotEqual(c2.predict((self.target, item()), labels), original)

    def test_set_prior_clears_cache_and_requires_training_variance(self):
        c2.predict((self.target, item()), [])
        self.assertTrue(c2._CACHE)
        c2.set_prior(self.prior, 0)
        self.assertFalse(c2._CACHE)
        with self.assertRaises(ValueError):
            c2.set_prior(self.prior)
        with self.assertRaises(ValueError):
            c2.set_prior(self.prior, float("nan"))
        with self.assertRaises(ValueError):
            c2.set_prior(self.prior, -1)

    def test_frozen_sources_and_prior_unchanged_after_predictions(self):
        paths = [ROOT / "irt_shrink/model.py", ROOT / "irt_shrink/prior.json"]
        before = [hashlib.sha256(path.read_bytes()).hexdigest() for path in paths]
        c2.predict((self.target, item()), [label(self.other, item(), 1)])
        self.assertEqual(before, [hashlib.sha256(path.read_bytes()).hexdigest() for path in paths])


if __name__ == "__main__":
    unittest.main(verbosity=2)
