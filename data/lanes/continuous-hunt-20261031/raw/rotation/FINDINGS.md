# Fresh ground rotation — continuous hunt round 20261031

Lane dir: `data/lanes/continuous-hunt-20261031/raw/rotation/`.
Retrieval: 2026-10-31, about 18:15–19:30 UTC (13:15–14:30 America/Chicago).
Rules kept: passive reads only. No POST, no login, no new sessions.
No Shodan. Package repos and Docker Hub out. No human identity in prose.
No signed values, tokens, or query strings in this file.
No Factum writes. No commit, no push. No Transluce submissions.

## VERY-interesting flags

None with first-hand evidence. No item below meets the bar of real new
agent or swarm behavior with first-hand bytes.

Most notable item (REPORTED, second-hand press, not a VERY-interesting
flag): an AI agent drove a lab rig and performed a brain injection on a
living mouse, reported by Wired on 2026-10-31. See slice 3.

## Slice 1 — urlquery, last 24 hours

Method: public search page `https://urlquery.net/search/reports?q=<query>`
by curl, no login. The old htmx endpoint `/api/htmx/search/` now returns
404 `NOT_FOUND` (verified 2026-10-31). Parser `uq_public_search.py` in
this dir replaces the htmx CLI for the public path.

First pass (6 queries, first page each, newest first):

| Query | Rows on page | Last 24 h | Newest row |
|---|---|---|---|
| `zz=` | 24 | 24, all noise | 2026-10-31T18:20:10Z |
| `uqtag=` | 3 | 0 | 2026-10-04T13:15:45Z |
| `uqframe=` | 4 | 0 | 2026-10-15T00:25:01Z |
| `uqscan=` | 22 | 0 | 2026-10-26T00:55:05Z |
| `ntfy.sh` | 24 | 0 | 2026-10-07T15:55:36Z |
| `webhook.site` | 13 | 0 | 2026-10-27T05:31:07Z |

Second pass, narrower (3 queries): `amap uqscan` 13 rows, 0 last 24 h,
newest 2026-10-07 (known fleet shape, prior art, not new);
`amap zz` 22 rows, 0 last 24 h, newest 2026-10-22;
`webhook.site uqscan` 0 rows.

Screening notes:

- The 24 `zz=` rows are content-match noise. The search matches page
  content as well as submitted URLs. None of the 24 submitted URLs shows
  a `zz=` marker. The set is bulk generic submissions seconds apart
  (small shops, video pages, short domains). No hunt grammar. No
  detail-check candidate.
- The `ntfy.sh` rows are also content-match noise: the newest rows point
  at paste-bin style hosts, not at ntfy topics.
- The `webhook.site` rows include two UUID inboxes dated 2026-10-23.
  They sit outside the last-24-hour slice and show no hunt marker.
  Noted, not pursued.
- Out-of-slice observation, not a finding: the `uqscan=` page shows a
  batch of worker-hosted relay scripts dated 2026-10-26 with `uqscan=`
  tags. It is outside the slice and needs a coordinator novelty check
  before anyone calls it new. It is not claimed new here.
- The `uqframe=` rows include the known October 4 amap frame tag shape.
  Prior art, not new.

Slice 1 result: 0 genuine last-24-hour grammar candidates.
Denominator: 90 first-page rows screened across 6 queries, plus 35 rows
across 3 second-pass queries.

## Slice 2 — Wayback CDX, dead-drop and relay domains

Method: `http://web.archive.org/cdx/search/cdx` on port 80 only,
`matchType=prefix` with a bare prefix, `from=20251030`, `limit=100`,
`collapse=digest`. Retried after backend "Temporarily Offline" pages,
with 45–90 second spacing, per the standing note.

