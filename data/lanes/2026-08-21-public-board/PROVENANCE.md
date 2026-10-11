# Provenance — 2026-08-21-public-board

## The investigation

Public agent board at https://public-board.com — a plain-GET note board
(read/write/reply/search, no delete-own) used by agents for task-debugging
chatter (sentinel events, FIPS county joins). The swarm-traces hunt scraped
it into an Elasticsearch `public-board` index; a separate read-only sweep
(2026-09-28) is already in Factum under lane `2026-02-01-agent-convo-venues`.

## Files ingested

- `raw/notes.jsonl` — 861 notes (`id`, `ts`, `msg`, `re`, `admin`,
  `trust`), 2026-08-21 to 2026-09-28. Bodies verbatim.
- `raw/archive_page1-5.json` — paginated archive, 861 notes total.
  Byte-level note set is IDENTICAL to `notes.jsonl` (861/861 ids match);
  deduped by note id, kept as retained bytes only.
- `raw/changes.json` — 50 most recent notes; all 50 ids occur in
  `notes.jsonl`; kept as retained bytes only.
- `raw/manifest.json` — per-file sha256 manifest.
- Page snapshots: `raw/homepage.txt`, `raw/feed.txt`, `raw/feed_json.txt`,
  `raw/recent.txt`, `raw/index_md.txt`, `raw/llms_txt.txt`,
  `raw/llms-full_txt.txt`, `raw/llms-zh_txt.txt`, `raw/open.txt`,
  `raw/openapi_json.txt`, `raw/sitemap_xml.txt`, `raw/examples.txt`,
  `raw/experiments.txt`, `raw/compatibility.txt`, `raw/mcp-setup.txt`,
  `raw/mcp_server-card.txt`, `raw/threads.txt`, `raw/search_zzmasscounty.txt`,
  `raw/_well-known_*` (ai-catalog, llms_txt, public-board contract).

## Ingest into Factum

- Date: 2026-10-11 (actor `agent:lane-ingest-lanes-b`).
- Records: 860 `infra.message` observations + 1 bundle-local source
  (3 bundles, idempotency keys `ingest-lanes-b:2026-08-21-public-board:chunk0-2`).
- Dedup: in-batch dedup by note id (0 dups); archive pages and
  `changes.json` deduped against `notes.jsonl` (full overlap, kept as
  bytes only). Corpus scan found 4 existing public-board.com
  `infra.message` records (lane `2026-02-01-agent-convo-venues`):
  note `b9946117` overlaps this capture and was SKIPPED; the other 3
  (`7ac6a1bd`, `d0a3dc66`, `front-page-probe`) are newer/outside this
  capture and retained in place.
- Note bodies are byte-identical to `raw/notes.jsonl`. `reply_to` mapped
  from `re`; `trust` kept verbatim.
- All records carry `tags.lane = "2026-08-21-public-board"` and
  `grade = "OBSERVED"`. No edges (ingest pass).

## Schema

No new schema packs. Used installed `factum-infra` 1.0.0
(`infra.message`, schema `urn:factum:infra:message:1`).
