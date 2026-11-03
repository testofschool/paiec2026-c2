# PAIEC C2-sigma14

Entry point: `model.predict(input, labeled=None)`. Optional acquisition hook: none (evaluator default random order).

Method: the frozen hierarchical-logistic predictor (`frozen_model.py`, bundled unchanged) plus a cross-pair item offset.
For a target (subject, item) the logit is frozen_mean + delta_item, where delta_item is a MAP estimate from other
subjects' revealed labels on the same item content in the same anonymous benchmark (prior N(0, sigma_delta^2),
sigma_delta^2 = 7.3585 = 14 x 0.5256 fitted on the public pool; the factor 14 was selected on split2 and confirmed
on split3 under rules fixed before evaluation). With no other-subject evidence for the item, the prediction equals
the frozen predictor exactly.

Data: public measurement-db pool only (`prior.json`). No pretrained models, no network access, Python standard library only.

Local validation (public pool, leave-benchmark-out, 6 folds): fresh-split (split3) Brier ALC 0.17971 vs 0.18486 for
unscaled C2; one-sided 99% benchmark-cluster bootstrap lower bound of the improvement 0.0023; 5/6 fold wins.
With at most two subjects per benchmark the improvement is 0.00006 and not distinguishable from zero.
Local numbers are not hidden-test scores.
