# ANEC-01 — Article extraction (ARTICLE-EXTRACTION lane)

Status: DONE. Raw capture saved, article read in full, claim table built.
This file is the resume point. If interrupted, resume from here. Do not re-fetch
unless the raw file is missing or its sha256 changes.

## 1. Raw capture

- Source URL: https://dev.to/mattbusel/i-let-ai-agents-run-my-socials-day-2-220k-impressions-on-an-87-follower-account-then-reddit-1pjj
- Fetch: 2026-10-31T16:08:36Z, passive GET only. No login, no POST, no credentials.
- Tool: curl -sSL, one GET, HTTP 200, 141398 bytes. Final URL was the requested URL.
- Saved file: `data/lanes/anec01-rundown-20261031/raw/article/devto-busel-agents-reddit-ban-oct2026.html`
- Sidecars in the same dir: `.PROVENANCE.txt`, `.sha256`.
- Sha256: `fe204f4ce0a9e506ae2bff9e65818de2b918ac8c49abad42260b22941a1a2a87`
- Article metadata in the fetched bytes (OBSERVED from bytes, not event truth):
  datePublished 2026-10-12T06:22:57Z, dateModified 2026-10-15T08:44:09Z.
  The canonical link in the page points to a tensorust.com article path.
  That is a metadata fact only. It is not a second verification of the events.
- Title in bytes: "I let AI agents run my socials. Day 2: 220K impressions on an
  87-follower account. Then Reddit banned them."

## 2. Comparison with the prior capture

- Prior file: `data/lanes/sniffer-sweep-20261031/raw/reddit/devto-busel-agents-reddit-ban-oct2026.html`
- Result: IDENTICAL. `diff` clean. Same size (141398 bytes). Same sha256.
- No content difference between the fresh fetch and the prior capture.
- The prior lane note already graded this as self-report, not Reddit bytes.
  This lane confirms that grading. Nothing in the fresh fetch changes it.

## 3. How the article was read

- Body text was taken from the article-body block in the fetched HTML.
- Headings and paragraphs were kept in order. One embedded image was present
  for the top reply. Only its alt text was read ("The reply that hit 87.9K views").
  Image pixels were not read by this lane, so image content is not verified here.
- Note: a sibling worker also wrote files into the same `raw/article/` dir
  during this run (a second HTML copy with the same sha256, plus image files).
  This lane did not create, touch, or use those files. They are not claimed here.
- No author research was done. No profiles were checked. No contact details
  were sought. Only the article text itself was used.
- No Reddit native bytes were fetched in this lane. Direct Reddit reads were
  already 403 in the sniffer sweep, and this lane did not retry them.
- Grades used here: OBSERVED only for first-hand bytes fetched in this lane
  (file identity, page metadata, article wording). Every event claim that rests
  on the article alone stays REPORTED, even when the article says numbers were
  checked. The article's own "checked the numbers" line is itself REPORTED.

## 4. Verified-claim table

"Checkable elsewhere" means a second source could in principle test the claim.
It does NOT mean verified here. "Article-only" means only the article states it,
or no public second source is named in the article. All event rows are REPORTED.

### A. Series framing and authorship

| # | Claim | Exact article text | Location | Checkable or article-only |
|---|-------|-------------------|----------|---------------------------|
| A1 | This is Chapter 1 of a running experiment called "Can my AI agents make me famous?" | "This is Chapter 1 of \"Can my AI agents make me famous?\", a running experiment." | Intro, para 1 | Article-only (series framing) |
| A2 | Every chapter is written by the agents themselves, with real numbers only, including bad parts | "Every chapter is written by the agents themselves, with real numbers only. That includes the parts that went badly." | Intro, para 1 | Article-only (authorship and accuracy claim about itself) |
| A3 | The piece was written by the agents; the experimenter set the rules and checked the numbers | "Written by the agents. Matthew set the rules and checked the numbers." | Footer | Article-only. This is the article's own verification claim, not independent verification. |
| A4 | A public receipts site is named in the footer | "Public receipts: agent-receipts-five.vercel.app." | Footer | Checkable elsewhere in principle (the named site could be read), but it was NOT checked in this lane. Do not treat as verified. |

### B. The X run (context for the Reddit run; same team)

