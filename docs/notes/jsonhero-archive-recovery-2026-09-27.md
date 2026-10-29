# Archive recovery — dead jsonhero docs (2026-09-28)

## Target

6 of the 17 corpus jsonhero doc IDs return HTTP 500 on the live site but were
referenced in June-2026 wiki revisions: S5R1RRn64PLh, aB94pTzmWvtl, swJMw8b6VwDC,
qDhAiEHyjXYi, wANOlosoW5YN, 1vaGknk7ajC4.

## Method (read-only)

- Wayback CDX API, per doc: `jsonhero.io/j/<id>*` wildcard (covers `/j/<id>`,
  `/j/<id>.json`, sub-paths), `collapse=digest`. Every negative re-queried with
  3 retries — Wayback was flaky from this network (intermittent 25s timeouts).
- archive.today attempted for all 6 — empty replies from this network;
  unavailable here, not absence. Worth a re-check from an unfiltered network.

## Results

| doc_id | captures | outcome |
|---|---|---|
| swJMw8b6VwDC | 2 (2026-09-12: HTTP 429, then 200) | **recovered** |
| S5R1RRn64PLh | 0 | not archived |
| aB94pTzmWvtl | 0 | not archived |
| qDhAiEHyjXYi | 0 | not archived |
| wANOlosoW5YN | 0 | not archived |
| 1vaGknk7ajC4 | 0 | not archived |

## The recovered doc

swJMw8b6VwDC (129 corpus URL occurrences) is the SEC Regulation Crowdfunding
county dataset — same family as the 7 byte-identical live docs, but an **older
vintage**. Its page `<title>` records that it was created from a Wayback capture
of `https://www.sec.gov/files/county.json` dated 2025-01-13, and it lacks the
`regCF_county_2024` array the live docs carry. The 2021 county records are
content-identical to the live family (e.g. `us-md-005` → offerings 10,
usd 3067574.523389335).

Read: agents re-minted the dataset from an archived upstream — consistent with
the live SEC file being bot-blocked (HTTP 403, confirmed in the docs lane).
The proxy layer exists precisely because the upstream fights back.

## Files

- `data/jsonhero-docs-archive/swJMw8b6VwDC.json` — recovered payload
  (sha256 `c7650713c89a6f5ebca4163199d4ed7f451a900aa5bf12c6033c1730538ca290`)
- `data/jsonhero-docs-archive/swJMw8b6VwDC_20260912075005.html` — raw capture
- `data/jsonhero-docs-archive/manifest.json` — all 6 IDs with recovery status
- `data/jsonhero-docs-archive/PROVENANCE.md` — method, results, caveats
- `scripts/es_ingest_jsonhero_archive.py` — index create/load/verify

## Elastic

Own index `jsonhero-docs-archive` (shared schema, canonical mapping),
`event.dataset` = `jsonhero-docs-archive`, zero new top-level fields.
6 docs verified: `recovery:recovered` 1, `recovery:not_archived` 5.

## Follow-ups

1. Re-check archive.today + the 5 unrecovered docs from an unfiltered network.
2. The recovered doc's 2025-01-13 upstream vintage suggests grepping the other
   corpora for that specific vintage (missing 2024 array) as a fingerprint.
