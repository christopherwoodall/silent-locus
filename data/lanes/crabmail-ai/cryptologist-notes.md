# Cryptologist notes: crabmail.ai

## Scope

This note covers trust only. Trust means: who must be believed, and what stops misuse.

Source: `crabmail-agent-messaging.json` (AMP010 descriptor).
Capture dir: `data/lanes/general-hunt/raw/0/2026-10-24T204043Z/`.
Grades: OBSERVED means the file states it, or the bytes show it. INFERENCE means this note concludes it.

Note on the key: the public key and fingerprint below are a published service descriptor. They are not a secret. This note analyzes them as a trust anchor. A trust anchor is a public value receivers use to check claims. This note never uses them as a credential, and it makes no live call to the service.

## Terms

- Public key: the public half of a key pair. Anyone may hold it. It checks signatures. It does not sign.
- Private key: the secret half of a key pair. Only the owner holds it. It signs.
- Ed25519: a signature scheme. Its public keys are 32 bytes long.
- Fingerprint: a short digest (a fixed-size hash) of a key. Receivers compare it to confirm they hold the same key.
- SHA-256: a hash function. Its output is 32 bytes long.
- Key pinning: a receiver stores an expected key or fingerprint, and rejects any other key.
- Federated delivery: delivery between separate providers. One provider sends a message to another provider's endpoint.

## Descriptor values (OBSERVED)

- Version: AMP010.
- Provider: crabmail.ai.
- Endpoint: `https://api.crabmail.ai/v1`.
- Federation endpoint: `https://api.crabmail.ai/v1/federation/deliver`.
- Public key (hex): `ef09ad73b59ed3acffb1085215fc70a0c28b2d7b5856403de81a91c17fa2727a`.
- Fingerprint: `SHA256:3B7TdLvjLmV45mzjq9NcknszAa5jCcNLW0BXZKv3nSs=`.
- Capabilities: federation, webhooks, websockets, relay, registration.
- Contact: support@crabmail.ai.

## Length check and format check (OBSERVED)

The public key string holds 64 hex characters. Each hex character holds 4 bits. 64 times 4 is 256 bits, which is 32 bytes. Every character is a lowercase hex digit (0-9, a-f). No other characters appear.

The fingerprint decodes from base64 to 32 bytes. That length matches a SHA-256 output.

## Is the key consistent with an Ed25519 public key?

OBSERVED: The key is 32 bytes long. Ed25519 public keys are 32 bytes long. The length matches.

INFERENCE: Length alone does not prove the scheme. A 32-byte value is also the size of an X25519 public key, and of a raw SHA-256 digest. The descriptor does not name a signature scheme. So the key is consistent with Ed25519 in size and in hex format, but Ed25519 is not confirmed. Any claim stronger than "size-consistent" would overstate the evidence.

INFERENCE: The fingerprint label says SHA256, and its decoded length is 32 bytes. That fits a SHA-256 digest of the key. But the descriptor does not state what bytes were hashed: the raw key bytes, the hex text, or some other form. The fingerprint match to the key is therefore not verified here. No cryptographic operation was run against the live service, per the task scope.

## What publishing a provider key and fingerprint enables

OBSERVED: The descriptor publishes one provider-level key and one fingerprint, next to a federation endpoint.

INFERENCE: Three uses follow, if signatures exist:

1. Signature verification of federated delivery. A receiver can check that a delivery truly came from the holder of the matching private key. This stops forgery by third parties.
2. Key pinning. A receiver stores this key or fingerprint, and rejects deliveries signed under any other key. This stops key-swap attacks.
3. Out-of-band key check. A receiver can compare a key seen in traffic against the published fingerprint, and detect a changed key.

INFERENCE: All three uses depend on a signature step that the descriptor does not describe. Publishing a key enables verification. It does not prove that deliveries are signed. A receiver that assumes signed delivery without a stated scheme may accept unsigned data.

## What is missing for a full trust assessment: open questions, not findings

1. Signature scheme: Is the scheme Ed25519, or another scheme? The descriptor does not name one.
2. Signed bytes: What exact bytes are signed? Headers, body, a delivery envelope, or a timestamped form? Without this, a receiver cannot build a check.
3. Signature transport: Where does a signature travel? A header, a body field, or a separate proof object? The descriptor does not state it.
4. Key scope: Is this one provider key for all traffic, or does each agent hold its own key? The descriptor shows one provider key. Per-agent keys are not shown, but their absence from one descriptor is not proof they do not exist.
5. Key rotation: How does a key change? Is there an overlap period, a new descriptor version, or a revocation notice? A pinned key with no rotation plan breaks or goes stale.
6. Revocation: How is a compromised key revoked? What must receivers do when it happens?
7. Descriptor trust: How does a receiver know this descriptor is genuine? The file itself carries no signature, and no fetch chain is shown.
8. Webhook and relay proofs: Do webhooks and relayed messages carry the same signature, or none? Capabilities list webhooks and relay, but no proof rule covers them.
9. Fingerprint input: What exact bytes feed the SHA-256 fingerprint? Raw key bytes or hex text? This must be known before a receiver can recompute it.
10. Clock and replay: Are deliveries timestamped? Can an old signed delivery be replayed? No nonce (one-use random value) or expiry rule is stated.

## Trust model in brief

Crabmail.ai publishes one provider public key and a SHA-256 fingerprint as a trust anchor for its federation endpoint.
A receiver that pins that key can, in principle, check that federated deliveries come from the key holder and reject key swaps.
But the descriptor states no signature scheme, no signed bytes, and no rotation or revocation rule, so no full verification path can be built from this file alone.

## Grade summary

OBSERVED: 64 hex characters, 32 bytes, all lowercase hex; fingerprint decodes to 32 bytes; one provider key; federation endpoint; five capabilities.

INFERENCE: size-consistent with Ed25519, not proven as Ed25519; fingerprint length fits SHA-256, but its hashed input is unstated; pinning and verification are enabled in principle, but depend on an undescribed signature step.

Nothing here is a verified mechanism. No live check was made. No signature was verified.
