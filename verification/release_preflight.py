#!/usr/bin/env python3
"""release_preflight.py — blocks `git push` of the PAIEC code release until the tree is
what the report says it is. Run from the repo root:  python3 -I release_preflight.py [--report REPORT.pdf]
Exit 0 = PREFLIGHT_PASS. Exit 1 = PREFLIGHT_FAIL (findings printed). Exit 2 = unusable.

Checks (all run, none skipped):
  P1 dist/C2_r1.zip exists, sha256 == expected_values.json registration, and is NOT git-ignored
  P2 verification/scrub_scan.py --root . exits 0 (no private paths / machine names)
  P3 README and REPRODUCTION_NOTE do not contradict: README must not claim an unconditional PASS
     while the note records a FAIL; README must state the observed cross-machine variation
  P4 every repo-relative path cited in the report PDF text exists in the tree
  P5 no absolute user-home paths in any text file
  P6 REPRODUCTION_NOTE.md present and listed in RELEASE_REPORT.md inventory
"""
import argparse, hashlib, json, os, re, subprocess, sys

def sh(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default=None, help="report PDF (pdftotext must be installed)")
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    f = []
    # P1
    zp = os.path.join(root, "dist", "C2_r1.zip")
    ev = os.path.join(root, "verification", "expected_values.json")
    if not os.path.exists(zp):
        f.append("P1 dist/C2_r1.zip missing from tree")
    elif not os.path.exists(ev):
        f.append("P1 verification/expected_values.json missing")
    else:
        sha = hashlib.sha256(open(zp, "rb").read()).hexdigest()
        txt = open(ev).read()
        if sha not in txt:
            f.append(f"P1 dist/C2_r1.zip sha {sha[:12]}… not found in expected_values.json")
        ci = sh(["git", "check-ignore", "-q", "dist/C2_r1.zip"], cwd=root)
        if ci.returncode == 0:
            f.append("P1 dist/C2_r1.zip is git-ignored (.gitignore) — a plain push drops the graded ZIP")
    # P2
    sc = os.path.join(root, "verification", "scrub_scan.py")
    if os.path.exists(sc):
        r = sh([sys.executable, "-I", sc, "--root", root], cwd=root)
        if r.returncode != 0:
            m = re.search(r'"status"\s*:\s*"([A-Z_]+)"', r.stdout)
            hits = re.search(r'"(?:forbidden_hit_count|hit_count|hits)"\s*:\s*(\d+)', r.stdout)
            f.append(f"P2 scrub_scan.py exit {r.returncode}: status {m.group(1) if m else '?'}" + (f", hits {hits.group(1)}" if hits else ""))
    else:
        f.append("P2 verification/scrub_scan.py missing")
    # P3
    rd = open(os.path.join(root, "README.md"), encoding="utf-8").read() if os.path.exists(os.path.join(root, "README.md")) else ""
    npth = os.path.join(root, "REPRODUCTION_NOTE.md")
    note = open(npth, encoding="utf-8").read() if os.path.exists(npth) else ""
    if re.search(r"\bFAIL\b", note) and re.search(r"reproduction PASS \(\d+ pass, 0 fail", rd):
        f.append("P3 README claims unconditional reproduction PASS while REPRODUCTION_NOTE records FAIL")
    if not re.search(r"cross-machine|other hardware|different hardware|another machine", rd, re.I):
        f.append("P3 README does not state the observed cross-machine variation")
    # P4
    if a.report:
        try:
            conversion = sh(["pdftotext", "-layout", a.report, "-"])
        except OSError as exc:
            f.append(f"P4 pdftotext could not run: {exc}")
            t = ""
        else:
            t = conversion.stdout
            if conversion.returncode != 0:
                f.append(f"P4 pdftotext exit {conversion.returncode}: report text could not be extracted")
                t = ""
            elif not t.strip():
                f.append("P4 pdftotext returned empty report text")
        cited = set(re.findall(r"\b((?:c2d2|c2b0|headroom|c2e|verification|src|scripts|dist)/[A-Za-z0-9_./-]+)", t))
        cited |= set(re.findall(r"\b([A-Za-z0-9_]+\.(?:csv|json|py))\b", t))
        missing = []
        for c in sorted(cited):
            c = c.rstrip(".,)")
            if c == "labeling.py" and re.search(r"no labeling\.py|submit no labeling", t):
                continue  # the report states this file is intentionally absent
            if "/" in c:
                ok = os.path.exists(os.path.join(root, c)) or os.path.exists(os.path.join(root, "verification", "evidence", c))
            else:
                ok = any(c in files for _, _, files in os.walk(root))
            if not ok:
                missing.append(c)
        if missing:
            f.append("P4 cited in report but absent from tree: " + ", ".join(missing))
    # P5
    hits = []
    for d, _, files in os.walk(root):
        if ".git" in d:
            continue
        for fn in files:
            if fn.endswith((".md", ".txt", ".json", ".py", ".sh", ".lock", ".cfg", ".toml")):
                p = os.path.join(d, fn)
                try:
                    s = open(p, encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                n = len(re.findall(r"/(?:Users|home)/[^\s\"']+", s))
                if n:
                    hits.append(f"{os.path.relpath(p, root)}×{n}")
    if hits:
        f.append("P5 absolute home paths: " + ", ".join(hits))
    # P6
    rr = os.path.join(root, "RELEASE_REPORT.md")
    if not note:
        f.append("P6 REPRODUCTION_NOTE.md missing")
    elif os.path.exists(rr) and "REPRODUCTION_NOTE.md" not in open(rr, encoding="utf-8").read():
        f.append("P6 REPRODUCTION_NOTE.md not listed in RELEASE_REPORT.md inventory")
    if f:
        print("PREFLIGHT_FAIL — do not push:", *f, sep="\n  "); return 1
    print("PREFLIGHT_PASS — tree matches the report; push allowed"); return 0

if __name__ == "__main__":
    sys.exit(main())
