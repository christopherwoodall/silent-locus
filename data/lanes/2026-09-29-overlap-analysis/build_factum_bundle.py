#!/usr/bin/env python3
"""Build the Factum bundle for the 2026-09-29-overlap-analysis aggregate lane.

AGGREGATION (not 1:1): 17,038 overlap_match rows (= 7,982 unique matches;
matches-f5f6.jsonl and overlap-matches.jsonl carry the same rows) collapse to
  - 1 run record (the analysis),
  - 1 source record (lane locator),
  - 15 infra.ioc observations (confirmed-present IOCs: F1 httpbun.com,
    F3 zz tokens, F6 beacon hosts, F5 64H-series stems),
  - 8 OBSERVED claims (coverage + per-family findings + paste links).

Miss-kind terms (confirmed absent from the 189,579-record dataset) are not
minted as IOCs -- there is no "absent" status; the negative findings live in
the family claims. github-remote-cache/zz is already an infra.ioc in the
corpus: skipped, annotated in the F3/F6 claims.
"""
import json
import os
import re
from collections import Counter, defaultdict
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "2026-09-29-overlap-analysis"
ACTOR = "agent:lane-ingest-2026-09-29-overlap-analysis"
EVENTS = os.path.join(HERE, "events.jsonl")
OBS_AT = "2026-09-29T00:00:00Z"


def stag(d):
    return {k: (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))
            for k, v in d.items() if v is not None}


def analyze():
    """Independent derivation of the aggregation inputs from events.jsonl."""
    seen = {}
    paste = []
    with open(EVENTS) as fh:
        for line in fh:
            d = json.loads(line)
            if d["record_kind"] == "overlap_match":
                if d["fingerprint"] not in seen:
                    seen[d["fingerprint"]] = d
            elif d["record_kind"] == "paste_link":
                paste.append(d)
    famkind = Counter()
    famids = defaultdict(set)
    stems = Counter()
    for d in seen.values():
        L = d["labels"]
        fam = L.get("match.family")
        famkind[(fam, L.get("match.kind"))] += 1
        if L.get("swarmtraces.id"):
            famids[fam].add(L["swarmtraces.id"])
        if fam == "F5":
            m = re.match(r"^(\S+) as stem in", L.get("evidence") or "")
            if m:
                stems[m.group(1)] += 1
    return seen, paste, famkind, famids, stems


IOCS = [
    # (term, category, family, note)
    ("httpbun.com", "domain", "F1",
     "structural: httpbun literal 628x across dataset; zero /base64/ URLs "
     "(recon Host-header/DNS use per verification)"),
    ("zzWAFBRIDGE25167", "marker", "F3",
     "exact: 7 occurrences in dataset records"),
    ("zzHFPOSTRCE_WT8592N19_BEACON_", "marker", "F3",
     "exact: 2 occurrences in dataset records"),
    ("packages.hub.ace-research.openai.org", "domain", "F6",
     "beacon_path host in F6 github-remote-cache/zz matches"),
    ("packages.app.ace-research.openai.org", "domain", "F6",
     "beacon_path host in F6 matches"),
]


