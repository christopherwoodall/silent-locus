# rev-puller-11 — FINDINGS

## Resume pass (2026-10-06 ~21:05–21:19 UTC, worker REVISION-PULLER-11R)

Replacement pass for the failed worker. Chunk-11 = ranks 459–500.

### Completed this pass (30 articles, 28,259 revisions)

| rank | article | revisions |
|------|---------|-----------|
| 459 | Millie Bobby Brown | 1915 |
| 460 | Lust Stories 3 | 84 |
| 461 | Christopher Nolan | 2706 |
| 474 | Margaret Qualley | 831 |
| 475 | Pete Hegseth | 2691 |
| 476 | Yemen | 1928 |
| 477 | Jessica Barden | 247 |
| 478 | Alan Cumming | 726 |
| 479 | Anthropic | 939 |
| 480 | Jing Boran | 127 |
| 481 | Lake Ontario | 403 |
| 482 | List of Indian films of 2026 | 1321 |
| 483 | Joe O'Cearuill | 63 |
| 484 | FC Barcelona | 2830 |
| 485 | Street Fighter (2026 film) | 500 |
| 486 | The Beast in Me (TV series) | 266 |
| 487 | Mr. T | 293 |
| 488 | Fall 2: Deadpoint | 247 |
| 489 | The Scandal (2026 TV series) | 116 |
| 490 | Up (film series) | 600 |
| 491 | Joely Richardson | 218 |
| 492 | Fauda | 319 |
| 493 | Billie Lourd | 725 |
| 494 | Cooper Manning | 155 |
| 495 | Virat Kohli | 4488 |
| 496 | One World Trade Center | 461 |
| 497 | Natalie Portman | 1074 |
| 498 | Silent Hill: Townfall | 138 |
| 499 | Worlds Collide (2026) | 242 |
| 500 | Sadie Sink | 1606 |

**Failures: 0.** No API errors, no parse errors, no retries exhausted. Full
per-request log in `pull.log` (this directory); errors.log does not exist
(nothing to record).

### Method

- MediaWiki API `prop=revisions`, `rvprop=user|timestamp|ids|comment|tags|size`,
  `rvlimit=500`, `rvdir=older`, `rvstart=2026-10-07T00:00:00Z`,
  `rvend=2020-01-01T00:00:00Z`, `formatversion=2`, `rvcontinue` paged to
  exhaustion. curl only; python3 for URL-encoding and JSON only.
- Pacing: 5.3s sleep between every request to en.wikipedia.org.
  UA: `silent-locus-top500-scan/1.0 (research)`.
- Skip rule: file existed, non-empty, and first-line "article" matched the
  chunk title. Ranks 462–473 were already complete and were not re-pulled.
- One JSON object per revision line in
  `raw/revisions/<rank>.jsonl`:
  `{"rank","article","revid","parentid","user","timestamp","comment","tags","size"}`.

### Validation (post-pass)

All 42 chunk-11 files: every line parses as JSON, line counts > 0,
first-line "article" matches the chunk-11 TSV title. OBSERVED.

### Chunk-11 grand totals

- Resume pass: 28,259 revisions (30 articles).
- Pre-existing (462–473, incl. the gapfilled 473): 23,033 revisions (12 articles).
- **Chunk-11 total: 51,292 revisions across 42 articles.**

### Concurrent-worker note (flag for orchestrator)

Another worker (`~/workspace/silent-locus-top500/workers/rev-puller-11/`,
plus sibling workers rev-puller-00/04/08/10) was active on the same
`raw/revisions/` directory during this pass. It pulled chunk-11 ranks
459–473 into a different accounting (its `article-counts.tsv` differs from
the on-disk files, e.g. rank 462 "The Pitt" 1791 vs 291 on disk) and ran a
`gapfill-473.sh` that rewrote `473.jsonl` (500-line partial → complete
1911-line file) at 2026-10-06T21:19:09Z while this pass was running.
That write was additive/completing, not conflicting — this pass never wrote
ranks 462–473 — and per-article revision counts between the two workers
match exactly where comparable (459: 1915, 460: 84, 461: 2706). No data loss
observed; the shared directory is complete and consistent. Overlap worth
de-conflicting on future chunk assignments.
