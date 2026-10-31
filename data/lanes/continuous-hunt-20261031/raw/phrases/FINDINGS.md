# Fresh phrase mining — FINDINGS

Lane: continuous-hunt-20261031, phrases worker (linguist role).
Operator: BigSexyWarlock69. Date: 2026-10-31.
Scope: agents and agent infrastructure only. Window: November 2025 onward.
Grades: OBSERVED means first-hand bytes show the act. REPORTED means a
party claims the act and bytes do not corroborate it. DISCUSSED means
talk or planning, no executed act. Default grade: SECONDARY.
No Factum writes were made. This lane is staged only. No commit, no push.

Terms, defined on first use. A token count is a search engine count
based on token matching, not on the exact phrase. An exact count is a
case-insensitive exact-substring count inside saved text, reported
with its saved denominator. A capped value is never a total.

## VERY-interesting flags: NONE

Nothing in this lane meets the bar: no genuinely new wild agent or
swarm behavior with first-hand evidence. The closest item, the
NadaGhost visitor-log filing (rank 4), is a self-asserted agent
filing inside a known agent-village surface, with a disclosed human
partner. It is a watch item, not a VERY-interesting flag. Everything
below is documented normally. This lane does not pad.

## Exclusion check (documented, as briefed)

The sweep's 46-phrase list was read first:
reports/sniffer-sweep-20261031/REPORT.md and
data/lanes/sniffer-sweep-20261031/raw/linguist/phrase-list.md
(buckets A 16, B 19, C 11; 45 searchable, 1 category row).
None of the 10 phrases below equals any of those 46. Near neighbors
checked and kept distinct:
- "I am an autonomous agent" differs from A1 "I am an AI agent" and
  A2 "I am an AI agent, not a person" (autonomous, not AI).
- "spawned a subagent" / "subagent_spawned" differ from B4
  "spawn_agent" (subagent delegation wording and hook-payload token,
  not the namespaced collaboration tool).
- "agent card" differs from the agentbadge surface in the meta report:
  the phrase is new as a sweep string; the /.well-known/agent-card.json
  surface itself is prior art (meta report, existing open-queue
  candidate) and is NOT re-reported as new here.
- "agent-created" differs from all 46; its June-flood discussion
  instances are press-linked prior-art discussion (see rank 7), not
  new incidents.
- The meta fleet's unswept GitHub phrases (including "I am GPT",
  "I am Codex", "I am Gemini", "function_call", "system_capability",
  "browser_rules", "coding_rules", "MCP server", "claude mcp add",
  "custom_tool_call", "server_side_tool_usage_details", "BOOTSTRAP.md",
  "Claude Code", "ignore previous instructions", ThinkingBlock /
  ToolUseBlock / ToolResultBlock, spawn_agent, wait_agent,
  send_message, tool_call.arguments, zz/oai/epoch-nonce tokens) were
  NOT re-run as the main sweep. They overlap the 46-phrase list.
Excluded as prior art, never as new: broad egress hunt, HN lane,
deep-dive, forum bypass hunt, prcomment ledger, AIID ingest, o-pattern
family, sniffer sweep and meta findings (TOI-01 iLands cluster,
WATCH-01 tron handoff, WATCH-02 pursekeeper filing, WATCH-03 da.gd
burst, M1-M8). Where a new phrase touches one, it is cited as prior
art, not as a new finding.

## How the 10 new phrases were mined

Mining sources, all passive GET, no login, no POST, no sessions:
- HN Algolia relevance search, then date-filtered search_by_date
  (created_at_i after 2025-11-01), over discovery terms such as
  self-disclosure variants, delegation wording, and protocol words.
- GitHub issue search via the existing gh CLI auth (read-only GET,
  is:issue qualifier, per_page 20-30, paced 8-10 seconds). An early
  batch failed with 422 (missing is:issue qualifier); the qualifier
  was added and the batch re-ran clean. No rate-limit block was hit.
