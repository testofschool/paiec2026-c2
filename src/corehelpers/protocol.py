"""Unchanged fold and budget definitions."""
import hashlib

BUDGETS = (0, 1, 3, 7, 15, 31)

WEIGHTS = (0.1, 0.2, 0.2, 0.2, 0.2, 0.1)

MIN_ITEMS = 80

N_FOLDS = 6


def _h(text):
    return int(hashlib.sha256(text.encode()).hexdigest()[:8], 16)


def fold_of(bench):
    return _h("fold:" + bench) % N_FOLDS
