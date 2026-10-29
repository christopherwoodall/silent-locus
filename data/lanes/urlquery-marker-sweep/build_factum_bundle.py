#!/usr/bin/env python3
"""Factum ingest bundle builder for the urlquery-marker-sweep lane.

Reads data/lanes/urlquery-marker-sweep/events.jsonl (975 venue_finding events)
and emits one Factum bundle (JSON) on stdout.

Record model (settled 2026-10-10):
- 1 run        : the sweep extraction run, with honest coverage (966/967).
- 1 source     : the lane artifacts (events.jsonl + raw/).
- 4 infra.ioc  : one per distinct marker term. term is the ACTUAL marker
                 value, never an internal id (schema-mapping rule). Batch
                 deduped by (term, category).
- 9 claims     : one per curated graded venue finding (analyst verdicts),
                 with byte-identical notes/matched strings.
- 1 claim      : aggregate coverage verdict for the 966 low-grade
                 unscoped-"exploitgym" pagination hits (aggregation strategy
                 for the bulk; per-report rows stay in the lane artifacts).

Every record carries tags.lane = "urlquery-marker-sweep". No edges are
created during ingest (no top-level "lane" key on the bundle).
"""

import json
import sys
from pathlib import Path

LANE = "urlquery-marker-sweep"
ACTOR = "agent:lane-ingest-2025-12-04-urlquery-marker-sweep"
IDEMPOTENCY_KEY = "urlquery-marker-sweep-ingest-2026-10-10"
LANE_DIR = Path(__file__).resolve().parent
EVENTS = LANE_DIR / "events.jsonl"

MARKER_STATUS = {
    # (status, status rationale)
    "exploitgym": (
        "noisy",
        "966 low-grade search-index-only hits; match location not verifiable "
        "via the public report API; none tied to incident traffic.",
    ),
    "cybergym": (
        "noisy",
        "5 hits: 3 benign (newsletter clickthrough, public repo scan, forum "
        "mention), 1 context-only curiosity probe, 1 low-grade; none incident "
        "traffic.",
    ),
    "catflag": (
        "candidate",
        "1 low-grade search-index-only hit; unverifiable via public API.",
    ),
    "restart_server": (
        "retired",
        "3 benign hits; all generic ops UI text (Cronicle, Splunk, AI support "
        "tool). Refuted as an ExploitGym controller-traffic marker.",
    ),
}


