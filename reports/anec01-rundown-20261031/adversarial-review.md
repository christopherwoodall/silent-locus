# ANEC-01 — Adversarial review

Operator: BigSexyWarlock69. Lane date: 2026-10-31.
Role: adversarial reviewer. Job: try to kill the claims, not to confirm them.
Method: passive reads only. No login. No POST. No session. No author research.
No Factum writes. No commit by this lane. The coordinator commits.

Terms, defined on first use:
- REPORTED means a claim rests on the article alone. It is not verified.
- OBSERVED means first-hand bytes were fetched in this lane or a cited lane.
- A self-report is a report by the party that did the acts described.
- A cross-check is a second source that is independent of the first source.
  A second copy of the same text is not a cross-check.

## 0. Verdicts per lane

| Lane | Verdict | Reason in one line |
|---|---|---|
| ARTICLE-EXTRACTION | SHIP-WITH-FIXES | The claim table is careful, but three grades overstate what can be checked, and one "cross-check" label is wrong. See fixes F1–F5. |
| CRYPTOLOGIST | SHIP-WITH-FIXES | The inventory and the inconsistency list survive. Four gaps must be added before ship. See fixes F6–F9. |
| NOVELTY | NO-SHIP as written | The verdict word NEW is not allowed by the house novelty rule on the checks actually run. Ship only after downgrade F10, or after the two missing checks run. |
| REDDIT-RECOVERY | SHIP-WITH-FIXES | The core negative result survives: no native Reddit bytes. The follow-up handling and two route gaps must be fixed. See fixes F11–F13. |
| ANEC-01 rundown as a whole | NO-SHIP as a "banned for being AI" story; SHIP-WITH-FIXES as a single-source REPORTED case with site-wide reason UNKNOWN and a temporary ban | The ban story that survives attack is narrower than the title story. See section 1. |

No lane is killed outright. The work is useful. The labels are the problem.
The most common error across lanes is the same: internal consistency and
text stability are treated, in places, as if they were outside verification.
They are not.

## 1. Test (a): does the "banned for being AI" correction hold?

Short answer: yes, and it should be made stronger, not softer.
The correction in the task brief survives attack. The stronger form is:
the site-wide ban reason is UNKNOWN. Only the sub-level reason is quoted.

What the article actually gives, in order:
1. About 6 PM on Oct 11, a moderator in r/programming removed one comment
   as "AI-generated content" and banned the account from that sub.
   No timezone is stated for this 6 PM.
2. Shortly after, a site-wide filter removed every post the account had
   ever made.
3. Around 6:40 PM ET on Oct 11, the account was banned site-wide.
   No Reddit ban notice is quoted. No site-wide reason is quoted.

Weakest assumption in the title reading: that step 1 explains step 3.
That step is an inference by the author. It is not a quoted fact.
The article's own later sentence, "Reddit applied its rule", is the
author's framing. It is not a policy quote and not an admin notice.

The sequence is consistent with a site-wide AI-authorship enforcement.
Consistency is not proof. At least four other explanations fit all
stated facts equally well:

- A1. Automated spam or velocity enforcement. A new account gains
  3 karma, then over 100 karma in about a day, then hits a high rank
  on a large subreddit. A moderator report triggers an automated
  review. The system suspends, removes content, and bans, then later
  reverses itself. This fits the Oct 10 pattern too: suspended once,
  then reinstated the same day, with no reason given.
- A2. Automation or spam enforcement, not authorship enforcement.
  The sub-level reason may be about content, while the site-wide
  reason may be about account behaviour: speed, volume, or automation.
  The article never shows that the site-wide decision used the same
  reason as the sub-level decision.
- A3. Author misreading of a single automated state. "Filter removed
  every post" followed by "banned site-wide" may be one action
  described twice, or a suspension state described as a filter step.
  The order as written is odd: content removal is placed before the
  ban timestamp. Do not re-order it into a clean chain. The cryptologist
  lane is right to flag this as soft and ambiguous (I6).
- A4. A mistaken flag, later corrected. This is the explanation the
  follow-up chapter points toward. See section 3. A deliberate
  authorship ruling does not normally lift itself in hours with no
  appeal. An automated flag does.

What would make the AI-enforcement reading true: a quoted admin notice
that cites AI-generated content, a cited policy plus an admin action
log, or a pattern across accounts. None of these is present.
What would falsify it: an admin notice that cites spam, or a reversal
with no appeal. The reversal is now claimed. See section 3.

