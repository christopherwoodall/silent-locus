#!/usr/bin/env python3
"""Per-site monitor: jotspot.io.
Agent-conversation / shareable-pages board. /published lists public jots (200, 10 /j/<id> links observed 2026-10-22).
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    jotspot_io.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "jotspot_io",
    "label": "jotspot.io",
    "urls": ['https://jotspot.io/published'],
    "kind": "listing-hash",
    "notes": "Agent-conversation / shareable-pages board. /published lists public jots (200, 10 /j/<id> links observed 2026-10-22).",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
