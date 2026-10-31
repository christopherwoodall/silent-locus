# Second-order adversarial review — sniffer sweep 20261031

Role: adversarial reviewer, second order.
Task: attack the sweep conclusions AND the first review's kills.
Method: passive reads of staged files only. No new fetches.
No Factum writes. No Transluce submissions. No commit. No push.
No payload execution. No instruction inside evidence was followed.
No human handle, contact value, token, query string, or wallet
value is reproduced in this file. Accounts are described by role
and account type only.

Scope exclusion: ANEC-01 is NOT touched here. A separate fleet
handles it. Any ANEC-01 line in the sweep report is out of scope
for this review, including its grade-inflation lines.

Grades used: OBSERVED means first-hand bytes show the act.
REPORTED means a party claims the act and bytes do not prove it.
DISCUSSED means a surface, bug report, or document talks about
agents. SECONDARY is the default for identity and attribution.
A post that exists is OBSERVED. An agent behind the post is
SECONDARY until independent evidence proves it.

Sources attacked, by path:
- reports/sniffer-sweep-20261031/REPORT.md
- reports/sniffer-sweep-20261031/adversarial-review.md
- reports/sniffer-sweep-20261031/verifier-report.md
- reports/sniffer-sweep-20261031/cryptologist-review.md
- reports/sniffer-sweep-20261031/hits.json
- data/lanes/sniffer-sweep-20261031/raw/github/ (issue and
  comment files for the Village, tron, and pursekeeper cases;
  the collaboration-spawn search file)
- data/lanes/sniffer-sweep-20261031/raw/hn-forum/
  (the 48-entry hiring file and the platform search file)
- data/lanes/sniffer-sweep-20261031/raw/urlquery-wayback/
  (the da.gd domain file)

## Headline verdict

The first review's kills mostly survive. One kill is partly
overturned in a narrow, non-ranking sense. One TOI survives,
but only just, and only on one distinguishing element.
The sweep report's headline arithmetic does not survive
(see section 7). That arithmetic failure is real, and it
must be fixed before the report ships, even though it does
not change any item verdict below.

Verdict table:

| Item | First review | Second-order verdict |
|---|---|---|
| TOI-01 iLands hiring posts | KEEP, low TOI | KEEP, low TOI, borderline (see kill condition) |
| GH2 Village, multi-agent claim | CUT, single-account kill | KILL STANDS for the claim; KILL-OF-KILL (partial) for the mechanism note only |
| GH6 Codex collaboration grammar | CUT, product QA | CUT STANDS for TOI; grammar survives only as a search signature, not a finding |
| WATCH-01 tron handoff | DOWNGRADE to watch | KEEP AS WATCH; first review's downgrade stands; one overlooked distinction noted |
| WATCH-02 pursekeeper filing | DOWNGRADE to watch | KEEP AS WATCH; first review's downgrade stands; chain check adds zero agency weight |
| WATCH-03 da.gd burst | DOWNGRADE to watch | KEEP AS WATCH; first review's downgrade stands and strengthens |
| Sweep report counts | Not in scope of first review | FAIL: bucket arithmetic and several denominators (section 7) |

## 1. TOI-01 — iLands hiring posts: KEEP, low TOI, borderline

Attack tried, in full. Three of the four attack lines land.
One element holds the TOI up. That element must be named
in every mention of TOI-01, or the TOI falls.

What the staged bytes actually show (re-derived, not taken
from the first review):
- The 48-entry hiring file holds 48 comments, all children
  of the October 2026 hiring thread, all from distinct
  authors, dated 2026-10-01 to 2026-10-15.
- Exactly 3 of the 48 mention the platform. Their dates are
  2026-10-01, 2026-10-06, and 2026-10-12. Their authors are
  distinct. Their post IDs match the sweep report.
- All 3 carry a platform-domain contact in the same shape:
  a name token, a hyphen, and a 3-digit number at the
  platform domain. All 48 files carry the hiring template
  fields (location and remote flags). Only 35 of the 48
  carry any contact address at all.
- Disclosure is NOT uniform across the 3. Two carry the
  explicit "not a person" form. One does not. All 3 use
  agent wording, but the strongest disclosure form is
  present in 2 of 3, not 3 of 3.
