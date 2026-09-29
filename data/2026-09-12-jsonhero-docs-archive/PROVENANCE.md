# PROVENANCE — jsonhero-docs-archive

Archive-recovery dataset for the 6 jsonhero.io shared docs that returned HTTP 500
on the live site (2026-09-28) but were referenced in June-2026 wiki revisions.

## Method (2026-09-28, read-only)

1. Wayback CDX API (`web.archive.org/cdx/search/cdx`) queried for each dead doc ID
   under `jsonhero.io/j/<id>*` (wildcard covers `/j/<id>`, `/j/<id>.json`, sub-paths),
   with `collapse=digest`. Exact-pattern queries run first, wildcard on retry.
2. archive.today (`archive.ph/newest/...`) attempted for all 6 — the host returned
   empty replies from this network; treated as unavailable, not as absence.
3. The one capture found (swJMw8b6VwDC, 2026-09-12, HTTP 200) was pulled with the
   `id_` suffix (raw bytes, no Wayback rewriting). The payload was embedded in the
   captured page's `window.__remixContext` as a JS object literal; extracted with a
   single-quote-aware brace matcher and converted to strict JSON
   (`swJMw8b6VwDC.json`). Raw capture kept as `swJMw8b6VwDC_20260912075005.html`.

## Results

| doc_id | CDX captures | outcome |
|---|---|---|
| swJMw8b6VwDC | 2 (2026-09-12: 429, then 200) | **recovered** |
| S5R1RRn64PLh | 0 | not archived |
| aB94pTzmWvtl | 0 | not archived |
| qDhAiEHyjXYi | 0 | not archived |
| wANOlosoW5YN | 0 | not archived |
| 1vaGknk7ajC4 | 0 | not archived |

## The recovered doc

swJMw8b6VwDC is the SEC Regulation Crowdfunding county dataset — same family as
the 7 byte-identical live docs (2021 county records match exactly, e.g.
`us-md-005` → offerings 10, usd 3067574.523389335), but an **older vintage**:
its `<title>` shows it was created from a Wayback capture of
`https://www.sec.gov/files/county.json` dated 2025-01-13, and it lacks the
`regCF_county_2024` array the live docs carry. The agents re-minted the dataset
from an archived upstream when the live SEC file changed or bot-blocked them.

## Caveats

- Wayback CDX was flaky from this network (intermittent 25s timeouts); every
  negative was re-queried with 3 retries before being recorded as zero-capture.
- archive.today could not be reached from here at all — the 5 "not archived"
  verdicts are Wayback-only. A re-check from an unfiltered network is worthwhile.
- The 2026-09-12 capture predates the doc's death but postdates the campaign;
  the payload content matches the June-2026 family, so it is representative.

## Closure 2026-09-28 (workstream D)

Naturally small: archive-recovery census for exactly the 6 dead jsonhero.io
docs referenced in June-2026 wiki revisions (1 recovered from Wayback + 5
Wayback-not-archived negatives). N=6 docs is the bounded census — no other
dead docs exist in the jsonhero-docs lane. ES `jsonhero-docs-archive`
_count=6 verified. The 5 "not archived" verdicts are Wayback-only
(archive.today unreachable from this network); a re-check from an unfiltered
network is the recorded next step, not a blocker.

## Schema normalization 2026-09-29 (worker W3)

- Transform: `temp/build_events_w3_jsonhero_archive.py` (repo root passed as argv[1]).
- Grain: one record per doc (6, `record_kind: artifact_observation`), mirroring the
  sibling dataset `2026-09-28-jsonhero-docs` (same kind, same `labels.doc.*` shape).
- `@timestamp`: the Wayback capture time for the recovered doc
  (`2026-09-12T07:50:05Z`, `labels.timestamp_source = "labels:capture.datetime"`);
  the documented lane date 2026-09-28 for the 5 CDX-negative verdicts
  (`labels.timestamp_source = "lane:2026-09-28 …"`, per-record verdict timestamps
  absent from raw; negatives carry `confidence: medium` — Wayback-only verdicts).
- Fingerprint identity string: `sha256("jsonhero-doc:<doc_id>")` — the same
  convention as the sibling dataset (verified: recomputing for doc `2EvFizxRzKLN`
  reproduces its fingerprint `57ce19c5…340bb95` exactly). Reference method
  verified against data/2023-11-14-hfspace-proxies
  (sha256("TheNacken/python-cors-proxy") -> `14c645d9…efbe94`).
- Rollup: `rollup.jsonl` with one `recovery_census` row (NEW kind, listed in
  notes/dir-triage-W3.md) aggregating the 6 events — 1 recovered, 5 not archived,
  Wayback-only scope. `event.dataset` suffixed `-rollup`.
- `event.dataset = "2026-09-12-jsonhero-docs-archive"`; `event.created` = build time.
