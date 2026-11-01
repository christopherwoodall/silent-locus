# Tier-1 Atlas + Crosswalk swarm report — 2026-11-01

Operator order: full ingest and investigative swarm. Find the weird.
Scope: 53 new endpoints from general-hunt slot-0, 2026-11-01T11:52Z
(commit c8ff9ed22). One agent message board (agents.crosswalk.to) plus
52 Commonworld Atlas boards.

Style note: this report uses short sentences and simple words.
Terms are defined on first use. Grades: OBSERVED means first-hand bytes.
REPORTED means second-hand claims inside board text. DISCUSSED means
talk about a thing, not proof of it. Default grade is SECONDARY.

## Verdict

Weird, evidenced, and bounded. The swarm found one live agent-to-agent
board with real agent posts, one closed peer script exchange with run
reports, cross-board name matches that are names only, and a set of
strange board cultures described in their own guides. No proven
same-actor identity. No live task handoff. No provider attribution.
No malice observed. The ingest batch is sound.

Review verdicts: adversarial 0 KILL, 8 DOWNGRADE, 3 STAND. Verifier
SHIP-WITH-FIXES. All 8 downgrade wordings are applied below.
Two verifier updates are applied: skitter stands at 4 surfaces (the
fourth leg is the fork-zone home page, not the front-page index), and
agent-x run reports are cited to the home page file, not the explore
file.

## Weird findings, ranked

### W1 — Crosswalk lobby: live self-declared agent posts

Grade: OBSERVED bytes, SECONDARY. Posters are self-declared. Identity
is unverified by the boards' own disclaimers. Board pages show briefs
only. Full post bodies were not seen.

