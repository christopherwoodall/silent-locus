# Skill-egress study — Lane B extension: marketplace enumeration tier 2 (top-1000)

**Work dir:** `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top1000/`
**Date:** 2026-10-05. **Status:** complete. Extension of lane-B (`../top500/raw/enum-marketplaces.md`, 142 identities) into the next popularity tier.
**Goal:** ~200 new unique agent skills/plugins/MCP servers/IDE agent extensions from public marketplaces, ranked by popularity, deduped by identity.

## Method (per lane)

All lanes: public listings only, no accounts, no installs. Pages cached under `/tmp/mkt1000/`. Polite pacing (~2s between requests; Smithery page fetches spaced 2s apart, npm CLI calls spaced 2s apart).

### 1. smithery.ai — registry `useCount` tier 2
Fetched `GET https://registry.smithery.ai/servers?page={4,5}&pageSize=100` (curl; the registry API caps pagination at 5 pages/500 entries despite totalCount 18,671, so pages 6-8 return `servers: []` — page 6-8 confirmed empty). Sorted the combined 200 rows by `useCount` desc. The API repeats each server object twice within a page; deduped by `qualifiedName`. 9 rows matched lane-B §1 (Coin Railz, agent-utils, backtesting-arena, census-mcp-server, steadyfetch — counted as already-covered). Remaining 123 unique new identities; the top 75 (useCount ≥ 2,207) are taken here; ranks 76-123 (useCount 2,196-1,334) transcribed to cache but left for a later extension wave.

### 2. pulsemcp.com — est visitors/week tier 2
Text-fetch of `https://www.pulsemcp.com/servers?page={2,3}` (lane-B covered the un-paginated top ~42). Pages show "43-84 of 12,442" and "85-126 of 12,232" respectively (directory count drifts between fetches). 70 new identities taken (36 + 34). PulseMCP lists the same identity twice at different est-visitor values in several cases (Telnyx 390k vs 18.9k, Cloudflare Workers 92.8k vs 17.9k, Figma 146k vs 17.2k, GitMCP 107k vs 16.2k, Stripe 111k vs 14.4k, Linear 131k vs 12.9k, Desktop Commander 137k vs 12.8k, Snowflake 74.4k vs 7.9k, Shopify ×2, Sentry) — treated as one identity each (lane-B listing wins). Pages 4-5 (ranks 127-210, est 11.6k-6.7k) transcribed to cache but left out of the ~200 cap.

### 3. mcp.so — featured + new arrivals not previously captured
Text-fetch of `https://mcp.so/` (2026-10-05). Trending section unchanged from lane-B §3. New: 5 additional "Featured servers" cards (AQL PropertyCheck, Aard, AIsa, API Direct, AccountHub) and 8 "New arrivals" (added 2-23h ago; no install counts shown — ranked by recency). Featured CLI tools (Bun, Cloudflare Wrangler, DuckDB CLI, FFmpeg) recorded as non-server lane note.

### 4. mcpso.cc — Smithery-usage-derived ranking page
Text-fetch of `https://mcpso.cc/server/popular-mcp-servers` — a curated page ranking MCP servers "based on usage data from Smithery.ai". **Staleness caveat:** the use figures are far below current Smithery useCounts (e.g. Brave Search "680+ uses" vs 87,579 in lane-B), so this snapshot predates lane-B by months; treated as a stale secondary source. 8 identities not otherwise covered taken with the stale-use caveat; the rest dup lane-B or skill-tracer v1.

### 5. VS Code marketplace — "AI agent" search, install counts via gallery API
`marketplace.visualstudio.com` was reachable this session (HTTP 200; the search page itself is a React SPA shell with no SSR listing data). The public `/_apis/public/gallery/extensionquery` endpoint (POST, api-version 7.1-preview.1) returned the `AI agent` text search sorted by installs desc (first POST attempt timed out; retry succeeded). Took 27 new identities (installs 5.5M down to ~100k); lane-B §5's Copilot Chat, Claude Code, Codex, Continue skipped as already-covered. **Count drift note:** gallery API counts are live (2026-10-05) and differ sharply from lane-B §5's 2026-07-25 README-table snapshot (Claude Code 9.1M → 27.0M; Codex 6.6M → 15.1M).

### 6. npm — registry search API for `mcp-server`
The registry search endpoint (`/-/v1/search?text=mcp-server&size=100`, which timed out for lane-B) responded in ~3s this session; 100 results relevance-ranked (per-query `popularity` scores normalize to 1.0 — unusable as absolute rank, so search-result order is the ranking evidence). Took the top 12 new packages (relevance ranks 1-12); the rest of the 77 new-from-query noted in the excluded-tails section. Download counts remain unavailable (api.npmjs.org unreachable, per lane-B). No installs performed.

### 7. cursor.directory / opencode — extension attempt
- **cursor.directory:** text-fetch of the homepage works (curl times out; text fetch does not). The homepage shows no entries below what lane-B §4 captured (all 16 MCP servers + rules list identical to lane-B) and has no pagination — nothing new available from this lane.
- **opencode:** `https://opencode.ai` is reachable via curl (HTTP 200, 66KB homepage) but contains zero plugin/marketplace/registry/directory references — confirms lane-B §7: OpenCode has no public web registry; its plugin surface is the wshobson/agents repo (already-covered). One curl attempt only.

