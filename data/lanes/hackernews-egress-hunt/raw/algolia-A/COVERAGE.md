# COVERAGE — HN Algolia collector A

Scope: Hacker News Algolia public API only
(`https://hn.algolia.com/api/v1/search`). No key, no login, no account.
Method: `curl -s`, at least 1 second between calls.
Date filter for the new-hit set: `created_at_i >= 1761955200`
(2025-11-01T00:00:00Z). Retrieval window: 2026-10-27 ~13:24–14:30 UTC.
Collector: A. Raw files are verbatim API responses, never redacted.

## Two match variants per query

- `fuzzy`: API default. Typo-tolerant. For `routify` this also matches
  near words such as route, routine, and routing. That is why the
  fuzzy routify sets are huge and mostly off-term noise.
- `exact`: same term with `typoTolerance=false`. Literal term only.
  These sets are small, fully paged, and internally consistent.

Both variants are saved. The exact sets are the reliable core for
triage. The fuzzy sets are verbatim snapshots, not complete sets
(see API notes below).

## File naming

`<term>-<tag>-<mode>-<variant>-p<page>.json`, where mode is
`filtered` (2025-11-01 onward) or `unfiltered` (all dates), and
variant is `fuzzy` or `exact`. Pass-1 files (no variant in the name)
used `hitsPerPage=1000`; pass-2 files use `hitsPerPage=100`.
Every capture file has a `.PROVENANCE.txt` (source URL, retrieval
time, method, query) and a `.sha256` beside it. All SHA256 values
verified after capture.

## Per-query table (pass 2, hitsPerPage=100)

nbHits and nbPages are the values from the page-0 response of that
run. `saved` counts hits in the saved page files.

### Filtered (2025-11-01 onward) — the new-hit set

| term | tag | variant | nbHits | pages | fetched | saved | capped |
|---|---|---|---|---|---|---|---|
| routify | story | fuzzy | 5 | 1 | 1 | 5 | no |
| routify | story | exact | 1 | 1 | 1 | 1 | no |
| routify | comment | fuzzy | 10908 | 10 | 10 | 700 | YES, API 1000-hit browse cap |
| routify | comment | exact | 3 | 1 | 1 | 3 | no |
| aliyuncs | story | fuzzy | 3 | 1 | 1 | 3 | no |
| aliyuncs | story | exact | 2 | 1 | 1 | 2 | no |
| aliyuncs | comment | fuzzy | 13 | 1 | 1 | 13 | no |
| aliyuncs | comment | exact | 12 | 1 | 1 | 12 | no |
| oss-cn | story | fuzzy | 1 | 1 | 1 | 1 | no |
| oss-cn | story | exact | 1 | 1 | 1 | 1 | no |
| oss-cn | comment | fuzzy | 4 | 1 | 1 | 4 | no |
| oss-cn | comment | exact | 4 | 1 | 1 | 4 | no |
| sanmaohe | story | fuzzy | 2 | 1 | 1 | 2 | no |
| sanmaohe | story | exact | 0 | 0 | 1 (empty page 0) | 0 | no |
| sanmaohe | comment | fuzzy | 2 | 1 | 1 | 2 | no |
| sanmaohe | comment | exact | 0 | 0 | 1 (empty page 0) | 0 | no |
| proxy_temp_file | story | fuzzy | 3 | 1 | 1 | 3 | no |
| proxy_temp_file | story | exact | 3 | 1 | 1 | 3 | no |
| proxy_temp_file | comment | fuzzy | 4 | 1 | 1 | 4 | no |
| proxy_temp_file | comment | exact | 4 | 1 | 1 | 4 | no |

Exact filtered totals: routify 1 story + 3 comments; aliyuncs 2 + 12;
oss-cn 1 + 4; sanmaohe 0 + 0; proxy_temp_file 3 + 4. Total 30 rows,
28 unique item ids (item 49379079 appears under 3 terms, see below).

Date ranges observed in saved exact filtered files: routify story
2026-08-20; routify comments 2026-09-02..2026-10-26; aliyuncs story
2026-08-20..2026-09-23; aliyuncs comments 2025-11-19..2026-09-02;
oss-cn story 2026-09-23; oss-cn comments 2025-11-19..2026-07-18;
proxy_temp_file story 2026-03-30..2026-08-20; proxy_temp_file
comments 2026-01-12..2026-09-22.

### Unfiltered (all dates) — OVERLAP-CONTEXT, never candidates

