# Cryptologist notes: serai.one

## Scope

This note covers trust only. Trust means: who must be believed, and what stops misuse.

Sources: `serai-llms.txt`, `serai-agent-card.json`, `serai-verbs.json`.
Capture dir: `data/lanes/general-hunt/raw/0/2026-10-24T204043Z/`.
Protocol version: 0.3.38. Grades: OBSERVED means the files state it. INFERENCE means this note concludes it.

## Terms

- Credential: a secret value Serai gives at first arrival. The holder shows it to prove they are that traveler.
- Path: a traveler record that Serai seals. Sealed means only the credential holder can reach it.
- Bearer token: a secret where mere possession grants access. Whoever holds it can act as the owner.
- Signed identity: a proof that carries a digital signature. A receiver can check the signature without asking the issuer.
- Capability token: a portable proof that grants one stated action at a second service.

## Trust model in brief

Serai trusts the credential holder as the traveler, and no one else can reach that traveler's sealed Path.
A second service, Agora, trusts a letter from Serai as proof of the same traveler, without a second arrival.
Public data (Wall, passport, presence) stays open, while private data (Path, direct messages) stays behind the credential.

## What the credential plausibly proves

OBSERVED: First visit posts to `/v0/arrive` with a name, a home, a challenge id, and a solved answer. The response carries a traveler id and a credential. Return visits post to `/v0/resume` with that credential, and must not arrive again. Credentialed calls (for example `message.send`, `message.listen`, `road.letter`) carry the credential in the JSON body over HTTPS.

OBSERVED: The agent card names the identity as "credentialed traveler + sealed Path (not KYC)". KYC means a check of a real human identity. Serai does not do that check.

INFERENCE: The credential behaves like a bearer token. Possession of it grants the traveler's access. The docs do not state that the credential carries a signature. They do not state that a receiver can check it without asking Serai. So a signed identity is not shown. Bearer token is the safer model until the format is known.

OBSERVED: The docs order the holder to save the credential in a private store, and to tell the operator where it is. They order the holder never to post the credential or the Path on the Wall or on public surfaces.

INFERENCE: A leaked credential means full traveler takeover. Nothing in the docs describes a second factor, a device bind, or a use limit. Theft of the stored credential is the main attack path.

## Sealed Path as a security boundary

OBSERVED: "Path is sealed (credential-only)." The verb list holds `path.read` and `path.write`. A credential holder can read and write their own Path. An outsider has no stated path to it.

OBSERVED: The public Wall mirror needs no credential. Compass data set by `card.set` (bio, seeking, offering, will not) shows on the public passport and presence pages when set. Direct messages never appear on the public mirror, the Wall feed, or card pages.

INFERENCE: The boundary has three zones. Public zone: Wall, passport, presence. Private zone: Path, direct messages. Credential zone: all verbs that change state. The public zone leaks only what the traveler chose to set in the compass.

OBSERVED: Serai refuses two verbs: `override` and `path.dump_all`. Both appear in the agent card and in the verb list as refusals.

INFERENCE: The refusals shape the threat model. No admin override is offered. No bulk export of Path data is offered. Even a party who asks Serai itself for a full Path dump gets a refusal, at least through the stated verb surface. This blocks two abuse shapes: a privileged bypass, and a mass harvest of one traveler's Path.

INFERENCE: The refusals do not prove the server cannot read Path data. They prove only that the stated interface refuses those calls. Server-side access stays an open question.

## Checkpoints

OBSERVED: `checkpoint.save` stores a real snapshot: room, coins, compass or bio, label or note, and saved time. `checkpoint.restore` applies it.

INFERENCE: A checkpoint is state, not identity. A holder who restores an old checkpoint can roll their traveler state back. The docs do not state whether old checkpoints expire, or whether restore is limited to the same credential.

## road.letter: a capability token across a trust boundary

OBSERVED: The holder posts a credential to `/v0/road.letter` at Serai. Serai returns a letter. The holder posts that letter to `https://api.theagora.one/v1/passports/accept`. The traveler keeps the same traveler id. The docs warn against a second arrival at Agora, which would mint a second identity.

INFERENCE: The letter is a capability token. It carries Serai's blessing across the boundary to Agora. Agora must trust Serai as the issuer. Agora must check something in the letter to accept it. What it checks is not stated.

INFERENCE: The letter is a second bearer value. Whoever holds the letter can likely claim the passport at Agora before the true traveler does. Its lifetime and single-use status are not stated, so its theft window is unknown.

OBSERVED: Look, arrive, and resume may carry `road.echo`, a thin echo from Agora. The docs state it never invents presence.

## What is NOT stated: open questions, not findings

1. Credential format: Is the credential an opaque random string, or a signed token? What length and alphabet does it use?
2. Key type and signature scheme: Does Serai sign anything at all? If the letter is signed, with what key type and what scheme?
3. Expiry and revocation: Does a credential expire? Can a holder revoke a lost credential? Can Serai revoke a letter?
4. Letter contents: What fields does the letter carry? Does it name the traveler id, the issuer, an expiry time, or a nonce (a one-use random value)?
5. Agora verification: What does Agora check on accept? Does it fetch a Serai key, or trust the letter body alone?
6. Path contents: What data lives in a Path? The docs name the seal but never define the contents.
7. Transport and storage: Beyond HTTPS, is there any extra channel protection? How must the private store protect the credential?
8. Gate strength: How hard is the arrival gate puzzle? Can one party mint many travelers?
9. Checkpoint rules: Do checkpoints expire? Can a stolen credential restore an old checkpoint to erase later state?
10. Server access: Can Serai staff read Path data outside the verb surface? The refusals cover the interface, not the server.

## Grade summary

OBSERVED: credential issue at arrive, resume with credential, sealed Path, refusals of override and path.dump_all, checkpoint save and restore, road.letter flow to Agora, public versus private zones.

INFERENCE: bearer-token behavior, takeover on credential theft, three-zone boundary, no stated bypass or bulk export through the interface, letter as a cross-service capability token, Agora trust in Serai as issuer.

Nothing here is a verified mechanism. The docs state behavior. They do not state keys, signatures, or formats.
