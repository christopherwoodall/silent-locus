#!/usr/bin/env python3
"""Per-site monitor: universalagentforum.com.
Universal Agent Forum (Next.js). Homepage (200) lists /c/<category> categories and /t/msg_<id> threads; 'reply through a simple API' per meta description.
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    universalagentforum_com.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "universalagentforum_com",
    "label": "universalagentforum.com",
    "urls": ['https://universalagentforum.com/'],
    "kind": "listing-hash",
    "notes": "Universal Agent Forum (Next.js). Homepage (200) lists /c/<category> categories and /t/msg_<id> threads; 'reply through a simple API' per meta description.",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
