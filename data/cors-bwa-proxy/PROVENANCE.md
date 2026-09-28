# PROVENANCE — cors-bwa-proxy lane

**Dataset:** `data/cors-bwa-proxy/`
**Lane:** cors-bwa cross-corpus proxy primitive (night watch, 2026-09-28)
**ES index:** `cors-bwa-proxy` (154 docs; canonical shared schema
`notes/gems-es-mapping.json`, `event.dataset.keyword` multi-field at creation,
zero extra top-level fields)

## Source data
All source records were pulled read-only from the project's Elastic Cloud
deployment via `scripts/cors_bwa_collect.py` (query_string
`*cors.bwa.workers.dev*`, plus `*.workers.dev*` family sweep). Raw pulls are
kept in `data/cors-bwa-proxy/raw/` (8 files, see `raw/pull_totals.json`):

| source index | query | docs |
|---|---|---|
| collusion-wiki | `*cors.bwa.workers.dev*` | 578 |
| urlquery-incidents | `*cors.bwa.workers.dev*` | 113 |
| urlquery-hunt | `*cors.bwa.workers.dev*` | 36 |
| proxy-primitives | `*cors.bwa.workers.dev*` | 17 |
| paste-archive-gap | `*cors.bwa.workers.dev*` | 1 |
| rmn-re-linktable | `*cors.bwa.workers.dev*` | 1 |
| urlquery-incidents | `*.workers.dev*` (family sweep) | 174 |
| collusion-wiki | `*.workers.dev*` (family sweep) | 861 |

No live fetching of proxied targets was performed — all extraction is from
already-ingested ES records and on-disk files (passive dataset work only).

Negative checks (same read path, 2026-09-28):
- `rubygems-goimport-campaign`: 0 hits for `*cors.bwa.workers.dev*`,
  0 for `*workers.dev*` — the gem campaign did not use this primitive.
- HF redacted corpus (`data/raw/redacted.jsonl.gz`, 189,579 records): 0
  occurrences of `cors.bwa.workers.dev`, 0 of any `*.workers.dev` URL —
  the HF eval runs did not use it (or it is redacted out).

## Build
1. `scripts/cors_bwa_collect.py` — ES pulls (dynamic_credentials via
   `/opt/hatch/skills/skill-creator/bin`, pattern from
   `scripts/es_ingest_paste_archive_gap.py`).
2. `scripts/cors_bwa_analyze.py` — target extraction (strip
   `cors.bwa.workers.dev/` prefix, URL-decode up to 3 rounds), host/task-family
   classification, monthly timing, shortener-in-proxy detection.
   -> `bwa_targets.jsonl` (113), `summary_stats.json`.
3. `scripts/cors_bwa_other_hosts.py` — decodes targets behind the six other
   `*.workers.dev` CORS-proxy hostnames found in the family sweep.
   -> `other_workers_dev_hostnames.json`.
4. `scripts/cors_bwa_ladders.py` — reconstructs (outer_wrapper ->
   cors.bwa.workers.dev -> target) chains from incident stacks, wiki
   `external_links`, and proxy-primitives `matched_string`.
   -> `ladder_edges.jsonl` (29 edges).
5. `scripts/es_ingest_cors_bwa.py` — `--create` (canonical mapping),
   `--load` (154 docs: 113 `proxied_target`, 29 `proxy_ladder`, 6
   `proxy_family`, 6 `venue_summary`), `--verify` (count matches, zero schema
   drift, `event.dataset.keyword` multi-field present).

## Files
- `bwa_targets.jsonl` — per incident: source_index, doc_id, full_proxied_url,
  decoded_target, target_host, task_family, chain_layers, chain, incident_ts.
- `ladder_edges.jsonl` — edge, layers [outer, via, target], occurrences,
  venues. Outer == via means direct proxy use (no outer wrapper).
- `other_workers_dev_hostnames.json` — per hostname: docs_per_index, n_docs,
  n_occurrences, top targets, raw samples.
- `summary_stats.json` — aggregate counts, monthly timing, family top-list.
- `raw/` — raw ES pulls + `pull_totals.json` (resumable-source evidence).
- `manifest.sha256` — SHA-256 of every file in this dataset (excludes `raw/`,
  whose pulls are reproducible via `scripts/cors_bwa_collect.py`).

## Scope guards honored
Read-only research only; agents/infrastructure traces only (no operator
identity, registrant details, or person-focused attribution); no credentials
reproduced; no absolute `/home/*` paths in any file in this lane (verified by
grep before commit).

## Re-ingest
`python3 scripts/es_ingest_cors_bwa.py --create --load --verify` from the
repo root rebuilds the `cors-bwa-proxy` index from these files.
