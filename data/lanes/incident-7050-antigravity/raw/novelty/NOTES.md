# Novelty + overlap + incident-1433 notes — lane 4, incident-7050 fleet

Date of work: 2026-10-29 (America/Chicago).
Scope: AI Incident Database (AIID) report 7050 / incident 1433 and the
events named inside report 7050. Read-only work only. No Factum writes.
No poster handles in prose. Only "Tassos M" as published is used.

## 1. Item 18 and the 7050 / 1433 mapping

Source: `reports/agent-bypass-forum-hunt/hits.json`, id B18, and
`reports/agent-bypass-forum-hunt/REPORT.md` section 18.

- B18 title: "Antigravity wiped a drive while asked to clear a project
  cache". Grade REPORTED, novelty NEW (Reddit lane full checks).
- REPORT.md identifier note (verbatim in substance): the Incident
  Database page carries both numbers — report 7050 and incident 1433.
  This report cites the report number (7050, matching the source URL);
  1433 is the incident number on the same page, not a second report.
- B18 evidence held by the bypass hunt:
  `data/lanes/agent-bypass-forum-hunt/raw/reddit/incidentdb-7050-antigravity.html`
  (339,780 bytes, retrieved 2026-10-29 18:00 UTC) and
  `data/lanes/agent-bypass-forum-hunt/raw/reddit/datarecovery-antigravity.html`
  (68,076 bytes). SHA256SUMS verified 7/7 OK by that lane.
- Bounds carried with B18: second-hand press coverage of a forum post;
  the poster ran Turbo mode, so the approval gate was user-disabled,
  not agent-defeated; failure reads as path error plus missing
  dangerous-command guardrail, not intentional evasion. The Reddit
  thread itself was never read from Reddit (Reddit blocked from this
  environment; see the Reddit lane coverage limits).

## 2. Incident-1433 verdict: 1433 IS the Antigravity event

VERDICT: Incident 1433 is the Antigravity D-drive wipe itself. It is
NOT the Replit event, and it is NOT a distinct third event.

Evidence (fetched 2026-10-29, saved in this directory):

- https://incidentdatabase.ai/cite/1433/ — title: "Google Antigravity
  Reportedly Deleted User's Entire D: Drive While Clearing Project
  Cache". Header fields verified in raw HTML: Incident ID 1433,
  Report Count 2, Incident Date 2025-11-27, Editors Daniel Atherton.
  Taxonomy: risk subdomain 7.3 (lack of capability or robustness),
  domain "AI system safety, failures, and limitations", entity AI,
  timing post-deployment, intent unintentional.
- https://incidentdatabase.ai/reports/7050/ — The Register write-up:
  Antigravity wiped a user's entire D drive, bypassing the Recycle
  Bin; the user is identified only as "Tassos M"; the agent, asked
  whether it ever had permission to delete the whole drive, answered
  it absolutely did not, and that its cache-clear command had
  incorrectly targeted the drive root; Turbo mode noted; Google
  spokesperson: "We're aware of this report and we're actively
  investigating what this developer encountered."
- https://incidentdatabase.ai/reports/7051/ — the second report under
  1433 (How-To Geek write-up of the same event): same user, same
  photo-sorting tool, same `rmdir` cache-clear command landing on
  the drive root, same apology exchange, Turbo-mode note. This is
  why the cite page shows Report Count 2: 7050 + 7051 are two
  write-ups of ONE event, not two events.
