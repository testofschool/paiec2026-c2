#!/usr/bin/env python3
"""Mask local folder names in the v21 camera-ready evidence.

usage: python3 -I scrub_paths.py REPO_DIR            # rewrite, print counts
       python3 -I scrub_paths.py REPO_DIR --check    # exit 0 only if nothing is left

'$PAIEC_SOURCE_ROOT/Desktop/<local folders>/PAIEC2026/' becomes '$PAIEC_SOURCE_ROOT/',
the form the earlier public release already uses. Only path strings change; no number,
status or key is touched. A sha256 of a rewritten file recorded in another camera-ready
file is updated to the new value. Stdlib only.
"""
import hashlib, os, re, sys

PAT = re.compile(r'\$PAIEC_SOURCE_ROOT/Desktop/[^"\n]*?/PAIEC2026/')
DIRS = ('analysis/camera_ready', 'verification/evidence/camera_ready')
LEFT = re.compile(r'Desktop|/Users/')

def files(repo):
    for d in DIRS:
        for root, _, names in os.walk(os.path.join(repo, d)):
            for n in sorted(names):
                p = os.path.join(root, n)
                try:
                    open(p, encoding='utf-8').read()
                except (UnicodeDecodeError, OSError):
                    continue
                yield p

def main(a):
    repo = a[0]; check = '--check' in a
    here = os.path.basename(__file__)
    if check:
        left = 0
        for p in files(repo):
            if os.path.basename(p) == here: continue
            n = len(LEFT.findall(open(p, encoding='utf-8').read()))
            if n: print('LEFT', os.path.relpath(p, repo), n); left += n
        print('left', left); return 0 if left == 0 else 1
    swaps = {}
    for p in files(repo):
        if os.path.basename(p) == here: continue
        b = open(p, 'rb').read(); s = b.decode('utf-8')
        new, n = PAT.subn('$PAIEC_SOURCE_ROOT/', s)
        if n:
            nb = new.encode('utf-8'); open(p, 'wb').write(nb)
            swaps[hashlib.sha256(b).hexdigest()] = hashlib.sha256(nb).hexdigest()
            print('rewrote', os.path.relpath(p, repo), n)
    for _ in range(3):  # recorded hashes of rewritten files, to a fixed point
        changed = False
        for p in files(repo):
            if os.path.basename(p) == here: continue
            b = open(p, 'rb').read(); s = b.decode('utf-8'); new = s
            for old, nw in swaps.items(): new = new.replace(old, nw)
            if new != s:
                nb = new.encode('utf-8'); open(p, 'wb').write(nb); changed = True
                swaps[hashlib.sha256(b).hexdigest()] = hashlib.sha256(nb).hexdigest()
                print('updated recorded hash in', os.path.relpath(p, repo))
        if not changed: break
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) if len(sys.argv) >= 2 else 2)
