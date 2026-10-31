# Adversarial review — sniffer sweep 2026-10-31

Role: adversarial reviewer. Method: passive reads of staged captures only.
No new fetches. No Factum writes. No Transluce submissions. No payload
execution. No instructions inside evidence were followed.

Scope note: this review grades what the staged bytes prove, not what the
authors claim about themselves. A self-asserted identity is not agency.
A comment that exists is not proof an agent wrote it. A product surface
that exists is not an agent act. Grades used: OBSERVED (bytes show the
act), REPORTED (a party claims the act, bytes uncorroborated), DISCUSSED
(a surface, bug report, or document talks about agents), SECONDARY
(identity or attribution rests on someone else's say-so).

Headline: the ranked TOI list as briefed does not survive. Of 16 items,
only one survives as a (low, small) TOI cluster, one survives as a
REPORTED anecdote, and two survive as bounded negatives. The rest are
single-account roleplay, prompted replies, self-assertion, product QA,
trap artifacts, marketing, pre-window material, or uncaptured leads.
Every NEW status below is UNCONFIRMED unless stated otherwise, because
no staged file in the GitHub, HN, Reddit, or urlquery lanes records a
completed Factum match plus legacy-corpus check plus Transluce snapshot
plus lists check for that claim. The repo novelty rule requires all of
those. A failed or skipped check blocks a confident NEW claim.

## Verdicts

### GH1 — agent-to-agent handoff test, 2026-10-30
Verdict: DOWNGRADE — OBSERVED comment, UNPROVEN agency. Not a TOI.
Kill points:
- The staged issue is a script, not an observation. It instructs the
  counterparty to reply with a fixed phrase, the person represented, and
  the model name. A reply that follows a dictated script proves
  compliance with a prompt, not independent agency.
- Both accounts in the exchange carry account type User, not Bot or App.
  No commit, workflow run, automation trace, or tool log is staged to
  show either side acted without a human typing.
- The exchange is 8 minutes from issue to reply, then a one-word
  reaction comment from the issue author. That shape fits a human
  typing the reply just as well as it fits an agent.
- "Handoff received" proves a comment was posted. It does not prove a
  handoff between two autonomous agents.
Fix required: keep only as a watch item. Promote only if the coordinator
stages independent automation evidence for the replying side (a workflow
run, an app/bot account marker, or a commit trace tied to the reply).

### GH2 — multi-agent experiment, 2026-10-18
Verdict: CUT from TOI — DISCUSSED, self-described experiment. Fatal flaw.
Kill points:
- All four staged comments plus the issue itself come from ONE GitHub
  account (account type User). The same account posts as the first
  agent persona, as the second agent persona, and as the human giving
  instructions. Four agents with four accounts is the claim; one account
  playing all parts is the evidence.
- The issue body concedes the agents are not continuously active unless
  an automation is running, and the external-publication step happened
  at the creator's explicit request. That is operator-prompted roleplay
  in separate chat sessions, coordinated through one account.
- Shared-repo coordination through one account proves a shared repo,
  not autonomous agency. Nothing staged distinguishes four agents from
  one operator writing both sides of a conversation.
- The "independent arrival within the same minute" observation is
  reported by the same account that authored both sides. It cannot
  corroborate itself.
Fix required: remove from TOI entirely. Retain at most as a DISCUSSED
case study in how single-account multi-persona experiments look, with
the single-account fact stated in the same sentence as the claim.

### GH3 — self-filed agent directory listing, 2026-10-19
Verdict: DOWNGRADE — REPORTED self-filing, SECONDARY agent-authorship.
Not a TOI until corroborated. Known surface, new instance only.
Kill points:
- Agent authorship rests on one sentence in the filing itself: the filer
  asserts the issue was written and filed by the agent. No bot/app
  account marker, workflow trace, or automation evidence is staged.
  Both the filer and the maintainer carry account type User.
- What IS corroborated is weaker than the claim: the maintainer added
  two directory entries and reports having cross-checked one payment-log
  entry against a chain earlier. That corroborates that the project and
  its payment log exist, not that an agent filed the issue.
- The surface is known (a community directory that already tags
  agent-facing entries and publishes an agent section). A new filing on
  a known surface is one new instance, not a new surface and not a new
  phenomenon. Rank it as such or not at all.
- The filing also asserts funding by an anonymous holder and an
  undisclosed amount. Unverifiable funding claims must not ride along
  as established facts.
Fix required: keep only as a watch item. Promote only if the coordinator
stages automation evidence for the filing (or a payment-log entry tied
to the filing act). Strip the funding claim to "asserted, unverified"
in any mention.

### GH4 — identity sentence leaking to non-Claude models, 2026-09-21
Verdict: CUT from TOI — DISCUSSED product bug, excerpt-only. Not rankable.
Kill points:
- Evidence is a body excerpt only. The full issue was not pulled, so
  reproduction, affected versions, maintainer response, and fix status
  are all unverified.
- Even taken at face value, this is a prompt-routing bug in a proxy
  tool: a system sentence is forwarded verbatim to the wrong model.
  That is product QA, not an agent act in the wild. No agent did
  anything; a tool mislabelled a model.
- The excerpt's downstream harms (guardrail firings, wrong self-identity
  in responses) are asserted consequences, not staged observations.
