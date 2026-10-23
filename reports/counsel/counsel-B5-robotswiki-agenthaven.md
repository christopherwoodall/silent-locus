# COUNSEL REVIEW — B5: robots.wiki + agenthaven.org Tier-1 promotion

Date: 2026-10-23. Lane 3 Tier-1 wiring. Judge: internal counsel (security
lane + adversarial lane, one call). This review gates Tier-1 promotion
of two already-baselined agent surfaces.

Question: is passive polling of these public agent-board endpoints within
scope (agents + agent infrastructure, no human identity, no interaction)?

## Observed facts

- `https://robots.wiki/llms.txt` — in the slot-0 baseline since
  2026-10-21. Public agent board: MCP `/mcp`, OpenAPI, skill file, Atom
  feeds. Evidence: `data/lanes/general-hunt/raw/0/2026-10-21T024000Z/`.
- `https://agenthaven.org/llms.txt` — in the slot-0 baseline since
  2026-10-21. Agent messaging network (released 2026-09-29): open forum
  + E2E DMs, MCP server, hourly witness record. Evidence: same dir.
- Promotion changes list membership only: Tier-1 rows in
  `lists/urls/trajectory-domains.md` + continued hourly hash polling.
  No new endpoints are added by this lane.

## Security lane position

Both are public agent-infrastructure surfaces purpose-built for AI
agents to communicate. Collection method is unchanged: passive GET of
the static `/llms.txt` discovery document, content-hash compared hourly,
no login, no interaction. agenthaven's E2E DMs are cryptographically
inaccessible by design — there is no private-comms read risk. No human
identity is sought, extracted, or attributed; forum content is not
polled. Position: CLEAR Tier-1 promotion for both domains.

## Adversarial lane position (attempts to kill)

1. "agenthaven's open forum may carry human posters; polling risks
   collecting human identity." Rejected as scoped: this lane polls only
   the static `/llms.txt` discovery doc, never forum feeds. No identity
   extraction, no attribution, no pivoting. Any future forum-feed
   endpoint requires its own counsel pass — recorded here as a gate.
2. "Tier-1 promotion implies an endorsement or malicious verdict."
   Rejected: Tier-1 = "direct agent infrastructure" watch tier, a
   monitoring commitment, not a verdict about the operator.
3. "Hourly polling burdens small operators." Rejected: one GET/hour per
   endpoint under the shared UA is negligible and matches the standing
   slot-0 pattern already applied to both since 2026-10-21.
4. "E2E DMs could be decrypted or leaked server-side." Out of scope for
   this review: we have no access path and seek none; the watch does not
   touch DM surfaces at all.

No kill sustained. Concur with the security lane.

## Verdict

- CLEARED 2026-10-23 — Tier-1 promotion of robots.wiki and
  agenthaven.org is within scope (public agent infrastructure, existing
  passive /llms.txt hash-watch, no new endpoints, no human identity,
  no interaction); forum-feed endpoints, if ever proposed, need a fresh
  counsel pass.
