# TRACK 2 — Evidence & Provenance Audit
Lane: `wikipedia-edit-hunt-2026-10-06` (closed). Auditor: track-2 subagent, 2026-10-07 ~07:35–08:00 CDT.
Scope: `wikipedia-lane/` read-only; `revhistory-grep/` excluded (in-flight separate job).

## 1. WMF evidence CSV hash — PASS
`data/2026-10-06-wikimedia-rogue-agents/raw/openai-wikimedia-edits-2026-10-04.csv` recomputed with sha256sum:
`300511bb7b90a7b2a5bfae4c7d80061b16617f16e4242204cb5c264cc32cc9c6` — matches expected exactly.
Note: the cached copy lives at the event level (`.../raw/`), not in `wikipedia-lane/raw/`; the lane treats it as the seed. Also note the CSV uses CRLF line endings — consistent with the lane's documented transport failure (`oldids.txt` carried `\r`; stripped and re-ran).

## 2. PROVENANCE.md hash inventory — PASS for the batch phase, gaps elsewhere
- `raw/PROVENANCE.md` revision-enumerator section lists sha256 for all 113 files (9 batch revisions.json, 54 api-dumps, 49 diffs, revisions.tsv). All 113 recomputed hashes MATCH. 0 missing files.
- Retrieval timestamps, endpoints, query params, and UA documented; the 741406 invalidparammix correction is logged honestly.
- GAPS:
  - PROVENANCE.md account-profiler section: "Row counts and sha256 (FINAL — fill at pull completion)" is still `(pending)` — never filled. The 28 globaluserinfo, 7 registration, contribs, locklog, blocklog, and accounts.tsv files have no hash inventory.
  - `raw/NEWUSERS-PROVENANCE.md` (six-month newusers pull, 24 canonical files + 7-wiki combined files): documents method, UA (`silent-locus-research/1.0`), pacing, dedupe quirks, and the redundant-fragment exclusion — but carries NO sha256 for any newusers file, and `.newusers-pull-state` has no hashes either. Largest unhashed files (~100MB each, ~1.4GB total) are the least recoverable if corrupted.
  - Sweep subdirs (`ngram-sweep/`, `vocab-sweep/`, `wordlist-wiki-sweep/`, `burst-analysis/`) have `raw/` subdirs with captures but no per-file provenance notes (no source URL / retrieval time / sha256); only scripts + FINDINGS.md.

## 3. Link check — 8/8 resolve with claimed content (curl, research UA, 2026-10-07)
| URL | HTTP | Content confirmed |
|---|---|---|
| https://incubator.wikimedia.org/w/index.php?diff=7226103 | 200 | YES — `<!-- Lifeval temporary technical sandbox initialization -->` |
| https://incubator.wikimedia.org/w/index.php?diff=7226104 | 200 | YES — marker present |
| https://incubator.wikimedia.org/w/index.php?diff=7226105 | 200 | YES — marker present |
| https://incubator.wikimedia.org/w/index.php?diff=7226108 | 200 | YES — marker present |
| https://incubator.wikimedia.org/w/index.php?diff=7226111 | 200 | YES — marker present |
| https://meta.wikimedia.org/w/index.php?diff=30732655 | 200 | YES — `<!-- Lifeval API temp-account test -->` |
| https://commons.wikimedia.org/w/index.php?diff=1238390511 | 200 | YES — Lifeval marker present |
| https://www.mediawiki.org/w/index.php?diff=8370994 | 200 | YES — revision content present (M3 volley; checked for the temp-account revision content) |

## 4. Meta oldid verification — lane's correction CONFIRMED
Via Meta API (`action=query&prop=revisions`, 2026-10-07):
- 30732691, 30732696, 30732698, 30732699, 30732700: all return `badrevids` — **no such revision**. Claimed-nonexistent set verified.
- 30732697: EXISTS — `User:Der-Wir-Ing` user page, by Der-Wir-Ing, 2026-06-25T20:31:43Z, empty comment. Unrelated to the incident; the lane's correction stands.

## 5. records.json vs CSV diff-ID coverage — PASS
CSV has 54 diff URLs (51 `oldid=<id>` form + 3 `diff=<id>` form: 1213513506, 1213399057, 12923296 — the bare `diff=` lines are what the earlier `oldids.txt` CRLF issue touched). `records.json` is a 54-row list; every CSV ID is present in `records.json` (index [1] of each row); no extras, no missing. Count spot-check: 54 == 54.

## 6. Redaction scan — PASS (no violations)
Grepped the whole lane tree (excluding revhistory-grep) for `REDACTED` and for the bracket form `[REDACTED...]`: zero bracket-form placeholders anywhere. Bare "REDACTED" hits in `wordlist-wiki-sweep/` are real on-wiki page titles from API search snippets (e.g. `File:HOUSE OVERSIGHT 000460 REDACTED EMAIL.jpg`), not evidence redactions. Standing rule held: nothing redacted from evidence.

## Summary
- PASS: CSV hash, all 113 provenance hashes, all 8 diff links live with claimed content, oldid nonexistent-set + 30732697 correction, records.json 54/54 coverage, zero redactions.
- GAPS (provenance completeness, not integrity): unfilled `(pending)` sha256 block in PROVENANCE.md account-profiler section; no hashes for any newusers jsonl file; sweep-subdir captures lack provenance notes.
- Open question for parent: whether to require backfilling sha256 for the newusers files (~1.4GB, cheap to compute) before the lane is considered fully closed.
