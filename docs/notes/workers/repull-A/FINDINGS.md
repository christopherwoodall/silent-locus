# REPULL-WORKER-A findings — missing-g1.tsv (ranks 47–96)

Run: 2026-10-06 21:35–21:52 UTC (~17 min). Method: curl-only GET to
en.wikipedia.org API (rvlimit=500, rvdir=older, window 2020-01-01 →
2026-10-07T00:00:00Z), continue pagination to exhaustion, ≥5.5s pacing,
UA `silent-locus-top500-scan/1.0 (research)`. Wrote each `<rank>.jsonl.tmp`
then fsync + atomic rename to `<rank>.jsonl`. No commits/pushes, no branch
switches (stayed on `wikipedia-top500-infra-scan-2026-10-06`).

## Per-article results

| rank | article | revisions | newest revision | oldest revision | verdict |
|------|---------|-----------|-----------------|-----------------|---------|
| 47 | The Paradise (2026 Indian film) | 1 | 2026-10-04T02:48:41Z | 2026-10-04T02:48:41Z | SUSPECT† |
| 48 | Donald Trump | 22871 | 2026-10-06T13:55:50Z | 2020-01-01T00:00:11Z | OK |
| 58 | Pac (wrestler) | 882 | 2026-10-05T22:44:49Z | 2020-01-04T01:36:31Z | OK |
| 59 | Macklemore | 408 | 2026-10-01T20:54:10Z | 2020-01-20T08:33:30Z | OK |
| 60 | John Tuggle | 95 | 2026-10-06T18:13:35Z | 2020-03-02T20:48:10Z | OK |
| 61 | Aryna Sabalenka | 2396 | 2026-10-03T10:17:33Z | 2020-01-07T12:34:03Z | OK |
| 62 | XXX (film series) | 385 | 2026-09-25T21:39:12Z | 2020-01-10T18:25:09Z | OK |
| 63 | XXXX (beer) | 536 | 2026-09-25T02:57:15Z | 2020-03-11T16:20:34Z | OK |
| 64 | YouTube | 2610 | 2026-10-05T19:20:34Z | 2020-01-01T15:15:18Z | OK |
| 65 | United Airlines Flight 93 | 1153 | 2026-10-05T08:16:25Z | 2020-01-09T01:32:12Z | OK |
| 66 | Kaya Scodelario | 703 | 2026-10-05T07:23:58Z | 2020-01-05T09:45:08Z | OK |
| 67 | Obsession (2025 film) | 2397 | 2026-10-06T04:06:58Z | 2025-09-07T20:25:03Z | SUSPECT† |
| 68 | Charlie Kirk | 4984 | 2026-10-05T04:43:46Z | 2020-04-18T05:48:21Z | OK |
| 69 | XXX (2002 film) | 462 | 2026-09-18T19:54:02Z | 2020-01-04T01:42:30Z | OK |
| 71 | Jeff Bezos | 1603 | 2026-10-04T20:32:00Z | 2020-01-06T16:55:55Z | OK |
| 72 | Digger (2026 film) | 931 | 2026-10-06T21:33:19Z | 2024-02-22T23:20:01Z | SUSPECT† |
| 73 | The Whisper Man | 151 | 2026-10-01T02:16:41Z | 2025-02-05T19:55:05Z | SUSPECT† |
| 74 | Lioness (American TV series) | 747 | 2026-10-05T04:20:00Z | 2023-01-13T14:50:05Z | SUSPECT† |
| 75 | Alan Ritchson | 714 | 2026-09-29T05:24:36Z | 2020-01-09T06:08:26Z | OK |
| 76 | Wikipedia | 2801 | 2026-10-06T19:55:21Z | 2020-01-04T12:52:30Z | OK |
| 77 | Ted Lasso | 3025 | 2026-10-06T13:38:41Z | 2020-05-30T02:08:28Z | OK |
| 78 | Cindy Crawford | 364 | 2026-10-05T15:55:10Z | 2020-01-06T20:38:35Z | OK |
| 79 | Matthew Rhys | 541 | 2026-09-30T00:44:01Z | 2020-01-01T02:11:26Z | OK |
| 81 | Dancing with the Stars season 35 | 581 | 2026-10-06T20:11:47Z | 2026-04-23T00:26:24Z | SUSPECT† |
| 82 | Silo (TV series) | 1091 | 2026-10-03T22:40:14Z | 2021-05-20T19:17:18Z | SUSPECT† |
| 83 | Practical Magic 2 | 424 | 2026-10-06T05:36:33Z | 2024-06-10T20:08:58Z | SUSPECT† |
| 84 | Shailene Woodley | 917 | 2026-09-27T09:15:01Z | 2020-01-03T15:46:30Z | OK |
| 85 | Justin Verlander | 1402 | 2026-10-02T15:45:40Z | 2020-01-04T18:53:46Z | OK |
| 86 | Practical Magic | 456 | 2026-10-05T22:47:23Z | 2020-02-08T20:38:35Z | OK |
| 87 | Slow Horses | 1481 | 2026-10-06T21:18:10Z | 2020-12-14T16:19:42Z | SUSPECT† |
| 88 | List of Marvel Cinematic Universe films | 2220 | 2026-10-04T20:58:00Z | 2020-01-03T23:16:37Z | OK |
| 89 | 2026 Swedish general election | 704 | 2026-10-05T01:37:42Z | 2022-10-19T13:47:34Z | SUSPECT† |
| 90 | Osama bin Laden | 2090 | 2026-10-06T00:40:54Z | 2020-01-06T05:56:17Z | OK |
| 91 | Sandra Bullock | 417 | 2026-09-21T14:47:04Z | 2020-01-03T17:05:25Z | OK |
| 92 | Nathan Fielder | 558 | 2026-10-04T23:45:52Z | 2020-01-13T07:11:17Z | OK |
| 93 | Microdata (HTML) | 49 | 2026-06-02T19:46:59Z | 2020-02-20T03:32:29Z | OK |
| 94 | Reacher season 4 | 299 | 2026-10-05T13:22:42Z | 2026-07-26T15:09:01Z | SUSPECT† |
| 96 | Michael Jackson | 2988 | 2026-10-06T00:18:18Z | 2020-01-05T16:19:05Z | OK |