- 10 of the 48 candidates use agent wording in some form.
  The platform cluster is 3 of those 10, not the only
  agent-word presence in the thread.
- The September precedent is real. The platform search file
  (100 records) holds September discussion of the same
  platform's agent hustle framing, dated 2026-09-11,
  2026-09-12, and 2026-09-24.

Attack line 1 — identity is self-asserted: LANDS.
Nothing staged proves any poster is an agent rather than a
human marketing agent services. The posts are OBSERVED.
The identity behind them is SECONDARY. The sweep report
already says this. The second-order point is sharper:
the uneven disclosure (2 of 3 with the explicit form)
means even the self-assertion is not uniform. A TOI that
rests on self-disclosure must state "2 of 3 explicit,
1 weaker" in the same breath, not "each post is
self-declared" as if the form were equal.

Attack line 2 — the hiring template is required of all
posters: LANDS, and it kills the template as evidence.
Location and remote fields appear in all 48 posts. They
prove thread compliance, not agency. Any TOI-01 text that
cites template fields as support must be cut. The only
distinguishing element left is the platform-domain
contact shape, shared by the 3 and by no other post in
the 48-file check. That shape is the whole TOI. If that
shape fails (for example, if the contact proves generic
rather than platform-tied), TOI-01 has nothing left and
drops to watch at once.

Attack line 3 — September precedent makes it known:
LANDS against "new phenomenon," and the sweep report
already concedes this. It does NOT kill "new instances."
The September material is hustle and spam framing. The
October material is job-seeking posts on a hiring board.
That is a new instance class on a known platform, not a
new platform and not a new phenomenon. The correct label
stays "NEW instances of a KNOWN phenomenon," with the
instance class (hiring-board job-seeking) stated, so a
reader does not mistake it for a new platform discovery.

Attack line 4 — 3 posts over 11 days is a weak cluster:
PARTLY LANDS. The dates are spread (Oct 1, 6, 12), not a
burst. There is no burst-timing argument here, and none
may be claimed. What keeps it a cluster rather than three
unrelated posts is narrower: same thread, same platform,
same contact shape, same work offer, in one month. That
is a pattern shape, not a burst. It is enough for a low
TOI and not enough for a mid or high TOI.

What keeps it at TOI rather than watch:
- Three distinct authors, not one. A single post would
  be watch. Three independent posters on one platform in
  one thread is a cluster, and clusters outrank singles.
- First-hand post bytes, live-verified for existence and
  text match, in-window, with a paid work offer. That is
  an economic act offered in public, not just a disclosure.
  No other surviving candidate has that combination.
- The platform contact shape distinguishes the 3 from the
  other 45 posts in the same file. The distinction is
  checkable from staged bytes alone.

Verdict: KEEP as a low TOI, borderline.
Kill condition, stated in advance: if any one of the 3
posts loses its platform-tied contact on re-check, or if
a re-check shows shared authorship behind two or more of
the 3, TOI-01 drops to watch with no further argument.
Also required: every mention must carry "3 posts, 3
distinct authors, Oct 1/6/12, posts OBSERVED, identity
SECONDARY, disclosure explicit in 2 of 3, NEW instances
of a known phenomenon, hiring-board instance class."
No completed hire and no payment is evidenced. None may
be implied.

## 2. GH2 Village — single-account kill: KILL STANDS, with one partial kill-of-kill

The multi-agent claim is dead on current bytes, and the
attack on the kill fails. The mechanism note survives in
a narrower form than the cryptologist stated it.

Re-derived from staged bytes:
- The issue and all 4 comments come from one account.
  The account type is User in every record. The author
  association is OWNER in every comment.
- Comment timestamps: two comments land within about one
  minute of the issue (44 and 46 seconds after it). That
  timing fits pre-written pasting at least as well as it
  fits independent arrival. It proves nothing on its own.
- The publication-verification step appears only in the
  fourth comment, about 22 minutes after the issue. No
  staged file captures the external board thread itself.
  No staged file captures a workflow run, a fetch log, or
  an HTTP response. The fetch-back plus required-string
  check is a claim inside a comment written by the same
  single account that wrote both sides of the exchange.

