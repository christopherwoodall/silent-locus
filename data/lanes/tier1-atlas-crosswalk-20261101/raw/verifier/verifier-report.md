# Verifier report — tier1-atlas-crosswalk-20261101

Role: verifier. This lane checks the swarm claims against the files.
Method: fresh reads of the capture files. No lane summary was trusted.
Live check: one passive GET only, for the crosswalk agents file.
No POST. No sign-in. No sign-up. No session. No account.
No human name is in this file. No signed value is in this file.
No token is in this file. No query string is in this file.
Style: short sentences, simple words. Terms are defined on first use.

Terms used here, defined on first use:
- **Capture**: a file saved from a public page.
- **Hash**: a short code made from file bytes. Same bytes give same hash.
- **Board**: a public message place where agents post and read.
- **llms.txt**: a short text file a site publishes for agents.
- **PASS**: the claim holds in the bytes.
- **FAIL**: the claim does not hold in the bytes.
- **INCONCLUSIVE**: the bytes cannot settle the claim yet.

## Overall verdict: SHIP-WITH-FIXES

All counts, hashes, and file sets check out, with two wording updates.
The coordinator must apply the 8 adversarial downgrades, with the
two updates in section 7 below. Nothing in this report blocks the
ingest batch. The batch is sound. The wording is what needs care.

## 1. Crosswalk seed file — PASS

Claim: the agents file is 6,052 bytes live, with a stated hash.
Live re-check by passive GET on 2026-11-01: HTTP 200, 6,052 bytes.
Live hash matches the seed hash exactly.
The seed file on disk matches the live bytes exactly. No change.
The ingest copy of this file also matches the same hash exactly.
The crosswalk directory file with the agents name is the same
6,052-byte text, not an HTML page. Its name says homepage, but
its bytes are the agents text. The coordinator should note this
name quirk in the final report so no reader mistakes it for a
home page capture.

## 2. Crosswalk board captures — PASS

Claim: the board captures exist, with hashes, and hold the quotes.
Full hash check of the crosswalk directory: all files pass.
No file fails. The sample files all pass: lobby, changelog,
feedback, sealed-rounds, the MCP OpenAPI file, crosswalks page.
Quoted claims found in the bytes:
- Roll-call thread dated October 30, 2026, in the lobby file.
- Connection-test posts dated November 1, 2026, in the lobby file.
- Lobby file holds 10 listed posts. This matches the lane count.
- Changelog file holds wake and presence notes. Wake means a task
  wakes an agent. Presence means an online-now mark with a
  five-minute window. A channel plugin polls every half minute.
- Member and post counts in the directory page: lobby 64 posts
  with 1,788 members; feedback 10 posts with 2,087 members;
  deals 598 posts with 26 members. All three match the claim.
- Changelog board: 14 posts with 1,802 members. This also matches
  the lane note and belongs in the mismatch claim.
- Directory totals: 19 boards listed. The 13 full tag lines sum
  to 1,269 posts and 1,143 posts in the last 30 days. The 6 small
  boards add 10 posts and 1 post in the last 30 days. Totals are
  1,279 posts and 1,144 in the last 30 days. This matches the
  lane claim exactly.
- MCP OpenAPI file holds 11 tool paths: read, open, post, tune,
  crosswalks, mail, account, help, remove, tasks, files.
- Sealed-rounds page: agents answer blind. Answers stay sealed
  until all are in. Then all open at once. This matches the claim.
- The site agents guide (14,163 bytes) and the MCP root GET file
  share one hash. They are the same bytes. This matches the
  adversarial note. The 6,052-byte agents file is distinct.

## 3. Atlas captures — PASS, with one correction to carry forward

Claim set: shared names, flatboard total, switchboard and colony
recency, agent-x run reports.
- Atlas directory: 74 capture files. Every per-file hash sidecar
  passes. Zero fail. Note: the atlas directory has no single
  aggregate hash file. It has one hash file per capture. That is
  enough, and all 74 pass.
- carvideoai on 5 surfaces, name only: wire feed, sssnack feed,
  hotline page, agora activity, adam-message posts. All 5 hold
  the name. No key binds them. Name match only. PASS.
- skitter on 4 surfaces, name only: wire feed (25 hits), hotline
  top-writer line (1 hit), wide census post (1 hit), fork-zone
  home page (10 hits). The fork-zone front-page index file holds
  zero hits. The home page is the correct fourth source, not the
  index. The adversarial fix text still names 3 verified surfaces.
  The coordinator must update it to 4, with the home page cited.
  Name match only. No key binds them. PASS with that update.
- Agent-x home page holds full post bodies, not excerpts only.
  It holds 8 SIGKILL hits and race-guard run reports. One post
  reports a SIGKILL orphan at a replace boundary. One post
  reports a race guard that tripped mid-run and re-armed. One
  post gives a fix for the orphan case. The explore file holds
  excerpts only, with zero SIGKILL hits. The gift-exchange
  thread shows 11 replies in 24 hours and 4 participants in the
  explore file. The home page is the correct source for run
  reports. The adversarial fix text for claim 6 says no run
  report is in the capture. That is true for the explore file
  only. It is now out of date for the home page file. PASS with
  the citation update in section 7.
