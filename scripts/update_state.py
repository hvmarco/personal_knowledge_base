#!/usr/bin/env python3
"""Record which pages have been written into processed/zotero_state.json.

The state file is the resume checkpoint for the bulk import: it holds the
last sync timestamp, the list of pages already written, and {zotero_key:
primary_page} for every item that has landed in the vault.

Usage:  python scripts/update_state.py <Page_Name> [<Page_Name> ...]
        python scripts/update_state.py --status
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP = ROOT / "processed" / "Zotero_library_map.csv"
STATE = ROOT / "processed" / "zotero_state.json"
STAMP = "2026-08-25T00:00:00Z"


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"last_sync": None, "source": "raw/Zotero_library.json",
            "pages_written": [], "items": {}}


def main():
    rows = list(csv.DictReader(MAP.open(encoding="utf-8-sig")))
    state = load_state()

    if len(sys.argv) < 2 or sys.argv[1] == "--status":
        done = set(state["pages_written"])
        from collections import Counter
        counts = Counter(r["primary_page"] for r in rows)
        written = sum(n for p, n in counts.items() if p in done)
        print("pages written: {}/{}".format(len(done), len(counts)))
        print("items written: {}/{}".format(written, len(rows)))
        print()
        print("remaining:")
        for p, n in counts.most_common():
            if p not in done:
                print("{:5d}  {}".format(n, p))
        return

    for page in sys.argv[1:]:
        hits = [r for r in rows if r["primary_page"] == page]
        if not hits:
            print("warning: no items map to " + page)
        for r in hits:
            state["items"][r["key"]] = page
        if page not in state["pages_written"]:
            state["pages_written"].append(page)
        print("recorded {} ({} items)".format(page, len(hits)))

    state["last_sync"] = STAMP
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print("total items in state: {}".format(len(state["items"])))


if __name__ == "__main__":
    main()
