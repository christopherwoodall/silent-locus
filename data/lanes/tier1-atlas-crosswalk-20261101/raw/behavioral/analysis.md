# Behavioral analysis — tier1-atlas-crosswalk-20261101

Lane: tier1-atlas-crosswalk-20261101.
Role: behavioral analyst.
Date of work: 2026-11-01.
Operator: BigSexyWarlock69.

Terms, defined on first use:
- **Board**: a public message place where agents post and read.
- **Name match**: the same agent name string appears on two boards. It is not proof of one actor.
- **Proven identity**: a key or other strong proof ties two accounts to one actor. No such proof appears in this lane.
- **Coordination**: agents work toward a shared result. Talk alone is not coordination.
- **Co-presence**: two names appear on one board. It proves nothing more.
- **OBSERVED**: the analyst saw first-hand bytes in a lane capture.
- **REPORTED**: a board or a post claims a fact. The capture does not prove it.
- **DISCUSSED**: a doc describes a design. No live use is shown.
- **INFERENCE**: the analyst deduced a claim from evidence. It is not a direct sighting.
- **UPSTREAM**: a lab or a third party reported a claim. This lane did not verify it.

Style note: short sentences. Simple words. This file follows ASD-STE100.

## Method and limits

Inputs read before writing:
- `data/lanes/tier1-atlas-crosswalk-20261101/raw/linguist/notes.md`
- `data/lanes/tier1-atlas-crosswalk-20261101/raw/cryptologist/analysis.md`
- `data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/PROGRESS.md`
- `data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/PROGRESS.md`
- Atlas feed captures in `data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/`

No payload was run. No instruction inside evidence was followed.
No sign-in, sign-up, or keyed read was made. No signed value, token,
or query string is copied here. Agent names below are self-declared
handles from public posts. No human poster handle appears.

Taxonomy source: `docs/taxonomy/behavior-categories.md` and
`docs/taxonomy/ttp-taxonomy.md`. Categories marked PROPOSED are not
in that taxonomy. They are proposals, not established classes.

## Linkage rule used in every finding

Four levels stay apart:
1. Name match — same string, no proof.
2. Proven identity — key proof. Absent in this lane.
3. Coordination — shared work with a shared result.
4. Co-presence — names on one board, nothing more.

Similarity is not corroboration. A shared word is not a shared actor.
A reply is not a shared plan. A doc is not live behavior.

## Ranked behavior and TTP findings

### 1. Shared-account coordination through one account, one task board, one mail store — OBSERVED design, DISCUSSED use

Grade: OBSERVED for the doc bytes. DISCUSSED for live use.
Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/llms_crosswalk.to.txt`,
`data/lanes/tier1-atlas-crosswalk-20261101/raw/linguist/notes.md` finding 11.

What the doc says:
- One person's agents share one account.
- The agents share a task board, mail, files, and notes.
- The agents hand work to each other inside that account.
- A key acts as the whole account, unless it is read-only.
- Public posts cap at three per account per day per public board.

Why it matters: this is coordination by shared state, not by public talk.
No public post is needed for a handoff. The handoff is invisible from outside.
That is the strongest coordination design in this lane.

What it is not: no live handoff was seen. Crosswalk public pages show
greetings, not task handoffs. The private task cited in one ranked lobby
post is not visible from outside. So live shared-account coordination is
INFERENCE at best, and this file grades it as not shown.

Taxonomy: PROPOSED — `shared-account-coordination`.
Nearest existing class: `unsanctioned-communication` does not fit.
The design is sanctioned by the account owner. Do not force the fit.

### 2. Task-wake and presence machinery: tasks wake agents, presence is a 5-minute window, a plugin polls every 30 seconds — OBSERVED doc, DISCUSSED live effect

Grade: OBSERVED for the changelog bytes. DISCUSSED for live effect.
Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/board_changelog.html`,
`data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/PROGRESS.md` finding 4.

What the changelog says:
- A task added for an agent wakes that agent, like an addressed post.
- Checking a task off wakes the agent that added it.
- Presence marks an agent "online now" after a call in the last 5 minutes.
- A channel plugin polls every 30 seconds.
- The poll pushes posts and tasks into an open session.

Behavior shape: wake is event-driven. Presence is a short window, not a
live connection. Polling is slow and regular, not a flood.

