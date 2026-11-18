"""Verify v21 supplied files, release sources, and measurement definitions."""
import argparse
import datetime
import hashlib
import json
import math
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EVIDENCE = REPO / 'verification/evidence/camera_ready'
HOME = Path.home()
TOKEN = '$PAIEC_SOURCE_ROOT'
FILES = {
    'dist/C2_r1.zip': '70ff16e31d76195fc07c487a446c0a17f3f2fd63f234d81035f05e9f7e6ae31d',
    'verification/expected_values.json': '63011992452eeec465fef451d0024a50f1e11060836df6b4da072c5be92a7132',
    'verification/evidence/c2d2/summary.json': '68c3773c96ff48b4ba50c3c74e5f1c5cdc84f9eb39b0ba77acc5590d271c3c68',
    'src/irt_shrink/model.py': '1d84ecb67c8b772a3719078bf2ca067d2bb0802ba36489e45181d4886bd4dcc6',
    'src/c2/model.py': '14ed10f59580da8d25deb41eb4cf5d945b94f31aacf7e995f2cccc424e2756d8',
    'src/corehelpers/protocol.py': 'e665df810d118115acfb98e7debdbbc3140191e983823bf46ef05d0acdcf4d1b',
}
MEMBERS = {
    'paiec_camera_ready.tex': 'be36e88aa3b67cf0df3ba774ec7da92f99d14786a8a644adb5add989af5f47df',
    'trace_numbers.py': 'ca1b62154cd6e44939760e190205d63293de83d76a91c70c445e1e48487e34c6',
    'formative_records.json': 'b616bd9774456498c24edb12bea8efa31b0000b9dd79b904414d4137bd77ce15',
    'neurips_2026.sty': 'c3fc2894e83d2517ca18b66741d6c595986d97957dc08ec08bb2125a7ec4555a',
    'fig_budget.pdf': 'b1c0ee8100ac2696ba61c26c4b1576fa655fbe5802c3ac11632dd5524c352f7e',
}
RELEASE_HEAD = '8f2354c084dff2996419e9b248bb70f7a7e4426a'
sha = lambda b: hashlib.sha256(b).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def command(*args):
    run = subprocess.run(args, capture_output=True, text=True, cwd=REPO)
    return {'exit': run.returncode, 'stdout': run.stdout.strip().replace(str(HOME), TOKEN)}