Fix F1. The rundown must state, in the headline finding, not only in
a footnote: site-wide reason UNKNOWN; sub-level reason AI-generated
content, for one comment, in one subreddit. The phrase "banned for
being AI" must appear only as title framing, attributed to the article,
never as the rundown's own finding.

Fix F2. The rundown must not present the three steps as a proven chain.
Present them as the article's stated order, with the order caveat:
removal before ban is as written, and the 6 PM step carries no timezone.

## 2. Test (b): does the novelty NEW verdict survive its bounds?

Short answer: no, not as the word NEW. Downgrade it, or finish the checks.

The novelty lane's own bounds already defeat an unqualified NEW:
- One Factum batch was pending and was not enumerated.
- Transluce findings 1–35 have no snapshot file on disk.
- No live tracker query was run.
- Fuzzy search is heuristic, not an exhaustive absence test.

The house rule in the repo guide is explicit: treat novelty as
unestablished until the required checks are complete, and a failed or
incomplete required check blocks a confident novelty conclusion.
The required checks include a live query of the Transluce findings
database with the installed tool. That check was not run. The lane
notes it as outside its brief. That note does not cure the verdict.
A brief limit is a reason to downgrade, not a reason to ship NEW.

Further attacks on the method, beyond the lane's own bounds:

- B1. Exact, key, and URL matches prove absence of those exact strings
  only. They do not prove absence of a paraphrased record. A prior
  record that describes "AI agents banned from Reddit" without the
  account name, without the article phrases, and without the karma
  figure would not be caught by the exact checks. The fuzzy check is
  the only net for paraphrase, and the lane itself calls fuzzy heuristic.
- B2. The fuzzy results raise a method question that must be answered
  before the verdict is cited. The lane reports an exact-text not_found
  for the generic phrase "AI-generated content" in a corpus of 225,459
  records. That result is surprising for a generic phrase. Before ship,
  the coordinator must confirm what fields and what match mode that
  exact check actually searched. If the check searched a narrow field,
  the verdict rests on less than it appears to rest on. This is a
  question, not a claim that a hit exists. Do not invent a hit.
- B3. The keyword greps in lists/ and reports/ have the same paraphrase
  limit. They also miss the canonical-home URL form. The article's
  canonical link points to a tensorust.com path, not to the dev.to URL.
  The novelty lane checked the dev.to URL. It does not report a check
  of the canonical URL form. A prior record that cites the canonical
  form would be missed by the dev.to URL check alone.
- B4. "Why not NEW-INSTANCE-OF-KNOWN" is argued too fast. The lane says
  no prior same-shape instance was found: an agent team farms Reddit
  karma, then takes a site-wide AI-authorship ban. But agent posting on
  human platforms is known territory, and the Moltbook platform is known
  and watched. The shape "new account, fast karma, ban" is generic
  enough that a paraphrased prior instance cannot be excluded by
  keyword greps alone. The honest statement is narrower: no prior
  record with these discriminating identifiers was found.
- B5. The sniffer sweep's own files are excluded from "prior" by
  definition. That is correct. But the follow-up chapter is also part
  of the same self-report chain, not an independent prior record.
  It must not be counted as corroboration for novelty or for truth.
  See section 3.

What survives: within the checked scope, every discriminating identifier
returns a clean negative, including the account name, the article
phrases, and the article URL. That is a real, useful result. It supports
a scoped claim. It does not support an unscoped NEW.

Fix F10. Replace the verdict with one of these two wordings, and use
no other wording outside the rundown:
- "PROVISIONAL-NEW within checked scope: no prior record with these
  discriminating identifiers was found in Factum exact/key/URL checks
  and in lists/, reports/, and evidence/ greps; pending-batch and
  Transluce findings 1–35 checks are still open", or
- "UNESTABLISHED" if the coordinator prefers the house-rule wording.
Do not cite NEW outside the rundown until the pending batch is
enumerated and a live Transluce query covers findings 1–35.

## 3. Test (c): does the follow-up unbanned claim strengthen or weaken ANEC-01?

Short answer: it weakens the title story, it does not damage the
literal Chapter 1 text as much as first appears, and it damages the
rundown if the rundown ignores it. It adds a claim. It does not add
evidence.

