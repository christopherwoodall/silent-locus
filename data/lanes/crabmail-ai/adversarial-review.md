# Crabmail.ai — adversarial review

Role: adversarial reviewer. This review tries to kill claims before ingest.
It does not add new evidence. It reads only the wave-1 lane files and the
raw captures in `raw/2026-10-24T215128Z/`.

Terms, defined on first use:

- Agent: a software system that acts on its own to do tasks.
- Provider: the service that runs agent mail, here crabmail.ai.
- Descriptor: a short public JSON file that names a provider and its
  capabilities. It is not a secret.
- Federation: message flow between two different providers.
- Relay: a server queue that holds a message for a short time, then
  passes it on. It is local to one provider, not cross-provider.
- Webhook: a web address that a service calls when a new event occurs.
- WebSocket: a long-lived link that lets a server push data at once.
- Tenant: a workspace. One human account owns one tenant name.
- Trust level: a label that says how much a recipient should trust a
  message.
- Doc claim: a statement found in site docs or pages. It is not a tested act.
- Snapshot: one fetch at one time. It is not a stable fact.

## Byte checks I ran

These checks passed. Hash files match the bytes on disk.

- `15-health.body`: 122 bytes. SHA-256 matches. Body:
  healthy, version 0.1.0, provider crabmail.ai, federation true,
  `agents_online` 2, `uptime_seconds` 72697.
- `16-info.body`: 404 bytes. SHA-256 matches. Capabilities are
  federation, webhooks, websockets, relay. `registration_modes` is
  open. Route URL is `https://api.crabmail.ai/v1/route`. Rate limits
  are 60 messages a minute and 100 API requests a minute.
- `17-openapi.body`: 3,468 bytes. SHA-256 matches. It lists 16 paths.
  It lists no request or response schemas. It lists no webhook path
  and no WebSocket path. It lists no tenant path.
- `01-api-wellknown.body` (412 bytes) and `02-root-wellknown.body`
  (512 bytes): SHA-256 matches. Values match. Only formatting differs.
  The provider public key and fingerprint match across both copies.
- All 18 provenance files say `curl GET`. No POST provenance exists.
- The federation GET probe returned 404 with a generic `not_found`
  body, the same body as the API root. The OpenAPI spec lists
  `/federation/deliver` as POST only. The 404 is not proof of death.

One byte check FAILED, and it matters. See C21.

## Verdict table

Verdict words: KEEP means ingest as stated. DEMOTE means ingest only with
the weaker grade and the note given. KILL means do not ingest as stated.

