#!/usr/bin/env python3
"""Parse the Netscape bookmark export into a flat table.

Emits processed/bookmarks_raw.csv with one row per link:
folder path, title, url, add date, and the normalised url used for dedup.

Usage:  python scripts/parse_bookmarks.py [raw/bookmarks_8_25_26.html]
"""
import csv
import datetime
import html
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_IN = ROOT / "raw" / "bookmarks_8_25_26.html"
OUT = ROOT / "processed" / "bookmarks_raw.csv"

H3_RE = re.compile(r"<H3[^>]*>(.*?)</H3>", re.I | re.S)
A_RE = re.compile(r'<A\s+HREF="([^"]*)"([^>]*)>(.*?)</A>', re.I | re.S)
ADD_RE = re.compile(r'ADD_DATE="(\d+)"', re.I)
TRACKING = re.compile(
    r"^(utm_[a-z]+|fbclid|gclid|ref|source|si|tab|ab_channel|t|index|feature|app|pp|"
    r"redirectedfrom[a-z]*)$", re.I)


def normalise(url):
    """Reduce a url to the resource it points at, for duplicate detection.

    Drops the scheme, www, trailing slash, index.html, the .html suffix,
    tracking and UI parameters, and the fragment -- except the "#!" and "#/"
    fragments that single-page apps use as the actual address.  YouTube links
    collapse to the video or playlist id.
    """
    u = re.sub(r"^https?://", "", url.strip(), flags=re.I)
    u = re.sub(r"^www\.", "", u, flags=re.I)

    if re.match(r"(m\.)?youtube\.com/watch", u, flags=re.I) or u.lower().startswith("youtu.be/"):
        vid = re.search(r"[?&]v=([\w-]+)", u) or re.search(r"youtu\.be/([\w-]+)", u)
        if vid:
            return "youtube.com/watch?v=" + vid.group(1).lower()
    if re.match(r"(m\.)?youtube\.com/playlist", u, flags=re.I):
        lst = re.search(r"[?&]list=([\w-]+)", u)
        if lst:
            return "youtube.com/playlist?list=" + lst.group(1).lower()

    if "#" in u:
        base, frag = u.split("#", 1)
        u = base if not frag.startswith(("!", "/")) else base + "#" + frag
    if "?" in u:
        base, query = u.split("?", 1)
        kept = [p for p in query.split("&")
                if p and not TRACKING.match(p.split("=", 1)[0])]
        u = base + ("?" + "&".join(kept) if kept else "")
    u = re.sub(r"/index\.html?$", "/", u, flags=re.I)
    u = re.sub(r"\.html?$", "", u, flags=re.I)
    return u.rstrip("/").lower()


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_IN
    text = io.open(src, encoding="utf-8", errors="replace").read()

    rows = []
    stack = []
    depth = 0
    for line in text.split("\n"):
        stripped = line.strip()
        up = stripped.upper()
        h3 = H3_RE.search(stripped)
        if h3:
            name = html.unescape(re.sub(r"<[^>]*>", "", h3.group(1))).strip()
            stack = stack[:depth] + [name]
            continue
        if up.startswith("<DL>"):
            depth = len(stack)
            continue
        if up.startswith("</DL>"):
            depth = max(0, depth - 1)
            stack = stack[:depth]
            continue
        a = A_RE.search(stripped)
        if a:
            url = html.unescape(a.group(1)).strip()
            title = html.unescape(re.sub(r"<[^>]*>", "", a.group(3))).strip()
            add = ADD_RE.search(a.group(2))
            when = ""
            if add:
                try:
                    when = datetime.datetime.utcfromtimestamp(
                        int(add.group(1))).strftime("%Y-%m-%d")
                except (ValueError, OSError):
                    when = ""
            rows.append({
                "folder": "/".join(stack),
                "title": title,
                "url": url,
                "added": when,
                "norm": normalise(url),
            })

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["folder", "title", "url", "added", "norm"])
        w.writeheader()
        w.writerows(rows)
    print("wrote {} ({} links)".format(OUT, len(rows)))

    from collections import Counter
    for folder, n in Counter(r["folder"] for r in rows).most_common():
        print("{:4d}  {}".format(n, folder))
    dupes = [u for u, n in Counter(r["norm"] for r in rows).items() if n > 1]
    print("duplicate urls: {}".format(len(dupes)))


if __name__ == "__main__":
    main()
