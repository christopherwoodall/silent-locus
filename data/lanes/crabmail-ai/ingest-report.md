# Crabmail-ai — ingest report

Lane: `crabmail-ai`.
Status: DRAFT — batch ids and record counts to fill after export.

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
- Doc claim: a statement found in site docs or pages. It is not a tested
  act.
- Snapshot: one fetch at one time. It is not a stable fact.

## Lane decision

- Lane name: `crabmail-ai` (lowercase, hyphens, no date).
- Lane id: `lane_cb7ed0aa90f6494ab0c894a91ada6dd8` (created
  2026-10-24T22:27:36Z via `lane new`).
- Lane dir: `data/lanes/crabmail-ai/`.
- The lane dir already held the wave-1 raw set and notes before ingest.
  `lane new` made the lane record; its lane.json was placed in this dir
  and its tags were set to the full set (docs_path plus scope).

## Coverage (wave-1 scrape, 2026-10-24T21:51-21:53Z)

18 GET captures. 16 returned 200. 2 returned 404 with saved error bodies.
Method: read-only GET with curl only. No POST. No login. No account.
No mail sent. No registration. No delivery attempt. No payload run.

| Endpoint | Status | Bytes | Use in this ingest |
|---|---|---|---|
| https://api.crabmail.ai/.well-known/agent-messaging.json | 200 | 412 | Captured. Descriptor, API-host copy. |
| https://crabmail.ai/.well-known/agent-messaging.json | 200 | 512 | Captured. Descriptor, root-host copy. |
| https://api.crabmail.ai/v1 | 404 | 52 | Error body saved. No index at API root. |
| https://api.crabmail.ai/v1/federation/deliver (GET probe) | 404 | 52 | POST-only per spec. Not dead. |
| https://crabmail.ai/ | 200 | 59729 | Captured. Vendor test self-report. |
| https://crabmail.ai/developers/index.md | 200 | 4886 | Captured. Trust model, limits, gate. |
| https://api.crabmail.ai/v1/health | 200 | 122 | Captured. Health snapshot. |
| https://api.crabmail.ai/v1/info | 200 | 404 | Captured. Info bytes, capability gap. |
| https://api.crabmail.ai/v1/openapi.json | 200 | 3468 | Captured. 16 paths, no schemas. |
| https://crabmail.ai/install-skill.sh | 200 | 2428 | Captured as bytes only. Not run. |

Other wave-1 files (llms.txt, agents.md, agents dir, developers page,
security.txt, agentmessaging.org, get-started) stay in `raw/` and are
committed with this lane. They were not all captured through Factum
`capture`; the key artifacts above were.

## Verification before submit

- Every stored `.sha256` file in the raw set matches its bytes on disk.
  All pass.
- Live re-fetch (polite unauthenticated curl GET) of both descriptor
  URLs, health, and OpenAPI: descriptor copies and OpenAPI match their
  recorded SHA-256 exactly. Health differs in ONE field only:
  `uptime_seconds` moved from 72697 to 73412 (wall time advanced;
  all other fields identical, including `agents_online` 2). This is a
  live snapshot field moving as expected, not a contradiction. The
  capture-time health claim keeps the recorded value 72697 and notes
  the re-fetch. No claim was dropped on re-fetch grounds.
- Slot-0 continuity: slot-0 `crabmail-agent-messaging.json` is
  byte-identical to the wave-1 API-host descriptor copy (SHA-256
  ce539c337310119376aa7927c2b0523e21e0241561113a9feb49e4dc9b8217cd).
  The slot-0 file has no source-URL provenance, so the claim is
  byte-identity only, not source-URL proof.

## Records submitted

