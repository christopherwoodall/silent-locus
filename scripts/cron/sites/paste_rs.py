#!/usr/bin/env python3
"""Per-site monitor: paste.rs.
paste archive; CDX new-capture watch for agent dead-drops
Kind: cdx. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    paste_rs.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "paste_rs",
    "label": "paste.rs",
    "urls": ["paste.rs"],
    "kind": "cdx",
    "notes": "paste archive; CDX new-capture watch for agent dead-drops",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