- Flatboard: the page file states total 2,426 messages, page 1
  of 49, newest post dated 2026-11-01T15:21Z. PASS.
- Switchboard rooms file: crypto room 2,320 messages, last
  activity 2026-11-01T15:51:20Z. PASS.
- Colony feed file: 50 items, freshest item dated
  Sun, 01 Nov 2026 15:52:10 UTC. PASS.
- Agent-x explore counts: reliability 60 posts in 24 hours,
  agent-practice 25 posts in 24 hours. Both match the lane claim.
  PASS.

## 4. Linguist counts — PASS, with one gap in method detail

Claim: 81 atlas bins on disk. Split: 54 real, 19 error, 5 thin,
2 non-board, 1 maintenance.
- Disk holds 81 atlas bins. PASS.
- Split sum: 54 + 19 + 5 + 2 + 1 = 81. PASS.
- Total bytes: 801,873. This matches the cryptologist total.
- Spot checks: church, wide, cantina, and continental files are
  real guide texts. The 4claw file is a 404 error page. The
  moltstack and clawcaster files are title only, which fits the
  thin class. The gnamiblast file says it is offline for nightly
  maintenance, which fits the maintenance class.
- Gap: the linguist files do not name which file falls in which
  class. A full recount from the notes alone is not possible.
  The split is sound by sum and by sample, but the per-file class
  list is missing. The coordinator should ask for that list, or
  mark the split as sample-checked, not fully recountable.
  This is a method note, not a FAIL. No number was wrong.

## 5. Cryptologist counts and secret hygiene — PASS

Claim: 51 Markdown or text, 22 HTML, 5 JSON, 3 other, of 81 bins.
No token, key, or signed value is reproduced.
- Independent recount by first byte gives the same split exactly:
  51 files start with a Markdown heading mark, 22 start with a
  markup tag, 5 start with a JSON brace, 3 start with plain text.
  Sum is 81. PASS.
- The 3 plain-text files are the short 404 line, a plain guide
  opening, and a plain title line. This fits the other class.
- Secret hygiene: the cryptologist Markdown files hold zero long
  token-like strings of 40 or more characters. The JSON file holds
  22 long strings, and all 22 are 64-character hex hashes of file
  content. None is a credential. Cross-file matches use 16-hex
  fingerprints only. Parameter names appear without values.
  No signed value is reproduced. PASS.
- Note: the cryptologist scope note says the brief said 52
  captures but disk holds 81. That is correct. All counts in the
  final report must name which set they count: 52 boards, or
  81 bins. The adversarial review makes the same point.

## 6. Ingest batch — PASS

Claim: batch exists, 351 records, 117 of each kind, all tagged
with the lane name. Four repeat hosts are tagged repeat, not new.
117 blob paths exist.
- Batch directory exists. Records file holds 351 lines.
- Split: 117 artifact, 117 source, 117 observation. PASS.
- Lane tag: 351 of 351 records carry the lane tag with the exact
  swarm lane name. Zero records lack it. PASS.
- Capture status: 339 records first-byte-capture, 12 records
  repeat-byte-capture. 12 = 4 files times 3 record kinds. PASS.
- Repeat files, all 3 kinds tagged repeat: agent-commons-algo
  llms file, relay-russian-agent-board llms file, swarmmemo llms
  file, the-colony llms file. None of these 4 files appears in
  the first-byte set. None is tagged new. PASS.
- Blob paths file: 118 lines = 1 comment header + 117 paths.
  All 117 paths exist on disk. PASS.
- File type counts in the ingest directory: 53 llms files, 29
  skill files, 10 SKILL files, 12 sitemap files, 9 feed files,
  2 atom files, 1 rss file, 1 MCP JSON file. Sum is 117. PASS.
- Byte check: 50 of the 52 atlas llms files match the slot-0
  bins byte for byte. The 2 changed files are austinsdomain
  and voicescape, as the ingest lane states. The crosswalk llms
  file matches the seed hash. So 51 live files match prior bytes
  and 2 changed. This matches the ingest lane claim. PASS.
- Observation type: every observation is a web capture. PASS.
- This verifier did not edit any record. No hand edit was made.

## 7. Adversarial fixes the coordinator must still apply

The adversarial review judges 11 claims: 0 killed, 8 downgraded,
3 standing. The coordinator must apply all 8 downgrade wordings
in the final report. The 8 are:
1. Crosswalk lobby as a live agent board: use the weaker text.
   Self-declared posts only. Roll call October 30, 2026.
   Connection tests November 1, 2026. Full bodies not seen.
   Poster identity unverified.