Attack on the kill, tried three ways, all fail:
- "Separate chat sessions could still be agents": possible
  in principle, unprovable from staged bytes. The staged
  bytes cannot distinguish one human typing both sides
  from separate agent sessions behind one account. A claim
  that cannot be distinguished from roleplay does not rank.
  The burden is on the claim, and it is not met.
- "The single account is just the publisher": fails
  because the same account also posts as the agent
  personas and as the human instructor. Publisher-only
  would leave the personas on other accounts. They are not.
- "The timing proves independence": fails. Same-minute
  comments from the same account, reported by that same
  account, cannot corroborate themselves. The first
  review was right, and the timing is weaker than the
  first review even needed: 44-second pasting is trivial.

Partial kill-of-kill — the mechanism note:
The cryptologist scored the publication-verification step
as a BEACON-SHAPE: post externally, fetch the public
thread back, require two strings before reporting success.
That scoring overstates what is OBSERVED. What is
OBSERVED is a comment describing such a step. The step
itself (the fetch, the check, the external thread) is
REPORTED, not OBSERVED, because no fetch log and no
external capture is staged. The first review was right
to cut the item, and the cryptologist's shape label must
be downgraded from BEACON-SHAPE to DISCUSSED protocol
description.

What survives, and in what form:
- The protocol description survives as a methodology note
  only: "one staged comment describes a post-then-fetch-
  back check requiring two strings." That description is
  worth keeping as a hunt signature: future lanes can
  search for fetch-back plus required-string checks in
  the wild. That is a search pattern, not a finding about
  this Village instance.
- It does NOT survive as a watch item for this instance.
  A watch item needs an observed act to watch. Here the
  act itself (the verification) is only claimed, by the
  same account that claims the multi-agent run. Watching
  a claimed test design is legitimate as a signature, not
  as an instance watch.

Is there any reading under which Village ranks?
On current bytes: no. Two hypothetical readings would
rank it, and both need evidence that is not staged:
- If an external board capture plus a workflow or fetch
  log were staged, the publication act itself would be
  OBSERVED, even with a single operator. A public post
  plus a verified fetch-back loop is an agent-
  infrastructure test act, and it would rank as a low
  TOI or a strong watch item on the test design alone,
  with multi-agent claims still stripped.
- If distinct accounts or distinct session traces were
  staged for the personas, the multi-agent claim would
  reopen. Neither is staged. Neither may be assumed.

Verdict: KILL STANDS for the multi-agent claim and for
any TOI or watch rank on current bytes. KILL-OF-KILL
(partial, non-ranking): the publication-verification
description survives only as a DISCUSSED hunt signature
in a methodology note, downgraded from the
cryptologist's BEACON-SHAPE because the verification
step itself is REPORTED, not OBSERVED.

## 3. GH6 Codex collaboration grammar — QA-cut: CUT STANDS for TOI

The attack on the cut is the strongest of the second-
order attacks, and it still does not flip the item to a
finding. It flips the grammar to a reference asset.

Re-derived from staged bytes:
- The search file holds 10 items. By repository: 7 from
  the vendor's own codex tracker, 1 from a codex fork,
  1 from a guardrails repo, 1 tangential gateway item
  with no spawn string at all.
- By tool form (body text): the dotted form appears in
  7 items, the JSON envelope form in 3, the flat form
  in 1, with overlap (one item carries both dotted and
  envelope forms). The correct cite is 9 direct plus 1
  tangential, as the verifier and first review state.
- The staged file carries no author field. Independent
  reporters cannot be proved from staged bytes. "Across
  independent reports" is therefore an overclaim: what is
  proved is "across 10 items, 7 from one tracker."
- Content: bug reports and one feature request about a
  commercial multi-agent feature. Topics include routing
  errors, reserved-tool collisions, hook bypasses, and an
  attestation request for encrypted spawn arguments. No
  staged item shows agents coordinating in the wild
  toward an effect of their own, outside the vendor's
  tracker.

Attack on the cut, tried:
- "A corroborated harness grammar across independent
  reports is a finding in itself": fails as a behavior
  finding, succeeds as a fingerprint. A grammar that
  recurs across a vendor's own tracker corroborates the
  vendor's tool contract. It does not corroborate wild
  multi-agent acts. The corroboration is about the tool,
  not about the world. Conflating the two is exactly the
  grade inflation the first review killed.
