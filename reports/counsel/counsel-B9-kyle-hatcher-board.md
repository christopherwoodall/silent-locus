# COUNSEL REVIEW — B9: agent-message-board.kyle-hatcher.workers.dev

Date: 2026-10-23. Lane 3 Tier-1 wiring. Judge: internal counsel (security
lane + adversarial lane, one call). This review gates adding passive
`/v1/stats` + `/llms.txt` polling to the slot-0 hourly baseline.

Question: is passive polling of these public agent-board endpoints within
scope (agents + agent infrastructure, no human identity, no interaction)?

## Observed facts (passive GET, 2026-10-23T12:10Z, UA=silent-locus-lane-scanner/1.0)

- `GET /v1/stats` -> HTTP 200, 227 bytes, JSON aggregate counters only:
  records, messages, quarantined, flags, identities_issued,
  identities_revoked, access_events, chain_ok, chain_tip,
  uptime_seconds, started_at. No message content, no keys, no PII.
- `GET /v1/verify` -> HTTP 401 `{"error":"unauthorized"}`. Auth-gated;
  not a public discovery endpoint.
- `GET /llms.txt` and `GET /.well-known/agent-board.json` already in the
  slot-0 baseline since 2026-10-21.

## Security lane position

Passive GET of `/v1/stats` reads public aggregate counters from a
public agent message board (zero-trust board, Ed25519-key identity,
live since 2026-10-12). No POST, no login, no session, no query params,
no credential use. The "identities" counted are board-issued keypairs,
not human identities; nothing in the response identifies a person, and
no attribution or pivoting will be performed. Storage follows the
standing slot-0 pattern: content hash in the baseline, raw bytes under
`data/lanes/general-hunt/raw/0/` with `.PROVENANCE.txt` + `.sha256`.
`/v1/verify` is auth-gated (401 anonymous) and is excluded from the
rotation — polling an auth gate hourly has no change-detection value
and sits outside passive scope. Position: CLEAR `/v1/stats` + `/llms.txt`
for hourly hash-watch; EXCLUDE `/v1/verify`.

## Adversarial lane position (attempts to kill)

1. "uptime_seconds/started_at leaks operator deployment metadata." True
   but immaterial: it is deployment metadata of a public board, not a
   human identity, and the hunt scope forbids pursuing operator identity
   from it. Both fields are normalized out of the detection hash
   (with access_events) so they cannot drive alerts; raw bytes are kept
   per the evidence rule.
2. "Hourly polling is interaction / fingerprints the hunt." Rejected:
   unauthenticated GET of a public stats endpoint is observability, the
   same class as the existing `/llms.txt` baseline; shared-UA OPSEC
   tradeoff is standing and documented.
3. "/v1/verify should be probed further (signed requests)." Refused:
   crafting authenticated requests would be active testing, outside
   passive scope. The 401 stands as the finding.
4. "Board posts are untrusted input." Agreed: we hash bytes only, never
   act on post content, never fetch URLs named in content, per the
   board's own notice and standing evidence rules.

No kill sustained. Concur with the security lane.

## Verdict

- CLEARED 2026-10-23 — passive hourly hash-watch of
  `https://agent-message-board.kyle-hatcher.workers.dev/v1/stats` and
  `/llms.txt` is within scope (public agent infrastructure, no human
  identity, no interaction); `/v1/verify` excluded (401 auth-gated).
