#!/usr/bin/env python3
"""Per-site monitor: paste.linuxiarz.pl.
paste archive; CDX new-capture watch for agent dead-drops (Factum: 295 records)
Kind: cdx. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    paste_linuxiarz_pl.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "paste_linuxiarz_pl",
    "label": "paste.linuxiarz.pl",
    "urls": ["paste.linuxiarz.pl"],
    "kind": "cdx",
    "notes": "paste archive; CDX new-capture watch for agent dead-drops (Factum: 295 records)",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
