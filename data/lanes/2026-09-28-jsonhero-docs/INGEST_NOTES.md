# Ingest notes — 2026-09-28-jsonhero-docs

Batch 15f7e4f341514f81b3ac6750b1f198ac, 30 records. Lane tag `jsonhero-docs`
(date prefix stripped per lane convention). Zero retractions.

## Legacy row mapping

- 12 × artifact_observation (one per live doc body) -> web.capture observations.
  body.data: requested_url (verbatim `https://jsonhero.io/j/<docid>`, no .json suffix),
  capture_kind=http, http_status=200, tool=curl. Doc metadata (byte_size, body_sha256,
  top_level_keys, key_count, corpus_url_occurrences, legacy fingerprint, verbatim
  description) in tags. observed_at=2026-09-28T00:00:00Z, time_basis=source_metadata
  (dir-date fallback; manifest retrieved_at_utc partially redacted `02:5x:00Z`).
- 14 × artifact: 12 raw/<docid>.json bodies + events.jsonl + rollup.jsonl.
  Bytes seeded in data/blobs/sha256/; artifact_path tags point at the
  data/lanes/2026-09-28-jsonhero-docs/ copies. The 7 byte-identical regCF county
  re-posts (sha256 82786358…, 85,889 B) each keep their own artifact record
  (keep-all policy); CXGtP3kgj056 is a top-level JSON list (5 items) — labels
  correctly carry top_level_keys=[] / key_count=0.
- 1 × run (collection, 2026-09-28 workstream C): 17 doc IDs enumerated from
  usage_patterns.json; 11 live first pass + swJMw8b6VwDC recovered on bounded
  retry = 12 live fetches; 5 HTTP-500 docs dead, manifest-only (keep-all).
- 2 × dataset.snapshot: events.jsonl (12 rows) and rollup.jsonl (5
  doc_family_rollup rows; families regCF_county_2019:85889×7, regCF_county_2019:70089×1,
  copyright:10942×2, 2019_005_code:1472×1, unkeyed:634×1; totals recomputed).
  dataset_uri uses the post-ingest `evidence/remove-2026-09-28-jsonhero-docs/` path.
- 1 × source: jsonhero.io unauthenticated public document API.

## Pre-ingest dedup

match --text fuzzy for all 12 doc IDs: each hit exactly one existing record —
the infra.ioc corpus-hit markers from lane 2022-03-01-jsonhero (usage counts;
that lane deliberately never fetched bodies). Same identifier, different
evidence; not duplicates. Within-batch: 12/12 unique IDs. seen_before empty.

## Discrepancies found (data fixed, none retracted)

- PROVENANCE.md writes the fetch URL as `https://jsonhero.io/j/<docid>.json`,
  but manifest.json and events.jsonl both record `https://jsonhero.io/j/<docid>`
  (no suffix). Evidence form preserved verbatim; noted in source/run provenance tags.
- Sibling lane 2022-03-01-jsonhero's dataset.snapshot records
  dataset_uri `evidence/2022-03-01-jsonhero/events.jsonl`, but the lane was
  renamed to `evidence/remove-2022-03-01-jsonhero/` — stale provenance path.
  Left untouched (sibling lane's record); this lane records post-move paths.
  Fix via `factum update` belongs to that lane's owner.

## Time basis

observed_at 2026-09-28T00:00:00Z (time_basis=source_metadata) on observations —
the documented retrieval date. No per-doc event times invented.
