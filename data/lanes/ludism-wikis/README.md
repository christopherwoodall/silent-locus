# ludism-wikis

Factum lane for the ludism.org + ApchemWiki public-reader-proxy reachability
sweep (Lane A, 2026-09-28).

## What this is

On 2026-09-28, a read-only sweep probed 9 wiki targets through 3 public
reader proxies (r.jina.ai, api.allorigins.win/raw, api.allorigins.win/get).
Result: 2/9 targets reachable (both ApchemWiki paths, via jina only);
ludism.org unfetchable from two vantage points. Full story in PROVENANCE.md.

## Contents

- `events.jsonl` — 29 legacy probe records (`venue_probe`), one per
  (target, proxy) pair plus 2 proxy controls. Kept as historical material.
- `rollup.jsonl` — 9 per-target verdict rows derived from the probe matrix.
- `raw/` — verbatim proxy fetch outcomes: response bodies where captured
  (4 files), per-fetch sidecar metadata (`.meta.json`), sweep summary,
  pattern sweep, and the two thecolony.ai claim excerpts quoted verbatim.
- `SHA256SUMS` — checksums for all lane files (run `sha256sum -c` here).
- `build_events_w7.py`, `build_rollup_w8.py` — the normalization-wave
  build scripts (historical).
- `lane.json` — the Factum lane record.
- `INGEST_NOTES.md` — how the 29 events entered Factum, mapping table,
  batch id, and discrepancies found.
- `FINDINGS.md` — short evidence summary.

## Factum records

58 records carry tag `{"lane":"ludism-wikis"}`: 29 `reachability.check`
observations (one per probe) + 29 `source` records (one per fetched URL).
Lane record id: `lane_5476928cefd54ef09e4714539a88822b`.

Legacy evidence lives on, renamed, at
`evidence/remove-2026-09-28-ludism-wikis/`.
