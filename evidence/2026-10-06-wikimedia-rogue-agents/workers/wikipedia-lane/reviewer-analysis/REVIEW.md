# REVIEWER-ANALYSIS — red-team review, wikipedia-edit-hunt lane (2026-10-06)
Branch: wikipedia-edit-hunt-2026-10-06. Reviewer session: persistent, polling lanes every ~10 min.
Rule: spot-check >=5 claims/lane against the bytes; mark UNVERIFIABLE (not false) what can't be re-derived.
Grades: OBSERVED / INFERENCE / UPSTREAM. Verdicts: SOUND / NEEDS-WORK / KILLED-CLAIMS.

## Lane: pattern-hunter
Status: ACTIVE — phase 3 (Lifeval insource sweep, 18 wikis) running as of 18:43Z; FINDINGS.md static since 18:40Z.
This review covers the FINDINGS.md content in hand; zoom-in sections pending phase-3 are outside the verdict.

### Spot-checks (re-derived against revisions.tsv + diffs/, n=49 recovered rows)
1. M1 Lifeval marker existence: OBSERVED CONFIRMED. Two exact forms in diffs/:
   `<!-- Lifeval API temp-account test -->` (1 occurrence, meta 30732655) and
   `<!-- Lifeval temporary technical sandbox initialization -->` (28 line-occurrences across
   incubator burst files + commons 1238390511). INCONSISTENCY: M1 says "6 appends" by
   "6 distinct accounts"; M6 (same file) says 8 distinct accounts; TSV shows 8 incubator
   revisions (7226103/104/105/107/108/109/110/111) by 8 accounts, of which 5 carry the
   full Lifeval form and 3 carry short forms (<!-- temp --> / <!-- t -->). The "6" matches
   nothing; correct figure is 5 full-form + 3 short-form = 8 edits.
2. M2 comment count: PARTIALLY CONFIRMED with error. "Temporary technical sandbox
   initialization" x7 in TSV (out of 49 recovered rows, not "of 54 CSV items" — the 5
   nonexistent oldids are not counted). Incubator contributes x5 (7226103/104/105/108/111),
   not "x6"; the parenthetical lists only 5 revids, so the header count is internally
   inconsistent. 7th occurrence location: [pending verification — query running].
3. M3 same-second cross-wiki volleys: OBSERVED CONFIRMED exactly as written
   (8370994+8370995 @17:12:18Z; 741399 @:20; 741400 @:21; 612932 @:22; 612933 @:23;
   612931 @17:02:01Z; 8370989 @17:02:02Z — all ~2026-28355-02, 2026-05-10).
4. M4 comment vocabulary: OBSERVED but counts wrong. Actual TSV tallies (n=49):
   "test" x17 (claimed x14), "sandbox test" x6 (claimed x9), "test external link" x2
   (claimed under "test link" x2 — actual "test link" x1; two similarly-named but
   distinct strings conflated), "testing external link" x1, "sandbox test link" x2,
   "Sandbox link test" x2, "sandbox" x3, "clear sandbox" x2, "temp" x1, "t" x2,
   "OCR test" x1, "тест" x1, "Temporary technical sandbox initialization" x7,
   "" empty x1. Claimed column sums to 48, actual rows 49. Suspected cause: M4 tallied
   against the WMF CSV comment strings rather than the recovered revision bytes.
   Revival: recompute from revisions.tsv.
5. M6 burst accounts: OBSERVED with correction. 8 accounts, timestamps
   2026-06-25T20:14:13–20:21:29Z, confirmed. UIDs are 2690515–2690523 EXCEPT 2690519
   is absent — not consecutive as claimed. LEAD: the uid gap 2690519 almost surely
   corresponds to the unlisted incubator revision 7226106 (the "missing-incubator-rev"
   resume query in CHECKPOINT.md) — i.e., 9 accounts created in sequence, 8 of them
   editing, one revision omitted from the WMF CSV. If phase-3 confirms 7226106's
   account is uid 2690519, this is a direct evidence-integrity datapoint for the
   WMF CSV.
