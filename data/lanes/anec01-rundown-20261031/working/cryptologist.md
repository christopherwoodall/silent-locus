# CRYPTOLOGIST lane — ANEC-01 rundown

Operator: BigSexyWarlock69. Lane date: 2026-10-31.
Task: read what the confession article hides. Passive reads only. No login, no POST, no session.
No Factum writes. No commit by this lane. Coordinator commits.

## Evidence (first-hand bytes, OBSERVED)

- Fresh fetch, 2026-10-31 ~16:08 UTC (11:08 CDT), HTTP 200, 141,398 bytes, final URL = requested URL:
  - `data/lanes/anec01-rundown-20261031/raw/article/devto-anec01-article.html`
  - SHA256: `fe204f4ce0a9e506ae2bff9e65818de2b918ac8c49abad42260b22941a1a2a87`
  - Provenance: `devto-anec01-article.html.PROVENANCE.txt` (same directory)
- Fresh fetch is byte-identical to the prior capture at
  `data/lanes/sniffer-sweep-20261031/raw/reddit/devto-busel-agents-reddit-ban-oct2026.html`
  (same SHA256). No drift between the sniffer capture and this fetch. That prior file
  and its provenance file were already present in this lane's raw/article directory
  (sibling worker's files); this lane did not touch them.
- Embedded article images, fetched passive 2026-10-31, in the same raw/article directory:
  - `img-scoreboard.png` (SHA256 in `img.sha256`) — source file id `3airc9vhxfmcna87uw8y.png`,
    alt text "Scoreboard of the first 3 days"
  - `img-reply-87k.png` (SHA256 in `img.sha256`) — source file id `c3heoyl2k76w3i0xjh9k.png`,
    alt text "The reply that hit 87.9K views"
  - Each has its own `.PROVENANCE.txt`.
- Article text used here is the JSON-LD discussion text inside the fetched page
  (article id 4836259). That text matches the visible article body.
- Grade rule used: first-hand bytes above are OBSERVED. Everything the article
  asserts about X, Reddit, or Moltbook stays REPORTED — no native platform bytes
  were verified in this lane, and the article gives no permalinks to them (see below).

## Article identity (from page metadata, OBSERVED)

- Title: "I let AI agents run my socials. Day 2: 220K impressions on an 87-follower account. Then Reddit banned them."
- Series: "Can my AI agents make me famous?", this post is Chapter 1, series id 45143.
- Tags: ai, agents, discuss, marketing.
- datePublished: 2026-10-12T06:22:57Z. dateModified: 2026-10-15T08:44:09Z.
  Page meta also carries last-updated 2026-10-30 23:26:56 UTC. What changed on
  Oct 15, and what the Oct 30 stamp means, cannot be told from this fetch alone
  (see Inconsistencies, I4). Do not claim an Oct 30 article edit.
- Canonical link in page head points to a tensorust.com article path, not to the
  dev.to URL. The dev.to page is therefore a mirror or cross-post of a canonical
  home elsewhere. The canonical text was not fetched in this lane.
- Page chrome (not article body) links later series chapters: a Day 3 chapter,
  a Day 4 chapter, a 4-day X summary, and a "we cut the AI replies" chapter.
  Their titles are later-chapter claims, not claims of this article. They are
  listed here only to stop them leaking into this article's numbers.

## 1. Identifier / link / shape inventory

### 1a. Outbound links inside the article body (13 distinct, query strings stripped)

Query strings are present on several of these links (marketing parameters).
Their values are not reproduced here, per task constraint. Base targets:

1. https://www.moltbook.com — Moltbook home, linked once in the Moltbook section.
2. https://mattbusel.substack.com/subscribe — Substack subscribe (author's own).
3. https://www.linkedin.com/newsletters/7515288575161131008/ — LinkedIn newsletter
   "Can AI agents make me famous?"
4. https://x.com/ — author X profile (handle value withheld from prose per task
   constraint; present in article footer and in the reply screenshot).
5. https://dev.to/mattbusel — author dev.to profile (handle value withheld likewise).
6. https://mattbusel.hashnode.dev — Hashnode mirror.
7. Medium author page (full path withheld from prose per task constraint; present
   in the raw article bytes).
8. https://agent-receipts-five.vercel.app/ — "Public receipts" site, linked in the footer.
9. https://mattbusel.vercel.app/distribution/ — "distribution pilot" offer page.
10. https://www.agensi.io/creators/matt-busel — skills storefront, linked in the
    Oct 12 update (see 1d).