def load_events():
    events = []
    with open(EVENTS, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events


def main():
    events = load_events()
    assert len(events) == 975, f"expected 975 events, got {len(events)}"

    curated = [e for e in events if e["labels"]["marker"] != "exploitgym"]
    bulk = [e for e in events if e["labels"]["marker"] == "exploitgym"]
    assert len(curated) == 9, f"expected 9 curated, got {len(curated)}"
    assert len(bulk) == 966, f"expected 966 bulk, got {len(bulk)}"

    # Within-batch dedup check: distinct markers must be unique terms.
    markers = sorted({e["labels"]["marker"] for e in events})
    assert markers == ["catflag", "cybergym", "exploitgym", "restart_server"], markers

    # Distinct report ids across the batch (no dupes).
    rids = [e["labels"]["report_id"] for e in events]
    assert len(set(rids)) == 975, "duplicate report_id within batch"

    records = []

    def tagged(extra):
        t = {"lane": LANE}
        t.update(extra)
        return t

    # 1. run
    records.append({
        "kind": "run",
        "ref": "run",
        "tags": tagged({"grade": "OBSERVED"}),
        "body": {
            "run_kind": "extraction",
            "tool": "build_factum_bundle.py (data/lanes/urlquery-marker-sweep)",
            "params": {
                "question": "Test whether third-party urlquery.net scans caught "
                            "ExploitGym incident traffic (Lead 4/6).",
                "source_corpus": "urlquery.net public report corpus via "
                                 "uq.py search (read-only, Secure Vault "
                                 "surrogate auth).",
                "queries": "sweep v1: 15 queries; v2: 19 queries "
                           "(corrected quoted/explicit-AND syntax); v3: 1 "
                           "query; full pagination of unscoped 'exploitgym' "
                           "(32 pages, offsets 30..960, 2026-09-29).",
                "event_count": 975,
            },
            "coverage": {
                "description": "975 venue_finding events: 966 one-per-hit "
                               "unscoped-'exploitgym' pagination hits "
                               "(evidence_grade=low, search-index match only) "
                               "+ 9 curated graded findings (cybergym x5, "
                               "catflag x1, restart_server x3). Pagination "
                               "captured 966/967 distinct report ids; 1 hit "
                               "not addressable via stable pagination "
                               "(result-window drift).",
                "scanned": 975,
                "total": 975,
                "complete": False,
            },
        },
    })

    # 2. source
    records.append({
        "kind": "source",
        "ref": "source",
        "tags": tagged({"grade": "OBSERVED"}),
        "body": {
            "locator": "data/lanes/urlquery-marker-sweep/events.jsonl",
            "source_type": "submitted",
            "title": "2025-12-04 urlquery marker sweep: 975 venue_finding "
                     "events (966 unscoped-exploitgym pagination hits + 9 "
                     "curated graded findings); raw API responses in raw/",
        },
    })

    # 3. one infra.ioc per distinct marker term (term = actual IOC value).
    # observed_at is REQUIRED by the observation schema; it is grounded in
    # the lane's documented event.created (2026-09-29 backfill), not invented.
    for marker in markers:
        status, rationale = MARKER_STATUS[marker]
        records.append({
            "kind": "observation",
            "ref": f"ioc-{marker}",
            "tags": tagged({
                "grade": "OBSERVED",
                "legacy_kind": "derived_marker_term",
                "status_rationale": rationale,
            }),
            "body": {
                "type": "infra.ioc",
                "data_schema": "urn:factum:infra:ioc:1",
                "data": {
                    "term": marker,
                    "category": "marker",
                    "provenance": "2025-12-04-urlquery-marker-sweep",
                    "status": status,
                },
                "observed_at": "2026-09-29T09:52:12Z",
                "time_basis": "source_metadata",
                "files": [],
                "source": "@source",
            },
        })

    # 4. one claim per curated graded finding; verdict text byte-identical
    for e in sorted(curated, key=lambda x: x["labels"]["report_id"]):
        lab = e["labels"]
        records.append({
            "kind": "claim",
            "ref": f"claim-{lab['report_id'][:8]}",
            "tags": tagged({
                "grade": "OBSERVED",
                "legacy_kind": "venue_finding",
                "legacy_fingerprint": e["fingerprint"],
            }),
            "body": {
                "subject": "@run",
                "property": "venue_finding_verdict",
                "value": {
                    "report_id": lab["report_id"],
                    "report_url": e["source_url"],
                    "marker": lab["marker"],
                    "evidence_grade": lab["evidence_grade"],
                    "match_location": lab["location"],
                    "matched_string": e.get("matched_string"),
                    "scan_time": e["@timestamp"],
                    "verdict": e["note"],
                },
                "basis": "OBSERVED",
                # cites must target observation/sighting/artifact/claim/run
                # (the citations def rejects source-kind records); the claim
                # interprets the marker-term observation for this finding.
                "cites": [f"@ioc-{lab['marker']}"],
            },
        })

    # 5. aggregate coverage claim for the 966 bulk hits
    records.append({
        "kind": "claim",
        "ref": "claim-sweep-coverage",
        "tags": tagged({"grade": "OBSERVED"}),
        "body": {
            "subject": "@run",
            "property": "sweep_coverage",
            "value": {
                "query": '"exploitgym" (unscoped, quoted)',
                "total_hits_reported": 967,
                "captured_distinct_report_ids": 966,
                "capture_gap": "1 hit not addressable via stable pagination "
                               "(off-0 page returned 29 rows; probe at "
                               "offset 966 returned an id already seen on "
                               "off-960: result-window drift).",
                "evidence_grade": "low",
                "verifiability": "search-index match only (captured HTML/JS "
                                 "text); match location not verifiable via "
                                 "the public report API.",
                "scan_time_range": "2026-05-27T07:25:18Z to 2026-09-28T14:17:49Z",
                "verdict": "No verifiable ExploitGym incident traffic in the "
                           "966 captured hits.",
            },
            "basis": "OBSERVED",
            "cites": ["@ioc-exploitgym"],
        },
    })

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": IDEMPOTENCY_KEY,
        "records": records,
    }

    # ---- adversarial self-checks (cleaner/validator) ----
    errors = []

    # A. every record tagged with the lane
    for r in records:
        if r.get("tags", {}).get("lane") != LANE:
            errors.append(f"missing lane tag: {r.get('ref')}")

    # B. no duplicate (term, category) within batch
    seen_terms = {}
    for r in records:
        d = r.get("body", {}).get("data", {})
        if "term" in d:
            key = (d["term"], d.get("category"))
            if key in seen_terms:
                errors.append(f"duplicate term in batch: {key}")
            seen_terms[key] = r["ref"]
            # C. term is the actual IOC value, never an internal id
            if key[0] not in MARKER_STATUS:
                errors.append(f"term is not a known marker value: {key[0]!r}")
            if "-" in key[0] and len(key[0]) == 36:
                errors.append(f"term looks like a report UUID (internal id): {key[0]}")

    # D. bundle envelope
    if bundle["bundle"] != 2:
        errors.append("bundle version != 2")
    if not bundle["actor"] or not bundle["idempotency_key"]:
        errors.append("actor/idempotency_key missing")
    if "lane" in bundle:
        errors.append("top-level lane key would create edges during ingest")

    # E. refs resolve
    refs = {r["ref"] for r in records}

    def check_refs(obj, where):
        if isinstance(obj, str) and obj.startswith("@"):
            if obj[1:] not in refs:
                errors.append(f"dangling @ref {obj} in {where}")
        elif isinstance(obj, dict):
            for v in obj.values():
                check_refs(v, where)
        elif isinstance(obj, list):
            for v in obj:
                check_refs(v, where)

    for r in records:
        check_refs(r["body"], r["ref"])

    # F. verbatim check: claim verdicts byte-identical to source events
    by_fp = {e["fingerprint"]: e for e in curated}
    for r in records:
        if r["kind"] == "claim" and r["ref"].startswith("claim-") and r["ref"] != "claim-sweep-coverage":
            fp = r["tags"]["legacy_fingerprint"]
            src = by_fp.get(fp)
            if src is None:
                errors.append(f"claim {r['ref']}: fingerprint not found in events")
                continue
            v = r["body"]["value"]
            if v["verdict"] != src["note"]:
                errors.append(f"claim {r['ref']}: verdict != source note (not verbatim)")
            if v["matched_string"] != src.get("matched_string"):
                errors.append(f"claim {r['ref']}: matched_string != source (not verbatim)")
            if v["match_location"] != src["labels"]["location"]:
                errors.append(f"claim {r['ref']}: match_location != source labels.location")
            if v["report_url"] != src["source_url"]:
                errors.append(f"claim {r['ref']}: report_url != source source_url")

    # G. expected record counts by kind
    kinds = {}
    for r in records:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    expected = {"run": 1, "source": 1, "observation": 4, "claim": 10}
    if kinds != expected:
        errors.append(f"record counts {kinds} != expected {expected}")

    # H2. cites must never target source-kind records: the citations def only
    #     accepts observation/sighting/artifact/claim/run (REFERENCE_TYPE
    #     failure at submit, found 2026-10-10). Claims cite observations;
    #     the source record is linked via observation.body.source.
    ref_kinds = {r["ref"]: r["kind"] for r in records}
    for r in records:
        for c in r.get("body", {}).get("cites", []):
            if c.startswith("@") and ref_kinds.get(c[1:]) == "source":
                errors.append(f"{r['ref']}: cites source-kind record {c}")

    # H. observation schema REQUIRES observed_at + time_basis (the template
    #    scaffold omits them); the value must be grounded, not invented.
    for r in records:
        if r["kind"] == "observation":
            b = r.get("body", {})
            if not b.get("observed_at") or not b.get("time_basis"):
                errors.append(f"{r['ref']}: observation missing observed_at/time_basis")
            elif b["time_basis"] not in ("collector_clock", "source_metadata",
                                         "source_text", "legacy_documented",
                                         "received_by_factum", "unknown"):
                errors.append(f"{r['ref']}: bad time_basis {b['time_basis']}")

    if errors:
        print("VALIDATOR FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"validator passed: {len(records)} records "
          f"({kinds['run']} run, {kinds['source']} source, "
          f"{kinds['observation']} infra.ioc, {kinds['claim']} claims)",
          file=sys.stderr)
    json.dump(bundle, sys.stdout, ensure_ascii=False, indent=1)
    print(file=sys.stdout)


if __name__ == "__main__":
    main()
