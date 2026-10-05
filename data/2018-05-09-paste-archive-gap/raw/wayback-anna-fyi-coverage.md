# Wayback CDX coverage for anna.fyi — queue note (Lane 1 retry, 2026-09-28)

## Why the existing shortener-cdx loop was NOT extended

`hidden_files/shortener-cdx/shortener_cdx_retry.sh` + `pull_and_explode.py` is a
**shortener-stats Wayback slice**: a hard-coded `TARGETS` list of 12 YOURLS
stats-page URLs, parsed by a bespoke `ReferrerTableParser` into the
`university-shorteners` evidence schema, committed under
`data/university-shorteners/wayback` + `data/university-shorteners-events`.

anna.fyi URLs are **not** covered there, and bolting them onto `TARGETS` would
break the loop's scope: the parser explodes rows as YOURLS traffic-source
events, the git-add pathspecs (`hidden_files/shortener-cdx`,
`data/university-shorteners/wayback`, `data/university-shorteners-events`)
don't fit anna.fyi paste records, and the loop's commit message semantics are
tied to the shortener slice. The loop polls every 15 min through
2026-09-30 12:00 UTC and must not be touched; no competing loop was launched.

## What to add (for a future lane, once CDX recovers)

A new, separate worker — same repo root conventions as `pull_and_explode.py`
(polite pacing, cache-busting nonce per the standing liveness rule, staged to
disk only, per-ID evidence records) — running these exact queries when
`https://web.archive.org/cdx/search/cdx?url=example.com&output=json&fl=timestamp&limit=1`
returns 200 again (currently 503):

### Query set (all read-only, JSON output)

1. **All archived anna.fyi view pages (paste-ID discovery):**
   `https://web.archive.org/cdx/search/cdx?url=anna.fyi/view/*&matchType=prefix&output=json&fl=timestamp,original,statuscode,digest&filter=statuscode:200&collapse=urlkey`
   — `collapse=urlkey` keeps one row per paste ID; `original` yields the ID
   in the URL path (e.g. `anna.fyi/view/3e9a2b38`). Sort by `timestamp` to
   recover creation ordering. Expected yield: any paste ever captured,
   including IDs outside our 55 and outside the 106 now held in Lane 1.

2. **API census snapshots:**
   `https://web.archive.org/cdx/search/cdx?url=anna.fyi/api/recent&output=json&fl=timestamp,original,statuscode,digest&filter=statuscode:200`
   — a captured `api/recent` response embeds 15 pids + titles + epochs as of
   capture time. Historical captures = point-in-time recents lists the live
   endpoint can never re-serve.

3. **Named-list pages:**
   `https://web.archive.org/cdx/search/cdx?url=anna.fyi/lists*&matchType=prefix&output=json&fl=timestamp,original,statuscode,digest&filter=statuscode:200`

### Why this matters now

Lane 1 (2026-09-28) recovered 51 new anna.fyi IDs from a third-party GitHub
corpus + search-engine index (see PROVENANCE.md). Wayback CDX is the only
remaining passive surface for IDs published in neither source, plus
point-in-time `api/recent` snapshots. When CDX recovers, the new worker should
dedupe discovered IDs against `data/paste-archive/anna.fyi/titles.jsonl`
(our 55) and the Lane-1 manifest before staging new bodies.

### Scope guard

This worker is DISK ONLY (hosted-Elastic writes frozen). It does not compete
with `shortener_cdx_retry.sh` — different target set, different parser,
different output dir (`data/paste-archive-gap/wayback/`), different DONE
marker (`data/paste-archive-gap/wayback/DONE`).
