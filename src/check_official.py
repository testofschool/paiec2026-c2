"""Run an independently supplied, hash-pinned official checker offline."""
import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from resident_files import local_path, local_file

CHECKER_SHA256 = 'abe3cae05f4b18450b36edca60faef8a39bdf21821f30ff195c3cc45e177c646'
HELPER_SHA256 = 'c6f2610f9c8b6cad8a2338ddc07a0cb25d40bca761a6628937a2cee2705a6267'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checker-dir', required=True, type=Path)
    parser.add_argument('--zip', required=True, type=Path)
    args = parser.parse_args()
    root = local_path(args.checker_dir)
    for relative, expected in [('check_submission_zip.py', CHECKER_SHA256),
                               ('tools/streaming_ingestion.py', HELPER_SHA256)]:
        path = local_file(root / relative)
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Official checker source hash mismatch: ' + relative)
    archive = local_file(args.zip)
    with tempfile.TemporaryDirectory(prefix='paiec-checker-cache-') as cache:
        environment = dict(os.environ, PYTHONPYCACHEPREFIX=cache, PYTHONDONTWRITEBYTECODE='1')
        environment.pop('PYTHONPATH', None)
        environment.pop('PYTHONHOME', None)
        return subprocess.call([sys.executable, '-B', str(root / 'check_submission_zip.py'), str(archive)],
                               env=environment)


if __name__ == '__main__':
    sys.exit(main())
