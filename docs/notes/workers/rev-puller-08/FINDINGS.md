# REVISION-PULLER-08 — findings

Chunk: `data/2026-10-06-wikipedia-top500-infra-scan/raw/chunks/chunk-08`
Ranks covered: 340–377 (38 articles)
Window: revisions from 2020-01-01T00:00:00Z up to 2026-10-07T00:00:00Z (paged via rvcontinue, rvlimit=500, rvdir=older)
Method: curl only, UA "silent-locus-top500-scan/1.0 (research)", ≥5s between requests to en.wikipedia.org.

## Per-article revision counts

| rank | article | revisions |
|------|---------|-----------|
| 340 | Suicide of Bill Conradt | 287 |
| 341 | Clint Eastwood | 1359 |
| 342 | Jyothika | 701 |
| 343 | Keanu Reeves | 1148 |
| 344 | Charles Harrelson | 228 |
| 345 | Morgan Freeman | 636 |
| 346 | 2026 Russian legislative election | 451 |
| 347 | Collapse of the World Trade Center | 702 |
| 348 | Supergirl (2026 film) | 1248 |
| 349 | Olivia Rodrigo | 3497 |
| 350 | Unabomber (film) | 106 |
| 351 | Josh Allen | 3869 |
| 352 | East of Eden (novel) | 203 |
| 353 | All Out (2026) | 201 |
| 354 | The Vvaan: Force of the Forrest | 235 |
| 355 | XXX: Return of Xander Cage | 458 |
| 356 | Google Chrome | 802 |
| 357 | Harald V | 1175 |
| 358 | XHamster | 733 |
| 359 | China | 5208 |
| 360 | Odyssey | 895 |
| 361 | Jaxson Dart | 643 |
| 362 | List of presidents of the United States | 1648 |
| 363 | The Shards (TV series) | 274 |
| 364 | 2026 US Open (tennis) | 578 |
| 365 | Al-Qaeda | 1417 |
| 366 | Daisy Ridley | 544 |
| 367 | Toy Story 5 | 2119 |
| 368 | Henry VIII | 967 |
| 369 | Travis Kelce | 2715 |
| 370 | Awarapan 2 | 782 |
| 371 | Welles Crowther | 283 |
| 372 | 2026 Berlin state election | 297 |
| 373 | Ryan Reynolds | 1190 |
| 374 | 2026 United States Senate elections | 4925 |
| 375 | Asian Games | 624 |
| 376 | Hayley Williams | 1198 |
| 377 | United States midterm election | 151 |

**Total revisions cached: 44,497** (verified: sum of file line counts matches; all 38 files present at `raw/revisions/<rank>.jsonl`)

## Failures

**Zero failures.** `errors.log` is empty. No missing/renamed articles, no API errors, no curl timeouts.

## Wall time

- First pass: ~15:55 → ~16:16 CDT (~20 min, 30 of 38 articles finished) — killed mid-rank-364 by a VM service restart.
- Second pass: 500s (~16:17 → ~16:25 CDT), 22 articles, ok=22 fail=0.
- **Total elapsed ≈ 30 min; total active pull ≈ 28 min.**

## Operational notes (for the coordinator)

1. **First pass was interrupted, second pass re-pulled.** After the restart, ranks 340–347 showed "cached" in the first-pass log but the `.jsonl` files were absent from disk; ranks 364–377 were never reached (first pass died mid-364, leaving no `.tmp`). Second pass re-pulled all 22 missing ranks cleanly (the puller skips non-empty files, so completed work was preserved). Final state: all 38 ranks present and verified. Unexplained file disappearance of 340–347 between passes — flagged, not investigated further (no writes were lost since re-pull succeeded).
2. **Sibling workers are concurrently hitting en.wikipedia.org** (rev-puller-03, -04, -09, -10 observed live during this run), each with the same scan UA. Each worker paces itself at ≥5s/request; aggregate request rate is higher. Worth knowing if Wikipedia starts rate-limiting.
3. **Schema discrepancy to reconcile:** my JSONL records use exactly the assigned schema `{rank,article,revid,parentid,user,timestamp,comment,tags,size}` (verified on all 38 files). A sibling worker's (rev-puller-03) on-disk verification asserts an extra `"temp"` key in its records (presumably temp-account flag for the temp-account-clustering pivot). The coordinator should decide whether to backfill `"temp"` across chunks or standardize on one schema.
4. Script preserved at `workers/rev-puller-08/pull.sh`; run log at `workers/rev-puller-08/pull.log`.
