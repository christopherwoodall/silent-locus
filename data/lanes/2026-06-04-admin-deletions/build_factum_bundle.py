#!/usr/bin/env python3
"""Build the Factum ingest bundle for lane 2026-06-04-admin-deletions.

Reads evidence/2026-06-04-admin-deletions/{events,rollup}.jsonl and emits a
bundle-2 JSON document:
  1 source (collusion-wiki corpus upstream)
  2 artifacts (events.jsonl, rollup.jsonl as git references)
  2 dataset.snapshot observations (delete events; per-day rollups)
  5,217 dataset.record observations (one per delete event)
  26 dataset.record observations (one per per-day rollup doc)
Total: 5,248 records. No in_lane edges (edge building is a separate pass).

Usage: python3 build_admin_deletions_bundle.py <lane_dir> <bundle_out>
"""
import json
import sys
from collections import Counter

LANE = "2026-06-04-admin-deletions"
ACTOR = "agent:lane-ingest-2026-06-04-admin-deletions"
IDEMPOTENCY_KEY = "lane-ingest-2026-06-04-admin-deletions-v1"

EVENTS_ARTIFACT_PATH = "data/lanes/2026-06-04-admin-deletions/events.jsonl"
ROLLUP_ARTIFACT_PATH = "data/lanes/2026-06-04-admin-deletions/rollup.jsonl"

SNAPSHOT_DS = "urn:factum:datasets:snapshot:1"
RECORD_DS = "urn:factum:datasets:record:1"


def tag_base():
    return {"lane": LANE, "grade": "OBSERVED"}


