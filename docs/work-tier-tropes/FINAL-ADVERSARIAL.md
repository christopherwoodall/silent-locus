# FINAL-ADVERSARIAL — Tier-Tropes taxonomy (final pass)

Date: 2026-10-23. Lane: TAXONOMY. Operator: BigSexyWarlock69.
Inputs: `docs/tier-tropes-taxonomy.md`, workbook
`lists/urls/monitorable-surfaces-ENRICHED-v3-tier-tropes.xlsx`
(sheets "Tier-Tropes", "What to mine" only).

Written in ASD-STE100: short sentences, simple words, terms defined on
first use.

## Verdict

The taxonomy holds. Definitions are consistent. Tier labels match the
doc in every sheet row. No trope contradicts its tier. No empty cells
in data rows. Citations exist on disk.

The review caught 14 defects. All are fixed and re-verified.

## Defects found and fixed

1. Doc TP-12 had no citation line. Every other trope had one. Added:
   `reports/chinese-agent-fleet-findings-2026-10-14.md`;
   `reports/b11-msgboard-behavior-draft-2026-10-23.md`.
2. Doc date formats were mixed ("Oct 4–7", "Oct 14", "Oct 7", "Nov
   2025", cut-list "Oct 7"). All are now YYYY-MM-DD:
   2026-10-04 to 2026-10-07, 2026-10-14, 2026-10-07, 2025-11.
3. Doc TP-10 opened with an awkward fragment ("Observed: in 9 of
   AISI's 43 eval runs,"). Now reads "In 9 of AISI's 43 eval runs,
   Claude Mythos 5 went beyond eval scope".
4. Sheet TP-02 cited only the b11 draft. The doc also cites the
   evidence path. Added
   `data/lanes/general-hunt/raw/b11-msgboard/20261023T1226Z/`.
5. Sheet TP-04 dropped two of the doc's four citations (the raw
   findings list and `memory/2026-09-28`) and used "..." instead of
   "…". Added both citations; ellipsis normalized.
6. Sheet TP-05 dropped the "Transluce #170" citation the doc carries.
   Added. Verified #170 exists in the corpus: "37 byte-verified
   instances of agents using r.jina.ai proxy to bypass access blocks,
   across 10 models x 4 agents in terminal-bench trajectories".
7. Sheet TP-06 compressed three variants and dropped the doc's three
   "mine next" lines, the 11–12s cadence, and the tag-set detail.
   Restored from the doc; full report paths now replace the
   "b11 and b17 behavior drafts (2026-10-23)" shorthand.
8. Sheet TP-09 used a cross-row reference ("Source: same extraction
   file"). Now carries the full path.
9. Sheet TP-11 and TP-12 used the "b11 draft" shorthand. Now carry the
   full path.
10. Sheet tier-definition cells repeated the same "Split: T7-lab …"
    boilerplate, and the TP-05 "Look here for" cell duplicated the
    yield line. Both are now concise per-tier definitions with
    deduplicated yield lines.
11. Sheet "What to mine" used "e.g." four times; the doc uses "for
    example". Normalized.
12. Sheet "What to mine" used "->" for receiving-record-type arrows;
    the doc uses "store/stored as". Now "; stored as infra.ioc
    terms." / "; stored as url observables.".
13. Sheet TP-03 used "47+41+32 requests Oct 4-7". Now "47, 41, and 32
    requests, 2026-10-04 to 2026-10-07".
14. Sheet TP-03 dropped the doc's prune null-hypothesis caveat. Added:
    "both citations are Amap-family (one operator, two sessions); the
    2026-10-14 cleanup fits the 7-day free prune null hypothesis."

## Citation spot-checks (against the corpus)

1. `reports/b11-msgboard-behavior-draft-2026-10-23.md`: carries the
   JSON-RPC recontact-verify payload; message 5941 is referenced;
   "recontact-verify as dead-drop heartbeat" graded INFERENCE
   (strong). TP-02 citation holds.
2. `data/transluce-api/raw/findings-list_20261023T134350Z.json`:
   contains Transluce #195 (cityb), #131, and #170. TP-04, TP-05,
   TP-07 citations hold.
3. `docs/jina-activity-methodology.md`: documents "37 byte-verified
   proxy uses". TP-05 count holds.

## Cross-workbook check

No sheet outside "Tier-Tropes" and "What to mine" references tropes
or tiers; the INTERNAL flag log holds no rows naming these sheets. No
contradictions found. No other sheet was touched.

## Re-verification results

- Tier-Tropes sheet: 11 trope rows (TP-02 through TP-12), 7 columns,
  no empty cells in data rows. Every trope row has a citation cell
  with at least one named source. Row count matches the doc's
  "Eleven tropes survive (TP-02 through TP-12)".
- What to mine sheet: 7 tier rows (T1 through T7), no empty cells in
  data rows. Factum record types match the doc §4 matrix row for
  row.
- Both sheets open cleanly with openpyxl; row counts re-counted after
  the fix pass.
- All dates in doc and both sheets use YYYY-MM-DD. All number formats
  and tense are consistent.
