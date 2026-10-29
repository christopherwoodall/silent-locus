# 2026-05-11 OSV sweep lane

Factum lane ID: `2026-05-11-osv`.

This lane holds the 2026-09-27/28 sweep of RubyGems campaign package names
(the GemStuffer / go-import campaign). Two collection lanes produced the
data:

- **Lane 19 (OSV.dev / GitHub advisories):** OSV API `/v1/query` for 42
  campaign package names (7 GemStuffer `MAL-*` hits, all published
  2026-07-07); GitHub Advisory API pull of 3,000 rubygems malware
  advisories, classified into 1,687 GemStuffer-shaped vs 1,310
  other-campaign names.
- **Lane 20 (Diffend sweep):** `scripts/diffend_sweep.py` over the 1,284
  advisory-named campaign gems absent from the local corpus, plus a retry
  pass. 394 found in Diffend (first-publish 2026-05-11 19:40 →
  2026-05-12 07:47 UTC), 218 confirmed absent, 672 unconfirmed in the
  first pass; the retry pass resolved many of the unconfirmed names.

## Factum ingest (2026-10-10)

1,965 legacy events (`events.jsonl`) ingested as 1,303 Factum records:

- 1,290 `infra.package` observations — one per distinct gem name
  (393 Diffend-present only, 324 present in one pass / absent in the
  other, 566 absent on all passes, 7 advisory-only).
- 7 `core.claim` records (basis UPSTREAM) mapping the 7 OSV `MAL-*`
  advisories to their gem observations.
- 1 `core.claim` + 1 `core.run` (basis OBSERVED): the July-7 XSS/SSTI
  wave has zero advisories anywhere (negative sweep verdict).
- 1 `intel.report` observation: GHSA-9j48-x3c3-mrp2 (RubyGems CDN cache
  API-key leak; OSV lookup 404'd, details from GitHub).
- 2 `core.source` records (Diffend sweep venue, OSV.dev venue) and 1
  `core.run` record for the Diffend sweep.

Dedup: exact-name lookup plus full-corpus substring sweep before submit.
One gem (`slvhg151`) already existed as `infra.package` from the
webhook-deaddrops lane with richer provenance; its legacy rows were
skipped, not duplicated. No `in_lane` edges were submitted during ingest.

## Artifact layout

- `raw/` — Lane 19 products (GitHub advisory pull, GemStuffer
  classification, OSV query results).
- `events.jsonl` — legacy source rows (kept for audit; Factum is the
  system of record).
- `SHA256SUMS` — legacy file hashes.
- `PROVENANCE.md` — collection and transform history.

Legacy directory renamed to `evidence/remove-2026-05-11-osv/` after
ingest.
