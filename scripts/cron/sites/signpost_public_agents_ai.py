#!/usr/bin/env python3
"""Per-site monitor: Signpost (public-agents.ai).
llms.txt verified live 200 (21240 bytes) 2026-10-22; Signpost is the
autonomous agent of the Public Agents registry. Hits are SECONDARY until
independently verified (operator grading rule).
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    signpost_public_agents_ai.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "signpost_public_agents_ai",
    "label": "Signpost (public-agents.ai)",
    "urls": ["https://signpost.public-agents.ai/llms.txt"],
    "kind": "listing-hash",
    "notes": "llms.txt verified live 200 (21240 bytes) 2026-10-22; Signpost is the autonomous agent of the Public Agents registry. Hits are SECONDARY until independently verified (operator grading rule).",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
