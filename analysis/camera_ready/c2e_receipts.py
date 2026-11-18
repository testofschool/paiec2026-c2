"""Inspect discovered outer-selection directories against the historical receipt format."""
import argparse
import datetime
import hashlib
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KST = datetime.timezone(datetime.timedelta(hours=9))
STOP = datetime.datetime(2026, 10, 20, 23, 59, tzinfo=KST)
HEX = re.compile(r'[0-9a-f]{64}')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inspect(path):
    entry = {'filename': path.name, 'benchmark': path.name.removesuffix('.done.json')}
    try:
        data = path.read_bytes()
        entry['sha256'] = sha(data)
        r = json.loads(data)
        binding = r.get('binding', {})
        complete = r.get('status') == 'COMPLETE'
        bound = (complete and binding.get('stage') == 'outer_selected'
                 and binding.get('benchmark') == entry['benchmark']
                 and bool(HEX.fullmatch(binding.get('provenance_sha256', '')))
                 and bool(HEX.fullmatch(r.get('csv_sha256', ''))))
        entry.update(status=r.get('status'), bound_complete=bound, fixture=r.get('fixture') is True)
        if bound:
            csv = path.with_name(entry['benchmark'] + '.csv')
            entry['csv_matches'] = csv.is_file() and sha(csv.read_bytes()) == r['csv_sha256']
            entry['completed_at_kst'] = r.get('completed_at_kst')
            timestamp = datetime.datetime.fromisoformat(entry['completed_at_kst'])
            entry['at_or_before_stop'] = timestamp.tzinfo is not None and timestamp <= STOP
    except (OSError, ValueError, TypeError, AttributeError) as e:
        entry['read_error'] = type(e).__name__
    return entry


def main():
    p = argparse.ArgumentParser()
    p.add_argument('t0', type=Path)
    p.add_argument('output', type=Path)
    a = p.parse_args()
    paths = json.loads(a.t0.read_text())['assets'].get('outer_selected', [])
    folders = []
    qualified = {}
    for label in sorted(paths):
        path = Path(label.replace('$PAIEC_SOURCE_ROOT', str(Path.home())))
        fixture_dir = 'fixtures' in path.parts
        with ThreadPoolExecutor(6) as workers:
            receipts = list(workers.map(inspect, sorted(path.glob('*.done.json'))))
        bound = [r for r in receipts if r.get('bound_complete')]
        verified = [r for r in bound if r.get('csv_matches') and r.get('at_or_before_stop') and not fixture_dir]
        for r in verified:
            qualified.setdefault(r['benchmark'], set()).add(r['sha256'])
        folders.append({'directory': label, 'fixture_directory': fixture_dir,
                        'receipt_count': len(receipts), 'bound_complete_count': len(bound),
                        'verified_before_stop_count': len(verified), 'receipts': receipts})
    duplicates = {b: sorted(hashes) for b, hashes in qualified.items() if len(hashes) > 1}
    values = {'stop_line_kst': STOP.isoformat(), 'discovered_directories': len(folders),
              'fixture_directories': sum(f['fixture_directory'] for f in folders), 'folders': folders,
              'duplicate_benchmarks_with_different_receipt_hashes': duplicates,
              'total_receipts_examined': sum(f['receipt_count'] for f in folders),
              'verified_benchmarks_before_stop': sorted(qualified),
              'historical_completed_count': len(qualified) if qualified and not duplicates else None}
    result = {'measured_at': datetime.datetime.now(KST).isoformat(),
              'status': 'COUNTED' if values['historical_completed_count'] is not None else 'NOT_FOUND',
              'values': values,
              'note': 'No historical count is inferred from missing run directories, inner-grid receipts, or test fixtures. A present-day receipt with no stop-line timestamp cannot certify historical completion.'}
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
