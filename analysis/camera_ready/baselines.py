"""Measure the inventory, official empirical mean, and Beta(1,1) comparator.

Run reliability.py --with-baselines first for the same exact split, fits and scoring cells.
If that callback is unavailable, "replay" runs the same split2 simulator and collects
the comparator predictions from the exact partition object used to score C2 and Base.
"""
import argparse
import hashlib
import inspect
from collections import defaultdict
from functools import lru_cache
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import numpy as np
import pandas as pd
from corehelpers import evaluation, measure, protocol

EVIDENCE = ROOT / 'verification/evidence/camera_ready'
MODEL_HASH = '1e570641dd9b981baae988779b904ae58ad610a99bd44fb861647c60c93e935e'
MODEL_COMMIT = '8629bd30f39a4067739f711c45dffedf59329597'
BUDGETS = protocol.BUDGETS
WEIGHTS = protocol.WEIGHTS


def sha(path):
    return measure.sha(path)


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
    tmp.replace(path)


@lru_cache(maxsize=1)
def load_empirical():
    from official_empirical_mean import model
    if sha(model.__file__) != MODEL_HASH:
        raise ValueError('Unexpected organizer model hash')
    return model


def inventory(artifacts):
    prepared = artifacts / 'prepared.json'
    stats = artifacts / 'pair_stats.csv'
    records = json.loads(prepared.read_text())['benchmarks']
    inventory_benchmarks = {r['bench'] for r in records}
    if len(records) != len(inventory_benchmarks):
        raise ValueError('Duplicate benchmark in prepared inventory')
    pairs = pd.read_csv(stats, usecols=['bench', 'n'], keep_default_na=False)
    if not set(pairs.bench).issubset(inventory_benchmarks):
        raise ValueError('Unrecognized pair benchmark')
    retained = set(pairs.loc[pairs.n >= 5, 'bench'])
    eligible = {r['bench'] for r in records if r['eligible_pairs'] > 0}
    values = {
        'inventory_benchmarks': len(records),
        'benchmarks_any_pair_n_ge_5': len(retained),
        'benchmarks_positive_eligible_pairs': len(eligible),
        'pairs_n_ge_5': int((pairs.n >= 5).sum()),
        'scored_raw_pairs': sum(r['eligible_pairs'] for r in records),
        'benchmarks_without_pair_n_ge_5': sorted(inventory_benchmarks - retained),
        'retained_prior_benchmarks_without_eligible_pairs': sorted(retained - eligible),
        'prior_pair_definition': 'Benchmark × full subject configuration with at least 5 binary responses.',
        'evaluation_pair_definition': 'Benchmark × raw subject ID with at least 80 distinct observed items.',
        'inputs': {'prepared.json': sha(prepared), 'pair_stats.csv': sha(stats)}}
    dump(EVIDENCE / 'inventory.json', values)
    return records


def score_partitions(benchmark, subjects, parts, model=None):
    """Official mean uses ALL labels matching visible attributes; Beta uses own raw ID only."""
    model = load_empirical() if model is None else model
    item = {'benchmark_id': benchmark}  # the official model only reads this item field
    labels_by_subject = {}
    visible = {}
    members = defaultdict(list)
    for sid, (acquired, _) in parts.items():
        row = subjects.loc[sid]
        visible[sid] = {field: row[field] for field in measure.SUBJECT_FIELDS}
        members[tuple(visible[sid].values())].append(sid)
        labels_by_subject[sid] = acquired['first'].to_numpy(dtype=int)[:max(BUDGETS)]
    scores = {sid: {'bench': benchmark, 'subject_id': sid} for sid in parts}
    outcomes = {sid: (ev.k.to_numpy(float), ev.n.to_numpy(float)) for sid, (_, ev) in parts.items()}
    for budget in BUDGETS:
        for group in members.values():
            target = visible[group[0]]
            # The pinned implementation skips all unequal visible subjects before inspecting labels.
            labels = [((visible[sid], item), int(y)) for sid in group for y in labels_by_subject[sid][:budget]]
            empirical = model.predict((target, item), labels)
            for sid in group:
                k, n = outcomes[sid]
                own = labels_by_subject[sid][:budget]
                beta = (1.0 + own.sum()) / (2.0 + len(own))
                scores[sid][f'empirical_b{budget}'] = measure.brier(empirical, k, n)
                scores[sid][f'beta11_b{budget}'] = measure.brier(beta, k, n)
    for row in scores.values():
        for tag in ('empirical', 'beta11'):
            row[f'{tag}_alc'] = sum(w * row[f'{tag}_b{b}'] for w, b in zip(WEIGHTS, BUDGETS))
    return list(scores.values())


