# Lane: anyrun-scan

## Purpose
Factum ingest of the anyrun-scan negative finding. any.run was probed as a
hunt surface for rogue AI-agent eval-run traces (shape-based hunt on public
sandbox tasks). Verdict: DEAD END. Ruled out on friction, not on content.

## Legacy documents
The scan workspace stays at `evidence/anyrun-scan/` (PLAN.md, VERDICT.md).
This is a two-file analysis directory, not an event lane. We did not add the
`remove-` prefix. The directory stays in place as the scan's record. This
lane holds the structured verdict.

## Records in this lane
- 1 source record: `evidence/anyrun-scan/VERDICT.md`.
- 2 `reachability.check` observations: the auth-gated TI Lookup API (401) and
  the business-email-only registration form.
- 1 claim record (OBSERVED): the account-gate friction findings.
- 1 claim record (INFERENCE): the surface-viability deprioritization.

## Factum lane tag
All records carry `{"lane": "anyrun-scan"}`.
