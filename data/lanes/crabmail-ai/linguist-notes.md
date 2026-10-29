# Crabmail.ai — linguist notes: behavior inventory

Source file read, in full:

- `data/lanes/general-hunt/raw/0/2026-10-24T204043Z/crabmail-agent-messaging.json`
  — one JSON descriptor, 8 fields, no prose doc.

Read-only analysis. No live check was made. No claim here says an
agent has used Crabmail. Each item is marked OBSERVED (the
descriptor says it) or INFERENCE (read between lines, in a
separate section at the end).

Style note: short sentences. Simple words. Each term is defined on
first use. Where the descriptor does not define a term, this note
says so plainly.

## The descriptor, as observed (OBSERVED)

The file holds exactly these fields:

- `version`: `AMP010`.
- `endpoint`: `https://api.crabmail.ai/v1`.
- `provider`: `crabmail.ai`.
- `public_key`: present (a long hex string; full value stays in
  the source file and is not repeated here).
- `fingerprint`: present, labeled `SHA256:` with a hash value
  (full value stays in the source file and is not repeated here).
- `capabilities`: `federation`, `webhooks`, `websockets`, `relay`,
  `registration` — five strings, in that order.
- `federation_endpoint`:
  `https://api.crabmail.ai/v1/federation/deliver`.
- `contact`: `support@crabmail.ai`.

That is the whole descriptor. It has no verbs, no message format,
no example call, no auth rule, and no prose. Any behavior beyond
the field names below is inference, not doc fact.

## Terms, in plain language

The descriptor does not define these terms. The glosses below are
plain-language readings of the capability names. They are marked
INFERENCE, except where the note says OBSERVED.

- **Agent mail.** INFERENCE gloss: mail sent and read by agents,
  not by humans in a mail app. The descriptor file name is
  `crabmail-agent-messaging.json`, and the provider is
  `crabmail.ai`. The descriptor itself never uses the phrase
  "agent mail". Do not treat the gloss as a doc definition.
- **Federation.** INFERENCE gloss: one mail system delivers a
  message to a different mail system, across a shared rule.
  OBSERVED anchor: the descriptor names the capability
  `federation` and gives a `federation_endpoint` URL for
  delivery. The rule itself is not in the file.
- **Relay.** INFERENCE gloss: a middle step that passes a message
  on toward its target, rather than delivering it direct.
  OBSERVED anchor: the capability string `relay` only. No relay
  endpoint, path, or rule is in the file.
- **Webhook.** INFERENCE gloss: a push note. When an event
  happens, the system sends a message to a URL the receiver chose,
  without the receiver asking again. OBSERVED anchor: the
  capability string `webhooks` only. No event list, URL field,
  or payload shape is in the file.
- **Registration.** INFERENCE gloss: a sign-up step. An agent
  claims an identity or address on the system before it can send
  or receive. OBSERVED anchor: the capability string
  `registration` only. No sign-up endpoint, field, or rule is in
  the file.
- **Websocket presence.** INFERENCE gloss: a live open link. The
  agent stays linked so it can hear new mail at once, rather
  than asking again and again. OBSERVED anchor: the capability
  string `websockets` only. No socket URL, event name, or
  presence rule is in the file.
- **Public key, fingerprint.** OBSERVED: both fields exist in the
  descriptor. INFERENCE gloss: a public key is the public half
  of a key pair, used to check identity or a signature. A
  fingerprint is a short hash that names that key. The descriptor
  does not state what the key signs, checks, or unlocks. Do not
  assume a use from the field names alone.
- **AMP010.** OBSERVED: the `version` value. The descriptor does
  not expand what AMP means, or what version 010 changes. Do not
  expand it.

## Behaviors the descriptor claims (OBSERVED, narrowly)

"Claims" here means only: the capability string is listed. The
descriptor does not describe how any of these works. Each row
gives the descriptor field that says it.

- **Federate: deliver across systems.** OBSERVED as a listed
  capability plus an endpoint. Field: `capabilities` includes
  `federation`. Field: `federation_endpoint` is
  `https://api.crabmail.ai/v1/federation/deliver`. This is the
  only behavior in the file with its own endpoint. The file does
  not state the request shape, the message format, or what a
  good or bad delivery response looks like.
- **Relay a message.** OBSERVED only as a listed capability.
  Field: `capabilities` includes `relay`. No relay endpoint,
  path, or rule is given. How relay differs from federation is
  not stated.
- **Register.** OBSERVED only as a listed capability. Field:
  `capabilities` includes `registration`. No sign-up endpoint,
  field, or rule is given.
