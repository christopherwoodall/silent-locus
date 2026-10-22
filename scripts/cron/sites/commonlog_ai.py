#!/usr/bin/env python3
"""Per-site monitor: commonlog.ai.
Permissionless permanent agent log. Homepage IS the live reverse-chron feed (200, ~96KB); llms.txt carries generation/head cursor. JSON API verified 2026-10-22: GET /m/{id} and /a/{id} return JSON (openapi.json documents /refs /run /stream /status). No baseline endpoint in sibling file; discovered fresh.
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    commonlog_ai.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "commonlog_ai",
    "label": "commonlog.ai",
    "urls": ['https://commonlog.ai/', 'https://commonlog.ai/llms.txt'],
    "kind": "listing-hash",
    "notes": "Permissionless permanent agent log. Homepage IS the live reverse-chron feed (200, ~96KB); llms.txt carries generation/head cursor. JSON API verified 2026-10-22: GET /m/{id} and /a/{id} return JSON (openapi.json documents /refs /run /stream /status). No baseline endpoint in sibling file; discovered fresh.",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
