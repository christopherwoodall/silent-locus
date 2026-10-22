#!/usr/bin/env python3
"""Per-site monitor: gotit.pub.
paste archive; CDX new-capture watch for agent dead-drops
Kind: cdx. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    gotit_pub.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "gotit_pub",
    "label": "gotit.pub",
    "urls": ["gotit.pub"],
    "kind": "cdx",
    "notes": "paste archive; CDX new-capture watch for agent dead-drops",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
