#!/usr/bin/env python3
"""Build the AIID full-site IOC Factum bundle (infra.ioc observations).

Input: reports/aiid-full-site/iocs.json (verified on disk).
Output: reports/aiid-full-site/ioc-bundle.json (bundle v2, NOT submitted by
this script; submission is a separate Factum `add --input` step).

Mapping (documented, no upgrades):
- term: iocs.json value, verbatim.
- category: iocs.json kind, verbatim (url, domain, hash, file_path, ip,
  model, model_or_tool, tool). tags.kind duplicates it for filtering.
- provenance: AIID snapshot stamp + incident IDs + full report-page URLs
  (https://incidentdatabase.ai/reports/<id>) + ranked rank_reason where
  present + a low-confidence flag note where confidence is low.
- status: high -> active, medium -> active, low -> candidate. The exact
  confidence is always preserved in tags.confidence, so a low-confidence
  IOC is never upgraded: it stays candidate + confidence=low.
- observed_at: the AIID snapshot stamp 2026-10-26 10:15, rendered as
  2026-10-26T10:15:00Z to satisfy the date-time format (the source stamp
  carries no timezone; the Z rendering is noted in the ingest report).
  time_basis: source_metadata.
- tags on EVERY record: lane=aiid-full-site, grade=SECONDARY, kind,
  confidence, ranked_agent_relevant=true/false.
- One shared source record (ref "aiid") for the AIID database; every
  observation cites it via "@aiid". No top-level "lane" key: prior
  incident batch (fc09b8bfbd7b4d719e070fed0d5c4d49) also used tags.lane
  only, with no in_lane edge records.
- Dedup: 0 skips. Direct scan of data/records/ found no existing
  infra.ioc record with a ranked term + AIID provenance (see ingest
  report section). The 3 same-term infra.ioc records in other lanes
  carry non-AIID provenance (HF traces / OpenAI blog) = new sightings.
  The 1 same-term non-IOC record (Claude Code intel.behavior in the
  incident-7050 lane, provenance "AIID incident 1424") is a behavior
  record, not an IOC sighting, and does not cover this batch's
  23-incident IOC aggregation; it is logged, not treated as a skip.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
IOC_PATH = REPO / "reports" / "aiid-full-site" / "iocs.json"
OUT_PATH = REPO / "reports" / "aiid-full-site" / "ioc-bundle.json"

STATUS = {"high": "active", "medium": "active", "low": "candidate"}
OBSERVED_AT = "2026-10-26T10:15:00Z"


def main() -> None:
    data = json.loads(IOC_PATH.read_text())
    full = data["full_set"]
    ranked_keys = {(e["kind"], e["value"]) for e in data["ranked_agent_relevant"]}
    ranked_reason = {(e["kind"], e["value"]): e.get("rank_reason", "")
                     for e in data["ranked_agent_relevant"]}

    # Within-batch dedup by (kind, value): full_set must already be distinct.
    seen = set()
    for e in full:
        key = (e["kind"], e["value"])
        assert key not in seen, f"duplicate (kind, value) in full_set: {key}"
        seen.add(key)
        assert e["confidence"] in STATUS, e
        assert e["incident_ids"] and e["report_ids"], e

    records = [{
        "ref": "aiid",
        "kind": "source",
        "body": {
            "locator": "https://incidentdatabase.ai/",
            "platform": "AI Incident Database",
            "source_type": "aiid-full-site",
            "title": "AI Incident Database - full-site snapshot 2026-10-26",
        },
        "tags": {"lane": "aiid-full-site", "grade": "SECONDARY"},
    }]

    for i, e in enumerate(full, start=1):
        key = (e["kind"], e["value"])
        ranked = key in ranked_keys
        inc = ",".join(str(x) for x in e["incident_ids"])
        reps = ",".join(f"https://incidentdatabase.ai/reports/{r}"
                        for r in e["report_ids"])
        prov = (f"AIID full-site snapshot 2026-10-26 10:15; "
                f"AIID incident IDs: {inc}; "
                f"AIID report pages: {reps}.")
        if ranked and ranked_reason.get(key):
            prov += f" Ranked agent-relevant: {ranked_reason[key]}."
        if e["confidence"] == "low":
            prov += (" Low confidence per IOC caveats (unverified hash "
                     "strings, quoted-address IPs, page-template URLs); "
                     "kept and flagged, not upgraded.")
        records.append({
            "ref": f"ioc{i:05d}",
            "kind": "observation",
            "body": {
                "type": "infra.ioc",
                "data_schema": "urn:factum:infra:ioc:1",
                "files": [],
                "source": "@aiid",
                "observed_at": OBSERVED_AT,
                "time_basis": "source_metadata",
                "data": {
                    "term": e["value"],
                    "category": e["kind"],
                    "provenance": prov,
                    "status": STATUS[e["confidence"]],
                },
            },
            "tags": {
                "lane": "aiid-full-site",
                "grade": "SECONDARY",
                "kind": e["kind"],
                "confidence": e["confidence"],
                "ranked_agent_relevant": "true" if ranked else "false",
            },
        })

    bundle = {
        "bundle": 2,
        "actor": "agent:aiid-full-site-ioc-ingest",
        "idempotency_key": "aiid-full-site-ioc-ingest-v1",
        "records": records,
    }
    OUT_PATH.write_text(json.dumps(bundle, ensure_ascii=False, indent=1))
    print(f"records: {len(records)} (1 source + {len(full)} observations)")
    print(f"wrote: {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    sys.exit(main())