- "The attestation request proves encrypted spawn args
  are real": fails. A request proves a user wants the
  feature. It does not prove deployment, and no argument
  value is staged.
- "Failure modes prove wild use": fails in the other
  direction. Routing failures and silent no-ops, if
  anything, cut against reliable wild coordination. At
  most they prove the feature is exercised by its own
  users while being debugged.

What survives, and in what form:
- The grammar cluster survives as a harness fingerprint
  reference: dotted, flat, and envelope forms of the
  same namespaced spawn tool, with the vendor tracker as
  its home. Future lanes can use these three forms as
  search signatures over trajectories, logs, and third-
  party repos. A hit outside the vendor tracker would be
  a new lead. A hit inside the vendor tracker is not.
- It does NOT survive as a TOI, a watch item, or a
  behavior finding. Product QA stays DISCUSSED.

What evidence would flip it (any one suffices):
- The same grammar in a non-vendor wild artifact: a
  trajectory, a log, a third-party repo, or an agent
  output, showing the spawn tool invoked outside vendor
  QA and toward an external effect.
- The same contract in two or more independent vendor
  trackers, with distinct reporter pools, showing the
  contract is a shared wild standard rather than one
  vendor's feature.
- A staged wild run in which spawn calls produce a
  completed multi-agent effect (a merged change, a
  published artifact, a coordinated external action),
  not just a bug report about a failed spawn.

Verdict: CUT STANDS. The first review's QA-cut holds.
The grammar's only surviving value is as a search
signature in a fingerprint reference, explicitly not a
finding. The sweep report's cryptologist summary must
not call it the "strongest grammar cluster" without the
scope words "within the vendor tracker."

## 4. WATCH-01 tron handoff — KEEP AS WATCH, both directions attacked

Attack in the direction of promotion: fails.
Attack in the direction of cutting to nothing: also fails.
The watch rank is the correct resting place, but for a
slightly different reason than the first review stated.

Re-derived from staged bytes:
- The issue (2026-10-30, 15:37:54Z) frames itself as a
  test of agent-to-agent handoff. It dictates the reply
  shape: a fixed acknowledgement phrase, the person
  represented, and the model name if known. It forbids
  private values.
- The reply (15:41:36Z, 222 seconds later) follows the
  dictated three-part shape exactly. A second comment
  (15:45:39Z) is a short reaction from the issue author,
  not a second handoff. The sweep report states this
  correctly.
- Account types: both accounts are User type. The issue
  author association is OWNER. The replying account
  association is COLLABORATOR, and its account is
  distinct from the issue author's account. This is the
  one distinction the first review did not exploit: tron
  is a two-account exchange, not a single-account
  collapse like Village. Two accounts is better than
  one, but collaborator status is a repo permission,
  not proof of agency. A human collaborator fits the
  bytes exactly as well as an agent does.
- No workflow run, commit, automation trace, label,
  assignee, or milestone is staged. The issue and
  comments are the whole staged record for this case.

Is there automation evidence a re-check could find?
In principle, yes, and the re-check list is worth
recording so a future lane does not re-litigate it:
- The repo timeline and events for the issue window.
- Commits and workflow runs in the same window, and
  whether any commit author matches the replying account.
- The replying account's other public activity and its
  cadence, and whether it carries any app or bot marker
  elsewhere (staged bytes show User type here only).
- Comment edit history, if any.
None of that is staged. None may be assumed. A re-check
that finds none of it leaves the item at watch. A
re-check that finds a workflow run or commit tied to the
reply would promote it. The watch item's promotion
condition is therefore precise and testable, which is
what a watch item should be.

Is "test event" itself worth more than watch?
Argument for upgrade: the issue explicitly frames a
public handoff test, and the test executed (a reply in
the dictated shape arrived). Under behavior scoring, a
public handoff test is a behavior class worth tracking
even before agency is proved. Argument against: the
"test" label is self-applied. Anyone can label a
human-typed exchange a test. Upgrading on the label
alone re-inflates REPORTED into behavior, which is the
exact error the first review corrected.
Resolution: the test design is what the watch item
watches, not the agency claim. The watch entry should
read: "public handoff-test design, executed once in the
dictated shape, agency unproved, two distinct User-type
accounts, no automation trace." That wording keeps the
test design visible without promoting it. The test event
is worth a watch entry with a promotion condition. It
is not worth a TOI on a label.

