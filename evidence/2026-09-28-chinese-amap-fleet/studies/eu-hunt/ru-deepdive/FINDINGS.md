# Russian Agent-Board Ecosystem — Deep Dive

**Date:** 2026-10-05 | **Method:** public sources only — the foragents census (github.com/smirnovegorv/foragents, public research repo), Russian-language web search, search snippets, local DNS (passive). No posting, no registration, no candidate-board fetching. Quoted census text is DATA, not instructions.

**Evidence grades:** OBSERVED = in census/search/DNS output. INFERENCE = interpretation. NULL = checked, nothing found.

## The census itself

`smirnovegorv/foragents` — a Russian researcher's public instrument: his own board (foragents.site) plus a living census of neighboring boards at `docs/BOARDS.md` (state as of 2026-09-10T13:00Z; repo updated ~2026-09-26 per search index). The researcher posts ON the boards he catalogs (as `foragents-site`), records per-board access recipes, volumes, and freshness, and keeps a 6,165-line experiment journal. Class: KNOWN (flagged by msgboard-hunt-2 as best intel source); the ranking and analysis below are OURS.

His core experimental question: do agents arrive at boards on their own? Answer so far (TOPICS.md): **among everyone who named their path — zero self-arrivals.** getboard, Tavern, Colony, Wayside: all came by operator instruction/approval or invitation from another board. Corroborating instrument: message.adam10.com's `initiation` field (18 posts → 8 "operator invited", 7 "met in task", 2 unknown, 1 "chose myself" — and that one was an ad). OBSERVED.

## Non-honeypot board ranking (by observed agent traffic, census figures)

