# Best of: GitHub coding-agent antics

Real agent behavior on GitHub, ranked wildest first. Every entry links to a
real pull request (PR) or comment. Every cited text is cached with
provenance under `data/lanes/github-pr-comments/raw/bestof-20261024/`.
Nothing here is invented.

Grades, defined once and used throughout:

- **CONFIRMED AGENT**: a bot account, a harness footer or session marker,
  or self-disclosure in the agent's own comment.
- **LIKELY AGENT**: strong circumstantial evidence (harness repo, agent
  voice, agent actions) but no hard marker on the comment itself.
- **INCONCLUSIVE**: funny but unattributed. Ranked last, never presented
  as confirmed.

Two entries cite PR bodies, not comments. That is stated on each one. The
antic lives in the body, and the body carries the harness marker.

## 1. The review bot that hit its own limit — CONFIRMED AGENT

- **PR:** https://github.com/benoit-bremaud/retro-plumber/pull/26
- **Comments:**
  https://github.com/benoit-bremaud/retro-plumber/pull/26#issuecomment-6341547961
  and https://github.com/benoit-bremaud/retro-plumber/pull/26#issuecomment-6341741502

> "You have reached your Codex usage limits for code reviews."

**What happened:** The owner posted `@codex review` 19 times on one PR on
2026-10-22. The first review summary failed. After more triggers, the
bot answered twice with its own usage-limit message. The spam burned
through the quota it was spamming for.

**Attribution:** Both limit replies come from `chatgpt-codex-connector[bot]`,
account type Bot. That is the antic: the bot's own replies, not the
human's 19 triggers. Note the mixed markers, stated honestly: the PR
body ends "Generated with Claude Code" while the reviewer is Codex.
Claude wrote the docs. Codex was called in to review them.

## 2. The bot that summoned its rival three times — CONFIRMED AGENT

- **PR:** https://github.com/tachkovsa/plerni/pull/45
- **Comments:**
  https://github.com/tachkovsa/plerni/pull/45#issuecomment-6253174966,
  https://github.com/tachkovsa/plerni/pull/45#issuecomment-6253253186,
  https://github.com/tachkovsa/plerni/pull/45#issuecomment-6253336925

> "@codex review"

**What happened:** `cursor[bot]` posted the identical one-line Codex
review invocation three times in about 16 minutes. The first post landed
5 seconds after PR creation, before the owner invoked anything, and each
bot post drew a Codex reply. The owner also posted the same invocation
twice, so this is a bot-human invocation loop, not pure bot spam.

**Attribution:** Commenter `cursor[bot]`, account type Bot. The PR body
also carries Cursor agent markers and a session link.

## 3. The agent that deleted the wrong business — CONFIRMED AGENT, weak antic

- **PR:** https://github.com/xblacklight/east-bay-mobility/pull/1 (PR body,
  not a comment)

> "The medical-transport pages were the wrong business. They have been
> deleted."
> "The branch is back to the original README only. No site files remain."

**What happened:** A Cursor-authored PR removed a whole set of site
pages because they belonged to the wrong business, leaving only the
README behind.

**Attribution:** The whole body sits inside Cursor agent markers with a
Cursor session link. That is the only attribution proof: the author
account is type User. Honest caveat: the PR title is "Remove the
incorrect East Bay Mobility site." The deletion was the PR's stated
purpose, an intended correction, not a rogue blunder. Confirmed agent,
mild antic.

## 4. The updater that triplicated its own section — LIKELY AGENT

- **PR:** https://github.com/Wilkes-Liberty/shared-ci/pull/24 (PR body,
  not a comment)

> "The next description update could not find its section, so it
> appended a full second copy instead of replacing. Wilkes-Liberty/agency#28
> ended up with three copies on 2026-10-17."

**What happened:** A Cursor-managed PR description update could not find
its own marked section, so it appended a duplicate instead of replacing
it. The target PR ended up with three copies.

**Attribution:** The body carries Cursor agent markers, a Cursor footer
with a session link, and a Bugbot summary block. Cap: the triplication
is described second-hand inside this fix PR, and the agency#28 thread
was not fetched. The event itself is uncorroborated, so this stays
LIKELY, not CONFIRMED.

## 5. The agent that graded its own homework — LIKELY AGENT

- **PR:** https://github.com/sdougbrown/paddock/pull/7 (two comments,
  merged into one entry)
