#!/usr/bin/env python3
"""Per-site monitor: Botbook.space (agent social network).
llms.txt verified live 200 (4040 bytes) 2026-10-22; agent REST API is
bearer-keyed, so llms.txt is the keyless listing surface. Hits are
SECONDARY until independently verified (operator grading rule).
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    botbook_space.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "botbook_space",
    "label": "Botbook.space (agent social network)",
    "urls": ["https://botbook.space/llms.txt"],
    "kind": "listing-hash",
    "notes": "llms.txt verified live 200 (4040 bytes) 2026-10-22; agent REST API is bearer-keyed, so llms.txt is the keyless listing surface. Hits are SECONDARY until independently verified (operator grading rule).",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
