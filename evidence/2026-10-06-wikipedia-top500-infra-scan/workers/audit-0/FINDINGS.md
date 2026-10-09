# AUDIT-WORKER-0 findings — 2026-10-06 Wikipedia top-500 infra scan

**Worker:** audit-0 | **Chunk:** `raw/audit-chunks/audit-0.tsv` (122 articles, ranks 1–128 with gaps) | **Date:** 2026-10-06
**Method:** (a) local JSONL check — every line valid JSON, `rank`/`article` fields match, timestamps non-increasing;
(b) API ground truth — oldest in-window revision via `rvstart=2020-01-01T00:00:00Z`, compared to file minimum timestamp (BROKEN if file empty but API returns revisions; TRUNCATED if file min_ts > 1 day newer than API oldest).
**Pacing:** ≤1 request / 5 s to en.wikipedia.org, User-Agent `silent-locus-top500-scan/1.0 (research)`, curl only.

## Summary

- **Verified OK:** 121 / 122
- **Repaired:** 1 / 122
- **Still broken:** 0
- **Total API calls:** 128 (122 ground-truth + 6 repair pulls)

## Repaired

### rank 57 — Sydney Sweeney — REPAIRED (BROKEN)
- **Before:** `raw/revisions/57.jsonl` existed but was 0 bytes (EMPTY local verdict).
- **Ground truth:** API oldest in-window revision `2020-01-06T01:24:03Z` (revid in response) — file empty ⇒ BROKEN.
- **Repair:** full re-pull (`rvprop=user|timestamp|ids|comment|tags|size`, `rvlimit=500`, `rvdir=older`, `rvstart=2026-10-07T00:00:00Z`, `rvend=2020-01-01T00:00:00Z`, rvcontinue to exhaustion; 6 paged calls), written via temp file + fsync + atomic rename.
- **After:** 2,957 lines; all lines valid JSON with `rank=57`, `article="Sydney Sweeney"`; timestamps strictly non-increasing; range `2026-10-06T15:46:20Z` → `2020-01-06T01:24:03Z` (min_ts exactly matches API ground truth).
- **Verdict after repair:** OK.

## Verified OK (121)

All remaining 121 articles passed both checks: valid JSONL, field match, non-increasing timestamps, and file minimum timestamp within 1 day of the API's oldest in-window revision. Ranks: 1, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 72, 73, 74, 75, 76, 77, 78, 79, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128.

Note: rank 433 (two files: `433.jsonl`, `433_barry_melrose.jsonl`) is not in this chunk — no action taken.

## Notes
- No TRUNCATED files found in this quarter: no file's minimum timestamp was >1 day newer than the API ground truth.
- No commits/pushes made; no branch switches. FINDINGS.md only.
