# Provenance — 2026-09-03-collusion-manifest

## The investigation

Coverage census ("collusion manifest") of the wiki-revision review database
used in the collusion-wiki investigation: 14,591 held revisions (write cut
>= 2026-05-01), 4,579 pages, 3,103 published labels, graded by save / delete
/ revert / probe populations, plus a per-site coverage-gap assessment of
110 surfaces (wikis, shorteners, pastebins, relays, documents, hosting,
new_discord_posting_surface) with prior-status, compilation-status, and
limitation notes. Generated 2026-09-03T03:42:36Z; db sha256
`199241bf9e0b38b58764cf1545680de8fec8896db034050bde145e3b6f6ce0bb`.

## Files ingested

- `raw/manifest.json` — census manifest (counts, per_wiki breakdown,
  population_counts, grade_histograms, body_bytes, body_encoding,
  page_family_coverage, facts, recreation_source, resources,
  tool_versions, source_scan, request_source_note, checks).
- `raw/coverage-gaps.csv` — 110 site rows (site, host, canonical_url,
  category, prior_status, compilation_status, selected_distinct_texts,
  discord_urls, fresh_responses_saved, fresh_read_failures_or_redirects,
  specific_prior_gap_remains, limitations, prior_evidence, scope).

## Ingest into Factum

- Date: 2026-10-11 (actor `agent:lane-ingest-lanes-b`).
- Records: 1 `dataset.snapshot` (the census; dataset_uri
  `sha256:199241bf...`, coverage `partial`, row_count 110, census counts
  in tags) + 110 `dataset.record` (one per CSV site row; locator =
  canonical_url, external_record_id = site, gap assessment in tags)
  + 1 bundle-local source (1 bundle, idempotency key
  `ingest-lanes-b:2026-09-03-collusion-manifest:chunk0`).
- Dedup: CSV rows unique by (site, host); no db-sha256 or
  `collusion-manifest` mentions anywhere in the exported corpus —
  no overlap.
- All records carry `tags.lane = "2026-09-03-collusion-manifest"` and
  `grade = "OBSERVED"`. No edges (ingest pass).

## Schema

No new schema packs. Used installed `factum-datasets` 1.0.0
(`dataset.snapshot` schema `urn:factum:datasets:snapshot:1`,
`dataset.record` schema `urn:factum:datasets:record:1`).
