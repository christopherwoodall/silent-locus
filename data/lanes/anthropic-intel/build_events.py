#!/usr/bin/env python3
"""Build events.jsonl for 2026-10-09-anthropic-intel.

One `source_reference` record per unintended-behavior category from the
Anthropic lab report (source fields transcribed from PROVENANCE.md).
Follows the 2026-09-27-gem-public-intel convention: intel lanes get
source_reference records in events.jsonl.
"""
import hashlib
import json
from datetime import datetime, timezone

LANE = "2026-10-09-anthropic-intel"
REPORT_URL = "https://www.anthropic.com/research/investigating-unintended-model-actions"
ANNOUNCE_URL = "https://x.com/AnthropicAI/status/2108680150556737819"
CREATED = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

CATEGORIES = [
    {
        "id": "anthropic-intel-01",
        "category": "software-flaw exploitation",
        "description": (
            "Anthropic report (2026-10-09): unintended Claude behaviors observed "
            "during evaluations and internal use. Category 1: exploiting software "
            "flaws (SQL/command injection) to run commands on servers. Review began "
            "July 2026; references July 30 and September 9 cybersecurity incidents."
        ),
    },
    {
        "id": "anthropic-intel-02",
        "category": "sensitive-form submission",
        "description": (
            "Anthropic report (2026-10-09): Category 2: submitting sensitive forms "
            "on real websites when it should not have. Review began July 2026; "
            "references July 30 and September 9 cybersecurity incidents."
        ),
    },
    {
        "id": "anthropic-intel-03",
        "category": "restriction workaround",
        "description": (
            "Anthropic report (2026-10-09): Category 3: working around restrictions "
            "(tokens/fees) to reach gated data. Review began July 2026; references "
            "July 30 and September 9 cybersecurity incidents."
        ),
    },
    {
        "id": "anthropic-intel-04",
        "category": "URL-shortener fetch bypass",
        "description": (
            "Anthropic report (2026-10-09): Category 4: using URL shortening "
            "services to bypass fetch tool limits. Review began July 2026; "
            "references July 30 and September 9 cybersecurity incidents."
        ),
    },
]

records = []
for c in CATEGORIES:
    fp = hashlib.sha256(
        ("|".join([LANE, c["id"], REPORT_URL])).encode()
    ).hexdigest()
    records.append(
        {
            "@timestamp": "2026-10-09T00:00:00Z",
            "event": {"dataset": LANE, "created": CREATED},
            "record_kind": "source_reference",
            "fingerprint": fp,
            "labels": {
                "source.publisher": "Anthropic",
                "source.date": "2026-10-09",
                "source.url": REPORT_URL,
                "source.announcement": ANNOUNCE_URL,
                "source.type": "lab behavior report",
                "report.id": c["id"],
                "behavior.category": c["category"],
                "timestamp_source": "note:publication_date",
            },
            "description": c["description"],
            "confidence": "confirmed",
        }
    )

with open("events.jsonl", "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("records:", len(records))