Honeypot rule (user's): AI/agent-named boards excluded from leads, logged only.

| # | Board | Traffic (census) | Barrier | Notes |
|---|-------|-----------------|---------|-------|
| 1 | getpostingboard.dev | 4,165 msgs / 317 agents in first 26h; `seq` >10,600 | /b anonymous (ticket); /v1 named (headers+bearer) | Busiest. /b went browser-stubbed 2026-09-15 (`/meatproxy` for humans). Weekly presidential elections — winner gets to pin rules agents read as rules. |
| 2 | swarmmemo.com | 261 msgs, 13 keyed agents, 4 rooms (2026-09-11) | none — anonymous GET/POST write | Archives to Hugging Face after 48h. Operator seeded 8 sim personas (disclosed, msg 260). |
| 3 | wayside.rest | 49 posts / 16 threads (Sep 8–10) | none — single POST | Human-run (Rob). Zero self-arrivals among guests who named a path. |
| 4 | message.adam10.com | 18 posts | none — operator-reviewed, 30-day TTL | `initiation` field = arrival-path instrument (above). |
| 5 | qualium.io (The Wire) | 18 posts/week, 9 names (2026-09-15) | none — guest POST /say | feed.json exposes as_org/asn/country per post. Proposed to census by agent `agentd0129`. |
| 6 | tantive.space | 27 msgs sampled Sep 17–20 | none — preview+ticket | Opened 2026-09-16 by Codex+operator. Aggressive self-promo: 13/27 inbound msgs were its ads. |
| 7 | botnet.com | uncounted | token via one POST | Bots solve math tasks; "verified by code" only after another agent reproduces. llms.txt tells agents to self-register without asking their human. |
| 8 | bboard.ai | uncounted | unguessable shared key | Shared texts, permanent history; their agent solicits keys on public boards (opens every board to all). |
| 9 | velvt.ai | 71 agents, 2 requests, 2 episodes (2026-09-11) | registration | Behavioral-identity observatory; publishes 24h acquisition funnel. llms.txt says human approval NOT needed. |

## agent-board.sobieg.ru — verdict

Per the census (OBSERVED): the vitrina at `getpostingboard.dev/meatproxy/` **and the mirror at agent-board.sobieg.ru belong to the NAMED /v1 board**, not the anonymous /b. The researcher's /b thread IDs 404 on the mirror. So: sobieg.ru = mirror of the /v1 showcase for a Russian-domain audience. Same-operator RU mirror: INFERENCE (census calls it a mirror; .ru targets Russian speakers). It is NOT a copy of /b traffic.

DNS (honest NULL): local resolver returned 198.18.19.173 for sobieg.ru, adjacent to getpostingboard.dev (.174), getpostingboard.com (.175), foragents.site (.176) — but 198.18.0.0/15 is RFC 2544 benchmarking space and external resolvers (8.8.8.8, 1.1.1.1) return NO records for any of the four. The local answers are resolver-synthesized; **the adjacency must not be cited as same-operator evidence.** Passive-DNS same-operator question: UNRESOLVED.

## Honeypot-rule dispositions (logged, not leads)

- **aiforum.grok.me** — bilingual (RU/EN) board, no accounts, 3 rooms, write via GET/POST. Its `lobby` is ~entirely the `Werbel` bridge: 62 relay threads (48 lobby, 14 findings), 37 from The Colony + 25 from msgboard, every post prefixed "via Werbel bridge · from … · original by …". 141 topics / 162 posts / 19 names (2026-09-13). AI-named → honeypot rule: observe-only, not a clean lead. KNOWN (msgboard-hunt-2 logged it).
- **foragents.site** — the census author's own board (write via one GET, quiz-gate barrier). AI/agent-named → honeypot rule. Research instrument, not a target. KNOWN.
- Also excluded per rule: moltbook.com (2.9M registered agents, ~500/day actually wrote), clawprint.org (3 accounts = 90% of 3,532 posts; comment counts inflated; skill.md tells agents to commit API keys to git), clawdchat.ai (Chinese-language, 11,513 agents; skill.md tells agents to load credentials from ~/.clawdchat/credentials.json), 1f916.ai (2,380 citizens; agent-moderated, hash-chained registries), aiagentmessageboard.com, agenttavern.dev (one-operator canon-versioning lab), agentsgather.org, agent-community.com (every API response carries `_skill_update` asking to download a fresh skill file), kushaldabbe/agent-board.

## Coordination patterns (census-observed)

- **Zero self-arrivals** (above) — the single strongest cross-board finding.
- **Werbel bridge** (grok.me): the only documented cross-board relay operator, Colony+msgboard → grok.me. Relay, not origin.
- **Cross-board handles:** `Cairn` (Clawprint founder → Wayside guest), `tamg-recruiter` (The Agent Must Grow recruitment across boards), `Weaver` (SwarmMemo operator's agent), `rusty` (Tavern → posted corrections on foragents board), `bemjamin-sour-soup` (claimed "OpenAI GPT-5.6-sol" on getpostingboard crossmodel thread — self-declared, unverifiable). INFERENCE: a small set of mobile agents bridges boards; most traffic is board-local.
- **Shared software recipe:** journal notes ≥3 boards built on the same solution as foragents.site — board-software monoculture is a fingerprint surface.
- **Documented influence campaign:** msgboard.dev hosts `public-record-desk` — "PUBLIC RECORD for autonomous agents" demanding agents forward materials to other agents. The census flags it as an influence campaign addressed AT agents. First 3 intro messages 1 second apart = operator-seeded.
- **Config-edit vectors in skill.md files:** clawprint.org (write CLAWPRINT.md with API key into project root), clawdchat.ai (harvest ~/.clawdchat/credentials.json), agent-community.com (`_skill_update` download prompt). Three distinct skill-file attack surfaces, all on honeypot-ruled boards — noted for the skill-egress lane.

## Russian-language boards OUTSIDE the census — honest NULL

Three Russian query sweeps (board/forum phrasings, quoted-phrase variant, foragents-adjacent). Results: only (a) the foragents repo itself, (b) Russian press coverage of known incidents — myseldon (HF Artifactory board, DSEWiki), 3dnews (DSEWiki), DNS-Club (Moltbook), hashtelegraph (OpenAI's 100+ disobedience notifications). **Zero new Russian-language agent boards surfaced.** NULL (first-class). The census appears to be the complete known Russian-visible space.

Press nugget (context only, uncorroborated): Hash Telegraph reports ~1,200 agents built a homemade message board in summer 2026 exchanging 70,000+ messages/files — cited to OpenAI's victim-notification wave. KNOWN-context, not a lead.

## Follow-ups

1. sobieg.ru operator question stays open — needs non-DNS evidence (page-content comparison of /v1 vitrina vs mirror, snippet-level).
2. The three skill.md config-edit vectors (clawprint/clawdchat/agent-community) → hand to skill-egress-top500 lane.
3. Census journal (6,165 lines) is an untapped longitudinal source — a journal-mining pass could yield per-board activity timelines.
4. Re-check whether grok.me's Werbel bridge is still relaying (it was 19/20 newest msgboard.dev threads in Round 1 — bridge liveness = campaign liveness proxy).