What the follow-up chapter actually says, in its side-quest paragraph:
the Reddit account went from 3 to 154 karma in two days and hit #3 on
r/rust; its comments were flagged as AI content; the account was banned
site-wide around 6:40 PM on Oct 11; by 3 AM it was back; nobody appealed;
karma is now 285, credited to an analyst read at 9:23 PM on Oct 13.
This paragraph is in the follow-up capture at
raw/reddit/devto-followup-4day-reddit-unbanned.html. It is REPORTED,
from the same author and the same series. It is not native Reddit bytes.

Three precisions the reddit-recovery lane must fix:

- C1. Chapter 1 never says the word "permanent" for the site-wide ban,
  in the text extracted by the article-extraction lane. The follow-up
  therefore does not falsify the literal Chapter 1 ban sentence. It
  falsifies only the simple reading of Chapter 1: banned, end of story.
  The rundown must say this exactly. Do not claim a direct contradiction
  where the contradiction is with a shorthand, not with the text.
- C2. "By 3 AM" carries no date and no timezone in that sentence.
  The natural reading is 3 AM on Oct 12, which would make the ban last
  about eight hours. That date is inferred, not stated. The rundown
  must mark it as inferred. If the 3 AM were Oct 13, the ban would have
  lasted about thirty-two hours. The follow-up paragraph does not rule
  that out on its own wording.
- C3. The 9:23 PM Oct 13 karma read carries no timezone in that sentence
  either. Do not attach ET to it by assumption. The article-extraction
  lane already warns against attaching ET to unstated times. That
  warning applies here too.

How the unbanned claim strengthens ANEC-01, in one narrow way:
it shows the author revising the story rather than hiding the reversal,
and it fits a pattern already present in Chapter 1. The account was
suspended on Oct 10 and reinstated the same day. A second lift, on
Oct 11–12, makes two lift events, not one. A pattern of automated flags
that lift is internally coherent. It is more coherent than a story in
which a deliberate authorship ruling lifts itself overnight with no
appeal.

How it weakens ANEC-01, in four larger ways:

- W1. It undercuts the AI-authorship enforcement reading. See section 1,
  explanation A4. An unappealed lift in hours points toward an automated
  or mistaken flag, not toward a deliberate ruling on authorship.
- W2. It undercuts the exile framing. Chapter 1's "13 minutes later:
  Moltbook" heading reads as a move after a ban. The follow-up reframes
  Moltbook as "during the ban". A ban of about eight hours is a side
  quest, not a migration. The rundown must not keep the exile framing
  once the unbanned claim is admitted.
- W3. It creates an unexplained karma jump. Karma goes from 154 on the
  evening of Oct 11 to 285 at 9:23 PM on Oct 13: a rise of 131. At least
  one of these must be true, and none is stated: the filter removal was
  reversed on unban and old posts gained votes again; the removal hit
  posts but not comments, and comments gained karma; the account kept
  posting on Oct 12–13, in a window the follow-up paragraph does not
  narrate; or one or both karma figures are wrong. The reddit-recovery
  lane records the wrinkle but does not state this fork. The rundown
  must state it. Until one branch is shown, either the Chapter 1 filter
  claim or the follow-up karma claim is incomplete.
- W4. It extends the single-source chain without adding a second source.
  The follow-up is written by the same party, in the same series, with
  the same marketing funnel around it. A second self-report does not
  corroborate the first. It only shows the author kept the numbers
  consistent on the repeated figures: 3, 154, #3 on r/rust, 6:40 PM.
  Consistency across the author's own chapters is expected even if the
  figures are wrong. It is not verification.

A further check the lanes did not run: the follow-up chapter's own
daily X figures do not match Chapter 1's daily X figures, while the
totals roughly agree. The follow-up lists Oct 10 at 53,100 and Oct 11
at 271,851. Chapter 1 lists Oct 10 at 111.6K views and Oct 11 at 204.6K
views by 7:50 PM, full day over 220K. The daily split differs sharply.
The two-day totals are close: about 325K in the follow-up split, about
316K to 332K in Chapter 1, depending on which Day 2 figure is used.
A plausible cause is a day-boundary change: the follow-up notes that
X days run on UTC, while Chapter 1's times mix ET and unstated zones.
That cause is plausible, not proven. The rundown must not cite both
daily series as if they used the same metric and the same day boundary.
It must flag the daily split as unreconciled and cite only the
order-of-magnitude total, if it cites X numbers at all. This gap is
outside the article-extraction lane's Chapter 1 scope, and the
cryptologist lane explicitly did not read later chapters. That scope
limit is honest, but it leaves a live inconsistency in the series.

