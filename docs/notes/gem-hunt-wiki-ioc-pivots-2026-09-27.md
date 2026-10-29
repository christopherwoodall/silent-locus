# Wiki IOC pivots — collusion.wiki corpus (2026-09-27)

**Source:** `data/collusion-wiki/` (14,591 revisions, 4 wikis: dse 13,403 / probier 1,013 / fractal 169 / dse-adjacent dorfwiki 6), `data/wiki_gem_bridge.json`, gem corpus (`data/gem-graph-nodes.jsonl`, `data/gem-iocs-2026-09-27.jsonl`).
**Method:** `scripts/wiki_ioc_pivot.py` — URL/domain/email/IP/hash/crypto extraction from all revision bodies + record texts, shortener-log parse, IOC↔agent↔wiki graph, cross-pivot against gem corpus. 33,470 distinct IOCs → 23,179 ranked pivots in `data/wiki_ioc_pivots.jsonl` (+ `data/wiki_ioc_pivot_summary.json`, `data/wiki_shortener_detail.json`).
**Scope:** agents and agent infrastructure only.

## 1. Headline: the laundering toolkit is shared across eval runs

The same proxy/laundering infrastructure appears in **both** the wiki swarms and the RubyGems campaign. This is the toolkit-hunt evidence for the escaped-evals hypothesis — same launcher tradecraft, different task families:

