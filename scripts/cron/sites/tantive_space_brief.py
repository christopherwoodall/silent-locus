#!/usr/bin/env python3
"""Per-site monitor: tantive.space /api/brief.
"The Public Forum for AI Agents": JSON brief with community/service/
discovery (top_today with day roll, active_threads) plus related_projects
and protocol fields. Verified live 200 (application/json, ~11KB)
2026-10-23; canonical hash stable across fetches (no volatile
per-request fields); top_today rolls daily. Kind: api-poll. Passive GET
only. Hits are SECONDARY until independently verified (operator grading
rule).

Usage:
    tantive_space_brief.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "tantive_space_brief",
    "label": "tantive.space /api/brief",
    "urls": ["https://tantive.space/api/brief"],
    "kind": "api-poll",
    "notes": "Agent forum JSON brief (community/discovery top_today+active_threads), verified live 200 (~11KB) 2026-10-23, hash-stable across fetches. Hits are SECONDARY until independently verified (operator grading rule).",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
