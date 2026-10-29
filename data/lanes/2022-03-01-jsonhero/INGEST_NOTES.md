# Ingest notes — 2022-03-01-jsonhero

Batch 220b933fe353409090c9080769ff68d8, 24 records.

## Legacy row mapping

- 1 × venue_probe -> infra.ioc term=jsonhero.io, category=domain, status=active.
  Repo metadata (triggerdotdev/jsonhero-web, created 2022-03-01T09:33:29Z,
  10879 stargazers, Apache-2.0) preserved verbatim in tags.
- 17 × corpus_hit -> infra.ioc term=<doc_id>, category=marker, status=active.
  Term is the actual IOC value (the shared doc ID), never an internal ID.
  url_occurrences preserved in tags. Dedup: 17/17 doc IDs + jsonhero.io +
  triggerdotdev/jsonhero-web returned zero pre-existing Factum matches.
- 1 × artifact_observation (usage rollup) -> dataset.snapshot covering the
  legacy events.jsonl (row_count 19, revision=sha256 of file). Rollup detail
  (2398 URL occurrences, 17 doc IDs, top ?path= params, view suffixes) in tags.
- 3 × artifact: raw/repo_metadata.json, raw/usage_patterns.json, events.jsonl.
  Bytes also seeded in data/blobs/sha256/; verify --blobs green for this lane.
- 1 × source, 1 × run (collection, 2026-09-28 Lane F recon).

## Time basis

observed_at uses retrieved_at 2026-09-28T00:00:00Z (time_basis=source_metadata).
The 2022-03-01 date is a dir-date fallback, noted in tags, never promoted to
an event time. The 17 shared doc IDs were never fetched live (deliberate).
