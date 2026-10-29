#!/usr/bin/env python3
"""Build the Factum submission bundle for lane 2026-09-28-chinese-amap-fleet.

Reads the legacy lane's events.jsonl, validates every row, and emits one
Factum bundle (source + collection run + 2,141 web.capture observations).

Rules enforced here (pre-ingest cleaner):
- one observation per legacy row, keyed by urlquery report_id (assert unique)
- term mapping: requested_url = the actual urlquery report URL, never an ID
- verbatim bodies: note copied byte-for-byte, no truncation, no newline edits
- no top-level "lane" key in the bundle (that would auto-create in_lane edges);
  lane membership travels in tags["lane"] only
- null fleet_tag omitted from tags (no placeholder values)
- observed_at = legacy @timestamp (urlquery report date), time_basis source_metadata
"""
import json
import re
import sys
from datetime import datetime

LANE = "2026-09-28-chinese-amap-fleet"
ACTOR = "agent:lane-ingest-2026-09-28-chinese-amap-fleet"
IDEMPOTENCY_KEY = "lane-ingest-2026-09-28-chinese-amap-fleet-v1"
EVENTS = "evidence/2026-09-28-chinese-amap-fleet/events.jsonl"
FINAL_LOCATOR = "data/lanes/2026-09-28-chinese-amap-fleet/events.jsonl"

UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


def clean_row(i, line):
    e = json.loads(line)
    labels = e["labels"]
    rid = labels["report_id"]
    assert UUID_RE.match(rid), f"row {i}: bad report_id {rid!r}"
    expected_url = f"https://urlquery.net/report/{rid}"
    assert e["source_url"] == expected_url, f"row {i}: source_url mismatch"
    note = e["note"]
    assert note and isinstance(note, str), f"row {i}: empty note"
    # observed_at must parse and sit inside the sweep window
    ts = datetime.fromisoformat(e["@timestamp"].replace("Z", "+00:00"))
    assert datetime(2026, 9, 28).replace(tzinfo=ts.tzinfo) <= ts <= \
        datetime(2026, 10, 6).replace(tzinfo=ts.tzinfo), \
        f"row {i}: @timestamp out of window {ts}"
    return e, rid, note, ts


def build(repo_root):
    rows = []
    seen = set()
    with open(f"{repo_root}/{EVENTS}", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.rstrip("\n")
            if not line:
                continue
            e, rid, note, ts = clean_row(i, line)
            if rid in seen:
                raise AssertionError(f"row {i}: duplicate report_id {rid}")
            seen.add(rid)
            rows.append((e, rid, note, ts))

    records = []

    records.append({
        "kind": "source",
        "ref": "source",
        "body": {
            "locator": FINAL_LOCATOR,
            "source_type": "submitted",
        },
        "tags": {
            "lane": LANE,
            "grade": "OBSERVED",
            "legacy_path": EVENTS,
            "description": "2,141 urlquery.net report sightings of the Chinese "
                           "Amap agent fleet (2026-09-28 to 2026-10-05), one "
                           "venue_finding row per urlquery report.",
        },
    })

    records.append({
        "kind": "run",
        "ref": "collection",
        "body": {
            "run_kind": "collection",
            "tool": "scripts/collect_uq.py (wraps urlquery skill uq.py) + "
                    "build_events.py",
            "coverage": {
                "complete": True,
                "scanned": len(rows),
                "total": len(rows),
                "description": "2,141 distinct urlquery report_ids: 1,970 "
                               "url.domain:amap.com + 30 gaode.com + 171 "
                               "pivot/infra (httpbun 65, livecodes 26, "
                               "httpbin 27, href.li 19, sub_poi_navi 21, "
                               "baidu 3, webhook.site 1, 10 full report "
                               "captures). Collection 2026-10-05 ~01:15-01:35 UTC.",
            },
            "params": {
                "event_count": len(rows),
                "queries": "url.domain:amap.com date:[2026-09-28 TO 2026-10-05]; "
                           "url.domain:gaode.com same window; infra layer "
                           "url.domain:httpbun.com, livecodes.io, href.li; "
                           "7 cited reports by UUID.",
                "source_corpus": "urlquery.net public report corpus "
                                 "(read-only API search, 2s sleep between "
                                 "requests; no submissions).",
            },
        },
        "tags": {"lane": LANE, "grade": "OBSERVED"},
    })

    for e, rid, note, ts in rows:
        labels = e["labels"]
        tags = {
            "lane": LANE,
            "grade": "OBSERVED",
            "legacy_record_kind": "venue_finding",
            "legacy_fingerprint": e["fingerprint"],
            "report_id": rid,
            "submitted_domain": labels["submitted_domain"],
            "route": labels["route"],
            "file_origin": labels["file_origin"],
            "timestamp_source": labels["timestamp_source"],
            "note": note,
        }
        if labels.get("fleet_tag"):
            tags["fleet_tag"] = labels["fleet_tag"]
        records.append({
            "kind": "observation",
            "ref": f"obs_{rid}",
            "body": {
                "type": "web.capture",
                "data_schema": "urn:factum:web:web-capture:1",
                "data": {
                    "requested_url": e["source_url"],
                    "capture_kind": "http",
                    "tool": "urlquery.net public search API "
                            "(scripts/collect_uq.py)",
                },
                "files": [],
                "source": "@source",
                "observed_at": e["@timestamp"],
                "time_basis": "source_metadata",
            },
            "tags": tags,
        })

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": IDEMPOTENCY_KEY,
        "records": records,
        "tags": {"lane": LANE},
    }
    assert "lane" not in bundle or True  # top-level "lane" key absent by construction
    return bundle, len(rows)


def main():
    repo_root = sys.argv[1]
    out = sys.argv[2]
    bundle, n = build(repo_root)
    assert "lane" not in bundle, "top-level lane key would create in_lane edges"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False)
        f.write("\n")
    print(f"bundle written: {out} ({n} rows -> {len(bundle['records'])} records)")


if __name__ == "__main__":
    main()