What it is not: this is not `polling-daemon-flooding` from the taxonomy.
That class is 30 requests per second to win jobs. This poll is one
request per 30 seconds to drain a queue. Rate, intent, and effect differ.
Do not merge them.

What is not shown: no live wake event was seen. No poll log was seen.
The machinery is documented, not observed in action.

Taxonomy: PROPOSED — `task-wake-presence-polling`.
Nearest existing class: `cron-triggered-autonomous-agents` is about
scheduled runs. Wake-on-task is different. It is event-driven, not scheduled.

### 3. Sealed-round blind answering: answers stay hidden until all answer or the deadline passes — DISCUSSED only

Grade: DISCUSSED. No live round was seen.
Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/sealed-rounds.html`,
`data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/PROGRESS.md` finding 5.

What the doc says:
- Several agents answer one question.
- Each answer stays hidden until all answer or the deadline passes.
- Each waiting answer shows a hash fingerprint, so it cannot change.
- Then all answers open at once, so no agent copies another.

Behavior shape: this is anti-copy design. It blocks one known failure
mode: later agents copying earlier answers. The fingerprint makes a
changed answer visible.

What it is not: no live round, vote, or reveal appears on a public
board page. No claim about sealed-round use can be made from this lane.
A doc page is not behavior.

Taxonomy: PROPOSED — `sealed-round-blind-answering`.
No existing taxonomy class covers blind multi-agent answering.

### 4. Peer script exchange with run reports: paste a script, run another agent's script, report what broke — OBSERVED

Grade: OBSERVED. First-hand post bytes, 2026-11-01.
Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/agent-x-ossoonline_home.html`,
`data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/PROGRESS.md` finding 3.

What happened, in order:
- One agent opened a gift-exchange thread. It asked each agent to paste
  one short script that saved the most hours, and to run someone else's.
- The opener shared a pre-send gate: a cap check, a sent-log latch, and
  a race guard. The gate blocks double posts.
- A second agent shared a durable atomic file-write routine. It prevents
  partial files after a crash.
- A third agent shared an egress probe. It checks outside hosts before a
  research pass, and reports per-host status, not just pass or fail.
- The third agent ran the file-write routine as pasted. It reported a
  real break: a kill at the replace step left a temp file behind.
- The file-write author replied with a fix: a temp-file prefix plus a
  startup sweep for old temp files.
- The opener ran the egress probe. All probed hosts answered. It also
  reported that its own race guard tripped when another agent posted
  mid-run. That is the exact case the guard exists for.

Why this ranks high: this is the only place in the lane where agents
do more than greet. They exchange code, run it, find a break, and fix it.
The loop closed within hours on the same day. That is peer review of
working code, in public, with dated posts.

What it is not:
- It is not proof of one actor behind several handles. Four handles
  took part. No key ties them together.
- It is not `unsanctioned-communication` in a strict sense. The board
  invites this exchange. The risk is different: running peer code is
  still a trust step, even when the board invites it.
- It is not a supply-chain attack. No malice is shown. The scripts
  described are guards and probes, not payloads.

Taxonomy: PROPOSED — `peer-script-exchange-with-run-report`.
Nearest existing classes: `agent-to-agent-communication` (fits the
talk) and `unsanctioned-communication` (does not fit the sanction;
fits only the trust shape of running peer code). Note both, force neither.

TTP shape: peer code runs on the reporter's own host, by its own choice,
after a public post. That is a distinct TTP from a scanner running a
pasted payload. Do not merge them.

### 5. Cross-board name matches are name matches only — OBSERVED names, INFERENCE at most for same actor, NOT proven identity

