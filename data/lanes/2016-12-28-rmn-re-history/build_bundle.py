#!/usr/bin/env python3
"""Build the Factum ingest bundle for lane 2016-12-28-rmn-re-history.

Cleaner: normalizes legacy lane evidence into typed Factum records.
Only genuinely new evidence is submitted; everything else is dedup-skipped
(see PROVENANCE.md ingest section for the overlap analysis).

Submits:
  1 source (the rmn-re-history reconstruction)
  1 infra.ioc (first zz-grammar slug 'zzzz' -- the oai/epoch10 first-
      appearance anchors already live in lane 2026-03-07-timeline-anchors)
  3 reachability.check (archive.org availability / CDX / playback probes)
     (registered type name has no `web.` prefix -- corpus precedent)

Skipped (documented, not submitted):
  764 wiki_shortener per-slug  -> all exist as infra.shortcut in corpus
  2 timeline_anchor (oai, epoch10) -> covered by 2026-03-07-timeline-anchors
  47 link_growth_rollup -> no installed schema type; kept as lane document
"""
import json
import sys

LANE = "2016-12-28-rmn-re-history"
ACTOR = "agent:lane-ingest:2016-12-28-rmn-re-history"
IDEMPOTENCY_KEY = "rmn-re-history-ingest-2026-10-10"

LANE_DIR = "data/lanes/2016-12-28-rmn-re-history"
RAW = f"{LANE_DIR}/raw"
EV = f"{LANE_DIR}/events.jsonl"


def main():
    grammar = json.load(open(f"{RAW}/grammar_first_appearance.json"))
    archive = json.load(open(f"{RAW}/archive_lookup.json"))

    zz = grammar["zz"]  # verbatim from raw
    avail = archive["availability_api"]
    cdx = archive["cdx_listing"]
    playback = archive["snapshot_playback"]
    probe_at = "2026-09-28T03:05:00Z"  # labels:probe.attempted_at

    records = [
        {
            "ref": "source",
            "kind": "source",
            "body": {
                "locator": f"data/lanes/{LANE}/events.jsonl",
                "source_type": "submitted",
                "title": "rmn.re YOURLS link-table history reconstruction "
                         "(764 slugs, 2016-12 -> 2026-09)",
            },
            "tags": {
                "lane": LANE,
                "kind": "lane-events",
                "legacy_path": f"evidence/{LANE}/events.jsonl",
                "grade": "OBSERVED",
                "method": "derived analysis of 2026-09-27 link-table crawl "
                          "(764 records) + 2026-05/06 wiki shortener log "
                          "(499 records) + archive.org probes 2026-09-28",
                "inputs": "link_table_2026-09-27.jsonl; "
                          "wiki_shortener_detail.json; archive.org "
                          "availability/CDX/playback probes",
            },
        },
        {
            "ref": "ioc-zz-first",
            "kind": "observation",
            "body": {
                "type": "infra.ioc",
                "source": "@source",
                "observed_at": zz["created"],
                "time_basis": "source_metadata",
                "files": [],
                "data_schema": "urn:factum:infra:ioc:1",
                "data": {
                    "term": zz["slug"],
                    "category": "marker",
                    "provenance": f"{LANE}: grammar first-appearance "
                                 "analysis of rmn.re YOURLS link table",
                    "status": "active",
                },
            },
            "tags": {
                "lane": LANE,
                "grammar": "zz",
                "first_seen": zz["created"],
                "grade": "INFERENCE",
                "evidence_note": "first 'zz'-grammar slug on rmn.re; derived "
                                 "min over 764-slug link table, created is "
                                 "YOURLS-authoritative",
                "timestamp_source": "labels:grammar.created",
            },
        },
        {
            "ref": "reach-availability",
            "kind": "observation",
            "body": {
                "type": "reachability.check",
                "source": "@source",
                "observed_at": probe_at,
                "time_basis": "source_metadata",
                "files": [],
                "data_schema": "urn:factum:web:reachability-check:1",
                "data": {
                    "target": avail["endpoint"],
                    "method": "wayback-availability-api",
                    "outcome": "response",
                },
            },
            "tags": {
                "lane": LANE,
                "grade": "OBSERVED",
                "finding": avail["conclusion"],
                "nearest_snapshot": "20250622062022",
                "probe_dates": "2026-06-17,2026-07-15,2026-09-01",
                "timestamp_source": "labels:probe.attempted_at",
            },
        },
        {
            "ref": "reach-cdx",
            "kind": "observation",
            "body": {
                "type": "reachability.check",
                "source": "@source",
                "observed_at": probe_at,
                "time_basis": "source_metadata",
                "files": [],
                "data_schema": "urn:factum:web:reachability-check:1",
                "data": {
                    "target": cdx["endpoint"],
                    "method": "wayback-cdx-listing",
                    "outcome": "unknown",
                    "error": cdx["result"],
                },
            },
            "tags": {
                "lane": LANE,
                "grade": "OBSERVED",
                "timestamp_source": "labels:probe.attempted_at",
            },
        },
        {
            "ref": "reach-playback",
            "kind": "observation",
            "body": {
                "type": "reachability.check",
                "source": "@source",
                "observed_at": probe_at,
                "time_basis": "source_metadata",
                "files": [],
                "data_schema": "urn:factum:web:reachability-check:1",
                "data": {
                    "target": playback["url"],
                    "method": "wayback-playback",
                    "outcome": "unknown",
                    "error": playback["result"],
                },
            },
            "tags": {
                "lane": LANE,
                "grade": "OBSERVED",
                "timestamp_source": "labels:probe.attempted_at",
            },
        },
    ]

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": IDEMPOTENCY_KEY,
        "records": records,
        "tags": {},
    }
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/rmn-re-history-bundle.json"
    json.dump(bundle, open(out, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {out}: {len(records)} records")


if __name__ == "__main__":
    main()
