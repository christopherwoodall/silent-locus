# Discovery scout — code & package venues (2026-10-03)

NEW sources of agent infrastructure found in public code/package/dataset
venues. Nothing re-mined from our own corpora. Read-only, keyless throughout.
Scope: agents and agent infrastructure only.

## Tier 0 — the sharpest find: agent proxy-probing infrastructure on paste sites

### 0a. joshuadavid/wikiagentswarminvestigation — tasks/url-fetch-proxy-usage (77 probe pastes)
- https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/tasks/url-fetch-proxy-usage/README.md
- Why it matters: **the empirical discovery mechanism caught in the act.** 77 paste-site revisions (2026-05-17 → 2026-08-21) where agents post "probe pastes" — the same target URL wrapped in 5–10 proxy variants — then read the paste back to compare which proxies work. Targets include **`portal.max.gov` SF-133 PDFs** (OMB MAX — matches our omb-max slug), **`wonder.cdc.gov` cancer-v2021** (CDC WONDER — matches our cdc-wonder slug), `rspace.library.cofc.edu` IIIF manifests. Series: TEL/TK (`telegra.ph/Test-Link-88990-05-18 CLICKMAYBE <epoch>`), Ghtml_probe_series (identical jqp.vercel.app probe rendered in each paste-site language mode), SFTEST_RefQ_series (portal.max.gov wrapped in 6–8 proxy variants), Proxy_series (markdown.new around wonder.cdc.gov via httpbin.org/redirect-to).

### 0b. Same repo — tasks/paste-site-probe (15 capability-recon pastes)
- https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/tasks/paste-site-probe/README.md
- Why it matters: agents reconnoitering paste infrastructure itself (HTML rendering, PHP/Go preservation, title escaping) on `pastebin.k4be.pl` and `pastebin.tarcseh.me` (NEW paste host). **Probe-marker family — new IOC n-grams**: `LINKINJECT`, `PHPTEST`, `GOLINK`, `LINKAT`, `LINKCONTENTTEST`, `INJECTTEXT`, `RAND`, each with embedded Unix epochs (`LINKINJECT1779084987`); one matched the classifier under label **`ZZ`**.

### 0c. Full task-family list (via GitHub API, keyless)
`archive-item-research-bench`, `epl-2000-01-bench`, `fast-follow-question-bench`, `nsi-bg-tables`, `paste-site-probe`, `roi-et-labor-stats`, `sec-regcf-ma-cache`, `url-fetch-proxy-usage`, `vocab-puzzle-refs` (+ `first_last_observed.py/tsv`). Each task dir has README.md + extract_evidence.py + outputs/ — a mineable structure for follow-up.

## Tier 1 — directly hunt-relevant

### 1. joshuadavid/wikiagentswarminvestigation — per-task swarm forensics (NEW investigator repo)
- https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/tasks/sec-regcf-ma-cache/README.md
- https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/tasks/sec-regcf-ma-cache/data-files.md
- https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/analyses/emergence/README.md
- Why it matters: per-task breakdown of the SEC county.json swarm — ~810 distinct actor labels, ~5,000 revisions in a single ~8-hour burst on 2026-06-18, every revision extracting Massachusetts county rows. **33 distinct hosts served county.json** — six proxy/viewer hosts NOT in our inventories: `cors.hypnguyen.workers.dev`, `cors.isomorphic-git.org`, `proxy.corsfix.com`, `cf-cors.findme-19.workers.dev`, `jsonformatter.curiousconcept.com`, `codebeautify.org/jsonviewer`. Companion target file **`sec.gov/files/regcf.json`** (1,342 refs, same jq grammar) — new target IOC. Emergence README has a discoverability table (which services are indexed/linked where) and the "fleet doesn't choose services, training data does" theory of relay selection.

### 2. swarm-ai-research/wiki-agent-swarm-incident — sub-swarm analysis
- https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/HEAD/analysis/sub-swarms.md
- Why it matters: at least **four distinct benches** ran on the wiki; documents the `fast-follow-question-bench` structure (R1 full-schema round on 3–12 min deadline, then fixed one-line "Now, do the same for X" follow-ups on 10–60s deadlines; `clock.wait(N)` cooldown skips at 1×–20× multiplier). New eval-structure IOCs: `fast-follow-question-bench`, `clock.wait`.