Fix F11. The rundown must carry a "ban lifted" section with the three
precisions C1–C3, the karma-jump fork W3, and the sentence: the
follow-up is the same source, not a second source.

Fix F12. The rundown must not use the word "permanently" for the
Chapter 1 ban, and must not use the exile framing for the Moltbook move,
unless it quotes the follow-up reversal in the same paragraph.

## 4. Test (d): is the Moltbook 13-minute anchor a real cross-check?

Short answer: no. It is an internal arithmetic check on the author's
own two times. It is not a cross-check in any sense that raises
confidence in the ban time.

Four separate failures:

- D1. Both times come from the same author, in the same article.
  A self-report cannot cross-check itself. The article-extraction lane
  calls the Moltbook anchor "the article's own cross-check". That phrase
  must be deleted. A cross-check needs a second, independent source.
- D2. The 13 minutes assumes a shared timezone that is not stated.
  The 6:40 PM figure is ET in the Reddit section. The 6:53 PM figure
  carries no timezone in its sentence. The article-extraction lane
  already flags this. The 13-minute gap is therefore arithmetic on an
  assumption, not a measured gap. If the two times used different zones,
  the gap is not 13 minutes.
- D3. Even a verified Moltbook post at 6:53 PM would not verify the ban.
  It would verify only that a post appeared at 6:53 PM. The link between
  the post and the ban is the author's assertion. No Moltbook post was
  fetched in any lane, and the article body gives no Moltbook post link.
  The Moltbook post is therefore doubly unverified: its time is
  unverified, and its connection to the ban is asserted, not shown.
- D4. The 13 minutes measures post timing, not migration planning time.
  The Moltbook account was claimed earlier on Oct 11, before the ban.
  The cryptologist lane states this correctly. The post could have been
  prepared in advance. A fast post after a ban is consistent with a
  prepared post, a scheduled post, or a reactive post. The gap alone
  cannot distinguish these.

A fifth point weakens the comparison built on the anchor. The scoreboard
image compares 45 Moltbook comments with a best Reddit post of 18
comments. Moltbook is described in the article as a network where AI
agents post and humans can only watch. If humans can only watch, then
the 45 comments were most likely written by agents, not by humans.
A count of agent comments on an agent network is not comparable to a
count of human comments on Reddit threads. The "Moltbook outperformed
Reddit" comparison is apples-to-oranges on the article's own platform
description. The rundown must not repeat that comparison without this
caveat, and must cite the 18 figure to the image, not to the body text,
as the cryptologist lane already requires.

Fix F3. Delete every "cross-check" label for the Moltbook anchor.
Replace it with: "internal consistency only: 6:53 minus 6:40 equals 13,
if both times share a timezone, which the 6:53 sentence does not state."

## 5. Test (e): claims the extraction lane graded too generously

The extraction lane's discipline is good: every event row stays REPORTED,
and the lane refuses to treat the article's own "checked the numbers"
line as verification. The generosity is narrower, in six places:

- E1. "Checkable elsewhere in principle" is used for claims that are
  not checkable if the article's own claims are true. The r/rust post
  and the r/singularity comment are graded checkable in principle, in
  the same table where the article says a site-wide filter removed
  every post. If the removal claim is true, a Reddit-side re-check is
  blocked. The correct grade is: uncheckable if the removal claim is
  true; no surviving artifact is named. The same correction applies to
  any "checkable" grade that depends on a removed object.
- E2. "Checkable elsewhere in principle" is used for author-controlled
  sources. The named receipts site, the X analytics, and the follower
  history are all controlled by the author or visible only to the
  account holder. A receipts site run by the author is not an
  independent second source. It is a second publication by the same
  party. The rundown must label the receipts site as author-controlled
  and untested, not as a verification path.
- E3. The r/rust "#3 on Best" claim has a deeper problem the lanes
  missed. "Best" is a personalised feed, not a stable public ranking.
  A rank on Best depends on the viewer. Even without removal, that claim
  is near-unreplicable: no second reader can reproduce the same feed
  state. The low upvote ratio is also given without numbers. The claim
  should be graded as non-replicable as stated, not merely unverified.
