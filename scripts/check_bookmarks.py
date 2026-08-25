#!/usr/bin/env python3
"""Verify the bookmark bullets against processed/bookmarks_map.csv.

Catches:
  * a bookmark written on a page other than the one it is mapped to
  * a mapped bookmark that was never written (on a page already done)
  * a link in a bookmark bullet that is not in the map (fabricated or mistyped)
  * the same bookmark written twice
  * a bookmark bullet with no #type/ tag (CLAUDE.md requires one)

Exit code 1 if anything is wrong.
"""
import csv
import io
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "notes"
MAP = ROOT / "processed" / "bookmarks_map.csv"

LINK_RE = re.compile(r"\[[^\]]*\]\(((?:[^()]|\([^()]*\))+)\)")
ZOTERO_RE = re.compile(r"zotero://select/library/items/")
TYPE_RE = re.compile(r"#type/[a-z]+")

# links that were ingested from raw/New_Notes.md before the bookmark import
# and are therefore not in the bookmark map
EXEMPT = {
    "https://github.com/montimaj/agribound",
    "https://zenodo.org/records/18647054",
    "https://cloudnativegeo.org/blog/2026/02/the-technical-debt-of-earth-embedding-products/",
    "https://www.linkedin.com/feed/update/urn:li:activity:7478690057026207745/",
}


def main():
    rows = list(csv.DictReader(MAP.open(encoding="utf-8")))
    by_url = {r["url"]: r for r in rows}
    problems = []
    written = defaultdict(list)
    pages_with_bookmarks = set()

    for path in sorted(NOTES.glob("*.md")):
        page = path.stem
        if page in ("index", "log"):
            continue
        for line in io.open(path, encoding="utf-8"):
            if not line.startswith("- ") or ZOTERO_RE.search(line):
                continue
            urls = [u for u in LINK_RE.findall(line) if u.startswith("http")]
            hits = [u for u in urls if u in by_url]
            if not hits:
                # a bullet with an unknown external link: only a problem if it
                # looks like a bookmark bullet (has a #type/ tag)
                if urls and TYPE_RE.search(line) and urls[0] not in EXEMPT:
                    problems.append("{}: link not in the bookmark map: {}".format(page, urls[0]))
                continue
            url = hits[0]
            pages_with_bookmarks.add(page)
            written[url].append(page)
            if by_url[url]["primary_page"] != page:
                problems.append("{}: {} is mapped to {}".format(
                    page, url[:70], by_url[url]["primary_page"]))
            if not TYPE_RE.search(line):
                problems.append("{}: bookmark bullet without a #type/ tag: {}".format(page, url[:70]))

    for url, pages in written.items():
        if len(pages) > 1:
            problems.append("{} written on {}".format(url[:60], ", ".join(pages)))

    for row in rows:
        if row["primary_page"] in pages_with_bookmarks and row["url"] not in written:
            problems.append("{}: mapped bookmark not written: {} ({})".format(
                row["primary_page"], row["title"][:40], row["url"][:60]))

    print("bookmark bullets checked: {}   pages: {}".format(
        len(written), len(pages_with_bookmarks)))
    if problems:
        print("\n{} problem(s):".format(len(problems)))
        for p in problems[:60]:
            print("  - " + p)
        sys.exit(1)
    print("no problems found")


if __name__ == "__main__":
    main()
