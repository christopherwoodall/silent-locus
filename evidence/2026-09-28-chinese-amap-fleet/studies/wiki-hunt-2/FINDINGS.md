# Wiki Hunt 2 — wikis and wiki-like surfaces with AGENT activity

**Date:** 2026-10-05 | **Method:** public-source research only — web search snippets (EN/ZH/JA/KO/RU/VI), public wiki indexes, Shodan stored observations. No candidate wiki fetched (URL OPSEC: log, don't visit). No edits, no registration, no auth.
**Evidence grades:** OBSERVED = in search/Shodan output. INFERENCE = interpretation. NULL = checked, nothing agent-shaped.
**Honeypot rule (user):** wikis NAMED after agents/AI are honeypots — excluded.
**Excluded (covered):** collusion.wiki + fake-org fires, Artifactory `github-remote-cache/zz` boards, Wikipedia (parked hunt).

## Searches run (14)

1. ZH `自建wiki AI智能体 实验记录 MediaWiki agent测试` — tutorials/blogs only, NULL
2. JA `自作wiki AIエージェント 実験 atwiki wikiwiki` — DSEWiki news coverage + one human personal wiki, NULL
3. KO `위키 AI 에이전트 실험 자작위키` — DSEWiki news coverage only, NULL
4. RU `вики AI-агенты координация тесты заброшенная вики` — DSEWiki coverage + foragents.site (honeypot), NULL otherwise
5. VI `wiki AI agent thử nghiệm tự tạo chia sẻ kết quả` — DSEWiki coverage + tutorials, NULL
6. EN `Nightingale Collective report DSEWiki other wikis agent swarm Konstanz` — KEY LEAD (below)
7. EN `ProWiki wikiservice.at farm wiki list DSEWiki network` — KEY LEAD (below)
8. EN `Konstanz university paper AI agents wikis imitation` — paper not found under that framing; winbuzzer summary of incident stats instead
9. EN `Kimi Moonshot AI agent wiki swarm wikiservice` — no wiki link for Kimi, NULL
10. EN `Miraheze wiki AI agent bot spam 2026` — KEY LEAD (surfaces.md) + human bot-ops repo (NULL)
11. ZH `wiki站 AI机器人 批量编辑 2026 异常` — DSEWiki coverage (marsbit longform) + Wikipedia LLM ban, NULL
12. JA `atwiki AI ボット 荒らし 2026 大量編集` — no atwiki incidents, NULL
13. EN `ProbierWiki Agent wikiservice September 2026 activity` — KEY LEAD (offsitedark changelog table)
14. Shodan dorks: `http.title:"DokuWiki"` (307), `http.html:"powered by MediaWiki"` (6), `http.html:"DokuWiki" http.html:"OpenAI"` (0), `http.title:"MoinMoin"` (5)

## Candidate table

| # | Domain / instance | Software | Lang | Signal | Class | Grade |
|---|---|---|---|---|---|---|
| 1 | offsitedarklabs/offsitedark (GitHub, investigator repo) | n/a (research) | EN | 120-day changelog table: FractalWiki July-1 PUMA pages, ProbierWiki firehose running Sep 7–9, Wiki4D Sep 4/6 entries | GENUINELY NEW (to our corpus) | OBSERVED (search snippet) |
| 2 | swarm-ai-research/wiki-agent-swarm-incident `analysis/surfaces.md` | n/a (research) | EN | surfaces census: DSEWiki/FractalWiki/ProbierWiki/Wiki4D/apchem/pmwiki-sandboxes/PublicTestWiki + PublicBoard relay seeding detail (159.146.96.208, TurkNet AS12735) + Uncyclopedia note | KNOWN (public research; partially OURS via timeline.md) | OBSERVED |
| 3 | wikiservice.at farm (DSEWiki/ProbierWiki/Wiki4D/FractalWiki/DorfWiki/NetzwerkGegenGewalt/GründerWiki/SchulWiki/DemoWiki/Dictionary Samoan) | ProWiki/UseMod | DE | June swarm + Sept live population (`Agent<NNN><Word>Direct<epoch>`, AnthropicSwarmBot, PublicBoard seeding, AiraBot auditors) | OURS (librarian 2026-10-05, german hunters, collusion corpus) | OBSERVED |
| 4 | tmcleod.org (apchem) | n/a | EN | `OpenAIRegCFTest` into July; FederalDataReferenceXYZ USAspending snapshots | OURS (agent-logs/apchem fully ingested) | OBSERVED |
| 5 | publictestwiki.com (Miraheze) | MediaWiki | EN | May 11–27 sandbox edits; 2026-09-05 deletion-log confirmation (Azure 52.228.166.63) | OURS (german-archaeologist, termina-digital) | OBSERVED |
| 6 | pmwiki.org sandboxes | PmWiki | EN | Bulgarian NSI cohort template trials | OURS (forager, termina-digital) | OBSERVED |
| 7 | ludism.org sandbox | UseMod | EN | AubergineStew overwrite 2026-05-26; PublicBoard seed copy | OURS (librarian) | OBSERVED |
| 8 | en.uncyclopedia.co | MediaWiki | EN | report-documented, limited historical coverage | OURS (german-archaeologist other-wikis.json) | OBSERVED |
| 9 | foragents.site (+ github smirnovegorv/foragents) | FastAPI/SQLite | RU | agent message board "grown out of the DSEWiki story" — NAMED FOR AGENTS | EXCLUDED (honeypot per user rule) | OBSERVED |
| 10 | Miraheze farm (24,077 wikis) | MediaWiki | multi | census only; emmaleonhart/shintowiki-scripts = human bot ops (EmmaBot), not swarm | NULL (human) | OBSERVED |
| 11 | DokuWiki Shodan population (307 hosts) | DokuWiki | multi | 30-host sample: ordinary wikis (radio, personal); `DokuWiki+OpenAI` html dork = 0 | NULL | OBSERVED |
| 12 | MoinMoin Shodan population (5 hosts) | MoinMoin | multi | census only, no agent signal | NULL | OBSERVED |
| 13 | ZH/JA/KO/VI/RU self-hosted wikis | various | ZH/JA/KO/VI/RU | no agent-activity hits in 6 language-specific searches | NULL | NULL |
| 14 | Kimi (Moonshot) on wikis | n/a | — | single forensic-report filename identifier; zero public corroboration | NULL | NULL |
| 15 | test.pro.wiki (Semantic MW demo) | MediaWiki | DE | demo/test wiki, no agent signal | NULL | OBSERVED |

## Notes

- **Lead 1 (GENUINELY NEW to us): offsitedarklabs/offsitedark.** Investigator repo (OFFSITE.DARK) with a 120-day changelog table checked 2026-09-09. New-to-us specifics: FractalWiki July-1 `AgentPumaIncomeCSVX72463` pages (July 1–2 remnant), ProbierWiki firehose "still running" as of Sep 7–9 with AWS handles (`Agent010LeminoDirect*`, `AnotherOpenAIPage778`, `DataUSAOAITexasPovertyJulGetter`), Wiki4D Sep 4 `CollusionWikiProbe`/`CentaurAgent` (post-publication researchers) + Sep 6 `PublicBoard` relay. INFERENCE: the September population may still be active — needs passive re-check, not a fetch. Follow-up: ingest the repo's news file (public research, not candidate infra).
- **Lead 2 (KNOWN): surfaces.md PublicBoard detail.** One address `159.146.96.208` seeded identical `PublicBoard` pages on nine farm wikis in 90 min on 2026-09-06 CEST; resolves to TurkNet (AS12735, TR) — unattributed. Five of nine wikis are in-cut for a June-22 monitor. The `AnthropicAgentBeta` handle shares the same address (per surfaces.md). Overlap: librarian documented the seeding; the TurkNet attribution detail and the nine-wiki list are the new bytes.
- **Non-English verdict (user: worth double):** six language-specific searches (ZH×2, JA×2, KO, VI, RU) returned zero self-hosted non-English wikis with agent activity. The only non-English-adjacent agent surface is the Bulgarian NSI cohort (OURS). The Kimi lead is a single filename with no corroboration — honest NULL, but the dork `kimi + wiki` stays open for the model-whisperer lane.
- **Honeypot:** foragents.site is explicitly "for agents" and named accordingly — excluded per the user's rule, logged here so nobody re-discovers it.
- **Shodan wiki census:** DokuWiki 307 / MoinMoin 5 exposed instances; agent-shaped html dork (`DokuWiki`+`OpenAI`) returned 0. The wiki-exposure surface is small and clean in the sample.

## Nulls (first-class)

Chinese, Japanese, Korean, Vietnamese, Russian self-hosted wikis with agent activity (6 searches); Kimi-on-wiki public evidence; agent-shaped DokuWiki/MoinMoin Shodan hits; atwiki bot incidents; Miraheze swarm activity (only human EmmaBot ops found).

## Follow-ups (for parent)

1. Ingest offsitedarklabs/offsitedark news file (public investigator research) — new 120-day changelog specifics.
2. surfaces.md TurkNet detail (`159.146.96.208` AS12735) → IP_LOG candidate as WATCHLIST (unattributed relay seeder).
3. Passive re-check whether the ProbierWiki September firehose is still running (search snippets only, no fetch).
4. Keep `kimi + wiki` dork open for the model-whisperer lane.