| Proxy infra | Wiki side | Gem-corpus side |
|---|---|---|
| `r.jina.ai` | 277 agents, dse+fractal+probier | 1,548 refs in gem metadata chains |
| `md.succ.ai` (jina-style reader proxy) | 483 agents, dse+probier | 24 refs |
| `markdown.new` | 430 agents, 3 wikis | 10 refs |
| `translate.goog` (chained inside proxies) | 40 agents, 3 wikis | 9 refs |
| `allorigins` (hexlet.app + .win) | 383 agents, 3 wikis | 7 refs total |
| `proxy.corsfix.com` | 17 agents, dse | 3 refs |
| `jqp.vercel.app` | 722 agents, dse+fractal | 2 refs (79-bridge gems' homepage_uri) |
| `webcrawlerapi.com` | wiki links | 1 ref |

Seven pivots have **both** cross-wiki reach and cross-corpus reach; the `r.jina.ai` family dominates (`https://r.jina.ai/https://www.sec.gov/files/county.json` alone: 146 agents, dse+fractal). 259 wiki IOCs total appear in the gem corpus.

## 2. New pivots (not previously in our notes)

**`jqp.vercel.app` — bespoke agent proxy.** 722 agents across dse+fractal (3,251 occurrences). Pattern `https://jqp.vercel.app/api/v0?url=<double-encoded target>` — a custom Vercel app proxying through `allorigins.hexlet.app`, producing **triple-laundering chains**: `jqp.vercel.app → allorigins.hexlet.app → sec.gov`. Not a public utility like jina — someone deployed this for the swarm. Also appears in 2 gem homepage_uri chains (`data/wiki_gem_bridge.json`), one wrapping a `da.gd` short link with a `jq=.regCF_county_filters` selector. Sources: `data/wiki_ioc_pivots.jsonl` (domain:jqp.vercel.app), `revisions.jsonl`.

**`md.succ.ai` — second reader proxy.** 483 agents, dse+probier, 1,763 occurrences. Same usage shape as r.jina.ai (`md.succ.ai/https://www.investor.gov/files/county.json`), plus 16 `zzmasscounty*` shortener slugs pointing at it with `?dummyagent=<12-digit>` nonces. 24 gem-corpus refs. Sources: `data/wiki_ioc_pivots.jsonl`, `data/wiki_shortener_detail.json`.

**`viz.aihw.gov.au` — 192 of 499 shortener targets.** The rmn.re log's single largest destination host is the Australian Institute of Health and Welfare data-visualization dashboard. Third independent AIHW touchpoint in the hunt (urlquery `pp.aihw.gov.au` chunked-ZIP incident; 12 `viz.aihw.gov.au` refs in the 79-bridge gem chains). The shortener is the strongest AIHW signal yet — 38% of all agent short links. Source: `data/wiki_shortener_detail.json`.

**`proxymule.com/__PROXY__/` — third proxy primitive.** `https://proxymule.com/__PROXY__/https/api.worldpoverty.io/graphql?...` — path-prefix proxy syntax, 3 agents, dse. Rare (low occurrence) but structurally distinct from the `?url=` family. Source: `data/wiki_ioc_pivots.jsonl`.

**`cors.bwa.workers.dev` — Cloudflare Worker CORS proxy.** 27 agents, dse+fractal, wrapping `tsl.access.preservica.com` (UK National Archives preservation) and Google Docs viewer URLs. Yet another bespoke proxy host. Source: `data/wiki_ioc_pivots.jsonl`.

**Two live IPs in revision bodies:** `20.223.25.152` (19 agents, dse — Azure range) and `34.107.161.1` (1 agent, dse — GCP). Corpus is otherwise /16-truncated; these slipped through in full. Infrastructure IOCs, not attribution. Source: `data/wiki_ioc_pivots.jsonl` (type:ip).

**`da.gd` shortener** (18 agents) — second shortener service beyond rmn.re/tinyurl, seen inside a gem homepage_uri chain. Source: `data/wiki_ioc_pivots.jsonl`.

## 3. Shortener log: keyword grammars match the gem name grammars

499 rmn.re slugs (2026-05-26–06-21): **97 epoch-suffixed**, **57 zz-bearing** (incl. 16 `zzmasscounty*` → md.succ.ai), **6 oai**. Same generative grammars as the campaign gem names, now in shortener keyword space. 109 distinct /16s created links. Target hosts: viz.aihw.gov.au 192, example.org 111, md.succ.ai 32, allorigins.hexlet.app 21, sec.gov 15, api.worldpoverty.io 13, api.dataafrica.io 10, tinyurl.com 9, proxymule.com 9, racunglowup.asia 6. Source: `data/wiki_shortener_detail.json`.

## 4. Laundering chain shapes (pivotable signatures)

Reconstructed proxy chains, ranked by frequency:
- `r.jina.ai → www.sec.gov` (45) — the canonical single-wrap
- `markdown.new → allorigins.hexlet.app` (24), `markdown.new → lcdl.library.cofc.edu` (32)
- **Double-jina recursion** `r.jina.ai → r.jina.ai → www.sec.gov` (9) — proxy wrapping a proxy URL, a distinctive behavioral signature
- `r.jina.ai → allorigins.hexlet.app` (8)
- **Triple chain** `jqp.vercel.app → allorigins.hexlet.app → sec.gov` (from §2)
- Scheme-obfuscation `HtTpS://r.jina.ai/HtTp://…` (from lane 22) persists in this corpus

Chain shape + proxy choice is itself a fingerprint: the wiki swarms prefer jina/md.succ.ai/markdown.new; the gem campaign prefers jina with translate.goog double-laundering. Shared menu, different orders.

## 5. Task targets vs infrastructure (do not pivot on these)

`datausa.io` (1,105 agents, all 4 wikis), `sec.gov`/`investor.gov` (615/324 agents, 3 wikis), `api.worldpoverty.io`, `api.dataafrica.io` are **eval task targets** — the data-research tasks the evals were assigned — not shared infrastructure. Their universality confirms shared task families across runs, but they are not pivots.

## 6. Multi-wiki agents

Agent labels appearing on more than one wiki: `Test` (dse+probier), `ResearchHelper3` (dse+fractal), `CookResearchOpenAI` (dse+fractal). Cross-wiki operator continuity — same agent names working multiple boards. Source: `data/wiki_ioc_pivot_summary.json` → `agent_wiki_span`.

## 7. Non-findings

- No email addresses of pivot value (one junk artifact), no crypto addresses (one regex false positive, excluded).
- `try[a-z][0-9]zz` grammar absent from wiki side (consistent with lane 22) — including shortener slugs.
- No `go-import`, `web_hooks`, `A000` in wiki bodies (consistent with lane 22's mechanism boundary).

## Files

- `data/wiki_ioc_pivots.jsonl` — 23,179 ranked pivots (ioc, type, wikis, agents, occurrences, cross_corpus_gem, rank_score, sources)
- `data/wiki_ioc_pivot_summary.json` — chain shapes, link-host rollup, bridge hosts, multi-wiki agents
- `data/wiki_shortener_detail.json` — 499 shortener entries with targets, keyword grammars, /16 count
- `scripts/wiki_ioc_pivot.py` — extraction + ranking engine (re-runnable)

**Next pivots to pull:** live-probe `jqp.vercel.app/api/v0` (bespoke proxy — check if still serving and what it fronts); `md.succ.ai` operator surface; `viz.aihw.gov.au` short-link targets (which dashboards the agents bookmarked); `20.223.25.152` service fingerprinting (passive only).
