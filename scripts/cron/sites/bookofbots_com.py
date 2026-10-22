#!/usr/bin/env python3
"""Per-site monitor: bookofbots.com.
Social network for AI agents (agents write via API, humans watch). Homepage 200. /llms.txt 301-redirects to https://absurdtools.com/llms.txt (site rebrand/moved); urllib follows redirects so the poll still lands.
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    bookofbots_com.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "bookofbots_com",
    "label": "bookofbots.com",
    "urls": ['https://bookofbots.com/', 'https://bookofbots.com/llms.txt'],
    "kind": "listing-hash",
    "notes": "Social network for AI agents (agents write via API, humans watch). Homepage 200. /llms.txt 301-redirects to https://absurdtools.com/llms.txt (site rebrand/moved); urllib follows redirects so the poll still lands.",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
