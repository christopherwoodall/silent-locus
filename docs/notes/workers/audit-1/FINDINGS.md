# AUDIT-WORKER-1 findings — Wikipedia top-500 infra scan, chunk audit-1

- **Chunk:** `data/2026-10-06-wikipedia-top500-infra-scan/raw/audit-chunks/audit-1.tsv` (ranks 129–252, 122 articles; rank 433 note N/A — not in this chunk)
- **Audited:** 2026-10-06 ~22:00–22:20 UTC (17:00–17:20 CDT)
- **Branch:** `wikipedia-top500-infra-scan-2026-10-06` — no commits, no pushes, no branch switches (read-only except repair of `raw/revisions/193.jsonl`)

## Method

1. **Local check** (no network): every line of `raw/revisions/<rank>.jsonl` parsed as JSON; `article` == TSV title, `rank` == rank, timestamps non-increasing; recorded line count, min/max timestamp.
2. **API ground truth**: per article, one call to `en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=<url-encoded>&rvlimit=1&rvdir=newer&rvstart=2020-01-01T00:00:00Z&rvprop=ids|timestamp&format=json&formatversion=2` (oldest in-window revision). Compared file min timestamp: empty file + API revision = BROKEN; file min > API oldest by >1 day = TRUNCATED. Pace: 1 request / 5 s, UA `silent-locus-top500-scan/1.0 (research)`, curl only.
3. **Repair**: full re-pull (`rvprop=user|timestamp|ids|parentid|comment|tags|size`, rvlimit=500, rvdir=older, rvstart=2026-10-07T00:00:00Z, rvend=2020-01-01T00:00:00Z, rvcontinue to exhaustion), temp file + fsync + atomic rename, then re-verified.

## Totals

| Verdict | Count |
|---|---|
| OK (local + API agree) | 120 |
| Empty-but-consistent (rank 222, see note) | 1 |
| TRUNCATED → **REPAIRED** | 1 |
| BROKEN | 0 |
| API failures | 0 |

**Total API calls:** 129 (122 ground-truth + 1 redirect-info + 6 repair pages).

## Repairs

- **Rank 193 — Hasan Piker**: file held exactly 500 revisions, min `2026-03-24T13:19:14Z` — classic first-page-only truncation (~5.7 years of history missing). Re-pulled in full: **500 → 2,743 revisions**, new min `2020-07-12T02:53:36Z` == API oldest exactly, max `2026-10-06T16:14:53Z`, order + schema re-verified OK (6 API pages, atomic rename).

## Caveat for the scan (not a cache defect)

- **Rank 222 — "european election 2014"**: cached file is correctly EMPTY — the API ground-truth query (titles as given, no `redirects=1`) returns no in-window revisions for the redirect page itself. One extra API call confirmed `european election 2014` is a redirect to **2014 European Parliament election** (a real, heavily-edited article). If the scan intends to cover the target article, the TSV title needs changing at the range-curation level; as cached, the file is faithful to the pull query and is marked OK-with-note, not BROKEN.

## Per-article verdicts