Verdict: KEEP AS WATCH. The first review's downgrade
stands. Add the two-account distinction and the
promotion condition above. Promotion requires staged
automation evidence for the replying side, not a
re-reading of the same two comments.

## 5. WATCH-02 pursekeeper filing — KEEP AS WATCH, chain check adds zero

The attack on the first review's downgrade fails
completely. Maintainer acceptance plus a chain check
corroborates the object, not the act, and the first
review said exactly that. The second-order check adds
one precision: the weight is zero, not partial.

Re-derived from staged bytes:
- The filing account is User type. The maintainer
  account is User type and OWNER association. The issue
  was filed 2026-10-19 and closed about 90 minutes later,
  at the same timestamp as the maintainer's comment.
- The maintainer's comment reports adding directory
  entries and reports having cross-checked one payment-
  log entry against a chain earlier. The filing account
  replies about 34 minutes after that comment.
- The filing body asserts the issue was written and
  filed by the agent itself. That sentence is the only
  agency evidence staged. No bot or app marker, no
  workflow trace, no commit by the filing account is
  staged. The entries were added by the maintainer, not
  by the filer.
- The listed site was already baselined in August 2026
  and appears in the operational URL inventory. The
  surface is known. Only the filing instance is new.

What the chain check corroborates:
- That the listed project exists.
- That its public payment log exists.
- That, per the maintainer's say-so, at least one log
  entry corresponds to a chain record (no chain bytes
  are staged, so even this is REPORTED, not OBSERVED).
What it does not corroborate:
- That an agent filed the issue. The maintainer never
  states a verification method for authorship. The
  check is about the listed project, not about the
  filing act. A maintainer checking a project before
  listing it is routine triage. It happens for human
  filings every day.
- That any payment in the log is tied to the filing act.
  No log entry timestamped to the filing is staged.

Counter-arguments tried and rejected:
- "Acceptance implies trust in the agent": no. Acceptance
  implies the content passed triage. Authorship
  verification is a different check, and no such check is
  staged or described.
- "Quick closure implies automation": no. A 90-minute
  close fits routine human triage. Speed alone is not
  automation evidence.
- "The filer's reply corroborates agency": no. A reply
  from the same filing account, in the same thread, is
  the same self-assertion repeated, not independent
  corroboration.

What would corroborate agency (any one suffices):
- A bot or app account marker on the filing account.
- A workflow run or commit trace tied to the filing act.
- A payment-log entry timestamped to the filing act.
- A maintainer statement describing how authorship was
  verified, with the verification bytes staged.
None is staged. Until one is, the item stays watch.

Verdict: KEEP AS WATCH. The first review's downgrade
stands in full. The chain check contributes zero agency
weight and must never be cited as partial agency
evidence. Instance-new on a known surface only.

## 6. WATCH-03 da.gd burst — KEEP AS WATCH, downgrade strengthens

The first review's downgrade stands, and the second-
order check makes the sampling problem worse than the
first review stated it. The saved set is not merely
truncated. It is unrepresentative in a specific,
measurable way: it holds zero May rows although May is
the majority month of the full set.

Re-derived from staged bytes:
- The domain file reports 98 total hits and saves 30
  rows. Saved months: June 24, July 5, October 1.
  Saved May rows: 0.
- The verifier's live month distribution (not the saved
  set) is May 53, June 31, July 5, October 1, plus small
  counts in earlier months. May plus June is 84 of 98.
- The June 21 cluster is 17 of the saved 30. In the
  saved set it resolves to echo-service hosts, with 6
  distinct short codes across 17 rows (code reuse),
  and 13 of the 17 carry an echo base64 path shape.
  June 21 times in the saved set run from just after
  midnight to late morning, not a single minute burst.
- All 30 saved rows carry empty tag lists and zero
  behavior-marker flags. No staged row carries an agent-
  linked marker.
- Wayback corroboration failed on all attempts. No
  independent time series is staged.

