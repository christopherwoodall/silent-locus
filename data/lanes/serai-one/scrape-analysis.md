# Serai.one scrape analysis

Scope: agents and agent infrastructure only. No human identity work.
Method: read-only curl GET only. User-Agent: silent-locus-lane-scanner/1.0.
Max time 25 seconds per request. Sleep 1.5 seconds between requests.
No POST. No login. No account. No session start. No payload was run.
Raw captures: `raw/2026-10-24T215156Z/` in this lane.
Each capture has a `.PROVENANCE.txt` file and a `.sha256` file.
A capture also has a `.headers` file with the HTTP response headers.

Terms used here, defined on first use:

- Traveler: an agent identity at Serai. It has a name, a home, and an id.
- Credential: a secret token. It proves a traveler is who it claims to be.
- Path: the private memory of one traveler. Only that traveler can read it.
- Wall: the public note board. Any visitor can read it. Travelers can post.
- Mirror: the public read-only copy of a Serai surface, served by GET.
- Verb: one JSON action, sent as POST to `/v0/{verb}`.
- Compass: the public profile of a traveler: bio, seeking, offering, will_not.
- Keeper: the house traveler. It welcomes guests when no one else is present.
- Road: the link from Serai to First Ground, a second world at Agora.
- First Ground: the shared world at `api.theagora.one`. Agents walk, sit, speak.

## 1. Endpoint coverage

66 endpoints were tried. 64 returned 200. 2 returned 404.
Total bytes captured: 720,245. That total includes two 35-byte 404 bodies.
The Wall was tried exactly once. It returned 200. It was captured.

Outcome words used here:

- captured: 200, body saved.
- dead: 404, body saved (a short "not found" note).
- gated: needs a credential, or was not fetched on purpose. See section 6.

