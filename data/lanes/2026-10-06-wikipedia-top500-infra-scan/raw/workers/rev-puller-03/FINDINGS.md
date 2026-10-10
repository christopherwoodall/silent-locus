# rev-puller-03 FINDINGS

**Chunk:** `data/2026-10-06-wikipedia-top500-infra-scan/raw/chunks/chunk-03` (ranks 132-173)
**Method:** MediaWiki revisions API, `rvlimit=500`, `rvdir=older`, window 2020-01-01 -> 2026-10-07T00:00:00Z,
`rvprop=user|timestamp|ids|comment|tags|size`; paginated on `continue.rvcontinue` until exhausted.
HTTP via curl only (UA `silent-locus-top500-scan/1.0 (research)`), <=1 req/5s. python3 used only for
URL-encoding and JSON parsing. Script: `workers/rev-puller-03/pull.sh`.
One extra field beyond the spec: `temp` (boolean) flags Wikipedia temporary-account revisions
(`~2026-…` usernames; relevant to the temp-account clustering hunt lane).

**Coverage:** 42/42 articles complete, 0 failures, errors.log empty.
**Total:** 48,559 revisions across 117 API pages.
**Temp-account revisions:** 1,984 of 48,559.
**Wall time:** ~30 min total (run 1: 17 articles, then exec session reaped mid-chunk; run 2 resumed
ranks 149-173 and completed — no data loss; all 42 files validated: schema exact, counts match counts.tsv,
timestamps within window).

| rank | article | pages | revisions | temp-acct revs |
|---:|---|---:|---:|---:|
| 132 | Sex | 1 | 249 | 13 |
| 133 | Mohamed Atta | 3 | 1,147 | 57 |
| 134 | World Trade Center (1973–2001) | 2 | 875 | 0 |
| 135 | Arch Manning | 2 | 807 | 35 |
| 136 | XXX | 1 | 33 | 0 |
| 137 | Chad Gilbert | 1 | 216 | 19 |
| 138 | Tim Curry | 4 | 1,587 | 116 |
| 139 | Avengers: Doomsday | 6 | 2,552 | 0 |
| 140 | Katseye | 4 | 1,988 | 13 |
| 141 | Alternative for Germany | 5 | 2,344 | 0 |
| 142 | Cristiano Ronaldo | 10 | 4,887 | 0 |
| 143 | Vicky Krieps | 1 | 296 | 2 |
| 144 | Reacher (TV series) | 3 | 1,406 | 37 |
| 145 | Charlie Hunnam | 2 | 661 | 37 |
| 146 | 2026 Saxony-Anhalt state election | 2 | 675 | 71 |
| 147 | Mayday (2026 film) | 1 | 219 | 25 |
| 148 | Hijackers in the September 11 attacks | 2 | 768 | 45 |
| 149 | Tom Bateman (actor) | 1 | 200 | 15 |
| 150 | XNXX | 1 | 434 | 37 |
| 151 | Guy Ritchie | 2 | 796 | 26 |
| 152 | Mamitha Baiju | 3 | 1,382 | 103 |
| 153 | Hope (2026 film) | 1 | 331 | 59 |
| 154 | Annette Bening | 1 | 279 | 12 |
| 155 | Ed Gein | 3 | 1,231 | 14 |
| 156 | Irumudi | 1 | 252 | 88 |
| 157 | John Ternus | 1 | 468 | 96 |
| 158 | 2026 in film | 6 | 2,930 | 671 |
| 159 | 2026 United States elections | 2 | 956 | 159 |
| 160 | Casualties of the September 11 attacks | 3 | 1,156 | 0 |
| 161 | Austin Abrams | 1 | 295 | 12 |
| 162 | Tom Cruise | 3 | 1,091 | 0 |
| 163 | Roblox | 3 | 1,388 | 0 |
| 164 | World War II | 6 | 2,984 | 0 |
| 165 | MobLand | 2 | 528 | 10 |
| 166 | Warren Beatty | 2 | 603 | 4 |
| 167 | Tom Holland | 5 | 2,272 | 0 |
| 168 | Nicole Kidman | 5 | 2,072 | 41 |
| 169 | American Airlines Flight 11 | 3 | 1,230 | 33 |
| 170 | Riley Green | 2 | 623 | 8 |
| 171 | Kaley Cuoco | 1 | 410 | 0 |
| 172 | UFC 331 | 1 | 238 | 61 |
| 173 | Opinion polling for the next United Kingdom general election | 8 | 3,700 | 65 |

## Failures

None. `workers/rev-puller-03/errors.log` is empty; no missing pages, no API errors.

## Notes

- Rank 136 `XXX`: only 33 revisions in window (low edit volume).
- Rank 146 `2026 Saxony-Anhalt state election` and 147 `Mayday (2026 film)`: youngest articles; history starts 2022/2023.
- All timestamps fall within 2020-01-01 .. 2026-10-07; pagination exhausted per article (no rvcontinue at end).
