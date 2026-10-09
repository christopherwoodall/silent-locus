# FINDINGS — wiki-surgeon-2 (independent verifier, wikipedia lane)
Branch: `wikipedia-edit-hunt-2026-10-06`. Verdict target: revisions.tsv (54 rows) + diffs/ + the "54 rows" count claim.

## 1. Independent CSV re-parse (DONE)
- My parse (sed/grep, independent of enumerator's tooling): 54 (wiki,oldid) pairs.
- Sorted-pair diff vs revisions.tsv: EMPTY — exact match. No missed rows, no duplicates, no wiki misassignments.
- oldids.txt also matches my parse byte-for-byte.
- Tricky URL forms all parsed correctly by the enumerator: `?diff=1213513506` (commons, no title), `?diff=1213399057` (commons), `?diff=12923296` (bg), `&oldid=30xxxxxx` Web2Cit meta URLs (no diff=), `title=User_talk:Example/sandbox` (underscore -> table has "User talk:..." with space, correct per API convention).
- OBSERVED: CSV has NO header row, NO blank lines, NO duplicate (wiki,oldid) pairs. `wc -l`=53 because the final line lacks a trailing newline — row count is still 54.

## 2. "54 rows" count claim (DONE -> VERIFIED)
- CSV: 54 non-empty lines. TSV: 55 wc-lines = 1 header + 54 data rows. oldids.txt: 54 lines. Consistent.

## 3. Diff-file sha256 spot check (5 files, DONE -> EXPECTED MISMATCH, not a table error)
- 5/5 diff files' sha256 != content_sha256 column.
- REASON (OBSERVED): diff files are `action=compare` API JSON responses (parent->revision HTML diffs) with a provenance header line, NOT revision content. content_sha256 = sha256 of raw revision content (slot main). PROOF: sha256("hello test") == table value 25ed9241... for en/1353490694.
- Conclusion: the spot check as specified tests the wrong object. The column's true verification is sha256(independently pulled content) — running now via API re-pull.

## 4. API field re-verification (DONE -> VERIFIED, zero mismatches)
- pull_api.sh: 9 wiki calls, 6s pacing, all HTTP 200, rvprop=ids|timestamp|user|comment|tags|content, formatversion=2.
- Sample: 17 oldids across ALL 9 wikis in the CSV (en 1353490694,1356419247; test 741406,744268; test2 612931,613856; mediawiki 8370989; commons 1213513506,1238390511; simple 10891416; incubator 7226107,7226111; meta 30732655 + 3 missing; bg 12923296).
- compare.py: 14 resolved rows checked field-by-field (page, user, timestamp_utc, comment, tags, minor, parent_oldid, content_sha256, content_bytes) -> NO FIELD MISMATCHES.
- OBSERVED: content_sha256 = sha256(utf-8 bytes of revision content); content_bytes = utf-8 byte length. Both verified against independent pulls.

## 5. "Failed to resolve" claims (DONE -> all 5 VERIFIED as genuinely missing)
- meta.wikimedia.org 30732691, 30732696, 30732700, 30732698, 30732699: independent API re-query returns `badrevids` with `"missing": true` for each. These are genuinely absent revision IDs (not API errors — transport was healthy, HTTP 200, sibling revid 30732655 resolved in the same call). The enumerator's empty-field rows are correct.
- INFERENCE: the Web2Cit meta URLs in the WMF CSV carry oldids that do not exist as revisions on meta.wikimedia.org (stale/deleted/fabricated upstream; out of my lane to adjudicate which).

## 6. Diff-file internal consistency (5 sampled -> 4 OK, 1 DISCREPANCY in diffs/, not in the TSV)
- For 4/5 sampled diff files: JSON `torevid` == filename oldid and `fromrevid` == table parent_oldid. OK.
- DISCREPANCY: `diffs/test.wikipedia.org_741406.txt` is NOT a diff — it is an API error response (`invalidparammix`: "fromslots and fromtext can not be used together"). The enumerator's collect_diffs.sh saved the error JSON as a successful diff and collection.log falsely logged "OK test.wikipedia.org 741406 diff". Root cause: the enumerator used `fromtext=&fromslots=main` together (for 741406, which has no parent_oldid in the table). Fix: retry with fromtext alone (no fromslots), or fromrev=0. NOTE: diff collection was still in progress at verification time (37/49 files); only 1 of the 37 present files has this error.

## VERDICT: revisions.tsv VERIFIED (with one adjacent discrepancy in diffs/)

**revisions.tsv — VERIFIED.** Independent re-parse of the WMF CSV yields 54 (wiki,oldid) pairs; sorted diff vs the table is empty. Count claim holds (54 rows, no header, no blanks, no dupes; `wc -l`=53 is a missing trailing newline, not missing data). 17 oldids / 9 wikis re-pulled independently via MediaWiki API (curl, 6s pacing, all HTTP 200): all 14 resolved rows match the table field-by-field (page, user, timestamp_utc, comment, tags, minor, parent_oldid, content_sha256, content_bytes) with zero mismatches. All 5 "missing" meta Web2Cit oldids independently confirmed missing via API `badrevids` (genuine absence, not transport error). content_sha256 semantics confirmed: sha256 of raw revision content bytes (proven by reproduction).

**diffs/ — one DISCREPANCY (adjacent, not in the TSV):** `diffs/test.wikipedia.org_741406.txt` is an API error response (`invalidparammix`), saved by the enumerator as a successful diff and falsely logged "OK" in collection.log. Retry needed with corrected compare params (drop `fromslots` when using `fromtext`). 4/5 other sampled diff files are internally consistent (torevid/fromrevid match filename/table). The "diff files' sha256 vs content_sha256" spot check as specified tests the wrong object: diff files are compare-API JSON, the column hashes revision content — expected mismatch, not a table error.

**Coordinator action items:** (1) retry diff for test.wikipedia.org 741406; (2) diff collection was still running (37/49) at verification time — re-run this spot check when complete; (3) the 5 missing meta Web2Cit oldids are genuinely absent upstream — flag to whoever owns the WMF-CSV provenance question.