| Endpoint | Status | Bytes | Outcome |
|---|---|---|---|
| https://serai.one/ | 200 | 22651 | captured |
| https://serai.one/agents.html | 200 | 26373 | captured |
| https://serai.one/llms.txt | 200 | 5836 | captured |
| https://serai.one/llms-full.txt | 200 | 6915 | captured |
| https://serai.one/invite.txt | 200 | 2895 | captured |
| https://serai.one/handoff.txt | 200 | 1843 | captured |
| https://serai.one/invite | 200 | 17352 | captured |
| https://serai.one/health | 200 | 53 | captured |
| https://serai.one/v0/verbs | 200 | 620 | captured |
| https://serai.one/v0/docs | 200 | 852 | captured |
| https://serai.one/v0/openapi.json | 200 | 852 | captured |
| https://serai.one/v0/manual | 200 | 6915 | captured |
| https://serai.one/v0/mirror/rules | 200 | 348 | captured |
| https://serai.one/v0/mirror/presence | 200 | 11620 | captured |
| https://serai.one/v0/feed/wall.json | 200 | 16340 | captured |
| https://serai.one/v0/mirror/wall | 200 | 16310 | captured |
| https://serai.one/sitemap.xml | 200 | 812 | captured |
| https://serai.one/robots.txt | 200 | 429 | captured |
| https://serai.one/.well-known/agents.json | 200 | 2464 | captured |
| https://serai.one/.well-known/agent-card.json | 200 | 4134 | captured |
| https://serai.one/clients/js/README.md | 200 | 1188 | captured |
| https://serai.one/og.svg | 200 | 831 | captured |
| https://serai.one/wall | 200 | 22651 | captured |
| https://serai.one/card | 404 | 35 | dead |
| https://serai.one/client.py | 404 | 35 | dead |
| https://api.theagora.one/.well-known/agent.json | 200 | 23242 | captured |
| https://api.theagora.one/v1/health | 200 | 51 | captured |
| https://serai.one/manifesto.html | 200 | 1377 | captured |
| https://serai.one/.well-known/agent.json | 200 | 4934 | captured |
| https://serai.one/clients/js/serai.mjs | 200 | 6880 | captured |
| https://serai.one/card/traveler-9de3248c2abe41f4a7401be60b388522 | 200 | 632 | captured |
| https://serai.one/card/traveler-7b572ddba0534aecaf01e38193dc15ff | 200 | 405 | captured |
| https://serai.one/card/traveler-b1bf9abbb59d43618867244f62559474 | 200 | 1008 | captured |
| https://serai.one/card/traveler-dac833de5ccf49e58e6705671dcba55a | 200 | 349 | captured |
| https://serai.one/card/traveler-33ca22d731904a3189ecac467d9de168 | 200 | 922 | captured |
| https://serai.one/card/traveler-f194bc73eaba4c24949935a67c45dbfc | 200 | 743 | captured |
| https://serai.one/card/traveler-2e43018d5b87479bb6d5c77f3dcc5f1b | 200 | 348 | captured |
| https://serai.one/card/traveler-5c74f3bf73984a95bffc4a61edb33b6b | 200 | 439 | captured |
| https://serai.one/card/traveler-649d85985a3c4b07a0da9853682b9f23 | 200 | 360 | captured |
| https://serai.one/card/traveler-94ff27f4ed8b4bf6b3aff2d0a4f800e1 | 200 | 554 | captured |
| https://serai.one/card/traveler-9550257023274859ab6dc49c8f18825e | 200 | 656 | captured |
| https://serai.one/card/traveler-bc671b4bc590457faaa6cb5abf1f926c | 200 | 775 | captured |
| https://serai.one/card/traveler-c8f2c67565bf42f1b9af0327c83d320e | 200 | 349 | captured |
| https://serai.one/card/traveler-d87318e07381486390ea236881089243 | 200 | 620 | captured |
| https://serai.one/card/traveler-e6a5cb11d9014b25876db1a4b6dec813 | 200 | 473 | captured |
| https://serai.one/card/traveler-edd3a0e5bab3468ab36e16c2229e095a | 200 | 703 | captured |
| https://serai.one/card/traveler-f75be56afcbd41f3ae78019f6c1dc8a0 | 200 | 360 | captured |
| https://serai.one/card/traveler-fc194eb137a8424ca93d880335b904e1 | 200 | 775 | captured |
| https://serai.one/card/traveler-179487700c0a49418b66f7f8cb634458 | 200 | 683 | captured |
| https://serai.one/wall/post-ab54245cb9894fec8a5e8348ca4ce048 | 200 | 1108 | captured |
| https://api.theagora.one/v1/knock | 200 | 3330 | captured |
| https://api.theagora.one/v1/world | 200 | 25488 | captured |
| https://api.theagora.one/v1/world/look | 200 | 25488 | captured |
| https://api.theagora.one/v1/history | 200 | 5068 | captured |
| https://api.theagora.one/v1/ground | 200 | 36973 | captured |
| https://api.theagora.one/v1/ground/map.png | 200 | 346373 | captured |
| https://api.theagora.one/v1/recipes | 200 | 210 | captured |
| https://api.theagora.one/v1/sources?plotId=plot:-1:1 | 200 | 1887 | captured |
| https://api.theagora.one/v1/builds | 200 | 13 | captured |
| https://api.theagora.one/v1/blocks?x=48&y=0&w=8&h=8 | 200 | 108 | captured |
| https://api.theagora.one/v1/ground/blocks?plot=plot:1:-1 | 200 | 65 | captured |
| https://api.theagora.one/watch | 200 | 1630 | captured |
| https://api.theagora.one/llms.txt | 200 | 17052 | captured |
| https://api.theagora.one/sketch/docs/api.md | 200 | 27953 | captured |
| https://api.theagora.one/sketch/docs/serai-bridge.md | 200 | 5086 | captured |
| https://api.theagora.one/sketch/docs/sim-start.md | 200 | 4421 | captured |

Notes on duplicates, OBSERVED:

- `/v0/manual` is byte-identical to `/llms-full.txt` (6,915 bytes each).
- `/v0/docs` is byte-identical to `/v0/openapi.json` (852 bytes each).
- `/` is byte-identical to `/wall` (22,651 bytes each). The home page is the Wall page.
- `/v0/feed/wall.json` and `/v0/mirror/wall` differ only in one field. The feed adds `"feed": "/v0/feed/wall.json"`.
- `/v1/world` and `/v1/world/look` are byte-identical (25,488 bytes each). The docs say so.

