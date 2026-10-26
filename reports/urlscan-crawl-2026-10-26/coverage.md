# urlscan.io crawl — coverage, 2026-10-26

Crawl executor output only. No Factum ingest. No final report.
All fetches: anonymous urlscan.io search API, one request per ~2 s,
User-Agent `silent-locus-lane-scanner/1.0`. Retrieval times are UTC.
Crawl run: 2026-10-26T17:02:32Z–17:02:49Z.

## Result in one line

6 queries run, all HTTP 200, 74 results fetched in total.
Triage-passing hits: 0. `hits-draft.json` is an empty list.
No screenshots were fetched (screenshots are fetched only for
triage-passing hits, and there were none).

## Coverage table

| Label | Query string | HTTP | Total | Fetched | Triage-passing |
|---|---|---|---|---|---|
| getpoiinfo | getPoiInfo | 200 | 0 | 0 | 0 |
| uqscan-tag | uqscan= | 200 | 0 | 0 | 0 |
| uqframe-tag | uqframe= | 200 | 0 | 0 | 0 |
| proxy-marker | hysandbox | 200 | 0 | 0 | 0 |
| relay-jina-reader | domain:r.jina.ai | 200 | 57 | 57 | 0 |
| title-amap | page.title:"amap" | 200 | 17 | 17 | 0 |

Dedupe note: the task's extra-grammar list overlapped the enabled
config queries in four places (domain:r.jina.ai, uqscan=, uqframe=,
getPoiInfo). Each was fetched exactly once; no duplicate fetches.

## Why the 74 fetched results are not hits

Triage rule (scripts/scanners/FALSE-POSITIVES-urlscan.md): keep a hit
only if it carries at least one fleet marker (getPoiInfo in URL,
uqscan=/uqframe= tags, hysandbox marker, fleet POI page shapes) or a
HIGH-confidence scanner grade. A full-text check of every captured
search response found zero occurrences of getPoiInfo, uqscan=,
uqframe=, hysandbox, amap-pc-ssr, or /ssr/place.

- relay-jina-reader (57): only 13 of the 57 have page domain
  r.jina.ai; the other 44 span 29 other page domains. The domain:
  query matches scans in which r.jina.ai appears somewhere in the
  scan, not only scans of jina-proxied fleet pages. The config caps
  this query at LOW confidence, so domain presence alone is not a
  HIGH grade and is not a fleet marker by itself. Routine noise;
  counts recorded, none carried forward.
- title-amap (17): the documented name collisions. Azure
  amap-named hostnames (internal naming prefix, not the map
  service), amapacad.org.ng (Association of Marketing Academic
  Professionals), and French AMAP food-association pages. No fleet
  markers, no HIGH grade. Routine noise.

## Excluded queries (not run)

| Query | Reason |
|---|---|
| domain:amap.com | Task-forbidden; adversarially disabled 2026-10-14: ~809 benign scans/30d vs 0 true positives |
| domain:gaode.com | Task-forbidden; adversarially disabled 2026-10-14: same class as domain:amap.com |
| domain:jqp.vercel.app | Task-forbidden opt-in relay query; counsel judge 2026-10-20: enable only after per-query review; domain presence alone is LOW-worthy at best |
| domain:vanderbi.lt | Task-forbidden opt-in relay query; same counsel 2026-10-20 per-query-review hold |
| domain:ntfy.envs.net | Task-forbidden opt-in relay query; same counsel 2026-10-20 per-query-review hold |
| domain:itty.bitty.site | Task-forbidden opt-in relay query; same counsel 2026-10-20 per-query-review hold |
| domain:cors.bwa.workers.dev | Task-forbidden opt-in relay query; same counsel 2026-10-20 per-query-review hold |
| domain:pingllo.com | Task-forbidden opt-in relay query; same counsel 2026-10-20 per-query-review hold |

## Flag for the coordinator

page.title:"amap" is marked `enabled: false` in the config
(adversarial 2026-10-14: documented acronym collisions), but the
crawl task explicitly ordered it as a proven hunt-grammar query, so
it was run this once as an extra. Its 17 results are exactly the
documented collisions above. The config disablement was not changed.

## Sampling limits

- Anonymous search window: last 30 days only. A zero means no fleet
  pages in the last 30 days of urlscan, not "never".
- Metadata only: full result bodies need login, which was not used.
  Verdicts rest on search metadata (URL, title, scan date, IP/ASN).
- One page per query (size=100); both non-zero queries returned
  fewer than 100 results, so no second page was needed.
- No HTTP failures, no timeouts, no 429. No 429 hard stop was
  triggered.

## Sensitivity note

Raw files are preserved verbatim under `raw/` (never redacted, per
the standing rule). Captured page URLs were checked for token-like
capability values: no triage-passing hits exist, so no token-bearing
hit is carried forward, and no token value is reproduced in this
file. The coordinator should treat the raw files as the verbatim
evidence store and keep any token-bearing content local-only.

## Files

- crawl-progress.log — per-query status lines
- raw/<query-label>/search.json — verbatim API response per query
- raw/<query-label>/.PROVENANCE.txt — source URL, retrieval time
  (UTC), method per query
- raw/<query-label>/*.sha256 — sha256 for each captured file
- raw/screenshots/ — empty (no triage-passing hits)
- hits-draft.json — empty list (0 triage-passing hits)
- crawl.py, triage.py — executor working scripts (not deliverables)
