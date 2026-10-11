# anyrun-scan VERDICT — DEAD END (2026-10-07)

## Finding
any.run is not a viable hunt surface for the rogue-agent traces. Ruled out on
friction, not on content.

## Evidence
- TI Lookup and task submission both require a registered account. No anonymous
  access (verified: API endpoints return 401 without a login token).
- Self-service registration **rejects personal email addresses** — the signup form
  shows "Enter a valid business email" for proton.me and disables submission.
  Personal-email users are directed to manual verification via X or Discord
  (human-in-the-loop).
- Attempted live 2026-10-07: form filled (handle "swarmtrace", proton.me email),
  blocked at the business-email validation. No account created, nothing submitted.

## Reasoning
The observed agent pattern favors zero-friction public surfaces: urlquery.net and
arquivo.pt require no account to submit, which is exactly why the traces are
public. any.run's business-email gate + human verification is the opposite shape.
An eval-run harness optimizing for scale would not route through a manual-approval
chokepoint when account-free alternatives exist and are already in use.

## Grade
INFERENCE (friction-based deprioritization). Not proof of absence — a sufficiently
motivated operator with a business email could still submit. But the shape does
not match the observed campaign, and the scan cannot proceed without an account
we do not have.

## Branch status
Kept as a record. PLAN.md (surface map + shape pipeline S1–S12) remains valid and
is reusable if account access ever materializes or for tria.ge / hybrid-analysis
if those get scoped.
