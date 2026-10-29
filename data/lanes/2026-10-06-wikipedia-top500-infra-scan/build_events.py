#!/usr/bin/env python3
"""Build events.jsonl for 2026-10-06-wikipedia-top500-infra-scan.

One `infra_ip_candidate` record per line of raw/ip-matches.jsonl (the 90
pre-kill matcher hits, retained as evidence per SCAN-SUMMARY.md, annotated
with the reviewer-1 kill verdict), plus one `scan_summary` record with the
lane's reviewed headline verdict.
"""
import hashlib
import json
from datetime import datetime, timezone

LANE = "2026-10-06-wikipedia-top500-infra-scan"
CREATED = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fp(*parts):
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


records = []

with open("raw/ip-matches.jsonl", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        m = json.loads(line)
        records.append(
            {
                "@timestamp": m["timestamp"],
                "event": {"dataset": LANE, "created": CREATED},
                "record_kind": "infra_ip_candidate",
                "fingerprint": fp(LANE, "ip-match", m["article"], str(m["revid"])),
                "labels": {
                    "article.rank": m["rank"],
                    "article.title": m["article"],
                    "rev.id": m["revid"],
                    "ip": m["ip"],
                    "providers": m["providers"],
                    "services": m["services"],
                    "rev.comment": m["comment"],
                    "rev.tags": m["tags"],
                    "review.verdict": "killed",
                    "review.kill_reason": (
                        "range currency: provider CIDR entered the published feed "
                        "1-6 years after the edit; 0/67 distinct IPs in any "
                        "edit-contemporaneous provider range (reviewer-1, 2026-10-06)"
                    ),
                    "timestamp_source": "record",
                },
                "description": (
                    f"pre-kill matcher hit: IP {m['ip']} ({'/'.join(m['providers'])}) "
                    f"on '{m['article']}' rev {m['revid']} ({m['timestamp']}) — "
                    f"attribution KILLED by reviewer-1 on range currency"
                ),
                "confidence": "killed",
            }
        )

records.append(
    {
        "@timestamp": "2026-10-07T00:00:00Z",
        "event": {"dataset": LANE, "created": CREATED},
        "record_kind": "scan_summary",
        "fingerprint": fp(LANE, "scan-summary"),
        "labels": {
            "revisions.scanned": 677635,
            "articles.scanned": 489,
            "ip.editors": 61179,
            "temp.accounts": 21922,
            "named.users": 594534,
            "prekill.hits": 90,
            "surviving.attributions": 0,
            "ai.lab.range.matches": 0,
            "agent.era.ip.visible.matches": 0,
            "verdict": (
                "zero verified datacenter-infra edits attributable to any provider "
                "and zero attributable to any AI lab in the visible history of the "
                "top-500 articles (clean reviewed negative)"
            ),
            "reviewer1": "KILLED all 90 attributions (range currency)",
            "reviewer2": "KILLED the AI-agent headline claim (IP visibility 0% in 2026)",
            "timestamp_source": "note:review_completion",
        },
        "description": (
            "Wikipedia top-500 infra scan (2026-10-06) final verdict: zero verified "
            "datacenter-infra edits attributable to any provider, zero attributable "
            "to any AI lab. 90/90 pre-kill matcher hits killed by reviewer-1 on "
            "range currency. AI-agent headline claim killed by reviewer-2 (IP "
            "visibility 0% in 2026; method blind to the agent era). See SCAN-SUMMARY.md."
        ),
        "confidence": "reviewed",
    }
)

with open("events.jsonl", "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("records:", len(records))
