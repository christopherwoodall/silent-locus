# Elastic DB export — 2026-09-28

Full snapshot of the hunt's Elasticsearch indices, taken after the
`collusion-wiki` ingest stabilized (80,434 docs, stable across 5-min checks).

Cluster: agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud (Elastic Cloud, us-east-1)

| Index | Docs | File | Size | SHA-256 |
|---|---|---|---|---|
| rubygems-goimport-campaign | 6,619 | rubygems-goimport-campaign-20260928T022324Z.jsonl.gz | 284 KB | 439e7fcdcc7812203435ce794956f440cde12c0c84937adb80266829fd9125dc |
| urlquery-incidents | 51,643 | urlquery-incidents-20260928T022324Z.jsonl.gz | 8.5 MB | b46f0f3a7dc6f133618bcdf24bed3393f6985309598fa8764204bb5752d899dd |
| collusion-wiki | 80,434 | collusion-wiki-20260928T025051Z.jsonl.gz | 9.9 MB | 53f19bb1a7cd28ea4ea6d8460e46f150495b913211ef4b795baf00d569ade06a |

Export method: scroll API (`scripts/es_export.py`), read-only, `sort: ["_doc"]`.
Each line: `{"_id": ..., "_source": {...}}` (UTF-8 JSON, gzip).
Verification: `gunzip -t` clean on all files; 100 sampled lines per file parse
and carry `_id`/`_source`; exported doc count == live `_count` per index.

## Restore

1. Create the index with the canonical mapping from
   `../notes/gems-es-mapping.json` (shared schema, 56 properties).
2. Convert each line to `_bulk` action pairs:
   `{"index": {"_index": "<index>", "_id": "<_id>"}}` followed by the `_source` JSON.
3. `POST /_bulk` in batches (5–10 MB per request).

The `.meta.json` sidecar per file records expected vs exported counts and status.
