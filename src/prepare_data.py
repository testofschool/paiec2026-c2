"""Validate and copy an already obtained public dataset, entirely offline."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import time
from resident_files import local_path, local_file

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SHA256 = '09d46c62efb511713af315e167322492d599cd768a72aa9baa7c6ab7dca75eba'


def resident(path):
    return local_file(path)


def digest(path):
    path = resident(path)
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    manifest_path = ROOT / 'verification/public_input_manifest.json'
    if digest(manifest_path) != MANIFEST_SHA256:
        raise ValueError('Public input manifest changed')
    manifest = json.loads(manifest_path.read_bytes())
    source, output = local_path(args.source), local_path(args.out, missing_ok=True)
    if output.exists():
        raise ValueError('A fresh data output directory is required')
    if ROOT == output or ROOT in output.parents:
        raise ValueError('Keep public data outside the source release tree')
    if source == output or source in output.parents:
        raise ValueError('Keep generated copies outside the original public input root')
    selected = []
    for record in manifest['files']:
        relative = Path(record['path'])
        if len(relative.parts) != 2 or '..' in relative.parts or relative.is_absolute():
            raise ValueError('Unsafe public input path')
        benchmark, name = relative.parts
        names = [name, 'responses.parquet'] if name == 'response.parquet' else [name]
        candidates = [source / benchmark / item for item in names]
        candidates += [source / benchmark / 'formatted_tables' / item for item in names]
        existing = []
        for path in candidates:
            guarded = local_path(path, missing_ok=True)
            if guarded.exists():
                existing.append(local_file(guarded))
        if not existing:
            raise ValueError('Missing public input: ' + relative.as_posix())
        matched = None
        for path in existing:
            resident(path)
            if path.stat().st_size == record['size_bytes'] and digest(path) == record['sha256']:
                matched = path
                break
        if matched is None:
            raise ValueError('Public input hash mismatch: ' + relative.as_posix())
        selected.append((record, matched))
    required = sum(record['size_bytes'] for record, _ in selected)
    existing_parent = output.parent
    while not existing_parent.exists():
        existing_parent = existing_parent.parent
    if shutil.disk_usage(existing_parent).free < required + 8 * 1024 ** 3:
        raise ValueError('Insufficient space for public copy and training reserve')
    output.mkdir(parents=True)
    for record, path in selected:
        destination = output / record['path']
        destination.parent.mkdir(exist_ok=True)
        shutil.copyfile(path, destination)
        if destination.stat().st_size != record['size_bytes'] or digest(destination) != record['sha256']:
            raise ValueError('Copied public input differs: ' + record['path'])
    receipt = {'status': 'COMPLETE', 'mode': 'OFFLINE', 'files': len(selected),
               'bytes': required, 'manifest_sha256': MANIFEST_SHA256,
               'public_revision': manifest['public_revision'],
               'wall_seconds': time.perf_counter() - started}
    output.with_name(output.name + '_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