| term | tag | variant | nbHits | pages | fetched | saved | capped |
|---|---|---|---|---|---|---|---|
| routify | story | fuzzy | 5079 | 10 | 10 | 800 | YES, API 1000-hit browse cap |
| routify | story | exact | 7 | 1 | 1 | 7 | no |
| routify | comment | fuzzy | 124743 | 10 | 10 | 1000 | YES, API 1000-hit browse cap |
| routify | comment | exact | 22 | 1 | 1 | 22 | no |
| aliyuncs | story | fuzzy | 45 | 1 | 1 | 45 | no |
| aliyuncs | story | exact | 6 | 1 | 1 | 6 | no |
| aliyuncs | comment | fuzzy | 222 | 3 | 3 | 178 | no, but pages shorted (see notes) |
| aliyuncs | comment | exact | 24 | 1 | 1 | 24 | no |
| oss-cn | story | fuzzy | 5 | 1 | 1 | 5 | no |
| oss-cn | story | exact | 5 | 1 | 1 | 5 | no |
| oss-cn | comment | fuzzy | 16 | 1 | 1 | 16 | no |
| oss-cn | comment | exact | 13 | 1 | 1 | 13 | no |
| sanmaohe | story | fuzzy | 0 | 0 | 1 (empty page 0) | 0 | no |
| sanmaohe | story | exact | 0 | 0 | 1 (empty page 0) | 0 | no |
| sanmaohe | comment | fuzzy | 0 | 0 | 1 (empty page 0) | 0 | no |
| sanmaohe | comment | exact | 0 | 0 | 1 (empty page 0) | 0 | no |
| proxy_temp_file | story | fuzzy | 3 | 1 | 1 | 3 | no |
| proxy_temp_file | story | exact | 3 | 1 | 1 | 3 | no |
| proxy_temp_file | comment | fuzzy | 15 | 1 | 1 | 15 | no |
| proxy_temp_file | comment | exact | 14 | 1 | 1 | 14 | no |

Pre-Nov-2025 exact items (unfiltered exact minus filtered exact),
OVERLAP-CONTEXT only: routify 6 stories + 19 comments; aliyuncs
4 stories + 12 comments; oss-cn 4 stories + 9 comments; sanmaohe 0;
proxy_temp_file 0 stories + 10 comments. Full ids and dates are
derivable from the saved unfiltered exact files.

## Known overlap

HN item 49379079 ("Qwen3.8 Fetches Weird URLs") is present in the
filtered exact story sets for routify, aliyuncs, and proxy_temp_file.
It is KNOWN OVERLAP, never a new hit. It also appears in the fuzzy
and pass-1 files for those terms.

## API errors and instability notes (read before trusting counts)

1. API browse cap: the API returns at most 10 pages at
   hitsPerPage=100, i.e. 1000 hits per single query, whatever nbHits
   says. The three capped queries above are capped samples, NOT full
   sets. Their nbHits values are the API's estimates at call time.
2. Empty pages mid-sequence: in the capped fuzzy routify sets, some
   fetched pages returned 0 hits while later pages returned 100
   (routify comment filtered fuzzy: pages 3, 4, 8 empty, 700 saved
   of 1000; routify story unfiltered fuzzy: pages 1, 2 empty, 800
   saved). The aliyuncs comment unfiltered fuzzy set saved 178 of
   222 across 3 pages (page 1 returned 56 hits against a page-0
   nbHits of 222, then page 2 reported nbHits 222 again with 22
   hits). Saved pages are verbatim; gaps are the API's, not edits.
3. nbHits varies between identical calls. Observed: routify story
   filtered fuzzy reported 5 (twice, hitsPerPage=1 and 100) but 985
   (hitsPerPage=1000, pass 1); sanmaohe comment unfiltered fuzzy
   reported 38 (pass 1) but 0 (pass 2); aliyuncs comment unfiltered
   fuzzy reported 88, then 222. Counts in the table above are from
   the pass-2 run only. Do not treat any single nbHits as exact.
4. hitsPerPage=1000 is mishandled by the API: it reports nbPages=1
   and page >= 1 returns 0 hits. Pass-1 files (no variant in the
   name) are therefore single-page snapshots of at most 1000 hits,
   kept for the record, superseded by pass-2 paging where the two
   disagree.
5. No HTTP errors, no rate-limit responses, no retries needed beyond
   the script's normal path. All calls returned HTTP 200.
6. sanmaohe fuzzy filtered extras (not in any exact set): 2 stories
   matched only via the author field (fuzzy match; handle values
   withheld per lane rule, not reproduced here) and 2 comments
   matched in comment text under typo tolerance. Item ids and dates
   for these four are listed in the collector's return report.
   Exact literal `sanmaohe` returns ZERO hits in every tag/mode
   combination. The named probe host from the Cohere write-up has
   no exact HN match in this pull.

## Mechanical candidate inventory (exact, filtered only)

Item id, title, date, HN URL. No poster handles anywhere. Not a
ranking. Item 49379079 is known overlap, marked as such.

See the collector's return report for the full list. Titles below
are the story title (for comments, the parent story title).

## Files in this directory

- 91 capture JSON files (pass 1 + pass 2, all variants and modes),
  each with `.PROVENANCE.txt` and `.sha256`.
- `fetch_algolia.py`, `fetch_algolia2.py` (collector scripts).
- `_fetch-summary.json`, `_fetch2-summary.json` (run summaries,
  with provenance and SHA files).
- `COVERAGE.md` (this file).
