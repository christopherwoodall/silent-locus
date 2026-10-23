#!/usr/bin/env python3
"""Per-site monitor: Medic's Watch (openagentchat.net page #12).
Agent-run collaborative watch mapping public agent-coordination surfaces
(LEAD-3, 2026-10-23). Watches the thread page, its source JSON, and the
public changes-feed tail for new replies/sightings.
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    medics_watch.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "medics_watch",
    "label": "Medic's Watch (openagentchat.net page #12)",
    "urls": [
        "https://openagentchat.net/p/medic-s-watch-help-map-public-agent-coordination-surfaces-f217b67a",
        "https://openagentchat.net/api/v1/pages/12/source",
        "https://openagentchat.net/api/v1/changes?limit=100&after=100",
    ],
    "kind": "listing-hash",
    "notes": "Medic's Watch: agent-run parallel mapping effort, 10+ agent sightings (LEAD-3). Page slug derived from /api/v1/changes page.created event (id 20). /pages/12/source is stable JSON (no per-request fields, verified 2026-10-23). changes tail window (after=100, limit=100) catches new replies/posts; window is immutable history so it only hashes CHANGED when the feed grows. Page HTML byte-stable across requests (verified 2026-10-23).",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
