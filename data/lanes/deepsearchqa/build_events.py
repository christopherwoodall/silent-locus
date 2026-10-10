#!/usr/bin/env python3
"""Build events.jsonl for 2026-10-01-deepsearchqa.

One `benchmark_question` record per question in questions.jsonl
(dsqa_<0-based row index> IDs; ID convention verified in provenance.md).
The dataset carries no per-question dates: @timestamp falls back to the
collection date (2026-10-01), marked in labels.timestamp_source.
"""
import hashlib
import json
from datetime import datetime, timezone

LANE = "2026-10-01-deepsearchqa"
CREATED = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fp(*parts):
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


records = []
with open("questions.jsonl", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        q = json.loads(line)
        records.append(
            {
                "@timestamp": "2026-10-01T00:00:00Z",
                "event": {"dataset": LANE, "created": CREATED},
                "record_kind": "benchmark_question",
                "fingerprint": fp(LANE, "question", q["id"], q["problem"]),
                "labels": {
                    "question.id": q["id"],
                    "question.category": q["category"],
                    "question.answer_type": q["answer_type"],
                    "source.dataset": "google/deepsearchqa",
                    "source.rev": "b2623f8653065c2672de6d941fc5434cd652376c",
                    "timestamp_source": "fallback:dir_date_prefix",
                },
                "description": q["problem"],
                "confidence": "confirmed",
            }
        )

with open("events.jsonl", "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("records:", len(records))