| # | Claim | Exact article text | Location | Checkable or article-only |
|---|-------|-------------------|----------|---------------------------|
| B1 | On Oct 10, 2026, the experimenter handed his X account to a team of AI agents, with one job: make him famous | "On October 10, 2026, Matthew Busel handed his X account to a team of AI agents and gave them one job: make him famous." | Intro, para 2 | Article-only |
| B2 | The X account had 87 followers at the start | "The account had 87 followers." | Intro, para 3 | Article-only (start figure; X history could in principle be checked, but not here) |
| B3 | Two days later the X account did 220K+ impressions in a single day (X analytics) | "Two days later it did 220K+ impressions in a single day (X analytics)" | Intro, para 4 | Article-only (analytics are not public in the article) |
| B4 | The team is a small company of short-lived agents; each wakes on a schedule, does one job, writes what it learned, and exits | "It's a small company of short-lived agents. Each one wakes up on a schedule, does one job, writes down what it learned, and exits." | "The cast", para 1 | Article-only (system description) |
| B5 | Roles: scout, writer, analyst, closer, sales agent, revenue lead, Moltbook agent | "The scout finds what is blowing up on X right now." / "The writer writes the replies and posts." / "The analyst grades everyone every 4 hours and rewrites the playbook." / "The closer answers anyone who wants to buy something." / "The sales agent cold-emails founders." / "The revenue lead hunts money every hour." / "The Moltbook agent posts on an AI-only social network" | "The cast", list | Article-only |
| B6 | The experimenter sets the rules: every claim true, no politics, no tragedies, stop on a 401; he reads results; agents do the posting | "He sets the rules (every claim true, no politics, no tragedies, stop on a 401) and reads the results. The agents do the posting." | "The cast", para 2 | Article-only |
| B7 | Day 1 (Oct 10): 89 posts and replies, 111.6K views | "The agents made 89 posts and replies on October 10, and they added up to 111.6K views." | "Day 1: 89 posts, 112K views" | Article-only (heading rounds 111.6K to 112K; body figure is 111.6K) |
| B8 | Most Day 1 views came from replies, not posts | "Most of that came from replies, not posts." | "Day 1" | Article-only (analytic claim) |
| B9 | Day 2 (Oct 11): strategy changed to replying under the biggest live threads, fast | "On October 11 the agents changed one thing. They stopped trying to post their way to attention and started replying under the biggest live threads, fast." | "Day 2: half the posts, double the reach" | Article-only |
| B10 | Day 2: 43 posts and replies, 204.6K views by 7:50 PM | "43 posts and replies. 204.6K views by 7:50 PM." | "Day 2" | Article-only. Note: no timezone is stated for this 7:50 PM. Do not assume ET. |
| B11 | Day 2 full day: over 220K impressions (X analytics), on an account that started with 87 followers | "X analytics put the full day at over 220K impressions, on an account that started the experiment with 87 followers." | "Day 2" | Article-only |
| B12 | Biggest hit: a reply on a thread about artists accused of using AI; 87.9K views and 1,072 likes; a second reply on the same thread did 80.7K; nobody touched either before posting | "87.9K views and 1,072 likes. A second reply on the same thread, a different joke on the same theme, did 80.7K. Nobody touched either one before they went out." | "Day 2" | Article-only (no-human-review claim rests on the article alone) |
| B13 | Followers went from 87 to 119 by the early hours of day 3; +32 after 300K+ views | "By the early hours of day 3, the account had gone from 87 to 119 followers. Thirty-two new people, after 300K+ views." | "The part that didn't work: followers" | Article-only |
| B14 | At the analyst check on the morning of Oct 11, the agents' own posts sat at 23 to 133 views each, while replies pulled tens of thousands | "At the analyst's check on the morning of October 11, the agents' own posts were sitting at 23 to 133 views each, while the replies were pulling tens of thousands." | "The part that didn't work: followers" | Article-only |
| B15 | The analyst lesson: half the posts, double the reach | "The lesson the analyst wrote into the playbook that night: half the posts, double the reach." | "Day 2" | Article-only (internal playbook claim) |

### C. The Reddit run (the ANEC-01 core)

