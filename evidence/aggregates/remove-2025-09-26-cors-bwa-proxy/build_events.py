#!/usr/bin/env python3
"""Materialize events.jsonl for the cors-bwa-proxy aggregate collection.

Reuses the ES ingest transform (`es_ingest_cors_bwa.build_docs()`, verified
offline 2026-09-29 to assemble 154 docs: 113 proxied_target, 29 proxy_ladder,
6 proxy_family, 6 venue_summary) and adds the schema-required `fingerprint`
(ES ingest docs predate the fingerprint requirement) plus a `file` pointer at
the raw transform input each doc was built from.

Fingerprint identity strings (documented in PROVENANCE.md):
  proxied_target: source_index + "|" + doc_id
  proxy_ladder:   edge
  proxy_family:   proxy_host
  venue_summary:  venue
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from es_ingest_cors_bwa import build_docs  # noqa: E402

OUT = os.path.join(HERE, "events.jsonl")

SOURCE_FILE = {
    "proxied_target": "data/aggregates/2025-09-26-cors-bwa-proxy/raw/bwa_targets.jsonl",
    "proxy_ladder": "data/aggregates/2025-09-26-cors-bwa-proxy/raw/ladder_edges.jsonl",
    "proxy_family": "data/aggregates/2025-09-26-cors-bwa-proxy/raw/other_workers_dev_hostnames.json",
    "venue_summary": "data/aggregates/2025-09-26-cors-bwa-proxy/raw/pull_totals.json",
}


def identity(doc):
    kind = doc["record_kind"]
    lab = doc["labels"]
    if kind == "proxied_target":
        return lab["source_index"] + "|" + lab["doc_id"]
    if kind == "proxy_ladder":
        return lab["edge"]
    if kind == "proxy_family":
        return lab["proxy_host"]
    if kind == "venue_summary":
        return lab["venue"]
    raise ValueError(f"unknown kind {kind}")


def main():
    docs = build_docs()
    records = []
    for _id, doc in docs.items():
        doc["fingerprint"] = hashlib.sha256(
            identity(doc).encode("utf-8")).hexdigest()
        doc["file"] = SOURCE_FILE[doc["record_kind"]]
        records.append(doc)
    with open(OUT, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    kinds = {}
    for r in records:
        kinds[r["record_kind"]] = kinds.get(r["record_kind"], 0) + 1
    print(f"wrote {len(records)} records to events.jsonl: {kinds}")


if __name__ == "__main__":
    main()
