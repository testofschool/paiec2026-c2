# PAIEC C2

Entry point: `model.predict(input, labeled=None)`. Optional acquisition hook: none (evaluator default random order).

Method: the frozen hierarchical-logistic predictor (`frozen_model.py`, bundled unchanged) plus a cross-pair item offset.
For a target (subject, item) the logit is frozen_mean + delta_item, where delta_item is a MAP estimate from other
subjects' revealed labels on the same item content in the same anonymous benchmark (prior N(0, sigma_delta^2),
sigma_delta^2 = 0.5256 fitted on the public pool). With no other-subject evidence for the item, the prediction equals
the frozen predictor exactly.

Data: public measurement-db pool only (`prior.json`). No pretrained models, no network access, Python standard library only.

Local validation (public pool, leave-benchmark-out, 6 folds, pre-registered acceptance rules):
fresh-split Brier ALC 0.18488 vs 0.20153 for the frozen predictor; 6/6 fold wins; benchmark-cluster
bootstrap 95% CI of the improvement [0.0042, 0.0290]. Runtime: 2,000 predictions with 62,000 revealed labels in under 1 s.
Local numbers are not hidden-test scores.