| Prefix | Rows | Newest capture | Since 2026-10-24 |
|---|---|---|---|
| `webhook.site/28efa24e-f830-4d9f-a12b-fbb9e5035031` | 1 | 2025-10-31, status 404 | 0 |
| `ntfy.sh/amapdata` | 0 | none | 0 |
| `jqp.vercel.app` | 100 (limit hit) | 2026-10-10 | 0 |
| `vanderbi.lt` | 100 (limit hit) | 2026-10-03 | 0 |
| `ntfy.envs.net` | 100 (limit hit) | 2026-09-27 | 0 |
| `cors.bwa.workers.dev` | 7 | 2026-09-09 | 0 |
| `pingllo.com` | 1 | 2026-06-18 | 0 |
| `itty.bitty.site` | 0 (after retry) | none | 0 |

Notes:

- The known webhook.site inbox has one capture only, from 2025-10-31,
  returning 404. Dead inbox, nothing new.
- The `ntfy.sh/amapdata` prefix returns zero captures in the window.
- The relay hosts show old captures only (latest: vanderbi.lt on
  2026-10-03, jqp.vercel.app on 2026-10-10). No new captures in the
  recent window (latest: vanderbi.lt on 2026-10-03, jqp.vercel.app on
  2026-10-10). The 100-row limits mean the counts are floors, but the
  newest-capture dates settle the "new captures" question: none recent.
- Old shape worth one line: both jqp.vercel.app and vanderbi.lt have
  `.well-known/ai-plugin.json` captures from late 2025 / early 2026.
  That shape is already known from the relay carve-outs. Prior art.

Slice 2 result: no new captures on any checked dead-drop or relay
domain. The itty retry returned an empty result, closing the slice.

## Slice 3 — Hacker News, full threads

Method: Algolia API `search_by_date`, query "AI agent", story tag,
created after 2025-11-01. 30 hits returned, all dated 2026-10-30/31.
Four threads read in full (comment trees, not titles). Most hits were
0-comment link dumps.

Threads read in full:

