#!/usr/bin/env python3
"""Inspect only the current run's private intent directory; UNKNOWN never permits deletion."""
import os
from pathlib import Path
import stat
import sys

def inspect(directory):
    path = Path(directory)
    if not path.is_absolute():
        raise ValueError('private absolute directory required')
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    descriptor = os.open(path, flags)
    try:
        actual = os.fstat(descriptor)
        if actual.st_uid != os.getuid() or stat.S_IMODE(actual.st_mode) != 0o700:
            raise ValueError('private owned directory required')
        names = os.listdir(descriptor)
        current = os.stat(path, follow_symlinks=False)
        if not stat.S_ISDIR(current.st_mode) or (actual.st_dev, actual.st_ino) != (current.st_dev, current.st_ino):
            raise ValueError('directory identity changed')
        return any(name.endswith('.json') for name in names)
    finally:
        os.close(descriptor)

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('one directory required')
        retained = inspect(sys.argv[1])
    except (OSError, ValueError):
        print('RECONCILIATION_STATUS:UNKNOWN', file=sys.stderr)
        raise SystemExit(2)
    print('RECONCILIATION_STATUS:' + ('RETAINED' if retained else 'CLEAN'))
    raise SystemExit(1 if retained else 0)