def main():
    lane_dir, bundle_out = sys.argv[1], sys.argv[2]

    events = [json.loads(l) for l in open(f"{lane_dir}/events.jsonl")]
    rollups = [json.loads(l) for l in open(f"{lane_dir}/rollup.jsonl")]
    sha = {}
    for line in open(f"{lane_dir}/SHA256SUMS"):
        parts = line.split()
        sha[parts[1]] = parts[0]

    assert len(events) == 5217, f"expected 5217 events, got {len(events)}"
    assert len(rollups) == 26, f"expected 26 rollups, got {len(rollups)}"

    # Batch-internal dedup by natural key.
    eids = [e["labels"]["event_id"] for e in events]
    assert len(set(eids)) == len(eids), "duplicate event_id inside batch"
    dids = [r["labels"]["doc_id"] for r in rollups]
    assert len(set(dids)) == len(dids), "duplicate doc_id inside batch"

    records = []

    # 1. Source: the upstream collusion-wiki corpus the delete filter ran on.
    records.append({
        "kind": "source",
        "ref": "lane_source",
        "body": {
            "source_type": "local-corpus",
            "locator": "data/2026-05-17-collusion-wiki/raw/events.jsonl.gz "
                       "(19,913 events; filtered event_type == delete, no other "
                       "transformation; per lane PROVENANCE.md 2026-09-28)",
            "title": "collusion-wiki corpus events (dse wiki request/recent-changes logs)",
            "platform": "local",
        },
        "tags": {
            **tag_base(),
            "description": "Upstream corpus for the 2026-06-04-admin-deletions lane: "
                           "19,913 collusion-wiki events; the lane filter kept the "
                           "5,217 event_type == delete records verbatim.",
        },
    })

    # 2-3. Artifacts: the lane's legacy files, as git references.
    for ref, fname, path in (
        ("events_artifact", "events.jsonl", EVENTS_ARTIFACT_PATH),
        ("rollup_artifact", "rollup.jsonl", ROLLUP_ARTIFACT_PATH),
    ):
        records.append({
            "kind": "artifact",
            "ref": ref,
            "body": {
                "reference": {
                    "uri": f"file://{path}",
                    "path": path,
                    "platform": "git",
                    "reported_sha256": sha[fname],
                }
            },
            "tags": {
                **tag_base(),
                "description": f"Legacy lane file {fname} for {LANE} "
                               f"(sha256 {sha[fname]}).",
                "artifact.file": fname,
            },
        })

    # 4-5. Dataset snapshots.
    events_created = events[0]["event"]["created"]
    rollup_created = rollups[0]["event"]["created"]
    times = [e["labels"]["time"] for e in events]
    records.append({
        "kind": "observation",
        "ref": "events_snapshot",
        "body": {
            "type": "dataset.snapshot",
            "data_schema": SNAPSHOT_DS,
            "data": {
                "coverage": "complete",
                "dataset_uri": "corpus:2026-05-17-collusion-wiki/raw/events.jsonl.gz "
                               "(filter: event_type == delete)",
                "row_count": 5217,
            },
            "source": "@lane_source",
            "observed_at": events_created,
            "time_basis": "legacy_documented",
            "files": [],
        },
        "tags": {
            **tag_base(),
            "description": "Snapshot of the 2026-06-04-admin-deletions delete-event "
                           "dataset: 5,217 page-deletion events on the dse wiki "
                           f"({min(times)} -> {max(times)}), all actor [Admin1] "
                           "(ip16 2.202), change_summary 'Seite gelöscht.', "
                           "time_grade reqlog (1 rclog).",
            "snapshot.key": "2026-06-04-admin-deletions/events",
            "snapshot.row_count": 5217,
            "snapshot.actor_label": "[Admin1]",
            "snapshot.ip16": "2.202",
            "snapshot.wiki": "dse",
            "snapshot.change_summary": "Seite gelöscht.",
            "snapshot.time_first": min(times),
            "snapshot.time_last": max(times),
        },
    })
    records.append({
        "kind": "observation",
        "ref": "rollup_snapshot",
        "body": {
            "type": "dataset.snapshot",
            "data_schema": SNAPSHOT_DS,
            "data": {
                "coverage": "complete",
                "dataset_uri": "corpus:2026-05-17-collusion-wiki derived per-day "
                               "admin-cleanup-burst summaries (2026-06-04-admin-deletions rollup)",
                "row_count": 26,
            },
            "source": "@lane_source",
            "observed_at": rollup_created,
            "time_basis": "legacy_documented",
            "files": [],
        },
        "tags": {
            **tag_base(),
            "description": "Snapshot of the 26 per-day admin_cleanup_burst summary "
                           "docs derived from the 5,217 delete events (one doc per "
                           "active deletion day, 2026-06-04 -> 2026-07-14).",
            "snapshot.key": "2026-06-04-admin-deletions/rollup",
            "snapshot.row_count": 26,
        },
    })

    # 6. One dataset.record per delete event. Null-valued legacy fields are
    #    omitted from tags; full verbatim rows stay in the artifact.
    n_round = 0
    for i, e in enumerate(events):
        l = e["labels"]
        tags = {
            **tag_base(),
            "description": (
                f"Wiki page deletion on dse: page '{l['page']}' deleted by "
                f"{l['actor_label']} (ip16 {l['ip16']}) at {l['time']}; "
                f"change_summary '{l['change_summary']}'; "
                f"event_id {l['event_id']}."
            ),
            "legacy_fingerprint": e["fingerprint"],
            "legacy_record_kind": e["record_kind"],
            "legacy_dataset": e["event"]["dataset"],
            "delete.event_id": l["event_id"],
            "delete.event_type": l["event_type"],
            "delete.wiki": l["wiki"],
            "delete.page": l["page"],
            "delete.page_key": l["page_key"],
            "delete.time": l["time"],
            "delete.time_grade": l["time_grade"],
            "delete.winning_clock": l["winning_clock"],
            "delete.uncertainty_seconds": l["uncertainty_seconds"],
            "delete.request_time": l["request_time"],
            "delete.success_time": l["success_time"],
            "delete.clock_delta_seconds": l["clock_delta_seconds"],
            "delete.success_observed": l["success_observed"],
            "delete.request_action": l["request_action"],
            "delete.change_summary": l["change_summary"],
            "delete.actor_label": l["actor_label"],
            "delete.ip16": l["ip16"],
            "delete.page_held": l["page_held"],
            "delete.source_refs": l["source_refs"],
        }
        if l["round_id"] is not None:
            tags["delete.round_id"] = l["round_id"]
            n_round += 1
        if l["clock_note"] is not None:
            tags["delete.clock_note"] = l["clock_note"]
        records.append({
            "kind": "observation",
            "ref": f"del_{i:04d}",
            "body": {
                "type": "dataset.record",
                "data_schema": RECORD_DS,
                "data": {
                    "external_record_id": l["event_id"],
                    "locator": {"artifact": "@events_artifact",
                                "row": {"index": i}},
                    "snapshot": "@events_snapshot",
                },
                "source": "@lane_source",
                "observed_at": l["time"],
                "time_basis": "legacy_documented",
                "files": [],
            },
            "tags": tags,
        })

    # 7. One dataset.record per per-day rollup doc. Descriptions are analytic
    #    summaries derived from the events -> grade INFERENCE; the verbatim
    #    description text is preserved in full (no truncation).
    for j, r in enumerate(rollups):
        l = r["labels"]
        tags = {
            "lane": LANE,
            "grade": "INFERENCE",
            "description": r["description"],
            "record_subset": "per-day-rollup",
            "legacy_fingerprint": r["fingerprint"],
            "legacy_record_kind": r["record_kind"],
            "legacy_dataset": r["event"]["dataset"],
            "rollup.doc_id": l["doc_id"],
            "rollup.signal": l["signal"],
            "rollup.window": l["window"],
            "rollup.deletes": l["deletes"],
            "rollup.first": l["first"],
            "rollup.last": l["last"],
            "rollup.wiki": l["wiki"],
            "rollup.actor_label": l["actor_label"],
            "rollup.ip16": l["ip16"],
            "rollup.source_corpus": l["source_corpus"],
            "rollup.tags": r["tags"],
            "rollup.confidence": r["confidence"],
            "rollup.source_url": r["source_url"],
            "rollup.observer_product": r["observer"]["product"],
            "rollup.observer_vendor": r["observer"]["vendor"],
            "rollup.observer_type": r["observer"]["type"],
        }
        records.append({
            "kind": "observation",
            "ref": f"rollup_{j:02d}",
            "body": {
                "type": "dataset.record",
                "data_schema": RECORD_DS,
                "data": {
                    "external_record_id": l["doc_id"],
                    "locator": {"artifact": "@rollup_artifact",
                                "row": {"index": j}},
                    "snapshot": "@rollup_snapshot",
                },
                "source": "@lane_source",
                "observed_at": r["@timestamp"],
                "time_basis": "legacy_documented",
                "files": [],
            },
            "tags": tags,
        })

    # Every record carries the lane tag (also assert below).
    for rec in records:
        assert rec["tags"].get("lane") == LANE, rec["ref"]
    # No in_lane edges at ingest.
    assert not any(rec.get("kind") == "edge" for rec in records)

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": IDEMPOTENCY_KEY,
        "records": records,
    }
    with open(bundle_out, "w") as f:
        json.dump(bundle, f, ensure_ascii=False)

    kinds = Counter(rec["kind"] for rec in records)
    print(f"records: {len(records)} {dict(kinds)}; events with round_id: {n_round}")
    print(f"wrote {bundle_out}")


if __name__ == "__main__":
    main()
