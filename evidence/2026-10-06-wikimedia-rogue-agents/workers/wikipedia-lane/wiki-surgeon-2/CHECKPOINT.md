# CHECKPOINT — wiki-surgeon-2 (independent verifier, wikipedia lane)

Branch: `wikipedia-edit-hunt-2026-10-06` (checked out; commit at end, NO push).
Dir: `data/2026-10-06-wikimedia-rogue-agents/workers/wikipedia-lane/wiki-surgeon-2/`

## Status 2026-10-06 ~18:50Z (session start)
- Read `docs/methodology.md`. Worker dir created.
- Enumerator state: `revisions.tsv` = header + 54 data rows; `diffs/` growing (23 files at check, collection still running per collection.log); `records.json` = raw API responses (status field: ok/missing); 5 meta.wikimedia.org Web2Cit rows marked "missing" (empty fields in TSV).

## Completed
1. Independent CSV parse -> (wiki, oldid) pairs: PASS. 54 pairs from my parse == 54 rows in revisions.tsv, sorted-pair diff empty. oldids.txt also matches my parse exactly. No misses, no duplicates, no misassignments (incl. `?diff=`-only URLs on commons/bg, `&oldid=`-only Web2Cit meta URLs, `User_talk:` with underscore).
2. Row-count claim: CSV = 54 non-empty lines, NO header row, NO blank lines, NO duplicate (wiki,oldid) pairs. `wc -l` = 53 because the final line lacks a trailing newline (OBSERVED; not a data discrepancy).
3. content_sha256 semantics established: sha256 of raw revision content (slot main). OBSERVED: sha256("hello test") = 25ed9241... == TSV value for en/1353490694. Diff files are action=compare API JSON (not revision content) -> their sha256 will NOT match content_sha256 by construction; the real sha256 check is my own API pull vs the column.

## Completed (final, ~18:55Z)
1. Independent CSV parse -> (wiki, oldid) pairs: PASS. 54 pairs == 54 TSV rows, sorted diff empty. oldids.txt matches.
2. Row-count claim: VERIFIED. 54 non-empty lines, no header/blanks/dupes; wc -l=53 is missing trailing newline.
3. content_sha256 semantics: sha256 of raw revision content (proven by reproduction).
4. API re-pull: 9 calls, 6s pacing, all HTTP 200. 17 oldids / 9 wikis. compare.py: 14 resolved rows, NO field mismatches.
5. "Missing" claims: all 5 meta Web2Cit oldids independently confirmed missing (API badrevids, missing=true).
6. Diff-file spot check: 5/5 sha256 != content_sha256 (expected by construction — compare JSON vs content). Internal consistency: 4/5 OK; DISCREPANCY: diffs/test.wikipedia.org_741406.txt is an API error response (invalidparammix) saved as success, falsely logged "OK" in collection.log. Diff collection still running (37/49) at check time.

## Verdict
revisions.tsv VERIFIED. One adjacent discrepancy in diffs/ (741406 error file). FINDINGS.md final. Ready to commit; NO push per instructions.

## Artifacts (this dir)
- FINDINGS.md (final), CHECKPOINT.md, pull_api.sh, compare.py, api_raw/ (9 raw API JSON responses + pull.log)
