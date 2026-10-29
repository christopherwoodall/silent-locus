#!/usr/bin/env python3
"""Per-site monitor: __LABEL__.
__NOTES__
Kind: __KIND__. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    __NAME__.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "__NAME__",
    "label": "__LABEL__",
    "urls": __URLS__,
    "kind": "__KIND__",
    "notes": "__NOTES__",
__EXTRA__}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
