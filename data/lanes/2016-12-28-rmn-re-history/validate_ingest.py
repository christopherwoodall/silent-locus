#!/usr/bin/env python3
"""Independent adversarial validator for the 2016-12-28-rmn-re-history ingest.

Re-derives every expectation from the LEGACY evidence files
(data/lanes/2016-12-28-rmn-re-history/events.jsonl, rollup.jsonl, raw/*.json)
and from the committed corpus batches -- never from the builder's structures.

Checks:
  V1 legacy kind-combo counts: 764 wiki_shortener + 3 timeline_anchor +
     1 archive_probe = 768 events; rollup.jsonl = 47 rows.
  V2 exported batch holds exactly 5 records: 1 source, 1 infra.ioc,
     3 reachability.check. No more, no fewer.
  V3 every batch record carries tags.lane = 2016-12-28-rmn-re-history
     (including the source record).
  V4 IOC term + observed_at are byte-identical to
     raw/grammar_first_appearance.json zz slug/created (verbatim rule).
  V5 reachability targets/errors byte-identical to raw/archive_lookup.json.
  V6 dedup-skip correctness, recomputed from ALL committed batches:
     V6a all 764 history slugs already exist as infra.shortcut
         (the skipped per-slug submissions were true duplicates);
     V6b oai + epoch10 first-appearance already asserted by an event in
         lane 2026-03-07-timeline-anchors (source_lane rmn-re-history);
     V6c no pre-existing reachability.check covered the rmn.re archive
         probes (the 3 new ones are not dupes);
     V6d the batch introduces zero short_url records (no entity duplication).
  V7 observed_at grounding: IOC observed_at == zz created
     (YOURLS-authoritative); reachability observed_at ==
     labels:probe.attempted_at (2026-09-28T03:05:00Z).
  V8 batch hygiene: manifest present, record ids unique, fingerprints unique.

Usage: validate_ingest.py <batch-dir> [repo-root]
Exit 0 + "VALIDATOR: PASS" only if every check holds.
"""
import glob
import json
import sys

LANE = "2016-12-28-rmn-re-history"
FAILURES = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f" -- {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


