# REPULL-WORKER-B findings — 2026-10-06 (repull of ranks 118–131)

Task: re-pull revision JSONL for the 14 articles in `raw/missing-g2.tsv`
(ranks 118–131), lost to VM storage flakiness. HTTP via curl only
(`silent-locus-top500-scan/1.0 (research)` UA, ≥5.5s pacing to
en.wikipedia.org). Temp-file + fsync + atomic rename write path.
Python used for URL-encoding/JSON parsing only — never for HTTP.

Branch: `wikipedia-top500-infra-scan-2026-10-06`. No commits, no pushes,
no branch switches (per brief).

## Run summary

- 14/14 articles pulled successfully; **34,189 revision records** total.
- 77 API requests (rvlimit=500, rvdir=older, rvstart=2026-10-07T00:00:00Z,
  rvend=2020-01-01T00:00:00Z, continue.rvcontinue followed until exhausted).
- No API errors, no transport failures, no retries needed.
- Script bug hit and fixed mid-run: `os.fsync` after the `with` block
  closed the file (ValueError). Rank 118 was re-pulled cleanly after the
  fix; its `.tmp` was deleted before the re-pull. No partial data survived
  into any final file.

## Per-article counts

| rank | article                        | revisions | oldest rev         | newest rev         |
|------|--------------------------------|----------:|--------------------|--------------------|
| 118  | Woody Harrelson                |       706 | 2020-01-03         | 2026-10-05         |
| 119  | Heart of the Beast             |       282 | 2024-03-22         | 2026-10-06         |
| 120  | Michael Polansky               |       273 | 2025-03-14         | 2026-09-28         |
| 121  | Forgotten Island               |       806 | 2025-04-15         | 2026-10-06         |
| 122  | Kate Upton                     |       396 | 2020-01-16         | 2026-10-05         |
| 123  | Frances Tiafoe                 |     1,959 | 2020-01-05         | 2026-09-20         |
| 124  | Rande Gerber                   |       134 | 2020-01-02         | 2026-10-04         |
| 125  | Kaia Gerber                    |       793 | 2020-01-02         | 2026-10-04         |
| 126  | Assassination of Charlie Kirk  |     6,349 | 2025-09-10         | 2026-10-03         |
| 127  | 2026 Iran war                  |    14,257 | 2026-02-28         | 2026-10-06         |
| 128  | Duncan Sheik                   |       222 | 2020-02-11         | 2026-09-23         |
| 129  | Lady Gaga                      |     3,631 | 2020-01-01         | 2026-10-04         |
| 130  | Furious (TV series)            |       183 | 2026-06-28         | 2026-09-26         |
| 131  | Zohran Mamdani                 |     4,198 | 2020-07-22         | 2026-10-06         |

## Verification (verify.py, see verify.log)

For every file: every line parses as JSON; `article` matches the TSV
title; `rank` matches; timestamps are non-increasing (newest → oldest,
rvdir=older). **Zero failures on any of these.**

- 7 files fully OK per the ≤2020-06-01 oldest-revision bar:
  118, 122, 123, 124, 125, 128, 129.
- 7 files flagged SUSPECT by the oldest-newer-than-2020-06-01 rule:
  119, 120, 121, 126, 127, 130, 131.

## SUSPECT-flag disposition: CLEARED (coverage complete, flag benign)

Investigated all 7 rather than silently accepting:

1. Each pull's `continue` loop terminated on an **absent rvcontinue
   token** (the loop only exits on exhaustion), i.e. the MediaWiki API
   returned the article's entire history inside the requested window.
2. Spot-check (independent curl, ≥5s pacing): queried
   `Assassination of Charlie Kirk` for revisions older than its file's
   oldest timestamp (`2025-09-10T19:08:17Z`) with rvend=2020-01-01 — the
   API returned exactly one revision (the creation rev at that timestamp)
   and **no continue token**. There is no deeper history to fetch.
3. The oldest timestamps align with article creation, not truncation:
   - 126 Assassination of Charlie Kirk — 2025-09-10 (day of the event)
   - 127 2026 Iran war — 2026-02-28
   - 130 Furious (TV series) — 2026-06-28
   - 119 Heart of the Beast — 2024-03-22
   - 120 Michael Polansky — 2025-03-14
   - 121 Forgotten Island — 2025-04-15
   - 131 Zohran Mamdani — 2020-07-22 (early stub)

Verdict: the SUSPECT flag is a heuristic true-positive for
"article younger than the window", not incomplete coverage. All 7 files
contain **complete** revision history from article creation to present
within the scan window. Marked as such — do not treat these as gaps.

## Side note (not mine)

`raw/revisions/76.jsonl.tmp` exists but has no final `76.jsonl` — it
belongs to another worker's lane (rank 76 is outside my 118–131 set).
Left untouched for its owner to handle.
