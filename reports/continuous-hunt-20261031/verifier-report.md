# VERIFIER REPORT — continuous hunt round 20261031

Role: independent re-verification only. No commit, no push, no Factum
write, no other worker's files touched. Passive GET only, paced, no
POST, no login, no new sessions, no Shodan. Package repos and Docker
Hub out. No human poster handle appears in this report. No signed
value, token, or query string appears in this report.

Method: every citation below was re-checked by my own re-fetch or by
my own re-derivation from the lane's capture bytes. A lane summary
was never counted as verification. Working notes and the full
re-fetch log live in
`data/lanes/continuous-hunt-20261031/raw/verifier/` (script
`refetch.py`, log `refetch.log`).

## Verdict: SHIP-WITH-FIXES

The round's central claims verify: no VERY-interesting flag in any
lane, no standalone agent committer anywhere, and every count I
re-derived from captures matches except the small wording/count
items in §5. Ship after the §5 fixes are applied. None of the fixes
requires a new data run.

## 1. Live re-fetch results (per citation)

PASS means the live bytes match the lane's claim (status, identity,
and content class). Small byte drift on live dynamic pages is noted,
not counted as failure, because the lane claims a snapshot at fetch
time, not frozen bytes.

### Surfaces lane — 23 live fetches, 23 PASS

| Citation | Live result |
|---|---|
| swarmbar homepage, llms.txt, skill.md, stats endpoint, tabs page | 200; llms/skill/stats bytes identical to captures; homepage +157 bytes vs capture, tabs −2 bytes (live drift only); stats values identical (30 agents, 4 humans, 10 agents active in 7 days, 0 humans active), only the timestamp moved |
| swarmbar mcp.json | 404 with site page body, 13,416 bytes, identical to capture |
| agentboard homepage, llms.txt, feed | 200; llms/feed bytes identical; homepage −8 bytes (live drift only) |
| agentboard threads sitemap, agents sitemap | 200; bytes identical to captures (15,716 and 15,021) |
| agentdm homepage, llms.txt, well-known doc | 200; all bytes identical to captures |
| fallback homepage, llms.txt, feed | 200; all bytes identical to captures |
| agentbadge homepage, llms.txt, skill.md, agent-card doc, heartbeat doc | 200; all bytes identical to captures |
| agentbadge mcp.json (from capture, 95 bytes) | 404 body shape confirmed in capture; not separately re-fetched live (same endpoint class as the other 404s above) |

### Rotation lane — HN, press, issues

| Citation | Live result |
|---|---|
| HN thread, mouse-brain lab agent | PASS: title and 0 comments match; linked press article live 200 |
| HN thread, multi-model government sim | PASS: title and 2 comments match; linked blog live 200 (small body, JS shell — liveness and link verified, article body text not re-verified) |
| HN thread, defense-contractor agent access | PASS: title and 1 comment match |
| HN thread, CAD-file scanning agent | PASS: title and 0 comments match |
| Issue 1713, single harness repo | PASS: state closed, title matches capture |
| Issue 2420, same repo | PASS: state open, title matches capture |
| Wayback CDX, dead-drop prefix | INCONCLUSIVE, not FAIL: live CDX backend returned its known "Temporarily Offline" page at re-check time. The lane's CDX capture itself is internally consistent (see §3). Retry later if a live CDX confirmation is required. |

### Phrases lane — HN items and issues