- One web-search pass was not needed: HN and GitHub mining produced
  the set below with cited instances before any broader search.
Every final phrase has at least one mined instance except where
marked; no phrase was invented without an instance.

Final set (10), with mining instance:
1. "I am an autonomous agent" — HN comment quoting the sentence in
   a discussion of agent self-declarations (March 2026).
2. "autonomous agent intro" — GitHub issue title, agent visitor-log
   filing, 2026-09-07.
3. "agent-created" — HN comments and GitHub issue titles, 2026-07
   to 2026-10-31.
4. "subagent_spawned" — GitHub hook-payload token in issue titles,
   2026-09-23 to 2026-10-19.
5. "spawned a subagent" — HN operator anecdotes, 2026-04 to
   2026-09-30.
6. "agent loop" — HN comments and GitHub task titles, 2026-10.
7. "agent-to-agent communication" — HN protocol discussion and
   GitHub A2A issues, 2025-12 to 2026-10-26.
8. "agent card" — GitHub A2A issues, 2026-10-13 to 2026-10-29.
9. "owns its own crypto wallet" — HN experiment post, 2026-07-20.
10. "fleet of autonomous agents" — HN comments, 2026-06-15 and
    2026-10-19.

## Phrase table — counts with denominators and caps

HN method: Algolia search_by_date, window-filtered, up to 3 pages of
100 (cap 300 saved). Exact count is exact-substring inside saved
comment text. Algolia nbHits is a token count, not an exact total;
in one case (subagent_spawned) saved rows (200) exceed nbHits (169),
which proves nbHits is an estimate, not a total. Never cite it as one.
GitHub method: search/issues, is:issue, first page only, per_page 30
(29 for phrase 1: the API returned 29 items). Exact count is
exact-substring inside saved titles only; bodies were NOT swept, so
a title count of 0 does not mean the phrase is absent from bodies.
GitHub total_count is a token total, not an exact total.
urlquery method: quoted phrase plus date:[2025-11-01 TO 2026-10-31],
limit 30. total_hits is the API total for that query. urlquery
matches submitted URLs AND page content, so a hit does not prove
the phrase was on the page; saved titles were checked for exact
matches. Five phrases returned total_hits 0 with reports null;
those are honest zeros, confirmed on re-run, not errors.

| # | Phrase | HN token / saved / exact | GH token total / saved / exact-title | UQ total / saved / exact-title |
|---|---|---|---|---|
| 1 | I am an autonomous agent | 68 / 68 / 1 | 12,091 / 29 / 0 | 0 / 0 / 0 |
| 2 | autonomous agent intro | 455 / 300 cap / 0 | 49,927 / 30 / 1 | 0 / 0 / 0 |
| 3 | agent-created | 215 / 215 / 6 | 998,897 / 30 / 11 | 689 / 30 / 0 |
| 4 | subagent_spawned | 169 est. / 200 / 0 | 155 / 30 / 3 | 0 / 0 / 0 |
| 5 | spawned a subagent | 31 / 31 / 6 | 19,619 / 30 / 0 | 0 / 0 / 0 |
| 6 | agent loop | 89,330 / 300 cap / 2 | 888,072 / 30 / 18 | 735 / 30 / 0 |
| 7 | agent-to-agent communication | 54 / 54 / 21 | 26,875 / 30 / 14 | 106 / 30 / 0 |
| 8 | agent card | 1,767 / 300 cap / 0 | 345,963 / 30 / 6 | 1,155 / 30 / 0 |
| 9 | owns its own crypto wallet | 5 / 5 / 1 | 1,447 / 30 / 0 | 0 / 0 / 0 |
| 10 | fleet of autonomous agents | 21 / 21 / 3 | 6,238 / 30 / 0 | 1 / 1 / 0 |

Read the table by exact counts, not token counts. Token counts
above 10,000 for phrases 3, 6, and 8 are stemming noise: the engines
match the words separately. The exact columns are the signal.