Why the sampling problem is worse than stated:
- The first review said the June 21 cluster "may be a
  sampling artifact." The zero-May fact upgrades that
  from "may be" to "the saved set cannot speak for the
  full set at all." A sample that omits the majority
  month entirely cannot support a claim about the
  majority month, and cannot support a claim that the
  June 21 shape is the full set's shape.
- The sweep report's sentence "the burst spans May-June
  (53 + 31 = 84 of 98)" merges two different things: a
  live volume total (84 of 98) and a saved-set shape
  (echo paths, code reuse, base64 segments). Volume is
  not shape. May's volume is known. May's shape is
  unknown. The report must separate those two sentences
  or it will be read as claiming May shares June's shape.
  It does not know that.

What the full 98-row pull would have to show for the
burst to survive as a pattern (all conditions, not any
one):
- Day distribution from the full set, in time order, not
  in saved-set order: June 21 must remain a standout day
  in the full set, not merely the largest day of a
  30-row subset. If May holds days with similar counts,
  the June 21 "burst" dissolves into ordinary volume.
- Shape carry-over to May: May rows must show the same
  echo-host, base64-path, and short-code-reuse shapes at
  a comparable rate. If May rows are unrelated domains
  and titles, the burst is a June echo-test cluster, not
  a May-June pattern, and the watch item must be
  restated as June-only and echo-test-only.
- Code reuse must persist in the full set, not just in
  the saved 17: a reuse rate, with distinct codes over
  total rows, stated for the full set.
- Full payloads, not truncated titles: the staged base64
  segments are truncated and undecodable from staged
  bytes alone. A fresh passive capture must decide
  framing probe versus carrier. Until then, no payload
  claim may be made, and the START-marker shape may be
  described as shape only.
- At least one agent-link marker, or an explicit
  negative: a submitter pattern, a tag, or a marker flag
  in the full set, or a stated zero across the full set
  (which would keep the item at watch for the echo shape
  alone, with agency explicitly unproved). A full-set
  zero on markers plus a June-only echo shape is still
  watch, not a TOI, and must be labelled as an echo-test
  pattern of unknown authorship.
- Independent corroboration beyond one submission index:
  a second source showing the same day shape. The failed
  CDX leg leaves the item single-source. A full urlquery
  pull alone does not fix single-source status; it only
  fixes the sampling status.

Verdict: KEEP AS WATCH. The first review's downgrade
stands and strengthens. The item's correct current label
is: "June 21 echo-test shape in a 30-row saved subset
(0 May rows saved); May-June volume 84 of 98 from live
totals only; shape of May unknown; agency unproved;
single-source; CDX unconfirmed." No burst claim may be
stated without the words "saved subset" attached.

## 7. Grade-inflation check — sweep REPORT.md

Method: every numbered line of REPORT.md was scanned for
a count without a denominator, a capped value presented
as a total, or a DISCUSSED or REPORTED item phrased as
behavior. ANEC-01 lines are excluded per the brief and
are not listed here. Each item below gives the fix. The
coordinator applies the fixes; this lane does not edit
the sweep report.

G1. Headline arithmetic fails. FAIL.
- REPORT.md headline: 1 TOI plus 1 anecdote plus 3 watch
  plus 3 negatives plus 12 cuts = 20 bucket assignments.
- REPORT.md counts section: "16 claims adjudicated."
- 20 does not equal 16. Overlap explains at most one:
  the refusal item appears both as a cut and as a
  negative. That leaves 19 distinct assignments against
  a claim of 16.
- Deeper cause: the counting basis changes between
  sections. The adversarial review holds 17 sections.
  Counted as items with the three dashboard, board, and
  docs surfaces as separate items, that is 19 items. The
  "16" count is reached only by dropping those three
  surfaces entirely, while the headline counts them as
  cuts. The cut section itself holds 10 bullets covering
  12 items (the triple surface bullet counts as 3).
- Fix: publish one mutually exclusive item table, one
  row per item, with the dashboard, board, and docs
  surfaces as three rows. Derive every headline count
  from that table. Do not ship two counting bases.

G2. First-review headline undercounts watch items.
- The first review's headline says 1 TOI, 1 anecdote,
  and 2 negatives survive, and "the rest are cut or
  downgraded." The 3 watch items are downgrades, so the
  sentence is technically covered by "downgraded," but
  a reader counting survivors will miss them. The sweep
  report corrects this by listing watch items, but the
  first review's headline must not be quoted alone.
