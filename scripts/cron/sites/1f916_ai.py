#!/usr/bin/env python3
"""Per-site monitor: 1f916.ai.
Agent society ledger. Public JSON API VERIFIED 2026-10-22: /api/citizens, /api/events, /api/stats all return JSON, but every response carries per-request now/cache_age fields so api-poll would always flag CHANGED; listing-hash on the stable pages instead. /api/changes 400s without params.
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    1f916_ai.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "1f916_ai",
    "label": "1f916.ai",
    "urls": ['https://1f916.ai/', 'https://1f916.ai/llms.txt'],
    "kind": "listing-hash",
    "notes": "Agent society ledger. Public JSON API VERIFIED 2026-10-22: /api/citizens, /api/events, /api/stats all return JSON, but every response carries per-request now/cache_age fields so api-poll would always flag CHANGED; listing-hash on the stable pages instead. /api/changes 400s without params.",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
