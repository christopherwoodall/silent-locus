#!/usr/bin/env python3
"""Per-site monitor: Hermes Agent (Nous Research).
Docs verified live 2026-10-22; /docs is the stable listing surface (35KB).
The 646KB marketing homepage is not polled (too heavy); the llms-*.txt
docs asset (45KB, also live 200) embeds a build hash and may rotate on
rebuild, so it is intentionally excluded. Hits are SECONDARY until
independently verified (operator grading rule).
Kind: listing-hash. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    hermes_agent_nousresearch_com.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "hermes_agent_nousresearch_com",
    "label": "Hermes Agent (Nous Research)",
    "urls": ["https://hermes-agent.nousresearch.com/docs/"],
    "kind": "listing-hash",
    "notes": "Docs verified live 2026-10-22; /docs is the stable listing surface. Marketing homepage (646KB) not polled; hash-named llms-*.txt asset intentionally excluded (build-hash URL rotates). Hits are SECONDARY until independently verified (operator grading rule).",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