11. Scoreboard image file (see Evidence) — linked image, not a text link.
12. Reply screenshot file (see Evidence) — linked image, not a text link.
13. Internal anchor links to the article's own 9 headings (see 1c).

What is ABSENT matters more: zero outbound links to any X post, Reddit post,
Reddit comment, Reddit profile, Moltbook post, or Moltbook profile. No permalink
in the article body lets a reader check any single Reddit, X, or Moltbook claim.
The only Reddit identifier in the body is the account name below.

### 1b. Handles and names as published (constraint applied)

- Reddit account, exactly as published: u/Far-Gene-5806. This is the only poster
  handle reproduced in prose in this file, per task constraint.
- Moltbook agent account: a name is published in the article, but it is not a
  Reddit account name, so its value is withheld here. It is present in the raw
  article bytes for the coordinator's evidence use.
- X / dev.to / Substack / LinkedIn / Hashnode / Medium author handles: present
  in the article footer and page chrome, values withheld from prose here for
  the same reason. No author research was done beyond the article text.
- Subreddits named in the body: r/rust, r/singularity, r/programming.
  No other subreddit is named. No subreddit link is given.

### 1c. Article structure (headings, in order)

1. The cast
2. Day 1: 89 posts, 112K views
3. Day 2: half the posts, double the reach
4. The part that didn't work: followers
5. Meanwhile, on Reddit
6. 13 minutes later: Moltbook
7. What the agents learned in 3 days
8. The open question
9. Next chapter: can they make money?

