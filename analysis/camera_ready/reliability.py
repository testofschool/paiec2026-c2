"""Collect response-weighted calibration bins while replaying the split2 predictions."""
import argparse
import gc
import json
from pathlib import Path

import numpy as np
import pandas as pd
from cell_scoring import ROOT, atomic_json, bindings, ev, load_benchmark, records, score

OUTPUT = ROOT / "verification/evidence/camera_ready"
BUDGETS = (0, 15, 31)
METHODS = ("frozen", "C2")


class Calibration:
    def __init__(self):
        self.totals = {(m, b): np.zeros((10, 3)) for m in METHODS for b in BUDGETS}

    def add(self, budget, frozen, c2, successes, counts):
        if budget not in BUDGETS:
            return
        fixed_bin = min(int(frozen * 10), 9)
        self.totals["frozen", budget][fixed_bin] += (
            counts.sum(), frozen * counts.sum(), successes.sum())
        cell_bins = np.minimum((c2 * 10).astype(int), 9)
        total = self.totals["C2", budget]
        for column, weights in enumerate((counts, c2 * counts, successes)):
            total[:, column] += np.bincount(cell_bins, weights=weights, minlength=10)

    def summarize(self, method, budget, expected_count):
        bins = []
        for i, (count, predicted, successes) in enumerate(self.totals[method, budget]):
            bins.append({"lower": i / 10, "upper": (i + 1) / 10, "responses": int(count),
                         "mean_prediction": float(predicted / count) if count else None,
                         "observed_rate": float(successes / count) if count else None})
        total = sum(x["responses"] for x in bins)
        assert total == expected_count
        ece = sum(x["responses"] * abs(x["mean_prediction"] - x["observed_rate"])
                  for x in bins if x["responses"]) / total
        return {"responses": total, "ECE": ece, "bins": bins}


def plot(result):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator

    with plt.rc_context({"pdf.fonttype": 42, "font.family": "DejaVu Sans",
                         "font.size": 9, "axes.spines.top": False, "axes.spines.right": False}):
        fig, axes = plt.subplots(1, 3, figsize=(8.7, 3.2), sharex=True, sharey=True,
                                 layout="constrained")
        for ax, budget in zip(axes, BUDGETS):
            ax.plot([0, 1], [0, 1], color="#828282", linewidth=1, linestyle="--")
            for method, color, marker, label in (("frozen", "#bb5629", "o", "Base"),
                                                  ("C2", "#17698f", "s", "C2")):
                stats = result["reliability"][method][str(budget)]
                filled = [b for b in stats["bins"] if b["responses"]]
                ax.plot([b["mean_prediction"] for b in filled], [b["observed_rate"] for b in filled],
                        marker=marker, color=color, markersize=3, linewidth=1,
                        label=f"{label}  ECE {stats['ECE']:.3f}")
            ax.set(xlim=(0, 1), ylim=(0, 1), aspect="equal", title=f"Budget {budget}",
                   xlabel="Mean predicted probability")
            ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
            ax.legend(loc="upper left", frameon=False, fontsize=7)
        axes[0].set_ylabel("Observed success rate")
        fig.savefig(OUTPUT / "reliability.pdf")
        plt.close(fig)


def run_analysis(run, score_partitions=None):
    calibration = Calibration()
    all_scores = []
    for record in records(run):
        bench = record["bench"]
        args = load_benchmark(run, record)
        frame = score(bench, *args, observe=calibration.add, score_partitions=score_partitions)
        assert len(frame) == record["eligible_pairs"]
        out = run / "camera_ready_m5" / bench
        out.mkdir(parents=True, exist_ok=True)
        frame.to_csv(out / "scores.csv", index=False)
        all_scores.append(frame)
        ev.c2.clear_cache()
        del args
        gc.collect()
        print(bench, len(frame), flush=True)
    scores = pd.concat(all_scores, ignore_index=True)
    assert not scores.duplicated(["bench", "subject_id"]).any()
    expected = json.loads((ROOT / "verification/expected_values.json").read_text())["split2"]
    metrics = {m + "_ALC": float(scores[m + "_alc"].mean()) for m in METHODS}
    diffs = {k: abs(v - expected[k]) for k, v in metrics.items()}
    gate = {"status": "PASS" if max(diffs.values()) <= 1e-9 else "FAIL",
            "expected": {k: expected[k] for k in metrics}, "actual": metrics,
            "absolute_differences": diffs, "tolerance": 1e-9}
    count = int(scores.n_eval.sum())
    result = {"wrapper_gate": gate, "pairs": len(scores), "benchmarks": scores.bench.nunique(),
              "evaluation_responses_per_method_budget": count,
              "bin_rule": "Ten equal-width bins left-closed and right-open, with 1 in the last bin.",
              "weighting": "Calibration weights each recorded evaluation response once; ALC weights each pair once.",
              "reliability": {m: {str(b): calibration.summarize(m, b, count) for b in BUDGETS}
                              for m in METHODS}, **bindings(run)}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    atomic_json(OUTPUT / "reliability.json", result)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--plot-only", action="store_true")
    parser.add_argument("--scores-only", action="store_true", help="Plot separately with --plot-only.")
    parser.add_argument("--with-baselines", action="store_true", help="Score M2/M6 on the same partitions.")
    args = parser.parse_args()
    if args.plot_only:
        plot(json.loads((OUTPUT / "reliability.json").read_text()))
    else:
        callback = None
        if args.with_baselines:
            import baselines
            model = baselines.load_empirical()
            def callback(bench, subjects, parts):
                return baselines.score_partitions(bench, subjects, parts, model)
        result = run_analysis(args.run, callback)
        if not args.scores_only:
            plot(result)
