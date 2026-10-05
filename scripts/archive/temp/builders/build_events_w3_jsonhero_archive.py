#!/usr/bin/env python3
"""Build events.jsonl + rollup.jsonl for data/2025-01-13-jsonhero-docs-archive.

Worker W3, 2026-09-29. Usage: python3 temp/build_events_w3_jsonhero_archive.py <repo_root>

Inputs (all under data/2025-01-13-jsonhero-docs-archive/raw/):
  manifest.json                 - per-doc recovery table (6 docs): the pre-schema source
  swJMw8b6VwDC.json            - recovered doc payload (from Wayback capture)
  swJMw8b6VwDC_20260912075005.html - raw Wayback capture bytes

Grain: one record per doc (kind=artifact_observation), mirroring the sibling
dataset 2026-09-28-jsonhero-docs (same kind, same labels.doc.* shape).
Rollup: one recovery-census row aggregating the 6 events (kind=recovery_census,
NEW - listed in notes/dir-triage-W3.md).

Fingerprint identity strings (documented in PROVENANCE.md):
  events: sha256("jsonhero-doc:<doc_id>")  -- same convention as the sibling
          dataset 2026-09-28-jsonhero-docs (verified: recomputing for
          doc 2EvFizxRzKLN reproduces its fingerprint exactly)
  rollup: sha256("jsonhero-archive-census")
"""
import json, sys, hashlib, os
from datetime import datetime, timezone

ROOT = sys.argv[1]
D = os.path.join(ROOT, "data", "2025-01-13-jsonhero-docs-archive")
RAW = os.path.join(D, "raw")
SLUG = "2025-01-13-jsonhero-docs-archive"
CREATED = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
LANE_TS = "2026-09-28T00:00:00Z"

def fp(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

manifest = json.load(open(os.path.join(RAW, "manifest.json")))
events = []
for m in manifest:
    doc = m["doc_id"]
    status = m["recovery_status"]
    labels = {
        "doc.id": doc,
        "doc.recovery_status": status,
        "doc.corpus_url_occurrences": m.get("corpus_url_occurrences"),
        "doc.note": m.get("note", ""),
    }
    kw = {
        "source_url": m.get("source_url"),
        "description": f"jsonhero.io shared doc {doc}: archive-recovery {status}",
    }
    if status == "recovered":
        # capture_timestamp like 20260912075005 -> ISO Z
        cts = m["capture_timestamp"]
        ts = f"{cts[0:4]}-{cts[4:6]}-{cts[6:8]}T{cts[8:10]}:{cts[10:12]}:{cts[12:14]}Z"
        labels.update({
            "doc.archive_source": m.get("archive_source"),
            "doc.capture.timestamp": ts,
            "doc.capture.url": m.get("capture_url"),
            "doc.capture.file": m.get("raw_capture_file", "").split("/")[-1],
            "doc.byte_size": m.get("byte_size"),
            "doc.sha256": m.get("sha256"),
            "timestamp_source": "labels:capture.datetime",
        })
        kw.update({
            "sha256": m["sha256"],
            "size_bytes": m["byte_size"],
            "retrieved_at": m["retrieved_at_utc"],
            "retrieved_via": "web.archive.org (id_ raw bytes, no Wayback rewriting)",
            "confidence": "confirmed",
            "description": (f"jsonhero.io shared doc {doc}: RECOVERED from Wayback capture "
                            f"{ts} ({m['byte_size']} B); payload extracted from window.__remixContext"),
        })
    else:
        ts = LANE_TS
        labels["timestamp_source"] = ("lane:2026-09-28 (Wayback CDX verdict; per-record verdict "
                                      "timestamps absent from raw)")
        kw.update({
            "confidence": "medium",  # Wayback-only; archive.today unreachable from this network
            "note": "Wayback-only verdict: archive.today could not be reached from this network",
            "description": f"jsonhero.io shared doc {doc}: NOT ARCHIVED (Wayback CDX zero captures)",
        })
    events.append({
        "@timestamp": ts,
        "event": {"dataset": SLUG, "created": CREATED},
        "record_kind": "artifact_observation",
        "fingerprint": fp(f"jsonhero-doc:{doc}"),
        "labels": labels,
        **kw,
    })

with open(os.path.join(D, "events.jsonl"), "w", encoding="utf-8") as fh:
    for r in events:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

# --- rollup: the bounded recovery census ---
rec_ids = [m["doc_id"] for m in manifest if m["recovery_status"] == "recovered"]
neg_ids = [m["doc_id"] for m in manifest if m["recovery_status"] != "recovered"]
rollup = [{
    "@timestamp": LANE_TS,
    "event": {"dataset": f"{SLUG}-rollup", "created": CREATED},
    "record_kind": "recovery_census",
    "fingerprint": fp("jsonhero-archive-census"),
    "labels": {
        "census.total": len(manifest),
        "census.recovered": len(rec_ids),
        "census.not_archived": len(neg_ids),
        "census.recovered_doc_ids": rec_ids,
        "census.not_archived_doc_ids": neg_ids,
        "census.capture.timestamp": "2026-09-12T07:50:05Z",
        "census.verdict_scope": "wayback-only (archive.today unreachable)",
        "timestamp_source": "lane:2026-09-28 (archive-recovery census)",
    },
    "description": (f"Archive-recovery census for 6 dead jsonhero.io docs: 1 recovered "
                    f"({', '.join(rec_ids)}), 5 not archived (Wayback-only verdicts)"),
    "confidence": "medium",
}]
with open(os.path.join(D, "rollup.jsonl"), "w", encoding="utf-8") as fh:
    for r in rollup:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"events: {len(events)}, rollup: {len(rollup)}")