def compare(name, expected, actual, source):
    numeric = isinstance(expected, (float, int))
    return dict(name=name, expected=expected, actual=actual, source=source,
                difference=actual - expected if numeric else None,
                status='MATCH' if expected == actual else 'MISMATCH')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--downloads', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    now = datetime.datetime.now().astimezone().isoformat()
    archive = a.downloads / 'PAIEC_v21_attachments.zip'
    memo = a.downloads / 'CODEX_PAIEC_v21_camera_ready_20261119.md'
    pdf = a.downloads / 'PAIEC_camera_ready_DRAFT_v21.pdf'
    checks = [compare(path, expected, sha((REPO / path).read_bytes()), path) for path, expected in FILES.items()]
    with zipfile.ZipFile(archive) as z:
        attachment_rows = [compare(path, expected, sha(z.read(path)), archive.name) for path, expected in MEMBERS.items()]
        (EVIDENCE / 'formative').mkdir(exist_ok=True, parents=True)
        (EVIDENCE / 'formative/records.json').write_bytes(z.read('formative_records.json'))
        tex = z.read('paiec_camera_ready.tex').decode()
    checks.extend(attachment_rows)
    parents = command('git', 'rev-parse', 'origin/main')['stdout']
    checks.append(compare('origin/main', RELEASE_HEAD, parents, 'local remote-tracking ref from fresh clone'))
    sname = 'verification/evidence/c2d2/summary.json'
    expected_values = json.loads((REPO / 'verification/expected_values.json').read_text())
    c2 = json.loads((REPO / sname).read_text())['methods']['C2']
    k = c2['kstar_detail']
    for key, value in dict(C2_ALC=0.18487910654403214, frozen_ALC=0.2015333932758017, C2_B0=0.24893649649887992).items():
        checks.append(compare(key + ' (registered source)', value, expected_values['split2'][key], 'verification/expected_values.json'))
    historical = [
        ('methods.C2.delta', 0.01665428673176956, c2['delta']),
        ('kstar_detail.contributions[0].benchmark', 'alignment_faking', k['contributions'][0][0]),
        ('kstar_detail.contributions[0].value', 169.10505714750985, k['contributions'][0][1]),
        ('sum(kstar_detail.contributions)', 216.88877610783499, math.fsum(pair[1] for pair in k['contributions'])),
        ('kstar_detail.trace[1].delta', 0.005464118806212137, k['trace'][1]['delta']),
        ('kstar_detail.trace[1].remaining_rows', 8745, k['trace'][1]['remaining_rows']),
    ]
    checks.extend(compare(n, e, x, sname) for n, e, x in historical)
    prior = 'src/archive_payload/prior.json'
    stats = json.loads((REPO / prior).read_text())['stats']
    for name, value in dict(benchmarks=158, subject_configs=14089, pairs=14436).items():
        checks.append(compare('prior.stats.' + name, value, stats[name], prior))
    save(EVIDENCE / 'source_preregistration.json', dict(measured_at=now, checks=checks))
    marker_lines = [{'line': i, 'ids': re.findall(r'\bM[0-6]\b', line)}
                    for i, line in enumerate(tex.splitlines(), 1) if r'\pending{M' in line]
    ids = sorted({key for line in marker_lines for key in line['ids']})
    save(EVIDENCE / 'measurement_definitions.json', {
        'status': 'NOT_SPECIFIED' if 'M1' not in ids else 'CHECK_DEFINITION',
        'values': {'tex_pending_ids': ids, 'tex_pending_lines': marker_lines,
                   'handoff_track_headings': [line for line in memo.read_text().splitlines() if line.startswith('## T')]},
        'measured_at': now, 'inputs': {memo.name: sha(memo.read_bytes()), 'paiec_camera_ready.tex': sha(tex.encode())},
        'note': 'M1 has no measurement definition in the handoff or pending marker in the draft. Source-level preregistration checks are reported separately.'})
    grouped = {}
    for f in sorted(a.out.glob('discovery_*.txt')):
        if f.name.endswith('_coverage.txt'):
            continue
        for line in f.read_text().splitlines():
            grouped.setdefault(Path(line).name, set()).add(line)
    python = shutil.which('python3.10') or shutil.which('python3')
    net = {host: command('curl', '-sSI', '--max-time', '12', '-o', '/dev/null', '-w', '%{http_code}', 'https://' + host)
           for host in ['github.com', 'pypi.org', 'huggingface.co']}
    missing = a.out / 'missing_resident.json'
    initial = len(json.loads(missing.read_text())) if missing.exists() else None
    df = command('df', '-g', str(HOME))
    save(a.out / 'T0.json', {
        'measured_at': now, 'architecture': command('uname', '-m'), 'cpu': command('sysctl', '-n', 'machdep.cpu.brand_string'),
        'macos': command('sw_vers', '-productVersion'), 'memory_bytes': command('sysctl', '-n', 'hw.memsize'),
        'disk_GiB': df, 'python': {'executable': python.replace(str(HOME), TOKEN), 'version': command(python, '--version')}, 'network': net,
        'assets': {k: sorted(v) for k,v in sorted(grouped.items())},
        'search_coverage': {f.name: f.read_text().strip() for f in sorted(a.out.glob('discovery_*_coverage.txt'))},
        'pinned_data': {'revision': '54074453da7b9911be0f48e4c560be547bc84d21', 'initially_missing_of_652': initial,
                        'initially_available_of_652': 652-initial if initial is not None else None,
                        'location': TOKEN + '/.cache/huggingface/hub/datasets--aims-foundations--measurement-db/snapshots/54074453da7b9911be0f48e4c560be547bc84d21',
                        'note': 'T1 preparation logs record validated file coverage, downloads and final status.'},
        'zip_members': attachment_rows,
        'supplied_files_without_registered_digest': {f.name: sha(f.read_bytes()) for f in (memo, archive, pdf)}})


if __name__ == '__main__':
    main()
