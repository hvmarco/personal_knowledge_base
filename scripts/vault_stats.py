#!/usr/bin/env python3
"""End-of-run maintenance report for the vault.

Reports bullets per page, notes per candidate, pages over the ~80-bullet split
threshold, pages with no inbound links, unresolved wiki-links, and counts of
#needs-review / #needs-topic. Run after every ingest or sync.
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

NOTES = Path(__file__).resolve().parent.parent / "notes"
SPLIT_THRESHOLD = 80
PROMOTE_THRESHOLD = 5

WIKILINK = re.compile(r"\[\[([^\]|#]+)")
CANDIDATE = re.compile(r"^##\s+Candidate:\s*(.+?)\s*$", re.M)
BULLET = re.compile(r"^- ", re.M)


def main():
    pages = sorted(NOTES.glob("*.md"))
    if not pages:
        sys.exit("no pages found in " + str(NOTES))

    bullets, inbound, candidates = {}, defaultdict(set), {}
    tags = Counter()
    outbound = {}
    is_moc = {}

    for p in pages:
        text = p.read_text(encoding="utf-8")
        name = p.stem
        body = text.split("## Notes", 1)[1] if "## Notes" in text else ""
        bullets[name] = len(BULLET.findall(body))
        is_moc[name] = "moc" in (re.search(r"^tags:.*$", text, re.M) or
                                 type("", (), {"group": lambda s, n=0: ""})()).group(0)
        outbound[name] = {t.strip() for t in WIKILINK.findall(text)}
        for target in outbound[name]:
            if target != name:
                inbound[target].add(name)
        for m in CANDIDATE.finditer(text):
            section = text[m.end():].split("\n## ", 1)[0]
            candidates[(name, m.group(1))] = len(BULLET.findall(section))
        tags["#needs-review"] += text.count("#needs-review")
        tags["#needs-topic"] += text.count("#needs-topic")
        tags["#removed-from-zotero"] += text.count("#removed-from-zotero")

    existing = set(bullets)
    total = sum(bullets.values())

    print("pages: {}   bullets: {}".format(len(pages), total))
    print()

    print("--- bullets per page (top 25) ---")
    for name, n in sorted(bullets.items(), key=lambda kv: -kv[1])[:25]:
        flag = "  <-- over {}".format(SPLIT_THRESHOLD) if n > SPLIT_THRESHOLD else ""
        print("{:5d}  {}{}".format(n, name, flag))
    print()

    over = [n for n, c in bullets.items() if c > SPLIT_THRESHOLD]
    print("--- pages over {} bullets (propose a split) ---".format(SPLIT_THRESHOLD))
    print("  " + (", ".join(sorted(over)) if over else "none"))
    print()

    print("--- candidates ---")
    if candidates:
        for (page, cand), n in sorted(candidates.items(), key=lambda kv: -kv[1]):
            mark = "  <-- PROMOTE" if n >= PROMOTE_THRESHOLD else ""
            print("{:5d}  {} (on {}){}".format(n, cand, page, mark))
    else:
        print("  none")
    print()

    orphans = sorted(n for n in existing
                     if not inbound.get(n) and n not in ("index", "log"))
    print("--- pages with no inbound links ---")
    print("  " + (", ".join(orphans) if orphans else "none"))
    print()

    unresolved = Counter()
    for name, targets in outbound.items():
        for t in targets:
            if t not in existing:
                unresolved[t] += 1
    print("--- unresolved wiki-links ({} distinct) ---".format(len(unresolved)))
    for t, n in unresolved.most_common(40):
        print("{:5d}  {}".format(n, t))
    if len(unresolved) > 40:
        print("  ... and {} more".format(len(unresolved) - 40))
    print()

    print("--- needs attention ---")
    for k, v in tags.items():
        print("{:5d}  {}".format(v, k))


if __name__ == "__main__":
    main()