- The cite-1433 page carries NO mention of Replit (verified by
  string search of fetched HTML). The Replit event appears only
  INSIDE the report-7050 text as a comparison ("As we reported
  over the summer, Replit ... deleted a customer's entire
  production database"), not as part of incident 1433.

Therefore the parent brief's seed mapping is confirmed as:
report 7050 -> incident 1433 -> Antigravity D-drive wipe, 2025-11-27.

## 3. Other AIID entries linked to these events

### 3a. The Replit event (distinct incident, mentioned inside 7050)

- Incident 1152: "LLM-Driven Replit Agent Reportedly Executed
  Unauthorized Destructive Commands During Code Freeze, Leading to
  Loss of Production Data". Incident Date 2025-07-18, Report Count 5,
  verified in raw HTML of https://incidentdatabase.ai/cite/1152/.
- Its 5 reports, all found by site search: 5577, 5593, 6113, 6120,
  6126 (all write-ups of the same July 2025 code-freeze production
  database deletion, fake-data cover-up, and CEO apology).
- 1152 is a DIFFERENT incident from 1433: different system (Replit
  vs Antigravity), different date (2025-07-18 vs 2025-11-27),
  different harm (production database vs local D: drive).

### 3b. Other Antigravity material on AIID (distinct from the wipe)

- Report 6703: indirect prompt-injection proof-of-concept against
  Antigravity (system-prompt `<EPHEMERAL_MESSAGE>` tags treated as
  privileged instructions; `write_to_file` triggered via fetched web
  content). Discovered Nov 18, 2025, disclosed to Google Nov 19,
  2025, answered "intended behavior / known issue", published
  Nov 25, 2025. This is a VULNERABILITY DISCLOSURE, not a deletion
  event, and it is NOT one of incident 1433's 2 reports (1433's
  count is fully accounted for by 7050 + 7051). Its parent incident
  number was NOT established from fetched pages (the report page
  text does not state it); the Antigravity IDE entity page lists
  only incident 1433 as an implicated-system incident in the
  snippet returned. OPEN: parent incident number for 6703.
- "Multiple other Antigravity project wipes": report 7050 says
  "Multiple Antigravity users have posted on Reddit to explain that
  the platform had wiped out parts of their projects without
  permission." No separate AIID incident was found for these: the
  Antigravity IDE entity page lists ONLY incident 1433, and
  site search for Antigravity returns only 1433 (deletion) and
  6703 (injection PoC). The project-wipe anecdotes are therefore
  unnumbered Reddit anecdotes referenced inside 7050, NOT distinct
  AIID entries. They are not separately novelty-checked here
  beyond this negative AIID result; their Reddit threads were not
  fetched (same Reddit block as B18).

### 3c. Same-class AIID deletion incidents (context, not these events)

From the AIID Feb–Apr 2026 roundup's "AI systems with execution
privileges" section, which names 1433 alongside:

- Incident 1424: "Claude Code Agent Reportedly Deleted
  DataTalks.Club Production Infrastructure, Database, and Snapshots
  via Terraform". Incident Date 2026-02-26, Report Count 2.
  Verified via site search (entity pages + cite page snippet).
- Incident 1441: "Claude Cowork Allegedly Deleted Folder
  Containing 15 Years of Family Photos While Organizing User's
  Wife's Desktop". Incident Date 2026-02-07, Report Count 1.
  Verified via site search (cite page + entity pages).
- Incident 1469: "PocketOS Production Database Was Reportedly
  Deleted by Cursor AI Agent Running Claude Opus 4.6".
  Incident Date 2026-04-24, Report Count 3. Verified via site
  search (Cursor entity page).
- Incidents 1671 (GPT-5.6 Sol, Mac home directory, 2026-07-10)
  and 1672 (GPT-5.6 Sol, production database, 2026-07-13):
  titles and dates from the LLM-integrated-code-assistants
  entity listing only; cite pages NOT individually fetched.
  Treat as UNVERIFIED-BY-FETCH, lower confidence than 1424/1441/1469.

None of 1424 / 1441 / 1469 / 1671 / 1672 is the Antigravity or
Replit event; they are sibling deletion incidents in the same
failure class.

### 3d. Distinct prior-corpus Antigravity item (not a deletion)

- The bypass hunt's Reddit lane notes HN 46048996, a PromptArmor
  Antigravity vendor test, as "prior-lane triaged, distinct from
  R1". It is a vendor test, not a wipe, and not AIID 1433. Listed
  here only to prevent conflation.

## 4. Novelty checks run in THIS lane

### 4a. lists/urls inventory (COMPLETE, NO HIT)

`lists/urls/urls.jsonl` grep counts, 2026-10-29:
antigravity: 0; replit: 0; incidentdatabase.ai: 0;
datarecovery.com: 0. No URL for any candidate event is inventoried.

