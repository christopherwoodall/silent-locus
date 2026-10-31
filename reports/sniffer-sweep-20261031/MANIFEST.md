# MANIFEST — sniffer sweep 20261031

## Report dir (reports/sniffer-sweep-20261031/)

- REPORT.md — adjudicated report. 1 TOI, 1 anecdote, 3 watch items,
  3 negatives, 12 cuts with reasons.
- hits.json — adjudicated items with grade, novelty, evidence path.
- adversarial-review.md — copy of raw/adversarial/adversarial-review.md.
- verifier-report.md — copy of raw/verifier/verifier-report.md.
- cryptologist-review.md — copy of raw/cryptologist/cryptologist-review.md.
- MANIFEST.md — this file.
- SHA256SUMS — hashes for the report dir files.

## Raw evidence (data/lanes/sniffer-sweep-20261031/raw/)

- linguist/ — phrase-list.md (46 rows), .PROVENANCE.txt.
- committer-accounts/ — gh commit captures, .PROVENANCE.txt, .sha256
  aggregate list, per-file .sha256 sidecars (added in curation).
- tango-zulu/ — lane notes, counts, HN/urlquery/CDX/Factum captures,
  per-file .sha256 sidecars.
- github/ — 24 captures, .PROVENANCE.txt, .sha256 aggregate list,
  per-file .sha256 sidecars (added in curation).
- hn-forum/ — per-phrase Algolia JSON, hiring candidates, ilands
  captures, thread_47304534.json, _summary.json, ALL.sha256
  (43 entries after curation added _summary.json).
- reddit/ — 8 captures, 00-PROVENANCE.txt, SHA256SUMS.txt,
  per-file .sha256 sidecars.
- urlquery-wayback/ — 36 urlquery files, 4 CDX files, 2 sweep scripts,
  .PROVENANCE.txt, sweep-results.json, SHA256SUMS.txt.
- cryptologist/ — cryptologist-review.md, .PROVENANCE.txt.
- adversarial/ — adversarial-review.md, .PROVENANCE.txt.
- verifier/ — verifier-report.md, .PROVENANCE.txt.

## Curation actions by the coordinator

1. Read the linguist phrase list and pasted it into sweep-lane briefs.
2. Ran read-only Factum match checks (no writes): exact ilands,
   pursekeeper, "handoff received", Beno, agent-swarm, ecoradar,
   "GPT Village" = not_found; exact da.gd = found (25); exact
   "tango zulu" = not_found (tango lane). Fuzzy "ilands hiring" = 25
   matches, likely generic-token driven, not cited as corroboration.
3. Ran Transluce snapshot grep (2026-10-31 file): ilands 36,
   pursekeeper 1, village 0, handoff 0, beno 0, da.gd 0, tango 0.
4. Applied all adversarial verdicts (see REPORT.md cut list) and all
   8 verifier fixes (UQ1 May-June reframe, GH6 9+1, GH5 issue 293 only,
   GH4 excerpt-only label, UQ2-UQ4 rewording, TZ uncaptured-total label,
   missing sidecars, RD1 self-report qualifier).
5. Generated 39 missing per-file .sha256 sidecars (github/,
   committer-accounts/, linguist/) and added _summary.json to hn
   ALL.sha256.
6. Hash verification: all checks pass, 0 failures. Per-file sidecars
   61 checked OK (plus aggregate lists: committer 15 OK, github 25 OK).
   hn ALL.sha256 43 OK. urlquery-wayback 45 OK. reddit 8 OK.
   tango-zulu 12 OK (verifier count).

## Known defects in this delivery (not hidden)

- Raw captures contain human handles, contact addresses, and
  credential-like or wallet values (adversarial presence note, values
  not reproduced in REPORT.md or hits.json). Raw files left intact
  per the never-redact-evidence rule. DO NOT PUSH until the parent
  triages this conflict.
- Legacy-tree grep incomplete (killed on large files in two lanes).
- Reddit live verification blocked (403). ANEC-01 stays REPORTED.
- Committer lanes for Claude, Codex, Devin, and PR search failed on
  the GitHub secondary rate limit. Re-run needed.
- GitHub sweep left 20 phrases unswept (politeness cap). See REPORT.md.
- No Factum writes were made, per the brief. This overrides the repo
  AGENTS.md Factum-storage note for this sweep.
- Commit is local only. The parent pushes and verifies.
