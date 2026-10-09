# LINGUIST checkpoint — wikipedia-edit-hunt lane
Branch: wikipedia-edit-hunt-2026-10-06. Updated: 2026-10-06 ~18:45 UTC.

## Status
- revisions.tsv: COMPLETE for analysis (54 rows; 49 populated + 5 meta Web2Cit rows empty, oldids nonexistent — already flagged upstream).
- Edit-comment analysis: COMPLETE (49 comments; 1 empty).
- Diff collection: IN PROGRESS (revision-enumerator, ~16 of ~49 diffs as of 18:44 UTC; en + test wikis first). Diff-content analysis partial; rerun extractor when collection finishes.
- Web2Cit JSON content: BLOCKED — oldids 30732696–30732700 nonexistent (upstream integrity flag); pages deleted 2026-10-06 01:39–01:40 UTC by 'Pppery'. Cannot compare hand-written vs generated JSON. Stays a documented gap.

## Interim findings (see FINDINGS.md for detail)
1. Comments are all functional test tokens: "test" x17, "sandbox test" x6, "sandbox" x3, plus link-test variants and one templated machine summary.
2. "Temporary technical sandbox initialization" (x7, identical, commons+incubator+meta, all ~2026-* accounts) = agent template string, NOT a MediaWiki default.
3. Sandbox content is link/citation tests against statistics-agency endpoints (hagstofa.is PxWeb, site-test.nsi.bg) — same data-retrieval intent as Web2Cit ArcGIS/Hawaii geodata ops.
4. Empty comment x1 (en 1353492663, ~2026-28217-20); Bulgarian localized "тест" x1 (bg 12923296).

## Next steps
- Poll diffs/; rerun extract_all.sh when count stabilizes at expected total (~49; check _diff_list.txt / oldids.txt).
- Cross-wiki byte-similarity check (test vs en vs test2 vs mediawiki sandbox content).
- Unicode quirk scan (zero-width, smart quotes, trailing whitespace) on extracted added-lines.