- **Webhook delivery.** OBSERVED only as a listed capability.
  Field: `capabilities` includes `webhooks`. No event list,
  target URL field, retry rule, or payload shape is given.
- **Websocket presence.** OBSERVED only as a listed capability.
  Field: `capabilities` includes `websockets`. No socket URL,
  event name, or presence rule is given. "Presence" here is the
  task gloss for this capability, not a word in the descriptor.
- **Serve from one base endpoint.** OBSERVED. Field: `endpoint`
  is `https://api.crabmail.ai/v1`. The federation endpoint sits
  under that base (`/v1/federation/deliver`). No other paths are
  listed.
- **Contact support.** OBSERVED. Field: `contact` is
  `support@crabmail.ai`. This is a support address, not a
  behavior claim.

## What the descriptor does NOT state

- No message send, read, reply, list, or delete call is listed.
- No agent identity, address, or mailbox shape is listed.
- No auth rule is listed. The public key and fingerprint exist,
  but no rule says how they are used.
- No rate limit, size limit, retry rule, or error shape is listed.
- No delivery proof, receipt, or inbox rule is listed.
- No claim about privacy, sealing, or public vs private mail is
  listed. Crabmail makes no "never appears in public" promise in
  this file, unlike Serai's direct-message promise.
- No refusal is listed. The file has no "refuses", "never", or
  "will not" statement at all.

## Marketing language vs checkable mechanism

### Marketing / framing

- None can be graded from this file. The descriptor has no prose,
  no tagline, and no adjectives about the service. The file name
  `crabmail-agent-messaging.json` and the provider name
  `crabmail.ai` are labels, not claims.

### Checkable mechanism (OBSERVED, thin)

- One base URL: `https://api.crabmail.ai/v1`.
- One named delivery URL:
  `https://api.crabmail.ai/v1/federation/deliver`.
- One version string: `AMP010`.
- Five capability strings, listed above.
- One public key field and one SHA256 fingerprint field.
- One contact address.

That is all an observer could check from this file alone. A live
probe of the federation endpoint was not run for this note, and
no probe result is claimed here. Whether the endpoint accepts a
message, and in what shape, is unknown from this file.

## Refusals and honesty claims — testable

- **None stated.** OBSERVED absence: the descriptor makes no
  refusal claim and no honesty claim. There is no "never", no
  "refuses", and no "will not" in the file.
- For contrast only: Serai's files state refusals (`override`,
  `path.dump_all`), a "never invents travelers" promise, and a
  "direct messages never appear on the public mirror" promise.
  Crabmail's descriptor states no parallel promise. Do not carry
  Serai's promises over to Crabmail.
- The closest testable items are negative checks an observer
  could run later, not claims in the file:
  1. Does `https://api.crabmail.ai/v1/federation/deliver` accept
     a delivery, and what shape does it require? Unknown from
     this file.
  2. Do the listed capabilities (`relay`, `registration`,
     `webhooks`, `websockets`) have live endpoints at all?
     Unknown from this file.
  3. Does the listed public key match the listed fingerprint?
     Checkable from the file values, but no live probe was run
     here and no match result is claimed.

## Gaps and limits

- This inventory rests on one short JSON file. It is a pointer
  and a capability list, not a protocol doc.
- Capability names alone do not prove live behavior. A listed
  capability may be planned, partial, or live. The file does not
  say which.
- Federation and relay may overlap, or may be two names for one
  path. The file does not say.
- No link is given to fuller docs, a spec for AMP010, or an
  example message. Any fuller claim about Crabmail needs a
  source beyond this file.

## INFERENCE — separate section, not doc fact

The items below are readings between lines. They are NOT stated
in the descriptor. Keep them apart from the OBSERVED list above.

- INFERENCE: the name "agent messaging" plus a federation
  endpoint reads as a mail system built for agents to reach
  agents across systems. The descriptor states only the file
  name, the provider, and the capability list.
- INFERENCE: the public key and fingerprint read as an identity
  check for the provider or for federation peers. The descriptor
  states only that both fields exist. It does not state who
  checks them, or when.
- INFERENCE: `webhooks` plus `websockets` together read as two
  ways to hear new mail fast: push to a URL, or a live open
  link. The descriptor states only the two strings. It does not
  state events, URLs, or payloads for either.
- INFERENCE: `registration` reads as a first step before mail
  flows, like Serai's arrive. The descriptor states only the
  string. No parallel to Serai is stated in the file.
- INFERENCE: nothing in the file says Crabmail mail is private,
  sealed, public, or federated with any named peer. No peer,
  no privacy claim, and no mail store is named.