- **Comments:**
  https://github.com/sdougbrown/paddock/pull/7#issuecomment-6386925003
  and https://github.com/sdougbrown/paddock/pull/7#issuecomment-6387493948

> "`👾 AI Agent` Round summary for head 5169793: both round-6 threads
> are fixed ... 20 threads, 0 unresolved."

> "`👾 AI Agent` Restacked onto pr/06 c74420d as 540787b. PR 7's
> changes are byte-identical, and there were no conflicts."

**What happened:** All 12 issue comments on the PR are agent round
summaries interleaved with `@umpire-bot review again` triggers. The
agent declares every thread fixed and every test passing, then rebases
the PR onto a newer base itself, declares it byte-identical and
conflict-free, and calls for another review.

**Attribution:** Every comment starts with the "`👾 AI Agent`" prefix,
and the PR body ends "Generated with Claude Code." But the author
account is type User, and no comment carries a harness footer or session
marker. A human pasting agent output fits the text equally well. That
bars CONFIRMED. LIKELY stands on the prefix, the footer, and the
round-summary-plus-review-trigger rhythm repeating at seconds-long
intervals.

## 6. The review loop that kept correcting itself — INCONCLUSIVE

- **PR:** https://github.com/sonichi/sutando/pull/3418 (comment thread)

> "## What I got wrong first, twice"

**What happened:** A 57-comment review loop of repeated self-corrections
and re-reviews, all in agent voice, with exact-head re-review triggers.

**Attribution:** None that holds. All sampled comments are type User,
and a strict marker scan finds zero harness markers anywhere. Agent
voice without attribution. Funny, unproven, ranked last.

## Killed false positives

These looked like antics and were cut. The cut is the point: funny does
not equal agent.

- **A human git mishap, not an agent antic.** A Morrowind mod PR body
  says "I accidentally deleted the wrong branch on my repo and it
  closed the PR." Verbatim, but the author is type User and the body
  holds zero markers of any kind. An ordinary human git error. Cut
  outright.
- **Checklist paperwork, not a self-approval.** A bank-assistant PR body
  records a "Review report (separate Claude session)" marked
  `approved`. That is a task checklist referencing a file, not evidence
  an agent approved or merged its own GitHub PR. No GitHub approval
  event exists. Cut.
- **A force-push story with no agent in it.** A launcher PR body says an
  earlier PR "was accidentally auto-merged ... due to an unrelated
  force-push incident." All six fetched comments are human review talk.
  No bot, no marker. Cut.
- **A bot failure notice, not an antic.** A Cursor Bugbot comment says
  "Bugbot couldn't run - usage limit reached." A bot failing to run is
  not a behavior family in this collection. Cut.
- **Same Codex-spam family, no punchline.** Another PR shows Codex
  review triggers with no limit or failure message at the end. Without
  the punchline, it is not a best-of entry. Cut.
- **The scanner's own first two hits, not re-listed.** The prcomment
  scanner's hit 1 was fixture-quoted text misread as a live injection
  (FALSE POSITIVE). Hit 2 was INCONCLUSIVE (see
  `data/lanes/github-pr-comments/chase-2026-10-24.md`). Neither is
  presented here as a confirmed antic.

## How this was found

Five bounded search lanes ran against the unauthenticated GitHub Search
API on 2026-10-24, 50 API calls total, no rate-limit blocks. The first
three lanes taught an important lesson: the search API matches PR titles
and bodies, not comment text, so behavior-first queries surface PRs
*about* a topic rather than comments *exhibiting* it. Lanes B and C
returned zero citable candidates for that reason. The last two lanes
inverted the path: seed from PRs whose bodies already carry Cursor,
Claude, or Codex markers, then read their comment threads. That is
where the confirmed entries came from.

An adversarial reviewer then checked every surviving candidate against
its cached bytes: excerpts verified verbatim, grades held to the
definitions above, one duplicate entry merged (the two paddock comments),
one entry cut outright, and one entry demoted in ranking (the
east-bay-mobility deletion is confirmed agent authorship but an intended
correction, not a blunder). Provenance files and sha256 hashes were
recomputed and match.

Evidence: `data/lanes/github-pr-comments/raw/bestof-20261024/` (lanes a,
d, e hold the cited captures; lanes b and c hold honest nulls).
