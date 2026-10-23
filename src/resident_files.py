"""Check local ancestors before traversing or reading potentially offloaded files."""
import os
from pathlib import Path
import stat


def local_path(value, missing_ok=False):
    path = Path(os.path.abspath(value))
    redirects = 0
    while True:
        current = Path(path.anchor)
        parts = path.parts[1:]
        for index, part in enumerate(parts):
            current = current / part
            try:
                info = current.lstat()
            except FileNotFoundError:
                if missing_ok:
                    return current.joinpath(*parts[index + 1:])
                raise ValueError('Required local path is missing') from None
            if getattr(info, 'st_flags', 0) & 0x40000000:
                raise ValueError('Required local path is offloaded; automatic restoration is disabled')
            if stat.S_ISLNK(info.st_mode):
                redirects += 1
                if redirects > 40:
                    raise ValueError('Too many local symbolic link redirects')
                target = Path(os.readlink(current))
                if not target.is_absolute():
                    target = current.parent / target
                path = Path(os.path.abspath(target.joinpath(*parts[index + 1:])))
                break
            if index < len(parts) - 1 and not stat.S_ISDIR(info.st_mode):
                raise ValueError('Required local parent is not a directory')
        else:
            return path


def local_file(value):
    path = local_path(value)
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError('Expected a regular local file')
    return path