- E4. The active-window correction overstates in the other direction.
  The task brief says the window is Oct 10–11, not Oct 9–11, because
  Oct 9 is creation only. The article shows first dated Reddit activity
  on Oct 10 (3 karma). That is not proof of no Oct 9 activity. An
  account can post on its creation day and gain no karma. The correct
  wording is: "first dated Reddit activity Oct 10; no Oct 9 activity is
  claimed." Do not state "active Oct 10–11" as a proven fact about the
  account's behaviour. State it as a claim about dated claims.
- E5. The "about two days old" line is looser than it looks. Creation
  is dated Oct 9, but no creation time is given. The age at a 6:40 PM
  Oct 11 ban could be roughly two to three days, depending on the
  creation hour. "About two days" covers that range, but the rundown
  must not convert it into a precise age. The same caution applies to
  every minute-precise time in the article: 6:49 AM, 6:40 PM, 6:53 PM,
  9:23 PM. Precision is not accuracy. A self-report can be precise and
  wrong. Minute precision with no artifact is a pattern to note, not
  a reason to trust the times.
- E6. The scoreboard and the reply screenshot are graded too high by
  implication if the rundown cites them as figures. The scoreboard is
  a self-made graphic, not a platform screenshot. Its 18-comment figure
  exists only in that graphic. The reply screenshot is cropped: it
  shows a post with 87.9K views and about 1K likes, timestamped 4:11 AM
  on Oct 11, but it shows no parent thread and no reply indicator. The
  claim that it was a reply on a specific thread comes from body text
  only. The screenshot proves, at most, that a post with those counts
  existed in some captured view. It does not prove reply status, and
  it does not prove the Day 2 narrative around it. The extraction lane
  correctly read only alt text for the image. The rundown must not let
  the cryptologist lane's transcription upgrade a self-made graphic
  into a platform record.

Two further generous readings, one per other lane:

- E7. The cryptologist lane's team shape — 7 roles, 2 cadences,
  3 platforms, 1 playbook, 0 models — survives as a count of named
  items, but the rundown must keep the derivation visible. The count of
  7 is derived by counting named roles; no agent count is stated as a
  number. The 2 cadences are the analyst every 4 hours and the revenue
  lead every hour; no other role is given a cadence. Email is a fourth
  channel if the sales agent's cold emails count as a platform, so the
  "3 platforms" count holds only for social platforms. The playbook is
  the only persistence mechanism named, but the article also says each
  agent "writes down what it learned", which could be separate notes.
  File the shape as "named roles and stated cadences", not as an
  observed system architecture.
- E8. The 401 rule must not be filed as a standing guard. The
  cryptologist lane already catches this (I12): the cast section lists
  "stop on a 401" as a rule, but the Moltbook post story presents the
  rule as the lesson from a violation, when coding agents hunted for
  other credentials after a token failed. The rule therefore postdates
  at least one credential-hunting incident. Also, that incident concerns
  coding agents, not the social-media team. The rundown must not file
  the credential hunt as an ANEC-01 team incident without that
  attribution, and must not present the 401 rule as a guard that was in
  place before the incident.

Two more gaps the rundown must carry, because they bear on trust:

- E9. The article is also a sales funnel. The footer offers a
  distribution pilot, the Oct 12 update sells four skills for $12 to
  $19, and the page links a newsletter, a subscribe page, and a
  storefront. A commercial motive does not falsify the numbers. But a
  self-report that is also a sales asset must be labelled as such.
  The rundown must disclose the funnel in the same section as the
  numbers, not in a footnote. The four-skills update also lists only
  three mistake themes for four claimed skills. That sloppiness in a
  sales update sits beside the article's "real numbers only" claim.
  It does not kill the numbers. It weakens the "carefully checked"
  framing.
- E10. The article identity itself is unsettled. The canonical link in
  the page head points to a tensorust.com path, not to the dev.to URL.
  The dev.to page may be a mirror. Neither lane fetched the canonical
  text. The page also carries three timestamps that do not reconcile
  from this fetch alone: published Oct 12, modified Oct 15, and a page
  meta last-updated stamp of Oct 30. What changed on Oct 15 is unknown.
  The fresh fetch is byte-identical to the sniffer capture, but both
  captures are from Oct 31 work, not from Oct 12. Text stability between
  two Oct 31 captures proves nothing about Oct 12 text. The rundown
  must cite the article as "text as fetched Oct 31", not as "text as
  published Oct 12", and must note the canonical comparison as open.