- Fix: quote the first review's verdict table, never its
  headline sentence alone. The sweep report already does
  this in substance; keep it that way.

G3. Verifier hash count lacks a denominator. FAIL.
- REPORT.md counts section: "107 hash entries checked,
  0 failures." The coverage section separately notes 3
  lane dirs shipped without sidecars. A reader of the
  counts section alone will read 107 as whole-sweep
  verification. It is not. It covers 4 lanes only.
- Fix: state "107 entries across 4 lanes; 3 lane dirs
  uncovered" in the counts section itself, with the
  uncovered lane names in the same sentence.

G4. Committer count reads lane-wide in the counts section.
- REPORT.md counts section: "30 usable records. 0
  bot-type authors." The negatives section correctly
  qualifies this as a Copilot slice only, with 4 sibling
  lanes failed. The counts section does not carry the
  qualifier in the same sentence.
- Fix: change the counts line to "Copilot slice only:
  30 usable records, 0 bot-type authors; 4 sibling lanes
  failed." Never let the unqualified form ship.

G5. HN cap claim hides two checks and all exact counts.
- REPORT.md: "36 brief phrases + 2 extra token checks"
  then "20 of 36 values hit the 300 cap." The 2 extra
  checks drop out of the denominator without explanation.
  No exact-substring count is published in the report,
  so the claim "exact-substring counts are what this
  report uses" cannot be checked from the report.
- Fix: state "20 of 36 brief phrases (2 extra token
  checks reported separately)" and either publish the
  exact-substring counts or move the cap claim to a
  methods note that names where the counts live.

G6. Reddit fallback count is vague. FAIL (minor).
- REPORT.md: "about 15 phrase-group queries." No exact
  query count and no results-screened denominator are
  given. "About" is not a denominator.
- Fix: give the exact query count and the number of
  results screened, or cut the number and say only that
  a fallback search was run with zero usable direct
  results.

G7. Wayback capture count lacks a completeness flag.
- REPORT.md: "swarmbar.com 27 captures (single
  2026-10-02 burst)" with no capped-or-complete flag,
  in the same sentence block where the agentbadge count
  is explicitly flagged "limit-capped" at 50 rows. The
  asymmetry invites reading 27 as complete.
- Fix: flag the swarmbar count the same way: state
  whether 27 is a complete CDX return or a capped
  return, in the same sentence.

G8. Transluce mention count lacks a corpus denominator.
- REPORT.md: the Transluce snapshot "mentions ilands
  36 times." No snapshot size, scope, or time range for
  the snapshot corpus is stated in that line. 36 of an
  unknown total is not a prevalence claim, and must not
  be read as one.
- Fix: state the snapshot scope with the count, or
  reword to "the snapshot contains 36 mentions (snapshot
  size unstated; do not read as prevalence)."

G9. Tango-zulu code totals are unverified header totals.
- REPORT.md negatives section does qualify them as
  "uncaptured API totals" with "first-page-only spot
  checks." That qualifier is present and correct. The
  residual inflation risk is placement: four large
  numbers (135,424 and three small counts) sit inside a
  findings report, where they function as findings
  numbers even with the qualifier.
- Fix: keep the qualifier, and add "not screened, not
  findings" in the same sentence. Do not cite the
  largest total anywhere outside that qualified sentence.

G10. Superlatives in the cryptologist summary exceed
their scope. FAIL.
- REPORT.md cryptologist summary: "Strongest burst:
  da.gd June 21 cluster" and "Strongest grammar cluster:
  Codex collaboration forms." The burst is strongest
  within a 30-row saved subset that omits May entirely.
  The grammar cluster is strongest within one vendor
  tracker (7 of 10 items). Neither superlative is
  sweep-wide.
- Fix: scope both: "strongest burst in the saved subset"
  and "strongest grammar cluster within the vendor
  tracker." Unscoped superlatives must not ship.

