"""Rebuild the registered archival C2 package from immutable member bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
from resident_files import local_path, local_file

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SHA256 = 'f4a89cd195b5b2b1537930fdf588e1a572d981389d0b13fd737f125750c524f5'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    manifest_bytes = local_file(ROOT / 'verification/archive_payload_manifest.json').read_bytes()
    if hashlib.sha256(manifest_bytes).hexdigest() != MANIFEST_SHA256:
        raise ValueError('Registered archival member manifest changed')
    manifest = json.loads(manifest_bytes)
    locations = {'README.md': ROOT / 'src/archive_payload/README.md',
                 'prior.json': ROOT / 'src/archive_payload/prior.json',
                 'model.py': ROOT / 'src/c2/model.py',
                 'frozen_model.py': ROOT / 'src/irt_shrink/model.py'}
    members = {}
    for name, path in locations.items():
        data = local_file(path).read_bytes()
        if hashlib.sha256(data).hexdigest() != manifest['payload_members'][name]:
            raise ValueError('Archival member hash mismatch: ' + name)
        members[name] = data
    output = local_path(args.out, missing_ok=True)
    if output.exists():
        raise ValueError('A fresh archive output is required')
    if ROOT == output or ROOT in output.parents:
        raise ValueError('Keep built outputs outside the source release tree')
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.name + '.tmp')
    if temporary.exists():
        raise ValueError('A previous temporary archive exists')
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(members.items()):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            archive.writestr(entry, data)
    observed = hashlib.sha256(temporary.read_bytes()).hexdigest()
    if observed != manifest['reference_archive_sha256']:
        raise ValueError('Built archive differs from the registered exact hash')
    temporary.replace(output)
    print(json.dumps({'status': 'PASS', 'archive': 'C2_r1.zip',
                      'size_bytes': output.stat().st_size, 'sha256': observed}))


if __name__ == '__main__':
    main()