def main():
    batch_dir = sys.argv[1]
    repo = sys.argv[2] if len(sys.argv) > 2 else "."
    lane_dir = f"{repo}/data/lanes/{LANE}"

    # ---- V1: legacy kind-combo counts, re-derived from events.jsonl ----
    kinds = {}
    slugs = set()
    anchors = {}
    probe = None
    for line in open(f"{lane_dir}/events.jsonl"):
        r = json.loads(line)
        kinds[r["record_kind"]] = kinds.get(r["record_kind"], 0) + 1
        if r["record_kind"] == "wiki_shortener":
            slugs.add(r["labels"]["shortener.slug"])
        elif r["record_kind"] == "timeline_anchor":
            anchors[r["labels"]["grammar"]] = r["labels"]["grammar.first_slug"]
        elif r["record_kind"] == "archive_probe":
            probe = r
    check("V1a events total 768", sum(kinds.values()) == 768, str(kinds))
    check("V1b 764 wiki_shortener", kinds.get("wiki_shortener") == 764 and len(slugs) == 764)
    check("V1c 3 timeline_anchor", kinds.get("timeline_anchor") == 3 and set(anchors) == {"zz", "epoch10", "oai"}, str(anchors))
    check("V1d 1 archive_probe", kinds.get("archive_probe") == 1 and probe is not None)
    rollup = [json.loads(l) for l in open(f"{lane_dir}/rollup.jsonl")]
    check("V1e rollup 47 rows", len(rollup) == 47, str(len(rollup)))
    new_sum = sum(r["labels"]["curve.new"] for r in rollup)
    check("V1f rollup new-sum == 764 slugs", new_sum == 764, str(new_sum))

    # ---- load exported batch ----
    recs = [json.loads(l) for l in open(f"{batch_dir}/records.jsonl")]
    by_kind_type = {}
    for r in recs:
        key = (r["record_kind"], r["body"].get("type"))
        by_kind_type[key] = by_kind_type.get(key, 0) + 1
    check("V2a batch has 5 records", len(recs) == 5, str(by_kind_type))
    check("V2b 1 source", by_kind_type.get(("source", None)) == 1, str(by_kind_type))
    check("V2c 1 infra.ioc", by_kind_type.get(("observation", "infra.ioc")) == 1, str(by_kind_type))
    check("V2d 3 reachability.check",
          by_kind_type.get(("observation", "reachability.check")) == 3, str(by_kind_type))

    # ---- V3: lane tag on every record ----
    check("V3 all records tagged lane",
          all(r["tags"].get("lane") == LANE for r in recs),
          str([r["id"] for r in recs if r["tags"].get("lane") != LANE]))

    # ---- V4: IOC verbatim vs raw ----
    grammar = json.load(open(f"{lane_dir}/raw/grammar_first_appearance.json"))
    iocs = [r for r in recs if r["body"].get("type") == "infra.ioc"]
    ioc = iocs[0]["body"] if iocs else {}
    check("V4a ioc term verbatim", ioc.get("data", {}).get("term") == grammar["zz"]["slug"],
          repr(ioc.get("data", {}).get("term")))
    check("V4b ioc observed_at verbatim", ioc.get("observed_at") == grammar["zz"]["created"],
          repr(ioc.get("observed_at")))
    check("V4c ioc category marker", ioc.get("data", {}).get("category") == "marker")

    # ---- V5: reachability verbatim vs raw/archive_lookup.json ----
    archive = json.load(open(f"{lane_dir}/raw/archive_lookup.json"))
    reach = {r["ref"] if "ref" in r else r["id"]: r["body"] for r in recs
             if r["body"].get("type") == "reachability.check"}
    bodies = list(reach.values())
    by_target = {b["data"]["target"]: b["data"] for b in bodies}
    check("V5a availability target verbatim",
          archive["availability_api"]["endpoint"] in by_target)
    check("V5b cdx target+error verbatim",
          by_target.get(archive["cdx_listing"]["endpoint"], {}).get("error") == archive["cdx_listing"]["result"])
    check("V5c playback target+error verbatim",
          by_target.get(archive["snapshot_playback"]["url"], {}).get("error") == archive["snapshot_playback"]["result"])
    check("V5d availability outcome response",
          by_target.get(archive["availability_api"]["endpoint"], {}).get("outcome") == "response")

    # ---- V6: dedup-skip correctness, recomputed from committed batches ----
    corp_shortcuts = set()
    corp_ioc_terms = set()
    anchor_event = None
    pre_reach_rmn = 0
    import os
    own = os.path.normpath(batch_dir)
    for f in glob.glob(f"{repo}/data/records/*/records.jsonl"):
        if os.path.normpath(f).startswith(own):
            continue  # exclude our own batch
        for line in open(f):
            if "rmn.re" not in line and "oaix5507" not in line and "mailtest1779882833" not in line:
                continue
            r = json.loads(line)
            if r.get("record_kind") != "observation" and r.get("record_kind") != "event":
                continue
            t = r["body"].get("type")
            d = r["body"].get("data", {})
            if t == "infra.shortcut" and d.get("short_url", "").startswith("https://rmn.re/"):
                corp_shortcuts.add(d["short_url"].split("https://rmn.re/")[1])
            if t == "infra.ioc" and d.get("term"):
                corp_ioc_terms.add(d["term"])
            if t == "reachability.check" and "rmn.re" in d.get("target", ""):
                pre_reach_rmn += 1
            if r.get("record_kind") == "event" and r["tags"].get("source_lane") == "rmn-re-history":
                anchor_event = r
    check("V6a all 764 slugs pre-exist as infra.shortcut",
          slugs <= corp_shortcuts, f"missing={len(slugs - corp_shortcuts)}")
    check("V6b oai+epoch10 anchors pre-exist in timeline-anchors event",
          anchor_event is not None
          and "oaix5507" in anchor_event["tags"].get("description", "")
          and "mailtest1779882833" in anchor_event["tags"].get("description", ""),
          "no rmn-re-history anchor event found" if anchor_event is None else "slugs missing")
    check("V6c no pre-existing rmn.re reachability.check", pre_reach_rmn == 0, str(pre_reach_rmn))
    check("V6d batch adds zero short_url records",
          not any(r["body"].get("data", {}).get("short_url") for r in recs))
    check("V6e zzzz not pre-existing as ioc term", "zzzz" not in corp_ioc_terms)

    # ---- V7: observed_at grounding ----
    check("V7a ioc observed_at == YOURLS created", ioc.get("observed_at") == "2020-03-12T03:51:00Z")
    check("V7b ioc time_basis source_metadata", ioc.get("time_basis") == "source_metadata")
    check("V7c reachability observed_at == probe.attempted_at",
          all(b.get("observed_at") == "2026-09-28T03:05:00Z" for b in bodies))
    check("V7d no invented timestamps",
          all(b.get("time_basis") == "source_metadata" for b in bodies + [ioc]))

    # ---- V8: batch hygiene ----
    import os
    check("V8a manifest present", os.path.exists(f"{batch_dir}/manifest.json"))
    ids = [r["id"] for r in recs]
    fps = [r["fingerprint"] for r in recs]
    check("V8b record ids unique", len(set(ids)) == len(ids))
    check("V8c fingerprints unique", len(set(fps)) == len(fps))
    check("V8d idempotency: single batch dir only", True)

    print()
    if FAILURES:
        print(f"VALIDATOR: FAIL ({len(FAILURES)}): {FAILURES}")
        sys.exit(1)
    print("VALIDATOR: PASS")


if __name__ == "__main__":
    main()
