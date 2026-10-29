#!/usr/bin/env python3
"""Build the Factum bundle for the 2026-09-28-pastebin-cluster-sweep lane.

Reads events.jsonl verbatim (byte-identical detail/markers strings) and emits
a bundle: 8 reachability.check observations (venue probes) + 1 dataset.snapshot
(sweep summary), all tagged {"lane":"pastebin-cluster-sweep"}.
"""
import json

LANE = "pastebin-cluster-sweep"
LEGACY_EVENTS = "evidence/2026-09-28-pastebin-cluster-sweep/events.jsonl"
OBSERVED_AT = "2026-09-28T20:05:00Z"

events = []
with open("/home/hatch/workspace/silent-locus/evidence/2026-09-28-pastebin-cluster-sweep/events.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if line.strip():
            events.append(json.loads(line))

assert len(events) == 9, f"expected 9 events, got {len(events)}"

probes = [e for e in events if e["record_kind"] == "venue_probe"]
summaries = [e for e in events if e["record_kind"] == "venue_finding"]
assert len(probes) == 8 and len(summaries) == 1

records = [
    {
        "kind": "source",
        "ref": "source",
        "body": {
            "locator": LEGACY_EVENTS,
            "source_type": "submitted",
            "title": "2026-09-28 pastebin cluster sweep events",
        },
        "tags": {
            "lane": LANE,
            "grade": "OBSERVED",
            "provenance": "legacy lane dir evidence/2026-09-28-pastebin-cluster-sweep/ (PROVENANCE.md: passive recon, page-text fetches of public venue surfaces, 2026-09-28)",
        },
    }
]

for e in probes:
    lab = e["labels"]
    venue = lab["venue"]
    records.append(
        {
            "kind": "observation",
            "ref": f"probe-{venue.replace('.', '-')}",
            "body": {
                "type": "reachability.check",
                "data_schema": "urn:factum:web:reachability-check:1",
                "data": {
                    "target": e["source_url"],
                    "method": "page-text fetch",
                    "outcome": "response",
                },
                "source": "@source",
                "observed_at": OBSERVED_AT,
                "time_basis": "collector_clock",
                "files": [],
            },
            "tags": {
                "lane": LANE,
                "grade": "OBSERVED",
                "venue": venue,
                "result": lab["result"],
                "markers_checked": lab["markers_checked"],
                "detail": lab["detail"],
                "legacy_events": LEGACY_EVENTS,
                "legacy_fingerprint": e["fingerprint"],
                "legacy_record_kind": "venue_probe",
                "timestamp_source": "labels.observed_utc:probe_observation",
            },
        }
    )

s = summaries[0]
slab = s["labels"]
records.append(
    {
        "kind": "observation",
        "ref": "summary",
        "body": {
            "type": "dataset.snapshot",
            "data_schema": "urn:factum:datasets:snapshot:1",
            "data": {
                "dataset_uri": LEGACY_EVENTS,
                "coverage": "complete",
                "row_count": 9,
            },
            "source": "@source",
            "observed_at": OBSERVED_AT,
            "time_basis": "collector_clock",
            "files": [],
        },
        "tags": {
            "lane": LANE,
            "grade": "OBSERVED",
            "venue": slab["venue"],
            "result": slab["result"],
            "markers_checked": slab["markers_checked"],
            "detail": slab["detail"],
            "legacy_events": LEGACY_EVENTS,
            "legacy_fingerprint": s["fingerprint"],
            "legacy_record_kind": "venue_finding",
            "timestamp_source": "labels.observed_utc:sweep_summary",
            "dataset_uri_note": "dataset identity is the lane's events.jsonl (repo-relative path); the sweep covered 8 external venues, no single URL",
        },
    }
)

bundle = {
    "bundle": 2,
    "actor": "agent:lane-ingest/pastebin-cluster-sweep",
    "idempotency_key": "lane-ingest-pastebin-cluster-sweep-001",
    "records": records,
    "tags": {"lane": LANE},
}

out = "/tmp/pastebin-cluster-sweep-bundle.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump({"bundle": bundle}, f, ensure_ascii=False, indent=1)

# self-checks
kinds = [r["kind"] for r in records]
types = [r["body"].get("type") for r in records if r["kind"] == "observation"]
print("records:", len(records), "| kinds:", kinds.count("source"), "source +", kinds.count("observation"), "observations")
print("obs types:", types)
# byte-identical check: detail strings in bundle match source events exactly
b = json.load(open(out, encoding="utf-8"))["bundle"]
for rec, ev in zip([r for r in b["records"] if r["kind"] == "observation"],
                   probes + summaries):
    assert rec["tags"]["detail"] == ev["labels"]["detail"], "detail mismatch"
    assert rec["tags"]["markers_checked"] == ev["labels"]["markers_checked"], "markers mismatch"
    assert rec["tags"]["legacy_fingerprint"] == ev["fingerprint"], "fp mismatch"
print("byte-identical checks passed; bundle at", out)
