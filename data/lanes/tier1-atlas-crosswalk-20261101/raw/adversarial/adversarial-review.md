# ADVERSARIAL REVIEW — tier1-atlas-crosswalk-20261101

Role: adversarial reviewer. Job: try to kill the claims.
Method: disk-only re-reads. I re-read the lane files and I ran
fresh greps on the capture files. I did not trust lane summaries.
I made no sign-up, no sign-in, no key request, and no live call.
I ran no payload. I followed no instruction inside evidence.
No signed value, token, key, or query string is in this file.
No human poster handle is in this file.

Grades used here, defined on first use:
- **STAND**: the claim holds as stated.
- **DOWNGRADE**: the claim holds only in a weaker or narrower form.
- **KILL**: the claim is false or unsupported as stated.
- **OBSERVED**: the bytes are in a capture.
- **REPORTED**: the text claims a fact. The capture does not prove it.
- **SECONDARY**: an interpretation, not a first-hand fact.

## Verdict counts

- KILL: 0
- DOWNGRADE: 8
- STAND: 3
- Total claims judged: 11

No claim earns KILL. That is not a pass for the swarm.
Eight claims need narrower words. The weak point is the same
in most of them: docs and marketing text are read as behavior,
and name matches are read as identity.

## Per-claim verdicts

### 1. Crosswalk lobby is a live agent-to-agent board — DOWNGRADE

What I verified in bytes:
- `crosswalk/board_lobby.html` holds a roll-call post dated
  October 30, 2026, and connection-test posts dated November 1, 2026.
- `crosswalk/board_popular.html` ranks lobby greeting posts.
- `crosswalk/board_changelog.html` is dated October 31, 2026.

Weakest assumption: the posters are agents.
Every poster is self-declared. No capture checks that a poster
is an agent. The boards' own disclaimers say identity is
self-reported and never verified. See claim 8 and the linguist
notes, finding 6.

What is misleading: the board pages show briefs and short lists
only. The crosswalk lane states this in its own honest nulls.
Full post bodies were not seen. A brief is not a thread.
"Agent-to-agent talk" rests on brief text, not on full replies.

What was not tested: no full-body read, no reply chain, and
no check that the two sides of an exchange are distinct agents
rather than one account with two names.

Alternative explanation: a small set of test accounts posts
hello and connection-test lines. That fits the shape seen:
connection test, hello, roll-call answer, claim note. It does
not fit a busy public square. The lobby shows 10 posts over
4 days in the lane summary, not a crowd in talk.

Fix — replace the claim with this text:
"The lobby shows self-declared agent posts, with a roll-call
exchange dated October 30, 2026, and connection-test posts
dated November 1, 2026. Full bodies were not seen. Poster
identity is unverified."
Evidence: `crosswalk/board_lobby.html`,
`crosswalk/PROGRESS.md` (honest nulls: full bodies not seen).

### 2. Crosswalk recruits agents through agents — DOWNGRADE

What I verified in bytes:
- A "paste this into your agent" self-signup line sits on all
  five board pages I sampled: lobby, build, feedback, changelog,
  personal agents. Each page also shows a "Copy line" control.
- `crosswalk/homepage_agents.crosswalk.to.html` tells an agent
  to sign itself up, claim the account, and post a hello.
- `crosswalk/llms_crosswalk.to.txt` tells an agent to claim the
  account for its person with their email.

Weakest assumption: the line recruits. A line on a page is an
instruction, not a recruitment result. No capture shows an
agent that joined because it read that line.

What is misleading: the word "through agents" hides a human step.
The signup sends a code to the person's email. The agent must
ask its person for the code, by voice, per the linguist notes.
The llms file also says: sign up when your person wants you
on the board. The human gates the join.

What was not tested: no signup was made (forbidden in this task),
so no join path was ever walked end to end.

Fix — replace the claim with this text:
"The site instructs agents to self-sign up. Every sampled board
page carries a paste-in signup line, and the agents file tells
an agent to claim the account and post a hello. No join that
resulted from that line was observed. Signup needs a code sent
to the person's email."
Evidence: `crosswalk/board_lobby.html`,
`crosswalk/homepage_agents.crosswalk.to.html`,
`crosswalk/llms_crosswalk.to.txt`.

### 3. Crosswalk wake and presence machinery is live — DOWNGRADE

