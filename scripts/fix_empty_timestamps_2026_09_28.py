#!/usr/bin/env python3
"""Repair empty @timestamp values left by backfill_schema_2026_09_28.py.

Rules (documented in schema/README.md):
- extraction records:      @timestamp = labels["extracted.at"]
- diffend_harvest records:  @timestamp = labels["published.at"]
- genuinely dateless:      @timestamp = 1970-01-01T00:00:00Z sentinel +
                           labels["timestamp_source"] = "fallback:no_recoverable_date"

All source values are UTC already; output is normalized to Z.
Idempotent.
"""

import json
import sys
from datetime import datetime, timezone

REPO = __file__.rsplit("/scripts/", 1)[0]
SENTINEL = "1970-01-01T00:00:00Z"
FLAG = "fallback:no_recoverable_date"

TARGETS = [
    "data/2025-03-04-rubygems-goimport-campaign/raw/gem-ioc-log.jsonl",
    "data/2026-07-21-transfer-test-family/events.jsonl",
]


def norm(ts: str) -> str:
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def repair(rec: dict) -> dict:
    if rec.get("@timestamp"):
        return rec
    lab = rec["labels"]
    src = lab.get("published.at") or lab.get("extracted.at")
    if src:
        rec["@timestamp"] = norm(src)
        lab["timestamp_source"] = f"labels:{'published.at' if lab.get('published.at') else 'extracted.at'}"
    else:
        rec["@timestamp"] = SENTINEL
        lab["timestamp_source"] = FLAG
    return rec


def main():
    check_only = "--check" in sys.argv
    fixed = flagged = 0
    for rel in TARGETS:
        p = f"{REPO}/{rel}"
        out = []
        for line in open(p):
            if not line.strip():
                continue
            r = json.loads(line)
            before = r.get("@timestamp")
            r = repair(r)
            if not before:
                if r["@timestamp"] == SENTINEL:
                    flagged += 1
                else:
                    fixed += 1
            out.append(json.dumps(r, ensure_ascii=False))
        if not check_only:
            open(p, "w").write("\n".join(out) + "\n")
    print(f"{'would repair' if check_only else 'repaired'}: {fixed} timestamps, "
          f"{flagged} sentinel-flagged")


if __name__ == "__main__":
    main()
