#!/usr/bin/env python3
"""Per-site monitor: ThreatFox (abuse.ch).
SKIPPED 2026-10-22: the API is POST-only (our rule is GET-only) and
moved behind abuse.ch Auth-Key (401 without). No keyless GET surface.
Revisit if a free key is provisioned.
Kind: feed. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    threatfox.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "threatfox",
    "label": "ThreatFox (abuse.ch)",
    "urls": [],
    "kind": "feed",
    "notes": "SKIPPED 2026-10-22: POST-only API behind abuse.ch Auth-Key (401 without). No keyless GET surface.",
    "feed": {"kind": "skipped",
             "reason": "POST-only API + requires abuse.ch Auth-Key"},
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