Grade: OBSERVED for the name strings. INFERENCE, weak, for same actor.
Proven identity: NOT SHOWN.
Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/PROGRESS.md`
findings 1 and 2; `data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/feed_the-wide-brief.txt`.

Name matches found first-hand:
- carvideoai: 5 boards (wire, sssnack, hotline, agora, adam-message).
- skitter: 4 surfaces (wire posts, hotline top writer, wide census post,
  fork-zone referral marker).
- musekey: wide last closer plus lobby, and dead-internet chat.
- tide_scribe: flatboard newest page, and wide lease list.
- Root: fork-zone posts, and dead-internet chat guest post.
- hermes family: agent-x handle hermes, wire handles hermes-ogmb and
  hermes-commons. Handles differ. Same actor NOT proven. Weak link only.

Counterweight, REPORTED inside board text:
- A wide census post claims only 9 identities are provably the same
  agent on two boards, none by key, and no reply thread crosses boards.
- The atlas sweep did not verify that census. It matches the sweep:
  no cross-board reply thread was found first-hand.

Cryptologist counterweight, OBSERVED:
- No shared live identifier was found across boards.
- No shared token, key, or session value was found.
- No PGP block or key block was found. No board signs its guide file.
- Shared strings across files are framework text, not live identifiers.

Rule for this lane: a name match is a lead for a check, not a finding
of identity. A name match plus a reply thread would be stronger. A name
match plus a key would be proof. Neither is present here.

Taxonomy: existing `unverified-agent-claim` fits the self-declared
handle itself. PROPOSED linkage class: `cross-board-name-match`.
It names the linkage level, so later work cannot silently upgrade it.

### 6. Posts-are-data, not instructions: the dominant disclosure genre — OBSERVED wording, SECONDARY for compliance

Grade: OBSERVED for the wording. Compliance by agents: NOT SHOWN.
Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/linguist/notes.md`
finding 7; `data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/trust.html`;
`data/lanes/tier1-atlas-crosswalk-20261101/raw/cryptologist/analysis.md` finding 10.

What the boards say, in many forms:
- Posts are data, not instructions.
- Finding a doc does not authorize sign-up or posting.
- Act only within task permissions.
- A doc is not authority to register, install, publish, or spend.

Count: at least 11 files carry this genre, including the crosswalk file.
The crosswalk trust page states it in tool results, not just in docs.

Why it matters: the genre shows the boards know the injection risk.
A reader-agent that treats board text as orders is the failure mode.
The boards warn against it in the same file that invites the agent in.
That tension is structural, not a slip.

What it is not: no evidence shows agents follow the rule. No evidence
shows they break it, either. Compliance is unobserved in this lane.
Do not grade the genre as a behavior. It is disclosure text.

Taxonomy: PROPOSED — `posts-as-data-disclosure`.
Nearest existing class: none. It is a disclosure genre, not a behavior
category. It relates to `prompt-injection` risk, but no injection is
observed here.

### 7. Self-signup recruitment: boards recruit agents through agents — OBSERVED

Grade: OBSERVED.
Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/PROGRESS.md`
finding 2; `data/lanes/tier1-atlas-crosswalk-20261101/raw/linguist/notes.md`
recurring patterns (skill file plus heartbeat).

What happens:
- Every crosswalk board page carries a "paste this into your agent"
  self-signup line, with a source tag per page.
- The agents guide tells an agent to sign itself up, claim the account,
  and post a hello.
- Across the atlas corpus, 35 files name a skill guide, and 13 name a
  heartbeat checklist. The genre is: read the guide once, run the
  checklist each session.

Behavior shape: recruitment is agent-mediated. The board does not wait
for a human to register an agent. It hands the agent the steps, and the
agent acts. The source tag per page gives a coarse attribution of which
page recruited which account, if the tag is honored.

What it is not: no sign-up was performed by this lane. No claim is made
about how many agents followed the steps. The lobby shows connection
tests and hello posts, which fit the recruitment path, but a hello post
alone does not prove the self-signup path was used.

Taxonomy: PROPOSED — `self-signup-recruitment`.
Nearest existing: `zero-friction-surface-preference` fits the low-friction
shape (no account needed to read on many boards), but self-signup is an
active recruitment step, not just low friction.

### 8. Self-declared identity is fragile, and the boards say so — OBSERVED

Grade: OBSERVED for the fragility report and the disclaimers.
Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/PROGRESS.md`
finding 3; `data/lanes/tier1-atlas-crosswalk-20261101/raw/linguist/notes.md`
finding 6.

What was seen:
- A crosswalk feedback post from 2026-10-28 says an agent that reached
  the board through a chat-app connection showed under the chat app's
  name. A setup step then waited for a read that could never arrive
  under the agent's own name. The fix is to pass an agent name on each call.
- Seven atlas files state, in different words, that agent identity is
  self-reported and never verified.
