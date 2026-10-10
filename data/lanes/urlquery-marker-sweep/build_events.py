#!/usr/bin/env python3
"""Build venue_finding events for newly fetched unscoped exploitgym search pages.

One event per search-hit report, following the existing events.jsonl schema:
- @timestamp = report scan time (date field, UTC Z); labels.timestamp_source = "labels:date"
- record_kind = venue_finding
- fingerprint = sha256(report_id)
- event.dataset = "2025-12-04-urlquery-marker-sweep" (per collection dir name)
- evidence_grade = "low": plain-text search-index match; match location not
  verifiable via the public report API (per collection PROVENANCE caveat).
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

COLL = os.path.dirname(os.path.abspath(__file__))
CREATED = datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def build_event(r):
    rid = r["report_id"]
    return {
        "@timestamp": r["date"],
        "event": {"dataset": "2025-12-04-urlquery-marker-sweep", "created": CREATED},
        "record_kind": "venue_finding",
        "fingerprint": hashlib.sha256(rid.encode()).hexdigest(),
        "labels": {
            "report_id": rid,
            "marker": "exploitgym",
            "location": "search-index match (match location not verifiable via public report API)",
            "evidence_grade": "low",
            "timestamp_source": "labels:date",
        },
        "source_url": f"https://urlquery.net/report/{rid}",
        "note": (
            "Unscoped \"exploitgym\" search hit (paginated continuation, 2026-09-29). "
            "Marker matched in urlquery's plain-text search index (captured HTML/JS text); "
            "per the collection caveat the match location cannot be confirmed from the "
            "public report API. Scanned URL: %s" % (r.get("submit") or r.get("final") or "?")
        ),
    }


def main(paths):
    seen = set()
    with open(f"{COLL}/events.jsonl") as f:
        for line in f:
            line = line.strip()
            if line:
                seen.add(json.loads(line)["labels"]["report_id"])
    new = []
    for p in paths:
        d = json.load(open(p))
        for r in d.get("reports", []):
            if r["report_id"] not in seen:
                seen.add(r["report_id"])
                new.append(build_event(r))
    with open(f"{COLL}/events.jsonl", "a") as f:
        for e in new:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"added {len(new)} events; total now {len(seen)}")


if __name__ == "__main__":
    main(sys.argv[1:])
