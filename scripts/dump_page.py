#!/usr/bin/env python3
"""Dump the items assigned to one page, newest first, for note writing.

Usage:  python scripts/dump_page.py <Page_Name> [start] [count]
        python scripts/dump_page.py --list
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP = ROOT / "processed" / "Zotero_library_map.csv"
SRC = ROOT / "raw" / "Zotero_library.json"

ABSTRACT_CHARS = 340


def load():
    rows = list(csv.DictReader(MAP.open(encoding="utf-8-sig")))
    data = json.loads(SRC.read_text(encoding="utf-8"))
    by_key = {it.get("key"): it for it in data["items"] if it.get("key")}
    return rows, by_key


def main():
    rows, by_key = load()
    if len(sys.argv) < 2 or sys.argv[1] == "--list":
        from collections import Counter
        for page, n in Counter(r["primary_page"] for r in rows).most_common():
            print("{:5d}  {}".format(n, page))
        return

    page = sys.argv[1]
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 10**6

    sel = [r for r in rows if r["primary_page"] == page]
    sel.sort(key=lambda r: (r["year"] or "0000"), reverse=True)
    total = len(sel)
    sel = sel[start:start + count]

    print("# {}  ({}-{} of {})".format(page, start + 1, start + len(sel), total))
    for r in sel:
        it = by_key.get(r["key"], {})
        abstract = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", it.get("abstractNote") or "")).strip()
        if len(abstract) > ABSTRACT_CHARS:
            abstract = abstract[:ABSTRACT_CHARS] + "…"
        notes = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", n.get("note", "")))[:200]
                 for n in (it.get("notes") or [])]
        auto = [t["tag"] for t in it.get("tags", []) if t.get("type") == 1][:8]
        print()
        print("## {} | {} | {}".format(r["key"], r["year"] or "n.d.", r["item_type"]))
        print("T: " + r["title"])
        print("A: {} | P: {}".format(r["authors"] or "—", r["publication"] or "—"))
        print("L: " + (r["link"] or "—"))
        if r["candidate"]:
            print("CANDIDATE: " + r["candidate"])
        if r["related_pages"]:
            print("R: " + r["related_pages"])
        if r["tags"]:
            print("G: " + r["tags"])
        if auto:
            print("K: " + ", ".join(auto))
        print("S: " + (abstract if abstract else "(no abstract)"))
        for n in notes:
            print("N: " + n)


if __name__ == "__main__":
    main()
