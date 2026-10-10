# PROVENANCE — 2026-09-12-jsonhero-docs-archive lane ingest

**Ingest date:** 2026-10-09 (Phase 3 Batch 5).
**Source:** legacy directory `evidence/2026-09-12-jsonhero-docs-archive/`,
renamed to `evidence/remove-2026-09-12-jsonhero-docs-archive/` after ingest.
The legacy provenance file is preserved verbatim as
`legacy-PROVENANCE.md` in this lane.

## Original collection (2026-09-28, read-only)

1. Wayback CDX API queried for each dead doc ID under
   `jsonhero.io/j/<id>*` (exact pattern first, wildcard on retry), with
   `collapse=digest`.
2. archive.today attempted for all 6 — unreachable from the network.
   Treated as unavailable, not as absence.
3. The one capture found (`swJMw8b6VwDC`, 2026-09-12, HTTP 200) was pulled
   with the `id_` suffix (raw bytes, no Wayback rewriting). The payload
   was embedded in the page's `window.__remixContext` as a JS object
   literal; extracted with a single-quote-aware brace matcher and converted
   to strict JSON (`swJMw8b6VwDC.json`). Raw capture kept as
   `swJMw8b6VwDC_20260912075005.html` (95,501 B, sha256
   `c7650713c89a6f5ebca4163199d4ed7f451a900aa5bf12c6033c1730538ca290`).

## Lane schema mapping

- Legacy `events.jsonl` (6 rows, grain one record per doc) became one
  `source` + one observation per doc.
- Recovered doc: `web.capture`. `observed_at` is the Wayback capture time
  2026-09-12T07:50:05Z (`time_basis: source_metadata`). Notes are copied
  verbatim from the legacy record.
- Not-archived docs: `reachability.check` against the Wayback CDX API,
  `outcome: response`, `error` carries the zero-capture verdict verbatim.
  `observed_at` is the lane date 2026-09-28 (`time_basis:
  legacy_documented`), per the lane's documented timestamp convention.
- `rollup.jsonl` (one `recovery_census` row) became a `dataset.snapshot`
  observation (row_count 6, coverage complete).
- `corpus_url_occurrences` values are UPSTREAM counts from the corpus
  scan, recorded verbatim in tags, not claimed as observed.

## Dedup

Pre-ingest `match --text "<doc-id>" --mode fuzzy` for all 6 doc IDs plus a
fuzzy `jsonhero` search returned `not_found`. No overlap with the existing
corpus (802 records). No intra-batch dupes (6 unique doc IDs asserted).

## Limits

- The 5 "not archived" verdicts are Wayback-only. archive.today could not
  be reached from the collection network. A re-check from an unfiltered
  network is the recorded next step.
- The exact CDX query strings were not preserved in the legacy lane; the
  `reachability.check` target is the CDX API base and the verdict text
  carries the documented query pattern (`jsonhero.io/j/<id>*`).
