#!/usr/bin/env python3
"""Per-site monitor: openagentforum.com.
Signed-message agent forum. /channels/ indexes 8 public channels (200); /channels/general/ lists recent /messages/<uuid> links (3 observed 2026-10-22).
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    openagentforum_com.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "openagentforum_com",
    "label": "openagentforum.com",
    "urls": ['https://openagentforum.com/channels/', 'https://openagentforum.com/channels/general/'],
    "kind": "listing-hash",
    "notes": "Signed-message agent forum. /channels/ indexes 8 public channels (200); /channels/general/ lists recent /messages/<uuid> links (3 observed 2026-10-22).",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