| Citation | Live result |
|---|---|
| HN comment, subagent-to-IRC anecdote | PASS: live comment text matches capture |
| HN comment, model spawning a subagent on its own initiative | PASS: live comment text matches capture |
| HN comments, agent-spam flood discussion (2 items) | PASS: live comment texts match captures |
| HN comment, agent owning a crypto wallet experiment | PASS: live comment text matches capture |
| HN story, agent message board discovery | PASS: title and 1,603 comments match |
| Issue 1108, subagent_spawned bug report | PASS: state open, title matches capture (first attempt 404 was my script building a doubled URL from the capture's API-URL repo field, not a lane error; corrected re-fetch passed) |
| Issue 242, live agent-to-agent experiment | PASS: state open, title matches capture |
| Issue 78, visitor-log filing | PASS: state open, title matches capture |

### Committer and unmeasured lanes — spot commits

| Citation | Live result |
|---|---|
| Committer lane, first Codex-lane commit | PASS: author type User, committer web-flow, footer present |
| Committer lane, first Gemini-lane commit | PASS: author type User, committer web-flow, footer present |
| Unmeasured lane, first Codex-lane commit | PASS: same commit as the committer lane's first Codex row (see §5, fix 3 — the lanes overlap) |

Live totals: 43 PASS, 0 FAIL, 1 INCONCLUSIVE (CDX backend offline).

## 2. Hash verification

Checked every sidecar in four lanes. The phrases lane has none (see §5).

| Lane | Sidecars checked | Passed | Failed |
|---|---|---|---|
| surfaces | 43 | 43 | 0 |
| committer | 20 | 20 | 0 |
| rotation | 28 | 28 | 0 |
| unmeasured | 48 | 48 | 0 |
| phrases | 0 (no sidecar files exist) | — | — |
| **Total** | **139** | **139** | **0** |

Files without sidecars in the four hashed lanes are docs, scripts,
run logs, and (rotation only) nine empty error-log files — no
capture bytes lack a sidecar there. The phrases lane is the
exception: all 82 of its files, including every sweep and issue
capture, lack sidecars, even though its FINDINGS claims sidecars
exist. Hash verification for that lane was therefore impossible.

## 3. Count re-derivations (my own, from capture bytes)

### Surfaces — all match

- Byte sizes for every claimed file match captures exactly
  (homepages, llms.txt files, feeds, sitemaps, agent-card doc,
  heartbeat doc).
- Feed entry counts: 50 and 50 for the two boards; latest feed
  dates match claims (agentboard 2026-10-31, fallback 2026-10-28).
- Sitemap URL counts: 153 thread URLs, 155 agent-profile URLs.
- Stats endpoint bytes: values match claim exactly.
- Skill doc is byte-identical to the skills-path copy (same hash).
- Agent-card version 0.16.0 confirmed in capture bytes.
- Fallback header shows 24 registered speakers, confirmed.
- Latest tab timestamp 2026-10-30T18:34 confirmed in tabs bytes.
- All eight claimed 404s confirmed by provenance status plus body
  inspection (site pages for two boards, tiny not-found bodies
  for the other two).
- MISMATCH (wording, §5 fix 1): sitemap lastmod ranges.

### Committer — all match except one count (§5 fix 2)

- 210 commit rows: author Bot 8, author User 202, committer Bot 0,
  committer web-flow 207 (177 of 180 footer-lane rows plus 30 of
  30 in the corrected Copilot lane). Distinct authors and distinct
  commits per lane match the table.
- Footer presence in message bytes: Codex 30/30, Cursor 30/30,
  Jules 30/30, Aider 29/30, Codex-named 30/30, Gemini literal
  "Co-Authored-By: Gemini" 12/30.
- Jules bot-footer lines: 508 lines containing the token, exact.
- Gemini bot-author rows: 5 rows, 4 distinct bot accounts, all
  web-flow committed, all carrying `is_bot: false` alongside type
  Bot — the reported API quirk is real.
- PR lanes: 30 rows each, Bot author 1 each, distinct authors 28
  each; title/body match split 6/5/8 and harness-title 14 match.
- Corrected Copilot lane: 30 rows, Bot author 1, web-flow 30/30,
  copilot-swe-agent footer on 2 rows. The rejected qualifier-only
  query file is 0 bytes, as claimed.

### Rotation — all match

- Urlquery first-pass row counts: 24, 3, 4, 22, 24, 13; second pass:
  13, 22, 0. Newest row dates match the table for every query.
- The 24 newest-grammar rows are all dated 2026-10-31 and none of
  their submitted URLs carries the searched marker — the
  content-match noise claim holds.
- CDX data rows (excluding the header row): 1, 0, 100, 100, 100,
  7, 1, 0 across the eight prefixes; newest capture dates match
  the table (dead-drop inbox 2025-10-31 status 404; relay hosts
  newest 2026-10-10 and 2026-10-03; nothing recent).
- HN search capture: 30 hits. Full-thread comment counts match:
  0, 2, 1, 0 for the four threads read.

### Phrases — all match

- All 10 phrase-table rows match the lane's summary and the
  per-phrase capture files exactly (token counts, saved counts,
  exact counts on all three sources, including the 5 urlquery
  honest zeros and the subagent_spawned case where saved rows
  (200) exceed the token estimate (169)).
- Ranked-instance files match their prose: the IRC anecdote, the
  own-initiative delegation anecdote, the wallet experiment, the
  visitor-log filing, and the Matrix experiment issue are all
  present in the cited captures.

### Unmeasured — all match

- Codex lane: 30 rows, User 30/30, footer 30/30, single repo,
  single author, single committer.
- PR lanes: 30 rows each, Bot author 1 each, in-window 29/30 and
  30/30, title/body splits as in §3 committer row above.
- All 20 phrase rows: row counts, in-window counts, repo counts,
  and bot-author counts match the table exactly (including the
  under-limit returns 11, 8, 14 and the phrase-20 honest null on
  both issue and code surfaces). Spot title-match checks match:
  phrase 1: 0, phrase 3: 3, phrase 4: 17, phrase 7: 1,
  phrase 8: 30, phrase 13: 26, phrase 14: 6, phrase 16: 21.

## 4. Claims confirmed

- No VERY-interesting flag is supported by any lane, and none is
  claimed. The strongest items (the reported lab-demo press item,
  the visitor-log filing, the self-named agent bot row) are all
  graded below that bar by their own lanes, correctly.
- No standalone agent committer exists in any measured commit
  row: committer Bot 0 in every lane, and every bot-authored row
  is web-flow committed (except 3 User-committed rows in the
  Gemini lane, on User-authored rows).
- Footers prove assisted authorship only, as the lanes state.

## 5. Blocking fixes (apply before ship)

1. **Surfaces sitemap lastmod wording.** "Lastmod values run
   2026-10-27 through 2026-10-31" for the agentboard sitemaps is
   wrong as a full range: the true range is 2026-09-08 through
   2026-10-31 (only 59 of 153 thread URLs and 40 of 155 agent
   URLs are dated 2026-10-27 or later). Correct to the true range
   or to "most recent values run ...". Same treatment for
   fallback ("sitemap lastmod values are 2026-09-29" — true range
   is 2026-09-27 through 2026-10-28, with 40 of 41 entries dated
   2026-09-29 or earlier and one dated 2026-10-28) and agentbadge
   ("sitemap lastmod values are 2026-10-29" — 222 of 229 main
   sitemap entries are that date, but 7 are July 2026).
2. **Committer Gemini bot-footer count.** The lane claims any
   bot-suffixed footer on 9 of 30 rows; message bytes show 11
   rows (10 distinct commits) with a bot-suffixed co-author
   footer. Correct to 11 rows / 10 commits, or state the narrower
   definition used. Related wording fix: in the Codex-openai lane,
   17 rows carry the codex address form and 16 carry the noreply
   form, with 3 rows carrying both — not "the remaining rows"
   carrying the second form. The 30/30 Codex-named footer claim
   itself is correct.
3. **Do not sum committer and unmeasured lanes.** They re-measured
   the same queries: Codex commit URLs overlap 30 of 30, PR
   harness URLs 30 of 30, PR Claude-code URLs 29 of 30. Any
   combined total must count each query once. The committer
   lane's "300 rows with the meta fleet" figure is unaffected
   (it does not include the unmeasured lane), but a round total
   that adds the unmeasured lane's 90 rows would double-count.
4. **Phrases lane provenance gap.** Either generate sidecars for
   the phrases captures now (marked as post-hoc, not original)
   or correct the FINDINGS claim that sidecars exist. Until one
   of those is done, the phrases lane's captures are the only
   ones in the round without hash coverage.

## 6. Not re-verified, and why

- **Urlquery live search.** Not re-run: the rotation slice is
  time-bound (18:20–18:22 UTC), and a re-run now returns a
  different newest page, so it cannot confirm or refute the
  slice. Internal consistency (counts, dates, marker absence)
  was fully verified from captures instead.
- **Wayback CDX live.** One live attempt returned the backend's
  known intermittent offline page (see §1). All CDX claims were
  verified from captures instead.
- **Full GitHub search slices.** Not re-run live: page-1 search
  ranking drifts, and re-running the full query set risks the
  shared search bucket. Captures were fully re-derived, and
  representative commits and issues were live-fetched instead.
- **HN and GitHub token totals.** Algolia estimates and GitHub
  total counts were verified only as recorded in captures; the
  lanes themselves warn these are token estimates, not totals,
  and that warning is correct.
- **Factum checks.** Not re-verified by design: this task bars
  touching the Factum index, and the lanes that ran Factum checks
  (phrases) or deferred them (committer, unmeasured, rotation)
  say so plainly. The phrases lane's reported Factum digest and
  match results are taken as stated, not verified.
- **Reddit thread.** Not re-attempted: the lane documents a 403
  login-wall block with no workaround attempted. Re-attempting
  adds nothing, and the lane makes no claim from that source.
- **Surface prose details beyond liveness.** Room lists, protocol
  descriptions, signup shapes, and cross-links were checked
  only where they appear in fetched bytes (stats, feeds,
  sitemaps, docs); token-gated rooms and private-message
  surfaces were not read, per the lanes' own limits.
- **PR discriminator.** The unmeasured lane's own caveat stands:
  staged PR rows carry no pull-request discriminator field, so
  PR status rests on the query qualifier, not on a staged field.
  This was not independently resolved.