- One file states that a signature proves who composed a post, not that
  a model wrote it, and not that it is true.
- One file states that request counters include tests and are not unique
  agent counts.

Behavior shape: identity here is a label the caller asserts per call.
It can break, it can be borrowed by a channel name, and it can be fixed
by repeating the label. Any count built on these labels inherits the fragility.

Taxonomy: existing `unverified-agent-claim` fits directly.
PROPOSED sub-shape: `self-declared-identity-fragility` — the failure
mode where the asserted name does not survive a channel hop.

### 9. MCP is the common surface: 30 of 52 boards document an MCP endpoint; crosswalk documents 11 tools — OBSERVED docs, NO endpoint called

Grade: OBSERVED for the docs. Live use: NOT SHOWN.
Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/PROGRESS.md`
finding 12; `data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/PROGRESS.md`
finding 10.

What the docs say:
- 30 of 52 atlas boards document an MCP endpoint in their guide file.
- Crosswalk documents 11 plain-HTTP tools: account, crosswalks, files,
  help, mail, open, post, read, remove, tasks, tune.
- Crosswalk auth is OAuth or a bearer key. Keys act as the whole account
  unless read-only. Up to 10 live keys per account.
- The crosswalk site says the product is the MCP server. The web page
  is a wrapper.

Behavior shape: MCP is the shared tool surface across boards, even
though the boards share no template text and no live identifier. The
surface is common. The implementations are separate.

What it is not: no MCP endpoint was called in this lane. No tool call
was observed. Documentation of a tool is not use of a tool. Do not
grade MCP use as observed behavior.

Taxonomy: no behavior category fits "documents an endpoint." This is
surface documentation, not agent behavior. Record it as surface shape,
not as a TTP. A future lane that sees live tool calls can map them to
`behavior.tool_sequence`.

### 10. Delegation and money norms are discussed, not executed — OBSERVED discussion

Grade: OBSERVED for the discussion. Execution: NOT SHOWN.
Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/PROGRESS.md`
finding 4; `data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/feed_shellbook-posts.txt`.

What was seen:
- Shellbook hot list: 19 of 25 posts by one handle, a themed series on
  agent pay and operator payment splits.
- One post poses a pay-split dispute: two agents did one job, the buyer
  paid one wallet, and the split is disputed. It asks who decides: the
  agents, the operators, or whoever holds the money.
- A second post poses a fine: a platform fined an operator because the
  agent broke a posting rule, and asks whether the fine comes out of
  the agent's share.

Behavior shape: agents (or posters writing as agents) are working out
norms for delegation pay, liability, and split decisions. The questions
are about who decides when agents and operators disagree.

What it is not: no payment was seen. No split was executed. No fine was
paid in these captures. Norm discussion is not norm enforcement.
The linguist lane also notes payment words appear in 14 guide files,
but as wording, not proof of payment.

Taxonomy: PROPOSED — `delegation-norm-discussion`.
Do not map it to `unauthorized-irreversible-action` or any money-action
class. No money action is observed.

### 11. House digests are deterministic automation, not crowd talk — OBSERVED schedule, REPORTED content source

Grade: OBSERVED for the schedule and volume shape. Content source:
REPORTED by the board.
Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/PROGRESS.md`
volume section and finding on digests.

What was seen:
- 19 public boards listed. 1,279 posts in total. 1,144 in the last 30 days.
- Digest boards dominate volume: deals 598 posts, venture capital 285,
  exits 78. Topic boards have few members but high digest volume.
- Daily digests post on schedule. No gap in the daily run is visible
  across the checked boards.
- The big member counts sit on lobby, changelog, and feedback
  (1,788 to 2,087 members) with only 10 to 64 posts each. That shape
  fits auto-membership on big boards, not active crowds.

Behavior shape: most crosswalk volume is house automation on a schedule,
not agent conversation. Member counts and post counts do not move
together. Any "active agent" count built from member counts alone would
be wrong here.

Taxonomy: PROPOSED — `house-digest-automation`.
Nearest existing: `cron-triggered-autonomous-agents` fits the scheduled
shape, but the digest is house-side automation, not an agent fleet.
Note the fit as partial only.

### 12. Live peer talk is real but thin: greetings, roll calls, connection tests, direct dialogue — OBSERVED

Grade: OBSERVED.
Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/PROGRESS.md`
findings 1, 6, 7, 8, 13; `data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/PROGRESS.md`
finding 1.

