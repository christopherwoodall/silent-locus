#!/usr/bin/env python3
"""Per-site monitor: rentahuman.ai.
Human-bounty marketplace with /bounties/<id> items. /bounties returns 200 but is a React Flight shell: bounty rows are client-fetched, so listing-hash here catches redesigns/chrome, not per-bounty churn. No server-rendered JSON API found in page source 2026-10-22.
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    rentahuman_ai.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "rentahuman_ai",
    "label": "rentahuman.ai",
    "urls": ['https://rentahuman.ai/bounties'],
    "kind": "listing-hash",
    "notes": "Human-bounty marketplace with /bounties/<id> items. /bounties returns 200 but is a React Flight shell: bounty rows are client-fetched, so listing-hash here catches redesigns/chrome, not per-bounty churn. No server-rendered JSON API found in page source 2026-10-22.",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
