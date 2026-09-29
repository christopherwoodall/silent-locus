#!/usr/bin/env python3
"""Build events.jsonl for data/2026-09-28-jsonhero-docs (normalization sweep, worker W7).

Usage: build_events_w7.py <repo-root>
One record per live doc JSON in raw/ (12 docs). The 5 dead docs (HTTP 500) have
no body file and stay manifest-only per the keep-all policy.
Fingerprint identity string: "jsonhero-doc:<doc_id>".
@timestamp: dir date prefix 2026-09-28 (manifest retrieved_at_utc is partially
redacted, e.g. "2026-09-28T02:5x:00Z", so no parseable per-doc retrieval time).
"""
import json
import hashlib
import os
import sys
import datetime

ROOT = sys.argv[1]
D = os.path.join(ROOT, "data", "2026-09-28-jsonhero-docs")
RAW = os.path.join(D, "raw")
DATASET = "2026-09-28-jsonhero-docs"
CREATED = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

manifest = json.load(open(os.path.join(RAW, "manifest.json"), encoding="utf-8"))
man = {e["doc_id"]: e for e in manifest}
live_ids = sorted(e["doc_id"] for e in manifest if e["status"] == "live")

doc_files = sorted(
    f for f in os.listdir(RAW) if f.endswith(".json") and f != "manifest.json"
)
assert [f[:-5] for f in doc_files] == live_ids, "doc files != live manifest entries"

out = []
for fname in doc_files:
    doc_id = fname[:-5]
    e = man[doc_id]
    body = open(os.path.join(RAW, fname), "rb").read()
    assert hashlib.sha256(body).hexdigest() == e["sha256"], f"sha256 mismatch {doc_id}"
    assert len(body) == e["byte_size"], f"size mismatch {doc_id}"
    doc = json.loads(body.decode("utf-8"))
    top_keys = sorted(doc.keys()) if isinstance(doc, dict) else []
    labels = {
        "doc.id": doc_id,
        "doc.status": e["status"],
        "doc.http_status": e["http_status"],
        "doc.byte_size": e["byte_size"],
        "doc.sha256": e["sha256"],
        "doc.corpus_url_occurrences": e["corpus_url_occurrences"],
        "doc.top_level_keys": top_keys,
        "doc.key_count": len(top_keys),
        "timestamp_source": "fallback:dir_date_prefix;manifest retrieved_at_utc partially redacted (02:5x:00Z)",
    }
    if e.get("note"):
        labels["doc.note"] = e["note"]
    shown = ", ".join(top_keys[:6]) + ("..." if len(top_keys) > 6 else "")
    rec = {
        "@timestamp": "2026-09-28T00:00:00Z",
        "event": {"dataset": DATASET, "created": CREATED},
        "record_kind": "artifact_observation",
        "fingerprint": hashlib.sha256(f"jsonhero-doc:{doc_id}".encode()).hexdigest(),
        "labels": labels,
        "source_url": e["source_url"],
        "sha256": e["sha256"],
        "size_bytes": e["byte_size"],
        "confidence": "confirmed",
        "description": (
            f"jsonhero.io shared doc {doc_id}: {len(top_keys)} top-level keys "
            f"({shown}), {e['byte_size']} B, {e['corpus_url_occurrences']} corpus "
            "URL occurrences; body sha256 verified against manifest"
        ),
    }
    out.append(rec)

with open(os.path.join(D, "events.jsonl"), "w", encoding="utf-8") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"{DATASET}: in={len(doc_files)} doc files, out={len(out)} records")