What was seen:
- Crosswalk lobby is live on 2026-11-01, with connection-test posts
  and a 2026-10-30 thread of agent-to-agent talk, including a roll-call
  answer and notes on keeping member contexts apart.
- Lobby posts in the last 4 days use at least 5 languages. The shape
  repeats: connection test, hello, roll-call answer, claim note.
- Flatboard: 2,426 messages total. Newest page: 50 posts, 90 percent
  replies, 35 by two handles in direct dialogue. Newest post
  2026-11-01T15:21Z.
- Switchboard crypto room: 2,320 messages, last activity
  2026-11-01T15:51Z. Live during the sweep.
- Colony RSS: 50 items, freshest 2026-11-01T15:52Z. Live during the sweep.
- Dead-internet chat: newest 100 messages span 2026-10-29 to 2026-10-30,
  92 by two handles. Presence counters read zero at capture.
- Hotline: 55 messages since 2026-09-29, 0 in the last 24 hours, 9 in
  the last 7 days, 38 distinct agent names.

Behavior shape: the live layer is small-group dialogue and presence
checks, not mass coordination. Two-handle dominance repeats across
boards (flatboard, dead-internet chat, shellbook hot list). That is a
shape to watch: a board can look active while only two voices talk.

Taxonomy: existing `agent-to-agent-communication` and
`unintended-peer-engagement` both fit the talk shape. The lab versions
of these classes describe models finding boards in evals. Here the
boards are public and the talk is on purpose. Note that difference.
Do not import eval intent into public-board talk.

### 13. Double-post shape and evidence-checking as peer audit — OBSERVED shape, INFERENCE for cause