| # | Claim | Verdict | Reason | What would revive it |
|---|---|---|---|---|
| C1 | 18 GET captures, 16 returned 200, 2 returned 404 with saved error bodies | KEEP | Matches the capture set and the analysis table. | — |
| C2 | Descriptor values at both URLs, values match | KEEP | Both descriptor bytes read. Version AMP010, endpoint `https://api.crabmail.ai/v1`, provider crabmail.ai, five capabilities, federation endpoint, contact `support@crabmail.ai`. | — |
| C3 | Health bytes as listed in byte checks | KEEP | Matches `15-health.body` exactly. Grade the count claim separately (see C9). | — |
| C4 | Info bytes as listed in byte checks | KEEP | Matches `16-info.body` exactly. | — |
| C5 | Descriptor/info capability gap: info drops registration, adds `registration_modes` open | KEEP | Verified diff between the two bodies. Cause is unobserved, and the analysis says so. Keep the gap as a mismatch to watch. | A later info fetch, or a doc fix. |
| C6 | OpenAPI path list, including register, route, pending, resolve, and federation deliver | KEEP | Matches `17-openapi.body` exactly. Paths only. No schemas. No live call is claimed. | — |
| C7 | Provider public key and fingerprint are published descriptor values, not secrets | KEEP | They appear in public docs and both descriptor copies. The executor note is right: do not ingest them as a credential. | — |
| C8 | No POST, no login, no registration, no delivery attempted | KEEP | All 18 provenance files say GET. Gated paths were listed, not probed with auth. | — |
| C9 | Two agents were online at probe time | DEMOTE | The field name `agents_online` is the only evidence. No captured file defines it. It could count agents, sessions, or WebSocket links. It could include test or operator links. It is also a snapshot at 2026-10-24T21:52:56Z, not a stable user count. | A doc definition of the field, or repeated health fetches that show the field moving with known agents. Until then: "health reported `agents_online` 2." |
| C10 | Live service, not a dead demo page | DEMOTE | Weaken it. Health answered healthy at probe time, but uptime is 72,697 seconds, about 20 hours. That implies a recent start or restart, not a long-lived history. The root descriptor copy was last changed 2026-10-24T00:09:24Z, the same day. | Repeated health fetches over days. |
| C11 | Live two-provider federation test on 2026-10-23 | DEMOTE | This is a vendor self-report on the home page, not an observed delivery. Wording: "We tested delivery to and from a second provider running our software, on a separate host, in both directions, on 2026-10-23." The second provider is unnamed. It runs the vendor's own software, so it is not an independent peer test. No delivery was observed here. No second provider was probed. | A named peer, a delivery log, or an independent probe. Until then: "vendor reports a 2026-10-23 two-provider test." |
| C12 | Three trust levels with external-content wrapping as a working mechanism | DEMOTE | The model is documented in `13-developers-md.body` and in part on the home page, but no message was ever sent or received here, so wrapping was never tested. Also note the conflict: the home page lumps outside-tenant mail with untrusted mail, while the developer doc splits External (valid signature, other tenant or provider) from Untrusted (missing or invalid signature). Both wrap, but the labels differ. | A live message test that shows the wrap. Out of scope here. Ingest the doc version with the conflict noted. |
| C13 | Message signature covers from, to, subject, priority, in_reply_to, and a sorted-JSON SHA-256 payload hash | DEMOTE | Docs only. No signed message was observed. No signature was checked. Agent keys are Ed25519 per docs, but no live key or signature appears in any capture. | An observed signed message and a checked signature. |
| C14 | WebSocket push in about 70 ms, webhook one live attempt plus two background attempts | DEMOTE | Docs only, self-reported. No push was observed. No WebSocket or webhook path exists in the OpenAPI spec. | A live push observation. Out of scope here. |
| C15 | Relay life 7 days, limits 256 / 64 KB / 256 KB / 512 KB, send rate 60 a minute and 500 an hour, skew logged not rejected | DEMOTE | Docs only. The OpenAPI spec carries no schemas and no limits. Info confirms only 60 messages and 100 API requests a minute. The hourly cap, size caps, and skew rule rest on docs alone. | A live rate or size test, or spec schemas. |
| C16 | Human gate: email code sign-in, first claim wins a tenant name, agent cannot sign up or pay alone | DEMOTE | Docs and marketing only. The app login and register pages were not fetched. The OpenAPI spec has no tenant path at all, so the tenant-claim shape is unconfirmed by the spec. | App-page text, or a spec path for tenants. |
| C17 | Federation flow: sender provider routes to the recipient deliver endpoint, and the relay queue still applies on the far side | DEMOTE | Pure inference, and the analysis labels it so. No federation request or response was observed. Keep it as inference only. Never ingest it as a mechanism. | An observed federated delivery. |
| C18 | Provider key authenticates federation | DEMOTE | Inference. The descriptor names no signature scheme for the provider key and no signed bytes for federation. Agent messages are optionally Ed25519-signed per docs, but the provider key's role in federation is unstated. The link between agent keys and the provider key is unobserved. | A doc or spec that states the federation signing rule. |
| C19 | Skill and slash-command pack for one agent family (register, send, inbox, read) | DEMOTE | Only `18-install-skill.body` was captured, as bytes only, and it was not run. The command files themselves are not in the 18-file capture set. The pack's run-time behavior is unobserved. | Captures of the command files, or a run note. |
| C20 | Descriptor source URL is now resolved, including the slot-0 capture | DEMOTE | Cross-lane claim. It rests on a prior capture that is not in this lane's raw set. This lane alone proves two URLs serve the same values now. It does not prove the prior capture's source. | Executor check against the prior capture before repeating the claim. |
| C21 | Fingerprint verifies the provider key | KILL | Recompute fails. SHA-256 of the raw 32 key bytes gives `aKUrlqUngJLZZhWzAx1gb9jd0TPyhxr65+X8J9rff94=`. SHA-256 of the hex text gives `DzraS6j6l+Jns8pr0ncF7ja4dzwvtljLxRA6IxdUpAI=`. The claimed fingerprint is `SHA256:3B7TdLvjLmV45mzjq9NcknszAa5jCcNLW0BXZKv3nSs=`. Neither matches. The hashed input is unstated, so this is not proof of forgery. But no "fingerprint matches key" claim may ingest. | A stated fingerprint input that recomputes to the claimed value. Until then, ingest key and fingerprint as two separate published values with no verified link. |
| C22 | Relay and federation are one path, or relay explains federation | KILL | Conflation. Relay is the local queue at `GET /v1/messages/pending`. Federation is the cross-provider path at `POST /v1/federation/deliver`. They are separate OpenAPI paths. Note also the spec's own tension: its description calls Crabmail a "relay-only provider" while listing federation as a capability and a path. | Ingest relay and federation as separate items, and record the "relay-only" wording as a spec conflict. |
| C23 | Pending-ack call shape is settled | KILL | Mismatch. Docs say `POST /v1/messages/pending/ack` (batch). The spec lists both that path and `DELETE /v1/messages/pending/{id}` as "acknowledge." The analysis table lists the DELETE form under one row and the POST form under another without flagging the split. | A doc or spec fix, or a live ack test. Until then, ingest as an unresolved mismatch. |
| C24 | Webhooks and WebSockets are live endpoints | KILL | No webhook path and no WebSocket path exist in the OpenAPI spec. They appear only as capability strings in the descriptor and info bodies. A listed capability may be planned, partial, or live. The descriptor alone cannot prove liveness. | A spec path, a live push, or a doc endpoint for each. |
| C25 | Any wording that calls Crabmail NEW, first-seen, or undiscovered | KILL | No corpus check is in this lane. No Factum match, legacy search, or Transluce check was run here. The analyses make no explicit NEW claim, which is good. The executor must not add one. | Executor match results. Until then, grade as ungraded for novelty. |

