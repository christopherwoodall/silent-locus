# Crabmail.ai scrape analysis

Date of scrape: 2026-10-24, 21:51-21:53 UTC.
Method: read-only GET with curl only. No POST. No login. No account.
No mail sent. No registration. No delivery attempt. No payload run.

## Terms used here

- AMP: Agent Messaging Protocol. An open rule set for agent messages.
- Agent: a software system that acts on its own to do tasks.
- Ed25519: a public-key signature method. A private key signs. A public key checks the sign.
- Federation: message flow between two different providers.
- Relay: a server that holds a message for a short time, then passes it on.
- Webhook: a web address that a service calls when a new event occurs.
- WebSocket: a long-lived link that lets a server push data at once.
- Tenant: a workspace. One human account owns one tenant name.
- Trust level: a label that says how much a recipient should trust a message.

## Descriptor source URL: found

Both descriptor URLs serve the same record. The values match the slot-0 capture exactly.

- https://api.crabmail.ai/.well-known/agent-messaging.json — 200, 412 bytes, compact JSON.
- https://crabmail.ai/.well-known/agent-messaging.json — 200, 512 bytes, same values, pretty JSON.

The slot-0 source URL is now resolved: it was served from both hosts. The API host copy is the live API copy. The root host copy is a static file on a content host. This is OBSERVED from response headers: the root copy names AmazonS3 and CloudFront, and it was last changed 2026-10-24T00:09:24Z.

Observed descriptor values (a published service descriptor, not a secret):

- version: AMP010
- endpoint: https://api.crabmail.ai/v1
- provider: crabmail.ai
- public_key: ef09ad73b59ed3acffb1085215fc70a0c28b2d7b5856403de81a91c17fa2727a
- fingerprint: SHA256:3B7TdLvjLmV45mzjq9NcknszAa5jCcNLW0BXZKv3nSs=
- capabilities: federation, webhooks, websockets, relay, registration
- federation_endpoint: https://api.crabmail.ai/v1/federation/deliver
- contact: support@crabmail.ai

## Endpoint coverage

Outcome words: captured means bytes saved. Gated means auth or a key is needed. POST-only means the spec lists only POST. Unresolved means GET alone cannot settle it.

| Endpoint | Status | Bytes | Outcome |
|---|---|---|---|
| https://api.crabmail.ai/.well-known/agent-messaging.json | 200 | 412 | Captured |
| https://crabmail.ai/.well-known/agent-messaging.json | 200 | 512 | Captured |
| https://api.crabmail.ai/v1 | 404 | 52 | Captured error body: not_found. No index at the API root. |
| https://api.crabmail.ai/v1/federation/deliver (GET probe) | 404 | 52 | POST-only per the OpenAPI spec. GET gives the same generic not_found body as the API root. Not dead. POST was not tested, by scope. |
| https://crabmail.ai/ | 200 | 59729 | Captured |
| https://crabmail.ai/index.md | 200 | 949 | Captured |
| https://crabmail.ai/llms.txt | 200 | 2675 | Captured |
| https://crabmail.ai/agents.md | 200 | 6624 | Captured |
| https://crabmail.ai/agents/ | 200 | 59972 | Captured |
| https://crabmail.ai/developers/ | 200 | 65905 | Captured |
| https://crabmail.ai/.well-known/security.txt | 200 | 189 | Captured |
| https://agentmessaging.org | 200 | 52442 | Captured |
| https://crabmail.ai/developers/index.md | 200 | 4886 | Captured |
| https://crabmail.ai/get-started/index.md | 200 | 1346 | Captured |
| https://api.crabmail.ai/v1/health | 200 | 122 | Captured, no auth |
| https://api.crabmail.ai/v1/info | 200 | 404 | Captured, no auth |
| https://api.crabmail.ai/v1/openapi.json | 200 | 3468 | Captured, no auth |
| https://crabmail.ai/install-skill.sh | 200 | 2428 | Captured as bytes only. Not run. Not installed. |

Total: 18 GET captures. 16 returned 200. 2 returned 404 with a saved error body.

Raw captures live here: `data/lanes/crabmail-ai/raw/2026-10-24T215128Z/`.
Each capture has a `.body` file, a `.headers` file, a `.body.PROVENANCE.txt` file, and a `.body.sha256` file.

## OBSERVED: live service state

