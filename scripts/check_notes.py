#!/usr/bin/env python3
"""Verify written notes against the classification map.

Catches the failure modes that matter when writing 1400 bullets by hand:
  * a link that is not the one Zotero holds for that key (fabricated or pasted
    from the wrong row)
  * a bullet whose Zotero key is not in the map at all
  * an item placed on a page the map does not assign it to
  * items the map assigns to a written page that never got a bullet
  * duplicate bullets for the same key
  * wiki-links pointing at pages that do not exist

Usage:  python scripts/check_notes.py
"""
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "notes"
MAP = ROOT / "processed" / "Zotero_library_map.csv"

KEY_RE = re.compile(r"zotero://select/library/items/([A-Z0-9]{8})")
LINK_RE = re.compile(r"\*\*\[[^\]]*\]\(([^)]+)\)\*\*")
WIKI_RE = re.compile(r"\[\[([^\]|#]+)")


def main():
    rows = list(csv.DictReader(MAP.open(encoding="utf-8-sig")))
    by_key = {r["key"]: r for r in rows}
    assigned = defaultdict(set)
    for r in rows:
        assigned[r["primary_page"]].add(r["key"])

    problems = []
    seen_keys = defaultdict(list)
    pages = {p.stem for p in NOTES.glob("*.md")}
    # a wiki-link to a page the import will still create is fine; only flag
    # targets that are neither on disk nor planned anywhere
    planned = set(assigned)
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from page_meta import PAGES as META_PAGES
        planned |= set(META_PAGES)
    except Exception:
        pass
    known = pages | planned
    written_pages = set()

    for path in sorted(NOTES.glob("*.md")):
        page = path.stem
        text = path.read_text(encoding="utf-8")
        body = text.split("## Notes", 1)[1] if "## Notes" in text else ""
        page_has_notes = False

        for line in body.splitlines():
            if not line.startswith("- "):
                continue
            keys = KEY_RE.findall(line)
            if not keys:
                continue
            page_has_notes = True
            for key in keys:
                seen_keys[key].append(page)
                row = by_key.get(key)
                if row is None:
                    problems.append("{}: key {} not in map".format(page, key))
                    continue
                if row["primary_page"] != page:
                    problems.append("{}: key {} is mapped to {}".format(
                        page, key, row["primary_page"]))
            # link check: the bolded title link must match the mapped link
            m = LINK_RE.search(line)
            if m and keys:
                expected = (by_key.get(keys[0]) or {}).get("link", "")
                got = m.group(1)
                if expected and got != expected:
                    problems.append("{}: key {} link mismatch\n     map: {}\n     note: {}".format(
                        page, keys[0], expected, got))
                if not expected:
                    problems.append("{}: key {} has no link in the map but the note links to {}".format(
                        page, keys[0], got))
        if page_has_notes:
            written_pages.add(page)

        for target in set(WIKI_RE.findall(text)):
            if target.strip() not in known:
                problems.append("{}: wiki-link to unknown page [[{}]]".format(page, target.strip()))

    for key, where in seen_keys.items():
        if len(where) > 1:
            problems.append("key {} appears on {}".format(key, ", ".join(where)))

    for page in sorted(written_pages):
        missing = assigned.get(page, set()) - set(seen_keys)
        if missing:
            problems.append("{}: {} mapped items not written ({})".format(
                page, len(missing), ", ".join(sorted(missing)[:8])))

    print("pages with notes: {}   bullets checked: {}".format(
        len(written_pages), sum(len(v) for v in seen_keys.values())))
    if problems:
        print("\n{} problem(s):".format(len(problems)))
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print("no problems found")


if __name__ == "__main__":
    main()