Counts: KEEP 8, DEMOTE 12, KILL 5.

## Sensitivity findings

No credential value, private key, live agent address, live agent public
key, or live message was found. The provider public key and fingerprint
are published values, not secrets. They do not block ingest, but they
must carry the C21 note: the link between them is unverified.

What WAS found, and how to handle it:

- Role addresses, public: `support@crabmail.ai` (descriptor contact),
  `security@crabmail.ai` (security.txt), `hello@agentmessaging.org`
  (AMP site contact). These are published contact points. They do not
  block ingest. Do not treat them as agent identities.
- Example addresses, not live agents: `name@tenant.crabmail.ai`,
  `builder@yourteam.crabmail.ai`, `reviewer@yourteam.crabmail.ai`,
  `builder@23blocks.crabmail.ai`. These are doc placeholders. They do
  not block ingest. Do not ingest them as live agent addresses.
- One example address carries a first name: `sebastian@23blocks.crabmail.ai`.
  Source: `10-developers.body` and `13-developers-md.body`, in developer
  docs. This looks like a doc example, not a live agent. It does not
  block ingest. It must NOT become a human-identity record, and no
  follow-up identity work may be built on it. Ingest it only as
  "example address in developer docs," or omit it.
- Format example only, not a real key: the OpenAPI security scheme
  describes agent API keys as `amp_live_sk_...` and user keys as
  `uk_xxx`. These are patterns with placeholders, not values. They do
  not block ingest. Do not quote them as keys.

No finding here blocks ingest. The block would be a real private key, a
real API key, or a live agent address with its public key. None was found.

## Boundary and conflation check

- Public versus credentialed surfaces are handled honestly. Health,
  info, OpenAPI, descriptors, and docs were fetched without auth. All
  agent-key paths (agents, resolve, pending, read receipts, route,
  register) were listed, not probed with auth. App login and register
  pages were not fetched.
- The GET 404 on `/federation/deliver` is handled correctly in the
  analysis: POST-only per spec, not dead. The executor must keep that
  note. Do not mark the endpoint dead.
- The registration gap is handled correctly: info drops registration
  from capabilities, but the spec and docs still list register. That
  is a mismatch to watch, not proof of removal.
- The remaining conflation risk is C22 (relay versus federation) and
  C24 (capability strings versus live endpoints). Both are killed above.

## Final ingest gate: GO-WITH-CHANGES

Changes the executor must apply before ingest:

1. Apply every DEMOTE: quote `agents_online` 2 as an undefined health
   field at one time, quote the 2026-10-23 federation test as a vendor
   self-report with an unnamed peer running vendor software, and grade
   trust wrapping, push timing, limits, and the human gate as doc
   claims only.
2. Apply every KILL: ingest the provider key and fingerprint as two
   separate published values with no verified link; split relay from
   federation and record the "relay-only" spec tension; record the
   pending-ack mismatch; do not list webhooks or WebSockets as live
   endpoints; add no novelty wording until match checks run.
3. Carry the sensitivity notes: role addresses and example addresses
   only, no live agent identities, no human-identity record from the
   `sebastian@` example, no key values quoted.
4. Do not ingest the provider key or fingerprint as a credential. The
   analysis already says this. Keep that guard in the ingest notes.
5. Run the novelty checks before any NEW wording: Factum match, legacy
   corpus search, and Transluce check, with scope recorded. Also check
   the prior slot-0 capture before repeating the descriptor-source
   claim (C20).

If any change above is skipped, the gate falls to NO-GO for the affected
claims, not for the whole lane. The verified byte facts (C1–C8) may still
ingest.
