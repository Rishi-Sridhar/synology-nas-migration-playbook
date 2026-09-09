#!/usr/bin/env python3
"""Validate a private CSV path map for obvious ambiguity."""

from __future__ import annotations

import argparse
import csv
import os
import re
from pathlib import Path
from pathlib import PurePath

REQUIRED = ("purpose", "old_path", "new_path", "container_path")
PLACEHOLDER = re.compile(r"<[^>]+>")


def normalized(value: str) -> str:
    return os.path.normcase(os.path.normpath(value.strip()))


def overlaps(left: str, right: str) -> bool:
    a, b = PurePath(left), PurePath(right)
    return a == b or a in b.parents or b in a.parents


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args()
    with args.csv_file.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = tuple(reader.fieldnames or ())
        rows = list(reader)
    missing = [field for field in REQUIRED if field not in fields]
    problems: list[str] = []
    if missing:
        problems.append("missing columns: " + ", ".join(missing))
    else:
        for number, row in enumerate(rows, start=2):
            for field in REQUIRED:
                value = (row.get(field) or "").strip()
                if not value:
                    problems.append(f"row {number}: empty {field}")
                elif PLACEHOLDER.search(value):
                    problems.append(f"row {number}: unresolved placeholder in {field}")
            for field in ("old_path", "new_path", "container_path"):
                value = (row.get(field) or "").strip()
                if value and not (os.path.isabs(value) or value.startswith("/")):
                    problems.append(f"row {number}: {field} is not absolute")

        new_paths = [(index + 2, normalized(row["new_path"])) for index, row in enumerate(rows)]
        for index, (left_number, left) in enumerate(new_paths):
            for right_number, right in new_paths[index + 1 :]:
                if overlaps(left, right):
                    problems.append(f"rows {left_number}/{right_number}: overlapping new paths")

    for problem in problems:
        print(f"BLOCK: {problem}")
    print(f"ROWS={len(rows)}")
    print(f"PATH_MAPPING_AUDIT={'FAIL' if problems else 'PASS'}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