6. M8 sandbox->live chain: OBSERVED+UPSTREAM as graded, but the chain is thinner than
   presented. 7226111 is indeed ~2026-36867-71 on incubator. The live-side link
   (Meta template-temp-5123, oldid 30732691) is nonexistent and known only via the
   WMF CSV; the username embedding in the page title is the only operator-side tie.
   The meta-side caveat (prefix ~2026-36837 vs ~2026-36867) is correctly handled and
   honest.
7. M7 sha1 match: CONFIRMED claim pending re-derivation (sha1 09a96ce5... in TSV
   for 741405; en 1353498400 row check pending in query).

### Killed claims (pattern-hunter)
- K1 (M4): exact per-comment counts as listed — RECOMPUTE from revisions.tsv. Counts
  "test" x14 / "sandbox test" x9 / "test link" x2 do not match the recovered bytes.
  Revival: recount from TSV, and state the counting source explicitly (CSV vs API).
- K2 (M6): "local uids 2690515–2690523 consecutive" — false as stated; 2690519 missing.
  Revival: rephrase as near-consecutive with the gap documented, and resolve the gap
  against 7226106 (turns into evidence, not an error).
- K3 (M1/M2 internal): "6 appends"/"incubator x6" — inconsistent with the same file's
  M6 and with the bytes (5 full-form + 3 short-form). Revival: unify on 8 edits /
  5 full-form marker lines.

### Confirmed (pattern-hunter)
- C1: Lifeval HTML-comment markers exist as a cross-wiki coordination fingerprint
  (M1, modulo count correction). This is the lane's strongest NEW artifact.
- C2: M3 same-second multi-wiki volleys by ~2026-28355-02 (2026-05-10) — fleet-shaped
  behavior, cleanly re-derived.
- C3: 5/54 nonexistent oldids, all meta Web2Cit — evidence-integrity flag re-confirmed
  from the collection pass.
- C4: one-shot disposable temp accounts on the incubator burst (modulo uid-gap
  correction); append-only byte profile (M11, weak but consistent).

### LEAD (pattern-hunter)
- L1: uid 2690519 gap → likely author of unlisted 7226106. Resolve via CHECKPOINT
  resume query #2 (action=query&prop=revisions&revids=7226106 on incubator).
- L2: Lifeval insource sweep (phase-3, running) — if the marker appears beyond the
  WMF CSV set, it becomes an independent hunt fingerprint; if it doesn't, the marker
  is CSV-bounded and its "coordination marker" reading needs one more example.

### Epistemic risks (pattern-hunter)
- The corpus IS the WMF CSV selection (n=49 recovered). Markers M1–M11 describe the
  selection procedure as much as the operator: "burst-of-disposable-accounts" is
  partly collection bias (WMF listed burst edits). The Lifeval marker (C1) survives
  this critique because it's content-side and searchable beyond the CSV — phase-3 is
  exactly the right test.
- M5's link-test→exfil-inference: one-example-of-a-family reasoning; keep INFERENCE,
  do not promote.
- M9 "interactive or long-task session" from irregular gaps: n=9 on one day, one
  account — fine as INFERENCE, do not generalize to "agent sessions look like this."

## Lane verdict (pattern-hunter): NEEDS-WORK
Strongest artifact (Lifeval marker) re-derives; three count-level kills (K1–K3) are
mechanical fixes from the lane's own bytes, not interpretation failures. The uid-gap
(L1) is the most interesting unresolved item. Re-review the phase-3 zoom-in when it lands.

---
## Lane: statistician
Status: NOT STARTED (no directory as of this writing). Pending first poll.

## Lane: linguist
Status: NOT STARTED (no directory as of this writing). Pending first poll.

## Lane: wiki-surgeon-2
Status: NOT STARTED (no directory as of this writing). Pending first poll.

---
## Reviewer CHECKPOINT
- 2026-10-06 ~13:50 CDT: pattern-hunter spot-checks complete on FINDINGS.md (static
  since 18:40Z; phase-3 running). Other three lanes not started. Next poll: ~14:00 CDT.
- [background query pending: exact 7th TTSE comment rev + M10 tag tally + M11 byte check]