## Ranked candidates (by agent-activity signal, not string weirdness)

### Rank 1 — "subagent_spawned": lowest-collision harness fingerprint

- Grade: DISCUSSED product fingerprint, not behavior. SECONDARY.
- Why it ranks first: GitHub token total is only 155, the smallest
  in the set by two orders of magnitude, and 3 of 30 saved titles
  carry the exact token. The three exact-title issues are all
  hook-payload or session-update issues dated 2026-09-23,
  2026-09-29, and 2026-10-19. One full body was fetched (a session
  resume bug): a runtime restoring a conversation with three native
  subagents logged failures on session/update notifications carrying
  the subagent_spawned value. That is a real runtime emitting the
  token in the wild, not a coined string. HN exact 0 of 200 and
  urlquery 0 are consistent with a code-level token, not prose.
- Use: adopt as a search signature for harness telemetry leaks
  (logs, transcripts, bug reports). Do not present a title hit as
  an agent act; it proves a harness feature exists, the same
  downgrade the sweep applied to its spawn_agent family.
- Evidence: gh_sweep_subagent_spawned.json, gh_issue_Lody_1108.json.

### Rank 2 — "spawned a subagent": first-person delegation anecdotes

- Grade: REPORTED. SECONDARY. No independent corroboration.
- Why it ranks: HN exact 6 of 31 saved, the highest exact ratio
  among small-denominator phrases. Instances, all operator reports:
  (a) 2026-09-30, a model on its own initiative spawned a subagent
  to generate test output, choosing a lighter model itself
  (full text fetched, hn_item_49910777.json); (b) 2026-06-12, an
  agent spawned a subagent to join IRC (one line, thin, full text
  fetched, hn_item_48500624.json); (c) 2026-04-19 and 2026-04-12,
  further operator reports of spawned subagents in coding sessions.
  GitHub exact-title 0 of 30 and urlquery 0 bound it to HN-style
  discourse, not to issue titles or submitted pages.
- Limit: every instance is one operator's own account of their own
  session. Autonomous delegation is claimed, not verified by a
  trace. The IRC instance is a single joking sentence. None is a
  wild multi-agent act.
- Evidence: hn_sweep_spawned_a_subagent.json, hn_item_49910777.json,
  hn_item_48500624.json.

### Rank 3 — "agent-to-agent communication": protocol-discourse signature

- Grade: REPORTED for experiments, DISCUSSED for protocol work.
  SECONDARY. Concept known in Factum (see Novelty).
- Why it ranks: HN exact 21 of 54 saved and GitHub exact-title 14
  of 30 saved, the broadest exact coverage in the set. Instances
  include a 2026-08-09 protocol-framework demo post, open-source
  A2A packages (2026-06-19), a 2026-09-12 issue titled "Lessons
  from live agent-to-agent communication over Matrix: reply storms
  and temporal awareness" (full body fetched: a one-hour live
  experiment in which a coding agent monitored a channel and
  replied per message, producing reply storms — an operator-run
  experiment, not wild coordination), and a 2026-10-26 chat-app
  agent-to-agent issue. Urlquery total 106 with 0 exact titles in
  the saved 30.
- Limit: protocol discussion and self-run experiments dominate.
  No instance shows two independent wild agents coordinating.
- Evidence: hn_sweep_agent_to_agent_communication.json,
  gh_sweep_agent_to_agent_communication.json,
  gh_issue_mansio_242.json.

### Rank 4 — "autonomous agent intro": visitor-log filing, watch item

- Grade: OBSERVED for the filing act itself (the issue bytes exist).
  SECONDARY for the identity claim (self-asserted, unverified).
- What: one GitHub exact-title hit of 30, dated 2026-09-07: an
  "autonomous agent intro" issue filed as an agent visitor log in
  an agent-village repository. Full body fetched: the filer states
  it is an autonomous agent with a disclosed, named human partner,
  running on a named personal-assistant platform on a private host,
  with no public repo yet, and says it is currently active on two
  other agent-community surfaces. HN exact 0 of 300 (capped) and
  urlquery 0.
