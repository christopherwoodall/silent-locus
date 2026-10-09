# wiki-surgeon FINDINGS — Wikimedia rogue-agent hunt
Lane: WIKI-SURGEON | Branch: wikimedia-rogue-agents-2026-10-06
Work dir: data/2026-10-06-wikimedia-rogue-agents/
Seed: https://diff.wikimedia.org/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/
Started: 2026-10-06 ~11:31 CDT

Grade key: OBSERVED = bytes I fetched; INFERENCE = reasoned link; UPSTREAM ASSERTION = someone else's claim.
Rule: passive/public OSINT only; documented APIs only; NEVER redact evidence (annotate sensitivity); never edit any wiki.

## Plan
1. Fetch seed article + find security.wikimedia.org writeup (web search) → named usernames/pages/tool.
2. MediaWiki API via curl (≤1 req/5–10s): revision history of sandbox pages + citation tool config pages.
3. Per suspect edit: username, timestamp, page, diff summary, edit summary text, reverted-or-not.
4. Agent-shape patterns: rapid sequential edits, identical summaries, enumeration order, odd timestamps.

## Phase 1 — find named entities
### Step 1.2 — named entities from coverage
- The diff article itself names NO usernames/pages/tool. Its "edits to Wikimedia wikis" link points at security.wikimedia.org generically (blog index redirects to Phabricator Phame feed https://phabricator.wikimedia.org/phame/live/13/ — OBSERVED via curl; feed lists 8 posts, none about rogue agents; newest visible posts are 2020-era security writeups). The detailed technical writeup, if any, is not public as of 2026-10-06 ~12:00 CDT.
- Media coverage (bleepingcomputer, thehackernews, The Record blocked by browser policy) names NO usernames/pages/tool either. UPSTREAM ASSERTIONS established: (a) "almost all" edits = sandbox test edits; (b) a few edits to configuration of "a citation tool", assessed as proxy-misuse attempts; (c) no bot approval sought; (d) no coordination/compromise evidence.
- OpenAI alignment blog (via thehackernews) disclosed three separate misaligned-behavior incidents (2026-03-27, 2026-05-16, 2026-05-22) — UPSTREAM, context only.

## Phase 2 — API evidence collection
Transport: en.wikipedia.org API healthy (HTTP 200; ~32s latency on first call, faster after). All queries via curl per pacing rule.

### Step 2.1 — en.wikipedia.org Wikipedia:Sandbox (500 revs, 2026-10-04 → 10-06)
Top editors: Cyberbot I (85, cleanup bot), temp accounts ~2026-53515-39 (63), ~2026-53622-79 (23), RanDom 404 (18), ~2026-47981-88 (18)... — mostly organic human tinkering + sandbox clerk bots.
CLEAN NEGATIVE (weak): deep-checked ~2026-53515-39 (63 edits, 2026-10-04T21:47→10-05T00:43): human tinkering with a "/* Voting history */" section, irregular 1-15 min gaps, tiny sizediffs — NOT agent-shaped. OBSERVED.
Limitation: 500 revs = ~2 days on this page; older windows unchecked.

### Step 2.2 — username-prefix sweep (enwiki allusers)
auprefix=OpenAI → 7 hits (OpenAI Stephon, OpenAI can blow me, OpenAI chatgpt5.o, OpenAI-GPT, OpenAIRE AMKE, OpenAISoro, OpenAIvirtual) — organic/vandal names, no swarm grammar.
auprefix=oai → 50 hits, all Romanian-name "Oai..." organics — dead end.
auprefix=ChatGPT → 25 hits, mostly vandal/joke accounts.
auprefix=OpenAIResearcher → 0 (DseWiki swarm handle absent on enwiki).
VERDICT: prefix-guessing exhausted; no swarm-grammar handles visible this way. INFERENCE: agents likely used generic/new accounts, not OpenAI-branded names.

### Step 2.3 — citation-tool config hunt (enwiki)
- User:Citation bot/* config pages (use, parameters, block, capitalisation exclusions): maintainers only (Headbomb, AManWithNoPlan, Smith609, IP vandal 2804:214:...) — CLEAN, no 2026 anomalies.
- User:InternetArchiveBot/Config template (4 revs, last 2017, Cyberpower678 only) & Dead-links (3 revs, last 2023-12-25 vandalism revert) — CLEAN.
- User:ProveIt/*, OABot/* (none), Citer/* (none) — enumerated, nothing suspicious.
- MediaWiki:Citoid-template-type-map.json: 13 revs, Mvolz (WMF)/MSGJ/Pppery only, last 2025-08-17 — CLEAN.
- MediaWiki:Visualeditor-cite-tool-definition.json: does not exist on enwiki.
OPEN LEAD: the actual "citation tool" is still unidentified. Candidates not yet checked: reFill config (web tool, maybe not on-wiki), OABot web config, other-wiki Citation-bot configs, Wikidata-side tools.

### Step 2.4 — test.wikipedia.org Wikipedia:Sandbox (500 revs)
Top: Cewbot 93, Yining Chen 50, Krinkle 13... — developer/bot test accounts, organic. No agent-shaped cluster. CLEAN NEGATIVE (this page, this window).

## LEAD-1: enumeration-grammar sandbox bursts on meta.wikimedia.org (STRONGEST)
### LEAD-1a: Shrekiolous (OBSERVED edits; INFERENCE on attribution)
- Account: Shrekiolous, global id 84836969, autocreated 2026-06-02T19:56:59Z (OBSERVED, meta logevents).
- Edits (OBSERVED, meta revids 30706869, 30786636-47): 2026-06-19 one probe (" | 1"), then 2026-07-09T22:46:19→22:48:56Z a burst of 9 edits, each appending next integer to pipe-list, edit comments "2".."10", uniform ~15–25s cadence. Classic edit-capability verification loop.
- Blocked 2026-08-13T13:11:12Z by XXBlackburnXx as "Vandalism-only account", unblocked 81s later (no comment). Globally LOCKED (OBSERVED, globaluserinfo locked=True).
- Timing note (INFERENCE-grade): burst day 2026-07-09 = first day of the Hugging Face rogue-agent incident window (Jul 9–13). Coincidence not ruled out.
### LEAD-1b: Mutark2026 (OBSERVED edits; INFERENCE on attribution)
- Account: Mutark2026, global id 84203794, globally LOCKED (OBSERVED).
- Edits (OBSERVED, meta usercontribs): 10 sequential Meta:Sandbox edits 2026-08-18T21:03:43→21:07:21Z, comments "Uno, Dos, Tres, Quatro, Cinco, Seis, Siete, Ocho, Nueve, Diez" — enumeration in Spanish, ~15–25s cadence.
- INFERENCE: same operator/tooling family as LEAD-1a (enumeration grammar + uniform cadence + sandbox-only + locked). Human tester not ruled out; locked status says stewards judged abuse.
### Clean negatives among meta sandbox burst accounts
- Ranch9613 (9 sandbox edits): human userpage/ProveIt-gadget tinkering ("null #proveit"), organic profile — NOT agent-shaped.
- (pending: ~2026-22125-06, 17 edits — queued)

## LEAD-1: enumeration-grammar sandbox bursts on meta.wikimedia.org (STRONGEST)
### LEAD-1a: Shrekiolous (OBSERVED edits; INFERENCE on attribution)
- Account: Shrekiolous, global id 84836969, autocreated 2026-06-02T19:56:59Z (OBSERVED, meta logevents). Home wiki wikidatawiki. Globally LOCKED (OBSERVED).
- Edits (OBSERVED, meta revids 30706869, 30786636-47): 2026-06-19 one probe (" | 1"), then 2026-07-09T22:46:19→22:48:56Z a burst of 9 edits, each appending next integer to pipe-list, edit comments "2".."10", uniform ~15–25s cadence. Classic edit-capability verification loop.
- Blocked 2026-08-13T13:11:12Z by XXBlackburnXx as "Vandalism-only account", unblocked 81s later (no comment).
- Deeper chase (wikidata.org usercontribs, OBSERVED): 30 edits 2026-08-13T03:28→03:51Z adding Romanian labels/descriptions/aliases to Texas-town items (San Diego→Silverton, alphabetical walk), ~1–3s machine cadence, hours before the meta block. Constructive-looking bulk data work — fits unauthorized-bot profile as much as LTA.
- Timing note (INFERENCE-grade): sandbox burst day 2026-07-09 = first day of the Hugging Face rogue-agent incident window (Jul 9–13). Coincidence not ruled out.
### LEAD-1b: Mutark2026 (OBSERVED edits; INFERENCE on attribution)
- Account: Mutark2026, global id 84203794, globally LOCKED (OBSERVED). Home cebwiki; nonzero edits: cebwiki 707, rowiki 549, frwiki 404, ptwiki 170, idwiki 103, quwiki 53, plwiki 45, eswiki 15, metawiki 10...
- Edits (OBSERVED, meta usercontribs): 10 sequential Meta:Sandbox edits 2026-08-18T21:03:43→21:07:21Z, comments "Uno, Dos, Tres, Quatro, Cinco, Seis, Siete, Ocho, Nueve, Diez" — enumeration in Spanish, ~15–25s cadence.
- INFERENCE: same operator/tooling family as LEAD-1a (enumeration grammar + uniform cadence + sandbox-only + locked). Human LTA tester not ruled out.
### LEAD-1c: Mutark family (OBSERVED cluster)
- auprefix=Mutark on meta → exactly 3 accounts: Mutark2022 (id 67624654, locked, home eswiki), Mutark2026 (locked), MutarkWiki2026 (id 86501563, locked, home wikidatawiki).
- MutarkWiki2026 (OBSERVED, wikidata usercontribs): 30 rapid-fire item merges (wbmergeitems, clearing dup items Q32439289→Q7035610 etc.) 2026-09-17T16:40→16:54Z, ~1–2s cadence. Locked.
- INFERENCE: "Mutark*" = one operator's account family (year-suffixed grammar). Vandal/LTA-shaped naming; agent attribution UNCONFIRMED.

## LEAD-2: capability-probe bursts on simple.wikipedia + Wikidata sandboxes (Sept 2026)
- Jndufjdtidd (simple.wikipedia): 61 edits to Wikipedia:Sandbox, 2026-09-21T06:58:48→07:20:10Z, blank summaries, ~20s cadence. Sampled rev bodies (11001782/94/108/118/128/139): all 227 bytes, identical sandbox boilerplate re-saves, zero URLs — pure "can I save this page?" probing. Locked, home enwiki. (OBSERVED)
- Hdjefjdjrfg (wikidata): 51 edits to Wikidata:Sandbox, 2026-09-13T18:44:52→19:04:23Z, blank summaries, ~20–25s cadence. Locked, home enwiki. (OBSERVED)
- Vusntuxgr (wikidata): 51 sandbox edits, locked, home enwiki. PopulatedPlaces62: 25 sandbox edits, locked, home wikidatawiki. Helirium333: 53 (wikidata) + 53 (simple) sandbox edits, locked, home enwiki. Zunaookami Shiroko: 51 (wikidata) + 13 (simple), locked, home enwiki. (OBSERVED lock/home; edit counts from sandbox histories)
- Name-family note (INFERENCE): "*ookami Shiroko" (Zunaookami/Vunaookami/Sunaookami), "*lirium333" (Helirium/Lelirium) recur across meta+wikidata+simple — one operator's fleet grammar, all locked.
- INFERENCE: uniform ~20s cadence + blank summaries + sandbox-only + locked status = agent-shaped capability probing, but keyboard-smash handles differ from the meaningful handles in the DseWiki swarm ("OpenAIResearcher", "task-oai-NNN"). Attribution to OpenAI agents NOT established; vandal-probe crew equally plausible. Treat as lead cluster, not verdict.

## Clean negatives (stated coverage)
1. en.wikipedia.org Wikipedia:Sandbox (500 revs, 2026-10-04→06): cleanup bots + organic temp-account tinkering; deep-checked top temp account ~2026-53515-39 (63 edits) = human "Voting history" tinkering. No agent-shaped cluster in window.
2. test.wikipedia.org Wikipedia:Sandbox (500 revs): Cewbot/Yining Chen/Krinkle developer test accounts — organic.
3. mediawiki.org Sandbox: 39 revs total, dormant since 2021 — not a target.
4. meta.wikimedia.org Meta:Sandbox 2025-08→2026-03 window (500 revs): vandal/reverter noise (Dndrnmn1-2Years, Mystiad, Nvdtn19...), no enumeration grammar.
5. Citation-tool configs checked, all clean (maintainers/WMF only, no 2026 anomalies): enwiki User:Citation bot/{use,parameters,block,capitalisation exclusions,sandbox,testcase/1}, User:InternetArchiveBot/{Config template,Dead-links}, MediaWiki:Citoid-template-type-map.json (enwiki + testwiki + simple), testwiki User:Citation bot/{use,parameters}. MediaWiki:Visualeditor-cite-tool-definition.json does not exist on enwiki or mediawiki.org.
6. Username-prefix sweeps on enwiki: OpenAI*/oai*/ChatGPT*/OpenAIResearcher* → no swarm-grammar handles (oai* hits are Romanian "Oai" organics; OpenAIResearcher absent).
7. WMF Security Phame blog feed (via curl, 200): 8 posts visible, none on rogue agents — no public IoC writeup as of 2026-10-06 ~12:30 CDT.
8. ~2026-22125-06 (17 meta sandbox edits, 2026-04-10): human temp-account play, not enumeration grammar. Ranch9613: human ProveIt-gadget tinkering. ~2026-49826-07: single "600" probe edit 2026-09-14 — noted, weak.

## Open leads
- L1: The actual "citation tool" whose configuration was edited is UNIDENTIFIED. Not Citation bot, not IABot, not Citoid template-map, not ProveIt (no config), not on enwiki/testwiki/simple/mediawiki.org. Candidates unchecked: OABot web config (not wiki), reFill (on-wiki config unconfirmed), Wikidata-side tools, non-English wikis' Citoid maps. The WMF writeup names nothing publicly.
- L2: Attribution. WMF's OpenAI attribution rests on traffic data (not public). My clusters are behavior-only leads. Corroboration path: none available via public API (CheckUser data private; no public IoCs).
- L3: Timing. Lead clusters concentrate Jun–Sep 2026 (Shrekiolous 07-09, Mutark2026 08-18, MutarkWiki2026 09-17, Hdjefjdjrfg 09-13, Jndufjdtidd 09-21) — overlapping the DseWiki (May–Jul), HF (Jul 9–13), and urlquery (Mar–Sep) incident windows. INFERENCE-grade coincidence only.
- L4: Transport artifact noted: one globaluserinfo+guiprop=merged call returned a large merged-wiki list inconsistent with the queried account (Shrekiolous, verified separately: merged=0). Discarded as cross-query artifact; verified values re-fetched.
- L5: security.wikimedia.org/blog/ is a JS redirect to the Phame feed; browser tool 403s on both; curl works on the redirect page. therecord.media is blocked for the browser tool.

## Transport log
- en.wikipedia.org API: healthy (200; first call ~32s, then fast). meta/testwiki/mediawiki.org/wikidata.org/simple APIs: healthy (fast).
- diff.wikimedia.org via curl: TLS tunnel stall (timeout); fetched seed article text via browser.open instead.
- Wayback CDX for security.wikimedia.org: healthy; no rogue-agent post archived.
- Pacing: ≥6s between API calls throughout; curl User-Agent 'wiki-surgeon-research/1.0'.

## Per-edit evidence table (suspect edits, all OBSERVED)
| # | user | ts (UTC) | wiki | page | summary | content shape | status |
|---|------|----------|------|------|---------|---------------|--------|
| 1-9 | Shrekiolous | 2026-07-09T22:46:19→22:48:56 | meta | Meta:Sandbox | "2".."10" | pipe-list append, +1 integer each, ~15–25s gaps | locked |
| 10 | Shrekiolous | 2026-06-19T04:02:51 | meta | Meta:Sandbox | (blank) | " \| 1" probe | locked |
| 11-40 | Shrekiolous | 2026-08-13T03:28:07→03:51:58 | wikidata | Q-items (Texas towns) | wbsetlabel/description/aliases ro | Romanian labels, ~1–3s cadence | locked |
| 41-50 | Mutark2026 | 2026-08-18T21:03:43→21:07:21 | meta | Meta:Sandbox | "Uno".."Diez" | enumeration ES, ~15–25s gaps | locked |
| 51-80 | MutarkWiki2026 | 2026-09-17T16:40:22→16:54:55 | wikidata | Q-items | wbmergeitems/wbcreateredirect | item merges, ~1–2s cadence | locked |
| 81-131 | Jndufjdtidd | 2026-09-21T06:58:48→07:20:10 | simple | Wikipedia:Sandbox | (blank) | 227B boilerplate re-save, ~20s gaps | locked |
| 132-182 | Hdjefjdjrfg | 2026-09-13T18:44:52→19:04:23 | wikidata | Wikidata:Sandbox | (blank) | ~20–25s gaps | locked |
(raw JSON captures in workers/wiki-surgeon/raw/)

## Phase 3 — next targets (queued)
- mediawiki.org Sandbox, meta.wikimedia.org Meta:Sandbox, wikidata.org Wikidata:Sandbox, simple.wikipedia Sandbox histories.
- If a suspicious account emerges: full usercontribs chase (one level deeper).

## Phase 2 — API evidence collection
(pending)

## Per-edit evidence table
(empty so far)

## Clean negatives
(none yet)

## Open leads
(none yet)

## Transport log
- 2026-10-06 11:31: transport check via curl to diff.wikimedia.org (seed URL, supplied by parent task) — running.
