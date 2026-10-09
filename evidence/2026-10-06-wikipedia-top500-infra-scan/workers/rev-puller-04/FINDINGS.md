# REVISION-PULLER-04 — chunk-04 findings

Worker: REVISION-PULLER-04R (resume of the failed 04 worker).
Branch: `wikipedia-top500-infra-scan-2026-10-06`. No commits/pushes from this worker.
Method: MediaWiki `action=query&prop=revisions`, `rvprop=user|timestamp|ids|comment|tags|size`,
`rvlimit=500`, `rvdir=older`, window `2020-01-01T00:00:00Z` → `2026-10-07T00:00:00Z`,
`rvcontinue` followed to exhaustion. curl only; python3 for encoding/JSON.
Pace: ≥5s between requests to en.wikipedia.org. UA: `silent-locus-top500-scan/1.0 (research)`.

## Resume pass (2026-10-06, ~19 min wall)

Chunk-04 has 41 articles (ranks 174–200, 203–216; ranks 201/202 absent from chunk).
The previous worker had cached ranks 179–193 (15 articles) with correct first-line
`article` fields — all skipped. 26 articles pulled fresh this pass; **0 failures**.

### Articles pulled this pass (26), revision counts 2020-01-01 → present

| rank | article | revisions |
|------|---------|-----------|
| 174 | Constance Fisher | 77 |
| 175 | Ryan Garcia | 1,643 |
| 176 | Sitee | 22 |
| 177 | Andy Burnham | 2,326 |
| 178 | Mariska Hargitay | 1,072 |
| 194 | Jeffrey Dahmer | 1,936 |
| 195 | Elizabeth II | 5,048 |
| 196 | Charles Spencer, 9th Earl Spencer | 442 |
| 197 | 2026 Formula One World Championship | 1,798 |
| 198 | Ella Langley | 955 |
| 199 | Benjamin Netanyahu | 1,541 |
| 200 | Resident Evil | 1,293 |
| 203 | Ruth Kearney | 148 |
| 204 | Tom Pelphrey | 269 |
| 205 | Google | 1,750 |
| 206 | Elon Musk | 11,528 |
| 207 | Madonna | 2,689 |
| 208 | Maria Sten | 99 |
| 209 | American Horror Story | 1,971 |
| 210 | Elizabeth Báthory | 1,069 |
| 211 | American Horror Story: 13 | 392 |
| 212 | DC (film) | 525 |
| 213 | Haiwaan (film) | 410 |
| 214 | Zach Cregger | 390 |
| 215 | Artificial intelligence | 3,660 |
| 216 | United Kingdom | 5,033 |

Resume-pass total: **48,086 revisions** across 26 articles. Failures: 0.
`errors.log` is empty (created, no entries).

### Grand totals (chunk-04, all 41 articles)

- Articles: 41 (15 pre-cached + 26 resume-pulled)
- Revisions: **69,224**
- Verification: every `raw/revisions/<rank>.jsonl` exists, non-empty, first line
  `article` matches the chunk title, and every line's `rank` matches the filename.

### Notes

- Largest histories in this chunk: Elon Musk (11,528), Elizabeth II (5,048),
  United Kingdom (5,033), Artificial intelligence (3,660), Madonna (2,689).
- One record to note for downstream infra analysis: 174.jsonl, 175.jsonl,
  176.jsonl, 177.jsonl existed in the previous commit but were *deleted* from
  the working tree before this resume (git shows `D`); they were re-pulled
  from scratch this pass. No data loss — fresh pulls verify against chunk titles.
- Schema per line: `{"rank", "article", "revid", "parentid", "user", "timestamp",
  "comment", "tags", "size"}`.
