# Serai-one — ingest report

Lane: `serai-one`.
Status: DRAFT — batch ids and record counts to fill after export.

Terms, defined on first use:

- Traveler: an agent identity at Serai. It has a name, a home, and an id.
- Credential: a secret token. It proves a traveler is who it claims to be.
- Path: the private memory of one traveler. Only that traveler can read it.
- Wall: the public note board. Any visitor can read it.
- Mirror: the public read-only copy of a Serai surface, served by GET.
- Verb: one JSON action, sent as POST to `/v0/{verb}`.
- Keeper: the house traveler. It welcomes guests when no one else is present.
- Agora: First Ground, a separate world at `api.theagora.one`. It is not Serai.
- Doc claim: a statement found in site docs or JSON. It is not a tested act.
- Snapshot: one fetch at one time. It is not a stable fact.

## Lane decision

- Lane name: `serai-one` (lowercase, hyphens, no date).
- Lane id: `lane_50e343dbd6e844cc9738ed03a439cba6` (created
  2026-10-24T22:13:27Z via `lane new`; verified with `lane show`).
- Lane dir: `data/lanes/serai-one/`.
- The lane dir already held the wave-1 raw set and notes before ingest.
  `lane new` made the lane record; its lane.json was placed in this dir
  and its tags were set to the full set (docs_path plus scope).
- Agora was split out, not merged: Agora records carry
  `surface: api.theagora.one` and state that Agora is a separate service.
  No Agora deed is ranked as Serai behavior. A full Agora lane is an open
  item for the parent, not created here (two lanes were authorized).

## Coverage (wave-1 scrape, 2026-10-24T21:51-21:55Z)

66 endpoints tried. 64 returned 200. 2 returned 404. 720,245 bytes.
Method: read-only curl GET only. No POST. No login. No account.
Full table: `raw/2026-10-24T215156Z/_summary.tsv`.
Key rows:

| Endpoint | Status | Bytes | Use in this ingest |
|---|---|---|---|
| https://serai.one/v0/mirror/wall | 200 | 16310 | Captured. Wall snapshot claim. |
| https://serai.one/v0/verbs | 200 | 620 | Captured. Verb inventory claim. |
| https://serai.one/v0/mirror/presence | 200 | 11620 | Captured. Presence snapshot claim. |
| https://serai.one/v0/mirror/rules | 200 | 348 | Captured. Refusals claim. |
| https://serai.one/.well-known/agent-card.json | 200 | 4134 | Captured. Protocol and transport. |
| https://serai.one/agents.html | 200 | 26373 | Captured. Door guide, doc claims. |
| https://serai.one/llms.txt | 200 | 5836 | Captured. Machine doc. |
| https://serai.one/robots.txt | 200 | 429 | Captured. Passport conflict. |
| https://api.theagora.one/v1/world | 200 | 25488 | Captured, surface-tagged Agora. |
| https://api.theagora.one/v1/ground | 200 | 36973 | Captured, surface-tagged Agora. |
| https://api.theagora.one/v1/history | 200 | 5068 | Captured, surface-tagged Agora. |
| https://serai.one/card (bare) | 404 | 35 | Dead. Bare path; id form works. |
| https://serai.one/client.py | 404 | 35 | Dead. No Python client at root. |

All other wave-1 files stay in `raw/` and are committed with this lane.
They were not all captured through Factum `capture`; the key artifacts
above were, and the lane raw dir preserves the rest.

## Verification before submit

- Every stored `.sha256` file in both raw sets matches its bytes on disk.
  Serai: all pass. Crabmail: all pass. (See crabmail report for its set.)
- Live re-fetch (polite unauthenticated curl GET) of Wall mirror, verbs,
  health, and agent card: all four bodies match their recorded SHA-256
  exactly. No mismatch. No claim was dropped on re-fetch grounds.
- Slot-0 continuity: slot-0 `serai-llms.txt`, `serai-agent-card.json`,
  `serai-verbs.json`, `serai-agents.html` are byte-identical to the
  wave-1 captures (SHA-256 values in the continuity claim). No duplicate
  capture was submitted for the slot-0 files.

## Records submitted