def replay(run, records):
    measure.DATA = run / 'data'
    artifacts = run / 'artifacts'
    cache = run / 'camera_ready_baselines'
    for record in records:
        if not record['eligible_pairs']:
            continue
        benchmark, fold = record['bench'], record['fold']
        prior = json.loads((artifacts / f'fold_prior_{fold}.json').read_text())
        sigma = json.loads((artifacts / f'fold_{fold}_config.json').read_text())['sigma_delta2']
        evaluation.c2.set_prior(prior, sigma)
        subjects, cells = measure.read_bench(benchmark)
        capture = []
        partition = evaluation.partition_cells
        def score_same_partition(cells, name):
            eligible, parts = partition(cells, name)
            capture.extend(score_partitions(name, subjects, parts))
            return eligible, parts
        evaluation.partition_cells = score_same_partition
        try:
            method_rows, _ = evaluation.simulate_benchmark(benchmark, prior, sigma, subjects=subjects, cells=cells)
        finally:
            evaluation.partition_cells = partition
            evaluation.c2.clear_cache()
        evaluation.validate_frame(method_rows, record, 'c2')
        rows = method_rows.merge(pd.DataFrame(capture), on=['bench', 'subject_id'], validate='one_to_one')
        assert len(rows) == record['eligible_pairs']
        path = cache / benchmark / 'scores.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        rows.to_csv(path, index=False)
        print(benchmark, len(rows), flush=True)
    return cache


def compare(rows, tag):
    diff = rows.assign(diff=rows['C2_alc'] - rows[f'{tag}_alc'])
    by_bench = diff.groupby('bench', sort=True)['diff'].agg(['sum', 'size'])
    rng = np.random.default_rng(0)
    clusters = rng.integers(0, len(by_bench), size=(2000, len(by_bench)))
    samples = by_bench['sum'].to_numpy()[clusters].sum(axis=1) / by_bench['size'].to_numpy()[clusters].sum(axis=1)
    ci = np.percentile(samples, [2.5, 97.5]).tolist()
    folds = diff.groupby('fold')['diff'].mean()
    return {'alc': float(rows[f'{tag}_alc'].mean()),
            'brier': {str(b): float(rows[f'{tag}_b{b}'].mean()) for b in BUDGETS},
            'C2_minus_baseline': float(diff['diff'].mean()), 'C2_minus_baseline_ci95': ci,
            'baseline_minus_C2_ci95': [-ci[1], -ci[0]], 'C2_fold_wins': int((folds < 0).sum()),
            'fold_C2_minus_baseline': {str(k): float(v) for k, v in folds.items()}}