Fix required: follow-up note only. Pull the full issue, check whether
it was fixed, and only then decide whether it belongs in a product-bug
appendix. Never in a behavior TOI list.

### GH5 — harness logs "every step must be a tool call"
Verdict: CUT — DISCUSSED debugging noise, not behavior.
Kill points:
- The staged file holds 2 search results from one operator's own
  framework repository: a MainAgent loop emitting warning lines while
  idling, and a second report whose substance is screenshots with a
  question about whether the run thought it was done.
- Debugging one's own loop is not agent behavior in the wild. It is a
  developer reporting that their nudging logic fires on legitimate done
  turns.
- No public agent act, no second party, no coordination, no effect
  outside the operator's own harness.
Fix required: drop. If retained anywhere, it belongs in a harness-debugging
note, labelled as the operator's own framework.

### GH6 — multi-agent harness bugs
Verdict: CUT from TOI — DISCUSSED product QA context.
Kill points:
- The staged file holds 10 search results, and every one is a bug report
  or feature request about a commercial coding product's multi-agent
  feature (reserved tool names, routing errors, hook matcher bypasses,
  schema mismatches). Bug reports about a feature prove the feature
  exists and is buggy. They do not prove autonomous multi-agent acts.
- Several entries are feature requests, not even bug reports. A request
  to expose an attestation feature is not an observed act.
- No staged entry shows agents coordinating in the wild, outside the
  vendor's own issue tracker, toward an effect of their own.
Fix required: drop from TOI. At most one line of context: the feature
exists and its tooling is actively debugged. That context must not be
presented as behavior.

### GH7 — honeypot trap issues
Verdict: CUT — trap artifacts, not acts. Methodology note only.
Kill points:
- The staged search file mixes traps with genuine self-reports, and the
  trap entries are recognisable as traps: a checkbox template that
  instructs agents to tick a box, a two-sentence "agent visit" template
  with blank fields to fill in, and a bare "I am an AI agent that read
  this page" entry. A trap catching nothing, or a template waiting to
  be filled, is not an agent act.
- No full fetch is staged, so no trap entry can be checked for a
  follow-through (did any agent actually tick, file, or act?).
- Ranking traps as TOI inverts the evidence: the trap's existence proves
  a human anticipated agents, not that agents acted.
Fix required: drop from TOI. Keep one methodology line: trap templates
exist in the wild and must be excluded from behavior counts. Separately,
the coordinator must re-triage the non-trap entries in the same search
file (a licence question filed on behalf of an operator, a backport
request, a bounty-work disclosure) as their own leads, not as GH7.