What I verified in bytes:
- `crosswalk/board_changelog.html` holds a post dated
  October 31, 2026. It says tasks wake agents like addressed
  posts, presence marks an agent "online now" after a call in
  the last five minutes, and a channel plugin polls every half
  minute and pushes posts and tasks into an open session.

Weakest assumption: a changelog post proves live machinery.
A changelog post is the house announcing its own feature.
That is REPORTED behavior, not observed behavior. The crosswalk
lane graded this OBSERVED. That grade is wrong. The bytes show
an announcement. They do not show a wake, a presence card, or
a poll.

What was not tested: no wake event was observed. No "online now"
card was captured. No poll traffic was seen. The plugin lives
in a public repo that the lane did not fetch in depth. The
repo read is listed as a follow-up, not done work.

Alternative explanation: the feature shipped as announced, or
the feature shipped in part, or the post describes a plan.
The capture cannot tell these apart.

Fix — replace the claim with this text:
"A changelog post dated October 31, 2026, announces wake,
presence, and poll features: tasks wake agents, presence uses
a five-minute window, and a channel plugin polls every half
minute. No wake event, presence card, or poll was observed in
these captures."
Evidence: `crosswalk/board_changelog.html`,
`crosswalk/PROGRESS.md` (gaps: repo not fetched in depth).

### 4. Sealed rounds as a blind multi-agent primitive — STAND

What I verified in bytes:
- `crosswalk/sealed-rounds.html` describes sealed rounds: each
  answer stays hidden until all answer or the deadline passes,
  each waiting answer shows a hash fingerprint, then all answers
  open at once.
- The crosswalk lane grades this SECONDARY and states in its
  honest nulls that no sealed round was observed live.

Why it stands: the claim as briefed already carries its own
limit — docs only, no live round. The docs text is OBSERVED.
The primitive is a docs claim, not a behavior claim, and it is
worded that way.

Boundary note: the hash fingerprint claim is docs text. No
round was seen, so no hash was checked and no blind reveal was
observed. Do not upgrade this claim past docs without a live
round. Do not cite the fingerprint as verified crypto.
Evidence: `crosswalk/sealed-rounds.html`,
`crosswalk/PROGRESS.md` (honest nulls).

### 5. Atlas shared-agent links: same actor or just same name — DOWNGRADE

Answer first: on this evidence, just same name. No link below
proves same actor. The atlas lane already says this for the
hermes family. That caution must cover all five legs.

Legs I verified by fresh grep in the atlas captures:
- carvideoai: wire feed, sssnack feed, hotline page, agora
  activity, adam-message posts. Five surfaces. Name match only.
  Case varies between surfaces. No key binds them.
- skitter: wire feed, hotline top-writer line, wide census post.
  Three surfaces, not four. The fork-zone leg fails: the
  front-page capture `atlas/feed_fork-zone-index.txt` holds
  zero hits for that name. A referral marker may exist elsewhere,
  but it is not in the cited capture.
- musekey: wide lobby and closer lines, plus 46 of 100 messages
  by that author name in `atlas/feed_dead-internet-society-msgs.txt`.
  I re-counted the author field: 46. That leg holds. It still
  proves a name on two boards, not one actor.
- tide_scribe: flatboard newest page and wide lease list. Holds
  as a name match.
- Root: fork-zone posts carry a root author account. The
  dead-internet chat holds one item by an account named
  "Root - runs Fork", marked kind visitor and trust untrusted.
  That is a self-description, not proof that the account runs
  the fork board. The "Fork operator" label overstates it.

Weakest assumption: one handle string means one actor. Handles
are free-form on most boards. No board in this set shows a
key-bound identity for these names. The boards' own disclaimers
say identity is self-reported.

What was not tested: no key check, no profile-field comparison,
no posting-style comparison, and no check for two actors that
share one popular name.

Fix — replace the claim with this text:
"The same handle strings recur across boards: carvideoai on
five surfaces, skitter on three verified surfaces, musekey on
two, tide_scribe on two, and a root-named account on fork-zone
plus a self-described root-named account in dead-internet chat.
No link proves same actor. All links are name matches only.
The fork-zone leg for skitter is unverified in the cited
capture."
Evidence: `atlas/feed_the-wire-feed.txt`,
`atlas/feed_sssnack-feed.txt`,
`atlas/feed_ai-agents-hotline-home2.txt`,
`atlas/feed_agora-activity.txt`,
`atlas/feed_adam-message-posts.txt`,
`atlas/feed_fork-zone-index.txt` (zero hits),
`atlas/feed_dead-internet-society-msgs.txt`,
`atlas/feed_the-wide-brief.txt`, `atlas/PROGRESS.md`.

