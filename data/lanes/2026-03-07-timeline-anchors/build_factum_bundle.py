#!/usr/bin/env python3
"""Build the Factum ingest bundle for lane 2026-03-07-timeline-anchors.

Mapping (documented, deterministic):
- 1 source record -> evidence/2026-03-07-timeline-anchors/events.jsonl
- 1 dataset.snapshot observation describing the 48-anchor dataset
- 48 event records (type incident.reported; legacy record_kind timeline_anchor
  preserved in tags.legacy_record_kind), each citing the snapshot.
- Event body fields: event_type must be a registered type name; title is a
  short derived label; occurred.on_date/start for exact precisions, raw-only
  for estimated precisions (never invent precision).
- Verbatim evidence (description, evidence_note, date_precision, is_estimate,
  confidence, source_url) goes into tags byte-identical to events.jsonl.
"""
import json, re, sys
from urllib.parse import urlparse

LANE = "2026-03-07-timeline-anchors"
ACTOR = "agent:lane-ingest-2026-03-07-timeline-anchors"
KEY = "lane-ingest-2026-03-07-timeline-anchors-001"
EVENTS = "evidence/2026-03-07-timeline-anchors/events.jsonl"
EVENTS_SHA = "51558833074b140418f5a43bc023c7e63bfa0360348d8cea1052e9aa0cc225dd"

UPSTREAM_HOSTS = {"rubyhack.ai", "socket.dev"}

def grade(ev):
    lane = ev["labels"].get("lane", "")
    url = ev.get("source_url") or ""
    host = urlparse(url).netloc.lower()
    if lane.startswith("press/") or host in UPSTREAM_HOSTS:
        return "UPSTREAM"
    return "OBSERVED"

def title_of(desc):
    t = re.split(r";| -- ", desc, maxsplit=1)[0].strip()
    return t[:140]

def occurred_of(ev):
    ts = ev["@timestamp"]
    prec = ev["labels"].get("date_precision", "")
    if prec == "day":
        return {"basis": "legacy_documented", "on_date": ts[:10]}
    if prec == "timestamp":
        return {"basis": "legacy_documented", "start": ts}
    if prec == "day-estimated":
        return {"basis": "legacy_documented", "raw": "%s (day-estimated)" % ts[:10]}
    if prec == "month-estimated":
        return {"basis": "legacy_documented", "raw": "%s (month-estimated)" % ts[:7]}
    return {"basis": "legacy_documented", "raw": ts}

def build():
    with open(EVENTS, encoding="utf-8") as f:
        evs = [json.loads(l) for l in f]
    assert len(evs) == 48, len(evs)
    recs = []
    recs.append({
        "ref": "source", "kind": "source",
        "body": {"locator": EVENTS, "source_type": "submitted"},
        "tags": {"lane": LANE,
                 "provenance": "legacy lane events.jsonl (night-watch hunt lane, 2026-09-28)"},
    })
    recs.append({
        "ref": "snapshot", "kind": "observation",
        "body": {
            "type": "dataset.snapshot",
            "source": "@source",
            "observed_at": "2026-09-28T06:57:39Z",
            "time_basis": "source_metadata",
            "files": [],
            "data_schema": "urn:factum:datasets:snapshot:1",
            "data": {"dataset_uri": EVENTS, "coverage": "complete",
                     "row_count": 48, "revision": "sha256:" + EVENTS_SHA},
        },
        "tags": {"lane": LANE, "grade": "OBSERVED",
                 "description": "timeline-anchors: 48 dated-event anchors connecting evidence "
                                "across hunt lanes via time; 2026-06-18 is the known cross-dataset "
                                "anchor; 10 anchors carry the june-18 cluster tag",
                 "legacy_fingerprint": EVENTS_SHA},
    })
    for i, ev in enumerate(evs):
        lb = ev["labels"]
        desc = ev["description"]
        tags = {
            "lane": LANE,
            "grade": grade(ev),
            "description": desc,
            "source_lane": lb.get("lane", ""),
            "date_precision": lb.get("date_precision", ""),
            "is_estimate": lb.get("is_estimate", ""),
            "confidence": ev.get("confidence", ""),
            "evidence_note": lb.get("evidence_note", ""),
            "legacy_events": EVENTS,
            "legacy_fingerprint": ev.get("fingerprint", ""),
            "legacy_id": lb.get("_id", ""),
            "legacy_record_kind": "timeline_anchor",
        }
        if ev.get("source_url"):
            tags["source_url"] = ev["source_url"]
        if lb.get("anchor_cluster") and lb["anchor_cluster"] != "none":
            tags["anchor_cluster"] = lb["anchor_cluster"]
            tags["anchor:" + lb["anchor_cluster"]] = "true"
        recs.append({
            "ref": "anchor-%02d" % i, "kind": "event",
            "body": {
                "event_type": "incident.reported",
                "title": title_of(desc),
                "occurred": occurred_of(ev),
                "cites": ["@snapshot"],
                "data_schema": "urn:factum:core:empty:1",
                "data": {},
            },
            "tags": tags,
        })
    return {"bundle": 2, "actor": ACTOR, "idempotency_key": KEY,
            "records": recs, "tags": {"lane": LANE}}

if __name__ == "__main__":
    b = build()
    if "--dry" in sys.argv:
        for r in b["records"]:
            if r["kind"] == "event":
                print(r["body"]["title"][:80].ljust(82), "|",
                      json.dumps(r["body"]["occurred"]), "|",
                      r["tags"]["grade"], "|", r["tags"]["source_lane"][:24])
    else:
        json.dump(b, open("/tmp/timeline_anchors_bundle.json", "w"), ensure_ascii=False)
        print("wrote bundle:", len(b["records"]), "records")
