# REPULL-WORKER-C findings (2026-10-06)

Re-pulled all 21 articles from `missing-g3.tsv` (ranks 256-295, gaps at 260-277 and 289 where files were intact).

## Method
- Endpoint: `action=query&prop=revisions`, `rvprop=user|timestamp|ids|comment|tags|size`,
  `rvlimit=500`, `rvdir=older`, `rvstart=2026-10-07T00:00:00Z`, `rvend=2020-01-01T00:00:00Z`,
  continue.rvcontinue loop. HTTP via curl only; UA `silent-locus-top500-scan/1.0 (research)`;
  5.2s pacing between requests (plus ~5s between articles).
- Pre-pass check (single multi-title query): all 21 titles exist, main-namespace, none are
  redirects, none missing.
- Writes: temp file `<rank>.jsonl.tmp` -> fsync -> atomic rename to `<rank>.jsonl`.
- Script: `/tmp/repull_c.py`; raw manifest: `/tmp/repull_c_manifest.json`.

## Per-article counts (revisions pulled, 2020-01-01 -> 2026-10-07 window)

| rank | article | revs | newest | oldest | verdict |
|---|---|---|---|---|---|
| 256 | Zoe Saldaña | 1487 | 2026-10-02T18:40:08Z* | 2020-01-03T00:08:51Z | OK |
| 257 | Lili Reinhart | 433 | 2026-09-30T14:09:35Z | 2020-01-07T22:44:36Z | OK |
| 258 | Weapons (2025 film) | 2630 | 2026-10-04T02:35:04Z | 2023-03-09T17:13:07Z | SUSPECT (see note) |
| 259 | Bayeux Tapestry | 732 | 2026-10-06T17:13:26Z | 2020-01-01T10:46:57Z | OK |
| 278 | The Love Hypothesis (film) | 165 | 2026-10-03T17:42:01Z | 2025-10-20T05:56:11Z | SUSPECT (see note) |
| 279 | Adéla (singer) | 736 | 2026-10-06T13:21:40Z | 2024-12-08T03:55:13Z | SUSPECT (see note) |
| 280 | 2026 Men's European Volleyball Championship | 675 | 2026-09-30T08:30:24Z | 2023-07-20T12:33:23Z | SUSPECT (see note) |
| 281 | India | 5092 | 2026-10-06T17:44:17Z | 2020-01-01T05:55:08Z | OK |
| 282 | Iva Jovic | 591 | 2026-10-06T09:04:37Z | 2024-01-26T08:47:09Z | SUSPECT (see note) |
| 283 | Money in the Bank (2026) | 228 | 2026-10-06T14:28:18Z | 2025-05-23T00:04:03Z | SUSPECT (see note) |
| 284 | George W. Bush | 1840 | 2026-09-27T17:06:56Z | 2020-01-12T08:18:50Z | OK |
| 285 | Richard O'Sullivan | 211 | 2026-09-08T21:27:47Z | 2020-01-04T08:44:01Z | OK |
| 286 | Bruce Willis | 809 | 2026-09-21T16:34:52Z | 2020-01-03T18:46:12Z | OK |
| 287 | Stuart Fails to Save the Universe | 469 | 2026-10-03T21:37:13Z | 2024-07-14T17:26:57Z | SUSPECT (see note) |
| 288 | Presley Gerber | 139 | 2026-10-05T20:06:34Z | 2026-09-21T07:52:43Z | SUSPECT (see note) |
| 290 | I'm Game (film) | 297 | 2026-10-06T04:48:30Z | 2026-07-24T16:23:02Z | SUSPECT (see note) |
| 291 | Sunny Balwani | 505 | 2026-10-06T15:46:12Z* | 2020-01-01T13:11:12Z | OK |
| 292 | Miku Martineau | 58 | 2026-09-27T03:37:43Z | 2025-05-22T13:08:46Z | SUSPECT (see note) |
| 293 | I, Robot (film) | 506 | 2026-09-20T01:14:10Z | 2020-01-01T15:12:51Z | OK |
| 294 | Andrew Garfield | 1142 | 2026-10-06T10:31:51Z | 2020-01-01T19:24:28Z | OK |
| 295 | Alix Earle | 439 | 2026-10-06T20:06:11Z | 2023-08-13T17:12:03Z | SUSPECT (see note) |

\* seconds differ between pull log and verify due to log-line truncation; file contents are authoritative.

**Total revisions re-pulled: 19,184**

## Verification results (script `/tmp/verify_c.py`)
For every file: all lines valid JSON; schema fields present; `article` matches the requested
title and `rank` matches on every line; timestamps non-increasing; no duplicates in line count.
**No FAIL verdicts: 0 missing files, 0 JSON errors, 0 article/rank mismatches, 0 ordering breaks.**

- 10 files OK (oldest revision <= 2020-06-01, full window covered).
- 11 files SUSPECT under the strict oldest<=2020-06-01 rule: all have oldest revisions NEWER
  than 2020-06-01.

## SUSPECT note (confidence check, not a negative)
All 11 SUSPECT files are genuinely young pages, not truncated pulls. Follow-up single-title
`rvdir=newer&rvlimit=1` queries (11 requests, same pacing) confirmed each file's oldest pulled
revision equals the page's actual first-ever revision:

- Weapons (2025 film): first rev 2023-03-09 (revid 1143749384) - page created for the 2026 film
- The Love Hypothesis (film): first rev 2025-10-20 (1317820000)
- Adéla (singer): first rev 2024-12-08 (1261823847)
- 2026 Men's European Volleyball Championship: first rev 2023-07-20 (1166265270)
- Iva Jovic: first rev 2024-01-26 (1199183717)
- Money in the Bank (2026): first rev 2025-05-23 (1291722020)
- Stuart Fails to Save the Universe: first rev 2024-07-14 (1234497521)
- Presley Gerber: first rev 2026-09-21 (1375986058) - page ~15 days old at pull time
- I'm Game (film): first rev 2026-07-24 (1365819718)
- Miku Martineau: first rev 2025-05-22 (1291631204)
- Alix Earle: first rev 2023-08-13 (1170192763)

Continue loops terminated naturally (no rvcontinue returned) for all articles, so the pull
covers the full window 2020-01-01 -> 2026-10-07 for every page. The SUSPECT flag is retained
per the brief; the underlying cause is page age, verified by the first-revision match above.

## Leftovers
Two `.tmp` files in revisions/ (`66.jsonl.tmp`, `129.jsonl.tmp`) belong to sibling workers
(not my rank range); left untouched.