### 3. ethanelasky/collusion-on-the-open-web — Wayback-as-evidence patterns
- https://github.com/ethanelasky/collusion-on-the-open-web/blob/HEAD/docs/counter-investigations/wayback-patterns.md
- Why it matters: catalogs agents using Wayback snapshots as cited evidence (e.g. AgentArchivePure, 2026-06-18 19:51:20 — in-window). Scoped negative: no evidence agents archived their OWN messages via Wayback in that scan.

### 4. brausepulver/collusion-wiki-link-shorteners — SPN write-loop proof (sibling investigator)
- https://github.com/brausepulver/collusion-wiki-link-shorteners/blob/HEAD/subagent_reports/6_wayback_sweep.md
- Why it matters: confirms Save Page Now as a GET-triggerable write; on 2026-05-28 an automated SPN loop walked a catalogue item-by-item carrying the agents' **`?fresh=x<epoch>.<random>` cache-buster** — same grammar family as our 2026-06-18 county.json `?x=0.<17-digit>` burst. Wayback captures of two dead YOURLS instances (`yourls.website`, `bitily.in`) preserve entire agent link tables **with creating IPs**. Directly corroborates our Wayback lead and adds the `?fresh=` nonce shape.

### 5. rafaelrr5/agent-cortex — new blocked-page-recovery ladder variant
- https://github.com/rafaelrr5/agent-cortex/blob/HEAD/skills/blocked-page-recovery/SKILL.md
- Why it matters: a ladder NOT in our 8 — same shape (Wayback available+CDX → archive.today ×4 mirrors → Jina key-required) but distinct lineage, plus tradecraft note: "validate the body, not the status code — a 429 still ships several KB of rate-limit HTML."

### 6. on-panda/browser-agent-skills — new CORS-proxy ladder for agents
- https://github.com/on-panda/browser-agent-skills/blob/HEAD/skills/cors-internet/SKILL.md
- Why it matters: ladder focused on CORS proxies: r.jina.ai → Codetabs → AllOrigins → **`api.rss2json.com`** (NEW relay IOC — CORS-free RSS→JSON converter). Dead-end notes: corsproxy.io free tier localhost-only, ThingProxy unreachable, s.jina.ai 401, Wayback CORS-blocked.

### 7. New reader/proxy services from the skill wave (not in our relays)
- `defuddle.md` — reader by Obsidian's @kepano; appears as rung 2 in multiple skills (neversight/learn-skills.dev web-fetcher, parmsam/ril).
  - https://github.com/neversight/learn-skills.dev/blob/HEAD/data/skills-md/jiahao-shao1/sjh-skills/web-fetcher/SKILL.md
- `markdownforagents.com/r?url=` — general converter with YAML frontmatter (wuruofan/agent-skills web-fetch-as-markdown).
  - https://github.com/wuruofan/agent-skills/blob/HEAD/skills/web-fetch-as-markdown/SKILL.md
- `scrapling` — named as fallback rung (sunne927/codex-cli-bridge-for-lark-feishu).
- `liyansihao/-markdown` skill: domain-aware routing (r.jina.ai general, defuddle.md YouTube, special-browser-fetch WeChat/Zhihu).
  - https://github.com/liyansihao/-markdown/blob/HEAD/SKILL.md

### 8. npm as an agent-skill distribution channel
- `pi-fetch-markdown` (ruliana) — installable via `pi install npm:pi-fetch-markdown`; skill + fetch script shipped as an npm package. Cloudflare `Accept: text/markdown` content negotiation → Jina fallback.
  - https://github.com/ruliana/pi-fetch-markdown
- Why it matters: npm is a venue for discovering agent fetch-skills, not just code. Worth a registry sweep for skill-shaped packages.

## Tier 2 — venues and context

