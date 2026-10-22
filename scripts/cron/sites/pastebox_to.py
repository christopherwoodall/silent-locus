#!/usr/bin/env python3
"""Per-site monitor: pastebox.to.
paste archive; CDX new-capture watch for agent dead-drops
Kind: cdx. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    pastebox_to.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "pastebox_to",
    "label": "pastebox.to",
    "urls": ["pastebox.to"],
    "kind": "cdx",
    "notes": "paste archive; CDX new-capture watch for agent dead-drops",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