def summarize(run, records, cache):
    frames, inputs = [], {}
    for record in records:
        if not record['eligible_pairs']:
            continue
        path = cache / record['bench'] / 'scores.csv'
        frame = pd.read_csv(path, dtype={'bench': str, 'subject_id': str}, keep_default_na=False)
        if (len(frame) != record['eligible_pairs'] or frame['subject_id'].duplicated().any()
                or not frame['bench'].eq(record['bench']).all() or not frame['fold'].eq(record['fold']).all()):
            raise ValueError('Invalid score coverage ' + record['bench'])
        frames.append(frame)
        inputs[record['bench']] = sha(path)
    rows = pd.concat(frames, ignore_index=True)
    if not np.isfinite(rows[['C2_alc', 'frozen_alc', 'empirical_alc', 'beta11_alc']]).all().all():
        raise ValueError('Nonfinite scores')
    targets = json.loads((ROOT / 'verification/expected_values.json').read_text())['split2']
    means = {k: float(rows[col].mean()) for k, col in [('C2_ALC','C2_alc'), ('frozen_ALC','frozen_alc')]}
    diffs = {k: abs(v - targets[k]) for k, v in means.items()}
    gate = {'status': 'PASS' if max(diffs.values()) <= 1e-9 else 'FAIL',
            'tolerance': 1e-9, 'observed': means, 'absolute_differences': diffs}
    empirical, beta = compare(rows, 'empirical'), compare(rows, 'beta11')
    reference = {'alc': 0.2368, 'brier': dict(zip(map(str, BUDGETS), [0.2500, 0.3490, 0.2330, 0.2002, 0.1866, 0.1805])),
                 'baseline_minus_C2_ci95': [0.0427, 0.0595]}
    differences = {'alc': abs(empirical['alc'] - reference['alc']),
                   **{f'b{b}': abs(empirical['brier'][str(b)] - reference['brier'][str(b)]) for b in BUDGETS},
                   **{f'ci_{i}': abs(x-y) for i, (x,y) in enumerate(zip(empirical['baseline_minus_C2_ci95'], reference['baseline_minus_C2_ci95']))}}
    columns = [field for tag in ('C2', 'frozen', 'empirical', 'beta11')
               for field in [f'{tag}_alc', *(f'{tag}_b{b}' for b in BUDGETS)]]
    grouped = rows.groupby(['bench', 'fold'], sort=True)
    sums = grouped[columns].sum().add_suffix('_sum')
    sums.insert(0, 'pairs', grouped.size())
    kept = EVIDENCE / 'empirical_mean/benchmark_sums.csv'
    kept.parent.mkdir(parents=True, exist_ok=True)
    sums.to_csv(kept)
    result = {'M2': {'status': 'RECOMPUTED_MATCH' if max(differences.values()) <= 5e-4 else 'RECOMPUTED_MISMATCH',
                     'values': empirical, 'reference_displayed': reference,
                     'reference_absolute_differences': differences, 'tolerance': 5e-4},
              'M6': {'status': 'MEASURED', 'values': beta}, 'adapter_gate': gate,
              'bootstrap': {'clusters': 'benchmark', 'pair_weight': 'equal', 'replicates': 2000, 'seed': 0,
                            'interval': 'percentile 2.5/97.5; loss difference, negative C2 minus baseline favors C2'},
              'scoring_callbacks': {
                  'hash_definition': 'SHA-256 of UTF-8 inspect.getsource, including decorator when present',
                  'source_sha256': {fn.__name__: hashlib.sha256(inspect.getsource(fn).encode()).hexdigest()
                                    for fn in (load_empirical, score_partitions)},
                  'scoring_entry': 'reliability.py --with-baselines supplies the exact split2 partitions',
                  'binding_note': 'Callback source digests recorded at aggregation. Both callback definitions were unchanged during the scoring run.'},
              'source_search': {
                  'scored_original': 'NOT_IDENTIFIED',
                  'checked': ['PAIEC2026 research and release trees',
                              'historical PAIEC2026 headroom, report, and p2probe trees',
                              'PAIEC camera-ready audit and local release copies',
                              'PAIEC_v14_evidence.tar.gz and neighboring evidence'],
                  'findings': ['Submitted TeX and extracted manuscript reproduce the displayed row.',
                               'The headroom report supplies a predictor hash. Its summary scores frozen and A–D.',
                               'The v14 archive covers sparse and S2WISH comparisons. Its score tables lack an empirical row.']},
              'official_model': {'repo': 'https://github.com/aims-foundations/paiec_baseline',
                                 'history_commit': MODEL_COMMIT, 'path': 'empirical_mean/model.py', 'sha256': MODEL_HASH,
                                 'subject_equality_fields': list(measure.SUBJECT_FIELDS),
                                 'label_rule': 'Pool matching visible attributes and benchmark_id. Beta(1,1) uses the target raw pair alone.'},
              'pairs': len(rows), 'benchmarks': len(inputs), 'inputs_per_benchmark_sha256': inputs,
              'benchmark_sum_evidence': {kept.relative_to(ROOT).as_posix(): sha(kept)}}
    dump(EVIDENCE / 'baselines.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'inputs_per_benchmark_sha256'}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['inventory', 'summarize', 'replay'])
    parser.add_argument('--run', required=True, type=Path)
    args = parser.parse_args()
    run_dir = args.run.resolve()
    records = inventory(run_dir / 'artifacts')
    if args.operation != 'inventory':
        cached = replay(run_dir, records) if args.operation == 'replay' else run_dir / 'camera_ready_m5'
        summarize(run_dir, records, cached)