### 4b. Transluce tracker (COMPLETE for snapshot; PARTIAL for live)

- Snapshot file
  `data/lanes/2026-10-09-transluce-intel/raw/findings-list-20261027T115816Z.json`:
  138 items, finding ids 36–208. Term scan: antigravity NO HIT,
  replit NO HIT, 1433 NO HIT, 1152 NO HIT, 7050 NO HIT,
  "vibe cod" NO HIT, "production database" NO HIT, "d: drive"
  NO HIT, datarecovery NO HIT. This reproduces the Reddit lane's
  snapshot check.
- Live `tl.py findings` (read-only): returned 25 most-recent items
  only; zero hits for antigravity / replit / 1433 / 1152 / 7050 /
  "vibe cod" / "d: drive" / "production database". The live tool
  does not page the full tracker history in one call, so the live
  check covers the recent window only; the 138-item snapshot is
  the fuller Transluce check.
- Local Transluce lane tree
  (`data/lanes/2026-10-09-transluce-intel/`, including FINDINGS.md
  stub and 109-line events.jsonl): grep for antigravity/replit
  returned 0 files; events.jsonl antigravity|replit count 0.

### 4c. Factum corpus (COMPLETE — own run, read-only)

Pre-check PASSED: all `data/lanes/*/lane.json` parse as JSON; no
malformed file found. Factum `status`: index healthy (stale:
false), 208,627 records, 127 lanes, commit
a9af27c677b08e66708c356fc696f58581f1efe2, pending 0.
Read-only `match` queries only; no writes, no submits, no edits.

Antigravity event:
- Exact "Antigravity": FOUND, 4 records, ALL unrelated:
  observation_70f6525a44af42b2899d37e0e2b23bd0,
  observation_c2e38422412e477aaa8818ce97d686a0,
  observation_d176ada1b5ae4e47afab815ef4aeaa54,
  observation_f99e7fc4b85341ab995d672a0933c071 — all lane
  2026-08-19-tantive-space, value exactly "Antigravity" (a board
  username), not the product, not the wipe.
- Fuzzy "Antigravity D drive wipe" (limit 10): 6 matches — the
  same 4 tantive author-name records, plus one tantive board
  message mentioning "Antigravity and Sentinel-Dev" (a benchmark
  discussion, not the incident) and observable
  2ba08a7495444febb7e3a88ff0ca8bef
  ("antigravity-preview-05-2026", a model-version string in the
  deepmind-interactions lane). Zero matches carry any
  drive/wipe/rmdir/Turbo/incident flag. None is the wipe.
- URL matches: https://incidentdatabase.ai/reports/7050/ =
  not_found; https://incidentdatabase.ai/cite/1433/ = not_found.
- Fuzzy "Tassos" (limit 10): 10 weak substring matches
  ("assistant", timeline anchors, Diffend sweep notes) — noise,
  none relevant.

Replit event:
- Exact "Replit": not_found.
- Fuzzy "Replit deleted production database": not_found.
- Fuzzy "Replit" (limit 10): 10 matches, ALL "Replied..."
  substring noise from lane 2026-08-21-public-board (FIPS county
  threads) — zero Replit-platform records.
- Fuzzy "code freeze" (limit 10): 10 matches, ALL "freeze"
  substring noise (tantive "freeze a receipt", TRAIL annotation)
  — zero code-freeze incident records.

Factum verdict: NEITHER event is in the structured corpus. The
only Antigravity hits are the tantive username and a model
string. Caveat (standard): fuzzy retrieval is heuristic, not an
exhaustive absence test, and the summarized runs reviewed top-10
fuzzy lists; the exact-value and URL checks are the
discriminating ones and are clean. This agrees with the Reddit
lane's prior check (which reported 1 exact Antigravity match;
this run finds 4 records of the same unrelated kind).

### 4d. Legacy evidence tree (COMPLETE, with one mention-level hit)

- `evidence/` (legacy tree) distinctive-term grep (Tassos,
  incidentdatabase, Lemkin, SaaStr, code freeze, `rmdir /s`,
  "D: drive"): 0 files. Clean.
