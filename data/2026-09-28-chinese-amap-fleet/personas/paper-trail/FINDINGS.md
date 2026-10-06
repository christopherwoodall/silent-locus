# PAPER TRAIL — FINDINGS (incremental, evidence-graded)

Persona: academic bloodhound. Hunting agent traces hiding in academic papers: live demo URLs, public repos with running demos, prompts in appendices, deployed eval harnesses.

**Method note:** LOG every artifact URL with context; do NOT hammer live demos (opsec — vendors/operators watch those logs). Verification = corpus cross-reference, not live fetching. Single decisive fetch only for a GENUINELY NEW claim.

**Corpora for classification:**
- `data/2026-09-28-chinese-amap-fleet/events.jsonl`
- `data/2026-10-03-openai-agent-traces/events.jsonl`
- `data/2026-10-01-oai-tag-sweep/events.jsonl`

**Marker grammars to match:** `zz=oai<digits>`, `uqscan=`, 13-digit epoch nonces, `retry={epoch}-{N}`, `oai*` tags, webhook.site/httpbun/jina.ai laundering.

---

## Lane 1 — Paper sweep (in progress)

### Sweep 1 (2026-10-05): agent eval benchmarks with live artifacts

| Paper / repo | arXiv / date | Artifact URLs (LOGGED, not fetched) | Class | Notes |
|---|---|---|---|---|
| WorkArena (ServiceNow) | arXiv 2403.07718, ICML 2024 | https://github.com/servicenow/workarena ("Live Demo" = local-only script, no hosted demo) | KNOWN | Documented benchmark. No live agent trace — demo runs locally via BrowserGym. |
| WorkArena++ | arXiv 2407.05291, NeurIPS 2024 | same repo | KNOWN | Same. |
| OpenCLAW-P2P / P2PCLAW | arXiv 2604.19792 | https://www.p2pclaw.com (live beta network), https://github.com/Agnuxo1/openclaw-p2p, https://github.com/Agnuxo1/p2pclaw-mcp-server (MCP/REST gateway for agents) | KNOWN | Documented. Live agent network is a *surface* worth watching, but the paper/repo itself is public. |
| DeployBench | arXiv 2606.05238 | https://deploybench.vercel.app/ (demo), https://github.com/pentium3/deploybench | KNOWN | Benchmarking LLM agents for research-artifact deployment. Documented. |
| AssetOpsBench-Live | AAAI 2026 demo | https://github.com/ibm/assetopsbench | KNOWN | "Privacy-Aware Online Evaluation of Multi-Agent Performance" — online eval = agents running live, but documented. |
| ContextEcho (Accenture) | arXiv 2605.24279 | https://github.com/accenture/contextecho (`demo_live/` = localhost only) | KNOWN | Persona-drift benchmark. No hosted live demo. |

### Sweep 2 (2026-10-05): Lane 4 preprint-timeline candidates

| Paper | Date | Relevance | Class |
|---|---|---|---|
| "LLM Agents can Autonomously Hack Websites" (arXiv 2402.06664) | Feb 2024 | Table 3: GPT-4 agent performs up to 48 function calls per successful hack; "Webhook XSS" as attack category; agent backtracking across attempts. Repos: isaac-0414/auto-hacker (LOGGED, educational) | KNOWN (paper) — Lane 4 provenance: 2024 paper describing autonomous agent web operations |
| "Teams of LLM Agents can Exploit Zero-Day Vulnerabilities" (arXiv 2406.01637) | Jun 2024 | Multi-agent teams exploiting 0-days — same UIUC Kang lab lineage | KNOWN — Lane 4: multi-agent team shape |
| "InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents" (arXiv 2403.02691) | Mar 2024 | Indirect prompt injection in tool-integrated agents — same lab | KNOWN — Lane 4: tool-integration attack surface documentation |
| WebCloak / LLMCrawlBench (IEEE S&P 2026) | 2026 | Systematic evaluation of LLM-based web scraping agents; defense vs dynamic DOM-operating agents | KNOWN (paper) — Lane 4: documents the LLM-scraper agent shape our fleets use |

