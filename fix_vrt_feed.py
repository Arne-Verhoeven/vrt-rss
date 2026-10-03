#!/usr/bin/env python3
"""
Haalt de officiële VRT NWS-feed op en verwijdert '.rss.xml' uit de artikellinks,
zodat ze naar de echte artikelpagina wijzen.

Gebruik:
    pip install requests
    python fix_vrt_feed.py -o public/vrt.xml
"""
import argparse
import re
import sys

import requests

SOURCE = "https://www.vrt.be/vrtnws/nl.rss.articles.xml"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; personal-rss-script/1.0)"}

# Elke VRT NWS-URL die op .rss.xml eindigt (en niet de feed zelf, die eindigt op .rss.articles.xml)
PATTERN = re.compile(r"(https?://www\.vrt\.be/vrtnws/[^\s\"'<>]*?)\.rss\.xml(?=[\s\"'<>?#]|$)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", default="vrt.xml")
    ap.add_argument("--url", default=SOURCE)
    args = ap.parse_args()

    r = requests.get(args.url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    xml = r.content.decode(r.encoding or "utf-8", errors="replace")

    fixed, n = PATTERN.subn(r"\1", xml)
    print(f"{n} links gecorrigeerd")
    if n == 0:
        print("Waarschuwing: geen '.rss.xml'-links gevonden, feed ongewijzigd doorgegeven.", file=sys.stderr)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(fixed)


if __name__ == "__main__":
    main()