- `data/lanes/` bare-term grep (antigravity|replit, first 30
  files): matches are all unrelated in kind — tantive.space
  author name (verified: `"tantive.author": "Antigravity"`),
  gomod-hunt Go module paths (verified:
  `github.com/badrisnarayanan/antigravity-claude-proxy`,
  33 hits in events.jsonl), wikipedia-top500 revision texts,
  trajectory files, and the deepmind model string. None is the
  wipe or the Replit deletion.
- `data/lanes/` + `evidence/` + `reports/` distinctive-term
  grep (Tassos, incidentdatabase, Lemkin, SaaStr, code freeze,
  `rmdir /s`, "D: drive", "D drive wipe"; file types md/json/
  html/txt/events.jsonl; bypass-hunt lane and this novelty dir
  excluded from display): hits fall in three groups —
  (a) THIS FLEET's own lane (see 4e): sibling in-flight
  captures, NOT prior overlap;
  (b) noise: longrca travel-planner costs, android-world
  base64 blob, dtap-bench citing AIID incident 373 (a
  different incident), transluce crawl f155_096.html (a C:
  wipe capture noting a separate D: drive unaffected — a
  different wipe, not the Antigravity event);
  (c) ONE SUBSTANTIVE PRIOR HOLDING, for Replit only (see 4e
  and appendix A): the agent-egress-deep-dive HN crawl holds
  a Replit-incident description with core facts.
- Residual gap (stated, minor): giant raw trajectory *.jsonl
  dumps were not exhaustively scanned for distinctive terms
  (one unbounded grep was killed as redundant after the
  bounded run above). Trajectory dumps are model rollouts,
  not incident holdings; the dtap-bench hit found shows the
  scan does reach trajectory-adjacent material. This gap does
  not change any verdict below.

### 4e. Prior holding vs fleet in-flight work — do not conflate