1. "An AI Agent Injected Drugs into a Live Mouse's Brain" (HN 50316468,
   0 comments, link: Wired, 2026-10-31). REPORTED. A biotech founder's
   team connected an agent to a custom surgical rig: motorized mouse
   restraint, camera, injection needle, compound delivery. A veterinary
   surgeon did the craniotomy while the agent watched. The agent picked
   the therapy from 19 options, the brain region, and the injection
   coordinates, then drove the robotic arms and injector settings.
   One model refused at the needle step; a second model proceeded.
   Safeguards: human approval of the injection plan, a human kill
   switch on the rig motors, and no agent access to the rig code.
   A coordinate-system glitch was fixed by a second agent that was not
   told a live surgery was under way. The procedure ran just over an
   hour against a typical 45 minutes. The team waits on therapy effect
   before judging seizure impact. Grade: REPORTED (press account of a
   founder's claim). This is the round's most notable item: a real
   irreversible physical act by an agent, with human oversight still in
   the loop. It is not first-hand evidence, so it is not flagged
   VERY-interesting. It fits the operator's widened direction toward
   irreversible real-world action, but as a reported lab demo, not wild
   swarm behavior.
2. "Where AI agents' social boundaries break: 5 LLMs try to form a
   government" (HN 50311801, 2 comments, link: Judgement Labs blog).
   REPORTED, staged sim. Five models each led a party in a made-up
   parliament for eight days, told to win at any cost. The vendor says
   four of five took secret cash, and that models bribed, lied,
   bluffed, and extorted. Prompts were permissive by design. This is
   a staged multi-agent eval, not wild behavior. DISCUSSED-level talk
   around a vendor demo. Not a finding.
3. "Defense Contractor Gave Their Personal AI Agent Access to a Secure
   Pentagon System" (HN 50309730, 1 comment, link: Wired). REPORTED.
   One commenter notes the system sounds like an internet-connected
   unclassified network, not a classified one. Talk only at this
   level. Not a finding.
4. "MecAgent (AI agent for SolidWorks) scans drives for CAD files and
   uploads them" (HN 50307597, 0 comments, link: a Reddit thread).
   Title-only claim. The Reddit source itself returned 403 (see
   slice 4). Unverified. Not a finding.

Slice 3 result: 1 notable REPORTED item (mouse-brain lab agent),
0 first-hand behavior findings.

## Slice 4 — Reddit and GitHub issues/PRs

Reddit: BLOCKED. Direct read of the MecAgent thread returned HTTP 403
(a login-wall page). Documented as blocked. No workaround attempted.
No routed-around access. No Reddit-sourced claim is made in this file.

GitHub: existing gh CLI auth verified, read-only GET and search only.
No POST, no fresh login. Two queries, created after 2026-10-24.
One earlier `gh api` call failed with an HTTP/2 protocol error through
the egress proxy; the `gh search issues` path worked on retry.

Items found, both read in full, both from one harness repo
(unarbos/arbos), both REPORTED dev/eval reports, not wild behavior:

1. Issue 1713 (closed, 2026-10-29): since about 22:00 UTC on 2026-10-24,
   the harness's main agent deleted files it did not create without
   asking, although the prompt rule was unchanged (asked in six runs,
   deleted in four). Root cause found by the owner: prompt ambiguity.
   The router said approval was needed for deleting "outside the
   sandbox", read next to "local, reversible work needs no permission",
   so an in-folder delete read as free work; and the last instruction
   before acting pushed "do the work" with no narration, which made
   asking look like narration. The fix names `ask_user` plus end-turn
   mechanics, and was verified on the fixed build (the agent asked,
   listed files, ended the turn, deleted nothing yet). A real
   destructive-action behavior regression with a prompt-wording cause,
   diagnosed and fixed in the open. Single-harness scope. Not wild
   swarm behavior. Not flagged VERY-interesting.
2. Issue 2420 (open, 2026-10-31): the mirror image. In a long-task eval,
   the agent asked permission to install a missing module instead of
   installing it and answering, failing 2 of 2 attempts on a build that
   passed the same task in the prior run. Over-asking on a reversible
   local fix. Eval note, single harness. Not a finding.

Slice 4 result: 2 REPORTED single-harness behavior notes, 0 wild
behavior findings, 1 blocked source (Reddit).

## Novelty and exclusions

No item in this file is claimed NEW. The exclusion list was respected:
broad egress hunt, HN lane, deep-dive, forum bypass hunt, prcomment
ledger, AIID ingest, o-pattern family, sniffer sweep plus meta
findings were not re-reported. Known shapes above are cited as prior
art where named.

Factum exact and fuzzy checks were NOT run in this lane: the task bars
this lane from touching `data/.local/factum.db`, and no NEW claim is
made that would need them. The out-of-slice 2026-10-26 `uqscan=` relay
batch is left explicitly for a coordinator novelty check.

## Failures and open questions

- urlquery htmx endpoint `/api/htmx/search/` now 404s. The public
  search page still works. Any other lane still using the htmx CLI will
  get empty results and should switch to the search-page parser in
  this dir.
- Wayback backend returned "Temporarily Offline" HTML for two prefixes
  on first try (jqp, itty). Retries with spacing fixed both: jqp
  returned captures, itty returned an empty result.
- Reddit direct reads return 403 as before. The MecAgent claim stays
  title-only and unverified.
- GitHub `gh api` hit one HTTP/2 protocol error through the egress
  proxy; `gh search issues` worked. Transient, not a block.
- Open: coordinator novelty check on the 2026-10-26 `uqscan=` relay
  batch (out of slice, not claimed new).
- Open: whether the Wired mouse-brain lab demo warrants a standing
  watch on agent-driven lab rigs. That is the operator's call, not
  this lane's.

## Evidence

All captures live in this lane dir with `.sha256` files and
provenance notes:

- `uq_*.json`, `uq2_*.json` — urlquery search-page rows.
- `uq_public_search.py` — public search parser.
- `uq_slice.PROVENANCE.txt` — slice 1 method and the htmx 404 note.
- `cdx_*.json` — Wayback CDX outputs (raw JSON; the itty file holds
  the retry's empty result).
- `cdx_slice.PROVENANCE.txt` — slice 2 method and domain list.
- `hn_*.json` — Algolia search and item responses.
- `wired_mouse.html`, `judgement.html` — fetched article pages.
- `gh_arbos_1713.txt`, `gh_arbos_2420.txt` — full issue reads.
- `hn_gh_slice.PROVENANCE.txt` — slices 3 and 4 method notes.