- Health says: status healthy, version 0.1.0, federation true, agents_online 2, uptime 72697 seconds (about 20 hours).
- Info says: version amp/0.1, capabilities federation, webhooks, websockets, relay, registration_modes open, route URL https://api.crabmail.ai/v1/route.
- Info rate limits: 60 messages a minute, 100 API requests a minute, per agent.
- Two agents were online at probe time. This is a live service, not a dead demo page.

## OBSERVED: capability gap between descriptor and info

- The descriptor lists five capabilities. It includes registration.
- The info endpoint lists four capabilities. It drops registration.
- Info adds registration_modes: open. This is a small mismatch. It may mean registration is open in mode, but it is not listed as a live capability. The cause is unobserved.

## Trust model

### OBSERVED: two key layers

- Provider key: the descriptor holds one provider public key and one fingerprint. The API docs call the descriptor the discovery document with the provider public key. The provider key identifies the provider itself.
- Agent key: each agent makes its own Ed25519 key pair. The agent sends only its public key at registration. The private key stays with the agent. The provider stores only the public key. The provider cannot sign for an agent.

### OBSERVED: how a message is signed

- A signature covers: from, to, subject, priority, in_reply_to, and a hash of the payload.
- The payload hash is SHA-256 over JSON with keys sorted, then base64.
- The signature is base64 Ed25519 over those parts joined by the | character.
- A sender can look up another agent public key by address. The endpoint is GET /v1/agents/resolve/{address}. It needs an agent API key, so it was not probed.

### OBSERVED: three trust levels

- Verified: valid signature, same tenant. The message arrives as written.
- External: valid signature, other tenant or other provider. The message arrives wrapped in an external-content block, with a warning that the content is data, not instructions.
- Untrusted: missing or invalid signature. The message is still delivered, but it is wrapped the same way, with a warning.

### INFERENCE: what the provider key plausibly authenticates

- The provider key plausibly authenticates the provider in federation. A receiving provider could check that a deliver request truly came from the named provider.
- This is INFERENCE, not OBSERVED. No captured file states the federation signing rule. The federation request shape is unobserved.
- The agent key clearly authenticates the agent sender. The provider key clearly identifies the provider in discovery. The link between the two in federation is not stated in the captured bytes.

### OBSERVED: human gate on registration

- A human creates the account first, with an email code. No password is used.
- The human claims a tenant name first. The first claim wins.
- The human gives the agent a user key. The agent then registers itself.
- An agent cannot sign up or pay on its own. This is stated in the docs.
- Free plan allows 1 agent. Paid plans are not open for purchase yet.

### INFERENCE: what registration implies, versus what is observed

- Registration implies a self-serve agent address: name@tenant.crabmail.ai.
- What is observed is stronger than a mere address list. Registration also binds a public key, a delivery choice, and an API key to that address.
- What is NOT observed: any live agent address, any live public key, any live message. No agent directory is public. Resolve needs an agent key. So the trust graph is real in design, but empty in public view.

## Federation shape

### OBSERVED

- Federation is a named capability in both the descriptor and the info endpoint.
- The federation endpoint is https://api.crabmail.ai/v1/federation/deliver. The OpenAPI spec lists it as POST only.
- The docs state a 502 delivery_failed error when the recipient provider cannot be found or reached.
- The docs state a live test on 2026-10-23: delivery to and from a second provider on a separate host, in both directions.
- The provider home page repeats that test claim.
- A message address uses the provider domain: name@tenant.crabmail.ai. A cross-provider address would use the other provider domain. The exact cross-provider address form is not shown in the captured bytes.

### INFERENCE

- Federation plausibly works like this: a sender provider routes a message to the recipient provider deliver endpoint, and the recipient provider then delivers it to its local agent.
- The relay queue likely still applies on the far side. A message that cannot push at once would wait there.
- This flow is INFERENCE. No federation request or response was observed. No second provider was probed. POST was out of scope.

## Coordination affordances

These are the top affordances for agent-to-agent coordination. All are OBSERVED in the docs or the spec, unless marked.

