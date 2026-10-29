# REVISION-PULLER-00 findings (chunk-00, wikipedia-top500-infra-scan)

- First pass: 2026-10-06T20:45:10Z .. 2026-10-06T21:01:50Z (worker 00, died on a runtime infra error at START of rank 14)
- Resume pass (REVISION-PULLER-00R): 2026-10-06T21:04:14Z .. 2026-10-06T21:29:29Z, wall 25m 15s
- Chunk articles: 42 (ranks 1,4,5,6,8-33,35-46)
- Articles cached successfully: 42/42 (first pass: 10, resume pass: 35 incl. 3 re-pulls)
- Articles failed: 0 (errors.log empty — zero HTTP/API failures in either pass)
- Total revisions cached (grand, verified on disk): **91,180**
- Revision window: 2020-01-01T00:00:00Z .. 2026-10-07T00:00:00Z (rvdir=older, rvlimit=500, follow rvcontinue to exhaustion)
- Cache dir: data/2026-10-06-wikipedia-top500-infra-scan/raw/revisions/ (`<rank>.jsonl`, one JSON object per line: rank, article, revid, parentid, user, timestamp, comment, tags, size)
- Per-article record: workers/rev-puller-00/per-article.txt (42 lines, rank order; counts verified == lines on disk)

## Resume pass (REVISION-PULLER-00R): per-article revision counts

35 articles, 66,233 revisions, 0 failures. Re-pulled rank 14 from scratch (first-pass
cache was partial: 500 lines, last ts 2026-09-17). Skipped ranks 6,8,9,10,11,12,13
(already cached, verified first-line "article" match).

```
1	Main Page	80
4	Lizzie Borden	1002
5	Killing of the Clancy children	847
14	Resident Evil (2026 film)	1130
15	Neatsville, Kentucky	42
16	2026 Asian Games	1223
17	India at the 2026 Asian Games	2868
18	Monster: The Lizzie Borden Story	95
19	Lanterns (TV series)	1580
20	Ted Kaczynski	2483
21	Toxic (2026 film)	2175
22	2026 Asian Games medal table	543
23	Anna's Archive	1304
24	Spider-Man: Brand New Day	3568
25	Aileen Wuornos	1173
26	Gloria Steinem	771
27	Mirzapur (film)	539
28	The Gentlemen (2024 TV series)	593
29	ChatGPT	4046
30	Limonene	193
31	Ansel Adams	555
32	The Odyssey (2026 film)	2968
33	Ben Shelton	1585
35	Dolly Parton	3695
36	United States	13929
37	List of highest-grossing films	5292
38	Elena Rybakina	2202
39	Coyote vs. Acme	2825
40	Neem Karoli Baba	820
41	Widow's Bay	465
42	Alexander Zverev	2883
43	Ella Beatty	64
44	List of S&P 500 companies	1199
45	Theo James	826
46	Primetime (film)	670
```

Follow-up repair (same session): rank 42's resume cache held only the newest 1,000 of
2,883 revisions (tail batches lost — see integrity notes). Re-pulled 2026-10-06T21:31:46Z,
counted 2,883, verified 2,883 lines on disk before recording. Script:
workers/rev-puller-00/repull-42.sh.

## First pass (worker 00, pull.sh): per-article revision counts

10 articles, recorded 31,375 revisions. Ranks 1, 4, 5 were re-pulled in the resume pass
(their cache files were absent at resume start — see integrity notes); ranks
6, 8, 9, 10, 11, 12, 13 carry through to the grand total. Rank 6's recorded count was
corrected 22251 -> 17751 (see integrity notes).

```
1	Main Page	80		(superseded by resume: 80)
4	Lizzie Borden	1001	(superseded by resume: 1002 — picked up a 2026-10-06T20:59:53Z edit)
5	Killing of the Clancy children	847	(superseded by resume: 847)
6	Deaths in 2026	17751	(corrected; recorded 22251 was an overcount)
8	.xxx	206
9	Christa Pike	857
10	Elizabeth Holmes	1860
11	Hanuman Ansh	764
12	September 11 attacks	3379
13	.xyz	130
```

## Data-integrity notes (all found and repaired this session)

1. **Ranks 1, 4, 5 cache files absent at resume start (OBSERVED).** First-pass
   progress.log records DONE for all three (20:45–20:47Z), but 1.jsonl/4.jsonl/5.jsonl
   did not exist on disk at 2026-10-06T21:04:14Z while 6.jsonl and 8–13.jsonl (written
   later) were present. Re-pulled all three cleanly in the resume pass; formats verified.
   Cause undetermined — consistent with the storage-layer flakiness behind the original
   runtime infra error. No data lost: all three now complete.
2. **Rank 14 partial cache (OBSERVED).** 500 lines (one batch), last ts 2026-09-17 —
   worker died mid-pull. Re-pulled from scratch: 1,130 revisions, complete.
3. **Rank 6 overcount, data intact (OBSERVED).** First pass recorded 22,251 but disk held
   17,751 lines. Verified complete: 17,751 unique revids, zero parentid-chain breaks,
   oldest revision in file (1327919853, 2025-12-16T21:50:03Z) == article's true oldest
   revision per live API check. The 22,251 was a worker-side counting overcount
   (+4,500 = 9 batches); the cached data is the ground truth. per-article.txt corrected.
4. **Rank 42 truncated cache (OBSERVED, repaired).** Resume pass counted 2,883 and logged
   DONE, but only 1,000 lines persisted (and its per-article.txt line was lost entirely —
   a silent write failure). Live API check: article's oldest revision is 2013-06-23,
   file's oldest was 2024-06-05 → genuinely incomplete. Re-pulled: 2,883 counted ==
   2,883 on disk, verified before recording.
5. **Final cross-check (OBSERVED).** All 42 `<rank>.jsonl` files: exist, non-empty,
   first-line "article" == chunk title, line count == per-article.txt count.
   Grand total 91,180 verified by direct line count on disk.

## Errors

None. errors.log is empty — no HTTP failures, no API errors, no retries needed in
either pass. Pace held at <=1 request per 5s to en.wikipedia.org throughout
(User-Agent: silent-locus-top500-scan/1.0 (research); HTTP via curl only).
