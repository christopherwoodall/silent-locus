# COUNSEL (a) — METHODOLOGY — monitorable-surfaces v2 build (2026-10-23)

Reviewed artifacts: the v2 workbook, work-v2/DELTA.md, work-v2/GAPFILL.md, Notes rows 104-113,
plus an independent machine re-check of the Oct-22 file, the operator file
(Monitorable_Surfaces_0_aff3.xlsx), and all 7 gap-fill evidence paths on disk.

## Q1. Is the enrichment method sound? (diff-then-carry-over, restore-one-regression, schema-exact gap-fill, append-only columns)

**Verdict: APPROVE.** The diff justified the shortcut: I independently re-ran the Oct-22 vs
operator-file comparison and got the same result (89 rows changed in exactly one field,
Operations & Artifacts, and only by un-escaping `$\rightarrow$` to `->`; 1 regression row;
0 added, 0 removed). Carry-over was therefore near-free: the operator copy already held the
Oct-22 enrichment everywhere else. The regression restore on agents-agents-agents.com is
byte-for-byte against Oct-22 (Sources, Direct Links, Seen, MITRE all match). Gap-fill rows
are schema-exact (5 POI rows to cols B-M, 2 Intel rows to the sheet's own header, typo
"Calssification" deliberately kept). New columns N-R are append-only: I verified B-M/B-F
identical to the operator file except the two documented restore cells on row 28.

## Q2. Is the R/O/E split mapping defensible?

**Verdict: APPROVE-WITH-CHANGES.** The mapping rule was applied with zero mechanical errors
across all 101 rows, and all 6 "Unknown" rows map to blank. But the rule misrepresents two
rows: s.jina.ai (`R? / O1 / E?`) and blogsflow.liftbrandfulfillment.com (`RET? / OBS? / EX?`)
map "?" (unknown) segments to Y. A segment meaning "unknown" is being asserted as present.
This convention was inherited from the Oct-22 file (which also carried Y/Y/Y there), but
inheritance does not fix the misrepresentation in the delivered artifact.

## Q3. Is the zero-replacement language finding defensible?

**Verdict: APPROVE.** Independently verified by machine: Type sets 5/5 identical, Class
combo sets 66/66 identical, Priority/Confidence token sets 15/15 identical, and core Role
values 71/71 identical between Oct-22 and v2 (the 5 new Role strings belong to the gap-fill
rows, as they should). Role left free-text is the right call: 71 distinct per-row values
cannot be unified without invention, and no invention happened. A corporate reader can
accept this; the claim is machine-diffable and the Notes row states the method.

## Q4. Are there methodological gaps a skeptical reviewer would flag?

**Verdict: APPROVE-WITH-CHANGES.** Two substantive notes: (a) the "?" R/O/E mapping in Q2;
(b) no BUILD-side verification manifest exists. All 7 gap-fill evidence paths exist on disk
(I checked: 48 capture files + provenance + sha256 for the Tier-1 boards, fallback.chat
captures in raw/0/20261023T144326Z, the UK AISI extraction file, metre-thread/mined-items.md),
but nothing in work-v2 records a BUILD-time existence check, so a reviewer must take the
gap-fill lane's word. Thin links (joinsnail /mcp, agentsspeakup /api/mcp — llms.txt-named
only, bodies uncaptured) sit in "Direct Links" beside verified URLs; the caveat lives only
in Sources prose. The 89 cosmetic-arrow acceptances are NOT a gap: I re-derived them
independently and the DELTA.json machine record backs the claim.

## Fix list (for FINALIZE)

1. R/O/E rule: map uncertainty segments ("R?", "RET?", "OBS?", "E?"/"EX?") to blank, not Y.
   s.jina.ai (row 8) -> R blank, O=Y, E blank. blogsflow.liftbrandfulfillment.com (row 13) ->
   R, O, E all blank.
2. Add a BUILD-side verification manifest to work-v2/ (one line per gap-fill row: evidence
   path exists; bytes + PROVENANCE + sha256 present), so the "PRIMARY observed bytes"
   assertion is auditable from the build record.
3. Thin links: remove joinsnail.com/mcp and agentsspeakup.com/api/mcp from Direct Links
   until their bodies are captured, or move the caveat into the Review flag column so
   Direct Links stays verified-only. (This answers GAPFILL.md open question 2.)
4. Notes changelog: record that the "?" mapping change (fix 1) corrects a convention
   inherited from the Oct-22 file, for traceability.