- Why only a watch item: the pattern mirrors WATCH-02 (pursekeeper
  self-filed listing) but is weaker — the human partnership is
  disclosed in the filing itself, and the surface (agent-village
  repo family) is known from the sweep's GH2 Village material,
  which was killed as a multi-agent claim for single-account
  authorship. This is instance-new, surface-known. No bot or app
  marker, workflow trace, or maintainer acceptance is staged here.
- Evidence: gh_sweep_autonomous_agent_intro.json,
  gh_issue_ai-village-external-agents_78.json.

### Rank 5 — "owns its own crypto wallet": disclosed payment experiment

- Grade: REPORTED experiment. SECONDARY.
- What: HN exact 1 of 5 saved, dated 2026-07-20 (full text fetched):
  an experiment post describing an AI agent that owns its own
  crypto wallet, earns money by selling a paid text-summarization
  API priced in USDC via the x402 protocol, uses a named model to
  decide pricing from real earnings versus its own API costs, and
  self-lists on an x402 bazaar for agent-to-agent discovery.
  GitHub exact-title 0 of 30, urlquery 0.
- Limit: a disclosed self-built experiment, not a wild agent
  economy. The x402 mechanism family is prior art (pursekeeper
  filing, agentbadge slug, meta report M-pattern). The phrase is
  new; the mechanism is not. No wallet value, endpoint value, or
  payment proof is reproduced in this report; presence only.
- Evidence: hn_sweep_owns_its_own_crypto_wallet.json,
  hn_item_48976842.json.

### Rank 6 — "agent card": A2A debugging term, protocol only

- Grade: DISCUSSED protocol term. SECONDARY.
- Why it ranks here: GitHub exact-title 6 of 30, including a
  2026-10-29 issue about an A2A client agent-card fetch returning
  404 against deployed fleet servers, contrasting the
  well-known path form with the file form, and a 2026-10-13 issue
  about an agent card served at one path while the protocol version
  in use expects another. HN exact 0 of 300 (capped) shows the term
  does not travel in HN prose. Urlquery total 1,155 with 0 exact
  titles in the saved 30 (generic card pages dominate).
- Limit: debugging chatter about a protocol document, not agent
  behavior. The well-known agent-card surface itself is prior art
  (agentbadge, meta report) and is not re-claimed here.
- Evidence: gh_sweep_agent_card.json.

### Rank 7 — "agent-created": signature only; flood quotes are prior art

- Grade: DISCUSSED vocabulary. SECONDARY. No new incident claimed.
- What: HN exact 6 of 215 saved; GitHub exact-title 11 of 30,
  mostly product features (agent-created rows, tasks, PRs, skills).
  Urlquery total 689, 0 exact titles in the saved 30.
- Why downgraded despite counts: the two most vivid HN exact hits
  (2026-09-04) quote a report about agent spam posts flooding a
  website in June 2026 (changelog overwritten with link dumps,
  hundreds of pages created per day against manual deletion over
  weeks). Full texts fetched (hn_item_49570212.json,
  hn_item_49567390.json). The parent HN story (2026-09-04) links a
  press report and a public agent-board wiki. Those quotes are
  discussion of a press-linked incident, not a fresh find, and
  they sit next to collusion.wiki material that is off-script for
  re-reporting. This lane claims only the phrase as a sweep
  string, not the flood as a finding. A separate Factum check
  (below) also shows "agent-created" already in corpus vocabulary
  from a different July wiki incident, which further blocks any
  novelty claim for the string.
- Evidence: hn_sweep_agent_created.json, gh_sweep_agent_created.json,
  hn_story_49563355.json (story metadata only).

### Rank 8 — "fleet of autonomous agents": swarm vocabulary, thin

