# MANIFEST — Transluce submission-candidate audit, 2026-11-01

Freeze: filings frozen since 2026-10-08. Nothing submitted.
This manifest covers the report deliverable plus the scout
work lane. SHA256SUMS in this directory covers the 14
report files (REPORT, candidates.json, 10 drafts,
adversarial-review, verifier-report); this MANIFEST file
itself is the index and is excluded from that sum by
design.

## Report deliverable (reports/transluce-candidates-20261101/)

- REPORT.md — ranked shortlist (10), reserves (11–26),
  rejections, nulls, open questions.
- candidates.json — machine-readable shortlist + reserves
  + review counts.
- drafts/01-metr-monitoring-evasion.md (TC-01, rank 1)
- drafts/02-july-eval-escape-cluster.md (TC-02, rank 2)
- drafts/03-covert-channel-family.md (TC-03, rank 3)
- drafts/04-destructive-targeting-class.md (TC-04, rank 4)
- drafts/05-beacon-pattern-match.md (TC-05, rank 5)
- drafts/06-production-deletions.md (TC-06, rank 6)
- drafts/07-probe-upload-trace.md (TC-07, rank 7)
- drafts/08-delegated-acts.md (TC-08, rank 8)
- drafts/09-approval-guard-mechanisms.md (TC-09, rank 9)
- drafts/10-vendor-monitoring-suppression.md (TC-10, rank 10)
- adversarial-review.md — copy of the adversarial lane
  verdicts (no candidate earns STAND).
- verifier-report.md — copy of the verifier lane report
  (SHIP-WITH-FIXES; fixes applied in REPORT.md).
- SHA256SUMS — 14/14 verified OK at build time.

## Scout work lane (data/lanes/transluce-candidates-20261101/work/)

- reports/candidates.md + findings.md (26 kept, ~150 rejected)
- factum/candidates.md + findings.md (31 records, 12 batches)
- lanes/candidates.md + findings.md + tracker-index.md
  (140/140 cached findings indexed)
- crypto/candidates.md + findings.md (1 weak provisional,
  1 held, ~17 killed)
- adversarial/adversarial-review.md
- verifier/verifier-report.md

## Excluded by design

- data/lanes/tier1-atlas-crosswalk-20261101/ — in-flight
  atlas swarm lane; never opened, never written by this
  audit. Its findings are pending, not candidates.
- data/records/, data/.local/factum.db — read-only
  throughout; no Factum mutation.