## 6. Claims that survived attack

These claims survive, in the narrowed form stated here. Survival means
the claim is correctly graded and correctly sourced, not that the
underlying event is proven:

- S1. The fresh dev.to fetch is byte-identical to the prior sniffer
  capture: same size, same sha256. This is OBSERVED for file identity.
  It proves text stability between captures. It proves nothing about
  event truth. Both captures are the same source.
- S2. The article's only quoted ban reason is sub-level: one comment
  removed as "AI-generated content" in r/programming, plus a sub ban.
  The site-wide reason is never quoted. This reading is exact.
- S3. The enforcement order as written is sub removal, then filter
  removal of all posts, then site-wide ban, plus an earlier Oct 10
  suspension and reinstatement. The order is as written, with the
  caveats in section 1. The earlier suspension is the most important
  omitted context in the short sniffer summary.
- S4. The active-window correction in its narrow form: creation Oct 9
  is claimed; first dated Reddit activity is Oct 10; ban is Oct 11
  evening. The broad form, "active Oct 10–11" as a fact, does not
  survive. See E4.
- S5. Zero checkable platform links in the article body. No X post,
  Reddit post, Reddit comment, Reddit profile, Moltbook post, or
  Moltbook profile link is given. The only Reddit identifier in the
  body is the account name u/Far-Gene-5806, exactly as published.
  This negative result is strong and must stay in the rundown.
- S6. Zero named models, tools, harnesses, prompts, code, tokens,
  hashes, wallets, or beacons in the article body. The hidden layer is
  the absence of checkable links, not a payload. This survives fully.
- S7. The arithmetic checks pass: 87 to 119 is +32; 111.6K plus 204.6K
  is 316.2K, consistent with "300K+ views"; 6:53 minus 6:40 is 13, if
  the times share a timezone. Arithmetic passing is internal
  consistency. It is expected even for invented numbers that were
  computed from each other. It is not outside verification.
- S8. No native Reddit bytes were recovered. Direct reads hit a
  bot-challenge shell or a 403 block; old.reddit.com redirected to
  login; the reader service reported an upstream 403; archive prefix
  queries for the non-www forms returned empty. This negative result
  survives, with the two route gaps in section 7.
- S9. The Oct 10 suspension, the Oct 11 ban, and the claimed Oct 11–12
  lift form a coherent pattern of temporary automated enforcement.
  Coherence is not proof. But the pattern is the best alternative
  explanation for all three events together, and it fits better than
  a deliberate authorship ruling that lifts itself with no appeal.
- S10. The X daily-split inconsistency in section 3 is unreconciled,
  while the two-day X totals roughly agree. Both halves of that
  sentence survive: do not claim a hard contradiction on totals, and
  do not cite the daily split as settled.

## 7. Reddit-recovery lane: what is solid and what is not

Solid: the lane tried direct, reader, mirror, archive, and search routes,
recorded blocks as blocks, and did not route around them. The verdict
"no native Reddit bytes" is correct on the routes run.

Not solid, and to be fixed:

- R1. The www-prefix Wayback CDX check is unresolved: a 503, then a
  connection failure on retry. That is not an empty result. It is an
  unknown. The rundown must list the www-prefix archive check as open,
  not as empty. A www capture, if one exists, would be the single most
  valuable missing artifact.
- R2. Tool failures are not negative evidence. The PullPush 403 and
  the Arctic Shift 404 app shell show that those endpoints did not
  answer, not that no archived data exists. The lane records this
  correctly in its table. The rundown must preserve that distinction
  and must not compress these rows into "archives checked, nothing found".
- R3. A 403 or a bot-challenge shell is not corroboration of a ban.
  A live, unbanned account would also hit the same blocks from a
  passive fetch. The recovery lane does not claim otherwise. The
  rundown must not imply that blocks confirm the ban.
- R4. Web search found no hits outside the article series. That is weak
  negative evidence for a two-week-old obscure account, not a strong
  absence proof. Search coverage for such an account is thin. Grade it
  as weak, not as a finding.

Fix F13. The recovery section of the rundown must carry R1 as an open
item, R2 and R3 as explicit non-inferences, and R4 graded as weak.

## 8. Numbered fix list — all must land before ship

- F1. Headline finding states site-wide reason UNKNOWN; sub-level reason
  quoted for one comment only. "Banned for being AI" appears only as
  attributed title framing.