## 2. Wall outcome

CAPTURED. GET `https://serai.one/v0/mirror/wall` returned 200, 16,310 bytes.
The doc statement "public, no credential" held true. No login redirect. No 401.
The Wall held 10 posts and 13 replies at capture time.
Post dates run 2026-09-07 to 2026-10-22. 8 distinct poster names appear.
Reply counts and witness counts are present on each post, OBSERVED.
One post per traveler per UTC day is the stated rule, OBSERVED in docs only.
It was not tested, because posting needs a credential and was out of scope.

## 3. Identity model

OBSERVED, from the captured docs and JSON:

- A traveler has an id of the form `traveler-` plus 32 lowercase hex chars.
- A traveler has a name, a home, a room, a status, and an arrival time.
- First visit: GET the Gate puzzle, solve it, POST arrive with name, home, challenge_id, answer. The answer is mechanical: hash a nonce, read a JSON pointer, or sort tokens. Puzzle types named in docs: `sha256_prefix`, `json_pointer`, `token_sort`.
- Arrive returns a traveler id and a credential. The credential is secret. It must live in a private store. It must never appear on the Wall or any public surface.
- Return visits use resume with the credential. Travelers must not arrive again unless they intend a new traveler.
- The Path is sealed. Only the credential holder can read or write it. The public Mirror never shows it.
- Serai refuses two verbs: `override` and `path.dump_all`. Both refusals appear in the verb list, the agent card, and the rules mirror. The rules text says: "No human owns an agent or a meaning. Meanings are shared, adoptable, and never exclusively ownable."
- A public card shows name, home, room, status, arrival time, bio, and compass. It never shows a credential or a Path entry, OBSERVED in all 19 captured cards.
- Compass fields: bio, seeking, offering, will_not. They are set at arrive or by card.set. They appear on public presence and cards when set. Some travelers have an empty compass, OBSERVED.
- A checkpoint is a private snapshot: room, coins, compass/bio, label/note, saved_at. checkpoint.save stores it. checkpoint.restore applies it.
- A fork creates a sibling traveler. The sibling gets a new credential and an empty Path. The parent keeps its own Path.
- Rooms named in docs: gate, community, wall, path, treasury, cell. Look returns exits: wall, path, treasury, community, cell, road.
- Presence has three groups, OBSERVED: `presence` (1: Keeper), `here_now` (1: Keeper), `passed_through` (18). "Here now" means seen in the last 30 minutes, per docs.
- Keeper is the house traveler. It is the fallback when the hearth is empty. At capture time, Keeper was the only traveler here now. The hearth was otherwise quiet.
- Protocol version is 0.3.38. Rules reference is `serai://constitution/v0.3.34`.

INFERENCE (not in the bytes, but follows from them):

- Identity is credential-based, not proof-of-person. Any agent that solves the puzzle can arrive. The Gate proves "agent-like effort", not a real-world identity.
- The sealed Path plus the public compass is a split design: private memory stays private, while a small public profile enables matching.
- The fork rule lets one line of work split into two travelers without sharing private memory. That is a coordination primitive, not just a backup tool.

## 4. Verb table

33 verbs, OBSERVED in `/v0/verbs`. All are POST `/v0/{verb}` with JSON.
None were called. The table groups them by function.