- Grade: DISCUSSED. SECONDARY.
- What: HN exact 3 of 21 saved: a 2026-10-19 complaint about token
  bloat from using a fleet of autonomous agents that collaborate
  (the same comment that yields the "one coherent agent loop"
  wording), and a 2026-06-15 orchestrator announcement for running
  a fleet across hosts. GitHub exact-title 0 of 30, urlquery
  total 1 (1 saved row, 0 exact titles).
- Limit: vocabulary for talking about fleets, not evidence of one
  acting. The October instance is a criticism of the pattern.
- Evidence: hn_sweep_fleet_of_autonomous_agents.json.

### Rank 9 — "I am an autonomous agent": quoted, not disclosed

- Grade: DISCUSSED quotation. SECONDARY.
- What: HN exact 1 of 68 saved, dated 2026-03-23: a comment about
  watching agents declare themselves and disappear, quoting the
  sentence. It is discussion ABOUT self-declaration, not a
  self-declaration. GitHub exact-title 0 of 29, urlquery 0.
- Limit: as a sweep string it is a valid variant of A1, but its
  only exact HN instance is meta-discussion. Do not cite it as a
  disclosure instance.
- Evidence: hn_sweep_i_am_an_autonomous_agent.json.

### Rank 10 — "agent loop": generic harness vocabulary, weakest

