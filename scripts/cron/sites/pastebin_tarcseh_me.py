#!/usr/bin/env python3
"""Per-site monitor: pastebin.tarcseh.me.
paste archive; CDX new-capture watch for agent dead-drops
Kind: cdx. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    pastebin_tarcseh_me.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "pastebin_tarcseh_me",
    "label": "pastebin.tarcseh.me",
    "urls": ["pastebin.tarcseh.me"],
    "kind": "cdx",
    "notes": "paste archive; CDX new-capture watch for agent dead-drops",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