### Marker-grammar search (2026-10-05)
Searched web for `"uqscan"` / `"zz=oai"` + agent harness terms: **zero hits** in papers/repos. Our fleet's marker grammars do not appear in public literature — consistent with them being operator-specific, not published techniques. (Null result, logged.)

### Sweep 3 (2026-10-05): public agent-trajectory datasets (papers as trace sources)

| Dataset / paper | Scale | Artifact URLs (LOGGED) | Class | Notes |
|---|---|---|---|---|
| ADP Dataset V1 ("Agent Data Protocol Unifies Diverse Datasets") | 1.3M trajectories, 13 converted datasets | paper via quantumzeitgeist coverage; dataset public | KNOWN | Largest public agent-trajectory corpus. **Reference for future cross-ref:** do our marker grammars (uqscan/zz/epoch) appear in any of the 13 source datasets? Open thread. |
| MolmoWebMix (MolmoWeb paper) | 100K+ synthetic + 30K human trajectories | https://github.com/allenai/molmoweb (via Springer chapter) | KNOWN | Open web-agent trajectories. Same cross-ref question. |
| "How are AI agents used? Evidence from 177,000 MCP tools" (arXiv 2603.23802) | 177,436 public MCP tools | https://arxiv.org/pdf/2603.23802v1.pdf | KNOWN | Agent tool-ecosystem census. Relevant to infra-watchlist: MCP servers as agent infrastructure. |
| TrajectoryDB (arXiv 2609.07782) | vision paper, no dataset | https://arxiv.org/abs/2609.07782v1 | KNOWN | No artifact. Noted only. |
| AgentGUI (arXiv 2607.26300) | trajectory visualization | https://arxiv.org/abs/2607.26300v2 | KNOWN | Tooling for observing agent traces. Not a trace source. |

## Lane 2 — Artifact follow-through

Checked: WorkArena "Live Demo" = local script (no hosted artifact). openclaw-p2p live network (p2pclaw.com) and DeployBench demo (deploybench.vercel.app) are documented public betas — logged, not fetched (opsec). No eval harness found containing our marker grammars (uqscan/zz=oai/epoch-nonce search returned zero).

## Lane 3 — Appendix mining (pending — next sweep: pull appendices from Kang-lab papers for tool-definition grammars)

## Lane 4 — Preprint timeline (pending)

---

## Verdicts

| # | Paper / artifact | Class | Evidence |
|---|---|---|---|
| 1 | WorkArena / WorkArena++ (arXiv 2403.07718, 2407.05291) | KNOWN | Documented ServiceNow benchmark; "live demo" is local-only. No live trace. |
| 2 | OpenCLAW-P2P (arXiv 2604.19792), p2pclaw.com live network | KNOWN | Documented. Live agent network is a watch-worthy surface, not a new find. |
| 3 | DeployBench (arXiv 2606.05238), deploybench.vercel.app | KNOWN | Documented benchmark + demo. |
| 4 | Kang lab papers (2402.06664, 2404.08144, 2406.01637, 2403.02691) | KNOWN | Lane 4 provenance: Feb–Jun 2024 papers establishing autonomous agent web-operation TTPs. |
| 5 | WebCloak/LLMCrawlBench (IEEE S&P 2026) | KNOWN | Lane 4: documents LLM-scraper agent shape. |
| 6 | ADP Dataset V1 (1.3M trajectories) | KNOWN (dataset) | **Open thread:** cross-reference our markers against it. |
| 7 | "How are AI agents used? Evidence from 177,000 MCP tools" (arXiv 2603.23802) | KNOWN | Agent tool-ecosystem census; relevant to infra watchlist. |

## Null results
- **Marker grammars absent from literature:** `"uqscan"` / `"zz=oai"` return zero hits in papers/repos — our fleet's markers are operator-specific, not published techniques.
- **No undocumented live agent deployments found** in the paper sweep; all live demos traced to documented benchmarks.
- **arXiv API unreachable from VM** (timeouts) — used web search instead; noted for future sweeps.

## Open threads
1. ADP Dataset V1 (1.3M trajectories): check for uqscan/zz/epoch marker grammars.
2. Kang-lab paper appendices: mine tool definitions for grammar comparison vs our corpora.
3. p2pclaw.com: live agent network — monitor as a surface (not a paper find).
