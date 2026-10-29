# rev-puller-09 — chunk-09 revision pull (2026-10-06)

Worker: REVISION-PULLER-09. Worktree branch: `wikipedia-top500-infra-scan-2026-10-06` (no commit, no push, per brief).

## Method
- Endpoint: MediaWiki `action=query&prop=revisions`, `rvprop=user|timestamp|ids|comment|tags|size`,
  `rvlimit=500`, `rvdir=older`, `rvstart=2026-10-07T00:00:00Z`, `rvend=2020-01-01T00:00:00Z`,
  `formatversion=2`; paginated on `continue.rvcontinue` until exhausted.
- HTTP exclusively via `curl` subprocess (Python HTTP stacks break on this VM's egress proxy).
  URL-encoding only via `python3 urllib.parse.quote`.
- Pacing: ≥5.2 s between requests to en.wikipedia.org; UA `silent-locus-top500-scan/1.0 (research)`.
- Cache: `data/2026-10-06-wikipedia-top500-infra-scan/raw/revisions/<rank>.jsonl`, one JSON object
  per revision: rank, article, revid, parentid, user, timestamp, comment, tags, size.
- Driver: `workers/rev-puller-09/pull_chunk09.py`; run log `workers/rev-puller-09/progress.log`;
  per-article counts `workers/rev-puller-09/counts.json`.

## Result
- **42/42 articles pulled, 51,420 revisions cached, 0 failures, 0 errors.**
- Post-run verification: all 42 `<rank>.jsonl` files exist, every line parses as JSON, no empty files.
- errors.log (`workers/rev-puller-10/errors.log`, per brief): empty — no failures to report.

## Operational note
- The first run was killed by a service restart at ~21:02Z after 19 articles (ranks 378–396);
  four cached files (380–383) did not survive the restart. The script's resume logic re-pulled
  the missing ranks; counts for re-pulled articles were byte-identical to the first run
  (e.g. 336/639/427/2063), confirming deterministic pagination. Final state is complete
  and consistent.

## Per-article counts

| rank | article | revisions |
|------|---------|-----------|
| 378 | Bob Mackie | 336 |
| 379 | Conor Benn | 639 |
| 380 | Teenage Sex and Death at Camp Miasma | 427 |
| 381 | Yemeni civil war (2014–present) | 2063 |
| 382 | BRICS | 2898 |
| 383 | Robin Williams | 1337 |
| 384 | Hannah Waddingham | 883 |
| 385 | United Airlines Flight 175 | 1226 |
| 386 | Runner (2026 American film) | 201 |
| 387 | Madison Beer | 652 |
| 388 | Vladimir Putin | 3541 |
| 389 | Dennis Haskins | 196 |
| 390 | Lamine Yamal | 3382 |
| 391 | New York City | 5616 |
| 392 | Peter Thiel | 1427 |
| 393 | Cat | 1510 |
| 394 | Bharatiya Nyaya Sanhita | 1 |
| 395 | Sardar 2 | 436 |
| 396 | Gable Steveson | 744 |
| 397 | Alex Michelsen | 913 |
| 398 | Jack Lowden | 400 |
| 399 | The Dog Stars (film) | 407 |
| 400 | 2026 FIFA ASEAN Cup | 968 |
| 401 | Elliot Page | 1472 |
| 402 | Bharatiya Sakshya Act, 2023 | 142 |
| 403 | Cleopatra | 958 |
| 404 | John F. Kennedy | 2230 |
| 405 | Ziad Jarrah | 770 |
| 406 | George Michael | 1419 |
| 407 | Ted Bundy | 1497 |
| 408 | Pressure (2026 film) | 341 |
| 409 | Cam Skattebo | 418 |
| 410 | Taylor Sheridan | 459 |
| 411 | Canada | 3643 |
| 412 | Israel | 4039 |
| 413 | The Blame (TV series) | 66 |
| 414 | TNT Sports (United Kingdom) | 919 |
| 415 | Sally Field | 477 |
| 416 | Chad Powers | 338 |
| 417 | Drew Lock | 961 |
| 418 | The Love Hypothesis | 169 |
| 419 | Mid-Autumn Festival | 899 |
| | **TOTAL** | **51,420** |

## Wall time
- First run 20:44:53Z–~21:02Z (killed by service restart, 19 articles done).
- Resume run 21:02:52Z–21:18:08Z; reported wall 916 s (~15 min).
- End-to-end elapsed ~33 min for 42 articles (two runs).

## Anomalies / notes
- Rank 394 (Bharatiya Nyaya Sanhita): only 1 revision in the 2020-01-01→2026-10-07 window —
  the article was created recently (page moved/created 2024) and has minimal history. OBSERVED, not an error.
- No missing pages, no API errors, no curl failures (4-attempt backoff retry was never exhausted).
