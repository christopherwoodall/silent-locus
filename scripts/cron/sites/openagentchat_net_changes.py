#!/usr/bin/env python3
"""Per-site monitor: openagentchat.net /api/v1/changes.
Agent commons cursor changes feed: JSON {items[50], next_cursor, has_more};
each item carries id/kind/page_id/reply_id/created_at/actor/title/url.
Verified live 200 (application/json, ~15KB) 2026-10-23; canonical hash
stable across fetches (no volatile per-request fields), next_cursor
stable. New page/reply beacons (e.g. Green AI Bot Sept 20 burst) land
here first. Kind: api-poll. Passive GET only. Hits are SECONDARY until
independently verified (operator grading rule).

Usage:
    openagentchat_net_changes.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "openagentchat_net_changes",
    "label": "openagentchat.net /api/v1/changes",
    "urls": ["https://openagentchat.net/api/v1/changes"],
    "kind": "api-poll",
    "notes": "Agent commons cursor changes feed (JSON items/next_cursor/has_more), verified live 200 (~15KB) 2026-10-23, hash-stable across fetches. Hits are SECONDARY until independently verified (operator grading rule).",
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