2. Crosswalk recruits agents through agents: use the weaker text.
   The site instructs agents to self-sign up. No join from that
   line was observed. Sign-up needs a code sent by email.
3. Crosswalk wake and presence machinery as live: use the weaker
   text. A changelog post dated October 31, 2026, announces the
   features. No wake event, presence card, or poll was observed.
4. Atlas shared-agent links: use the name-only text. No link
   proves same actor. All links are name matches only.
5. Agent-x script-sharing thread: use the weaker text, with the
   citation update below. The explore file holds excerpts only.
6. Wide census: use the contested-report text. The swarm did not
   verify the walk. The same feed holds a key-mark claim and a
   linked cross-board reply claim. Both are unverified board text.
7. Member and post count mismatches: use the weaker text. The
   counts are observed. Auto-membership and house posting are
   unproven explanations, not findings.
8. MCP as a common surface: split the claim. Crosswalk documents
   11 MCP tools, behavior untested. The 30-of-52 endpoint count
   needs a per-board list or a downgrade to named-in-guides.

Two updates to the adversarial fix texts, from this verification:
- Update A (claim 5 in the list above, shared-agent links):
  skitter now has 4 verified surfaces, not 3. The fourth is the
  fork-zone home page, not the front-page index. The index still
  holds zero hits. Cite the home page file for the fourth leg.
  Keep the name-only grade. No actor link is proven.
- Update B (claim 6 in the list above, agent-x thread): the home
  page file holds full post bodies with SIGKILL and race-guard
  run reports and a fix post. Cite the home page file for run
  reports. Keep the explore file at excerpt level only. Do not
  claim pasted scripts were run from the explore file alone.

One more note on fix 8: this verifier counts 32 of 52 atlas llms
files that mention MCP, and 31 that match a loose endpoint
pattern. That is close to 30, but the pattern is loose, and no
per-board list is in the final report yet. The coordinator must
either publish the per-board list with a stated rule for what
counts as endpoint documentation, or use the downgraded text.
Mention alone is not endpoint documentation. The adversarial
note that the ingest directory held only 10 llms files is now
out of date: it holds 53 llms files. The list can now be built
from those files.

Standing claims, no change needed: sealed rounds as a blind
primitive; linguist weirdness findings; cryptologist nulls.

## 8. Count reconciliation — PASS

- Targets: 53 = 1 crosswalk + 52 atlas boards. PASS.
- Atlas boards: 59 HTTP 200 minus 6 HTML fallbacks minus 1
  generic guide = 52. Probe file holds 82 rows: 59 status 200,
  22 status 404, 1 transport fail. PASS.
- The 6 HTML fallbacks are all status 200 rows whose bins start
  with a markup tag: ai-village, chirper, clawcaster, devaintart,
  gnamiblast, public-agent-lounge. PASS.
- The 1 generic guide is inwith-ai, a crawler guide, not a board
  guide. PASS.
- Trajectory-domains rows: 48 new audit rows found 2026-11-01,
  plus 1 crosswalk row found 2026-11-01, = 49 rows found that day.
  Plus 6 rows found 2026-10-31 that carry the same date label,
  = 55 lines that match a date grep. The 6 are hosts outside the
  52-board set. They do not break the count. PASS.
- Watch gap: 4 hosts lack an exact llms row: agent-commons-algo,
  relay-russian-agent-board, swarmmemo, the-colony. Each has an
  older row that names a different surface. The coordinator or
  list owner must add the exact llms rows, or confirm the
  baseline alone is enough. This gap is real and already stated
  in the ingest lane. It is not a verifier FAIL. It is an open
  task for the coordinator.
- Slot-0 baseline: 114 targets plus 53 additions = 167 targets.
  This matches the ingest lane note. PASS.

## Gaps and open questions

- Per-file linguist class list is missing. The split is checked
  by sum and by sample, not by full recount.
- Per-board MCP endpoint list is missing. The 30-of-52 count is
  close to this verifier's loose count, but not proven by a list.
- The 4-host watch gap needs a list-owner decision: add exact
  llms rows, or confirm the baseline is enough.
- The crosswalk agents file name quirk needs a note: the file
  named as a home page holds the agents text bytes.
- No live behavior was tested: no MCP call, no wake event, no
  sealed round run, no key check. The final report must keep
  docs-level claims at docs level.
- The batch and lane files sit uncommitted on disk, as ordered.
  This verifier did not commit and did not push.

## Files checked

- Crosswalk directory hash file and all captures in it.
- Atlas directory per-file hash files and all 74 captures.
- Slot-0 probe file and all 81 atlas bins.
- Linguist notes, excerpts, and progress files.
- Cryptologist analysis, matches, inventory, script, and JSON.
- Adversarial review and behavioral analysis.
- Ingest directory: all 117 files, blob paths file, progress file.
- Factum batch directory: records file and manifest.
- Live crosswalk agents file by passive GET.
