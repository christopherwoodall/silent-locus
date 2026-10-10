# 2026-09-05-termina-digital

Factum lane for the termina.digital incident-DB recovery (Lane L, 2026-09-28).

## What this is

- On 2026-09-05, thecolony.ai investigators cited termina.digital /db/ as a
  downloadable incident JSONL database.
- On 2026-09-28, the live /db/ was dark (404). The full DB was recovered from
  the Wayback Machine under the subdomain **swarm.termina.digital**.
- Recovery set: 99 wayback files (incidents, campaigns, clusters, venues,
  actors, trackers, API/claims/evidence/tips/scan/summary pages, llms.txt,
  search-config, graph.json, search index) + live RSS snapshot + WASM bundle
  with blog strings + 2 CDX dumps + 2 live-probe negatives.
- A 21-pattern corpus sweep battery ran over the 97 recovered files
  (sweep.json). 16 patterns hit; 5 had zero hits (recorded as negatives).

## Factum records

- Lane ID: `lane_ed32f5b7b9b642ba9d95fb4bd77095fc`
- Batch 1: `7a482cebea3a4ff19d9a725eea9877a5` (352 records)
- Batch 2: `66ec5afa968147b49573d1760a4a89de` (14 records: 7 retractions +
  7 corrected artifacts)
- Active records: 359. Retracted: 7 (sha256 recorded from CRLF working-tree
  bytes; superseded by corrected artifact records).

Record types:

- 104 `web.capture` (100 OK incl. the 43-byte 503 tarball placeholder,
  4 failed captures kept per keep-all policy)
- 99 artifact records for recovered wayback bytes
- 105 `infra.ioc` (pattern markers, category=marker, one per (pattern,file) pair)
- 21 claims (pattern rollups, verbatim, subject=@run)
- 5 claims (zero-hit patterns, subject=@run)
- 2 `reachability.check` (live 404 / 503 probes)
- 12 lane-document artifacts (7 lane artifacts + events.jsonl + rollup.jsonl
  + PROVENANCE.md + SHA256SUMS + sweep.json)
- 2 sources, 1 run

## Files

- `PROVENANCE.md` — full recovery provenance (copied from the legacy lane).
- `SHA256SUMS` — checksums for the lane files.
- `events.jsonl` — 223 legacy rows (source material, unchanged).
- `rollup.jsonl` — 21 pattern rollup rows (source material, unchanged).
- `raw/` — recovered captures and sweep battery output.
- `INGEST_NOTES.md` — mapping, dedup, validator, root-cause fixes.
- `FINDINGS.md` — evidence summary.
