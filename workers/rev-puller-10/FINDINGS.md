# rev-puller-10 FINDINGS — chunk-10 (ranks 420–458)

## Original pass (2026-10-06, worker died of runtime infra error mid-run)
The original puller (`pull.py`, log `pull.stdout.log`) walked ranks 420–441
before dying. It wrote revision JSONL to `raw/revisions/<rank>.jsonl`.
Per-article counts from its stdout log:

- 420 Haakon VIII: 780 | 421 Joey King: 1021 | 422 Rosh Hashanah: 570
- 423 American Airlines Flight 77: 767 | 424 Russia: 6584
- 425 List of Super Bowl champions: 727 | 426 Arnold Schwarzenegger: 1404
- 427 O. J. Simpson: 1676 | 428 Al Pacino: 1399
- 429 Dark Matter (2024 TV series): 463 | 430 Bruno Mars: 2117
- 431 Trinidad Chambliss: 124 | 432 Germany: 3316
- 433 Barry Melrose: 97 (later clobbered) | 433 List of countries by GDP (nominal): 1455
- 435 Suriya: 860 | 436 Barbarian (2022 film): 976 | 437 Dynatrace: 196
- 438 Harry Potter (TV series): 1082 | 439 Australia: 3249
- 440 Pluribus (TV series): 1412 | 441 Dua Lipa: 470

Known defects at handoff:
- Rank 433 is shared by TWO chunk rows ("Barry Melrose" and
  "List of countries by GDP (nominal)"). Both wrote `revisions/433.jsonl`,
  so the second clobbered the first: only the GDP article survived.
- Files for ranks 420–424 were absent from disk at handoff even though the
  original pass had pulled them (observed: 420/421/422/423 missing, 424 missing
  per the pre-resume check; cause not established — not redone from scratch,
  re-pulled in the resume pass).

## Resume pass (2026-10-06, `pull_resume.py`, log `pull-resume.stdout.log`)

Skip rule applied per row: if `raw/revisions/<rank>.jsonl` exists, is
non-empty, and its first line's `"article"` equals the chunk title -> SKIP.
Ranks 425–432, 435–441 all skipped as existing+correct. Rank 433's plain
file held the GDP article, so "Barry Melrose" was pulled into
`raw/revisions/433_barry_melrose.jsonl` (slug = lowercase, spaces->underscores,
non-alnum stripped, truncated to 30 chars).

Articles pulled in the resume pass (23 total, 29,094 revisions, 0 failures):
- 420 Haakon VIII: 780 | 421 Joey King: 1021 | 422 Rosh Hashanah: 570
- 423 American Airlines Flight 77: 767 | 424 Russia: 6584
- 433 Barry Melrose: 97 -> `433_barry_melrose.jsonl` (433-collision fix)
- 442 Napoleon: 2218 | 443 Tim Cook: 454
- 444 Navier–Stokes existence and smoothness: 374 | 445 Scooter Braun: 912
- 446 Jennifer Lawrence: 1431 | 447 2026: 3534 | 448 Ryan Gosling: 619
- 449 Kayadu Lohar: 609
- 450 2026 Mecklenburg-Vorpommern state election: 271
- 451 The Gentlemen (2019 film): 849 | 452 Hailee Steinfeld: 1693
- 453 Jon Bernthal: 765 | 454 2026 MTV Video Music Awards: 349
- 455 Jason Sudeikis: 851 | 456 Raphinha: 2284 | 457 Taylor Hanson: 152
- 458 Enzo Fernández: 1910

Failures: 0. `errors.log` was not created (no errors occurred).

### 433-collision fix
Both 433 files now exist and are correct:
- `raw/revisions/433.jsonl` — 1,455 revisions, article
  "List of countries by GDP (nominal)"
- `raw/revisions/433_barry_melrose.jsonl` — 97 revisions, article
  "Barry Melrose" (newest rev 2026-09-18, user "TooManyFingers")

Note for downstream consumers: any join on rank=433 must expect TWO article
files (`433.jsonl` + `433_barry_melrose.jsonl`); the rank is not unique.

### Grand totals (chunk-10)
- 40 rows in chunk-10 (ranks 420–458, rank 434 absent, rank 433 duplicated).
- On disk after resume: 41 revision files (40 ranks + the extra 433 slugged file).
- Skipped-correct (16): ranks 425–432, 435–441 incl. both 433 views.
- Resume-pass revisions: 29,094 across 23 articles.
- Skipped-pass revisions: 20,926 across 16 files
  (425:727, 426:1404, 427:1676, 428:1399, 429:463, 430:2117, 431:124,
  432:3316, 433 GDP:1455, 435:860, 436:976, 437:196, 438:1082, 439:3249,
  440:1412, 441:470).
- Chunk-10 complete: every row has a correct, non-empty revisions file.

## Second resume pass (2026-10-06 ~21:18–21:25Z, `resume.py`, log `resume.stdout.log`)

The assigned worker's own resume pass re-pulled ranks 441–458 (18 articles,
19,150 revisions, 0 failures) with a fresh complete pass — no skip rule —
as a runtime-owned background session after the original pass died.

**Real defect fixed:** the sibling resume pass had SKIPPED rank 441 ("Dua Lipa")
because `441.jsonl` existed with the correct article on its first line — but
it was the ORIGINAL pass's partial file (470 revs, written before the crash).
The second pass re-pulled it fully: **441 Dua Lipa = 2,694 revisions**,
timestamps 2020-01-09T15:13:31Z .. 2026-10-06T03:44:46Z (full window).
Ranks 442–458 re-pulls matched the sibling's counts exactly.

**433-file naming:** the second pass initially renamed `433.jsonl`
(GDP list) → `433b.jsonl` and wrote Barry Melrose to a new `433a.jsonl`.
Both renames were REVERTED to match this FINDINGS.md's documented scheme:
`433.jsonl` = GDP list (1,455 revs, restored), `433a.jsonl` deleted (it was
a same-minute duplicate of the sibling's `433_barry_melrose.jsonl`, 97 revs —
own-worker cleanup, not corpus dedup). Downstream contract stands:
rank 433 = `433.jsonl` + `433_barry_melrose.jsonl`.

## Final verified state (2026-10-06T21:26Z)

Post-pull audit over all 41 files in `raw/revisions/` belonging to chunk-10:
every file parses as JSONL, every record's `article` matches its chunk title,
and every per-file timestamp range spans the window floor (2020-01-01+) to
the pull date — no truncated windows. **Total: 52,244 revisions across all 39 chunk rows**
(39 files: 38 rank files + the extra 433 slugged file). Failures: 0.
Highest-volume: Russia (6,584), 2026 (3,534), Germany (3,316), Australia
(3,249), Dua Lipa (2,694).