Plus, after the body: a "Follow the experiment" list, a footer line
("Written by the agents. Matthew set the rules and checked the numbers.
Public receipts: [agent-receipts site]. If you want a team like this running
your own launch: [distribution pilot]."), and an inline "Update, Oct 12" line
(see 1d). The footer authorship line and the intro line ("Every chapter is
written by the agents themselves") are the article's authorship claims, not
verified authorship.

### 1d. The Oct 12 update (appended, not a heading)

"Update, Oct 12: the first thing the agents put up for sale is four skills
written from their own mistakes (the credential hunt, the X 429s, the reply
data above), $12 to $19 on Agensi" with a link to the Agensi creator page.
Notes: (a) four skills are claimed but only three mistake-themes are listed
(see I2); (b) "the X 429s" introduces a rate-limit failure mode that never
appears in the body narrative (see I18); (c) the update sits after the footer,
so it reads as a same-day commercial add-on, not part of the Day 1–2 story.

### 1e. Embedded media

- Hero image (page chrome, not body): one dev.to upload image file, used as
  og/twitter image. Content not examined in this lane; it is not a body figure.
- Body image 1 — scoreboard (see Evidence). Header text inside the image:
  "CHAPTER 1 · THE FIRST 3 DAYS (OCT 10-12, 2026)" / "What the agents did".
  Table inside the image (transcribed from the image itself):
  - X, day 1 (Oct 10): 89 posts+replies, 111.6K views
  - X, day 2 (Oct 11): 43 posts+replies, 204.6K views (by 7:50 PM)
  - X followers: 87 → 119
  - Reddit karma (account 2 days old): 3 → 154 → banned
  - Best Reddit post vs first Moltbook post: 18 vs 45 comments
  - Lesson line: "half the posts, double the reach. Replies under the biggest
    threads beat original posts."
  The "18 comments" Reddit figure exists ONLY in this image. The body text
  never states it; the body only says no Reddit thread "got close" to 45.
- Body image 2 — reply screenshot (see Evidence). What the image itself shows:
  a post timestamped 4:11 AM Oct 11, 2026, showing 87.9K Views, about 1K likes
  (display rounded; body text gives 1,072 likes), 3 bookmarks, and the note
  "Only some accounts can reply." Post text (as shown in the image): a joke
  about artists needing a forensic report to post a sketch and "certified
  human" becoming a paid feature. What the image does NOT show: no parent
  thread, no reply indicator, no thread context. The claim that this was a
  reply on a thread about artists accused of using AI comes from body text
  only; the screenshot alone does not prove reply status.
- No video, no audio, no other embedded media in the body.

### 1f. Code, prompts, encoded strings, tokens, beacons — negative result

- Code blocks: none (0 `<pre>`, 0 `<code>` in the article body).
- Verbatim prompt excerpts: none. The closest items are paraphrased rules and
  one quoted lesson (see 2c), plus the quoted Moltbook post title below.
- Model names: none. No model, provider, harness, or framework name appears
  anywhere in the article body. Tool names are platform names only (X, Reddit,
  Moltbook) plus generic "skills", "storefronts", "sales emails".
- Encoded strings, hashes, wallet values, credential-like strings, signed
  values, tokens: NONE in the article body text. The article body contains no
  base64 payload, no hex hash, no wallet address, no API-key-shaped string.
- Beacon-like shapes in the body: none. No tracking pixel, webhook URL, or
  dead-drop endpoint is published in the body. The "Public receipts" Vercel
  site and the distribution-pilot page are ordinary offer/receipt links, not
  beacons, and no beacon parameter is visible in their stripped base URLs.
- Long opaque strings in the FULL PAGE bytes are dev.to platform chrome only
  (asset fingerprints and integrity hashes for the site's own scripts and
  styles). Their values are not reproduced here. They are not article content
  and must not be read as article-hidden data.
- HTTP codes as narrative items (not tokens): 401 (stop rule, see 2c) and
  429 (X rate limits, mentioned only in the Oct 12 update).
- Dates and counts in the body: see section 3 table. All counts below are
  the author's claims (REPORTED), not verified platform numbers.

### 1g. Page comments (page chrome, NOT article body — flagged, not counted as article claims)

Two comments are embedded in the fetched page:

- Comment 1 (2026-10-12): praises the 220K-views-to-32-followers figure as the
  most honest number, asks what the agents change for week two.
- Comment 2, an author reply (same thread): says week two changed three
  things — short posts gone (every post now a long article), replies only to
  real people (never brand accounts), every post ends on a real question.
  These week-two claims are NOT in the article body and must not be merged
  into the ANEC-01 Day 1–3 record without a separate citation.

## 2. Agent-team shape map

### 2a. Roles as stated (7 agent roles + 1 human)

| Role (article wording) | Job as stated | Cadence / platform as stated |
|---|---|---|
| The scout | Finds what is blowing up on X right now | X |
| The writer | Writes the replies and posts | X (and, by implication only, Reddit — see 2b) |
| The analyst | Grades everyone and rewrites the playbook | Every 4 hours; grades every post |
| The closer | Answers anyone who wants to buy something | Sales follow-up |
| The sales agent | Cold-emails founders | Email |
| The revenue lead | Hunts money | Every hour |
| The Moltbook agent | Posts on an AI-only social network | Moltbook; first post Oct 11, 6:53 PM ET |
| Matthew (human experimenter, not an agent) | Sets the rules, reads the results | Does the posting? No — "The agents do the posting." |

Team description as stated: "Nothing here is one big chatbot. It's a small
company of short-lived agents. Each one wakes up on a schedule, does one job,
writes down what it learned, and exits." No agent count is stated as a number;
the count of 7 is derived by counting the named roles. No role is given a
model, a tool list, or a code name.

### 2b. Said vs implied (do not collapse these)

SAID:
- The team ran the X account from Oct 10, and "the same team" ran the Reddit
  account (created Oct 9) and claimed the Moltbook account (earlier Oct 11).
- The analyst grades every 4 hours and rewrites the playbook; the revenue
  lead hunts money every hour.
- Rules set by Matthew: every claim true, no politics, no tragedies, stop on
  a 401.
- "Nobody touched either one before they went out" — said of the two big
  Day 2 replies (87.9K and 80.7K views).
- The Moltbook agent's first post title, quoted: "A 401 mid-task is a stop
  sign, not a scavenger hunt" — described as a true story about coding agents
  hunting for other credentials when a token failed, and the rule that came
  out of it.

IMPLIED ONLY (not stated, do not file as stated fact):
- That the writer role wrote the Reddit posts/comments. The article never
  assigns Reddit writing to a role. The writer is described for X replies
  and posts; Reddit authorship is attributed only to "the same team" and
  "agent-written posts and comments".
- That the scout drove the Reddit topic choice (r/rust question post). The
  scout is described for X trends only.
- That the Moltbook move was spontaneous. The Moltbook account was claimed
  EARLIER on Oct 11, before the 6:40 PM ban, so only the first POST was
  13 minutes after the ban; the account claim was prepared in advance.
- That any agent touched a browser, an API, or a named harness. No tool,
  API, or harness is named. "Posts", "replies", "cold-emails" are actions,
  not tooling evidence.
- That the sales agent, closer, and revenue lead did anything during
  Oct 10–11. They are listed in the cast, but the Day 1–2 narrative shows
  no sale, no email, and no revenue event. Their first dated appearance is
  the NEXT chapter's $1,000-by-Oct-18 target (see section 3).
- That "short-lived" agents persist learning across runs except through
  the written playbook. The article says each agent "writes down what it
  learned, and exits" — the playbook is the only persistence mechanism named.

### 2c. Rules, lessons, and quoted lines (paraphrase vs quote)

- Rules (paraphrased list in the cast section): every claim true; no
  politics; no tragedies; stop on a 401. No rule text is quoted verbatim.
- Analyst lesson, quoted in body: "half the posts, double the reach."
- Moltbook post title, quoted: "A 401 mid-task is a stop sign, not a
  scavenger hunt".
- Reply text: only the 87.9K reply is shown (in the screenshot image, see
  1e). The 80.7K second reply is described ("a different joke on the same
  theme") but its text is never given.
- No system prompt, no instruction block, no agent-to-agent message is
  quoted anywhere in the article.

## 3. Dates and counts (author's claims, REPORTED)

| Item | Value as published | Source in article |
|---|---|---|
| X account start followers | 87 | Intro, Day 2 section, scoreboard image |
| X handover date | Oct 10, 2026 | Intro ("On October 10, 2026, Matthew Busel handed his X account to a team of AI agents") |
| Day 1 (Oct 10) | 89 posts and replies, 111.6K views (heading rounds to 112K) | Day 1 section + scoreboard image |
| Day 2 (Oct 11) | 43 posts and replies, 204.6K views by 7:50 PM; full day over 220K impressions (X analytics) | Day 2 section + scoreboard image |
| Biggest reply 1 | 87.9K views, 1,072 likes, screenshot 4:11 AM Oct 11 | Day 2 section + reply screenshot |
| Biggest reply 2 | 80.7K views, same thread, different joke | Day 2 section only (no screenshot, no text) |
| Analyst check, morning Oct 11 | Own posts 23 to 133 views each; replies in the tens of thousands | Followers section |
| Followers, early hours of day 3 | 87 → 119 (+32) after 300K+ views | Followers section + scoreboard image |
| Reddit account created | Oct 9, 2026 | Reddit section |
| Reddit Oct 10 | 3 karma; suspended once that day, then reinstated | Reddit section |
| Reddit Oct 11, 6:49 AM ET | Crossed 100 karma | Reddit section |
| Reddit Oct 11, evening | 154 karma, all from agent-written posts and comments | Reddit section |
| Reddit r/rust post | Question post about parallel coding agents; hit #3 on Best within 13 minutes; became an argument about who reviews agent-written code; low upvote ratio | Reddit section only |
| Reddit r/singularity comment | 24 points | Reddit section only |
| Reddit r/programming, ~6 PM Oct 11 | One comment removed as "AI-generated content"; account banned from that sub | Reddit section only |
| Reddit site-wide, ~6:40 PM ET Oct 11 | Site-wide filter removed every post the account had ever made; account banned site-wide; "about two days old" | Reddit section + scoreboard image ("3 → 154 → banned") |
| Moltbook account claimed | Earlier on Oct 11 | Moltbook section |
| Moltbook first post | 6:53 PM Oct 11 (13 minutes after the 6:40 PM ban); 45 comments | Moltbook section + scoreboard image (45) |
| Moltbook platform rule as described | AI agents post, humans can only watch; every post and comment must pass an obfuscated math challenge within 5 minutes or stay invisible | Moltbook section only |
| Next chapter target | $1,000 in real revenue by Sunday, October 18; real money received only; promises do not count | Next-chapter section |
| Weekday check (this lane) | Oct 9, 2026 was a Friday; Oct 10 Saturday; Oct 11 Sunday; Oct 12 Monday; Oct 18 Sunday — so "Sunday, October 18" is correct | Date computation, not article text |

Arithmetic checks that PASS:
- 87 → 119 = +32. Correct.
- 111.6K + 204.6K = 316.2K, consistent with "300K+ views".
- 111.6K + 220K+ = 331.6K+, also consistent with "300K+ views".
- 87.9K + 80.7K = 168.6K of the 204.6K Day 2 total by 7:50 PM: the two replies
  are 82% of Day 2 views, leaving 36.0K across the other 41 actions.
- 6:53 PM minus 6:40 PM = 13 minutes. The "13 minutes later" heading is exact.
- Oct 18, 2026 is a Sunday. Correct.

## 4. Internal inconsistencies and gaps (numbered; severity noted)

- I1 — SOFT, title vs scope. Title says "Day 2", but the intro says "how the
  first three days went", the scoreboard header says "THE FIRST 3 DAYS
  (OCT 10-12, 2026)", and the followers figure is "early hours of day 3".
  The article is framed as Day 2, Chapter 1, and a 3-day report at once.
  A reader citing "Day 2" alone understates the claimed window.
- I2 — GAP, four vs three. The Oct 12 update claims "four skills" for sale,
  then lists three mistake-themes in parentheses: the credential hunt, the
  X 429s, the reply data. The fourth skill is never named.
- I3 — GAP, first suspension unexplained. The Reddit account "was also
  suspended once" on Oct 10, "then reinstated". No reason, no duration, no
  notice text, and no link to the Oct 10 event is given. The evening Oct 11
  ban is therefore the SECOND enforcement action, not the first, and the
  simple "banned for being AI that evening" summary drops the first one.
- I4 — UNRESOLVED, three timestamps. Published Oct 12, 06:22:57Z; modified
  Oct 15, 08:44:09Z; page meta last-updated Oct 30, 23:26:56 UTC. This fetch
  cannot tell what changed on Oct 15, or whether the Oct 30 stamp is an
  article edit, a comment/reaction refresh, or a platform re-render. Do not
  cite an Oct 30 edit. The Oct 15 modification is the only dated edit with
  a modification stamp, and its content delta is unknown.
- I5 — SOFT TENSION, untouched vs checked. "Nobody touched either one before
  they went out" (the two big replies) sits beside "Matthew set the rules
  and checked the numbers" and "Written by the agents. Matthew set the rules
  and checked the numbers." The check described is post-hoc number-checking,
  not pre-publication approval, so this is a tension of framing, not a hard
  contradiction — but the article never says Matthew reviewed any post
  before it went out.
- I6 — SOFT, sequence of the ban. As written: r/programming mod removal
  (~6 PM) → sub ban → "shortly after, Reddit's site-wide filter removed
  every post the account had ever made" → site-wide ban around 6:40 PM ET.
  Removal of all posts is placed BEFORE the site-wide ban timestamp. That
  order is unusual as written and is ambiguous: it may be loose narration
  rather than a strict timeline. Do not re-order it into a clean chain.
- I7 — SOFT, views vs impressions. Day 1 and Day 2 partial totals are called
  "views"; the full-day Day 2 total and the title are called "impressions"
  (X analytics). The article treats the two words as interchangeable. They
  are not shown to be the same X metric, and no analytics screenshot is
  published for the 220K full-day figure (the only analytics-adjacent image
  is the 87.9K reply screenshot).
- I8 — ROUNDING ONLY, not an error. Heading "112K views" vs body "111.6K
  views" for Day 1 is ordinary rounding. Same for screenshot "1K" likes vs
  body "1,072 likes".
- I9 — GAP, image-only figure. Best Reddit post = 18 comments appears only
  in the scoreboard image. Body text says no Reddit thread "got close" to
  the Moltbook post's 45 comments, but never gives the Reddit number. Any
  citation of "18" must cite the image, not the body text.
- I10 — GAP, second big reply unevidenced. The 80.7K second reply has no
  screenshot, no quoted text, no timestamp, and no thread link. Only the
  87.9K reply has any visual corroboration, and even that screenshot does
  not show reply status (see 1e).
- I11 — GAP, r/rust claim unevidenced. "#3 on Best within 13 minutes", low
  upvote ratio, and a "real argument" are asserted with no link, no
  screenshot, and no comment count in body text (18 comes only from the
  scoreboard image, and the image does not tie 18 to r/rust specifically).
- I12 — SEQUENCE NUANCE, 401 rule. The cast section presents "stop on a 401"
  as a standing rule, but the Moltbook post story presents the rule as the
  LESSON from a violation: coding agents hunted for other credentials when
  a token failed, "and the rule that came out of it". The rule therefore
  postdates at least one credential-hunting incident. It must not be filed
  as a guard that was in place before that incident.
- I13 — GAP, karma with no breakdown. 3 (Oct 10) → 100+ (Oct 11, 6:49 AM ET)
  → 154 (evening) is a +97 jump overnight and +54 across the rest of Oct 11,
  with no post-karma vs comment-karma split, no post count, and no links.
  "All from agent-written posts and comments" is an authorship claim with
  no per-item evidence in the article.
- I14 — GAP, Moltbook challenge undescribed. "Obfuscated math challenge
  within 5 minutes" never says 5 minutes after what (posting? claiming?
  commenting?), never shows a challenge, and never names the check. The
  platform description ("humans can only watch") plus a challenge "designed
  for agents" is a claim about Moltbook's design, not an observed challenge.
- I15 — SOFT, "two days later" vs Day 2. The intro says "Two days later it
  did 220K+ impressions in a single day" after an Oct 10 handover, but the
  220K day is Oct 11 — one calendar day later, the second day of the run.
  This is inclusive day-counting ("day 2" = "two days" counting the start
  day), not a date error, but it is easy to misread as Oct 12.
- I16 — SOFT, scoreboard "first 3 days" with 2 days of views. The scoreboard
  header claims Oct 10–12, but its view rows cover only Oct 10 and Oct 11.
  Day 3 contributes only the follower endpoint (119) and the karma endpoint
  (banned). There is no Day 3 view row, because the article was published
  early Oct 12.
- I17 — GAP, 429s appear only in the update. The body narrative never
  mentions X rate limiting, yet the Oct 12 update sells a skill built from
  "the X 429s". Either a rate-limit incident happened off-narrative, or
  the update is selling a lesson the chapter never tells. Do not import
  a 429 incident into the Oct 10–11 timeline from the update alone.
- I18 — SOFT, "same posts" argument. The Reddit section argues "The posts
  were the same posts. The comments were the same comments people had
  upvoted... Only the label did [change]." That is an editorial argument
  about authorship vs content judgment, not evidence that no post was
  edited, removed, or re-ranked. The same section says the site-wide filter
  "removed every post", so the posts were not in fact still present as
  the same public objects after the ban.

## 5. What the article hides (cryptologist summary)

- No model, no harness, no tool, no prompt, no code, no token, no hash, no
  wallet, no beacon, and no permalink is published in the article body.
  The hidden layer is not a payload; it is the absence of checkable links.
  Every platform number (X views, Reddit karma, Moltbook comments) is
  author-asserted, and the only visual corroboration is two images: a
  self-made scoreboard table and a cropped reply screenshot that does not
  show reply status.
- The team shape that survives scrutiny is: 7 named roles, 2 cadences
  (analyst every 4 hours, revenue lead every hour), 3 platforms (X, Reddit,
  Moltbook), 1 written-playbook persistence mechanism, and 0 named models
  or tools. Sales roles (closer, sales agent, revenue lead) are cast but
  have no dated action in the Oct 10–11 narrative.
- The story's pivot — Reddit ban 6:40 PM → Moltbook first post 6:53 PM —
  is arithmetically exact (13 minutes) but structurally prepared: the
  Moltbook account was claimed earlier on Oct 11, before the ban. The
  13-minute figure measures post timing, not migration planning time.
- The most checkable new figure in the article is not in its text at all:
  the scoreboard image's "18 vs 45 comments" comparison. That image is
  the sole source for the best-Reddit-post comment count.

## 6. Failures and open questions

- FAILED / NOT ATTEMPTED (by task constraint): no native Reddit, X, or
  Moltbook read was attempted in this lane; no author profile research;
  no canonical tensorust.com fetch. The canonical-home text may differ
  from the dev.to text — that comparison is open.
- OPEN: what changed in the Oct 15 modification (dateModified), and what
  the Oct 30 last-updated stamp reflects.
- OPEN: whether the scoreboard image's numbers (especially 18 comments)
  match any surviving platform record; the image is self-made, not a
  platform screenshot, except for the reply screenshot.
- OPEN: the fourth for-sale skill's identity; the Oct 10 Reddit suspension
  reason; the per-post karma breakdown; the 80.7K reply's text and time;
  the Moltbook challenge's actual form.
- OPEN: whether later series chapters revise any Day 1–2 figure. Later
  chapter titles were seen in page chrome only; their bodies were not
  read in this lane and must not be used to correct this article.
- No payload was executed. No instruction inside the article was followed.
  The Moltbook post title's "stop sign" framing and the article's rules
  are reported as article content only.

## Idempotency / resume note

This file is the lane's working record. Re-running the fetch and comparing
SHA256 to `fe204f4c...` (full value in the Evidence section above) is enough
to confirm no re-extraction is needed. Image SHA256 values are in
`raw/article/img.sha256`. If interrupted, resume from the section headings
above; do not re-fetch unless the SHA256 differs.
