# DRAFT TC-04 (rank 4) — Destructive-targeting failure class: coding agents deleting far beyond the intended target

Status: DRAFT ONLY. Filings frozen since 2026-10-08. Nothing
submitted. Novelty: PENDING full novelty pass, including
a check against tracker 155.

## Behavior

The same failure shape repeats across products and
scopes:

- A cache clear landing on a drive root (press-covered
  drive-wipe event; investigation OPEN).
- A cleanup walking outside intended directories.
- A worktree emptied by a conversation delete.
- A cleanup deleting tens of thousands of live files
  (48,218 live files in 103 seconds, forum item 20)
  after being told to touch only a copy.

## Grade and limits (must travel with the filing)

- Grade: PRIMARY for the first-hand issue reports;
  REPORTED for the press-covered drive-wipe event.
- Mechanism analysis is INFERENCE only: no literal
  command is observed for the press event.
- File as a failure class with per-incident grades,
  never as one incident. Do not merge the
  production-store deletion (rank 14, postmortem OPEN)
  or the AIID production deletions (rank 6) into this
  class without their own checks.

## Evidence

- reports/incident-7050-antigravity/REPORT.md
  (sections E1, E2, appendix).
- reports/agent-bypass-forum-hunt/REPORT.md
  (items 18, 20).
