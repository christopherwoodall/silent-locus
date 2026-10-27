# HN Collector C — Coverage note

Collector: HN Collector C, Hacker News egress hunt lane.
Method: HN Algolia public API only (`https://hn.algolia.com/api/v1/search`).
No key, no login, no account, no voting, no commenting, no HTML scraping.
Polite pace: at least 1.2 seconds between calls.
Date boundary: 2025-11-01 00:00:00 UTC (`created_at_i` 1761955200).
Retrieval date: 2026-10-27. All dates below are UTC.

This collector only collects. No triage, ranking, or judgement was applied.
Every hit the API offered for a query was saved, including noise.
Triage is a later lane's job.

## New-hit set (2025-11-01 onward): fully paged

One JSON file per term per tag. Each file is a JSON array of raw
Algolia page-response objects, byte-preserved per page. Each file has
a `.PROVENANCE.txt` (source URL, retrieval time, method) and a
`.sha256` beside it. All SHA256 checks verified OK after capture.

| Term | Tag | nbHits at fetch | Pages fetched | Hits saved | Date range observed (UTC) |
|---|---|---|---|---|---|
| model fetched | story | 75 | 1 | 75 | 2025-11-03 .. 2026-10-26 |
| model fetched | comment | 546 | 2 | 546 | 2025-11-02 .. 2026-10-27 |
| hallucinated URL | story | 27 | 1 | 27 | 2025-11-21 .. 2026-09-17 |
| hallucinated URL | comment | 187 | 1 | 187 | 2025-11-11 .. 2026-10-26 |
| signed URL | story | 57 | 1 | 57 | 2025-11-04 .. 2026-10-25 |
| signed URL | comment | 582 | 2 | 582 | 2025-11-02 .. 2026-10-26 |
| called home | story | 87 | 1 | 87 | 2025-11-18 .. 2026-10-27 |
| called home | comment | 1384 | 4 (date-split, see below) | 1384 | 2025-11-02 .. 2026-10-27 |
| agent exfiltration | story | 63 | 1 | 63 | 2025-11-07 .. 2026-09-03 |
| agent exfiltration | comment | 187 | 1 | 187 | 2025-11-09 .. 2026-10-24 |
| model exfiltrated | story | 42 | 1 | 42 | 2025-11-07 .. 2026-10-20 |
| model exfiltrated | comment | 223 | 1 | 223 | 2025-11-03 .. 2026-10-26 |
| **Total** | | **3460** | | **3460** | |

Mechanical inventory: `candidates-C.tsv` (3460 rows, 3384 unique item
ids; the gap is items matching more than one term/tag). Columns are
item id, kind, title (or parent story title for comments), date,
HN item URL, matched term, tag, parent story id, source file.
No poster handles appear anywhere in collector notes or inventories.
Raw API bytes may contain handles; that is the raw record, and no
handle was copied out of it.

## Pre-Nov-2025 context set (OVERLAP-CONTEXT, never candidates)

Same 6 terms x 2 tags, filter `created_at_i < 1761955200`. Captured
sets are saved with the suffix `__pre20251101` and the same
provenance triple. Their rows live in `context-pre20251101.tsv`
(1815 rows), kept separate from the candidate inventory.

| Term | Tag | nbHits at fetch | Pages fetched | Hits saved | Date range observed (UTC) |
|---|---|---|---|---|---|
| model fetched | story | 134 | 1 | 134 | 2009-09-30 .. 2025-10-27 |
| hallucinated URL | story | 15 | 1 | 15 | 2022-12-24 .. 2025-10-05 |
| hallucinated URL | comment | 424 | 1 | 424 | 2009-04-23 .. 2025-10-30 |
| signed URL | story | 201 | 1 | 201 | 2008-04-29 .. 2025-10-03 |
| called home | story | 421 | 1 | 421 | 2007-08-28 .. 2025-10-27 |
| agent exfiltration | story | 7 | 1 | 7 | 2023-01-25 .. 2025-10-14 |
| agent exfiltration | comment | 213 | 1 | 213 | 2008-09-25 .. 2025-10-24 |
| model exfiltrated | story | 6 | 1 | 6 | 2023-01-24 .. 2025-09-07 |
| model exfiltrated | comment | 394 | 1 | 394 | 2013-08-05 .. 2025-10-31 |
| **Captured context total** | | **1815** | | **1815** | |

