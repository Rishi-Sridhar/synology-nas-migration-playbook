#!/usr/bin/env python3
"""Compare two directory trees without modifying either tree."""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path


def regular_files(root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for base, directories, names in os.walk(root, followlinks=False):
        directories[:] = [d for d in directories if not (Path(base) / d).is_symlink()]
        for name in names:
            path = Path(base) / name
            if path.is_symlink():
                raise ValueError(f"symlink is outside verification policy: {path}")
            if path.is_file():
                files[path.relative_to(root).as_posix()] = path
    return files


def digest(path: Path, algorithm: str) -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--hash", choices=sorted(hashlib.algorithms_guaranteed))
    args = parser.parse_args()

    source = args.source.resolve(strict=True)
    destination = args.destination.resolve(strict=True)
    if not source.is_dir() or not destination.is_dir():
        parser.error("source and destination must be directories")
    if source == destination or source in destination.parents or destination in source.parents:
        parser.error("source and destination must be separate, non-nested trees")

    try:
        source_files = regular_files(source)
        destination_files = regular_files(destination)
    except ValueError as error:
        print(f"BLOCK: {error}", file=sys.stderr)
        return 2

    failed = False
    for relative in sorted(source_files.keys() | destination_files.keys()):
        left = source_files.get(relative)
        right = destination_files.get(relative)
        if left is None or right is None:
            print(f"MISSING: {relative} ({'source' if left is None else 'destination'})")
            failed = True
            continue
        if left.stat().st_size != right.stat().st_size:
            print(f"SIZE_MISMATCH: {relative}")
            failed = True
            continue
        if args.hash and digest(left, args.hash) != digest(right, args.hash):
            print(f"HASH_MISMATCH: {relative}")
            failed = True

    print(f"SOURCE_FILES={len(source_files)}")
    print(f"DESTINATION_FILES={len(destination_files)}")
    print(f"VERIFY_COPY={'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
