"""Portable file and population checks; no statistical calculations."""
import json
from pathlib import Path
import pandas as pd
from corehelpers import measure, protocol

EXPECTED_INVENTORY_BENCHMARKS = 163
EXPECTED_ELIGIBLE_BENCHMARKS = 145
EXPECTED_PAIRS = 13023


def resident(path):
    path = Path(path)
    if getattr(path.lstat(), 'st_flags', 0) & 0x40000000:
        raise ValueError('Required file is not resident: ' + path.name)
    return path


def read_json(path):
    return json.loads(resident(path).read_bytes())


def atomic_json(path, value):
    measure.atomic_text(path, json.dumps(value, indent=2, allow_nan=False) + '\n')


def create_output(path):
    path = Path(path).resolve()
    if path.exists():
        raise ValueError('A fresh output directory is required')
    path.mkdir(parents=True)
    return path


def capture_inputs(data):
    data = Path(data)
    inputs = {}
    for path in sorted(data.glob('*/benchmarks.parquet')):
        resident(path)
        meta = pd.read_parquet(path).iloc[0]
        if meta.get('response_type') != 'binary' or meta.get('granularity') != 'item':
            continue
        directory = path.parent
        response = directory / 'response.parquet'
        if not response.exists():
            response = directory / 'responses.parquet'
        for required in [path, directory / 'subjects.parquet', directory / 'items.parquet', response]:
            resident(required)
            inputs[str(required.relative_to(data))] = measure.sha(required)
    benches = {Path(name).parts[0] for name in inputs}
    if len(benches) != EXPECTED_INVENTORY_BENCHMARKS:
        raise ValueError('Public binary/item benchmark inventory is incomplete')
    return inputs


def validate_inventory(prepared, data):
    records = prepared['benchmarks']
    if len(records) != EXPECTED_INVENTORY_BENCHMARKS:
        raise ValueError('Prepared inventory must contain every public binary/item benchmark')
    names = [r['bench'] for r in records]
    if len(set(names)) != len(names) or names != sorted(names):
        raise ValueError('Prepared benchmark inventory is duplicated or out of order')
    actual = []
    for path in sorted(Path(data).glob('*/benchmarks.parquet')):
        meta = pd.read_parquet(resident(path)).iloc[0]
        if meta.get('response_type') == 'binary' and meta.get('granularity') == 'item':
            actual.append(path.parent.name)
    if names != actual:
        raise ValueError('Prepared inventory differs from public benchmark metadata')
    for record in records:
        if record['fold'] != protocol.fold_of(record['bench']):
            raise ValueError('Prepared benchmark fold differs from registered fold hash')
        if any(not isinstance(record[k], int) or record[k] < 0 for k in ['responses', 'cells', 'items', 'eligible_pairs']):
            raise ValueError('Invalid prepared benchmark counts')
    if sum(bool(r['eligible_pairs']) for r in records) != EXPECTED_ELIGIBLE_BENCHMARKS:
        raise ValueError('Eligible benchmark inventory differs from registered coverage')
    if sum(r['eligible_pairs'] for r in records) != EXPECTED_PAIRS or prepared['pairs'] != EXPECTED_PAIRS:
        raise ValueError('Eligible pair inventory differs from registered coverage')
    return records


def source_hashes():
    root = Path(__file__).resolve().parents[1]
    return {str(path.relative_to(root)): measure.sha(resident(path))
            for path in sorted(root.rglob('*.py'))}
