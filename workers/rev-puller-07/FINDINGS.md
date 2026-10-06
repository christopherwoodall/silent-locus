# REVISION-PULLER-07 FINDINGS — chunk-07 revision pulls (ranks 296–339)

- Worker: rev-puller-07, branch `wikipedia-top500-infra-scan-2026-10-06` (no branch switch, no commit, no push per task)
- Chunk: `data/2026-10-06-wikipedia-top500-infra-scan/raw/chunks/chunk-07` — 42 articles (ranks 296–300, 302–321, 323–339; ranks 301, 322 absent from chunk)
- Method: `en.wikipedia.org/w/api.php?action=query&prop=revisions`, `rvprop=user|timestamp|ids|comment|tags|size`, `rvlimit=500`, `rvdir=older`, `rvstart=2026-10-07T00:00:00Z`, `rvend=2020-01-01T00:00:00Z`, `formatversion=2`; `continue.rvcontinue` paged to exhaustion
- HTTP: curl only; python3 used for URL-encoding + JSON processing only
- UA: `silent-locus-top500-scan/1.0 (research)`; pacing ≥5 s between requests to en.wikipedia.org
- Cache: `data/2026-10-06-wikipedia-top500-infra-scan/raw/revisions/<rank>.jsonl`, one JSON object per line with keys `rank, article, revid, parentid, user, timestamp, comment, tags, size`
- Scripts/logs: `workers/rev-puller-07/pull_revisions.sh` (main), `pull_repull.sh` / `pull_repull299.sh` (repairs), `pull.log`, `repull.log`, `repull299.log`, `counts.tsv`, `errors.log` (empty — zero failures)

## Results

- Articles pulled OK: **42 / 42** (0 failures)
- Total revisions cached: **45,339**
- Main pass wall time: **892 s** (~14.9 min), 2026-10-06T20:45:12Z → 20:59:47Z (UTC)
- Repair passes: 10-article re-pull 209 s; single-file (299) re-pull 31 s
- Observed timestamp window across cache: **2020-01-01T03:02:56Z → 2026-10-06T20:12:58Z** (inside requested bounds)

## Per-article revision counts

| rank | article | revisions |
|------|---------|-----------|
| 296 | Freddie Mercury | 1277 |
| 297 | Dancing with the Stars (American TV series) | 1823 |
| 298 | Ezra Frech | 132 |
| 299 | Project Hail Mary (film) | 2356 |
| 300 | Celine Dion | 1275 |
| 302 | 2026 US Open – Women's singles | 651 |
| 303 | Kenneth Walker III | 604 |
| 304 | Katie Taylor | 984 |
| 305 | Florence Pugh | 1786 |
| 306 | Steve Jobs | 1162 |
| 307 | Emmy Rossum | 458 |
| 308 | Aaron Pierre (actor) | 511 |
| 309 | The Early Spring | 73 |
| 310 | Dungeon Crawler Carl | 384 |
| 311 | To Catch a Predator | 553 |
| 312 | Queen Victoria | 1166 |
| 313 | Yom Kippur | 598 |
| 314 | 2026 FIFA World Cup | 6747 |
| 315 | Tilcayo | 386 |
| 316 | The Blood of Dawnwalker | 239 |
| 317 | UEFA Nations League | 1206 |
| 318 | Kyle Chandler | 239 |
| 319 | Scarlett Johansson | 1256 |
| 320 | Barack Obama | 2964 |
| 321 | Tom Hardy | 1416 |
| 323 | Kenneth Branagh | 966 |
| 324 | Brothers (2026 TV series) | 101 |
| 325 | Emma Navarro | 805 |
| 326 | Vinnie Jones | 550 |
| 327 | Wordle | 1723 |
| 328 | Gary Oldman | 536 |
| 329 | 2026 Yemen offensives | 801 |
| 330 | David Bale | 92 |
| 331 | Grand Theft Auto VI | 2414 |
| 332 | Harry Shum Jr. | 400 |
| 333 | Adults (TV series) | 265 |
| 334 | Erling Haaland | 3932 |
| 335 | HTTP cookie | 250 |
| 336 | Pornhub | 582 |
| 337 | Todd Beamer | 259 |
| 338 | Wiki | 446 |
| 339 | Miss World 2026 | 971 |

## Failures

None — `errors.log` is empty. No article missing, no API errors.

## Integrity verification (post-repair)

- All 42 `<rank>.jsonl` files present and non-empty
- Every line is valid JSON with all required keys (`rank, article, revid, parentid, user, timestamp, comment, tags, size`)
- `rank`/`article` fields match the chunk on every sampled line; file line counts match `counts.tsv` for all 42 articles

## Incident notes (for orchestrator)

1. **External deletion mid-run (~21:00–21:01Z):** after the main pass completed (42/42 OK, 20:59:47Z), the first 10 files of this chunk (296–300, 302–306) were deleted from the working tree by an external actor. The same "first-N ranks of each chunk" deletion pattern appeared in every other chunk's range (e.g. 1,4 / 174–177 / 217–219 / 256–258 / 340–344 / 378–381 / 420–423 / 459–461). Cause not identified from this lane; no sibling pull script deletes other chunks' files. The 10 files were re-pulled cleanly (identical counts) at 21:03–21:06Z.
2. **Duplicate worker race on chunk-07:** a second agent (`data/.../workers/rev-puller-07/pull_chunk_resume.py`, PID 2702) ran a concurrent resume pass over the same chunk and the same output files while my re-pull was in flight. Its appends interleaved with mine and corrupted `299.jsonl` (2846 lines incl. truncated fragments vs 2356 expected). I did NOT kill it (out of mandate); it finished cleanly (`skipped=35 ok=7 failed=0`). `299.jsonl` was then re-pulled solo after it exited and now verifies clean. Recommendation: avoid assigning two writers to the same chunk/output files concurrently — truncate-then-append scripts corrupt each other's output when raced.
3. Sibling workers (rev-puller-00/03/04/09/11 and an account-profiler lane) were concurrently writing to the shared `raw/revisions/` dir throughout; their own chunks were unaffected by this worker's actions and vice versa, except as noted above.