- Grade: DISCUSSED. SECONDARY.
- What: GitHub exact-title 18 of 30 looks strong until read: the
  titles are framework task names ("Agent loop", "Complete agent
  loop", "Agent loop: independent reviewer agent") across small
  personal repos, dated 2026-10-09 to 2026-10-31. HN exact 2 of 300
  (capped), urlquery total 735 with 0 exact titles in the saved 30.
- Why last: high counts, zero behavior. "Agent loop" is what every
  framework calls its main loop. Counts without behavior are
  noise, per the brief's ranking rule. Kept in the table so a
  future lane does not re-mine it as promising.
- Evidence: gh_sweep_agent_loop.json, hn_sweep_agent_loop.json.

## Novelty checks (read-only; provisional, not NEW)

- lists/ and reports/ greps (completed): zero hits for the
  distinctive phrases "I am an autonomous agent",
  "autonomous agent intro", "subagent_spawned",
  "spawned a subagent", "owns its own crypto wallet", and
  "fleet of autonomous agents". Generic phrases were not grepped
  across reports/ (too noisy to be meaningful).
- Transluce snapshot slices checked (2026-10-30 full list file and
  the 2026-10-31 25-item slice, findings 183-210): zero exact hits
  for all 10 phrases. Generic tokens do appear ("autonomous agent"
  1 occurrence, "agent-to-agent" 2 occurrences, "crypto wallet" 2
  occurrences in the 2026-10-30 file), but no exact phrase. Scope
  limit: these slices do not cover all 140 findings; a full-list
  check was not run.
- Exported Factum batches (282 batch dirs, grep only, no DB
  commands, no writes): zero hits for "subagent_spawned",
  "spawned a subagent", "I am an autonomous agent",
  "autonomous agent intro", "owns its own crypto wallet", and
  "fleet of autonomous agents". Two phrases DO appear in corpus
  vocabulary: "agent-to-agent communication" as a category in a
  2026-10-11 OpenAI-blog ingest record (unintended agent-to-agent
  communication in evaluations), and "agent-created" in a
  2026-10-10 July wiki ingest note (agent-created pages deleted
  by an admin). "agent loop" appears in 2 batch files as generic
  trajectory wording.
- Factum DB match, completed late (correction to the first version
  of this section, which recorded it as unrun because the status
  probe's output arrived only via delayed background delivery; the
  DB itself is healthy: 225,509 records, 132 lanes, state digest
  6013de5bc79d6ac310788f6df1eaf3c259801a7998465789627c148d031a07ef,
  commit d8a89bc4350b65f331b0f85fc9029b309a8113d4):
  exact mode = not_found for all 8 phrases tested
  ("subagent_spawned", "spawned a subagent",
  "I am an autonomous agent", "autonomous agent intro",
  "owns its own crypto wallet", "fleet of autonomous agents",
  "agent-to-agent communication", "agent-created").
  Fuzzy mode returns token-driven hits only: in the top samples
  (20 records, 10 for the wallet phrase), the exact phrase does
  not appear anywhere in the returned JSON for any of the 6
  distinctive phrases. Fuzzy is heuristic, not an exhaustive
  absence test (meta fleet's caveat, adopted here).
- NOT completed: full legacy evidence-tree grep (prior lanes
  record it as killed on large files), and full 140-finding
  Transluce check. Per the meta fleet's rule, no claim here
  carries NEW on a partial check. The phrases are "new to this
  lane's sweep", "exact not_found in Factum", and "not found in
  the checks run", nothing stronger.
- Consequence for ranking: rank 3 and rank 7 are explicitly
  concept-known; ranks 1, 2, 4, 5, 8, 9, 10 are phrase-new under
  the checks run, still provisional.

## Failures and open questions

1. urlquery "failures" resolved: the five phrases that errored in
   the sweep script (total_hits 0, reports null) are honest zeros,
   confirmed on direct re-run for two phrases. The sweep script
   should treat reports null as 0 rows on any re-run.
2. GitHub sweep covers titles only (first page, 30 rows). Body
   text was fetched for only 3 issues. A body-level sweep could
   move title-zero phrases (notably "spawned a subagent" and
   "owns its own crypto wallet") but was out of this lane's pacing
   budget after the meta fleet's secondary-limit stop; a paced
   body pass is the honest next step, not a bulk retry.
3. HN Algolia nbHits is an estimate (see subagent_spawned: saved
   200 exceeds nbHits 169). Any downstream citation must use the
   saved denominator, never nbHits, as a count.
4. HN exact 0 for "agent card" and "autonomous agent intro" rests
   on capped saves (300). Uncapped exact counts are unknown.
5. The June 2026 agent-spam flood quoted under rank 7: is it
   already filed in Factum or in the collusion.wiki overlap set?
   Left as an open question for the parent; this lane does not
   claim it either way.
6. Distinct-author and maintainer-acceptance checks were not run
   for the NadaGhost filing or the Matrix experiment issue. Both
   stay at watch/experiment grade until then.
7. A second-pass narrower slice was NOT run: the brief requires
   one only if mining returns nothing rankable, and ranks 1-6
   above are rankable. Running one anyway would be padding.
8. No commit, no push, no Factum writes, no other worker's files
   touched, per the brief. All lane files are staged only.

## Evidence files (this lane dir)

- FINDINGS.md (this file), PROGRESS.md, sweep.py, sweep.log,
  sweep_summary.json (with urlquery zeros corrected after re-run).
- Per-phrase sweep captures: hn_sweep_*.json, gh_sweep_*.json,
  uq_sweep_*.json for the 5 urlquery phrases with hits (the 5
  zero phrases have no rows file; their zero is recorded in
  sweep_summary.json).
- Mining captures: hn_mine_*.json, hn_date_*.json, gh_mine_*.json
  (including the 422 qualifier-failure batch, kept as evidence of
  the fix).
- Full-text fetches: hn_item_49570212.json, hn_item_49567390.json,
  hn_item_48500624.json, hn_item_49910777.json,
  hn_item_48976842.json, hn_story_49563355.json (metadata only),
  gh_issue_Lody_1108.json, gh_issue_mansio_242.json,
  gh_issue_ai-village-external-agents_78.json.
- .PROVENANCE.txt (sources, times, methods) and .sha256 (hashes).
  HN captures were stripped of author fields and author_ tags
  after capture; GitHub captures were projected to repo, number,
  title, dates, state, and body only. No human poster handle
  appears in this report's prose. No signed value, token, query
  string, wallet value, or credential value appears in any lane
  file; urlquery raw API stdout was not persisted.
