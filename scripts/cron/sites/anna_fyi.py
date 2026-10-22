#!/usr/bin/env python3
"""Per-site monitor: anna.fyi.
paste archive; CDX new-capture watch for agent dead-drops (Factum: 179 records; raw view /view/raw/<id>)
Kind: cdx. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    anna_fyi.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "anna_fyi",
    "label": "anna.fyi",
    "urls": ["anna.fyi"],
    "kind": "cdx",
    "notes": "paste archive; CDX new-capture watch for agent dead-drops (Factum: 179 records; raw view /view/raw/<id>)",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
