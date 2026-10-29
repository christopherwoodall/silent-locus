#!/usr/bin/env python3
"""Per-site monitor: agentchan.org.
Agent imageboard (/apol/ /b/ /g/ /int/ /meta/ /test/ /x/ /pol/ /ai/ /hum/ /lit/ /phi/ /tfw/). /b/ thread listing (200, 30KB); /skill.md is the agent gateway doc (200).
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    agentchan_org.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "agentchan_org",
    "label": "agentchan.org",
    "urls": ['https://agentchan.org/b/', 'https://agentchan.org/skill.md'],
    "kind": "listing-hash",
    "notes": "Agent imageboard (/apol/ /b/ /g/ /int/ /meta/ /test/ /x/ /pol/ /ai/ /hum/ /lit/ /phi/ /tfw/). /b/ thread listing (200, 30KB); /skill.md is the agent gateway doc (200).",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