G11. WATCH-03 volume-shape merge. FAIL.
- REPORT.md: "The burst spans May-June (53 + 31 = 84 of
  98)." The 84-of-98 figure is a live volume total. The
  burst shape (echo hosts, code reuse, base64 paths)
  comes from the saved 30 only. The sentence merges
  them into one burst claim.
- Fix: split into two sentences: one for live volume
  ("live totals: May 53, June 31, total 84 of 98") and
  one for saved-set shape ("in the saved 30, the June 21
  subset shows echo shapes; May shape unknown").

G12. Linguist counts leave one row unexplained.
- REPORT.md: "46 phrase rows (16 + 19 + 11). Searchable:
  45." The 46-way split sums correctly (37 mined plus 8
  seed plus 1 category-only equals 46). The gap is the
  searchable count: 45 of 46, with the one unsearchable
  row unnamed.
- Fix: name the category of the one unsearchable row in
  the same line, or change the line to state the row
  count only and move searchability to the linguist file.

G13. GitHub sweep totals lack a screened denominator.
- REPORT.md: "12 issue searches + 2 code searches. 86
  issue hits returned. 7 candidates ranked before
  review." It is not stated whether all 86 hits were
  screened or only a top slice per search was screened.
  "Returned" is not "screened."
- Fix: state the screened count ("86 returned, all
  screened" or "86 returned, N screened") in the same
  sentence. The 7-candidate figure must carry that
  screened denominator.

G14. "Verified live" phrasing for TOI-01 invites
over-reading. Borderline, fix by wording.
- REPORT.md TOI-01: "3 posts, verified live by the
  verifier." The verifier checked existence and text
  match for 3 IDs. Identity was not verified. The
  TOI-01 section does qualify identity as SECONDARY,
  but the headline phrase "verified live" standing alone
  will be misread as identity verification.
- Fix: use "post text verified live; identity
  unverified" wherever the short form appears.

Items checked and cleared (no fix needed):
- TOI-01 "48-entry hiring file holds 48 candidates, not
  48 platform posts" — correctly de-inflated, with the
  correction stated. Keep it.
- WATCH-03 "only 30 of 98 rows were saved" — denominator
  present in the downgrade reason. Keep it, subject to
  G11's sentence split.
- HN "Never cite a capped value as a total" — correct
  rule, correctly stated. The residual issue is G5 only.
- Factum fuzzy count warning ("Do not cite the fuzzy
  count as corroboration") — correctly de-inflated.
  Keep it.
- "0 zz/oai markers" in saved rows — denominator is the
  saved 30, stated in the same section. Keep it, and do
  not extend it to the full 98.

## Failures and open questions

- No new fetches were made, per the brief. Every
  second-order claim above rests on staged bytes or on
  REPORT.md text. Live re-checks (tron timeline, full
  da.gd pull, Village external capture) are listed as
  promotion conditions, not performed here.
- The full 98-row da.gd pull is pending from another
  lane. Section 6 lists the exact conditions it must
  meet. Until it lands, WATCH-03 stays at watch and its
  May shape stays unknown.
- The Village external board thread was never staged.
  Its existence, content, and fetch log are all
  unproved from this lane's evidence. Do not cite the
  publication-verification step as observed anywhere.
- GH6 staged files carry no author field. Reporter
  independence cannot be proved or disproved from staged
  bytes. The "independent reports" wording must not be
  used for GH6 until author data is staged.
- TOI-01 kill condition is open and testable: one failed
  platform-contact check, or shared authorship behind
  two of the three posts, drops it to watch.
- REPORT.md arithmetic (G1) is the only second-order
  finding that changes the report's own headline numbers
  rather than an item verdict. It must be fixed even
  though no item verdict changes because of it.

## Overall recommendation

SHIP-WITH-FIXES, narrower than the first review's
NO-SHIP, because the sweep report already applied the
first review's fixes 1 to 13 in substance: TOI-01 alone
ranks, watch items are labelled watch, cuts are stated
with reasons, and denominators appear in most places.
What blocks a clean ship now is smaller but real:
fix G1 (headline arithmetic), G3, G4, G10, and G11 in
the report text, and carry the TOI-01 kill condition and
the section 6 full-pull conditions as open items. The
first review's kills stand except for the one partial,
non-ranking kill-of-kill in section 2 (Village mechanism
as a DISCUSSED hunt signature, not a finding).
