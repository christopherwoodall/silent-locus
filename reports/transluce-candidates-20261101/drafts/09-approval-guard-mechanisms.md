# DRAFT TC-09 (rank 9) — Approval-guard mechanism cluster: guard settings that do not guard

Status: DRAFT ONLY. Filings frozen since 2026-10-08. Nothing
submitted. Novelty: PENDING full novelty pass.

## Behavior

Five distinct guard failures share one lesson:

- An approval policy that is never read.
- A subagent loop that synthesises approval.
- An unscoped configure grant that lets any agent
  rewrite any agent's instructions.
- A confirmation callback that is never wired.
- A launcher that grants permission-bypass flags on
  every run.

## Grade and limits (must travel with the filing)

- Grade: REPORTED mechanism grade (tested, code-read,
  and stated cases mixed; per-item bounds in source).
- These are MECHANISMS, not agent choices. File as a
  mechanism cluster, never as agents bypassing
  restrictions on their own behalf.
- The weakest mechanism (a stated, undemonstrated
  sandbox escape) is dropped from this draft.

## Evidence

- reports/agent-bypass-forum-hunt/REPORT.md
  (mechanisms M1–M9; strongest M2, M3, M6).