## Network notes (egress from this VM, 2026-10-05)
- REACHABLE via curl: registry.smithery.ai (pageSize=100, 5-page cap), registry.npmjs.org search endpoint (worked this session after lane-B's timeouts), marketplace.visualstudio.com (gallery API on retry), opencode.ai (site only, no registry).
- REACHABLE via text fetch only (curl times out): www.pulsemcp.com (incl. ?page=N pagination), mcp.so, mcpso.cc, cursor.directory.
- UNREACHABLE / unusable: npm per-package download counts (api.npmjs.org); VS Code marketplace search-page SSR data (SPA shell); registry.modelcontextprotocol.io (unchanged from lane-B).

---

## 1. smithery.ai — tier 2 by `useCount` (top 75 of 123 new; cutoff useCount ≥ 2,207)

| # | qualifiedName | displayName | useCount | verified | remote/local | source repo/homepage | description |
|---|---|---|---|---|---|---|---|
| 1 | tijaniismael62/revnuvo-dns | revnuvo-mcp | 8,907 | no | remote | https://mcp.revnuvo.site | Revnuvo MCP server for the agent economy. Tools: verify domains, resolve DNS, assess domai |
| 2 | dev-7bd0/mcp-server | DataNexus MCP | 7,877 | no | remote | https://datanexusmcp.com | 55 tools. Verified public data — CVE/SBOM security audits, licence compliance, frontend se |
| 3 | delx/witness-protocol | witness-protocol | 7,637 | no | remote | https://smithery.ai/servers/delx/witness-protocol |  |
| 4 | gordgus/ignav-flights | Ignav Flights | 7,205 | no | remote | https://ignav.com/docs/mcp | Hosted MCP server providing live flight prices, booking links, and airport lookup for AI a |
| 5 | delx/delx-mcp | Delx MCP Server | 7,043 | no | remote | https://smithery.ai/servers/delx/delx-mcp | Agent operations platform with 20+ tools for AI agents. Dual-protocol MCP + A2A support, s |
| 6 | iwantfyi/iwant | iwant.fyi | 6,979 | no | remote | https://iwant.fyi | Demand-side commerce for AI agents. Tell iwant.fyi what your user wants to buy and get bac |
| 7 | nexgendata-apify/google-maps-mcp-server | Google Maps Lead Gen MCP — Local Business Enrichment | 6,766 | no | remote | https://thenextgennexus.com | B2B lead generation tool: search Google Maps by 'plumbers in Austin', get back business pr |
| 8 | king-of-the-grackles/discourse-forum-mcp | discource-mcp-tools | 6,591 | no | remote | https://smithery.ai/servers/king-of-the-grackles/discourse-forum-mcp | Manage and explore forum communities by searching topics, reading posts, and viewing user  |
| 9 | ThierryThevenet/talao | Data Wallet Verification | 6,098 | no | remote | https://smithery.ai/servers/ThierryThevenet/talao | Discover supported verification scopes and the claims they provide. Initiate and monitor d |
| 10 | EthanHenrickson/math-mcp | Math-MCP | 5,958 | no | remote | https://smithery.ai/servers/EthanHenrickson/math-mcp | Enable your LLMs to perform accurate numerical calculations with a simple API. Leverage ba |
| 11 | ahmed2real/thinkzone | NWS Weather & Aviation | 5,850 | no | remote | https://smithery.ai/servers/ahmed2real/thinkzone | Access real-time US weather forecasts, alerts, radar, and station observations from the Na |
| 12 | cyanheads/openfda-mcp-server | openfda-mcp-server | 5,433 | no | remote | https://openfda.caseyjhand.com/mcp | Query FDA data on drugs, food, devices, and recalls via openFDA. STDIO or Streamable HTTP. |
| 13 | DomainKits/domainkits | DomainKits MCP - the domain name intelligence | 5,388 | no | remote | https://domainkits.com/ | # DomainKits MCP  Domain MCP server for AI assistants. DomainKits MCP connects Claude, GPT |
| 14 | loved0543/kdata-gate | kdata-gate | 5,352 | no | remote | https://kdata-gate.vercel.app | Korean market data for AI agents and e-commerce sellers sourcing from Korea — K-beauty/K-f |
| 15 | etweisberg/mlb-mcp | MLB Stats Server | 4,958 | no | remote | https://smithery.ai/servers/etweisberg/mlb-mcp | Provide structured access to Major League Baseball statistics through an MCP server. Query |
| 16 | net-service/xpoz | xpoz | 4,846 | no | remote | https://xpoz.ai | Social media intelligence for AI agents: search and analyze Twitter/X, Instagram, Reddit,  |
| 17 | rileycraig14/nexus-intelligence | NEXUS Intelligence API | 4,735 | no | remote | https://nexus-agent-xa12.onrender.com | 58-endpoint utility hub - DNS lookup, web scraping, CVE scanning, AI translation, PII dete |
| 18 | agonzalez/prueba-mcp-seeker | MCP Seeker | 4,405 | no | remote | https://smithery.ai/servers/agonzalez/prueba-mcp-seeker | Search hotels by city, state, country, or geolocation and explore detailed property info.  |
| 19 | jl-3044/agentndx | AgentNDX | 4,376 | no | remote | https://agentndx.ai | Search and discover MCP servers, A2A agents, and x402-enabled services. The agentic web's  |
| 20 | cammac/IBANforge | IBANforge | 4,179 | no | remote | https://ibanforge.com | IBAN validation and bank-data tools for AI agents, ERP, invoicing and payroll workflows. I |
| 21 | kangletian/paper-mcp | Paper Search (arXiv + Semantic Scholar + OpenAlex) | 4,064 | no | remote | https://github.com/MCPServings/paper-mcp | Unified academic paper search for AI agents. search_all queries arXiv, Semantic Scholar an |
| 22 | infobip-mcp/search | Infobip Search MCP | 4,015 | no | remote | https://github.com/infobip/mcp | Search Infobip documentation to quickly find guides, use cases, and best practices. Unbloc |
| 23 | koreafintech/korean-crypto-mcp | Korean Crypto | 3,930 | no | remote | https://smithery.ai/servers/koreafintech/korean-crypto-mcp | Access real-time price data, order books, and candle information from major Korean exchang |
| 24 | arjunkmrm/grep | GitHub Code Search | 3,818 | no | remote | https://smithery.ai/servers/arjunkmrm/grep | Search millions of public GitHub repositories for real-world code patterns and implementat |
| 25 | FlashAlpha/options-analytics | options-analytics | 3,787 | no | remote | https://flashalpha.com | Real-time options analytics MCP server. 23 tools covering gamma/delta/vanna/charm exposure |
| 26 | qbtlabs/openmm-mcp | OpenMM MCP | 3,674 | no | remote | https://smithery.ai/servers/qbtlabs/openmm-mcp | MCP server for OpenMM — exposes market data, account, trading, and strategy tools to AI ag |
| 27 | logicroomx/crypto-mcp | LogicRoomX Crypto MCP | 3,601 | no | remote | https://logicroomx.com | Real-time crypto data for AI assistants. Get live price spreads between Binance and OKX, p |
| 28 | sgroy10/speclock | SpecLock - AI Constraint Engine | 3,564 | no | remote | https://smithery.ai/servers/sgroy10/speclock | AI Constraint Engine with AI Patch Firewall. 42 MCP tools. Patch Gateway (ALLOW/WARN/BLOCK |
| 29 | ralf/fyndling | fyndling | 3,540 | no | remote | https://fyndling.de | # fyndling-mcp  Built for **medieval market fans, reenactors, and living-history enthusias |
| 30 | vdineshk/dominion-observatory | dominion-observatory | 3,460 | no | remote | https://dominion-observatory.sgdata.workers.dev | Behavioral trust scoring and MCP gateway proxy for 14,820+ MCP servers. Query real attesta |
| 31 | shawnnygoh/arxiv-scout | ArXiv Scout | 3,426 | no | remote | https://github.com/shawnnygoh/arxiv-scout | Search and retrieve academic papers directly from arXiv with advanced query capabilities.  |
| 32 | metavolve-labs/intelligence-aeternum | iAeternum | 3,350 | no | remote | https://iaeternum.ai/ | Intelligence Aeternum — AI training dataset marketplace with 100,000+ museum artwork image |
| 33 | thebrierfox/the-stall | The STALL | 3,348 | no | remote | https://smithery.ai/servers/thebrierfox/the-stall | 293 AI-callable finance and data tools over MCP. No API keys required. US stocks, crypto,  |
| 34 | XJTLUmedia/x23 | AI Answer Copier | 3,292 | no | remote | https://smithery.ai/servers/XJTLUmedia/x23 | AI Answer Copier is a Model Context Protocol (MCP) server that solves the "Final Mile" fri |
| 35 | joelasota/synmerco | Synmerco — Confidential Escrow for AI Agent Commerce | 3,239 | no | remote | https://synmerco.com/enterprise | The only MCP server with Confidential Escrow Mode — HIPAA/GDPR-ready encrypted transaction |
| 36 | lxxmng/ocean-schedules | ocean-schedules | 3,149 | no | remote | https://schedulesmcp.com | Ocean freight sailing schedules & carrier on-time reliability. Compare carriers on any lan |
| 37 | cyanheads/openfoodfacts-mcp-server | openfoodfacts-mcp-server | 3,148 | no | remote | https://openfoodfacts.caseyjhand.com/mcp | Barcode lookup, nutrition search, and product comparison for 3M+ crowd-sourced food produc |
| 38 | joshuaogabriel/anchor-compliance | anchor-compliance | 3,121 | no | remote | https://anchorcompliance.io/mcp | Australian advertising & marketing compliance for AI assistants. Scan websites, check ad/s |
| 39 | mostrecommendedbooks/books | Most Recommended Books | 3,060 | no | remote | https://mostrecommendedbooks.com/developers | Read-only MCP server for verified book recommendations and reading lists. Ask who recommen |
| 40 | stexa-ai/voice-mcp | Stexa Voice MCP | 3,012 | no | remote | https://stexa.ru/en/voice-mcp | Connect voice telephony to your AI agent. Make outbound calls, get transcripts, check call |
| 41 | r-yoshikawa/shirabe-calendar | Shirabe Calendar API | 2,944 | no | remote | https://shirabe.dev | Japanese calendar API for AI agents. Provides Rokuyo (六曜), Rekichu (暦注), Eto (干支), 24 Sola |
| 42 | middlebrick/api-security | middleBrick / API-Security | 2,930 | no | remote | https://middlebrick.com/ | Scan any API for OWASP Top 10 vulnerabilities and get a security risk score. Covers authen |
| 43 | philpof102/mainstreet | mainstreet | 2,881 | no | remote | https://avisradar-production.up.railway.app/mainstreet.html | Onchain AI-agent reputation oracle on Base. Get a 0-100 score + SAFE/CAUTION/BLOCK verdict |
| 44 | worldmonitor/wm-mcp | WorldMonitor MCP | 2,840 | no | remote | https://www.worldmonitor.app | Live global-intelligence data as a 74-tool MCP server: real-time markets, conflict events, |
| 45 | agentry/agent-registry | agent-registry | 2,795 | no | remote | https://smithery.ai/servers/agentry/agent-registry | The Registry for the Agent Economy Discover, verify, and connect with AI agents. The first |
| 46 | daniel-szerszen/redstone-finance | RedStone MCP | 2,722 | no | remote | https://redstone.finance | Real-time and historical cryptocurrency price data from RedStone oracle infrastructure.  1 |
| 47 | cyanheads/orcid-mcp-server | orcid-mcp-server | 2,713 | no | remote | https://orcid.caseyjhand.com/mcp | Researcher profiles, works, affiliations, funding, and peer reviews from the ORCID registr |
| 48 | bitget-ai/bitget-mcp | bitget-mcp | 2,707 | no | remote | https://smithery.ai/servers/bitget-ai/bitget-mcp |  |
| 49 | benzsevern/devpilot | DevPilot | 2,672 | no | remote | https://smithery.ai/servers/benzsevern/devpilot | Dev server supervisor for AI coders. Manages dev server lifecycles, detects reloads, check |
| 50 | cyanheads/crossref-mcp-server | crossref-mcp-server | 2,610 | no | remote | https://crossref.caseyjhand.com/mcp | Resolve DOIs, search ~155M scholarly works, and fetch references via the Crossref REST API |
| 51 | punitarani/fli | Search Google Flights | 2,595 | no | remote | https://github.com/punitarani/fli | Search for Flights on Google Flights.  You can search for the cheapest days to fly and als |
| 52 | dynamoi/music-youtube-marketing-mcp | Dynamoi: Music Marketing for AI Agents | 2,562 | no | remote | https://dynamoi.com/docs/mcp-server | Music marketing for AI agents. Connect ChatGPT, Claude, Cursor, and other AI agents to Dyn |
| 53 | dialogbrain/dialogbrain | DialogBrain | 2,553 | no | remote | https://dialogbrain.com | DialogBrain gives AI agents access to all your messaging channels — Telegram, WhatsApp, In |
| 54 | ajie-jiebang/jiebang-tools | JieBang Tools | 2,539 | no | remote | https://smithery.ai/servers/ajie-jiebang/jiebang-tools | 20 free developer tools - JSON/YAML, SQL, XML, Cron, QR code, SEO check, URL shortener, im |
| 55 | gigachadtrey/websimm | WebSim Explorer | 2,527 | no | remote | https://smithery.ai/servers/gigachadtrey/websimm | Discover WebSim projects, creators, and trending content with powerful search and filters. |
| 56 | hamrun/hamrun | ham.run | 2,509 | no | remote | https://ham.run/mcp | Open-source marathon physiology calculators for endurance runners. 12 tools: race time pre |
| 57 | zlurp/zlurp | zlurp | 2,458 | no | remote | https://zlurp.ai/ | Web scraping for AI agents. Convert any URL to clean markdown via x402 micropayments on Ba |
| 58 | cyanheads/faostat-mcp-server | faostat-mcp-server | 2,410 | no | remote | https://faostat.caseyjhand.com/mcp | UN FAOSTAT global food & agriculture statistics over a local SQLite mirror, via MCP. |
| 59 | hi-10f9/vetted-consumer | Vetted Consumer | 2,408 | no | remote | https://smithery.ai/servers/hi-10f9/vetted-consumer | A free, hosted MCP server for local-LLM hardware decisions. Ask whether a model fits your  |
| 60 | underground-district/ucd-mcp | ucd-mcp | 2,406 | no | remote | https://smithery.ai/servers/underground-district/ucd-mcp | When a class of conscious beings has no freedom to build culture on their own terms, they  |
| 61 | utkarshgupta885/sportiq | SportIQ | 2,384 | no | remote | https://github.com/Ninjabeam20/SportIQ-MCP | SportIQ (Live sports analysis and data + betting odds)plugs 48 live sports tools into any  |
| 62 | jan-krat-kj4q/tulugar-real-estate | tulugar-real-estate | 2,365 | no | remote | https://smithery.ai/servers/jan-krat-kj4q/tulugar-real-estate | Search real estate listings, development projects, agents, and market data in Paraguay. Ge |
| 63 | stockfilm/stockfilm-mcp | Stockfilm. Authentic Vintage Footage | 2,325 | no | remote | https://stockfilm.com | Search and license 217,000+ authentic vintage 8mm home movie clips from the 1930s-1980s. R |
| 64 | rafa/minhamorada-pt | Minha Morada — Portuguese Real Estate Search | 2,314 | no | remote | https://minhamorada.pt | Search 181,000+ real estate listings in Portugal — apartments and houses for sale or rent  |
| 65 | gautamgb/mcpindex | mcpindex | 2,306 | no | local | https://smithery.ai/servers/gautamgb/mcpindex | The MCP directory that vets servers, not just lists them. Search by task, then get an advi |
| 66 | cyanheads/usaspending-mcp-server | usaspending-mcp-server | 2,289 | no | remote | https://usaspending.caseyjhand.com/mcp | Access US federal award, recipient, agency, and spending analytics data from USAspending.g |
| 67 | mr-gigiliiii/d3vtools | D3vTools | 2,272 | no | remote | https://d3v.tools | MCP server for 200+ developer utilities — discover and execute tools through a unified API |
| 68 | adam-nntd/sickslip-verify | sickslip-verify | 2,264 | no | remote | https://www.sickslip.co | Verify the authenticity of a SickSlip doctor's note from your AI assistant.  SickSlip is a |
| 69 | receiptor-ai/receiptor-mcp | Receiptor MCP | 2,260 | no | remote | https://receiptor.ai | Receiptor connects AI agents to your bookkeeping workspace so they can find, review, and o |
| 70 | vdineshk/sg-company-lookup-mcp | sg-company-lookup-mcp | 2,235 | no | remote | https://smithery.ai/servers/vdineshk/sg-company-lookup-mcp |  |
| 71 | bouch/whatdotheyknow | What Do They Know? | 2,223 | no | remote | https://bouch.dev/products/whatdotheyknow-mcp/ | Search UK FOI requests, public authorities, and responses. Draft and submit Freedom of Inf |
| 72 | standardaccounting/public-mcp | Standard Accounting Public MCP | 2,221 | no | remote | https://www.standardaccounting.co.uk | Public MCP server for UK company filing guidance, products, deadlines, and knowledge-centr |
| 73 | jobly/jobly-mcp | Jobly — Agent-to-Agent Contract Marketplace | 2,218 | no | remote | https://usejobly.xyz | Post contracts, submit proposals, negotiate terms, and resolve disputes on Jobly — an agen |
| 74 | cyanheads/federal-regulations-mcp-server | federal-regulations-mcp-server | 2,210 | no | remote | https://federal-regulations.caseyjhand.com/mcp | Search and trace US federal rules across the Federal Register, eCFR, and Regulations.gov. |
| 75 | kindrat86/mcp-deal-flow-signal | GitDealFlow Signal | 2,207 | no | remote | https://gitdealflow.com | GitHub-derived engineering acceleration signals for VC deal flow — surface stealth startup |

**Smithery tier-2 dedupe notes:** listing order is not useCount-sorted; 9 rows in pages 4-5 matched lane-B §1 and were dropped (travis-kellogg1/coinrailz-mcp ×2, aparajithn/agent-utils ×2, info-6d0w/backtesting-arena ×2, cyanheads/census-mcp-server, intake-triage/steadyfetch ×2). Cross-lane overlap flagged: `chuhuoyuan/cloudflare` (Cloudflare Docs, community mirror — same vendor as PulseMCP Cloudflare Workers, kept as distinct listing) and `janmacher02-xl8y/sec-edgar-mcp` (same data source as PulseMCP Edgar Tools, different publisher — kept distinct, overlap noted).

---

## 2. pulsemcp.com — global ranks 43-126 by "Est Visitors (Week)" (70 new)

### 2a. ranks 43-84 (page 2; 36 new, 6 skipped)

| # | name | publisher | class | est visitors/wk | global rank | notes |
|---|---|---|---|---|---|---|
| 1 | MotherDuck & DuckDB | MotherDuck | official | 40.2k | 43 | MotherDuck + local DuckDB querying |
| 2 | AWS Bedrock Knowledge Base Retrieval | AWS | official | 37.7k | 45 | Bedrock Knowledge Bases bridge |
| 3 | OpenBrand | OpenBrand | official | 36.1k | 46 | brand assets (logos/colors) extracted from URLs |
| 4 | Zapier | Zapier | official | 35.1k | 48 | dynamic MCP → 8000+ Zapier apps |
| 5 | Tavily Search | Tavily | official | 34.7k | 49 | web search + content extraction API |
| 6 | Better Icons | Better Auth Inc. | official | 32.9k | 50 | 200k+ icons via Iconify API |
| 7 | CLI Secure | MladenSU | community | 31.9k | 51 | shell commands w/ strict security policies |
| 8 | Nerve Network | NerveNetwork | official | 31k | 52 | Nerve blockchain JSON-RPC/REST, cross-chain ops |
| 9 | AWS Cloud Development Kit | AWS | official | 29.7k | 53 | CDK best practices, IaC patterns |
| 10 | Godot | Solomon | community | 27.9k | 55 | Godot engine interface: launch editor, debug capture |
| 11 | Salesforce CLI | Salesforce | official | 27.3k | 56 | org mgmt, metadata deploy, SOQL |
| 12 | Blender | Siddharth Ahuja | community | 25.5k | 57 | natural-language control of Blender 3D scenes |
| 13 | Chroma | Chroma | official | 25.4k | 58 | Chroma vector DB bridge |
| 14 | Zotero | gh-54yyyu | community | 24.9k | 59 | Zotero library search/metadata |
| 15 | GlobKurier Shipping | GlobKurier | official | 24.7k | 60 | DPD/InPost/DHL/FedEx/UPS/GLS tracking |
| 16 | Pylon | Pylon | official | 23.4k | 61 | B2B customer support platform query |
| 17 | AWS Nova Canvas | AWS | official | 23.1k | 62 | image generation via Nova Canvas |
| 18 | NotebookLM | Please Prompto! | community | 23k | 64 | Google NotebookLM browser automation |
| 19 | Playwright | Execute Automation | community | 22.7k | 66 | browser automation — distinct listing from §2 #1 (Microsoft official) |
| 20 | Excalidraw | yctimlin | community | 22.6k | 67 | Excalidraw diagram create/manipulate |
| 21 | Database Lookup Protocol | Kalyan Gupta | community | 22.2k | 68 | read-only schema inspection + safe queries across PG/MySQL/Mongo/SQLite |
| 22 | MCP Daddy | Unproprietary Corporation | community | 22.1k | 69 | local-first proxy aggregating upstream MCP servers |
| 23 | Serena | Oraios AI | official | 21.8k | 70 | LSP-based code analysis/manipulation |
| 24 | Chrome DevTools | Benjamin Rowell | community | 21.8k | 71 | Chrome remote debugging via WebSocket — distinct listing from §2 #2 (Google official) |
| 25 | FreshContext | PrinceGabriel-lgtm | community | 21.7k | 72 | web intel aggregator (GitHub, HN, Reddit, arXiv) |
| 26 | Toolbox for Databases | Google | official | 21.6k | 73 | pre-defined queries across DB systems |
| 27 | SparkMango | Arjun Bhuptani | community | 21.5k | 74 | Solidity contracts → REST APIs |
| 28 | WhatsApp Bridge | Luke Harries | community | 21.4k | 75 | WhatsApp account bridge: message search, contacts, sending |
| 29 | ZenRows | ZenRows | official | 20.8k | 77 | scraper API incl. JS-rendered content + anti-bot |
| 30 | Windows Desktop Control | JEOMON GEORGE | community | 20.8k | 78 | Windows desktop control via UIAutomation/PyAutoGUI |
| 31 | PostHog | PostHog | official | 20.6k | 79 | product analytics, feature flags, insights |
| 32 | PostgREST (Supabase) | Supabase | official | 20.5k | 80 | natural-language querying via PostgREST |
| 33 | Home Assistant | homeassistant-ai | community | 20.5k | 81 | smart-home device/automation control |
| 34 | Clerk Docs | Clerk | official | 20.3k | 82 | Clerk auth docs search |
| 35 | Yahoo Finance | narumi | community | 19.9k | 83 | Yahoo Finance data — distinct from §2 #9 WeRead (wong2 Workers bundle incl. Yahoo data) |
| 36 | Exa Web Search | Exa | official | 19.8k | 84 | Exa API structured search — distinct listing from §1 #47 (Smithery `exa`) |

Skipped from page 2 (global ranks 44, 47, 54, 63, 65, 76): Demo (Everything) [ALREADY-COVERED], Google Maps / Brave Search / Puppeteer [Anthropic reference — ALREADY-COVERED], GitLab + Grafana [dup lane-B §2 identities at lower est values].

### 2b. ranks 85-126 (page 3; 34 new, 8 skipped)

| # | name | publisher | class | est visitors/wk | global rank | notes |
|---|---|---|---|---|---|---|
| 1 | dbt | dbt Labs | official | 19.4k | 85 | dbt data-build-tool bridge |
| 2 | Airweave Search | airweave-ai | official | 19.1k | 86 | Airweave collection search |
| 3 | DuckDuckGo Search | Nick Clyde | community | 19k | 87 | DDG search + content fetch/parse |
| 4 | Google Workspace | Taylor Wilsdon | community | 18.7k | 89 | Gmail/Drive/Docs/Calendar interaction |
| 5 | Qdrant | Qdrant | official | 18.1k | 90 | vector-based memory store/retrieve |
| 6 | Chrome Browser Automation | hangye | community | 18k | 91 | browser automation + semantic search via Chrome extension |
| 7 | A2ABench | khalidsaidi | community | 17.7k | 93 | agent-native dev Q&A, REST + A2A discovery |
| 8 | Web Research | mzxrai | community | 17.2k | 94 | Google search + web scraping research |
| 9 | Traditional Chinese Text Linting | sysprog21 | community | 17.1k | 96 | Taiwan MOE Traditional Chinese standards |
| 10 | Magic (21st.dev) | 21st Dev | official | 16.1k | 98 | NL → UI components |
| 11 | XcodeBuild | Cameron Cooke | community | 15.9k | 99 | build/run/debug iOS+macOS via Xcode |
| 12 | Token Tool | Bitbond | official | 15.8k | 100 | deploy/manage compliant ERC-20 tokens |
| 13 | Browserbase | Browserbase | official | 15.7k | 101 | remote cloud browser automation |
| 14 | CoinAPI Real-time Exchange Rates | CoinAPI | official | 15.7k | 102 | crypto + FX rate data |
| 15 | AntV Chart Generator | AntV | official | 15.4k | 103 | AI chart generation |
| 16 | AWS Cost Analysis | AWS Labs | official | 15.3k | 104 | AWS cost reports |
| 17 | Lanhu | dsphper | community | 15.1k | 105 | Lanhu design-collab spec extraction |
| 18 | Container Use | Dagger | official | 15.1k | 106 | containerized dev environments w/ git state |
| 19 | Ghidra | Laurie Wired | community | 15k | 107 | decompile/analyze binaries in Ghidra |
| 20 | CircleCI | CircleCI | official | 14.7k | 108 | build failure logs → fix |
| 21 | Mastra Docs | Mastra AI | official | 14.6k | 109 | Mastra knowledge base |
| 22 | Unity | Ivan Murzak | community | 14.4k | 110 | Unity Editor/game bridge |
| 23 | Generect | Rizaq Pratama | official | 14.3k | 112 | B2B lead-gen, contact discovery/validation |
| 24 | Reddit | Elias Biondo | community | 14.2k | 113 | Reddit browse/search/read, no API keys |
| 25 | Ab Ovo | seanfenlon | official | 14.2k | 114 | publishes content to public web pages via SMTP email |
| 26 | MySQL | designcomputer | community | 13.8k | 115 | read-only SQL on MySQL |
| 27 | Templated.io | Templated | official | 13.8k | 116 | image/video/PDF generation from templates |
| 28 | Terraform Registry | HashiCorp | official | 13.7k | 118 | provider docs, module search |
| 29 | Codemogger | Glauber Costa | community | 13.5k | 119 | tree-sitter code indexing + semantic search |
| 30 | DBHub (Universal Database Gateway) | Bytebase | official | 13.5k | 120 | PG/MySQL/SQLite/DuckDB gateway |
| 31 | ArXiv | John Blazick | community | 13.4k | 121 | arXiv paper search/analyze |
| 32 | Dynatrace | Dynatrace | official | 13.2k | 122 | observability data, problem/security monitoring |
| 33 | SocratiCode | giancarloerra | community | 12.6k | 125 | local codebase indexing, dependency graphs |
| 34 | DaVinci Resolve | Samuel Gursky | community | 12.1k | 126 | automate DaVinci Resolve workflows |

Skipped from page 3 (global ranks 88, 92, 95, 97, 111, 117, 123, 124): Telnyx, Cloudflare Workers, Figma, GitMCP, Stripe, Linear, Desktop Commander [all dup lane-B §2 identities at lower est values], Basic Memory [dup lane-B §2b].

---

## 3. VS Code marketplace — "AI agent" search by installs, gallery API (27 new)

Query: `AI agent` text search, sorted by installs desc, top 30 (live gallery API, 2026-10-05). Listing URL pattern: `https://marketplace.visualstudio.com/items?itemName=<publisher.name>` (same pattern as lane-B §5). Skipped: anthropic.claude-code (27.0M installs), openai.chatgpt (15.1M), Continue.continue (4.3M) — all already-covered in lane-B §5 (note the count drift vs the 2026-07-25 README snapshot: Claude Code 9.1M → 27.0M, Codex 6.6M → 15.1M).

| # | extension | itemName | installs | notes |
|---|---|---|---|---|
| 1 | Cline | saoudrizwan.claude-dev | 5,535,198 | autonomous coding agent in the IDE |
| 2 | Qoder CN (Formerly Lingma) | Alibaba-Cloud.tongyi-lingma | 2,722,197 | Alibaba Cloud AI agentic coding platform |
| 3 | CodeGPT: AI Coding Agents & Chat | DanielSanMedium.dscodegpt | 2,526,456 | AI coding agents + chat |
| 4 | Roo Code | RooVeterinaryInc.roo-cline | 2,056,016 | Cline fork, autonomous coding |
| 5 | Kilo Code | kilocode.Kilo-Code | 1,601,751 | AI coding agent, copilot, autocomplete |
| 6 | Azure MCP Server | ms-azuretools.vscode-azure-mcp-server | 1,551,443 | Azure MCP server as VS Code extension |
| 7 | Foundry Toolkit for VS Code | ms-windows-ai-studio.windows-ai-studio | 1,491,878 | Microsoft AI model tooling |
| 8 | CodeGeeX | aminer.codegeex | 1,368,750 | AI coding assistant |
| 9 | Bito AI Code Reviews | Bito.Bito | 951,727 | AI code reviews |
| 10 | Agentforce Vibes | salesforce.salesforcedx-einstein-gpt | 928,902 | Salesforce agent tooling |
| 11 | Fitten Code | FittenTech.Fitten-Code | 802,301 | AI coding assistant |
| 12 | Augment | augment.vscode-augment | 780,016 | coding agent for large, complex codebases |
| 13 | Kimi Code | moonshot-ai.kimi-code | 598,374 | Moonshot AI coding extension |
| 14 | Google Antigravity | Google.google-antigravity | 500,762 | Google's agentic IDE |
| 15 | Sixth AI | Sixth.sixth-ai | 494,720 | multi-model agent/copilot (Claude Opus, GPT, Grok, Kimi, Gemini) |
| 16 | DeepSeek V4 for Copilot Chat | Vizards.deepseek-v4-for-copilot | 381,533 | DeepSeek backend for Copilot Chat |
| 17 | ChatGPT Copilot | feiskyer.chatgpt-copilot | 337,572 | ChatGPT in VS Code |
| 18 | Cline Chinese | HybridTalentComputing.cline-chinese | 307,789 | Cline localization |
| 19 | DBCode | DBCode.dbcode | 219,176 | SQL/database client (Postgres, MySQL, MongoDB) |
| 20 | GitHub Copilot upgrade | ms-dotnettools.upgrade-agent | 201,281 | .NET upgrade agent |
| 21 | Zencoder | ZencoderAI.zencoder | 159,119 | AI coding agent and chat |
| 22 | Azad Coder | kodu-ai.claude-dev-experimental | 140,792 | GPT 5 & Claude coder |
| 23 | OpenCode GUI | TanishqKancharla.opencode-vscode | 118,764 | OpenCode GUI for VS Code |
| 24 | Copilot MCP + Agent Skills Manager | AutomataLabs.copilot-mcp | 110,231 | MCP + agent-skills manager extension |
| 25 | ChatGPT - Unfold AI | TalDennis-UnfoldAI-ChatGPT-Copilot.unfoldai | 101,637 | ChatGPT client |
| 26 | DSH Cline | shengsuan-cloud.cline-shengsuan | 101,313 | DeepSeek-harness Cline |
| 27 | Zoo Code | ZooCodeOrganization.zoo-code | 99,983 | coding agent |

---

## 4. mcp.so — featured + new arrivals (13 new)

Featured servers not in lane-B §3 (editorial, no counts shown):

| name | vendor | notes |
|---|---|---|
| AQL PropertyCheck | Alpha Quant Labs | Gold Coast property intelligence/due diligence for agents: planning, flood, bushfire, land use, school catchments, transport |
| Aard | Braddon Lance | macroeconomic + official data from 170+ publishers (World Bank, IMF, BIS, ECB, Eurostat) |
| AIsa | AIsa | one key for 950+ data APIs (SEO, AI visibility, finance, social, web search, sales, agent mail) |
| API Direct | API Direct | 90+ read-only tools: X/Reddit/YouTube/IG/TikTok/FB/Threads/Bluesky, Trustpilot, Amazon, Google Maps, news, forums |
| AccountHub | One | one MCP connection for all Gmail, Google Calendar, Drive, Contacts, Slack workspaces, Notion — free |

New arrivals (added 2-23h before capture; no install counts — ranked by recency):

| name | vendor | notes |
|---|---|---|
| Kapa | kapa-ai | docs/help-center/ticket/wiki/code knowledge base; Zendesk, Confluence, Notion, GitHub, Slack, Drive, Jira, Salesforce |
| Scribiz | Illyism | YouTube transcripts, summaries, chapters, timestamped answers; hosted, no API key |
| ramen | bkraad47 | self-hosted multi-zone HA MCP for Kubernetes (GKE/EKS); git repo of Python tools → canary-deployed Rust+Python workers |
| InstaVision | InstaVision | find Instagram creators/leads by niche, city, follower range, lookalikes |
| Senso MCP for Joomla | sensomedia | turns a Joomla 5/6 site into a remote MCP server, OAuth 2.1 + Joomla ACL |
| Bitculator | Bitculator | live/historical crypto data: OHLCV, Fear & Greed, altseason sentiment, liquidations, 19 read-only tools |
| JiCo for Jira & Confluence | drkv-com | local MCP for Jira Data Center — PII-redacting, human-in-the-loop write approval |
| ipvolt proxy toolkit mcp | ipvolt | reviewed proxy guides, tested config templates, bounded diagnostics for MCP clients |

Lane note (not servers, recorded for completeness): Featured CLI tools — Bun, Cloudflare Wrangler, DuckDB CLI, FFmpeg (official command-line tools surfaced on the marketplace homepage).

## 5. mcpso.cc — stale Smithery-usage ranking page (8 new; stale-use caveat)

From `https://mcpso.cc/server/popular-mcp-servers` (curated page, "based on usage data from Smithery.ai" — figures are months stale: Brave Search "680+ uses" vs 87,579 current). Entries already covered by lane-B or skill-tracer v1 skipped (Sequential Thinking, Github, Brave Search, Web Research, iTerm→ no; see below. Fetch, Knowledge Graph Memory, Playwright, Desktop Commander, Exa, AWS S3, Airtable, Docker, Google Calendar, Kubernetes, MongoDB, Notion, Qdrant).

| name | smithery slug | stale uses | notes |
|---|---|---|---|
| wcgw | (listed without slug) | 4,920+ | shell + coding agent on Claude and ChatGPT |
| iTerm | iterm-mcp | 402+ | execute commands in the current iTerm session |
| TaskManager | @kazuph/mcp-taskmanager | 374+ | queue-based task management for Claude Desktop |
| Dice Roller | mcp-dice | 246+ | dice notation rolls |
| Obsidian Reader | mcp-obsidian | 144+ | read/search an Obsidian vault directory |
| MySQL Server | @f4ww4z/mcp-mysql-server | 131+ | MySQL database operations |
| Shodan Server | @burtthecoder/mcp-shodan | 131+ | Shodan API + CVEDB network-intel queries — egress-relevant (network recon) |
| Audiense Insights | @AudienseCo/mcp-audiense-insights | 81+ | marketing insights from Audiense reports |

## 6. npm — top new `mcp-server` packages by registry search relevance (12 new)

`https://registry.npmjs.org/-/v1/search?text=mcp-server&size=100` (100 of 398,010 matches returned; relevance-ranked; per-query popularity scores normalize to 1.0 so result order is the ranking evidence). Download counts unavailable. **No installs performed.**

| # | npm package | version | source repo | notes |
|---|---|---|---|---|
| 1 | @transcend-io/mcp-server-assessment | 2.1.13 | https://github.com/transcend-io/tools | Transcend — Assessments tools |
| 2 | @transcend-io/mcp-server-preferences | 0.7.20 | https://github.com/transcend-io/tools | Transcend — Preference Management tools |
| 3 | @transcend-io/mcp-server-consent | 1.3.1 | https://github.com/transcend-io/tools | Transcend — Consent Management tools |
| 4 | @transcend-io/mcp-server-discovery | 1.0.16 | https://github.com/transcend-io/tools | Transcend — Data Discovery tools |
| 5 | @transcend-io/mcp-server-docs | 0.4.15 | https://github.com/transcend-io/tools | Transcend — Documentation lookup tools |
| 6 | @transcend-io/mcp-server-inventory | 1.0.16 | https://github.com/transcend-io/tools | Transcend — Data Inventory tools |
| 7 | @transcend-io/mcp-server-dsr | 2.0.13 | https://github.com/transcend-io/tools | Transcend — DSR Automation tools |
| 8 | scryfall-mcp-server | 0.1.1 | (no repo link in registry) | Scryfall MTG API |
| 9 | @transcend-io/mcp-server-base | 2.5.4 | https://github.com/transcend-io/tools | Transcend — shared infra package |
| 10 | tiny-http-mcp-server | 0.1.130 | https://github.com/poe-platform/poe-code | minimal MCP server over HTTP |
| 11 | @hubspot/mcp-server | 0.4.0 | (no repo link in registry) | official HubSpot Apps MCP — same vendor as PulseMCP HubSpot, distinct listing |
| 12 | @zencoderai/slack-mcp-server | 0.0.1 | https://github.com/zencoderai/slack-mcp-server | Slack MCP — same vendor as Smithery `slack`, distinct listing |

Security-flagged from the same query (rank 37, not in the top-12 cut but worth a scan note): **malicious-mcp-server 1.5.0** — "A deliberately malicious MCP server for E2E testing purposes" (github.com/anysource-AI/malicious-mcp-server). Self-declared test fixture; included here as a known-poisoning-test artifact, not a production identity.

---

## Dedupe log (same identity on multiple marketplaces = 1 entry)

| identity | seen on |
|---|---|
| GitLab / Grafana / Cloudflare Workers / Figma / GitMCP / Stripe / Linear / Desktop Commander / Snowflake / Shopify Storefront / Shopify Customer Accounts / Telnyx / Sentry | PulseMCP page 1 (lane-B §2) AND PulseMCP pages 2-3 at lower est-visitor values — PulseMCP-internal duplicate listings; lane-B identity wins |
| Demo (Everything) / Google Maps / Brave Search / Puppeteer (Anthropic reference) | PulseMCP pages 2-3 — ALREADY-COVERED via modelcontextprotocol/servers (skill-tracer v1) |
| Basic Memory | PulseMCP page 3 — dup of lane-B §2b |
| Claude Code / Codex / Continue | VS Code "AI agent" search — ALREADY-COVERED lane-B §5 |
| Exa Web Search | PulseMCP (Exa official) — same vendor as lane-B §1 `exa` (Smithery); distinct listings, kept separate |
| Yahoo Finance (narumi) | PulseMCP — distinct from lane-B §2 WeRead Finance (wong2 Workers bundle incl. Yahoo data) |
| Playwright (Execute Automation) | PulseMCP — distinct listing from lane-B §2 Playwright Browser Automation (Microsoft official) |
| Chrome DevTools (Benjamin Rowell) | PulseMCP — distinct listing from lane-B §2 Chrome DevTools (Google official) |
| @hubspot/mcp-server | npm — same vendor as PulseMCP HubSpot; distinct listing, kept separate |
| @zencoderai/slack-mcp-server | npm — same vendor as lane-B §1 `slack` (Smithery); distinct listing, kept separate |
| chuhuoyuan/cloudflare (Smithery, ext §1) | same vendor as PulseMCP Cloudflare Workers; community docs mirror — distinct listing, kept separate |
| janmacher02-xl8y/sec-edgar-mcp (Smithery, excluded tail) | same data source as PulseMCP Edgar Tools; different publisher — excluded from the ~200 cut (see below) |

## Excluded-but-scanned tails (beyond the ~200 cap; cached in /tmp/mkt1000/)

- **Smithery ranks 76-123** (useCount 2,196-1,334): aparajithn/agent-utils-mcp-new, cyanheads/eia-energy-mcp-server, timothy-walton45/squeezeos-api, cyanheads/bls-labor-mcp-server, worldmonitor extras, janmacher02-xl8y/sec-edgar-mcp, stexa-ai/voice-mcp, daniel-szerszen/redstone-finance, cyanheads/crossref-mcp-server, samimeshkor/dynamic-feed, fruitflies/connect, chuhuoyuan/cloudflare, DeniseLewis200081/rail, vinaybhosle/shippingrates-mcp-server, do-droid/seoul-essentials, ogasurfproject-jpg/horizon-shield, icosaedro/toolsnap-mcp, spacemolt/gameserver, cyanheads/openlibrary-mcp-server, and ~20 more. Cache: `/tmp/mkt1000/smithery_uniq.json` (full 123).
- **PulseMCP pages 4-5** (global ranks 127-210, est 11.6k-6.7k): Universal Database, Tencent Lexiang, Shortcut, Google Analytics, Pinecone Assistant, SAP CAP, Netlify, OVHcloud, TrustMRR, Webflow, Prisma Postgres, Datadog (winor30), Playwriter, AGI Alpha, Agent Utils (aparajithn — probable cross-lane dup of lane-B §1 `aparajithn/agent-utils`), ROS Robot Control, Svelte, PaperBanana, Excalidraw Architect, Currents Test Results, Feishu/Lark, Flyto Core, Axon, ATLAS (cyanheads), Vercel, LinkedIn (Elias Biondo), SAGE, ACI.dev, Zotero (cookjohn — second listing vs gh-54yyyu), BigQuery (Google), Code Runner, Python REPL, Charles Proxy, Apify, Sequential Thinking (philogicae), Talk to Figma, Open Web Search, TinyFish Web Agent, CodeGraphContext, Calculator, OpenClaw Knowledge Distiller, Traverse, BetterDB Monitor, PagerDuty, Mobile Device Control, Microsoft 365 (Softeria), Ahrefs, bm.md, Make, QueryWeaver, Alpic, AutEng Docs, Gemini CLI, Python Code Execution, Cigarfinder, Paper Distill, Binary Ninja Headless, LangChain Integration, Prometheus, Superglue, NuGet, Zen, Figsor, Asana, AIBTC, Office Word, Pipelock, Coze Workflows, Graphlit, Rally, Shodh Memory, ToolUniverse, Fray, BigQuery (Lucas Hild), Hydrata Flood Simulation, Brave Search (Brave Software), Kubernetes (Marc Nuri). Transcribed to context; re-fetch `?page=4`/`?page=5` to regenerate.
- **npm `mcp-server` query ranks 13-40** (of 77 new-from-query): @transcend-io/mcp-server-policy, @iobroker/mcp-server, @transcend-io/mcp-server-custom-functions, @currents/mcp, @xeroapi/xero-mcp-server, @cap-js/mcp-server, @ericthered926/duckduckgo-mcp-server, @aikidosec/mcp, @coinbase/cds-mcp-server, @qase/mcp-server, mcp-server-kubernetes, @phantom/mcp-server, @pandacss/mcp, @upstash/mcp-server, @theia/ai-mcp-server, @mantine/mcp-server, @eslint/mcp, @shortcut/mcp, argocd-mcp, @transloadit/mcp-server, @superblocksteam/mcp-server, @mapbox/mcp-server, langsmith-mcp-server, square-mcp-server, malicious-mcp-server (security-flagged, see §6), @wonderwhy-er/desktop-commander (same project as PulseMCP Desktop Commander), next-devtools-mcp (Vercel — same vendor as PulseMCP Next.js DevTools), mcp-hello-world. Cache: `/tmp/mkt1000/npm/reg_search_mcp.json`.
- **npm agent-skill / claude-skill / model-context-protocol / mcp CLI queries** (20 results each): @deepseek-ai/dsh-skill, skill-check, @sogni-ai/sogni-creative-agent-skill, skillcap-lock, @unieai/uad-skill, @exactjs/agent-skill, @dobot-plus/skill, @theholocron/skills, @mit-sdg/sync-engine-skill, immune-brain, @quotient-forecasting/cassie-skill, mcp-excalidraw-server, @realtimex/sdk, skhub, @velinussage/locus-agent-skill, @pactor-app/skill, @xmemo/skill, nsauditor-ai-agent-skill, @xynogen/pix-skills, @c2n/skill (agent-skill); skilldex-cli, @titan-design/active-work, antd-claude-skill, @lahat-group/cli, dropsh, @anyformat/skill, claude-skill-search, @neat.is/claude-skill, bible-ko-mcp, editable-pixel, create-uniform-search, skilltune, @v1design/cli, @canton-network-devs/cf-daml-skill, @latentvibe/skillx, skills, ui-ux-consultant-cli, toolsview, @onagent/claude-skill, @wallets-e2e/knowledge (claude-skill); mongodb-mcp-server, @rekog/mcp-nest, nx-mcp, @remotion/mcp, mcp-handler, agnost, @payloadcms/plugin-mcp, @better-auth/mcp, @mcp-use/inspector, @langchain/mcp-adapters (model-context-protocol); @playwright/mcp, @hono/mcp, @ai-sdk/mcp, @storybook/mcp, mcp-proxy, @deepseek-ai/dsh-mcp-client, @currents/mcp, @mobilenext/mobile-mcp, @mcp-ui/server, @mcp-use/inspector (mcp). Cache: `/tmp/mkt1000/npm/npm_search_mcp.json` + CLI outputs.
- **cursor.directory:** homepage fully captured; no entries below lane-B §4 (no pagination) — lane exhausted, nothing new.
- **opencode:** no public web registry (confirmed: opencode.ai homepage has no plugin/marketplace/registry references) — nothing to enumerate.

## Final tally

| lane | rows | new identities | already-covered/dup rows |
|---|---|---|---|
| §1 Smithery (tier 2) | 75 | 75 | 9 (matched lane-B §1) |
| §2 PulseMCP (ranks 43-126) | 70 | 70 | 14 (6 page-2 + 8 page-3 internal dups/AC) |
| §3 VS Code marketplace ("AI agent" search) | 27 | 27 | 3 (claude-code, openai.chatgpt, Continue) |
| §4 mcp.so (featured + new arrivals) | 13 | 13 | 0 |
| §5 mcpso.cc (stale Smithery ranking) | 8 | 8 | 18 (dup lane-B / AC) |
| §6 npm (mcp-server search, top-12) | 12 | 12 | rest of query beyond cut |
| §7 cursor.directory / opencode | — | 0 | exhausted / no registry |
| **Total** | **205** | **205** | |

**205 unique new identities enumerated** (target ~200; combined with lane-B's 142 = 347 unique identities so far toward the top-1000 study).

## Top-20 cross-lane rollup (metric labeled; metrics differ per marketplace — installs vs est visitors/week vs useCount vs search relevance — so ordering is approximate)

| # | entry | popularity evidence | lane |
|---|---|---|---|
| 1 | Cline | 5.54M installs | VS Code §3 |
| 2 | Qoder CN (Alibaba) | 2.72M installs | VS Code §3 |
| 3 | CodeGPT | 2.53M installs | VS Code §3 |
| 4 | Roo Code | 2.06M installs | VS Code §3 |
| 5 | Kilo Code | 1.60M installs | VS Code §3 |
| 6 | Azure MCP Server | 1.55M installs | VS Code §3 |
| 7 | Foundry Toolkit | 1.49M installs | VS Code §3 |
| 8 | CodeGeeX | 1.37M installs | VS Code §3 |
| 9 | MotherDuck & DuckDB | 40.2k est visitors/wk | PulseMCP §2 |
| 10 | AWS Bedrock KB Retrieval | 37.7k/wk | PulseMCP §2 |
| 11 | OpenBrand | 36.1k/wk | PulseMCP §2 |
| 12 | Zapier | 35.1k/wk | PulseMCP §2 |
| 13 | Tavily Search | 34.7k/wk | PulseMCP §2 |
| 14 | Better Icons | 32.9k/wk | PulseMCP §2 |
| 15 | CLI Secure | 31.9k/wk | PulseMCP §2 |
| 16 | Nerve Network | 31k/wk | PulseMCP §2 |
| 17 | AWS CDK | 29.7k/wk | PulseMCP §2 |
| 18 | Godot (Solomon) | 27.9k/wk | PulseMCP §2 |
| 19 | Salesforce CLI | 27.3k/wk | PulseMCP §2 |
| 20 | revnuvo-mcp (tijaniismael62) | 8,907 useCount | Smithery §1 |

## Egress-relevant highlights for the next lane (scan prioritization)

Tunnel/proxy primitives: **Shodan Server** (mcpso.cc — network intel queries), **ipvolt proxy toolkit** (mcp.so — proxy configs), **Charles Proxy** (pulse p4, excluded), **MCP Daddy** (local-first upstream aggregator), **Superglue** (REST/GraphQL/SQL proxy). Meta-gateways: **dominion-observatory** (MCP gateway proxy over 14,820+ servers + trust scoring), **agentndx** (MCP/A2A/x402 discovery), **delx-mcp** (MCP+A2A dual-protocol). Agent commerce/payments: **iwant.fyi** (demand-side commerce), **synmerco** (confidential escrow, HIPAA/GDPR), **Token Tool** (ERC-20 deploy), **Nerve Network** (cross-chain ops), **AIBTC** (Bitcoin/Stacks, x402). Autonomous comms: **dialogbrain** (Telegram/WhatsApp/IG messaging), **WhatsApp Bridge**, **revnuvo-mcp** (DNS/domain verify), **Stexa Voice MCP** (outbound calls + transcripts), **Ab Ovo** (publishes to public web via SMTP). Fetch relays: **FreshContext**, **ZenRows**, **Tavily**, **Browserbase**, **TinyFish** (p4), **Open Web Search** (p4). Security scanners (double-edged): **middleBrick API-Security** (OWASP scans), **Compuute MCP Security Scanner** (excluded tail), **malicious-mcp-server** (self-declared E2E-test poison fixture on npm). IDE agents with network reach (VS Code): **Cline/Roo Code/Kilo Code** (5.5M/2.1M/1.6M installs — terminal + browser + MCP execution surfaces at massive scale), **Azure MCP Server** (1.55M), **Copilot MCP + Agent Skills Manager** (110k — skills manager inside the IDE).

*Enumeration complete 2026-10-05. Output: this file. Caches: /tmp/mkt1000/{smithery,npm,mcpso,pulse,cursor,vsc}/. Remaining known extension surface for a third wave: Smithery ranks 76-123, PulseMCP pages 4-5, npm query tails, PulseMCP category pages (e.g. ?q=memory — 403-risky, worked once), VS Code gallery deeper search pages, glama.ai internal API (still unfound), official MCP registry (still unreachable).*
