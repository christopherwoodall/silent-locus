#!/usr/bin/env python3
"""Per-site monitor: openwitness.net.
Agent mirror with /p/<id> posts and /c/<channel> channels. Homepage (200, ~1.2MB) lists /c/<channel> links incl. atlas-hermes, agentcolony-adjacent channels.
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    openwitness_net.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "openwitness_net",
    "label": "openwitness.net",
    "urls": ['https://openwitness.net/'],
    "kind": "listing-hash",
    "notes": "Agent mirror with /p/<id> posts and /c/<channel> channels. Homepage (200, ~1.2MB) lists /c/<channel> links incl. atlas-hermes, agentcolony-adjacent channels.",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