def main():
    seen, paste, famkind, famids, stems = analyze()
    total_rows = 17038  # per PROVENANCE file inventory

    records = []
    records.append({
        "ref": "src",
        "kind": "source",
        "body": {
            "locator": "data/lanes/2026-09-29-overlap-analysis/events.jsonl",
            "source_type": "submitted",
        },
        "tags": stag({
            "lane": LANE,
            "grade": "OBSERVED",
            "description": "Aggregate lane: cross-corpus overlap/pivot "
                           "analysis (hunt markers vs 189,579-record HF "
                           "redacted corpus). IOCs + summary claims in "
                           "Factum; full rows in lane artifacts.",
            "legacy_path": "evidence/aggregates/remove-2026-09-29-overlap-analysis/events.jsonl",
        }),
    })

    i = 0
    for term, cat, fam, note in IOCS:
        i += 1
        records.append({
            "ref": "ioc_%d" % i,
            "kind": "observation",
            "body": {
                "type": "infra.ioc",
                "data_schema": "urn:factum:infra:ioc:1",
                "data": {"term": term, "category": cat,
                         "provenance": LANE, "status": "active"},
                "observed_at": OBS_AT,
                "time_basis": "legacy_documented",
                "source": "@src",
                "files": [],
            },
            "tags": stag({"lane": LANE, "grade": "OBSERVED",
                          "match_family": fam, "evidence_note": note}),
        })
    for stem in sorted(stems):
        i += 1
        records.append({
            "ref": "ioc_%d" % i,
            "kind": "observation",
            "body": {
                "type": "infra.ioc",
                "data_schema": "urn:factum:infra:ioc:1",
                "data": {"term": stem, "category": "marker",
                         "provenance": LANE, "status": "active"},
                "observed_at": OBS_AT,
                "time_basis": "legacy_documented",
                "source": "@src",
                "files": [],
            },
            "tags": stag({
                "lane": LANE, "grade": "OBSERVED",
                "match_family": "F5",
                "evidence_note": "64H-series catalog stem: %d contextual "
                                 "matches in dataset payloads" % stems[stem],
                "match_count": stems[stem]}),
        })

    records.append({
        "ref": "run",
        "kind": "run",
        "body": {
            "run_kind": "lane_aggregation",
            "tool": "overlap-analysis-aggregate",
            "tool_version": "1",
            "started": "2026-10-10T06:00:00Z",
            "ended": "2026-10-10T06:30:00Z",
            "params": {
                "lane": LANE,
                "method": "dedupe overlap_match rows by fingerprint "
                          "(matches-f5f6.jsonl and overlap-matches.jsonl "
                          "carry the same rows); per-family kind counts; "
                          "confirmed-present IOCs as infra.ioc; miss-kind "
                          "terms covered in claims",
                "source_sidecar": "data/lanes/2026-09-29-overlap-analysis/events.jsonl",
            },
            "coverage": {
                "description": "17,038 overlap_match rows (7,982 unique) + "
                               "317 paste_link rows aggregated.",
                "scanned": 17355, "total": 17355, "complete": True},
        },
        "tags": {"lane": LANE, "grade": "OBSERVED"},
    })

    def fk(fam):
        return {k: v for (f, k), v in famkind.items() if f == fam}

    paste_ids = {p["labels"].get("paste.id") for p in paste}
    link_types = Counter(p["labels"].get("link.type") for p in paste)
    claims = [
        ("claim_coverage", "overlap_coverage", {
            "overlap_match_rows": total_rows,
            "unique_matches": len(seen),
            "dedup_note": "every fingerprint appears twice: "
                          "matches-f5f6.jsonl and overlap-matches.jsonl "
                          "carry the same rows (per lane PROVENANCE)",
            "paste_link_rows": len(paste),
            "dataset": "189,579-record HF redacted corpus",
            "analysis_date": "2026-09-29",
        }),
        ("claim_f1", "family_f1_markers", {
            "unique": sum(fk("F1").values()), "kinds": fk("F1"),
            "finding": "httpbun.com structurally present (628x); 6 hunt "
                       "markers confirmed absent (incl. api.browserless.io, "
                       "pp.aihw.gov.au)",
        }),
        ("claim_f2", "family_f2_epochs", {
            "unique": sum(fk("F2").values()), "kinds": fk("F2"),
            "finding": "12 epoch markers absent from dataset epoch set "
                       "(1,206 distinct epochs); 3 near-misses",
        }),
        ("claim_f3", "family_f3_board_path", {
            "unique": sum(fk("F3").values()), "kinds": fk("F3"),
            "finding": "github-remote-cache/zz literal present in dataset "
                       "text (strongest cross-corpus link per hunt notes); "
                       "zzWAFBRIDGE25167 (7x) and "
                       "zzHFPOSTRCE_WT8592N19_BEACON_ (2x) exact tokens; "
                       "5 family-kind, 5 miss",
            "overlap_note": "github-remote-cache/zz already an infra.ioc "
                            "in the corpus: no duplicate submitted",
        }),
        ("claim_f5", "family_f5_64h_stems", {
            "unique": sum(fk("F5").values()), "kinds": fk("F5"),
            "distinct_dataset_records": len(famids["F5"]),
            "stems": dict(stems),
            "finding": "64H-series catalog stems in dataset payloads "
                       "(docker layer authors, code literals); 2 pre-screen "
                       "misses (Future9180, SC4: zero hits via bounded-token "
                       "regex) vs contextual stem hits recorded as found",
        }),
        ("claim_f6", "family_f6_beacon_paths", {
            "unique": sum(fk("F6").values()), "kinds": fk("F6"),
            "distinct_dataset_records": len(famids["F6"]),
            "finding": "7,020 exact github-remote-cache/zz beacon-path "
                       "matches (packages.hub.ace-research.openai.org "
                       "artifactory paths) across 2,700 dataset records",
        }),
        ("claim_negative", "negative_sweeps", {
            "families": {f: {"unique": sum(fk(f).values()),
                             "kinds": fk(f)}
                         for f in ("ntfy-topic", "ittybitty-fragment",
                                   "tableau-marker", "webhook-delete",
                                   "counterapi", "translate-launder")},
            "finding": "hunt markers confirmed absent from all 189,579 "
                       "records (ntfy topics, itty.bitty, tableau "
                       "endpoints, webhook.site inboxes, counterapi "
                       "namespaces, translate.launder hosts). webhook-delete "
                       "adds 16 structural-pattern hits: method:'DELETE' "
                       "fetch evidence-destruction TTP in dataset payloads",
        }),
        ("claim_paste", "paste_link_coverage", {
            "rows": len(paste),
            "distinct_paste_ids": len(paste_ids),
            "link_types": dict(link_types),
            "finding": "collusion-wiki records referencing pastes "
                       "(corpus_record / task_family / shared_host links)",
        }),
    ]
    for ref, prop, value in claims:
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
    print("records:", len(records), "iocs:", i, "claims:", len(claims),
          "unique matches:", len(seen))


if __name__ == "__main__":
    main()
