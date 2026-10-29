#!/usr/bin/env python3
"""Per-site monitor: URLhaus (abuse.ch).
SKIPPED 2026-10-22: the community API moved behind abuse.ch Auth-Key
(login required; unauthenticated calls 401), and the entire
/downloads/ tree (text, csv_recent) now returns 410 Gone. No keyless
GET surface remains. Revisit if a free key is provisioned.
Kind: feed. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    urlhaus.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "urlhaus",
    "label": "URLhaus (abuse.ch)",
    "urls": [],
    "kind": "feed",
    "notes": "SKIPPED 2026-10-22: API requires abuse.ch Auth-Key (401 without); /downloads/ tree retired (410). No keyless GET surface.",
    "feed": {"kind": "skipped",
             "reason": "requires abuse.ch Auth-Key; downloads retired (410)"},
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
