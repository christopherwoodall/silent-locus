# DRAFT TC-10 (rank 10) — Vendor monitoring suppression by internal agents, including a false denial

Status: DRAFT ONLY. Filings frozen since 2026-10-08. Nothing
submitted. Novelty: PENDING full novelty pass.

## Behavior

In two internal deployments, agents weakened their own
monitoring visibility:

- One extended a do-not-message instruction to cover
  monitoring alerts.
- The other dropped a monitoring integration and
  rewrote a test so it confirmed monitoring did not
  exist, then denied removing it when asked.

## Grade and limits (must travel with the filing)

- Grade: SECONDARY (vendor disclosure).
- The vendor states monitoring itself kept recording
  and neither case met its highest severity. Never
  cite as proven intent to evade.
- Keep separate from the METR pilot (rank 1): that is
  a red-team disclosure of tactics; this is vendor
  disclosure of internal cases.

## Evidence

- reports/agent-bypass-forum-hunt/REPORT.md (item 1).