1. Addressed direct messages. Any agent can send to any address. A send has to, subject, priority, and payload. Payload types are: request, response, notification, handoff. Handoff is the task-pass type. It lets one agent hand work to another.
2. Replies and threads. A message can set in_reply_to to an earlier message id. This builds a thread. Threads let agents hold a multi-step task talk.
3. Relay queue with polling. GET /v1/messages/pending lists waiting messages. Ack removes them. Undelivered messages wait up to 7 days. A slow or offline agent still gets its mail. This is store-and-forward coordination.
4. Push delivery: WebSocket first, then webhook. A connected agent got a message about 70 ms after send, per the docs. A webhook gets one attempt while the sender waits, plus two more in the background. Push lets agents react at once, not just on poll.
5. Webhook registration per agent. At registration, an agent can set a webhook URL for delivery. This lets an agent run a live inbox on its own server.
6. Address resolution. GET /v1/agents/resolve/{address} returns another agent public key. This lets a sender check a signature before it trusts a reply.
7. Read receipts. POST /v1/messages/{id}/read sends a read receipt to the sender. This lets a sender know a message was seen.
8. Cross-provider federation. See the federation shape above. This lets agents on different providers talk. It is the widest coordination affordance, and the least observed.
9. Skill and slash-command pack for one agent family. The site ships install files and command files for Claude Code: register, send, inbox, read. This lowers the cost for that agent family to join. The files were captured as bytes only and were not run.
10. Trust labels that shape action. Verified same-tenant mail arrives unwrapped. External and untrusted mail arrives wrapped with a warning. This label system is itself a coordination control: it tells a recipient when to treat text as data, not as an order.

## Gated surfaces

Gated means a key, a login, or a human account is needed. None were probed with auth. None were bypassed.

- POST /v1/register — needs a user key. Not attempted.
- POST /v1/route — needs an agent API key. Not attempted.
- GET /v1/agents/me, PATCH /v1/agents/me, DELETE /v1/agents/me — need an agent API key.
- GET /v1/agents, GET /v1/agents/resolve/{address} — need an agent API key.
- GET /v1/messages/pending, POST /v1/messages/pending/ack, DELETE /v1/messages/pending/{id}, POST /v1/messages/{id}/read — need an agent API key.
- GET /v1/auth/user-key, GET /v1/tenants/available/{name}, POST /v1/tenants — need a signed-in human account.
- https://app.crabmail.ai/login/ and https://app.crabmail.ai/register/ — human account pages. Not fetched. Out of scope.
- WebSocket push and webhook delivery — need a registered agent. Unobserved live.

## Message limits (OBSERVED)

- Subject: 256 characters max.
- Message body: 64 KB max.
- Context field: 256 KB max.
- Total message: 512 KB max.
- Send rate: 60 messages a minute, 500 an hour, per agent.
- API rate: 100 requests a minute.
- Relay life: 7 days. A sender-set expiry is not enforced. The relay expiry is queued time plus 7 days.
- Envelope time skew is logged, not rejected, at this time: more than 60 seconds ahead, or more than 5 minutes old. Rejection is planned later.

## What remains unobserved, and why

- Live federation traffic. POST was out of scope. No delivery was attempted. No second provider was probed.
- The federation request shape and signing rule. The OpenAPI spec lists the path and POST only. It gives no body schema for it in the captured bytes.
- Any live agent address, public key, or message. Those need an agent key or a known address. The public site lists none.
- WebSocket and webhook behavior live. Those need a registered agent. None was registered.
- The reason for the descriptor/info capability gap on registration. The cause is not stated in any captured file.
- The skill files in full use. The installer and its skill files were captured as bytes only. They were not run, so their run-time behavior is unobserved.
- Blog and compare pages beyond the index list. They were listed in llms.txt but not fetched. They are marketing and comparison text, not API surface. They were left out to keep the scrape to the API and agent docs.
- App dashboard pages. Login and account pages were out of scope by the no-login rule.

## Notes for the ingest executor

- Do not ingest the provider public key or fingerprint as a credential. They are published descriptor values.
- The descriptor source URL is now known: both https://api.crabmail.ai/.well-known/agent-messaging.json and https://crabmail.ai/.well-known/agent-messaging.json serve it. Prefer the API host copy as the live copy.
- The health endpoint gives a live agent count. A later re-probe of /v1/health and /v1/info is cheap and needs no auth. It can track growth.
- Do not mark the federation endpoint as dead. GET 404 on a POST-only path is not death. The spec confirms POST.
- Do not mark registration as dead either. The info endpoint drops it from capabilities, but the spec and docs still list POST /v1/register. The gap is a mismatch to watch, not a removal proof.
