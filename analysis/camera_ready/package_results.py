"""Package the local commit, portable execution logs, checks and file inventory."""
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

BASE = Path(__file__).resolve().parents[3]
REPO, OUT, RUN = BASE / "repo", BASE / "out", BASE / "run"
TARGET = OUT / "PAIEC_v21_results.tar.gz"
UTC = dt.timezone.utc

def git(*args, **options):
    return subprocess.check_output(["git", *args], cwd=REPO, **options)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def save_json(name, doc):
    (OUT / name).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")

def verify_tree(patch, commit):
    with tempfile.TemporaryDirectory() as temp:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(temp)/"index")}
        git("read-tree", "main", env=env)
        git("apply", "--cached", str(patch), env=env)
        return git("write-tree", env=env).strip() == git("rev-parse", commit+"^{tree}").strip()

def collect():
    commit = git("rev-parse", "HEAD").decode().strip()
    patch = OUT / "camera-ready.patch"
    patch.write_bytes(git("format-patch", "--stdout", "--binary", "-1"))
    assert git("rev-parse", "--abbrev-ref", "HEAD").strip() == b"camera-ready"
    assert verify_tree(patch, commit)
    before = {}
    for line in (OUT / "frozen_before.sha256").read_text().splitlines():
        sha, path = line.split(maxsplit=1)
        before[path] = sha
    frozen = []
    for name, prev in before.items():
        actual = digest((REPO/name).read_bytes())
        main = digest(git("show", "main:"+name))
        frozen.append(dict(path=name, before=prev, after=actual, main=main,
                           unchanged=prev==actual==main))
    assert all(r["unchanged"] for r in frozen)
    changed = git("diff", "--name-only", "main..HEAD").decode().splitlines()
    allowed = ("analysis/camera_ready/", "verification/evidence/camera_ready/")
    assert changed and all(p.startswith(allowed) for p in changed)
    status = git("status", "--porcelain").decode()
    assert not status, status
    for name in changed:
        assert os.fsencode(str(Path.home().parent) + "/") not in (REPO/name).read_bytes(), name
    save_json("T7.json",dict(commit=commit, base=git("rev-parse","main").decode().strip(),
              branch="camera-ready", frozen=frozen, git_status_porcelain=status,
              git_diff_stat=git("diff","--stat","main..HEAD").decode(), files=changed,
              paths_outside_scope=[],home_path_matches=[], patch_rebuilds_commit_tree=True))
    discovered={p.name:p for p in OUT.glob("discovery_*") if p.is_file()}
    for n in ("missing_resident.json",):
        discovered[n]=OUT/n
    return {**{"out/discovery/"+name:p for name,p in discovered.items()},
            **{p: REPO/p for p in changed},
            **{"out/"+n: OUT/n for n in (
                "T0.json", "T1_stages.json", "T1_partial_hf_cache.json", "T1_offloaded.json",
                "T7.json", "frozen_before.sha256", "camera-ready.patch", "REPORT.md")},
            **{"out/logs/"+p.name:p for p in (OUT/"logs").glob("*") if p.is_file()},
            **{"out/verification/"+n:RUN/n for n in (
                "data_receipt.json", "identifier_sources.json", "artifacts/training_receipt.json", "artifacts/prepare_summary.json",
                "eval_split2/results.json", "compare_split2.json", "compare_split2.txt")}}

def pack():
    files=collect()
    # Report is outside the commit so it can name the exact commit and its QA.
    subprocess.run(["python3", str(Path(__file__).with_name("render_report.py"))],check=True)
    inventory=[]
    with tarfile.open(TARGET.with_suffix(".tmp"), "w:gz", compresslevel=7) as arc:
        def add(name,data,seconds,perms):
            meta=tarfile.TarInfo(name)
            meta.size,meta.mtime,meta.mode=len(data),int(seconds),perms
            arc.addfile(meta,io.BytesIO(data))
        for name,path in sorted(files.items()):
            data=path.read_bytes()
            if name.startswith("out/logs/"):
                data=data.replace(os.fsencode(Path.home()),b"$PAIEC_SOURCE_ROOT")
            assert os.fsencode(str(Path.home().parent) + "/") not in data, name
            epoch=path.stat().st_mtime
            add(name,data,epoch,0o755 if path.stat().st_mode & 0o111 else 0o644)
            inventory.append(dict(path=name,sha256=digest(data),bytes=len(data),
                                  mtime=dt.datetime.fromtimestamp(epoch,UTC).isoformat()))
        save_json("FILES.json",inventory)
        add("out/FILES.json",(OUT/"FILES.json").read_bytes(),(OUT/"FILES.json").stat().st_mtime,0o644)
    TARGET.with_suffix(".tmp").replace(TARGET)
    assert TARGET.stat().st_size < 25_000_000
    with tarfile.open(TARGET,"r:gz") as arc:
        manifest=json.load(arc.extractfile("out/FILES.json"))
        assert set(arc.getnames())=={x["path"] for x in manifest}|{"out/FILES.json"}
        for record in manifest:
            b=arc.extractfile(record["path"]).read()
            assert len(b)==record["bytes"] and digest(b)==record["sha256"]
    (OUT/"SHA256SUMS.txt").write_text(digest(TARGET.read_bytes())+"  "+TARGET.name+"\n"+
                                    digest((OUT/"FILES.json").read_bytes())+"  FILES.json\n")
    print(TARGET.stat().st_size, digest(TARGET.read_bytes()))
if __name__=="__main__":
    pack()
