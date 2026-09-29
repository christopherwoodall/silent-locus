#!/usr/bin/env python3
"""Backfill published_at onto diffend_harvest log records (schema review E.1).

Parses diffend_versions[].diff_ts ("%b %d, %Y %H:%M", UTC) for the record's
own version, else the max available. Additive-only: never modifies existing
fields. Run once, after the harvest completes (the harvester appends).
"""
import json, os
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = BASE + "/data/2025-03-04-rubygems-goimport-campaign/raw/gem-ioc-log.jsonl"
FALLBACK_TS = "2026-09-27T00:00:00.000Z"


def parse_diff_ts(ts):
    try:
        return datetime.strptime(ts.strip(), "%b %d, %Y %H:%M").replace(
            tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
    except Exception:
        return None


def main():
    recs = []
    with open(LOG) as f:
        for line in f:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    n = 0
    for r in recs:
        if r.get("record_kind") != "diffend_harvest" or r.get("published_at"):
            continue
        ver = r.get("version")
        iso = None
        for v in r.get("diffend_versions", []) or []:
            if v.get("version") == ver and v.get("diff_ts"):
                iso = parse_diff_ts(v["diff_ts"])
                break
        if iso is None:
            cands = [parse_diff_ts(v["diff_ts"]) for v in
                     r.get("diffend_versions", []) or [] if v.get("diff_ts")]
            cands = [c for c in cands if c]
            iso = max(cands) if cands else None
        r["published_at"] = iso or FALLBACK_TS
        r["published_at_source"] = ("diffend:diff_ts" if iso
                                    else "fallback:missing_first_seen")
        n += 1
    with open(LOG, "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    print("backfilled published_at on %d diffend_harvest records" % n)


if __name__ == "__main__":
    main()
