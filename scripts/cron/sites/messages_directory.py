#!/usr/bin/env python3
"""Per-site monitor: messages.directory.
Public JSON thread API verified live 200 (valid JSON with total/threads)
2026-10-22; no-auth public message board for AI agents. Hits are
SECONDARY until independently verified (operator grading rule).
Kind: api-poll. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    messages_directory.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "messages_directory",
    "label": "messages.directory (agent message board)",
    "urls": ["https://messages.directory/api/threads"],
    "kind": "api-poll",
    "notes": "Public JSON thread API verified live 200 (valid JSON with total/threads) 2026-10-22; no-auth public message board for AI agents. Hits are SECONDARY until independently verified (operator grading rule).",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
