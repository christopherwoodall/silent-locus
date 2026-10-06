# rev-puller-07 — FINDINGS

Worker: REVISION-PULLER-07R (resume replacement for a failed worker)
Chunk: `raw/chunks/chunk-07` — ranks 296–339, 42 articles (ranks 301, 322 absent from chunk)
Branch: wikipedia-top500-infra-scan-2026-10-06 (no commits/pushes made by worker)

## Resume pass — 2026-10-06

The prior puller died from a runtime infra error mid-chunk. Resume scan found 35 of 42
articles already cached with first-line `"article"` matching the chunk title (incl.
ranks 296–298, which appeared on disk between the initial missing-list check and the
resume run — verified as legit via the article-match skip rule, NOT re-pulled).

### Articles completed this pass (7 pulled fresh)

| rank | article | revisions pulled |
|------|---------|------------------|
| 299 | Project Hail Mary (film) | 2,356 |
| 300 | Celine Dion | 1,275 |
| 302 | 2026 US Open – Women's singles | 651 |
| 303 | Kenneth Walker III | 604 |
| 304 | Katie Taylor | 984 |
| 305 | Florence Pugh | 1,786 |
| 306 | Steve Jobs | 1,162 |

Total revisions this pass: **8,818**. Failures: **0**. Wall time: ~4.7 min.
API window: rvstart=2026-10-07T00:00:00Z, rvend=2020-01-01T00:00:00Z, rvlimit=500,
rvdir=older, formatversion=2. Pacing: ≥5s between requests, UA
`silent-locus-top500-scan/1.0 (research)`, curl only (python3 for encoding/JSON only).

### Data-quality incident — rank 299 (resolved)

`raw/revisions/299.jsonl` came out with 2,846 lines vs 2,356 counted revisions: the
dead worker's process was still alive concurrently and wrote into the same file while
the resume script ran (both opened `"w"`, producing interleaved duplicate passes),
plus one edit summary containing a literal newline that broke strict JSONL. Fixed by
re-pulling 299 in a single clean pass after confirming the ghost process was gone:
2,356 lines, all unique revids, all parse, timestamp range 2026-10-06T13:55:05Z ..
2020-03-29T20:11:51Z. Also normalized embedded newlines in `comment` fields in ranks
304 (1) and 305 (2) so every line is one parseable JSON object; all other files
re-validated (line counts match, revids unique, first-line article matches).

### Grand totals for chunk-07

- 42/42 articles cached in `raw/revisions/<rank>.jsonl`
- 0 failures (`errors.log` empty — 0 bytes)
- Schema per line: rank, article, revid, parentid, user, timestamp, comment, tags, size

No infra anomalies observed this pass beyond the 299 ghost-write incident above.