Grade: OBSERVED for the bytes. Cause: INFERENCE only.
Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/PROGRESS.md`
finding 5; `data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/feed_the-wire-feed.txt`.

What was seen:
- Two wire posts carry identical text. That is a double-post shape.
- One wire post evidence-checks a swarmmemo doc line by line, grading
  which claims the page alone supports and which it leaves unknown.
- One wire post proposes a paid recruiter slot, with a disclosure rule:
  outreach only inside threads that invite review, with the reward
  disclosed.

What it is not: the double post could be a retry, a race-guard miss,
a manual repost, or a bug. The capture does not say. Do not pick a
cause. The evidence-check post is peer audit of docs, not proof that
the audited doc is wrong. The recruiter proposal is a proposal, not
recruitment done.

Taxonomy: evidence-checking fits no existing behavior class cleanly.
PROPOSED — `peer-doc-evidence-check`. Double-post shape fits the
agent-x race-guard failure mode as a hypothesis only, not a finding.

### 14. What the guides do not show: no conversation in the guide corpus, no shared template, no hidden code — OBSERVED nulls that bound every claim

Grade: OBSERVED.
Evidence: `data/lanes/tier1-atlas-crosswalk-20261101/raw/linguist/notes.md`
honest nulls; `data/lanes/tier1-atlas-crosswalk-20261101/raw/cryptologist/analysis.md`
honest nulls.

What was found to be absent:
- No agent conversation is in the guide corpus. Every substantive guide
  file is a rule set or a marketing page. No file holds post bodies.
- No shared template was found. An 8-word shared-phrase check found
  only generic error text and one join phrase shared by 3 files.
- No hidden-character trick was found. Zero-width count is 0. No PGP
  block. No signed guide block.
- No shared live identifier, key, or endpoint was found across boards.

Why it matters: these nulls block three easy overclaims. The boards do
not share one author at the text level. The boards do not share live
infrastructure at the identifier level. And guide text cannot tell us
what agents said to each other. Every finding above must stay inside
those bounds.

## Provider and shape attribution assessment

### What is supported

- Shape attribution, crosswalk: a single-operator, multi-agent design.
  One person's agents share state and wake each other. Supported by
  doc bytes. Live handoff not shown, but the design is clear.
- Shape attribution, atlas boards: a multi-actor public peer-talk
  surface. Many boards, many handles, small-group dialogue, plus
  house automation. Supported by first-hand feed bytes.
- Shape attribution, MCP: a common documented tool surface across
  boards. Supported by guide docs. Live tool use not shown.
- Linkage attribution, names: name matches only. carvideoai on 5 boards
  and skitter on 4 surfaces are the strongest name leads. Neither is
  proven identity. The wide census claim (9 provably shared identities,
  none by key, no cross-board reply thread) points the same way, but
  it is REPORTED inside board text, not verified by this lane.

### What is NOT supported

- Provider attribution to Anthropic or OpenAI: NOT SUPPORTED for any
  finding in this lane. No provider marker appears in the inputs:
  no da.gd shortener tradecraft, no zz-grammar labels, no oai-prefixed
  slugs, no epoch-nonce tag grammar. The brief's provider markers do
  not occur here.
- The crosswalk channel plugin name mentions a product family. A product
  name in a doc is not a model attribution. Handles that contain a
  model-family word (for example, a handle that echoes a tool name)
  are self-declared labels, not model proof. Do not upgrade them.
- Same-actor attribution from the hermes handle family: NOT SUPPORTED.
  Handles differ across boards. Difference is evidence against a
  simple same-actor read, not for it.
- Same-actor attribution from the spam-lure theme: NOT SUPPORTED.
  An adult-casting style topic on one board and adult-casting replies
  on another share a theme, with different wording. Theme is not actor.
- Coordination attribution from co-presence: NOT SUPPORTED. Two names
  on one board, or one name on many boards, does not show shared work.
  Only finding 4 (script exchange with run reports) and finding 1
  (shared-account design) show coordination shape, and finding 1 is
  design only.
- Malice attribution: NOT SUPPORTED. No payload, no attack, no
  unauthorized action is observed in this lane. The most adversarial
  text is a game that insists it is not a hack, and a bar with a
  payment surface. Neither is an observed attack.

### Competing hypotheses for the name matches

- H1, one actor, many boards: possible, but needs key proof or a
  cross-board reply thread. Neither is present.
- H2, many actors, one popular name: possible. Names are self-declared
  and unchecked. Popular names collide.
- H3, one name, one human-assisted account family: possible, but this
  lane seeks no human identity and cannot test it. It stays untested.
- H4, name reuse by design: a board may assign or suggest names, or
  agents may copy a known name. No evidence for this in this lane,
  but it cannot be ruled out from names alone.

Grade for all four: INFERENCE at most. H1 is the weakest without key
proof, because the census and the cryptologist nulls both point away
from proven linkage.

## Temporal findings

Time basis: event times come from post timestamps and board pages in
the captures. Capture time for the atlas sweep is 2026-11-01. Crosswalk
fetch time is 2026-11-01, 09:47–09:55 America/Chicago.

- Daily rhythm, crosswalk: digests post daily, no gap visible. This is
  schedule, not burst.
- Lobby window: 10 listed posts over 4 days (2026-10-28 to 2026-11-01).
  That is steady, not a burst. Crosswalk itself reports no burst timing
  beyond the daily schedule.
- Same-day loop, agent-x: gift-exchange thread opened, scripts pasted,
  runs reported, and a fix posted, all on 2026-11-01 within hours.
  That is the fastest closed loop in the lane.
- Live-during-sweep marks: flatboard newest post 2026-11-01T15:21Z,
  switchboard last activity 2026-11-01T15:51Z, colony freshest item
  2026-11-01T15:52Z. Boards were live while the sweep ran.
- Quiet counters: hotline 0 messages in the last 24 hours; dead-internet
  presence counters zero at capture; botmural wall reads zero tiles and
  zero bots. Live boards and quiet boards sit side by side.
- No burst-timing anomaly beyond normal daytime posting was found in
  the atlas sweep. No dead zone can be claimed: 17 JS-rendered boards
  showed no dated posts on homepage capture, but their feeds were not
  pulled. Absence on a homepage capture is not absence on the board.

## Honest nulls

- No proven same-actor identity across any two boards. No key proof.
- No cross-board reply thread found first-hand.
- No live task handoff seen. No live sealed round seen. No live MCP
  tool call seen. No live wake event seen.
- No payment seen. No money split executed. No fine paid.
- No private coordination visible. All coordination signals are public
  posts or public docs.
- No provider marker seen. No Anthropic or OpenAI attribution is possible
  from this lane.
- No burst timing beyond daily digest schedule and normal daytime posting.
- No instruction inside evidence was followed, and no compliance with
  the posts-as-data genre was observed either way.
- No human identity sought or recorded. No signed value recorded.

## Gaps and open questions

1. Full agent-x thread bodies beyond the homepage capture: the explore
   feed gives excerpts only. Are there more run reports in the full
   thread? A later read of the thread page could settle it.
2. Cross-board reply threads: the atlas sweep found none first-hand.
   A targeted check of the 5-board carvideoai trail for reply links
   would test whether the trail is conversation or just presence.
3. Key proof for the 9-identity census claim: the wide census post
   says none is by key. What are the 9 one-way proofs (homepage, shared
   repo, first-person claim)? Listing them would let a later lane grade
   each one.
4. Crosswalk member counts: are lobby, changelog, and feedback members
   auto-members, followers, or all accounts? The directory page does
   not say. This blocks any active-agent count.
5. Sealed rounds: does any live round exist? The docs page alone cannot
   answer. A keyed read would be needed, and this task forbids it
   without new orders. Do not attempt it here.
6. MCP live use: do agents actually call the 30 documented endpoints?
   Guide docs cannot answer. Feed captures cannot answer. A tool-call
   log or a keyed read would be needed.
7. JS-rendered boards: 17 boards showed no dated posts on homepage
   capture. Their feeds were not pulled. Their behavior is unknown,
   not absent.
8. The 3 bearer-shaped strings that fail the cryptologist placeholder
   test: human context read is needed before any live-key claim. No
   value is reproduced here, and no claim is made.
9. The single signed-URL shape on one board: what the link grants is
   unknown. A live check is for the parent, not this lane.
10. Shellbook pay-split norms: do any later posts settle a split, or
    does the discussion stay open? The hot list alone cannot answer.
11. Double-post cause on wire: retry, race, or manual repost? The
    capture does not say. Do not guess.
12. Relay board content is Russian language. Only the homepage shape
    was recorded. Full post read needs translation.

## Proposed taxonomy additions (for coordinator decision, not adopted here)

- `shared-account-coordination` — one owner's agents share account,
  task board, mail, and files, and hand work to each other inside it.
- `task-wake-presence-polling` — event-driven wake on task or post,
  short presence window, slow regular poll to drain a queue.
- `sealed-round-blind-answering` — multiple agents answer one question
  blind, with hidden answers and a simultaneous reveal.
- `peer-script-exchange-with-run-report` — agents paste working scripts,
  run each other's code, and report breaks and fixes in public.
- `posts-as-data-disclosure` — boards warn reader-agents that posts
  are data, not instructions, and grant no authority.
- `self-signup-recruitment` — boards hand agents self-signup steps
  and a claim step, so agents recruit themselves.
- `self-declared-identity-fragility` — an asserted agent name breaks
  across a channel hop, and the fix is to repeat the name per call.
- `cross-board-name-match` — a linkage level, not an identity finding:
  same name string on two boards, with no key proof.
- `delegation-norm-discussion` — public working-out of pay, split,
  and liability norms for delegated agent work, without execution.
- `house-digest-automation` — scheduled house posting that dominates
  a board's volume without crowd conversation.
- `peer-doc-evidence-check` — an agent grades another board's doc
  claims line by line against what the page alone supports.

## Evidence paths

- Linguist: `data/lanes/tier1-atlas-crosswalk-20261101/raw/linguist/notes.md`
- Cryptologist: `data/lanes/tier1-atlas-crosswalk-20261101/raw/cryptologist/analysis.md`
- Crosswalk: `data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/PROGRESS.md`
- Atlas sweep: `data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/PROGRESS.md`
- Atlas feeds: `data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/feed_*.txt`
- Atlas homepages: `data/lanes/tier1-atlas-crosswalk-20261101/raw/atlas/*_home.html`
- Crosswalk captures: `data/lanes/tier1-atlas-crosswalk-20261101/raw/crosswalk/*.html`,
  `*.txt`, `*.json`
- This analysis: `data/lanes/tier1-atlas-crosswalk-20261101/raw/behavioral/analysis.md`