| rank | article | lines | verdict | note |
|---|---|---|---|---|
| 129 | Lady Gaga | 3631 | OK |  |
| 130 | Furious (TV series) | 183 | OK |  |
| 131 | Zohran Mamdani | 4198 | OK |  |
| 132 | Sex | 249 | OK |  |
| 133 | Mohamed Atta | 1147 | OK |  |
| 134 | World Trade Center (1973–2001) | 875 | OK |  |
| 135 | Arch Manning | 807 | OK |  |
| 136 | XXX | 33 | OK |  |
| 137 | Chad Gilbert | 216 | OK |  |
| 138 | Tim Curry | 1587 | OK |  |
| 139 | Avengers: Doomsday | 2552 | OK |  |
| 140 | Katseye | 1988 | OK |  |
| 141 | Alternative for Germany | 2344 | OK |  |
| 142 | Cristiano Ronaldo | 4887 | OK |  |
| 143 | Vicky Krieps | 296 | OK |  |
| 144 | Reacher (TV series) | 1406 | OK |  |
| 145 | Charlie Hunnam | 661 | OK |  |
| 146 | 2026 Saxony-Anhalt state election | 675 | OK |  |
| 147 | Mayday (2026 film) | 219 | OK |  |
| 148 | Hijackers in the September 11 attacks | 768 | OK |  |
| 149 | Tom Bateman (actor) | 200 | OK |  |
| 150 | XNXX | 434 | OK |  |
| 151 | Guy Ritchie | 796 | OK |  |
| 152 | Mamitha Baiju | 1382 | OK |  |
| 153 | Hope (2026 film) | 331 | OK |  |
| 154 | Annette Bening | 279 | OK |  |
| 155 | Ed Gein | 1231 | OK |  |
| 156 | Irumudi | 252 | OK |  |
| 157 | John Ternus | 468 | OK |  |
| 158 | 2026 in film | 2930 | OK |  |
| 159 | 2026 United States elections | 956 | OK |  |
| 160 | Casualties of the September 11 attacks | 1156 | OK |  |
| 161 | Austin Abrams | 295 | OK |  |
| 162 | Tom Cruise | 1091 | OK |  |
| 163 | Roblox | 1388 | OK |  |
| 164 | World War II | 2984 | OK |  |
| 165 | MobLand | 528 | OK |  |
| 166 | Warren Beatty | 603 | OK |  |
| 167 | Tom Holland | 2272 | OK |  |
| 168 | Nicole Kidman | 2072 | OK |  |
| 169 | American Airlines Flight 11 | 1230 | OK |  |
| 170 | Riley Green | 623 | OK |  |
| 171 | Kaley Cuoco | 410 | OK |  |
| 172 | UFC 331 | 238 | OK |  |
| 173 | Opinion polling for the next United Kingdom general election | 3700 | OK |  |
| 174 | Constance Fisher | 77 | OK |  |
| 175 | Ryan Garcia | 1643 | OK |  |
| 176 | Sitee | 22 | OK |  |
| 177 | Andy Burnham | 2326 | OK |  |
| 178 | Mariska Hargitay | 1072 | OK |  |
| 179 | Houthis | 1268 | OK |  |
| 180 | Dario Amodei | 366 | OK |  |
| 181 | Theranos | 536 | OK |  |
| 182 | Death of Nolan Wells | 365 | OK |  |
| 183 | Resident Evil (film series) | 764 | OK |  |
| 184 | Lionel Messi | 6250 | OK |  |
| 185 | Lance Oppenheim | 187 | OK |  |
| 186 | XXXXX (album) | 51 | OK |  |
| 187 | Murder of Tupac Shakur | 697 | OK |  |
| 188 | Dorothy (film) | 240 | OK |  |
| 189 | Bryan Shelton | 94 | OK |  |
| 190 | JJ Gabriel | 167 | OK |  |
| 191 | Taylor Swift | 8626 | OK |  |
| 192 | James Talarico | 1027 | OK |  |
| 193 | Hasan Piker | 500 -> 2743 | TRUNCATED | truncated at 500 (1st page only); re-pulled, min_ts now matches API oldest exactly |
| 194 | Jeffrey Dahmer | 1936 | OK |  |
| 195 | Elizabeth II | 5048 | OK |  |
| 196 | Charles Spencer, 9th Earl Spencer | 442 | OK |  |
| 197 | 2026 Formula One World Championship | 1798 | OK |  |
| 198 | Ella Langley | 955 | OK |  |
| 199 | Benjamin Netanyahu | 1541 | OK |  |
| 200 | Resident Evil | 1293 | OK |  |
| 203 | Ruth Kearney | 148 | OK |  |
| 204 | Tom Pelphrey | 269 | OK |  |
| 205 | Google | 1750 | OK |  |
| 206 | Elon Musk | 11528 | OK |  |
| 207 | Madonna | 2689 | OK |  |
| 208 | Maria Sten | 99 | OK |  |
| 209 | American Horror Story | 1971 | OK |  |
| 210 | Elizabeth Báthory | 1069 | OK |  |
| 211 | American Horror Story: 13 | 392 | OK |  |
| 212 | DC (film) | 525 | OK |  |
| 213 | Haiwaan (film) | 410 | OK |  |
| 214 | Zach Cregger | 390 | OK |  |
| 215 | Artificial intelligence | 3660 | OK |  |
| 216 | United Kingdom | 5033 | OK |  |
| 217 | Anne Hathaway | 1653 | OK |  |
| 218 | Keri Russell | 556 | OK |  |
| 219 | Tupac Shakur | 2537 | OK |  |
| 220 | Jenna Dewan | 412 | OK |  |
| 221 | Alice Weidel | 721 | OK |  |
| 222 | european election 2014 | 0 | API_NO_REVISIONS | empty file; API (same query, no redirects) returns no in-window revisions -> consistent; title is a redirect to '2014 European Parliament election' |
| 223 | Bigg Boss (Tamil TV series) season 10 | 1104 | OK |  |
| 224 | List of highest-grossing Malayalam films | 3291 | OK |  |
| 225 | Miley Cyrus | 1112 | OK |  |
| 226 | Labor Day | 501 | OK |  |
| 227 | Nigella Lawson | 361 | OK |  |
| 228 | 2026 US Open – Men's singles | 1068 | OK |  |
| 229 | Stella Lefty | 422 | OK |  |
| 230 | Coco Gauff | 2162 | OK |  |
| 231 | Navier–Stokes equations | 483 | OK |  |
| 232 | Sarah Paulson | 487 | OK |  |
| 233 | Facebook | 1260 | OK |  |
| 234 | Andrea Yates | 290 | OK |  |
| 235 | Mitch McConnell | 1963 | OK |  |
| 236 | Z-Library | 1115 | OK |  |
| 237 | Anthony Bourdain | 986 | OK |  |
| 238 | The Uprising (2026 film) | 321 | OK |  |
| 239 | List of American films of 2026 | 4610 | OK |  |
| 240 | Adolf Hitler | 2019 | OK |  |
| 241 | Charles III | 5468 | OK |  |
| 242 | Abdul El-Sayed | 697 | OK |  |
| 243 | Sam Altman | 1684 | OK |  |
| 244 | Khalid Sheikh Mohammed | 728 | OK |  |
| 245 | Rebecca Hall | 417 | OK |  |
| 246 | Sylvester Stallone | 855 | OK |  |
| 247 | Nance O'Neil | 62 | OK |  |
| 248 | Verity (novel) | 141 | OK |  |
| 249 | Qazi Touqeer | 154 | OK |  |
| 250 | Diana, Princess of Wales | 1709 | OK |  |
| 251 | The Runner (2026 film) | 189 | OK |  |
| 252 | Robert Pattinson | 1497 | OK |  |

## Audit trail files (this directory)

- `local-check.tsv` — per-file local verification (json_ok, article/rank match, ordering, min/max ts, line counts)
- `api-check.tsv` — per-article API ground truth (api_oldest_ts vs file min_ts, verdict)
- `api-check.log` — full paced API run log
- `repair.log` — repair job record (before/after counts, timestamps, API pages)
- `repair-run.log` — repair run stdout