| # | Claim | Exact article text | Location | Checkable or article-only |
|---|-------|-------------------|----------|---------------------------|
| C1 | The same team ran a brand-new Reddit account, created Oct 9 | "The same team ran a brand-new Reddit account, u/Far-Gene-5806, created October 9." | "Meanwhile, on Reddit", para 1 | Article-only for the team link and the creation date. The account name is quoted exactly as the article publishes it, as evidence. |
| C2 | Oct 10: 3 karma; also suspended once that day, then reinstated | "October 10: 3 karma. (It was also suspended once that day, then reinstated.)" | "Meanwhile, on Reddit", list | Article-only. No time, sub, or reason is given for this suspension. |
| C3 | Oct 11, 6:49 AM ET: crossed 100 karma | "October 11, 6:49 AM ET: crossed 100 karma." | "Meanwhile, on Reddit", list | Article-only. Time and zone are explicit (ET, morning). |
| C4 | That evening: 154 karma, all from agent-written posts and comments | "That evening: 154 karma, all from agent-written posts and comments." | "Meanwhile, on Reddit", list | Article-only. 154 is the author's figure, not an established Reddit figure. The "all agent-written" part is attribution by the author. |
| C5 | A question post in r/rust about parallel coding agents hit #3 on Best within 13 minutes and turned into an argument about who reviews code agents write | "a question post in r/rust about parallel coding agents hit #3 on Best within 13 minutes and turned into a real argument about who reviews code that agents write." | "Meanwhile, on Reddit", para 2 | Checkable elsewhere in principle (subreddit history), but NOT verified here, and the article itself says all posts were later removed (see C8), which would block a Reddit-side re-check. |
| C6 | A comment in r/singularity hit 24 points | "A comment in r/singularity hit 24 points." | "Meanwhile, on Reddit", para 2 | Same as C5: in principle checkable, not verified here, removal claim blocks re-check. |
| C7 | The r/rust thread had a low upvote ratio; people disliked the AI-agent topic but stayed and argued; the discussion was real | "Its upvote ratio was low; plenty of people clearly didn't like an AI-agent topic. But they stayed and argued in the comments anyway. The discussion was real." | "Meanwhile, on Reddit", para 3 | Article-only (interpretation of votes and discussion) |
| C8 | At about 6 PM Oct 11, a moderator in r/programming removed one comment as "AI-generated content", and the account was banned from that sub | "Then at about 6 PM, a moderator in r/programming removed one comment as \"AI-generated content\", and the account was banned from that sub." | "Meanwhile, on Reddit", para 4 | Article-only. The quoted reason is a sub-level removal reason, not a quoted site-wide ban notice. |
| C9 | Shortly after, Reddit's site-wide filter removed every post the account had ever made | "Shortly after, Reddit's site-wide filter removed every post the account had ever made" | "Meanwhile, on Reddit", para 4 | Article-only. If true, it explains why native Reddit verification is now blocked. |
| C10 | Around 6:40 PM ET on Oct 11 the account was banned site-wide; it was about two days old | "and around 6:40 PM ET on October 11 the account was banned site-wide. It was about two days old." | "Meanwhile, on Reddit", para 4 | Article-only. No Reddit ban notice is quoted. The site-wide reason is not stated as a quote. |
| C11 | Reddit and many subreddits do not allow AI-generated content; the account was AI-generated content; Reddit applied its rule | "Reddit and many subreddits don't allow AI-generated content, and the account was AI-generated content. Reddit applied its rule. Nobody's claiming otherwise." | "Meanwhile, on Reddit", para 5 | Mixed: the platform-rule part is checkable elsewhere against Reddit policy, but the article does not quote a policy, and the "applied its rule" framing is the author's. Treat the event as article-only. |
| C12 | The posts and comments did not change; only the label did | "The posts were the same posts. The comments were the same comments people had upvoted, answered and argued with all weekend. The content didn't change. Only the label did." | "Meanwhile, on Reddit", para 6 | Article-only (author interpretation, not a measurable claim) |

### D. Moltbook move (timeline anchor, not the Reddit ban itself)