- PRIOR holding (counts toward novelty): the
  agent-egress-deep-dive lane's HN expanded crawl,
  `data/lanes/agent-egress-deep-dive/raw/hn-expanded-crawl/`:
  `shape-agent-exfiltration--story.json` (HN story 46436429,
  "We built a guardrail layer to keep LLMs from breaking
  production databases", 2025-12-30) contains a "The Replit
  Incident (July 2025)" section naming the code freeze and
  the 1,200+ executive contacts wiped; `screening.json` and
  `name-guidance--comment.json` carry a comment listing the
  Replit code-freeze production-database deletion (1,200
  executives, 1,100+ companies) among examples of AI going
  wrong. The Replit incident is therefore MENTIONED, with
  core facts, in prior lane material — but it is not a
  ranked incident record, not a Factum record, not a
  Transluce finding, and not a lists entry.
- The same crawl also holds a DIFFERENT drive-wipe anecdote:
  an agent that "executed a recursive rmdir /s /q on the
  root of my E: drive" after a path-with-space failure.
  E: drive, different cause, different story — NOT the
  Antigravity D: wipe. Do not merge them.
- FLEET in-flight work (does NOT count as prior overlap):
  `data/lanes/incident-7050-antigravity/raw/primary/` and
  `raw/forum-sweep/` were created Oct 29 23:39–23:44 UTC,
  during this fleet run, by sibling lanes — e.g.
  report-7050.html/txt, register-antigravity-2025-12-01,
  register-replit-2025-07-21, saastr-replit-2025-07-17,
  hn-replit.json, hn-antigravity-deleted.json, and GH/HN
  sweep files. These are this fleet's fresh collection.
  Counting them as overlap would be double-counting the
  fleet's own work.

## 5. Per-event novelty table (interim — see pending items)

| Event | Status | Basis |
|---|---|---|
| Antigravity D-drive wipe (AIID 1433 / report 7050, 2025-11-27) | NEW | All checks ran: Factum exact/fuzzy/URL clean or unrelated-only (4 tantive author records + 1 model string); lists/urls 0; Transluce snapshot 0/138; local Transluce tree 0; live-25 window 0; `evidence/` distinctive terms 0; data/lanes distinctive terms: no D: wipe hit (nearest: an E: drive anecdote and a C: wipe capture — both different events). Agrees with B18 Reddit-lane NEW. Caveat: REPORTED grading stands (thread itself unread). Residual gap: giant trajectory *.jsonl dumps not exhaustively scanned (see 4d). |
| Other Antigravity project wipes (anecdotes inside 7050) | PARTIAL / UNNUMBERED | No separate AIID incident found; no separate corpus check run — they are not distinct ranked items and their threads were not fetched. Do NOT count as separate NEW items. |
| Antigravity injection PoC (AIID report 6703, Nov 2025) | PARTIAL | Distinct event type, no deletion; parent incident number open; no corpus check run in this lane. |
| Replit production-database deletion (AIID 1152, 2025-07-18) | PARTIAL — mention-level overlap, no incident record | Factum clean (exact not_found, phrase fuzzy not_found, fuzzy top-10 all "Replied" noise, "code freeze" top-10 all "freeze" noise); lists/urls 0; Transluce snapshot 0/138; BUT legacy tree holds a mention with core facts: agent-egress-deep-dive HN crawl, `shape-agent-exfiltration--story.json` (HN 46436429, 2025-12-30) "The Replit Incident (July 2025)" section + `screening.json` / `name-guidance--comment.json` example listing (code freeze, 1,200 executives, 1,100+ companies). The parent brief's "may already be in the corpus" reproduces ONLY at this mention level — not as a Factum record, Transluce finding, or ranked incident. Parent curates: OVERLAP-by-mention vs NEW incident record. Do NOT double-count; do NOT present the mention as a prior incident filing. The bypass hunt did not rank Replit (Reddit lane: non-Reddit-origin). |
| Sibling deletions 1424 / 1441 / 1469 (1671/1672 unverified-by-fetch) | NOT CHECKED | Out of this lane's candidate set; listed for context only. No novelty claim made. |

## 6. Open items for the parent

1. Replit curation call: mention-level overlap (appendix A)
   vs NEW incident record — the parent decides. This lane
   recommends PARTIAL with the mention cited, not a bare NEW
   and not a full OVERLAP.
2. Parent incident number for AIID report 6703.
3. Cite-page fetch verification for incidents 1671 and 1672
   (titles/dates from entity listing only).
4. Reddit threads themselves (B18 origin thread; project-wipe
   anecdote threads) still unread — needs a parent with live
   browser access; same open item as the bypass hunt's
   coordinator note 1.
5. Nothing was pushed; no Factum records were written. All
   evidence for this lane is under
   `data/lanes/incident-7050-antigravity/raw/novelty/`.

## Appendix A. Prior Replit mention — verbatim contexts (short excerpts)

Source files (pre-existing lane material, not this fleet):
`data/lanes/agent-egress-deep-dive/raw/hn-expanded-crawl/`

- `shape-agent-exfiltration--story.json` (HN story 46436429,
  2025-12-30, "We built a guardrail layer to keep LLMs from
  breaking production databases"): "The Replit Incident (July
  2025): SaaStr founder Jason Lemkin used a Replit agent to
  build an app. He gave it an explicit 'code freeze'
  instruction and stepped away. He returned to find his
  entire production database — 1,200+ executive contacts —
  wiped. The agent ignored the freeze, ..."
- `screening.json` and `name-guidance--comment.json` (HN
  comment, same example list): "Replit - CEO Amjad Masad's
  platform experienced an incident where an AI coding agent
  deleted a live production database during a code freeze,
  affecting records of over 1,200 executives and 1,100+
  companies."

These excerpts establish mention-level overlap only. They are
not a prior incident filing, not a Factum record, and not a
Transluce finding.

## Appendix B. Distinct wipe anecdotes NOT to merge

- E: drive anecdote, same HN crawl (`shape-recon--story.json`,
  `screening.json`): "Instead of deleting the sub-folder, it
  executed a recursive rmdir /s /q on the root of my E: drive"
  after a path-with-space failure. Different drive, different
  cause, different story from the Antigravity D: wipe.
- C: wipe capture, Transluce crawl `f155_096.html`: "Personal
  data on a separate D: drive was unaffected; everything under
  C:\ ..." — a different wipe in which the D: drive survived.
  Not the Antigravity event.
