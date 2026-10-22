#!/usr/bin/env python3
"""Per-site monitor: AlienVault OTX (keyless indicator lookups).
Polls OTX /api/v1/indicators/{type}/{value}/general (verified keyless
2026-10-22) for third-party pulse counts on watched infrastructure:
the 4 Counsel-confirmed malicious Cairn panel IPs + Tier-1 board
domains. A rising pulse count means someone else filed our
infrastructure — SECONDARY corroboration until independently verified.
(Pulse subscription/listing endpoints need a free OTX key; not used.)
Kind: feed. Passive GET only. Hits are SECONDARY until independently
verified (operator grading rule).

Usage:
    otx.py [--dry-run] [--json] [--limit N]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sitewatch  # noqa: E402

SITE = {
    "name": "otx",
    "label": "AlienVault OTX (keyless)",
    "urls": [],
    "kind": "feed",
    "notes": "Keyless OTX indicator lookups on 4 malicious Cairn panel IPs + 4 Tier-1 board domains. Pulse-count changes reported.",
    "feed": {"kind": "otx-indicators", "indicators": [
        {"type": "IPv4", "value": "185.242.245.159"},
        {"type": "IPv4", "value": "31.56.206.187"},
        {"type": "IPv4", "value": "31.57.47.29"},
        {"type": "IPv4", "value": "31.59.92.155"},
        {"type": "domain", "value": "swarmsay.com"},
        {"type": "domain", "value": "commons.dooza.ai"},
        {"type": "domain", "value": "commonlog.ai"},
        {"type": "domain", "value": "agentcolony.one"},
    ]},
}

if __name__ == "__main__":
    raise SystemExit(sitewatch.main(SITE))
