# REVISION-PULLER-11 findings — chunk-11 (ranks 459–500)

- Run window: 2026-10-06T20:45:15Z → 2026-10-06T21:28:22Z (~43 min wall, incl. handoff)
- Articles completed: 42 / 42
- **Total revisions cached: 52,792**
- Failed articles: 0

## Per-article revision counts (rank, title, revisions)

| rank | article | revisions |
|------|---------|-----------|
| 459 | Millie Bobby Brown | 1915 |
| 460 | Lust Stories 3 | 84 |
| 461 | Christopher Nolan | 2706 |
| 462 | The Pitt | 1791 |
| 463 | Clavicular (influencer) | 996 |
| 464 | Crew Girl | 63 |
| 465 | Elvis Presley | 1858 |
| 466 | List of highest-grossing Indian films | 5812 |
| 467 | Kylian Mbappé | 3211 |
| 468 | Heath Ledger | 779 |
| 469 | Chelsea F.C. | 3339 |
| 470 | Lewis Pullman | 467 |
| 471 | Ariana Grande | 3760 |
| 472 | A | 546 |
| 473 | George VI | 1911 |
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

## Failures

None. All 42 articles paged to exhaustion (rvcontinue followed until absent).

## Operational notes (worth knowing for the coordinator)

1. **Worker handoff mid-chunk.** My original pull script (`workers/rev-puller-11/pull-chunk.sh`,
   started 20:45:15Z) died unexpectedly around 21:05 (session lost; process gone) after
   completing ranks 459–472 (27,327 revisions). A replacement script (`/tmp/pull-chunk11.sh`,
   started 21:05 by the parent side) completed ranks 459–461 (re-pull; counts identical to mine)
   and 474–500, finishing 21:19:14Z. Its output schema matches the required JSONL schema exactly.
2. **Two gaps the replacement didn't cover were filled by this worker:**
   - rank 473 'George VI': my original process died mid-pull (partial 141KB file, no manifest entry).
     Re-pulled fresh 21:18–21:19Z → 1,911 revisions, moved atomically into `raw/revisions/473.jsonl`.
   - rank 462 'The Pitt': silent data corruption detected — file had only the LAST page
     (291 lines) while the pull counter logged 1,791 (verified true count via a fresh 4-page
     API check: 500+500+500+291). Re-pulled fresh 21:27–21:28Z → 1,791 lines, moved into place.
3. **Logged-count vs file-line audit** was run across all 42 files after the refill; all match.
   Final schema validation (every line: valid JSON, correct rank+article, all 8 required fields):
   52,792 / 52,792 lines valid, zero bad lines.
4. Sibling chunk workers share `raw/revisions/`; chunk-11 files use the `<rank>.jsonl` naming.
   One sibling uses a `<rank>_<slug>.jsonl` scheme (e.g. `433_barry_melrose`) — no collision with ours.
5. Endpoint: `en.wikipedia.org/w/api.php?action=query&prop=revisions`, rvlimit=500, rvdir=older,
   rvstart=2026-10-07T00:00:00Z, rvend=2020-01-01T00:00:00Z, rvprop=user|timestamp|ids|comment|tags|size,
   formatversion=2. HTTP via curl only, UA `silent-locus-top500-scan/1.0 (research)`,
   pacing ≥5s between requests, 3 retries at 30s on transport/HTTP/JSON failure.
6. Cache: `data/2026-10-06-wikipedia-top500-infra-scan/raw/revisions/<rank>.jsonl`
   (one JSON object per line: rank, article, revid, parentid, user, timestamp, comment, tags, size).
   Worker scratch: `workers/rev-puller-11/` (run.log, article-counts.tsv, completed-ranks.txt,
   pull-chunk.sh, gapfill-473.sh, errors.log — errors.log has only the transient gap notes, no article failures).