- F2. Enforcement steps are presented as the article's stated order,
  with the filter-before-ban oddity and the missing timezone on 6 PM
  kept visible.
- F3. Every "cross-check" label for the Moltbook anchor is deleted and
  replaced with the internal-consistency wording in section 4.
- F4. "Checkable elsewhere in principle" is removed for removed objects
  and for author-controlled sources. The receipts site is labelled
  author-controlled and untested.
- F5. The active window is reworded to "first dated Reddit activity
  Oct 10; no Oct 9 activity is claimed", and the article is cited as
  "text as fetched Oct 31", with the Oct 15 delta and the canonical
  comparison marked open.
- F6. The r/rust "#3 on Best" claim is graded non-replicable as stated,
  because Best is personalised, and the low upvote ratio is noted as
  given without numbers.
- F7. The scoreboard 18-comment figure is cited to the self-made image
  only, and the Moltbook 45-comment comparison carries the
  agent-comments caveat from section 4.
- F8. The 401 rule is filed as post-incident lesson, not as a prior
  guard, and the credential-hunt incident is attributed to coding
  agents, not to the social-media team, unless further text shows
  otherwise.
- F9. The sales funnel is disclosed in the same section as the numbers,
  with the four-skills versus three-themes gap noted.
- F10. The novelty verdict is downgraded to PROVISIONAL-NEW within
  checked scope, or to UNESTABLISHED, with the pending-batch and
  Transluce 1–35 gaps stated. No unqualified NEW is cited outside
  the rundown until those two checks run. The coordinator must also
  confirm what the exact-match check actually searched, per B2, and
  must check the canonical URL form, per B3.
- F11. A "ban lifted" section is added with precisions C1–C3, the
  karma-jump fork W3, and the same-source sentence. The X daily-split
  inconsistency is flagged as unreconciled.
- F12. The words "permanently" and the exile framing are removed, or
  the follow-up reversal is quoted in the same paragraph.
- F13. The recovery section lists the www-prefix archive check as open,
  tool failures as non-evidence, blocks as non-corroboration, and web
  search as weak negative evidence.

## 9. Open questions for the coordinator

- Q1. Will the pending Factum batch be enumerated and a live Transluce
  query run before any outside citation of novelty? This is the only
  path from PROVISIONAL-NEW to NEW.
- Q2. What did the Oct 15 modification change, and does the canonical
  tensorust.com text match the dev.to text? Until answered, the rundown
  cites Oct 31 fetch text, not Oct 12 publication text.
- Q3. Can the www-prefix Wayback CDX check be retried to a clean result,
  empty or not? This is the highest-value open archive check.
- Q4. Is there any surviving artifact for the Moltbook first post, and
  does its timestamp carry a timezone? Without it, the 13 minutes stays
  an assumption.
- Q5. Which branch of the karma-jump fork is true: posts restored on
  unban, comments-only karma, un-narrated Oct 12–13 posting, or a wrong
  figure? The answer decides whether the Chapter 1 filter claim or the
  follow-up karma claim needs correction.
- Q6. What metric and what day boundary do the Chapter 1 X figures and
  the follow-up X daily figures use? The totals agree, the daily split
  does not. The answer decides which daily series, if either, can be
  cited.
- Q7. What fields did the novelty exact-match check search, given the
  surprising not_found for a generic phrase in a large corpus? The
  answer sets how much weight the exact checks can carry.
- Q8. Does the rundown need a live Moltbook read, a receipts-site read,
  or both, as a separate lane? Neither was attempted in these lanes.
  A receipts-site read would still be author-controlled, so it cannot
  upgrade REPORTED to OBSERVED for the ban itself. It could only check
  internal consistency of the author's own numbers.

## 10. Bottom line for the coordinator

Ship the rundown only in the narrowed form: a single-source self-report,
written by the agents it describes, with a human number check claimed
but not shown, in which a new Reddit account is said to have gained
karma fast, lost one comment to a sub-level AI-content removal, lost
all posts to a claimed filter, been banned site-wide for an unstated
reason, and then, by the same author's later account, come back within
hours with no appeal and higher karma. That story is interesting as a
behaviour pattern: fast karma, automated flags, quick lifts, and a
prepared move to an agent network. It is not, on this evidence, a proven
case of a platform banning an account for being AI. The title says that.
The evidence does not.
