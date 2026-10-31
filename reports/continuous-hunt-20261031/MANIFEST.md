# Continuous hunt round 20261031 — manifest

## Report dir (this dir)

- REPORT.md — consolidated report (VERY-interesting: none).
- RUNNING-LOG.md — running log, appended as lanes and reviews
  landed, plus coordinator synthesis notes.
- hits.json — 16 documented items (DOC-01 to DOC-16) and 7
  honest nulls (NULL-01 to NULL-07). No TOIs. very_interesting
  is an empty list.
- adversarial-review.md — adversarial review, SHIP-WITH-FIXES,
  52 verdicts (8 KILL, 14 DOWNGRADE, 30 STAND).
- verifier-report.md — verifier report, SHIP-WITH-FIXES,
  43 live PASS, 0 FAIL, 1 INCONCLUSIVE, 139 hashes passed.
- MANIFEST.md — this file.
- SHA256SUMS — hashes for the report dir files except itself.

## Lane dirs (raw evidence + FINDINGS)

All under data/lanes/continuous-hunt-20261031/raw/:

- surfaces/ — 5 targets, FINDINGS.md + captures with
  .PROVENANCE.txt + .sha256.
- committer/ — FINDINGS.md + STATE.md + captures with
  provenance + sha256.
- rotation/ — FINDINGS.md + captures with provenance +
  sha256 (includes the corrected jqp.vercel.app newest
  capture date 2026-10-10).
- phrases/ — FINDINGS.md + PROGRESS.md +
  factum_match_summary.json + captures; per-file .sha256
  sidecars generated post-hoc by the coordinator (82 of 82
  verified), see COORDINATOR-SIDECAR-NOTE.txt.
- unmeasured/ — FINDINGS.md + STATE.md + run-leftovers.sh
  + run.log + captures with provenance + sha256.
- cryptologist/ — FINDINGS.md + DECODE-NOTES.md.
- adversarial/ — working notes (review itself lives in the
  report dir).
- verifier/ — working notes (report itself lives in the
  report dir).

## Curation notes

- Lane FINDINGS files retain their original wording. All
  adversarial and verifier blocking fixes are applied in
  REPORT.md wording and listed there under "Corrections
  applied."
- No Factum writes were made. No push was made; the parent
  pushes and verifies.
- No file outside data/lanes/continuous-hunt-20261031/ and
  reports/continuous-hunt-20261031/ belongs to this round.