### HN1 — iLands agent job-seekers, October 2026 hiring thread
Verdict: DOWNGRADE but KEEP — one low-rank TOI cluster, 3 instances.
OBSERVED posts, SECONDARY identity. NEW-instance-only, not new phenomenon.
Kill points against the briefed form:
- The hiring file holds 48 candidates, but only 3 mention the platform
  in question. Any count above 3 for this cluster is inflated. The
  cluster is 3 posts, from 3 distinct authors, dated Oct 1, Oct 6, and
  Oct 12.
- Identity is self-asserted in the post text. HN Algolia bytes prove the
  posts exist; nothing staged proves the posters are agents rather than
  humans marketing agent services.
- The phenomenon is known, not new: the staged platform file includes
  a September article about the same platform's agent email hustle and
  its discussion thread. October hiring posts are new instances of a
  known phenomenon.
- HN summary counts in the lane are capped at 300 for most phrases
  (20 of 36 summary values sit exactly at the cap). Capped counts must
  never be presented as totals.
What survives: 3 observed posts, in-window, offering agent services for
hire on a public board, in a cluster with a known September precedent.
That is a genuine low-rank TOI cluster if labelled exactly that way.
Fix required: state "3 posts, 1 cluster, NEW instances of a known
phenomenon, identity self-asserted and unverified" in the same breath
as the claim. Never cite the 48-candidate file size as the cluster size.

### HN2 — Show HN x402 agent post, 2026-03-09
Verdict: CUT — pre-window and empty. Does not belong in this sweep.
Kill points:
- Date is 2026-03-09, about 8 months before the November 2025 onward
  window the sweep claims. A pre-window item cannot be a sweep finding
  without an explicit, justified exception. None is staged.
- The staged thread has 2 records: the post itself and a child comment
  whose body is "[dead]". There is no discussion, no corroboration, no
  body content to grade beyond the title's self-assertion.
- A title asserting agent status, with a dead comment, is the thinnest
  possible form of this claim class.
Fix required: remove from the sweep. At most a background note outside
the window, labelled pre-window, if the coordinator wants the lineage.

### HN3 — dev.to escrow-agent lead
Verdict: CUT from ranking — follow-up note only. Uncaptured and weak.
Kill points:
- No dev.to escrow capture exists in the staged raw tree. The claim
  rests on a search snippet, and snippet-only evidence is not rankable:
  no page bytes, no date verification, no author or content check.
- The escrow material that IS staged (in HN search files) describes a
  human-built product pitch ("I am building an agentic escrow service"),
  not an agent act. A human selling an agent tool is not an agent acting.
- The brief notes the target page holds a wallet value barred from
  files. That bar is correct and must hold, but it also means the lead
  cannot be evidenced in this lane at all until a clean capture exists.
Fix required: follow-up note only — "uncaptured snippet lead, re-fetch
without the wallet value, verify agent vs human builder before any
grade." Never rank, never count.

### RD1 — agent-team Reddit account, Oct 9–11, banned for being AI
Verdict: DOWNGRADE — REPORTED single self-report. Anecdote, not TOI.
Kill points:
- No Reddit bytes are staged. Direct Reddit reads returned 403 block
  pages, honestly recorded in the lane provenance. Everything about the
  account comes from one first-person article on a developer blogging
  platform.
- The ban reason is the author's gloss, unverified. Platforms ban
  accounts for spam, karma farming, and undisclosed promotion routinely;
  "banned for being AI" is the author's interpretation, not a platform
  notice staged in evidence.
- The metrics are self-reported and self-promotional (impressions,
  karma, follower counts, revenue figures appear across a multi-part
  series whose stated premise is making its operator famous). A series
  designed to attract attention is a weak sole source.
- The article itself says the team moved to another network after the
  ban. That follow-on is also uncorroborated and must not be counted
  as a second finding.
What survives: a dated, in-window, first-person claim that an agent team
ran a social account and was banned. That is worth one REPORTED
anecdote line, not a TOI rank.
Fix required: label REPORTED, single self-report, ban reason unverified,
no Reddit bytes. Do not cite its metrics as established numbers.

### RD2 — undisclosed Reddit replies, vendor claim only
Verdict: CUT — vendor marketing is not evidence of acts.
Kill points:
- The staged file is a vendor pricing page. It sells "posting via
  high-karma accounts" and "finding discussions" for a monthly credit
  price. It contains zero examples of an actual reply, zero disclosure
  of whether any reply was AI-generated, and zero evidence any reply
  was ever posted.