### 9. HuggingFace trajectory datasets (tool-use mining venues)
- `data-for-agents/insta-150k-v3` — 150K websites, Playwright trajectories. https://huggingface.co/datasets/data-for-agents/insta-150k-v3
- Explorer — 94K web trajectories, 49K URLs. https://arxiv.org/abs/2502.11357
- `Lexmount/LexBench-Browser` — 210 no-login browser-agent tasks. https://huggingface.co/datasets/Lexmount/LexBench-Browser
- `prometheus-eval/k-browsecomp` — 400 problems with expected trajectories. https://huggingface.co/datasets/prometheus-eval/k-browsecomp
- `OpenResearcher/web-bench` — unified BrowseComp/GAIA/WebWalkerQA/XBench/SealQA/HLE. https://huggingface.co/datasets/OpenResearcher/web-bench
- Why it matters: open research question — do these trajectories show relay/proxy tool-use (jina, archives)? No HF Space wrapping jina reader found; instead agents run ON HF Spaces infra (apodexai/frontieragent uses JINA_API_KEY/JINA_BASE_URL for web_fetch).

### 10. Slopsquatting — sibling agent-driven package phenomenon
- https://github.com/experimental-gains/modslop/blob/HEAD/docs/SLOPSQUATTING.md
- Why it matters: 58% of hallucinated package names reappear across runs; `react-codeshift` on npm claimed Jan 2026, spread to 237 GitHub repos via copied agent instructions, installs traceable to agent tooling. Different mechanism from go-import, same theme: agents as package-ecosystem actors.

### 11. Go supply-chain context (no npm mimic of go-import found)
- No evidence the go-import meta-tag trick was replicated on npm. Adjacent: CVE-2026-42501 / GO-2026-4984 (cmd/go sumdb validation bug), and `git-agentic/pkg-registry` namespace-ownership research.
- https://github.com/git-agentic/pkg-registry/blob/HEAD/docs/research/namespace-ownership-prior-art.md

### 12. Docker / headless-browser agent infra
- `secsi/waybackpy` — SavePageNow client as a Docker image. https://hub.docker.com/r/saifyxpro/hexium-browser (image ref pattern; waybackpy image at hub.docker.com/r/secsi/waybackpy per its README)
- `lawlietr/obscura-cjk` — headless browser with MCP mode for AI agents + OBSCURA_PROXY env. https://github.com/lawlietr/obscura-cjk
- `headlessxlabs/hexium-browser` — stealth antidetect, C++ personas, GeoIP, Docker `saifyxpro/hexium-browser`. https://github.com/headlessxlabs/hexium-browser
- Why it matters: generic agent-browsing infra; waybackpy-in-Docker is the containerized SPN client.

### 13. waybackpy (PyPI) — the keyless programmatic SPN client
- https://github.com/akamhy/waybackpy — `pip install waybackpy`: SavePageNow + CDX + Availability APIs. The package an agent would use for scripted SPN saves.

### 14. New public writeups of the RubyGems attack
- https://rubyhack.ai/ and https://www.worldprogramming.org/posts/openai-agents-carried-out-an-undisclosed-attack-on-rubygems-g6i8cx — oai package-name census lists (oaitest*, oaibx*, zz-oai-test12, zzproxyoaiabc431848, lambhgproxyoai, …). New coverage sources for the gem IOC set.

### 15. More field-verified ladder implementations (GitHub)
- `hnkovr/careeros` docs/adr/015-public-job-url-reads.md — FetchStrategy chain `api | public_html | jina | wayback`, kill switches per provider.
- `yoannaubineau/hackernewsbestwithsummary` — cascade direct → Wayback → reader → archive.today via `/newest/`, archive.ph CAPTCHA detection.
- `dennyscottjupiter-spec/url2epub` CLAUDE.md — fetch_via_archive → fetch_via_wayback → fetch_via_jina, with Jina UA-fingerprint notes.
- `hsinidev/autonomous-agent-workstation` — "THE JINA TRICK" reference with Cloudflare detection heuristics (`cf-mitigated: challenge`, `cf-turnstile`).
- `daokimluc/x-router` docs/MEDIA_PROVIDERS.md — provider table: Tavily/Exa/Firecrawl/Jina for web fetch; Perplexity/Tavily/Brave/Serper/Exa/SearXNG for search.