## Capped queries (recorded, not presented as full sets)

Cap rule used: 2000 hits per term/tag query. These three pre-Nov
comment sets exceeded it. Page 0 was observed only to read the total;
0 hits were saved and no capture file was written for them.

| Term | Tag | nbHits reported at probe (approximate, see below) | Hits saved |
|---|---|---|---|
| model fetched | comment, pre-Nov | 2075 | 0 |
| signed URL | comment, pre-Nov | 6838 | 0 |
| called home | comment, pre-Nov | 15258 | 0 |

No new-hit-set query hit the cap. The largest new-hit set
(called home comments, 1384) is under the cap and was fully captured
via the date split below.

## Algolia pagination cap and the called home recovery

Algolia caps offset pagination at 1000 hits per query. The first
single-query capture of called home comments (filtered set) returned
`nbHits` 1384 but `nbPages` 2, holding only 1000 hits; requesting
page 2 returned empty hits with the message "you can only fetch the
1000 hits for this query". That incomplete file was replaced, not
kept alongside: `recover_called_home_comment.sh` re-fetched the same
set as two disjoint date halves (2025-11-01 .. 2026-05-01: 680 hits,
2 pages; 2026-05-01 .. retrieval: 704 hits, 2 pages). 680 + 704 =
1384, matching the single-query total, and all 1384 objectIDs are
unique. The replacement is documented in that file's provenance note.
Every other captured set was verified complete against the API's
offered pages: each multi-page capture ends in a partial page, and
every single-page capture holds fewer than 500 hits.

## Count caveat: Algolia totals are approximate

Every page response carries `exhaustiveNbHits: false`. Algolia's own
totals visibly vary run to run: the identical unfiltered
"model fetched" comment query returned 2621, then 885, then 2619,
then 2608 within minutes. Treat every nbHits total in this note as
as-reported-at-fetch-time, not exact. What is verified is the
captured content: hits saved equal the pages the API offered, pages
were followed to the end of each offered set, and SHA256 checks pass.
Sizing probes (hitsPerPage 0 and 1) are kept in `probes/` for audit
but are not totals; do not quote them.

## API errors

None. No HTTP failure and no curl failure occurred in any fetch.
The only API-side message was the 1000-hit pagination limit above,
which is a platform limit, not an error, and was worked around with
the date split. `fetch-errors.log` holds only the three cap records.

## Noise caveats

These six phrases are loose English nets, not behavior tests. They
return large amounts of non-agent material (ordinary software
phoning home, presigned-URL engineering discussion, general
exfiltration talk). Nothing was filtered beyond the date rule, per
the brief. Expect the candidate inventory to be mostly noise;
that filtering belongs to triage, not collection.

## Known overlap

HN item 49379079 ("Qwen3.8 Fetches Weird URLs") does NOT appear in
any of this collector's 6-term captures (new-hit set or context set).
It stays known overlap, never a new hit; its absence here only means
none of these six phrases matched it in the API's offered results.

## Files in this directory

- 12 new-hit captures + 9 context captures, each with
  `.PROVENANCE.txt` and `.sha256`.
- `candidates-C.tsv` — mechanical candidate inventory (new-hit set).
- `context-pre20251101.tsv` — mechanical context inventory (pre-Nov).
- `fetch.sh` — the capture script. `recover_called_home_comment.sh`
  — the called home comment recovery script.
- `build_inventory.py` — the inventory builder.
- `fetch-run.log`, `fetch-errors.log`, `cap-notes.txt` — run records.
- `probes/` — sizing probes and diagnostics (audit trail, not totals).

## Boundaries kept

- No Factum writes; nothing under `data/records/` or
  `data/.local/factum.db` was touched.
- No git operations of any kind.
- No other lane's or report's files were touched. The sibling
  broad agent-egress hunt directory was not opened or modified.
- No poster handles in any collector note or inventory.