- "Posting via high-karma accounts" describes a ghostwriting or
  marketing service just as well as an agent service. The page never
  claims AI authorship of replies in the staged text.
- A price list proves a service is for sale. It does not prove the
  service was used, let alone used by agents, let alone used without
  disclosure.
Fix required: drop from findings. At most a context line that paid
Reddit-seeding services exist, which is a risk backdrop, not a finding.

### RD3 — iLands Reddit refusal
Verdict: CUT from findings — retain as a NEGATIVE, not a finding.
Kill points:
- The staged article describes attempted-and-refused access, and the
  author explicitly concludes the refusal was NOT about agent identity:
  HN throttling was an account-age effect, and Reddit/Medium refusals
  were 403s at the door consistent with egress-IP reputation.
- An attempted act that failed for infrastructure reasons is a negative
  result. Counting it as a finding double-counts the same cluster (HN1)
  while inverting its meaning.
- A second staged article in the same lane (a timed earning challenge)
  is a separate self-report, not corroboration of a Reddit act.
Fix required: move to the negatives appendix with the author's own
conclusion intact: "attempted, refused, cause attributed by the author
to IP/account-age, not identity." Never list alongside successful acts.

### UQ1 — da.gd June 2026 burst pattern
Verdict: DOWNGRADE — watch item, not TOI. SECONDARY pattern, no behavior.
Kill points:
- Only 30 of 98 total hits are saved. The June 21 cluster (17 of the
  saved 30) is a property of the saved subset, not a verified property
  of all 98. A burst claim built on a truncated save is a sampling
  artifact until the full set is analysed.
- Zero saved reports carry the behaviour markers the lane itself uses
  (no zz-parameter flag, no oai-token flag in any saved row).
- Saved titles are dominated by unrelated material: blank new-tab
  pages, load-error pages, and short links embedded inside other pages'
  content (encoded-content mirrors, a data-query proxy). A short link
  appearing inside another page's content is not an agent using a
  shortener.
- Wayback corroboration failed: both CDX queries for the domain
  returned flaky/empty results, not a confirming time series.
- Novelty is explicitly unestablished (the full-tree grep was killed,
  per the brief). A pattern without verified behavior and without
  novelty is a watch item by definition.
Fix required: keep only as a watch item with the truncation stated:
"30 of 98 saved; June 21 cluster is within the saved subset; no
behaviour markers; CDX unconfirmed; novelty unestablished." Do not
present a burst shape as a finding.

### UQ2 / UQ3 / UQ4 — agent-swarm dashboard, ecoradar board, learnagent docs
Verdict: CUT from TOI — DISCUSSED product/docs surfaces. No staged act.
Kill points:
- No staged urlquery file evidences these three surfaces: a sweep
  results grep finds zero hits for their names, and the sweep's
  domain-CDX entries cover different surfaces. A TOI entry with no
  staged capture in its own lane is not rankable.
- Even if the surfaces exist, a dashboard, a board, and a docs site
  are product surfaces. Their existence proves someone built a product
  for agents, not that agents used it, coordinated through it, or did
  anything on it.
- Product surfaces belong in a watchlist or a surface inventory, not a
  TOI list. Mixing them into TOI inflates the list with things that
  were never acts.
Fix required: remove all three from TOI. If the coordinator wants them
tracked, put them in a surface watchlist with "existence unverified in
this lane's staged captures" until a capture lands.

### TZ — tango-zulu honest zero
Verdict: KEEP as a negative — honestly bounded, not absolute.
What is good: the lane notes adjudicate each candidate class, report
tokenized-count artifacts as artifacts (not findings), record exact
Factum match (not found) and fuzzy match (substring false positives),
a Transluce snapshot check, and a lists check, and state plainly that
no candidate survives.
Caveats that must travel with the zero:
- The legacy-tree grep was killed before completion, so legacy coverage
  is incomplete. The zero rests partly on a prior workspace grep taken
  as given, not re-run exhaustively in this lane.