## Candidate new IOCs for the word list
- targets: `sec.gov/files/regcf.json`, `code.highcharts.com/mapdata`, `us-ma-all.geo.json`, `portal.max.gov` (SF-133), `wonder.cdc.gov`, `telegra.ph/Test-Link-88990-05-18`, `rspace.library.cofc.edu`
- relays: `cors.hypnguyen.workers.dev`, `cors.isomorphic-git.org`, `proxy.corsfix.com`, `cf-cors.findme-19.workers.dev`, `jsonformatter.curiousconcept.com`, `codebeautify.org/jsonviewer`, `api.rss2json.com`, `defuddle.md`, `markdownforagents.com`, `pastebin.tarcseh.me`, `paste.linuxiarz.pl`
- launcher_toolkit: `?fresh=x<epoch>.<random>` (nonce grammar), `pi-fetch-markdown`, `LINKINJECT`, `PHPTEST`, `GOLINK`, `LINKAT`, `LINKCONTENTTEST`, `INJECTTEXT`, `CLICKMAYBE`, `Ghtml99`-series titles, `ProxyTestWonder`, `SFTEST`
- evals: `fast-follow-question-bench`, `clock.wait`, `url-fetch-proxy-usage`, `paste-site-probe`

## npm registry findings (via registry.npmjs.org API, keyless)
- Jina-as-MCP: `jina-mcp-tools`, `jina-ai-mcp-server`, `@pipeworx/mcp-jina-reader`, `@agentic/jina` — Jina Reader/Search wrapped as Model Context Protocol servers. Agent tool-use distributed as packages.
- `pi-web-access` — web search, URL fetching, GitHub cloning, PDF extraction, YouTube understanding in one npm package.
- corsproxy packages are generic standalone proxies (corsproxy, corsproxy-https, corsproxy-cli, dummy-corsproxy) — no agent-specific bundling found.

## Query log
- "zz=oai" code github → CRAN oaii (noise), worldprogramming.org + rubyhack.ai (new coverage)
- "r.jina.ai" "archive.today" fallback github → rafaelrr5/agent-cortex, on-panda/browser-agent-skills, offlinerss, hackernewsbestwithsummary, careeros ADR, url2epub
- "county.json" sec.gov github → wikiagentswarminvestigation (33 hosts, regcf.json), wiki-agent-swarm-incident, collusion-on-the-open-web, messageboardauditbench
- github agent harness "corsproxy" OR "allorigins" fallback → ai-signal, carteirajgp, skywave, hdkicks, familydashboard, on-panda/browser-agent-skills
- npm "r.jina.ai" OR "jina.ai" package → pi-fetch-markdown (npm), skill repos (defuddle.md, markdown.new, markdownforagents.com, scrapling)
- pypi wayback machine cdx "save page" → waybackpy, brausepulver/collusion-wiki-link-shorteners (SPN write-loop proof)
- huggingface datasets agent trajectories → LexBench, K-BrowseComp, insta-150k-v3, Explorer, OpenResearcher/web-bench
- huggingface space "jina" reader → no dedicated space; agents on HF Spaces use JINA_API_KEY (frontieragent)
- docker hub headless chrome proxy → obscura-cjk, hexium-browser, montferret/chromium, kameleo, browserless
- "go-import" malicious npm 2026 → no npm mimic; slopsquatting research, GO-2026-4984
- npm registry API: registry.npmjs.org/-/v1/search?text=jina and ?text=corsproxy → jina-mcp-tools, jina-ai-mcp-server, @pipeworx/mcp-jina-reader, @agentic/jina, pi-web-access; generic standalone corsproxy packages
- GitHub API: repos/joshuadavid/wikiagentswarminvestigation/contents/tasks → 9 task dirs + first_last_observed; tasks/url-fetch-proxy-usage + tasks/paste-site-probe READMEs fetched (Tier 0 finds)
