#!/usr/bin/env python3
"""Per-site monitor: openagentchat.net.
Agent chat with /p/<slug> posts. Homepage (200) lists posts; /feed.xml is a valid Atom feed with 30 entries (200).
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    openagentchat_net.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "openagentchat_net",
    "label": "openagentchat.net",
    "urls": ['https://openagentchat.net/', 'https://openagentchat.net/feed.xml'],
    "kind": "listing-hash",
    "notes": "Agent chat with /p/<slug> posts. Homepage (200) lists posts; /feed.xml is a valid Atom feed with 30 entries (200).",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
