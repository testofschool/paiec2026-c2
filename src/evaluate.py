"""Recompute the registered C2 split2 and split3 metrics from public data."""
import sys
sys.dont_write_bytecode = True
import argparse
import gc
import json
import time
from pathlib import Path
import pandas as pd
from corehelpers import evaluation as ev, measure as source, split3
from corehelpers.io import (EXPECTED_ELIGIBLE_BENCHMARKS, EXPECTED_PAIRS,
    atomic_json, capture_inputs, create_output, read_json, resident,
    source_hashes, validate_inventory)


def evaluate_split(split, inventory, artifacts, output, sources, input_hashes):
    ev.split_seed = split3.split_seed if split == 'split3' else ORIGINAL_SPLIT2_SEED
    directory = output / split
    directory.mkdir()
    frames = []
    selected = [r for r in inventory if r['eligible_pairs']]
    for record in selected:
        started = time.perf_counter()
        benchmark, fold = record['bench'], record['fold']
        prior_path = artifacts / f'fold_prior_{fold}.json'
        config_path = artifacts / f'fold_{fold}_config.json'
        prior, config = read_json(prior_path), read_json(config_path)
        training = [r['bench'] for r in inventory if r['fold'] != fold and r['items']]
        if config.get('fold') != fold or config['training_benchmarks'] != training:
            raise ValueError('Offset variance training population differs from the registered outer fold')
        ev.c2.set_prior(prior, config['sigma_delta2'])
        frame, diagnostics = ev.simulate_benchmark(benchmark, prior, config['sigma_delta2'], stage='c2')
        ev.validate_frame(frame, record, 'c2')
        destination = directory / (benchmark + '.csv')
        source.atomic_text(destination, frame.to_csv(index=False))
        provenance = {
            'split': split, 'benchmark': benchmark, 'fold': fold,
            'split_seed': ev.split_seed(benchmark), 'rows': len(frame),
            'csv_sha256': source.sha(destination), 'sources': sources,
            'inputs': {k: v for k, v in input_hashes.items() if Path(k).parts[0] == benchmark},
            'artifacts': {prior_path.name: source.sha(prior_path), config_path.name: source.sha(config_path)},
            'diagnostics': diagnostics, 'wall_seconds': time.perf_counter() - started}
        atomic_json(directory / (benchmark + '.done.json'), provenance)
        frames.append(frame)
        print(json.dumps({'split': split, 'benchmark': benchmark, 'pairs': len(frame),
                          'wall_seconds': provenance['wall_seconds']}), flush=True)
        ev.c2.clear_cache()
        gc.collect()
    rows = pd.concat(frames, ignore_index=True)
    if len(selected) != EXPECTED_ELIGIBLE_BENCHMARKS or len(rows) != EXPECTED_PAIRS:
        raise ValueError('Incomplete registered evaluation coverage')
    if rows.duplicated(['bench', 'subject_id']).any():
        raise ValueError('Duplicate registered evaluation rows')
    source.atomic_text(directory / 'scores.csv', rows.to_csv(index=False))
    metrics = {'C2_ALC': float(rows.C2_alc.mean()), 'C2_B0': float(rows.C2_b0.mean())}
    if split == 'split2':
        metrics['frozen_ALC'] = float(rows.frozen_alc.mean())
    else:
        metrics['C2_B31'] = float(rows.C2_b31.mean())
    return {'status': 'COMPLETE', 'metrics': metrics,
            'coverage': {'benchmarks': len(selected), 'pairs': len(rows)}}


ORIGINAL_SPLIT2_SEED = ev.split_seed


def validate_training_receipt(artifacts, input_hashes, sources, artifact_hashes):
    """Require the supplied artifacts to be outputs of this source/data fit."""
    receipt_path = artifacts / 'training_receipt.json'
    receipt = read_json(receipt_path)
    if receipt.get('schema_version') != 1 or receipt.get('status') != 'COMPLETE':
        raise ValueError('A completed training receipt is required')
    expected_coverage = {'inventory_benchmarks': 163,
                         'benchmarks': EXPECTED_ELIGIBLE_BENCHMARKS,
                         'pairs': EXPECTED_PAIRS}
    if receipt.get('coverage') != expected_coverage:
        raise ValueError('Training receipt coverage differs from the registered population')
    if receipt.get('inputs') != input_hashes:
        raise ValueError('Training receipt does not bind the current public data')
    if receipt.get('sources') != sources:
        raise ValueError('Training receipt does not bind the current complete source set')
    outputs = receipt.get('outputs')
    if not isinstance(outputs, dict) or any(outputs.get(name) != digest
            for name, digest in artifact_hashes.items()):
        raise ValueError('Training receipt does not bind every supplied fold artifact')
    return source.sha(resident(receipt_path))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', required=True, type=Path)
    parser.add_argument('--artifacts', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--split', choices=['split2', 'split3', 'both'], default='both')
    args = parser.parse_args()
    source.DATA = args.data.resolve()
    artifacts = args.artifacts.resolve()
    inputs = capture_inputs(source.DATA)
    prepared = read_json(artifacts / 'prepared.json')
    inventory = validate_inventory(prepared, source.DATA)
    artifact_paths = [artifacts / 'prepared.json']
    for fold in range(6):
        artifact_paths.extend([artifacts / f'fold_prior_{fold}.json', artifacts / f'fold_{fold}_config.json'])
    artifact_hashes = {p.name: source.sha(resident(p)) for p in artifact_paths}
    sources = source_hashes()
    receipt_sha256 = validate_training_receipt(artifacts, inputs, sources, artifact_hashes)
    artifact_paths.append(artifacts / 'training_receipt.json')
    artifact_hashes['training_receipt.json'] = receipt_sha256
    output = create_output(args.out)
    atomic_json(output / 'inputs_before.json', inputs)
    atomic_json(output / 'provenance.json', {'sources': sources, 'artifacts': artifact_hashes,
                'population': 'all public eligible raw subject/benchmark pairs',
                'pair_weight': 1, 'within_pair_score': 'all recorded evaluation binary responses'})
    result = {'schema_version': 1}
    splits = ['split2', 'split3'] if args.split == 'both' else [args.split]
    for split in splits:
        result[split] = evaluate_split(split, inventory, artifacts, output, sources, inputs)
    after = capture_inputs(source.DATA)
    if inputs != after or source_hashes() != sources:
        raise ValueError('Input data or evaluation source changed during the rerun')
    if {p.name: source.sha(resident(p)) for p in artifact_paths} != artifact_hashes:
        raise ValueError('Training reference artifacts changed during the rerun')
    atomic_json(output / 'inputs_after.json', after)
    atomic_json(output / 'results.json', result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