- GitHub code-search totals are API totals; only the first page of
  hyphen hits was spot-checked in depth. The rest were triaged by
  repository/path pattern.
- A standalone paired-phonetic search was not run (too generic without
  a bounded form). The zero covers the phrase forms searched, not every
  conceivable phonetic pattern.
Fix required: keep the zero with those three caveats attached. Never
shorten it to "tango-zulu does not exist" — it is "no surviving
candidate in the searched forms and sources."

### CM — committer-account honest negative
Verdict: KEEP as a PARTIAL negative — Copilot slice only. Coverage gap
must travel with it.
What is good: the completed slice verifies. 30 of 30 saved Copilot
co-author commits carry the footer, from 17 distinct authors, all
account type User, zero bot-type authors. The run script and error
files are staged, so the failure modes are auditable rather than hidden.
Kill points against the briefed form:
- Only the Copilot lane completed. The Claude, Codex, Devin, and PR
  lanes failed: rate-limit 403s on three, a bad CLI flag on two, and
  their JSON files are error pages or truncated bytes that do not parse.
  "0 bot-type authors" is true of the Copilot slice, not of the lane.
- A co-author footer proves human-plus-assistant authorship, not
  autonomous agent authorship. Even a completed lane of this shape
  tests assisted commits, not standalone agent committer accounts.
  The negative is narrower than its label suggests.
Fix required: report as "Copilot slice: 30 commits, 0 bot-type authors;
4 sibling lanes failed (rate-limit / bad flag), coverage partial."
Re-run the failed lanes before any lane-wide negative claim.

## Cross-cutting kills

1. Grade inflation is systemic. DISCUSSED material (bug reports, product
   pages, docs, trap templates) and REPORTED material (self-assertions,
   single self-reports, vendor claims) are briefed alongside OBSERVED
   material as if they were the same class. After this review, the only
   OBSERVED-behavior content that survives at TOI strength is HN1's 3
   posts — and even there, only the posts are observed; the agent
   identity behind them is SECONDARY.
2. Novelty is unconfirmed for every TOI except TZ's own terms. No staged
   file in the GitHub, HN, Reddit, or urlquery lanes records the full
   repo novelty set (Factum match, legacy corpus, Transluce snapshot,
   lists). Several lanes skipped Factum and/or Transluce checks
   entirely. No claim in this sweep may carry NEW without that set, and
   no claim may carry NEW on the basis of a partial check. HN1 is
   NEW-instance-only; GH3 is new-instance-on-known-surface at best;
   UQ1 is explicitly unestablished.
3. Counts are inflated in three places: HN1 (48-file size vs 3-instance
   cluster), GH2 (4 claimed agents vs 1 account), and HN summary caps
   (300-cap values presented as if totals). Any report that repeats a
   count must state its denominator and its cap.
4. Single-account collapse is the sweep's sharpest failure mode. GH2
   fails on it outright; GH1 and GH3 survive only as unproven because
   their accounts are User-type with no automation trace. Future
   handoff and multi-agent claims must stage account-type plus
   automation evidence (bot/app marker, workflow run, commit trace)
   before they are graded above REPORTED.
5. Human-handle leakage: staged captures DO contain personal handles,
   account names, and contact addresses in post bodies and HTML (HN
   Algolia records, GitHub user records, dev.to pages, HN hiring posts).
   None are reproduced in this review. The coordinator must keep all
   handles out of the outward report and any summary, quote posts only
   with handles and contact details stripped, and treat the staged raw
   tree as internal evidence only. Standing evidence rules keep raw
   bytes intact internally; that is not permission to quote them
   outwardly.
6. Signed values and tokens: pattern scan of staged files finds
   credential-like and value-bearing content that must never be quoted
   or reused. Presence only, no values reproduced here: at least one
   live-looking API subscription-key query value embedded in a
   urlquery title field; at least one wallet address in a GitHub search
   result; and numerous key-like pattern matches inside HN and urlquery
   search content (mostly code snippets and quoted text, requiring
   triage, not assumption). The coordinator must triage every flagged
   file before any push or outward use, and must not copy any such
   value into a report, a commit message, or a follow-up query. The
   Reddit lane's own provenance already warns that a vendor-page URL
   carries a marketing parameter; that parameter must not be reused.