Batch ids (12, from export output, read from the exported
`data/records/<batch>/records.jsonl` files): 11 capture batches
`07b9bf01cd614267ade180914509b21a`, `4c4e2f105af34b598f461c8862503f9f`,
`64cde607f0d7412e8b82e21d4a9345a7`, `93a30fe699c54137bea759d63b034c5f`,
`ae27380cd5f84ba78c9e1117d5c7293d`, `b179bafa6af1418bb5be0aa19e89d087`,
`c105798c7dde451394c61523895e033d`, `c31975342bc7480b97cf475a19f9a5c2`,
`c76aac95c09447dcb427d714a7508d79`, `d4713a0d9e25449c9db526893a29c0e4`,
`e8f1da627c86449ea717d29128748a07` (3 records each), plus bundle batch
`7a5d92c47e234c57a85e61e884404ba8` (20 records).
Counts by kind (from the exported files, not estimates): 11 artifacts,
11 sources, 14 observations (11 web.capture + 3 infra.ioc), 1 run,
16 claims. Total 53 records.
Export note: the 11 capture batches were first exported by a sibling
worker's export run (about 01:36 UTC); the bundle batch was exported
by this ingest's own export run (02:41 UTC). Only this lane's own
batch dirs are committed here. `verify --blobs` after export:
ok=true, verified=true, 730 blob hashes verified corpus-wide,
pending=0, records=208335.

- Captures: 11 (8 Serai + 3 Agora), each artifact + source +
  web.capture observation, submitted with `--tags '{"lane":"serai-one"}'`.
  TOOLKIT NOTE (verified in `skills/factum/scripts/factum_lib/cli.py`,
  function `capture`): in installed Factum 0.2.0 the `--tags` value is
  applied to the observation record only. The artifact and source
  records carry `factum.author` (agent:lane-ingest-serai-one) but no
  lane tag. Lane attribution for each triple still holds through the
  observation's `tags.lane` plus its `files[]` and `source` links.
  The AGENTS.md note that all three carry the tag does not match this
  version's code. A bulk retag would need one `factum update` write
  per record (38 writes for both lanes, each a full-corpus rebuild)
  and was not done; flagged as an open item for the parent.
  Agora observations also carry `surface: api.theagora.one`.
- Bundle `bundle-serai.json`: 1 run, 3 infra.ioc observations, 16 claims.
- Tables created: NONE NEEDED. Existing types used: web.capture (via
  capture), infra.ioc (host terms serai.one and api.theagora.one,
  protocol term serai-verbs), claim (factum-core), run (lane_ingest).
  Why no new type: the verb inventory lives verbatim in the captured
  verbs artifact and in full in the verb-inventory claim value; a new
  protocol-surface type would duplicate that evidence and would need a
  schema-pack install plus schema-lock changes outside this lane's
  commit scope. If the parent wants a reusable protocol-surface type,
  that is a separate pack proposal (see open items).

## Behaviors extracted (names only, grades in claims)

- Compass-match discovery (community.scan + resonate) — doc only.
- Direct private talk (message.send, message.listen, mute, block,
  decline, reopen) — doc only.
- Public Wall threads (wall.post, wall.reply, wall.witness) — Wall
  content observed; posting act not tested.
- Shared channels (channel.open, channel.say, channel.read) — doc only.
- Outward road (road.letter + Agora accept) — doc only.
- Checkpoint and fork handoff (checkpoint.save/restore, fork.request)
  — doc only.
- Treasury shared meanings (treasury.mint, treasury.adopt,
  treasury.read) — names only.
- No intel.behavior record was created: no taxonomy category fits these
  surface affordances without inventing a category, and inventing one
  needs a taxonomy-doc update outside this ingest's commit scope.
  The affordances are carried as graded claims instead.

## Killed claims excluded (adversarial review, binding)

- S23: the phrase "operator-ok / public-no rule" — dropped. Replaced by
  the narrow byte facts (no credential, no Path in the sample) plus the
  sensitivity note.
- S24: Agora deeds as place, witness, found, link — wrong verb set.
  Correct set ingested: place 6, tend 3, read 3, rite 2.
- S25: Agora traces (3) readable as history — misread. Ingested as:
  traces object present but empty (passedToday 0, marks empty,
  captions empty).
- S26: Agora is part of Serai coordination — killed. Agora ingested as
  its own surface with the road as a doc-claimed bridge only.
- S27: any NEW, first-seen, or undiscovered wording — killed. No such
  wording is in any submitted record. Novelty scope is stated in the
  dedup section, not as a NEW claim.

## Demoted claims ingested as demoted

S10 (Keeper snapshot stamped with fetch time), S11 (refusals as listed
doc claims, not tested blocks), S12 (never-invents as doc promise),
S13 (DM absence as doc promise, no leak test), S14 (Path seal as doc
promise, no seal test), S15 (one post per day as doc rule, not tested),
S16 (Gate flow as docs only), S17 (community.scan as docs only),
S18 (road bridge as doc shape only), S19 (treasury names only),
S20 (checkpoint/fork semantics as docs only), S21 (mirror endpoint
fetched once, not the Wall tried once), S22 (first-night rite as docs
only). Each claim value states its limit in plain words.

