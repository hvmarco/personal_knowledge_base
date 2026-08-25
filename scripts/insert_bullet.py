#!/usr/bin/env python3
"""Insert a bullet into a topic page at the right place in the year order.

Bulk-imported references are sorted by publication year, newest first, so a
late addition has to be slotted in rather than appended.  The year of every
bullet already on the page is looked up from the classification map by its
Zotero key.

Usage:  python scripts/insert_bullet.py <Page_Name> <KEY> < bullet.txt
        (the bullet text, one line, is read from stdin)

The bullet is placed before the first bullet with a strictly smaller year;
items with no year go last.  Insertion stops at the first "## Candidate:"
heading, so candidate sections are never disturbed.
"""
import csv
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP = ROOT / "processed" / "Zotero_library_map.csv"
KEY_RE = re.compile(r"zotero://select/library/items/([A-Z0-9]{8})")


def year_of(row):
    try:
        return int(row["year"])
    except (TypeError, ValueError):
        return -1


def main():
    page, key = sys.argv[1], sys.argv[2]
    bullet = sys.stdin.read().strip("\n")
    if not bullet.startswith("- "):
        sys.exit("bullet must start with '- '")

    by_key = {r["key"]: r for r in csv.DictReader(MAP.open(encoding="utf-8-sig"))}
    if key not in by_key:
        sys.exit("key {} not in the map".format(key))
    year = year_of(by_key[key])

    path = ROOT / "notes" / (page + ".md")
    lines = io.open(path, encoding="utf-8").read().split("\n")

    start = next(i for i, l in enumerate(lines) if l.strip() == "## Notes") + 1
    at = None
    i = start
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            break
        if line.startswith("- "):
            keys = KEY_RE.findall(line)
            other = year_of(by_key[keys[0]]) if keys and keys[0] in by_key else 10000
            if year > other:
                at = i
                break
        i += 1
    if at is None:
        at = i
        while at > start and not lines[at - 1].strip():
            at -= 1

    lines.insert(at, bullet)
    io.open(path, "w", encoding="utf-8").write("\n".join(lines))
    print("inserted {} into {} at line {}".format(key, page, at + 1))


if __name__ == "__main__":
    main()