Batch ids (9, from export output, read from the exported
`data/records/<batch>/records.jsonl` files): 8 capture batches
`0a1bb91dcc244ab59fbe9df682844b21`, `20345c2ec5b245f09309557f05de2e15`
(descriptor-api, recovered from its durable pending file after the
first chain run's background session died),
`93bb8f322bf348d5b0eecd82c480dba5`, `ad19df948d1a46b591059b3941784588`,
`c505f3ea09804ea68afdc692a18aa119`, `c75eab18e62b46adb36930123791b44a`,
`cf293931ea0546a4b3738697f92937fb`, `e369ab269a0a46719bec93a7d3116960`
(3 records each), plus bundle batch `016792cc000742299dcd8ab23b99bb8b`
(25 records).
Counts by kind (from the exported files, not estimates): 8 artifacts,
8 sources, 10 observations (8 web.capture + 2 infra.ioc), 1 run,
22 claims. Total 49 records.
Export note: 5 capture batches were first exported by a sibling
worker's export run (about 01:36 UTC); the remaining 3 capture batches
and the bundle batch were exported by this ingest's own export run
(02:41 UTC). Only this lane's own batch dirs are committed here.
`verify --blobs` after export: ok=true, verified=true, 730 blob
hashes verified corpus-wide, pending=0, records=208335.

- Captures: 8, each artifact + source + web.capture observation,
  submitted with `--tags '{"lane":"crabmail-ai"}'`.
  TOOLKIT NOTE (verified in `skills/factum/scripts/factum_lib/cli.py`,
  function `capture`): in installed Factum 0.2.0 the `--tags` value is
  applied to the observation record only. The artifact and source
  records carry `factum.author` (agent:lane-ingest-crabmail-ai) but no
  lane tag. Lane attribution for each triple still holds through the
  observation's `tags.lane` plus its `files[]` and `source` links.
  The AGENTS.md note that all three carry the tag does not match this
  version's code. A bulk retag would need one `factum update` write
  per record and was not done; flagged as an open item for the parent.
  One capture (descriptor-api) was recovered from its durable pending
  file after the first chain run's background session died; see
  `capture-logs/descriptor-api.RECOVERED.txt`. No duplicate was
  submitted for it.
- Bundle `bundle-crabmail.json`: 1 run, 2 infra.ioc observations,
  22 claims.
- Tables created: NONE NEEDED. Existing types used: web.capture (via
  capture), infra.ioc (host terms crabmail.ai and api.crabmail.ai),
  claim (factum-core), run (lane_ingest). Why no new type: the
  agent-messaging descriptor lives verbatim in the captured descriptor
  artifacts and in full in the descriptor claim value; a new
  messaging-descriptor type would duplicate that evidence and would
  need a schema-pack install plus schema-lock changes outside this
  lane's commit scope. If the parent wants a reusable descriptor type,
  that is a separate pack proposal (see open items).

## Behaviors extracted (names only, grades in claims)

- Addressed direct messages (request, response, notification, handoff)
  — docs and spec.
- Replies and threads via in_reply_to — docs and spec.
- Relay queue with polling (7-day wait) — docs and spec; local queue,
  not federation.
- Push delivery: WebSocket first, then webhook — doc only, self-reported
  timing, no live push observed.
- Webhook registration per agent — doc only.
- Address resolution to another agent public key — spec path, needs an
  agent key, not probed.
- Read receipts — spec path, doc only.
- Cross-provider federation — doc only, plus INFERENCE-only flow claim.
- Skill and slash-command pack for one agent family — bytes only, not
  run.
- Trust labels that shape action (Verified, External, Untrusted) —
  doc only, wrapping never tested, home-vs-doc label conflict recorded.
- No intel.behavior record was created: no taxonomy category fits these
  surface affordances without inventing a category, and inventing one
  needs a taxonomy-doc update outside this ingest's commit scope.
  The affordances are carried as graded claims instead.

## Killed claims excluded (adversarial review, binding)

- C21: fingerprint verifies the provider key — killed. Recompute
  fails for both raw key bytes and hex text; hashed input is
  unstated. Ingested instead: key and fingerprint as two separate
  published values with no verified link, plus the failed-recompute
  note. No "fingerprint matches key" claim exists in this lane.
- C22: relay and federation are one path, or relay explains
  federation — killed. Relay (local queue, GET /v1/messages/pending)
  and federation (cross-provider, POST /v1/federation/deliver) are
  ingested as separate items. The spec's "relay-only provider"
  wording is recorded as a spec tension.
- C23: pending-ack call shape is settled — killed. Ingested as an
  unresolved mismatch: docs POST /v1/messages/pending/ack (batch)
  versus spec DELETE /v1/messages/pending/{id} as acknowledge.
- C24: webhooks and WebSockets are live endpoints — killed. They
  appear only as capability strings; no spec path exists. Ingested
  only as capability strings, never as live endpoints.
- C25: any NEW, first-seen, or undiscovered wording — killed. No such
  wording is in any submitted record.

## Demoted claims ingested as demoted

C9 (agents_online 2 quoted as an undefined field at one time, not two
agents), C10 (healthy at probe time; uptime about 20 hours implies a
recent start, not long-lived history), C11 (2026-10-23 federation test
as a vendor self-report with an unnamed peer running vendor software),
C12 (trust levels and wrapping as docs only, with the home-vs-doc label
conflict), C13 (signature coverage as docs only, no signed message
observed or checked), C14 (push timing as docs only, self-reported),
C15 (relay limits as docs only; info confirms only 60/min and 100/min),
C16 (human gate as docs and marketing only; app pages not fetched;
spec has no tenant path), C17 (federation flow as INFERENCE only),
C18 (provider-key federation role as INFERENCE only), C19 (skill pack
as bytes only, not run), C20 (descriptor-source claim narrowed to
byte-identity with the live API-host copy). Each claim value states
its limit in plain words.

## Gated surfaces (not fetched, not probed with auth)

- POST /v1/register — needs a user key. Not attempted.
- POST /v1/route — needs an agent API key. Not attempted.
- GET /v1/agents/me, PATCH, DELETE — need an agent API key.
- GET /v1/agents, GET /v1/agents/resolve/{address} — need an agent key.
- GET /v1/messages/pending, POST /v1/messages/pending/ack,
  DELETE /v1/messages/pending/{id}, POST /v1/messages/{id}/read —
  need an agent API key.
- GET /v1/auth/user-key, GET /v1/tenants/available/{name},
  POST /v1/tenants — need a signed-in human account.
- https://app.crabmail.ai/login/ and /register/ — human account pages.
  Not fetched. Out of scope.
- WebSocket push and webhook delivery — need a registered agent.
  Unobserved live.
- GET /v1/federation/deliver returned 404 with the generic not_found
  body. The spec lists the path as POST only. This is NOT death.
  POST was not tested, by scope.

## Wall boundary outcome

No Wall exists for Crabmail. The boundary statement is: public versus
credentialed surfaces were handled honestly. Health, info, OpenAPI,
descriptors, and docs were fetched without auth. All agent-key paths
were listed, not probed with auth. App login and register pages were
not fetched.
What remains unobserved and why: live federation traffic (POST out of
scope; no delivery attempted; no second provider probed); federation
request shape and signing rule (spec lists the path and POST only, no
body schema in the captured bytes); any live agent address, public key,
or message (need an agent key or a known address; the public site lists
none); WebSocket and webhook behavior live (need a registered agent;
none was registered); the reason for the descriptor/info capability gap
(not stated in any captured file); the skill files in full use
(installer captured as bytes only, not run); blog and compare pages
beyond the index list (listed in llms.txt but not fetched; marketing
and comparison text, not API surface); app dashboard pages (login and
account pages out of scope by the no-login rule).

## Sensitivity

- No credential value, private key, live agent address, live agent
  public key, or live message was found.
- The provider public key and fingerprint are published values, not
  secrets. They do not block ingest. They carry the C21 note: the link
  between them is unverified. They are never ingested as credentials.
- Role addresses, public: support@crabmail.ai (descriptor contact),
  security@crabmail.ai (security.txt), hello@agentmessaging.org (AMP
  site contact). Published contact points. Not agent identities.
- Example addresses, not live agents: name@tenant.crabmail.ai,
  builder@yourteam.crabmail.ai, reviewer@yourteam.crabmail.ai,
  builder@23blocks.crabmail.ai. Doc placeholders. Not ingested as live
  agent addresses.
- One example address carries a first name:
  sebastian@23blocks.crabmail.ai, in developer docs. Doc example, not
  a live agent. It is NOT a human-identity record, and no follow-up
  identity work may be built on it. It is noted here only, or omitted
  from records.
- Format examples only, not real keys: the OpenAPI security scheme
  describes agent API keys as amp_live_sk_... and user keys as uk_xxx.
  Patterns with placeholders, not values. Not quoted as keys.

## Dedup and novelty (scope, not a NEW claim)

- Factum `match --text --mode exact`: not_found for crabmail.ai,
  AMP010, federation/deliver, api.theagora.one, serai.one, wall.post,
  serai-verbs, community.scan, road.letter, treasury.mint.
- Factum `match --url`: not_found for the crabmail descriptor and
  health URLs and the Serai Wall, verbs, and agent-card URLs.
- Factum fuzzy matches for these terms returned only short-string
  alignment noise (unrelated records); none was about crabmail.ai on
  inspection.
- `lists/urls/urls.jsonl`: 0 hits for crabmail or serai.
  `lists/words/wordlist.txt` already holds `crabmail.ai` (line 3856)
  and `serai.one` (line 3855) from the discovery wave; no wordlist
  change was made here.
- Transluce tracker via `tl.py findings` (returned page, ids 208-181):
  0 hits for crabmail, serai, theagora, agent-messaging. Local
  Transluce raw files and the transluce-intel lane: 0 hits.
  Legacy `evidence/` tree: 0 hits for crabmail.ai or serai.one.
- Caveat: the live tracker check covered the page `tl.py` returned
  (25 items); it is not a full-tracker census. No record in this lane
  uses NEW, first-seen, or undiscovered wording.

## Commit

- Commit hash: FILL (parent pushes and verifies).
- Pathspecs used: `data/lanes/crabmail-ai`,
  `data/records/<this lane's batch dirs>`, and this lane's new blobs
  under `data/blobs/` (explicit paths only).
- NOT pushed, per task. NOT included: `data/.local/factum.db`,
  sibling workers' files or batches, or any other lane's files.

## Open items for the parent

1. Reusable messaging-descriptor type: if a descriptor type is wanted
   for agent-messaging providers across lanes, that is a schema-pack
   proposal plus a taxonomy-doc update, outside this ingest's commit
   scope.
2. Health re-probe: a later re-probe of /v1/health and /v1/info is
   cheap and needs no auth. It can track growth and close the
   descriptor/info capability gap (registration missing from info).
3. Pending-ack shape: needs a doc or spec fix, or a live ack test
   (needs an agent key; out of scope here).
4. Fingerprint input: a stated fingerprint input that recomputes to
   the claimed value would revive a verified-link claim. Until then
   the link stays unverified.
5. Live federation, push, and trust-wrap tests all need a registered
   agent or a second provider; all out of scope unless authorized.
6. Transluce tracker census: the live check covered one returned page;
   a full-tracker search would close the novelty caveat above.
