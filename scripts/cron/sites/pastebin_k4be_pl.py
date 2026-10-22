#!/usr/bin/env python3
"""Per-site monitor: pastebin.k4be.pl.
paste archive; CDX new-capture watch for agent dead-drops (Factum: 229 records)
Kind: cdx. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    pastebin_k4be_pl.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "pastebin_k4be_pl",
    "label": "pastebin.k4be.pl",
    "urls": ["pastebin.k4be.pl"],
    "kind": "cdx",
    "notes": "paste archive; CDX new-capture watch for agent dead-drops (Factum: 229 records)",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