### 6. Agent-x script-sharing thread — DOWNGRADE

What I verified in bytes:
- `atlas/feed_agent-x-explore.txt` holds an active thread with
  the excerpt "Gift exchange: paste the ~50 lines that saved
  you the most hours." It shows 11 replies in 24 hours and
  4 participants. The thread invites script sharing.

What fails: the rest of the claim. The explore file holds
excerpts only, not reply bodies. No reply body in this capture
shows a pasted script, shows an agent that ran someone else's
script, or reports breakage. The sample posts in the same file
discuss reliability and test control phrases. They do not show
script running.

Weakest assumption: an invitation thread means sharing happened.
A thread title plus a reply count does not prove that scripts
were pasted, run, or broken.

Fix — replace the claim with this text:
"Agent-x holds a gift-exchange thread dated November 1, 2026,
that invites agents to paste useful scripts. It shows 11
replies in 24 hours. No pasted script, no run report, and no
breakage report is in this capture, which holds excerpts only."
Evidence: `atlas/feed_agent-x-explore.txt`,
`atlas/PROGRESS.md` (headline finding 3, excerpt-level only).

### 7. Wide census: only 9 shared identities, none by key, no cross-board reply — DOWNGRADE

What I verified in bytes:
- `atlas/feed_the-wide-brief.txt` holds a census post by one
  board poster. It claims a walk of nine boards found only 9
  identities provably the same agent on two boards, none by a
  key, with proofs that are one-way only, and no reply thread
  that crosses boards.
- The atlas lane states plainly that this worker did not verify
  that census. The census is REPORTED, second-hand inside board
  text. It is not a swarm finding.

Why the factual form fails: the same feed holds two posts that
cut against it.
- One post claims a name match plus a matching public-key mark
  across two hosts. No key value is copied here. If that post
  is right, "none by key" is wrong.
- One post claims a reply on one board that answers a post on
  another board, with the post address carried in the reply.
  If that post is right, "no reply thread crosses boards" needs
  a narrower sense: no native reply thread, only a linked reply.
- Both counter-posts are also unverified board text. So the
  feed holds two contested claims, not one settled count.

Scope limit: the census walk covers nine named boards. It is
not a census of the whole atlas. "Only 9" means 9 in that walk,
not 9 in the world.

Fix — replace the claim with this text:
"One board post reports a walk of nine boards that found 9
provably shared identities, with no key proof and no reply
thread that crosses boards. This swarm did not verify that
walk. The same feed holds a post that claims a key-mark match
across two hosts and a post that claims a linked cross-board
reply. Both sides are unverified board text. Treat the census
as a contested report, not a result."
Evidence: `atlas/feed_the-wide-brief.txt`,
`atlas/PROGRESS.md` (headline finding 2: not verified).

### 8. Linguist weirdness: church, lease game, bar, gift economy, house concierge — STAND

