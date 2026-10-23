"""Scan all resident release files and ZIP members without exposing matches."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import sys
import unicodedata
import zipfile

TOKEN_POINTS = {
    "P001": [47,85,115,101,114,115],
    "P002": [107,97,110,103,106,117,110,103,109,105,110],
    "P003": [103,97,110,103,106,101,111,110,103,109,105,110],
    "P004": [68,101,115,107,116,111,112],
    "P005": [44060,51064,32,50672,44396],
}
AUTHOR_POINTS = [74,117,110,103,32,77,105,110,32,75,97,110,103]
REGEX_POINTS = {
    "P101": [92,98,40,63,58,97,112,105,91,95,45,93,63,107,101,121,124,97,99,99,101,115,115,91,95,45,93,63,116,111,107,101,110,124,97,117,116,104,91,95,45,93,63,116,111,107,101,110,124,112,97,115,115,119,111,114,100,124,112,97,115,115,119,100,124,115,101,99,114,101,116,124,104,102,91,95,45,93,63,116,111,107,101,110,124,103,105,116,104,117,98,91,95,45,93,63,116,111,107,101,110,41,91,39,34,93,63,92,115,42,91,58,61,93,92,115,42,40,91,39,34,93,41,91,94,39,34,92,114,92,110,93,123,49,44,53,49,50,125,92,49],
    "P109": [92,98,40,63,58,97,112,105,91,95,45,93,63,107,101,121,124,97,99,99,101,115,115,91,95,45,93,63,116,111,107,101,110,124,97,117,116,104,91,95,45,93,63,116,111,107,101,110,124,112,97,115,115,119,111,114,100,124,112,97,115,115,119,100,124,115,101,99,114,101,116,124,104,102,91,95,45,93,63,116,111,107,101,110,124,103,105,116,104,117,98,91,95,45,93,63,116,111,107,101,110,41,91,39,34,93,63,92,115,42,91,58,61,93,92,115,42,91,65,45,90,97,45,122,48,45,57,95,46,47,43,61,45,93,123,49,50,44,50,53,54,125],
    "P102": [92,98,104,102,95,91,65,45,90,97,45,122,48,45,57,93,123,50,48,44,49,50,56,125,92,98],
    "P103": [92,98,115,107,45,40,63,58,112,114,111,106,45,124,115,118,99,97,99,99,116,45,41,63,91,65,45,90,97,45,122,48,45,57,95,45,93,123,50,48,44,50,53,54,125,92,98],
    "P104": [92,98,103,104,91,112,111,117,115,114,93,95,91,65,45,90,97,45,122,48,45,57,93,123,50,48,44,49,50,56,125,92,98],
    "P105": [92,98,103,105,116,104,117,98,95,112,97,116,95,91,65,45,90,97,45,122,48,45,57,95,93,123,50,48,44,50,53,54,125,92,98],
    "P106": [92,98,65,75,73,65,91,65,45,90,48,45,57,93,123,49,54,125,92,98],
    "P107": [92,98,66,101,97,114,101,114,92,115,43,91,65,45,90,97,45,122,48,45,57,46,95,126,43,47,45,93,123,50,48,44,50,53,54,125,61,123,48,44,50,125],
    "P108": [92,98,101,121,74,91,65,45,90,97,45,122,48,45,57,95,45,93,123,56,44,50,53,54,125,92,46,91,65,45,90,97,45,122,48,45,57,95,45,93,123,56,44,50,53,54,125,92,46,91,65,45,90,97,45,122,48,45,57,95,45,93,123,56,44,50,53,54,125,92,98],
}
DEFAULT_MAX_FILE_BYTES = 64 * 1024**2
DEFAULT_MAX_ARCHIVE_BYTES = 256 * 1024**2
UNSUPPORTED_ARCHIVE_SUFFIXES = {
    ".gz", ".bz2", ".xz", ".tar", ".7z", ".rar", ".z", ".zst", ".zstd",
    ".lz4", ".lzma", ".lzip", ".lzo", ".tgz", ".tbz", ".tbz2", ".txz",
    ".tlz", ".tzst", ".cpio", ".ar", ".deb", ".cab", ".zlib", ".deflate",
}


def archive_kind(data):
    """Identify containers from bytes; filenames cannot hide supported ZIPs."""
    if data.startswith((b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")) or zipfile.is_zipfile(io.BytesIO(data)):
        return "zip"
    signatures = (
        (b"\x1f\x8b", "gzip"), (b"BZh", "bzip2"), (b"\xfd7zXZ\x00", "xz"),
        (b"7z\xbc\xaf\x27\x1c", "7z"), (b"Rar!\x1a\x07", "rar"),
        (b"\x28\xb5\x2f\xfd", "zstd"), (b"\x04\x22\x4d\x18", "lz4"),
        (b"\x02\x21\x4c\x18", "lz4"), (b"LZIP", "lzip"),
        (b"\x89LZO\x00\r\n\x1a\n", "lzo"), (b"\x1f\x9d", "compress"),
        (b"\x1f\x1e", "pack"), (b"!<arch>\n", "ar"), (b"MSCF", "cab"),
        (b"070701", "cpio"), (b"070702", "cpio"), (b"070707", "cpio"),
        (b"\x71\xc7", "cpio"), (b"\xc7\x71", "cpio"),
    )
    for signature, kind in signatures:
        if data.startswith(signature):
            return kind
    if len(data) >= 4 and 0x184d2a50 <= int.from_bytes(data[:4], "little") <= 0x184d2a5f:
        return "skippable_compression_frame"
    if len(data) >= 2 and data[0] & 15 == 8 and data[0] >> 4 <= 7 and int.from_bytes(data[:2], "big") % 31 == 0:
        return "zlib"
    if len(data) >= 512:
        header = data[:512]
        if header[257:262] == b"ustar":
            return "tar"
        try:
            checksum = int(header[148:156].strip(b"\x00 "), 8)
        except ValueError:
            checksum = None
        body = header[:148] + b" " * 8 + header[156:]
        if header[:100].strip(b"\x00") and checksum in (
                sum(body), sum(byte if byte < 128 else byte - 256 for byte in body)):
            return "tar"
    return None


def decode(points):
    return "".join(chr(point) for point in points)


def normalize(text):
    return unicodedata.normalize("NFC", text).casefold()


TOKENS = {key: normalize(decode(value)) for key, value in TOKEN_POINTS.items()}
AUTHOR = normalize(decode(AUTHOR_POINTS))
SECRETS = {key: re.compile(decode(value), re.I) for key, value in REGEX_POINTS.items()}
ALLOWED_AUTHOR_BASENAME = re.compile(r"^(?:license|readme|citation)(?:\.[a-z0-9_-]+)?$", re.I)


def occurrences(text, token):
    position = 0
    while True:
        position = text.find(token, position)
        if position < 0:
            return
        yield position
        position += len(token)


def safe_location(location):
    folded = normalize(location)
    if any(token in folded for token in TOKENS.values()) or AUTHOR in folded:
        return "[path-id:" + hashlib.sha256(location.encode()).hexdigest()[:16] + "]"
    if any(pattern.search(location) for pattern in SECRETS.values()):
        return "[path-id:" + hashlib.sha256(location.encode()).hexdigest()[:16] + "]"
    return location


def text_hits(text, location, basename, location_kind="content"):
    folded = normalize(text)
    hits, allowed = [], []
    place = safe_location(location)
    for pattern_id, token in TOKENS.items():
        for offset in occurrences(folded, token):
            hits.append({"pattern_id": pattern_id, "file": place,
                         "location_kind": location_kind,
                         "normalized_character_offset": offset})
    for pattern_id, pattern in SECRETS.items():
        for match in pattern.finditer(text):
            hits.append({"pattern_id": pattern_id, "file": place,
                         "location_kind": location_kind,
                         "character_offset": match.start()})
    for offset in occurrences(folded, AUTHOR):
        hit = {"pattern_id": "P900", "file": place,
               "location_kind": location_kind,
               "normalized_character_offset": offset}
        if location_kind == "content" and ALLOWED_AUTHOR_BASENAME.fullmatch(basename):
            allowed.append(hit)
        else:
            hits.append(hit)
    return hits, allowed


def scan(root, max_file_bytes=DEFAULT_MAX_FILE_BYTES,
         max_archive_bytes=DEFAULT_MAX_ARCHIVE_BYTES):
    result = {"schema_version": 1, "status": None, "files_scanned": 0,
              "archive_members_scanned": 0, "forbidden_hit_count": 0,
              "forbidden_counts_by_pattern": {}, "forbidden_hit_examples": [],
              "forbidden_counts_by_file": {}, "file_sha256": {},
              "allowed_author_hits": [], "blocked": [], "errors": [],
              "matching": "case-insensitive NFC; token text, credential syntax, and names",
              "model_or_experiment_calls": 0, "network_calls": 0}
    def record(text, location, basename, kind="content"):
        hits, allowed = text_hits(text, location, basename, kind)
        result["forbidden_hit_count"] += len(hits)
        for hit in hits:
            key = hit["pattern_id"]
            result["forbidden_counts_by_pattern"][key] = result["forbidden_counts_by_pattern"].get(key, 0) + 1
            counts = result["forbidden_counts_by_file"].setdefault(hit["file"], {})
            counts[key] = counts.get(key, 0) + 1
        remaining = max(0, 100 - len(result["forbidden_hit_examples"]))
        result["forbidden_hit_examples"].extend(hits[:remaining])
        result["allowed_author_hits"].extend(allowed)

    def blocked(location, reason):
        result["blocked"].append({"file": safe_location(location), "reason": reason})

    def scan_archive(data, location):
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                infos = archive.infolist()
                total = sum(info.file_size for info in infos if not info.is_dir())
                if total > max_archive_bytes:
                    blocked(location, "archive_total_size_limit")
                    return
                for info in infos:
                    member = location + "::" + info.filename
                    record(info.filename, member, Path(info.filename).name, "archive_path")
                    if info.is_dir():
                        continue
                    if info.flag_bits & 1:
                        blocked(member, "encrypted_archive_member")
                        continue
                    if info.file_size > max_file_bytes:
                        blocked(member, "archive_member_size_limit")
                        continue
                    if stat.S_ISLNK((info.external_attr >> 16) & 0xffff):
                        blocked(member, "archive_symlink_not_followed")
                    try:
                        content = archive.read(info)
                    except (OSError, RuntimeError, ValueError, zipfile.BadZipFile):
                        blocked(member, "archive_member_read_error")
                        continue
                    record(content.decode("utf-8", errors="replace"), member,
                           Path(info.filename).name)
                    result["archive_members_scanned"] += 1
                    kind = archive_kind(content)
                    if kind is not None or info.filename.lower().endswith(".zip") or Path(info.filename).suffix.lower() in UNSUPPORTED_ARCHIVE_SUFFIXES:
                        blocked(member, "nested_archive_not_expanded")
        except (OSError, ValueError, zipfile.BadZipFile):
            blocked(location, "invalid_archive")

    def visit(directory):
        relative = "." if directory == root else directory.relative_to(root).as_posix()
        try:
            meta = directory.lstat()
        except OSError:
            blocked(relative, "directory_metadata_unavailable")
            return
        if getattr(meta, "st_flags", 0) & 0x40000000:
            blocked(relative, "dataless_directory")
            return
        try:
            with os.scandir(directory) as iterator:
                entries = sorted(iterator, key=lambda entry: entry.name)
        except OSError:
            blocked(relative, "directory_enumeration_unavailable")
            return
        for entry in entries:
            path = Path(entry.path)
            name = path.relative_to(root).as_posix()
            record(name, name, path.name, "path")
            try:
                meta = path.lstat()
            except OSError:
                blocked(name, "metadata_unavailable")
                continue
            if getattr(meta, "st_flags", 0) & 0x40000000:
                blocked(name, "dataless_input")
                continue
            if stat.S_ISLNK(meta.st_mode):
                try:
                    record(os.readlink(path), name, path.name, "symlink_target")
                except OSError:
                    blocked(name, "symlink_target_unavailable")
                blocked(name, "symlink_not_followed")
                continue
            if stat.S_ISDIR(meta.st_mode):
                visit(path)
                continue
            if not stat.S_ISREG(meta.st_mode):
                blocked(name, "special_file_not_read")
                continue
            if meta.st_size > max_file_bytes:
                blocked(name, "file_size_limit")
                continue
            try:
                data = path.read_bytes()
            except OSError:
                blocked(name, "content_unavailable")
                continue
            record(data.decode("utf-8", errors="replace"), name, path.name)
            result["file_sha256"][safe_location(name)] = hashlib.sha256(data).hexdigest()
            result["files_scanned"] += 1
            kind = archive_kind(data)
            if kind == "zip" or path.suffix.lower() == ".zip":
                scan_archive(data, name)
            elif kind is not None or path.suffix.lower() in UNSUPPORTED_ARCHIVE_SUFFIXES:
                blocked(name, "unsupported_archive_not_expanded")

    if not root.exists():
        blocked(".", "missing_root")
    else:
        visit(root)
    if result["forbidden_hit_count"] or result["errors"]:
        result["status"] = "FAIL"
    elif result["blocked"]:
        result["status"] = "BLOCKED"
    else:
        result["status"] = "PASS"
    result["all_resident_files_and_supported_archive_members_scanned"] = not result["blocked"]
    result["forbidden_hit_examples_omitted"] = max(0, result["forbidden_hit_count"] - len(result["forbidden_hit_examples"]))
    return result


def self_test():
    assert text_hits(decode(TOKEN_POINTS["P001"]), "x", "x")[0]
    assert text_hits(decode(TOKEN_POINTS["P004"]).upper(), "x", "x")[0]
    decomposed = unicodedata.normalize("NFD", decode(TOKEN_POINTS["P005"]))
    assert text_hits(decomposed, "x", "x")[0]
    author = decode(AUTHOR_POINTS)
    assert not text_hits(author, "README.md", "README.md")[0]
    assert len(text_hits(author, "README.md", "README.md")[1]) == 1
    assert text_hits(author, "metadata.json", "metadata.json")[0]
    sample = decode([104,102,95]) + "a" * 32
    assert text_hits(sample, "x", "x")[0]
    assert sample not in json.dumps(text_hits(sample, "x", "x"))
    assert not text_hits("public data with numeric values", "x", "x")[0]
    for points in ([67,108,97,117,100,101], [67,111,100,101,120]):
        label = decode(points)
        assert not text_hits(label, "sample.txt", "sample.txt")[0]
        assert not text_hits(label, label + ".txt", label + ".txt", "path")[0]
        assert safe_location(label + ".txt") == label + ".txt"
    own = Path(__file__).read_text()
    assert not text_hits(own, Path(__file__).name, Path(__file__).name)[0]
    import bz2
    import gzip
    import lzma
    import tarfile
    import tempfile
    import zlib
    payload = decode(TOKEN_POINTS["P001"]).encode()
    def make_zip(content):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("payload.txt", content)
        return stream.getvalue()
    def scan_one(content, basename="container.bin"):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / basename).write_bytes(content)
            return scan(root)
    renamed = scan_one(make_zip(payload))
    assert renamed["status"] == "FAIL" and renamed["archive_members_scanned"] == 1
    assert renamed["forbidden_counts_by_pattern"]["P001"] >= 1
    prefixed = scan_one(b"executable-prefix" + make_zip(payload))
    assert prefixed["status"] == "FAIL" and prefixed["archive_members_scanned"] == 1
    nested = scan_one(make_zip(make_zip(payload)))
    assert nested["status"] != "PASS" and any(x["reason"] == "nested_archive_not_expanded" for x in nested["blocked"])
    assert not nested["all_resident_files_and_supported_archive_members_scanned"]
    unsupported = [gzip.compress(payload), bz2.compress(payload), lzma.compress(payload), zlib.compress(payload),
                   b"7z\xbc\xaf\x27\x1c", b"Rar!\x1a\x07\x00", b"\x28\xb5\x2f\xfd",
                   b"\x04\x22\x4d\x18", b"LZIP", b"\x89LZO\x00\r\n\x1a\n",
                   b"\x1f\x9d", b"!<arch>\n", b"MSCF", b"070701"]
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w", format=tarfile.USTAR_FORMAT) as archive:
        info = tarfile.TarInfo("payload.txt")
        info.size = len(payload)
        archive.addfile(info, io.BytesIO(payload))
    unsupported.append(stream.getvalue())
    for content in unsupported:
        receipt = scan_one(content)
        assert receipt["status"] != "PASS"
        assert any(x["reason"] == "unsupported_archive_not_expanded" for x in receipt["blocked"])
        nested = scan_one(make_zip(content))
        assert nested["status"] != "PASS" and any(x["reason"] == "nested_archive_not_expanded" for x in nested["blocked"])
    truncated = scan_one(b"PK\x03\x04")
    assert truncated["status"] == "BLOCKED" and truncated["blocked"][0]["reason"] == "invalid_archive"
    assert scan_one(b"uncompressed public text")["status"] == "PASS"
    print("SELF_TEST PASS 47")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--max-file-bytes", type=int, default=DEFAULT_MAX_FILE_BYTES)
    parser.add_argument("--max-archive-bytes", type=int, default=DEFAULT_MAX_ARCHIVE_BYTES)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    if args.max_file_bytes <= 0 or args.max_archive_bytes <= 0:
        parser.error("size limits must be positive")
    result = scan(args.root.resolve(), args.max_file_bytes, args.max_archive_bytes)
    encoded = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    print(encoded, end="")
    if args.output:
        args.output.write_text(encoded)
    return {"PASS": 0, "FAIL": 1, "BLOCKED": 2}[result["status"]]


if __name__ == "__main__":
    sys.exit(main())

