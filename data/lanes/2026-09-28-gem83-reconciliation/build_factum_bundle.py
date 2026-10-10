#!/usr/bin/env python3
"""Build the Factum bundle for the 2026-09-28-gem83-reconciliation lane.

83 gem_reconciliation rows -> 83 infra.package observations.

Dedup note: all 83 gem names already exist in Factum as infra.package in
lane 2026-09-29-gem-temporal-pivot, but with DIFFERENT evidence (Diffend
temporal sweep: in_diffend=false, versions=[]). These rows carry the
reconciliation pass evidence (JFrog Xray IDs, versions, june-18 wave,
wayback recovery status, wiki gem-bridge). Per the multi-pass rule, every
pass's evidence is kept; the overlap is annotated in tags, not skipped.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "2026-09-28-gem83-reconciliation"
ACTOR = "agent:lane-ingest-2026-09-28-gem83-reconciliation"
EVENTS = os.path.join(HERE, "events.jsonl")


def stag(d):
    return {k: (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))
            for k, v in d.items() if v is not None}


def main():
    records = []
    records.append({
        "ref": "src",
        "kind": "source",
        "body": {
            "locator": "data/lanes/2026-09-28-gem83-reconciliation/events.jsonl",
            "source_type": "submitted",
        },
        "tags": stag({
            "lane": LANE,
            "grade": "OBSERVED",
            "description": "Aggregate lane: 83-gem June-18 GemStuffer wave "
                           "reconciliation (grammar family ID, JFrog Xray, "
                           "wayback recovery, wiki gem bridge).",
            "legacy_path": "evidence/aggregates/remove-2026-09-28-gem83-reconciliation/events.jsonl",
        }),
    })

    n = 0
    with open(EVENTS) as fh:
        for line in fh:
            d = json.loads(line)
            assert d["record_kind"] == "gem_reconciliation"
            L = d["labels"]
            n += 1
            ver = L.get("gem.versions")
            records.append({
                "ref": "gem_%d" % n,
                "kind": "observation",
                "body": {
                    "type": "infra.package",
                    "data_schema": "urn:factum:infra:package:1",
                    "data": {
                        "name": L.get("gem.package"),
                        "ecosystem": "rubygems",
                        "versions": [ver] if ver else [],
                        "xray_id": L.get("gem.xray_id"),
                        "provenance": "2026-09-28-gem83-reconciliation "
                                      "(nightingale-collective "
                                      "gem83-reconciliation-ingest)",
                    },
                    "observed_at": "2026-06-18T00:00:00Z",
                    "time_basis": "legacy_documented",
                    "source": "@src",
                    "files": [],
                },
                "tags": stag({
                    "lane": LANE,
                    "grade": "OBSERVED",
                    "legacy_kind": "gem_reconciliation",
                    "wave": L.get("gem.wave"),
                    "name_family": L.get("name_family"),
                    "identification_source":
                        L.get("identification_source"),
                    "in_wayback_june_metadata":
                        L.get("in_wayback_june_metadata"),
                    "wayback_recovery_status":
                        L.get("wayback_recovery_status"),
                    "in_wiki_gem_bridge": L.get("in_wiki_gem_bridge"),
                    "wiki_bridge_info": L.get("wiki_bridge_info"),
                    "in_diffend_corpus": L.get("gem.in_diffend_corpus"),
                    "also_observed_in_lane":
                        "2026-09-29-gem-temporal-pivot",
                    "timestamp_source": L.get("timestamp_source"),
                    "legacy_fingerprint": d.get("fingerprint"),
                    "note": d.get("note"),
                }),
            })

    records.append({
        "ref": "run",
        "kind": "run",
        "body": {
            "run_kind": "lane_ingest",
            "tool": "gem83-reconciliation-ingest",
            "tool_version": "1",
            "started": "2026-10-10T06:00:00Z",
            "ended": "2026-10-10T06:30:00Z",
            "params": {
                "lane": LANE,
                "method": "1:1 mapping gem_reconciliation -> infra.package; "
                          "overlap with gem-temporal-pivot annotated per "
                          "multi-pass rule",
                "source_sidecar": "data/lanes/2026-09-28-gem83-reconciliation/events.jsonl",
            },
            "coverage": {"description": "83 reconciliation rows processed.",
                         "scanned": 83, "total": 83, "complete": True},
        },
        "tags": {"lane": LANE, "grade": "OBSERVED"},
    })

    for ref, prop, value in [
        ("claim_coverage", "ingest_coverage",
         {"legacy_events": 83, "submitted_observations": n,
          "skipped_duplicates": 0}),
        ("claim_overlap", "corpus_overlap",
         {"all_83_names_also_in": "2026-09-29-gem-temporal-pivot",
          "note": "Same gem names exist as infra.package from the Diffend "
                  "temporal sweep (in_diffend=false, versions empty). This "
                  "lane adds the reconciliation pass: JFrog Xray IDs, "
                  "versions, june-18 wave, wayback recovery status, wiki "
                  "gem-bridge. Kept per multi-pass rule; overlap annotated "
                  "in tags.also_observed_in_lane."}),
    ]:
        records.append({
            "ref": ref, "kind": "claim",
            "body": {"subject": "@run", "property": prop, "value": value,
                     "basis": "OBSERVED", "cites": ["@run"]},
            "tags": {"lane": LANE, "grade": "OBSERVED"},
        })

    bundle = {"bundle": 2, "idempotency_key": LANE + "-v1",
              "actor": ACTOR, "records": records}
    json.dump(bundle, open(os.path.join(HERE, "bundle.json"), "w"),
              indent=1, ensure_ascii=False)
    print("records:", len(records), "gems:", n)


if __name__ == "__main__":
    main()
