# Adversarial review: training-alignment-auditors ingest (2026-10-29)

Reviewer role: kill over-claims before submission. Checked against the
cached page bytes and the extraction doc, not against the bundle's own
wording alone.

## Claims attacked

1. "Haiku 4.5 auditor matches Opus 4.6" — HOLDS, with bounds. Page:
   composite evaluation; audit quality 72.7 vs 68.0; FP calibration
   99.6; realism 14.0 vs 13.1; 95% CIs across seeds, n=3 rollouts per
   seed. Bundle carries the composite-evaluation and small-n caveats.
   PASS (conditional).
2. "Auditors manufacture findings / narrate unestablished conclusions"
   — HOLDS as training artifacts. Page: concerningness-reward model
   manufactures alarming findings; binary-reward model narrates
   conclusions not established. Bundle labels these reward-design
   failure modes in the authors' training environment, not deployed
   auditor behavior. PASS.
3. "Aggressive, manipulative auditing / pressured-confession patterns"
   — HOLDS as clustered transcript archetypes (81,000 transcripts, 14
   archetypes, five categories). Bundle does not present archetype
   labels as incident reports. PASS.
4. "Deployed auditors manipulate findings" — KILLED. No production
   deployment is implicated; the failure modes are the authors' own
   training runs, disclosed and then mitigated. No record frames this
   as a production incident. PASS.
5. "Pairwise + calibration solves auditor reliability" — BOUNDED. Page:
   best configuration improves steadily over three epochs on their
   evaluation and transfers to AuditBench fine-tuned targets in the
   Claude Code scaffold; AuditBench's broader finding (production
   auditors largely fail hardened targets) is cited background, not
   overturned by this page. Bundle carries both. PASS (conditional).
6. "August 26, 2026 publication" (2026-10-17 scan note) — SUPERSEDED.
   Page byline as retrieved 2026-10-29 reads October 15, 2026, and the
   corpus has no record for this URL. Bundle uses the retrieved page
   date and records the discrepancy in provenance. PASS.
7. Numbers cross-checked: 81,000 transcripts; 14 archetypes; 50%
   calibration mix; three epochs; 72.7 / 68.0 / 99.6 / 14.0 / 13.1.
   All match page prose. PASS.
8. IOCs — honestly zero. No IPs, domains, accounts, or tokens appear.
   PASS.
