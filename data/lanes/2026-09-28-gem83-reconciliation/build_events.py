#!/usr/bin/env python3
"""Materialize events.jsonl for the gem83-reconciliation aggregate collection.

Reuses the ES ingest transform (`es_ingest_gem83.build_docs()`) for the
83-row mapping, then adapts it to schema/record.schema.json, which the ES
ingest docs do NOT satisfy (they carry non-schema top-level keys like `gem`,
`package`, `versions`, and no `fingerprint`):

  - fingerprint: sha256(gem name) — identity string documented in PROVENANCE.md
  - non-schema top-level keys -> namespaced labels (gem.name, gem.package,
    gem.versions, gem.xray_id, gem.in_diffend_corpus, gem.wave)
  - description derived from the record's note
  - labels.timestamp_source documents the inferred June-18 wave date
  - file pointer at raw/gem83-reconciliation.jsonl

record_kind stays gem_reconciliation; event.dataset stays
2026-09-28-gem83-reconciliation.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from es_ingest_gem83 import build_docs  # noqa: E402

OUT = os.path.join(HERE, "events.jsonl")
FILE_PTR = "data/aggregates/2026-09-28-gem83-reconciliation/raw/gem83-reconciliation.jsonl"

DROP_TO_LABELS = {
    "gem": "gem.name",
    "package": "gem.package",
    "versions": "gem.versions",
    "xray_id": "gem.xray_id",
    "in_diffend_corpus": "gem.in_diffend_corpus",
    "wave": "gem.wave",
}


def main():
    docs = build_docs()
    records = []
    for doc in docs:
        labels = doc.get("labels", {})
        for old, new in DROP_TO_LABELS.items():
            if old in doc:
                labels[new] = doc.pop(old)
        labels["timestamp_source"] = (
            "inferred:june-18 wave date (name grammar + JFrog/thecolony.ai reports; "
            "JFrog CSV carries no per-row dates)"
        )
        doc["fingerprint"] = hashlib.sha256(
            labels["gem.name"].encode("utf-8")).hexdigest()
        doc["file"] = FILE_PTR
        doc["description"] = (
            "gem83 reconciliation: %s (%s) — wave june-18" % (
                labels["gem.name"], labels.get("name_family", ""))
        )
        records.append(doc)
    with open(OUT, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(records)} records to events.jsonl")


if __name__ == "__main__":
    main()