† **SUSPECT explained (not pagination failures):** the oldest revision in
each of these 11 files has `parentid=0` — i.e. it IS the page-creation
revision. These are young pages (2026 Indian film, 2026/2025 films, 2026
TV seasons, Swedish 2026 election, Slow Horses), so the window is fully
covered: no revisions exist before page creation. Not a data gap.

**Total: 66,513 revisions across 39 articles.**

## Verification results

- Valid JSONL on every line, all 39 files: **PASS** (0 malformed lines).
- `rank` + `article` match expected title/rank on every line: **PASS**.
- Timestamps non-increasing (rvdir=older order) in all 39 files:
  **PASS** (0 out-of-order lines).
- Oldest timestamp ≤ 2020-06-01 (full-window coverage): **28 PASS**,
  **11 SUSPECT** — all 11 confirmed as genuine page-creation revisions
  (`parentid=0` on oldest), i.e. the pages postdate the window start.
  Flagged here per the rule, not silently accepted.
- No `.tmp` files left behind; all files written via fsync + atomic rename.

## Notes

- Largest pulls: Donald Trump 22,871 (46 requests), Charlie Kirk 4,984
  (10 requests, heaviest 2025 activity), Ted Lasso 3,025, Michael Jackson
  2,988, Wikipedia 2,801, YouTube 2,610.
- Smallest: The Paradise (2026 Indian film) — exactly 1 revision total
  (page created 2026-10-04, no edits since).
- No API errors required retries this run; no title was missing/moved.
- Progress log: `workers/repull-A/progress.log`; collection script:
  `workers/repull-A/repull_a.py`.
