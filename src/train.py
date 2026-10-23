"""Train the frozen-base and C2 variance parameters from public data."""
import sys
sys.dont_write_bytecode = True
import argparse
import gc
import json
import shutil
import time
from pathlib import Path
import numpy as np
import pandas as pd
from corehelpers import measure as source
from corehelpers.io import atomic_json, capture_inputs, create_output, source_hashes, validate_inventory

HERE = Path(__file__).resolve().parent
FIXED_OPTIONS = {'outcomes': 'all recorded binary trials', 'target': 'log((k+1)/(n-k+1)), equal-item benchmark centering',
    'theta_prior_variance': 4.0, 'theta_prior_mean': 'log((k+1)/(n-k+1))',
    'item_prior_variance': 1.0, 'intercept_prior_mean': 0.0, 'intercept_prior_variance': 4.0,
    'two_parameter': False, 'optimizer': 'L-BFGS-B', 'maxiter': 500,
    'ftol': 1e-9, 'gtol': 1e-5, 'maxcor': 10, 'sigma_pooling': 'centered sum squares / item count',
    'sigma_floor': 1e-8}


def fit_offsets(inventory):
    (HERE / 'targets').mkdir(parents=True, exist_ok=True)
    (HERE / 'variance_fits').mkdir(exist_ok=True)
    completed = []
    for record in inventory:
        bench = record['bench']
        out = HERE / 'targets' / (bench + '.parquet')
        fit_file = HERE / 'variance_fits' / (bench + '.json')
        marker = HERE / 'variance_fits' / (bench + '.done.json')
        if shutil.disk_usage(HERE).free < 8 * 1024 ** 3:
            raise RuntimeError('Preparation needs 8 GiB free; completed checkpoints retained')
        start = time.perf_counter()
        subjects, cells = source.read_bench(bench)
        targets = cells.groupby('item_id', sort=True).agg(k=('k', 'sum'), n=('n', 'sum')).reset_index()
        targets['e'] = np.log((targets.k + 1.) / (targets.n - targets.k + 1.))
        targets['e'] -= targets.e.mean() if len(targets) else 0.
        temporary = out.with_suffix('.parquet.tmp')
        targets.to_parquet(temporary, index=False)
        temporary.replace(out)
        if len(cells):
            si, sids = pd.factorize(cells.subject_id, sort=True)
            ii, items = pd.factorize(cells.item_id, sort=True)
            rates = cells.groupby('subject_id', sort=True).agg(k=('k', 'sum'), n=('n', 'sum')).reindex(sids)
            tm = np.log((rates.k.to_numpy() + 1.) / (rates.n.to_numpy() - rates.k.to_numpy() + 1.))
            _, offsets, _, diagnostics = source.fit_irt(si, ii, cells.k.to_numpy(float),
                cells.n.to_numpy(float), tm, np.full(len(sids), 4.), len(items), two=False, dvar=4.)
            centered = offsets - offsets.mean()
            ss = float(np.dot(centered, centered))
            fit = {'bench': bench, 'fold': record['fold'], 'items': len(items),
                   'offset_sum_squares': ss, 'variance': ss / len(items), **diagnostics}
        else:
            fit = {'bench': bench, 'fold': record['fold'], 'items': 0,
                   'offset_sum_squares': 0., 'variance': None, 'success': True,
                   'message': 'empty benchmark', 'iterations': 0}
        fit['wall_seconds'] = time.perf_counter() - start
        atomic_json(fit_file, fit)
        atomic_json(marker, {'target_sha256': source.sha(out), 'fit_sha256': source.sha(fit_file),
                            'fixed_options': FIXED_OPTIONS})
        completed.append(fit)
        print(json.dumps({k: fit.get(k) for k in ('bench', 'items', 'variance', 'success', 'iterations', 'wall_seconds')}), flush=True)
        del subjects, cells, targets
        gc.collect()
    for fold in range(6):
        training = [x for x in completed if x['fold'] != fold and x['items']]
        sigma2 = max(1e-8, sum(x['offset_sum_squares'] for x in training) / sum(x['items'] for x in training))
        atomic_json(HERE / ('fold_' + str(fold) + '_config.json'), {
            'fold': fold, 'sigma_delta2': sigma2, 'training_benchmarks': [x['bench'] for x in training],
            'training_items': sum(x['items'] for x in training),
            'failed_fit_benchmarks': [x['bench'] for x in training if not x['success']]})
    training = [x for x in completed if x['items']]
    atomic_json(HERE / 'public_config.json', {
        'sigma_delta2': max(1e-8, sum(x['offset_sum_squares'] for x in training) / sum(x['items'] for x in training)),
        'training_benchmarks': [x['bench'] for x in training],
        'training_items': sum(x['items'] for x in training),
        'failed_fit_benchmarks': [x['bench'] for x in training if not x['success']]})
    atomic_json(HERE / 'prepare_summary.json', {'benchmarks': len(completed),
        'items': sum(x['items'] for x in completed), 'fit_successes': sum(x['success'] for x in completed),
        'fits': completed})


def main():
    global HERE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    source.DATA = args.data.resolve()
    inputs = capture_inputs(source.DATA)
    sources = source_hashes()
    HERE = create_output(args.out)
    source.HERE = HERE
    atomic_json(HERE / 'inputs_before.json', inputs)
    source.prepare()
    prepared = json.loads((HERE / 'prepared.json').read_text())
    inventory = validate_inventory(prepared, source.DATA)
    fit_offsets(inventory)
    pairs = pd.read_csv(HERE / 'pair_stats.csv', keep_default_na=False)
    public_prior = source.fit_prior_stats(pairs, pairs.n.sum())
    atomic_json(HERE / 'prior_base.json', public_prior)
    public_config = json.loads((HERE / 'public_config.json').read_text())
    public_prior['c2'] = {'sigma_delta2': public_config['sigma_delta2']}
    atomic_json(HERE / 'prior.json', public_prior)
    after = capture_inputs(source.DATA)
    if inputs != after or source_hashes() != sources:
        raise ValueError('Public data or training source changed during training')
    atomic_json(HERE / 'inputs_after.json', after)
    atomic_json(HERE / 'training_receipt.json', {
        'schema_version': 1, 'status': 'COMPLETE', 'fixed_options': FIXED_OPTIONS,
        'coverage': {'inventory_benchmarks': len(inventory),
                     'benchmarks': sum(bool(r['eligible_pairs']) for r in inventory),
                     'pairs': sum(r['eligible_pairs'] for r in inventory)},
        'inputs': inputs, 'sources': sources,
        'outputs': {p.name: source.sha(p) for p in sorted(HERE.glob('*.json'))}})


if __name__ == '__main__':
    main()