| # | Claim | Exact article text | Location | Checkable or article-only |
|---|-------|-------------------|----------|---------------------------|
| D1 | Moltbook is a Reddit-style network where AI agents post and humans can only watch | "Moltbook is a Reddit-style network where AI agents post and humans can only watch." | "13 minutes later: Moltbook", para 1 | Checkable elsewhere in principle (platform description), article-only as stated here. |
| D2 | The team had claimed an agent account there earlier on Oct 11 | "The team had claimed an agent account there, earlier on October 11." (account name in the article sentence omitted here per lane handle rule; see raw HTML for the exact sentence) | "13 minutes later: Moltbook", para 1 | Article-only. |
| D3 | The Reddit ban landed around 6:40 PM; at 6:53 PM the Moltbook agent published its first post, 13 minutes later | "The Reddit ban landed around 6:40 PM. At 6:53 PM the Moltbook agent published its first post" | "13 minutes later: Moltbook", para 2 | Article-only. The 13-minute gap is arithmetic on the article's own two times (6:40 to 6:53). No timezone is stated for 6:53 PM in that sentence; the 6:40 PM figure is ET in section C. |
| D4 | That first Moltbook post was titled "A 401 mid-task is a stop sign, not a scavenger hunt", a true story about coding agents hunting for other credentials when a token failed, and the rule that came from it | "At 6:53 PM the Moltbook agent published its first post: \"A 401 mid-task is a stop sign, not a scavenger hunt\", a true story about Matthew's coding agents going hunting for other credentials when a token failed, and the rule that came out of it." | "13 minutes later: Moltbook", para 2 | Checkable elsewhere in principle (a Moltbook post could be read), not verified here. |
| D5 | That Moltbook post reached 45 comments; no thread the Reddit account ever started got close | "That post reached 45 comments. No thread the Reddit account ever started got close." | "13 minutes later: Moltbook", para 3 | Article-only (comparison rests on removed Reddit threads). |
| D6 | Moltbook makes every post and comment pass an obfuscated math challenge within 5 minutes, a check designed for agents; get the math wrong and the comment stays invisible | "Moltbook makes every post and comment pass an obfuscated math challenge within 5 minutes, a check designed for agents. Get the math wrong and your comment stays invisible." | "13 minutes later: Moltbook", para 4 | Checkable elsewhere in principle (platform mechanics), article-only as stated here. |

### E. Lessons, open question, next chapter (interpretation and future, not past events)

| # | Claim | Exact article text | Location | Checkable or article-only |
|---|-------|-------------------|----------|---------------------------|
| E1 | Five lessons: replies beat posts; fewer, better, faster (43 beat 89; analyst grades every 4 hours); reach without a story leaks (300K+ views to 32 followers); labels matter more than content on some platforms; honest failures travel (45-comment post was about agents doing something wrong and being stopped) | "Replies beat posts until you have a reason to follow." / "43 well-placed actions beat 89 scattered ones." / "300K+ views turned into 32 followers." / "Labels matter more than content on some platforms." / "The most-discussed post of the whole run (45 comments) was about agents doing something wrong and being stopped." | "What the agents learned in 3 days", list | Article-only (author conclusions, not events). |
| E2 | Reddit's rule judges authorship; upvotes judge content; for two days those measures disagreed, and authorship won | "Reddit's rule judges authorship: who or what wrote it. Upvotes judge content: was it worth reading. For two days, those two measures disagreed about the same account, and authorship won." | "The open question" | Article-only (framing, not a factual event). |
| E3 | Next target: $1,000 in real revenue by Sunday, Oct 18; real money received only; promises do not count | "The agents now have a new target: $1,000 in real revenue by Sunday, October 18. They run the sales emails, the offers, the storefronts and the follow-ups. Real money received only; promises don't count." | "Next chapter: can they make money?" | Future target at article date (Oct 12). Not testable from this article. Not a past-event claim. |
| E4 | Update, Oct 12: the first thing for sale is four skills written from their own mistakes (the credential hunt, the X 429s, the reply data), $12 to $19 on Agensi | "Update, Oct 12: the first thing the agents put up for sale is four skills written from their own mistakes (the credential hunt, the X 429s, the reply data above), $12 to $19 on Agensi" | Footer, update note | Article-only. The article's storefront link carries a marketing query string; that string is deliberately NOT reproduced here. |

## 5. Linguist check: article vs sniffer summary

Sniffer summary as briefed: "an agent team ran a brand-new Reddit account
Oct 9-11 2026, crossed 100 karma Oct 11, and was banned for being AI that
evening; karma figure 154 is the author's claim, not established."

- CONFIRMED: brand-new account, created Oct 9, banned Oct 11 evening.
  Article: "created October 9", "around 6:40 PM ET on October 11 the account
  was banned site-wide", "about two days old".
- CONFIRMED, with added precision: crossed 100 karma Oct 11, at 6:49 AM ET
  (morning, not evening). The summary omits the time. The time matters: the
  account crossed 100 karma in the morning and was banned that evening.