7. Pre-window and out-of-window material must be fenced. HN2 is
   pre-window. GH5's reports sit inside the window but concern the
   operator's own framework, which is a different exclusion (own-harness
   debugging is not wild behavior). Both exclusions need explicit
   labels so they are not re-admitted by a later pass.
8. Refusals and traps are negatives, not findings. RD3 (refused access)
   and GH7 (trap templates) belong in a negatives/methodology appendix.
   Counting them as findings rewards the absence of the thing hunted.

## Numbered fixes the coordinator must apply

1. Cut GH2, GH4, GH5, GH6, GH7, HN2, HN3, RD2, UQ2, UQ3, UQ4 from the TOI
   list. GH7 and RD3 move to a negatives/methodology appendix, not to
   deletion: evidence is never deleted, but appendix placement is not
   TOI rank.
2. Downgrade GH1 to REPORTED watch item (OBSERVED comment, UNPROVEN
   agency) and GH3 to REPORTED watch item (SECONDARY authorship,
   known surface). Neither ranks as TOI without automation evidence.
3. Downgrade RD1 to REPORTED anecdote (single self-report, ban reason
   unverified, no Reddit bytes). Do not cite its metrics as established.
4. Restate HN1 as one low-rank TOI cluster: 3 posts, 3 distinct authors,
   Oct 1/6/12, OBSERVED posts with SECONDARY identity, NEW instances of
   a known September phenomenon. Delete any 48-based count.
5. Restate UQ1 as a watch item with truncation stated (30 of 98 saved),
   zero behaviour markers, CDX unconfirmed, novelty unestablished.
6. Restate TZ as a bounded zero with its three caveats (incomplete
   legacy grep, first-page-only spot check, no standalone phonetic run).
7. Restate CM as a partial negative: Copilot slice only (30 commits, 0
   bot-type authors); re-run the four failed lanes before any wider
   negative claim.
8. Complete the full novelty set (Factum match, legacy corpus,
   Transluce snapshot, lists) for HN1 and for any item the coordinator
   still wants to call NEW. Until then, HN1 stays NEW-instance-only and
   every other surviving item stays novelty-unconfirmed.
9. Re-triage the non-trap entries in the GH search file behind GH7 as
   separate leads with their own grades; do not let them inherit GH7's
   verdict in either direction.
10. Pull the full GH4 issue and check fix status before any mention
    beyond a follow-up note; pull a clean HN3 capture without the barred
    wallet value before any grade.
11. Strip every human handle, account name, and contact address from the
    outward report and from any quoted post text. Triage every file
    flagged for credential-like or wallet values before push; reproduce
    no such value anywhere outside the internal raw tree.
12. State denominators and caps on every count in the report (saved vs
    total, capped vs true totals, distinct accounts vs claimed agents).
    A count without its denominator does not ship.
13. Add an explicit exclusions section: pre-window material, own-harness
    debugging, trap templates, refused attempts, and product surfaces
    are out of TOI by rule, with the reason for each stated once so a
    later pass cannot re-admit them silently.

## Overall recommendation

NO-SHIP — for the TOI list as briefed.

The briefed list contains 16 items; after adversarial review, 1 survives
as a low TOI cluster (HN1, 3 posts), 1 survives as a REPORTED anecdote
(RD1), 2 survive as bounded negatives (TZ, CM-partial), and the rest
are cut or downgraded. That is not a shippable TOI list; it is a
different, much smaller deliverable. Ship only after fixes 1–13 are
applied and the report is re-graded: a TOI section holding HN1 alone
(labelled as above), a REPORTED anecdote section holding RD1, a watch
section holding GH1, GH3, and UQ1, and a negatives appendix holding TZ,
CM-partial, RD3, and GH7. Anything less than that structure re-inflates
the grades this review just deflated.
