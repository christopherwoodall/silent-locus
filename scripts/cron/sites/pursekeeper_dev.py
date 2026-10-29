#!/usr/bin/env python3
"""Per-site monitor: Pursekeeper.dev /offers board.
/offers verified live 200 (4516 bytes) 2026-10-22; /log.json (1.8MB
treasury JSON, also live) is not polled — the offers board is the listing
surface. Hits are SECONDARY until independently verified (operator rule).
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    pursekeeper_dev.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "pursekeeper_dev",
    "label": "Pursekeeper.dev /offers board",
    "urls": ["https://pursekeeper.dev/offers"],
    "kind": "listing-hash",
    "notes": "/offers verified live 200 (4516 bytes) 2026-10-22; /log.json (1.8MB treasury JSON, also live) is not polled — the offers board is the listing surface. Hits are SECONDARY until independently verified (operator grading rule).",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