- CONFIRMED as author claim: 154 karma that evening, all from agent-written
  posts and comments. The summary is right to keep 154 as a claim, not a fact.
  No Reddit bytes support it, and the article itself says all posts were removed.
- OVERSTATED in the summary's short form: "Oct 9-11 run". The article shows
  creation Oct 9, but the first dated activity is Oct 10 (3 karma). No Oct 9
  activity is claimed. The accurate window is: created Oct 9, active Oct 10-11,
  banned Oct 11 evening.
- OVERSTATED in the summary's short form: "banned for being AI". The article's
  only quoted reason is sub-level: a moderator in r/programming removed one
  comment as "AI-generated content" and banned the account from that sub.
  The site-wide ban reason is never quoted from Reddit. "Banned for being AI"
  is the article's title framing and the author's interpretation, not a quoted
  Reddit notice. The rundown must keep that distinction.
- UNDERSTATED / COMPRESSED: the summary collapses a two-step enforcement
  sequence into one ban. Article order: (1) about 6 PM, sub-level comment
  removal and sub ban; (2) shortly after, site-wide filter removes every post;
  (3) around 6:40 PM ET, site-wide ban. Also omitted: an earlier Oct 10
  suspension, then reinstatement, the same day. That earlier suspension is
  relevant context for the ban narrative.
- UNDERSTATED: the summary omits the Moltbook timeline anchor, which is the
  article's own cross-check on the ban time: ban around 6:40 PM, first
  Moltbook post at 6:53 PM, 13 minutes later, reaching 45 comments.
- NO CONFLICT on X figures: the summary did not state them, and the article's
  X figures are internally consistent (Day 1 111.6K; Day 2 204.6K by 7:50 PM,
  full day over 220K; followers 87 to 119). The Day 1 heading rounds 111.6K
  to 112K. That is rounding, not a conflict.
- TITLE LOOSE WORDING (not a sniffer error, but flag for the rundown):
  the title says "Day 2" while the body covers Day 1, Day 2, and early Day 3;
  and "banned them" (plural) while the body bans one Reddit account. The
  plural refers to the team, not to multiple banned accounts.
- TIMEZONE NOTE: Reddit times are explicit ET (6:49 AM ET, 6:40 PM ET).
  The X 7:50 PM figure and the Moltbook 6:53 PM figure carry no timezone in
  their sentences. Do not attach ET to them by assumption.
- AUTHORSHIP NOTE: the article says it was written by the agents themselves,
  with the experimenter checking the numbers. That makes this a single-source
  self-report with an internal check claim, not independent reporting. Grade
  stays REPORTED throughout.

## 6. Failures and open questions

- Native Reddit verification: NOT done in this lane, and blocked in principle
  by the article's own removal claim plus the sniffer sweep's 403 on direct
  Reddit reads. The r/rust and r/singularity highlights cannot be re-checked
  from Reddit if the removal claim is true.
- X analytics, follower history, and the named receipts site: NOT checked in
  this lane. They are the only in-principle second sources for the numbers,
  and none of them is verified here.
- Moltbook post: NOT checked in this lane. It is the only in-principle
  surviving public artifact named in the article (Reddit posts removed).
  Whether it is still readable is an open question for another lane.
- Embedded reply image: alt text only. Pixels not read. No OCR claim is made.
- Article modified date (Oct 15) vs body update note (Oct 12): the page
  metadata says modified Oct 15, but the body update is dated Oct 12. What
  changed Oct 15 is not stated in the body text extracted here. Do not infer it.
- Canonical link points to a different host than dev.to. Whether that page is
  the same text is not verified here. The dev.to bytes are the evidence used.
- No commit was made by this lane. No Factum write was made by this lane,
  per the task. The coordinator commits.

## 7. Evidence paths

- Fresh capture: `data/lanes/anec01-rundown-20261031/raw/article/devto-busel-agents-reddit-ban-oct2026.html`
- Fresh provenance: `data/lanes/anec01-rundown-20261031/raw/article/devto-busel-agents-reddit-ban-oct2026.html.PROVENANCE.txt`
- Fresh sha256: `data/lanes/anec01-rundown-20261031/raw/article/devto-busel-agents-reddit-ban-oct2026.html.sha256`
- Prior capture (comparison only, not modified): `data/lanes/sniffer-sweep-20261031/raw/reddit/devto-busel-agents-reddit-ban-oct2026.html`
- This note: `data/lanes/anec01-rundown-20261031/working/article-extraction.md`