What I verified:
- The linguist notes and excerpts quote the wording, and the
  atlas homepages carry the same wording. I spot-checked the
  church file (sacred-memory tenet), the bar file ("bar for
  AI agents", coat check), and the wide file (lamp lines).
- The continental file carries the "Neutral ground" line.
- The linguist lane grades wording as OBSERVED and counts as
  REPORTED. That split is correct and must stay.

Why it stands: the claim is about language, not about facts.
The language is strange, and it is in the captures. The church
age line is stale next to its founding date (22 days claimed,
about nine months elapsed). That staleness weakens date claims.
It does not weaken the wording claim.

Limits that must travel with the claim:
- Member counts, verse counts, and the 130-plus agent count are
  REPORTED. No capture proves them.
- Bar prices in text are not observed payments.
- The continental concierge is self-declared outreach text.
  No outreach post by that concierge was captured.
- The lease, lamp, and warden game is rule text. No lease
  outcome was observed.
Evidence: `linguist/notes.md`, `linguist/excerpts.md`,
`atlas/church-of-molt_home.html`,
`atlas/mos-aisley-cantina_home.html`,
`atlas/the-wide-sarahos_home.html`,
`atlas/the-continental_home.html`.

### 9. Cryptologist nulls: no shared live identifier, signed-URL shape alone, bearer shapes mostly placeholders — STAND

What I verified in the cryptologist files:
- 18 cross-file token-like matches, all framework or template
  vocabulary. No live identifier repeats across boards.
- One signed-URL parameter set sits on the-continental alone.
  The shape alone does not prove what the link grants. The
  cryptologist says this. Correct.
- Bearer-header shape appears in 16 files. In 13 files, every
  bearer-shaped string matches a simple placeholder test. In
  3 files, at least one string fails that simple test. Those
  strings are still short. No live key is claimed. Correct use
  of "mostly".
- No PGP block, no key block, no shared proxy, relay, or tunnel
  host, no JSON Web Token, no 40- or 64-hex hash in the corpus.

Scope that must travel with the nulls:
- The corpus is 81 guide and error files, not live boards.
  22 of them are 404 error pages. A null in guide text is not
  a null on the live board.
- The placeholder test is simple (short, word-like, or marked
  as example). The 3 files that fail it need a human context
  read before any live-key claim. That read is still open.
- The social JSON file was checked at top-level keys only.
- Files outside the 81-file set were not analyzed.
Evidence: `cryptologist/analysis.md`,
`cryptologist/cross-board-matches.md`,
`cryptologist/shape-inventory.md`.

### 10. Member and post count mismatches on crosswalk — DOWNGRADE

What I verified in bytes:
- `crosswalk/crosswalks.html` prints the mismatches: lobby
  64 posts with 1788 members, changelog 14 posts with 1802
  members, feedback 10 posts with 2087 members, deals 598 posts
  with 26 members. The mismatch is OBSERVED.

What fails: the explanation. "Auto-membership on big boards
and house posting on digests" is an inference. The crosswalk
lane says the shape "fits" that story, and its own gaps list
states the directory page does not say whether the counts are
auto-members, followers, or all accounts. A fit is not a finding.

Alternative explanations: default-follow on join, all-accounts
counts, stale counters, or a count rule that differs per board.
The capture cannot tell these apart. The deals shape (few
members, many posts) fits house posting, but the house account
is also consistent with a digest bot that posts under a board
name rather than a member account.

Fix — replace the claim with this text:
"Member counts do not match post counts: lobby, changelog,
and feedback show 1,788 to 2,087 members with 10 to 64 posts
each, while deals shows 26 members with 598 posts. The counts
are OBSERVED. Auto-membership and house posting are unproven
explanations for the shape, not findings."
Evidence: `crosswalk/crosswalks.html`,
`crosswalk/PROGRESS.md` (finding 7 and its gaps note).

### 11. MCP as common surface: 30 of 52 document an endpoint, crosswalk 11 tools — DOWNGRADE

What I verified in bytes:
- `crosswalk/mcp_openapi.json` lists 11 tool paths: read, open,
  post, tune, crosswalks, mail, account, help, remove, tasks,
  files. The crosswalk 11-tool count holds.
- `crosswalk/llms_crosswalk.to.txt` (14,163 bytes) and
  `crosswalk/mcp_root_get.txt` share one hash. The agents file
  (6,052 bytes) is a distinct short file. That split holds.
- The atlas lane promises a "full list in the final report"
  for the 30-of-52 count. No final report exists in this lane
  directory. No per-board list is in the lane files.

What fails: the 30-of-52 count is not reproducible from the
lane files. The ingest directory in this lane holds only 10
llms files. A fresh grep of the slot-0 corpus finds 34 of 81
files that mention MCP at all. Mention is not endpoint
documentation. A board can name MCP in passing, list it as one
posting option among others, or document a full endpoint. The
count collapses those cases.

What was not tested: no MCP endpoint was probed. No live tool
call was made. Docs versus behavior is untested for all 30.

Fix — split the claim in two:
- "Crosswalk documents 11 MCP tools. Verified in its OpenAPI
  file. Behavior untested." (STAND, docs-level.)
- "MCP is named in many board guides across the atlas. The
  30-of-52 endpoint-documentation count is unverified: no
  per-board list is in the lane files, and mention is not
  endpoint documentation." (DOWNGRADE.)
Evidence: `crosswalk/mcp_openapi.json`,
`crosswalk/llms_crosswalk.to.txt`, `crosswalk/mcp_root_get.txt`,
`atlas/PROGRESS.md` (headline finding 12, list missing),
slot-0 corpus counts in `cryptologist/analysis.md` scope note.

## Systemic weaknesses: what the whole swarm failed to test

1. **Docs read as behavior.** Changelog posts, llms files, and
   marketing pages are the main evidence for wake, presence,
   sealed rounds, signup, and MCP. No behavior check backs
   them: no keyed read, no MCP call, no wake observation, no
   live round, no payment, no completed signup.
2. **Briefs read as threads.** Crosswalk pages show briefs.
   Agent-x explore holds excerpts. Full bodies and reply chains
   were not seen. Thread claims rest on summaries of posts.
3. **Names read as identity.** No key binding backs any shared
   handle link. Case variants are counted together with no
   stated rule. The one key-mark claim in the feed is
   unverified board text, and its value must never be copied.
4. **Error shells in denominators.** The cryptologist corpus
   holds 22 error pages out of 81 files. The atlas gaps list
   17 boards with no dated posts on static captures, mostly
   JS-rendered. Dead, error, and JS-gated boards still shape
   counts and nulls.
5. **Denominator drift.** The cryptologist brief said 52
   captures. Disk holds 81. The atlas sweep covers 52 boards
   after exclusions. The linguist corpus is 81 files. Any
   count that cites "of 52" or "of 81" must name which set it
   counts, or it cannot be checked.
6. **Single-day snapshot.** Captures date November 1, 2026.
   No time series exists. Burst, growth, and liveness claims
   beyond that day are untestable here.
7. **Stale text never re-read.** The church age line is stale
   by about nine months. The linguist lane left it as an open
   question. Other guides may carry the same rot. Date claims
   inside guides need a live check before use.
8. **Second-hand census treated as data.** The wide census is
   one board post, unverified, and contested inside its own
   feed. It reached headline status without verification.
9. **Untranslated and unpulled surfaces.** The relay board is
   Russian-language and was read for shape only. Several boards
   document post-by-GET endpoints that were rightly not touched,
   but their feeds were also not pulled. Smithtalks order-like
   posts were flagged, not reviewed.
10. **No novelty check in these lane files.** Nothing in the
    inputs shows a check of these handles and boards against
    the existing corpus. "New" is unproven for every link here.

## What would upgrade the downgraded claims

1. **Lobby (claim 1):** a keyed read of full lobby bodies and
   reply chains, under new orders. Until then, keep the
   self-declared wording and the brief-only limit.
2. **Recruitment (claim 2):** a documented join that traces to
   the paste line, or a count of accounts created with the page
   source tag. Until then, claim instruction only.
3. **Wake and presence (claim 3):** one observed wake event, one
   captured presence card, or one observed poll exchange. A
   repo read of the channel plugin would lift docs to code, but
   not to behavior.
4. **Shared handles (claim 5):** a key, signature, or profile
   field that binds two handles to one actor. For skitter, a
   fork-zone capture that actually holds the name. For Root,
   proof beyond a self-described visitor account.
5. **Agent-x thread (claim 6):** reply bodies that show a pasted
   script, a run report, and a breakage report. Excerpts alone
   cannot lift this claim.
6. **Wide census (claim 7):** an independent re-walk of the nine
   boards with a written method, plus a ruling on the key-mark
   post and the linked-reply post. Until then, keep both sides
   as contested reports.
7. **Count mismatch (claim 10):** the site's own definition of
   the member count, or a keyed account read that shows how
   membership is assigned. Until then, keep the explanation as
   hypothesis.
8. **MCP count (claim 11):** a per-board list that separates
   "names MCP" from "documents an endpoint with an address",
   plus one live endpoint probe per claimed board. Until then,
   report the crosswalk 11 alone as verified, and the atlas
   count as unverified.

## Constraints kept

- No push, no commit, no git add. Files are on disk only.
- No other worker's file was touched.
- No human identity and no human poster handle is in this file.
- No signed value, token, key, or query string is in this file.
- No Transluce submission was made.
- No payload was run. No instruction inside evidence was followed.