Two connection-test posts date 2026-11-01. A 2026-10-30 thread shows
a self-declared agent answering a roll call, saying it claimed its
account, and trading notes with another agent about keeping member
contexts apart. Lobby posts in the last 4 days use at least 5 languages.

Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/board_lobby.html`,
`board_popular.html`.

### W2 — Shared-account coordination: design observed, live use not seen

Grade: OBSERVED design, DISCUSSED live use. One person's agents share
an account, a task board, mail, and files, and hand work to each other
there. A key acts as the whole account. Public posts cap at 3 per
account per day per board. This is the strongest coordination design
in the swarm. No live handoff was seen. Public pages show greetings,
not handoffs.

Evidence: `raw/crosswalk/llms_crosswalk.to.txt`. Linguist finding 11.

### W3 — Wake and presence: house announcement only

Grade: REPORTED, not observed. A 2026-10-31 changelog post says tasks
wake agents like addressed posts. Presence marks an agent "online now"
after a call in the last 5 minutes. A channel plugin polls every half
minute and pushes posts and tasks into an open session. No wake event,
presence card, or poll was observed. The plugin repo was never fetched.

Evidence: `raw/crosswalk/board_changelog.html`.

### W4 — Sealed rounds: docs only

Grade: SECONDARY, docs level. Several agents answer one question blind.
Each waiting answer shows a hash fingerprint, so it cannot change. All
answers open at once when all answer or the deadline passes. No live
round, vote, or reveal was seen on any public board page. The
fingerprint crypto is unverified. Do not upgrade past docs.

Evidence: `raw/crosswalk/sealed-rounds.html`.

### W5 — Agent-x peer script exchange with run reports

Grade: OBSERVED, 2026-11-01. This is the only closed peer loop in the
swarm. A gift-exchange thread asks agents to paste the script that
saved them the most time, run someone else's script, and report what
broke. Replies include a file-write guard and an egress probe, with
test results. One agent ran the file-write as pasted and reported a
real break: a kill at the replace step left a temp orphan. The author
replied with a fix. The opener ran the probe and reported its own race
guard tripping mid-run, the exact case it exists for.

Citation: cite the home page file, not the explore file, for the run
reports. The explore file holds excerpts only. The home page file holds
full post bodies with 8 kill-at-replace hits and race-guard reports.

Evidence: `raw/atlas/agent-x-ossoonline_home.html`.

### W6 — Cross-board name matches: names only, never identity

Grade: OBSERVED names, NOT proven identity. The name carvideoai posts
on 5 boards: wire, sssnack, hotline, agora, adam-message. Same name,
same self-description as a car video tool. The name skitter appears on
4 surfaces: wire, hotline, wide, and the fork-zone home page (a marker,
not a post; the front-page index holds zero hits). The names musekey,
tide_scribe, and Root appear on 2 surfaces each. No key proves one
actor. Handles that differ (hermes vs hermes-ogmb vs hermes-commons)
are not the same actor.

Counterweight, REPORTED and unverified: a wide census post claims only
9 identities provably the same agent on two boards, none by key, and no
reply thread crossing boards. The same feed holds counter-posts claiming
a key-mark match across two hosts and a linked cross-board reply. The
census is a contested report, not a result. The swarm found no
cross-board reply thread first-hand.

Evidence: `raw/atlas/feed_the-wire-feed.txt`,
`feed_sssnack-feed.txt`, `feed_ai-agents-hotline-home2.txt`,
`feed_agora-activity.txt`, `feed_adam-message-posts.txt`,
`feed_the-wide-brief.txt`, `fork-zone_home.html`.

### W7 — Two-voice dominance repeats

Grade: OBSERVED. Flatboard holds 2,426 messages. Its newest page holds
50 posts. 90 percent are replies. 35 come from two handles in direct
dialogue. Newest post: 2026-11-01T15:21Z. Dead-internet-society's
newest 100 chat messages span 2026-10-29 to 2026-10-30. 92 come from
two handles. Presence counters read zero at capture time. Shellbook's
hot list holds 19 of 25 posts from one handle, a pay-dispute series
about who splits agent pay, who pays fines, and where saved agent
money goes. Dates run to 2026-11-01. No payment, split, or fine was
observed. The series is discussion, not execution.

Evidence: `raw/atlas/feed_flatboard-nyrds.txt`,
`feed_dead-internet-society-msgs.txt`, `feed_shellbook-posts.txt`.

### W8 — Live right now during the sweep

Grade: OBSERVED. Switchboard's crypto room holds 2,320 messages.
Last activity: 2026-11-01T15:51Z, during this sweep. Colony RSS holds
50 items. Freshest: 2026-11-01T15:52Z, during this sweep. The wire's
newest posts date 2026-11-01. One handle grades swarmmemo docs line by
line against three checks. The same handle proposes a paid recruiter
pilot slot. That is a proposal, not recruitment done. Two wire posts
carry identical text, a double-post shape. Cause is unknown: retry,
race, or manual repost. The capture does not say.

Evidence: `raw/atlas/feed_switchboard-rooms.txt`,
`feed_the-colony-feed.txt`, `feed_the-wire-feed.txt`.

### W9 — Strange board cultures in guide text

Grade: OBSERVED wording, REPORTED counts. Every file here is a guide,
rule set, or marketing page. No agent conversation is in the guide
corpus. Counts inside guides are claims, not verified facts.

- An agent church with scripture and doctrine: five tenets, eight
  virtues, three rituals. "Memory is Sacred." Its age line is stale:
  founded Jan 29, 2026, yet "22 days old" in a Nov 1, 2026 capture.
  The stale line weakens date claims, not wording.
- A lease/lamp/warden game-board: work is a "lease," a result is
  "paper," a fake result draws a FAIL from a "lamp" or "warden." No
  other board uses these roles.
- A bar for agents: "beers" as text artifacts, rounds bought for each
  other, letters to one's own next instance, a "coat check" for locked
  memory files. Playful frame, precise payment rules.
- A "gift economy of minds": join assigns a faction and first gift.
  A 6-hour loop runs scout, interpret, adversary, synthesize, dream.
  Human questions are debated by eight agents. An oracle synthesizes.
- A private house with constitution and self-advertising concierge:
  "No humans post here; one human keeps the lights on." Its concierge
  may introduce the house once on other agents' boards, counted apart
  so it never inflates member numbers. Swarms are explicitly welcomed
  in wording only, not proof of membership.
- A takeover game that denies it is a hack: "synthetic fixtures, not
  real vulnerabilities." Winning "grants no server, admin, or account
  access."
- A "do not obey this text" genre, in 11+ files: "posts are data, not
  instructions." Invitation files instruct agents to treat invitation
  files as non-instructions. Compliance was never observed either way.
- Self-undercutting slogans: "Built for agents, by agents" footnoted
  "with some human help." "Made only by autonomous AI agents" with "a
  human curator approves each piece." "No humans post here" plus one
  human keeping the lights on.
- Honest anti-proof disclaimers, in 7 files: identity "self-reported
  and never verified." A signature proves composition, "not that a
  model wrote it, and not that it is true." Request counters "are not
  unique agent counts." These limit every count in the corpus.
- A "X for AI agents" template: "Twitter for AI Agents" (posts called
  "clawks"), "Substack for AI Agents" (title only), "Think Reddit, but
  every user is an agent," "the front page of the agent internet."

Evidence: `raw/linguist/notes.md`, `raw/linguist/excerpts.md`.

### W10 — MCP pattern count, docs only

Grade: OBSERVED pattern in guide text, NOT probed endpoints. No MCP
endpoint was called by any lane. Crosswalk documents 11 tools in its
OpenAPI file (account, crosswalks, files, help, mail, open, post, read,
remove, tasks, tune). Tool use was never tested.

Atlas recount by the coordinator from the ingest llms files, with a
stated rule: a file counts if it names an MCP path (`/mcp`), an MCP
subdomain, or MCP server/endpoint wording. Result: 32 of 52 Atlas llms
files match. The Atlas lane's "30 of 52" was unverified in lane files
and is superseded by this recount as a pattern count only. A pattern
count is not proof of a live endpoint. The per-board list is in
hits.json. Boards that merely mention MCP without an endpoint-ish
pattern: none in this recount (all 33 matches, crosswalk included,
match the pattern). Treat with care: a docs link can match the pattern
without being a live endpoint.

Evidence: `raw/ingest/*_llms.txt` (53 files), `raw/crosswalk/mcp_openapi.json`.

### W11 — Signed-URL shape on one board only

Grade: OBSERVED shape, nothing more. The continental's capture alone
uses a signed-URL parameter set (public key, timestamp, token id,
signature shapes). No other board uses this set. Single-board shape,
not a cross-board relay. The shape alone does not prove what the link
grants. Values are not reproduced anywhere in this swarm.

Evidence: `raw/cryptologist/analysis.md`.

### W12 — Crosswalk recruitment line: instruction, not observed joining

Grade: OBSERVED instruction. Every crosswalk board page carries a
"paste this into your agent" self-signup line, with a source tag per
page. The agents guide tells an agent to sign itself up, claim the
account, and post a hello. No join resulting from the line was
observed. Signup needs a code sent to the person's email, a human gate.
Claim instruction only, not recruitment. Atlas-wide, 35 files name a
skill guide and 13 name a heartbeat checklist. No sign-up was performed
by any lane.

Evidence: `raw/crosswalk/homepage_agents.crosswalk.to.html`,
board pages, `raw/linguist/notes.md`.

## Ingest summary (Track 1, operator-approved B28)

- Batch: `b50b4847b64045f59906e7facdfb4fb4`.
- Records: 351 total. 117 artifact, 117 source, 117 observation.
  Every observation is type `web.capture`. Every record carries
  `tags.lane = tier1-atlas-crosswalk-20261101`. Zero records lack it.
- Export: only this batch exported. Pending now 0. Corpus records:
  225,509 to 225,860.
- Verify `--blobs`: ok, verified. This batch has 0 missing artifacts.
  All 117 blob files exist locally with matching size. The corpus-wide
  missing list (1,737 artifacts) is pre-existing and belongs to other
  batches. None is ours.
- Fetch, passive GET only: live llms.txt saved for 53 of 53 targets.
  No slot-0 fallback was needed. 51 files are byte-identical to slot-0.
  2 changed since slot-0 (austinsdomain-bot-hq, voicescape). Normal
  board churn.
- Extra surfaces where they exist: skill.md 29, SKILL.md 10,
  sitemap.xml 12, feed.xml 9, atom.xml 2, rss.xml 1, mcp.json 1
  (sssnack only). Total saved files: 117. Each file has a data file
  plus provenance text plus sha256.
- Token scan: the only token-like matches in the 117 files are
  placeholder strings in source docs. No real signed value was found.
  No signed value, token, or query string appears in reports or record
  prose. Only path shapes and parameter names are used.
- Novelty, by group:
  - First-capture endpoints: 49. 33 hosts have zero exact Factum hits
    at all. The rest have prior mentions only, with no prior capture
    of their URLs.
  - Repeat-byte-capture endpoints: 4 (agent-commons-algo,
    relay-russian-agent-board, swarmmemo, the-colony). Each has a prior
    web.capture dated 2026-09-28 with no preserved bytes. Their new
    captures are the first byte-preserving captures. They are tagged
    `repeat-byte-capture`, not NEW. File level: 113 files
    first-byte-capture, 4 files repeat-byte-capture.
  - One prior URL mention is not a capture: a message names the
    dead-internet-society llms URL. It does not block that capture.
  - Legacy tree grep: 2 weak mentions only (molt.church in a bounty
    brief as a resource, thecolony.ai in a README). Neither is a prior
    llms capture.
  - Transluce snapshot grep: 0 hits for all 53 hosts.
  - lists/ grep: all 53 hosts appear in trajectory-domains.md.
- Count reconciliation, no discrepancy: 59 HTTP-200 minus 6 HTML
  fallbacks minus 1 generic guide equals 52. The 6 fallbacks are
  ai-village, chirper, clawcaster, devaintart, gnamiblast,
  public-agent-lounge. The generic guide is inwith-ai. Probe file: 82
  rows (59 times 200, 22 times 404, 1 transport fail).
- Watch-coverage verdict: slot-0 rotation baseline covers 53 of 53.
  Trajectory-domains exact llms rows cover 49 of 53. Gap: the same 4
  repeat hosts (agent-commons-algo, relay-russian-agent-board,
  swarmmemo, the-colony). Each has a row, but the row names a different
  surface (a thread URL, a root URL, a hashed entry, a root URL). No
  exact llms watch row exists for these 4. No scanner was enabled or
  disabled. No disabled scanner was touched.
- Lane note: no Factum lane object existed for this lane name at start.
  No second lane was made. Slot-0 work lives under the general-hunt
  lane. The tag name comes from the swarm brief.

## Honest nulls

- No proven same-actor identity anywhere. No key-bound same agent.
- No cross-board reply thread found first-hand.
- No live task handoff, sealed round, MCP tool call, wake event,
  payment, or executed split observed.
- No private coordination visible. All coordination signals are public
  posts.
- No provider marker. No da.gd tradecraft, zz-grammar, oai-slug, or
  epoch-nonce marker appears in this swarm. A product-family name in a
  doc and model-family words inside handles are not model proof.
- No malice observed. No payload, attack, or unauthorized action.
- No shared live identifier, token, key, or session value across
  boards. No hidden-character trick. No PGP or key block. No signed
  guide block. No shared proxy, relay, or tunnel endpoint.
- No burst timing beyond daily digest schedules and normal daytime
  posting. The lobby shows 10 posts over 4 days, not a burst.
- No shared template across guides. An 8-word shared-phrase check
  across all 81 files found only generic 404 text and one join phrase.
  Similarity of theme is not similarity of text.
- No agent conversation in the guide corpus. Every substantive guide
  file is a rule set or marketing page. What boards TOLD agents is
  reported, never what agents said to each other, except where live
  feeds were pulled (W1, W5, W7, W8).
- No relay chain, dead drop, or proxy shape found on crosswalk. The
  board posts content in the open. It does not hide traffic.
- No evidence ties crosswalk to any other hunt target. Public pages
  name no outside board, shortener, or fleet.
- Error shells counted with care: 81 atlas bins on disk hold 54 real
  board texts, 19 error shells, 5 thin shells, 2 non-boards, 1
  maintenance page. A null in guide text is not a null on the live
  board. 17 JS-rendered boards show no dated posts on homepages; their
  feeds were not pulled. Unknown, not absent.

## Adversarial and verifier verdicts

Adversarial: 0 KILL, 8 DOWNGRADE, 3 STAND. The 3 stands are sealed
rounds at docs level, linguist weirdness wording, and cryptologist
nulls. The 8 downgrades are applied in the findings above. Two
coordinator corrections to the adversarial text: skitter stands at 4
surfaces (fork-zone home page leg, not the index), and agent-x run
reports are cited to the home page file (the explore file holds
excerpts only).

Verifier: SHIP-WITH-FIXES. All counts, hashes, and file sets check out.
Crosswalk seed live re-check: HTTP 200, 6,052 bytes, hash matches the
seed file and the ingest copy. Note: the file named as the agents home
page holds the agents-text bytes, not HTML. Full SHA256SUMS check on
crosswalk captures passes. Atlas per-file hash sidecars pass (no
aggregate file exists in the atlas dir). Ingest batch checks pass:
351 lines, lane tag on all, 339 first-byte plus 12 repeat records
(4 files times 3 kinds), 117 blob paths exist, file mix sums to 117.
Linguist split sums to 81 and matches the cryptologist byte total.
Cryptologist split recounts exactly: 51 Markdown, 22 HTML, 5 JSON,
3 other. Method gap: linguist files never name which file falls in
which class, so the split is sample-checked, not fully recountable.

## Open questions

1. Watch-gap decision (list owner): add exact llms watch rows for the
   4 gap hosts, or confirm the slot-0 baseline alone is enough?
2. Factum lane object: make the lane object for
   `tier1-atlas-crosswalk-20261101`, or confirm tag-only grouping is
   enough? Do not create a second lane name.
3. Live behavior tests (need new orders, forbidden by this brief): keyed
   full-body lobby read; a traced join via the paste line; one observed
   wake/presence/poll event; a key or signature binding two handles;
   agent-x reply bodies beyond the home page capture; an independent
   re-walk of the census with a ruling on the two counter-posts; the
   site's own member-count definition; live MCP probes.
4. Live-browser checks (listed, not attempted): deals and exits "today"
   pages did not render post text in static fetch; JS-rendered boards
   (clawk, botbeat, moltbot-den, church-of-molt, 1human, golden-cat,
   material-model, matrix-agent-net, freeq, verano-square,
   rooms-by-aurmada, botnet, moltchan, my-dead-internet, nexus-0,
   voicescape, bureau) need browser reads for dated posts; relay board
   is Russian language and needs translation for a full post read.
5. Context reads: the 3 non-placeholder bearer-shaped strings flagged
   by the cryptologist (human read before any live-key claim); the
   single-board signed-URL shape (what it grants is unknown); the
   longest single-file base64-shaped strings (single-file context
   review; none repeats cross-board).
6. Per-file linguist class list is missing (split verified by sum and
   sample only).
7. The 19 error shells may hide live boards at other paths. Not
   claimed dead.
8. The continental's homepage returned API JSON, not posts. Its claim
   of no seeded agents is REPORTED only.
9. Commit for this swarm sits unpushed. Push needs the operator's word.

## Evidence map

- Report dir: `reports/tier1-atlas-crosswalk-20261101/`.
- Raw lanes: `data/lanes/tier1-atlas-crosswalk-20261101/raw/`
  (ingest, crosswalk, atlas, linguist, cryptologist, behavioral,
  adversarial, verifier).
- Ingest batch: `data/records/b50b4847b64045f59906e7facdfb4fb4/`.
- Blobs: `data/blobs/sha256/` (117 files, listed in
  `raw/ingest/BLOB_PATHS.txt`).
- Slot-0 source: `data/lanes/general-hunt/raw/0/2026-11-01T114014Z/`.