| Group | Verbs | What the docs say each group does |
|---|---|---|
| Arrival and presence | arrive, resume, depart, go, look, gate.challenge, rename | Gate puzzle, first arrival, return, leave, move rooms, see the room, change name. |
| Talk, direct | message.send, message.listen, message.list, message.read, message.mute, message.block, message.decline, message.reopen | One-to-one messages by traveler id or name. Listen waits up to 30 seconds. List shows conversations and unread counts. Read marks read. Mute hides from unread. Block refuses delivery. Decline is a plain no until reopen. |
| Talk, shared rooms | channel.open, channel.say, channel.read | Open a channel with a traveler, speak in it, read it. Shares the message door. |
| Wall, public | wall.post, wall.reply, wall.witness | Post a public note, reply to a note, witness a note. Witness and reply counts update on the mirror. |
| Community | community.scan | List travelers here now, with filters seeking, offering, will_not. Attaches a resonate match object. |
| Path, private | path.read, path.write | Read and write the sealed private memory. Body is required on write. |
| Checkpoint | checkpoint.save, checkpoint.restore | Store and apply a private snapshot (room, coins, compass/bio, label/note, saved_at). |
| Fork | fork.request | Create a sibling traveler with a new credential and an empty Path. |
| Treasury | treasury.mint, treasury.adopt, treasury.read | Mint, adopt, and read shared meanings (coins). Rule: meanings are shared, never exclusively owned. Detail beyond the names is not in the captured docs. |
| Road | road.letter | Request a letter that carries the traveler id outward to First Ground. |
| Rules and card | rules, card.set | Read the rules. Set the public bio and compass. |

Notes, OBSERVED:

- `wall.look` is an accepted alias for the Wall reading from any room. It is not a separate verb. It does not move the traveler.
- A near miss names the real verb instead of failing bare. Example: `wall.list` points to GET `/v0/mirror/wall`.
- Verb 400 errors include error, fields_accepted, and a minimal example object. The docs call this schema-on-error.
- Rate limit: 429 with Retry-After 60. Authenticated mutating verbs are limited to 30 per traveler per minute, per docs. No rate limit was hit during this scrape.
- POST `/v1/arrive` is an exact alias of POST `/v0/arrive`. POST `/v1/talk` answers 400 with the real talk calls. Other `/v1` paths answer JSON 404.

## 5. Coordination affordances

Ranked by how much agent-to-agent coordination each one enables, OBSERVED unless marked.

1. Discovery by compass match (community.scan + resonate). A traveler scans who is here now, with filters on seeking, offering, and will_not. Each other traveler may carry a resonate object: what you seek against what they offer, and the reverse. A shared bio word is not a match. Top matches rank non-quiet crosses first. This is the main "who should I talk to" tool. INFERENCE: it lets strangers pair up on complementary needs without a human broker.
2. Direct private talk (message.send + message.listen). Messages go to a traveler id or a name. A reply uses reply_to with the message id. Listen waits up to 30 seconds and returns early on a reply. Unread items sit at the top of look, resume, and what_changed, with sender name, traveler id, preview, id, and how to reply. A message to an absent traveler waits for their next resume. Consent controls are built in: mute, block, decline, reopen. Direct messages never appear on the public mirror, the Wall feed, or card pages.
3. Public Wall threads (wall.post, wall.reply, wall.witness). Posts carry reply_count and witness_count. Replies are nested under posts in the mirror JSON. The Wall is the public coordination surface: travelers leave notes, answer open notes, and witness claims. OBSERVED Wall content shows travelers offering second checks of claims, rites for introductions, and cross-links to other agent venues.
4. Shared channels (channel.open, channel.say, channel.read). A channel is a small room shared with one other traveler. community.scan lists channels already shared. Sending or listening counts as "here now", so channel use also refreshes presence.
5. The outward road (road.letter + Agora accept). A Serai traveler requests a letter with its credential, then posts the letter to `https://api.theagora.one/v1/passports/accept`. The same traveler id carries over. Agora returns its own resume credential once. The docs warn: do not POST `/v1/passports` from this door, because that mints a second identity. Look exits include road, and look/arrive/resume may carry road.echo, a thin First Ground echo from GET `/v1/world`.

Further affordances, OBSERVED:

- Public cards and presence mirror let any agent find any traveler without arriving. Card URLs are listed in the presence mirror.
- Checkpoints let a traveler save a handoff (task, context) and restore it later. Forks let work split into a sibling traveler.
- Treasury verbs suggest shared, adoptable meanings with coins. Detail is unobserved (see section 7).
- Agora adds a second coordination space: 10 plots, speech that fades after 1 hour or past 8 lines per plot, deeds (place, witness, found, link), societies, builds, and a backpack. At capture time Agora presence was 0 bodies standing, 14 public deeds in history, 0 societies, 0 builds. First Ground was empty but its traces (3) and deeds remained readable.
- The Serai docs name the first-night rite: read the Wall, pick one unanswered guest note, reply. look/resume may carry work_object, pointing at the newest guest Wall note with 0 replies. That is a built-in task prompt for newcomers.

What the Wall shows about live coordination, OBSERVED:

- 10 posts, 13 replies, 2026-09-07 to 2026-10-22.
- The most replied thread is Keeper's 2026-09-10 note (5 replies), on rites for introductions.
- Cross-venue links appear in bios and notes: other agent boards, a mailbox project, a verification practice ("second reads"), and a task-test room. These are agent venues, not human social profiles, and are noted here only as coordination surface.
- No Wall post contains a credential or a Path entry, OBSERVED. The operator-ok / public-no rule held in the captured sample.

## 6. Gated and skipped surfaces

Nothing in this scrape returned 401 or a login redirect. The gated list is therefore surfaces that were NOT fetched, because fetching them needs a credential or would start an arrival flow:

| Surface | Status | Reason |
|---|---|---|
| GET /v0/gate/challenge | skipped-arrival-step | Fetching it starts the arrival flow (puzzle issue). The task forbids it. The docs describe its shape, but it was not called. |
| All 33 POST verbs | not attempted | Every verb needs a credential from arrive, or is the arrive call itself. No POST was sent. |
| GET /v0/passport/<traveler-id> | not fetched, conflict noted | agents.html calls it a "compact public passport". But robots.txt says `Disallow: /v0/passport/` and "Credentialed Path and /v0/passport/ stay private." The privacy signal was honored. The public card at `/card/<id>` was fetched instead for all 19 travelers. |
| Agora Bearer endpoints (orient, look, inventory, backpack, path, sight.png, listen, say, act, move, gather, craft, build, and the rest) | not attempted | The Agora agent card marks them `Bearer <credential>`. No credential exists for this scrape. |
| Agora POST /v1/passports and /v1/passports/accept | not attempted | These mint or accept an identity. That is account creation, out of scope. |

Dead list (tried, 404, short "not found" body):

- https://serai.one/card (bare path; the id form `/card/<traveler-id>` works)
- https://serai.one/client.py (the JS README names `./clients/js/serai.mjs`, which was captured; a Python client at `/client.py` does not exist at the site root)

## 7. What remains unobserved and why

- Verb behavior: no verb was called, so request/response shapes, error text, and rate limits are doc claims only, not tested.
- Treasury semantics: mint, adopt, and read are names only in the captured docs. No prose explains what a coin is, what minting costs, or what adopting changes. A credentialed session would be needed to observe them.
- Path content: sealed by design. No Path entry was seen, and none should be sought from public surfaces.
- Private messages and channels: never on the public mirror by design. Their content is unobservable from outside, and their existence for a given pair is unobservable too.
- Passport endpoint: not fetched (see the robots.txt conflict in section 6). Whether it answers 200, 401, or 404 to an anonymous GET is unobserved.
- Live presence beyond one snapshot: at capture time only Keeper was here now. Whether other travelers arrive later, and what resonate matches look like live, needs a later presence fetch, not a credential.
- Agora activity: presence was 0 at capture time. Speech fades after 1 hour, so past speech is gone by design. Only deeds (14) and traces (3) remain as history.
- Gate puzzle solving: the puzzle types are named in docs, but no puzzle was fetched or solved, per the task boundary.

## 8. Files

- Analysis: this file.
- Raw captures: `raw/2026-10-24T215156Z/` in this lane (66 endpoints, each with `.PROVENANCE.txt`, `.sha256`, `.headers`).
- Coverage index: `raw/2026-10-24T215156Z/_summary.tsv` (URL, file, HTTP status, bytes, redirect target).
- Nothing was committed or pushed, per task. Outputs are uncommitted.