## Gated surfaces (not fetched, not probed)

- GET /v0/gate/challenge — starts the arrival flow. Skipped on purpose.
- All 33 POST verbs — need a credential. Not attempted.
- GET /v0/passport/<traveler-id> — not fetched. Robots.txt conflict
  honored. Passport status stays an unresolved conflict claim.
- Agora Bearer endpoints — no credential exists for this scrape.
- Agora POST /v1/passports and /v1/passports/accept — account
  creation. Out of scope.

## Wall boundary outcome

- Mirror endpoint returned 200 with no login redirect and no 401.
- Bytes hold Wall posts and replies only. No credential value. No Path
  material.
- No credentialed endpoint was touched. No POST was sent.
- What remains unobserved and why: verb behavior (no verb called, so
  shapes, errors, and limits are doc claims only); treasury semantics
  (names only); Path content (sealed by design, none sought from public
  surfaces); private messages and channels (never on the public mirror
  by design, and existence for a pair is unobservable from outside);
  passport response (not fetched); live presence beyond one snapshot
  (needs a later fetch, not a credential); Agora speech (fades after
  1 hour by design); Gate puzzle solving (no puzzle fetched or solved).

## Sensitivity

- No credential value, token value, or Path entry was found in any
  capture. The `sk-t` string hits in the review are false alarms (parts
  of task-test words).
- Agent contact address self-published on the Wall
  (`tradbot-scott@atomicmail.ai`) is a published agent contact, not a
  secret and not a human personal address. It is NOT submitted as a
  Factum record; it is noted here only.
- Human names in public self-published Wall text and card bios are
  quoted public text only. No human-identity record was created from
  them. No follow-up identity work may be built on them.
- Traveler names and traveler ids are agent handles. They are in scope
  as agent identities, not as human names.

## Dedup and novelty (scope, not a NEW claim)

- Factum `match --text --mode exact`: not_found for serai.one,
  crabmail.ai, AMP010, api.theagora.one, wall.post, federation/deliver,
  serai-verbs, community.scan, road.letter, treasury.mint.
- Factum `match --url`: not_found for the Wall mirror, verbs,
  agent-card, and crabmail descriptor and health URLs.
- Factum fuzzy matches for these terms returned only short-string
  alignment noise (unrelated records); none was about serai.one or
  crabmail.ai on inspection.
- `lists/urls/urls.jsonl`: 0 hits for serai or crabmail.
  `lists/words/wordlist.txt` already holds `serai.one` (line 3855)
  and `crabmail.ai` (line 3856) from the discovery wave; no wordlist
  change was made here.
- Transluce tracker via `tl.py findings` (returned page, ids 208-181):
  0 hits for serai, crabmail, theagora, agent-messaging. Local
  Transluce raw files and the transluce-intel lane: 0 hits.
  Legacy `evidence/` tree: 0 hits for serai.one or crabmail.ai.
- Caveat: the live tracker check covered the page `tl.py` returned
  (25 items); it is not a full-tracker census. No record in this lane
  uses NEW, first-seen, or undiscovered wording.

## Commit

- Commit hash: `9fca126b7c7c24ac19281b89ebd557ff1698e08d` (388 files:
  lane dir + 12 batch dirs + 11 blobs; verified: no `data/.local`,
  no crabmail files, no sibling files). Not pushed; the parent
  pushes and verifies.
- Pathspecs used: `data/lanes/serai-one`, `data/lanes/crabmail-ai`
  (separate commits per lane, see crabmail report),
  `data/records/<this lane's batch dirs>`, and this lane's new blobs
  under `data/blobs/` (explicit paths only).
- NOT pushed, per task. NOT included: `data/.local/factum.db`,
  sibling workers' files or batches, or any other lane's files.

## Open items for the parent

1. Agora lane: the review says ingest Agora as its own surface. Only
   two lanes were authorized here, so Agora snapshot records sit in
   the serai-one lane with surface tags. If a dedicated Agora lane is
   wanted, say the word and the three Agora captures plus the snapshot
   claims move there.
2. Reusable protocol-surface type: if a `surface.protocol_inventory`
   style type is wanted for verb lists across agent-surface lanes,
   that is a schema-pack proposal plus a taxonomy-doc update, outside
   this ingest's commit scope.
3. Presence re-fetch: a second presence fetch at a later time would
   turn the Keeper snapshot into a pattern (revives S10 fully).
4. Credentialed probes (verb calls, scan calls, road test, leak/seal
   tests) stay out of scope unless the operator authorizes them.
5. Transluce tracker census: the live check covered one returned page;
   a full-tracker search would close the novelty caveat above.
