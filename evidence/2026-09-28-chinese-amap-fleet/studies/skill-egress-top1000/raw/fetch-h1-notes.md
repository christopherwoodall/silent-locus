# FETCH-MKT-1 — fetch log (lane-h1, top-1000 marketplace extension)

Subagent session 63580e94-0297-4507-8db1-4e7ba9ff0c6f · 2026-10-05.
Work dir: `~/workspace/skill-egress-work-1000/lane-h1/` (scratch; NOT `~/workspace/skill-egress-work/` which belongs to the top-500 study).
Source lists: `../silent-locus/data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top1000/raw/enum-marketplaces-ext.md` §1 (smithery.ai, 75) + §2 (pulsemcp.com, 70).

## Method

- Smithery: only entries whose enumeration row carried a public GitHub repo were fetched. `remote: true` listings are vendor-hosted with no public source → NO SOURCE (same convention as top-500 lane-E scan-c). Clones: `git clone --depth 1`, sequential, ~2s pacing; subdir `<owner>-<repo>` lowercased.
- PulseMCP: enumeration rows carry no repo links, so per-entry resolution was attempted: (1) npm registry search API (`/-/v1/search?text=<name> mcp`), accept only when the package's `links.repository` pointed at a GitHub repo whose owner plausibly matched the publisher (same login or same official org); (2) one GitHub repo-search API call (`<name> mcp in:name`), same acceptance rule. Rejected matches (community fork of an official listing, unrelated product) were dropped rather than fetched — a wrong repo would poison the scan attribution. Raw resolution outputs: `/tmp/pulse_npm_resolve.json`, `/tmp/pulse_gh_resolve.json`.
- Repos already staged in the top-500 lane (`~/workspace/skill-egress-work/lane-e/`) were NOT re-cloned; recorded as COVERED.
- Static staging only: shallow clones, no installs, nothing executed.

## Fetch log

| # | marketplace entry | source fetched | how | status |
|---|---|---|---|---|
| S-1 | tijaniismael62/revnuvo-dns (Smithery, 8,907 uses) | — | — | NO SOURCE: remote-only (mcp.revnuvo.site) |
| S-2 | dev-7bd0/mcp-server (Smithery, 7,877) | — | — | NO SOURCE: remote-only (datanexusmcp.com) |
| S-3 | delx/witness-protocol (Smithery, 7,637) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-4 | gordgus/ignav-flights (Smithery, 7,205) | — | — | NO SOURCE: remote-only (ignav.com/docs/mcp) |
| S-5 | delx/delx-mcp (Smithery, 7,043) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-6 | iwantfyi/iwant (Smithery, 6,979) | — | — | NO SOURCE: remote-only (iwant.fyi) |
| S-7 | nexgendata-apify/google-maps-mcp-server (Smithery, 6,766) | — | — | NO SOURCE: remote-only (thenextgennexus.com) |
| S-8 | king-of-the-grackles/discourse-forum-mcp (Smithery, 6,591) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-9 | ThierryThevenet/talao (Smithery, 6,098) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-10 | EthanHenrickson/math-mcp (Smithery, 5,958) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-11 | ahmed2real/thinkzone (Smithery, 5,850) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-12 | cyanheads/openfda-mcp-server (Smithery, 5,433) | — | — | NO SOURCE: remote-only (openfda.caseyjhand.com/mcp) |
| S-13 | DomainKits/domainkits (Smithery, 5,388) | — | — | NO SOURCE: remote-only (domainkits.com; description mentions GitHub but no repo link) |
| S-14 | loved0543/kdata-gate (Smithery, 5,352) | — | — | NO SOURCE: remote-only (kdata-gate.vercel.app) |
| S-15 | etweisberg/mlb-mcp (Smithery, 4,958) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-16 | net-service/xpoz (Smithery, 4,846) | — | — | NO SOURCE: remote-only (xpoz.ai) |
| S-17 | rileycraig14/nexus-intelligence (Smithery, 4,735) | — | — | NO SOURCE: remote-only (nexus-agent-xa12.onrender.com) |
| S-18 | agonzalez/prueba-mcp-seeker (Smithery, 4,405) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-19 | jl-3044/agentndx (Smithery, 4,376) | — | — | NO SOURCE: remote-only (agentndx.ai) |
| S-20 | cammac/IBANforge (Smithery, 4,179) | — | — | NO SOURCE: remote-only (ibanforge.com) |
| S-21 | kangletian/paper-mcp (Smithery, 4,064) | MCPServings/paper-mcp → `mcpservings-paper-mcp/` | git shallow clone (enum-listed repo) | FETCHED |
| S-22 | infobip-mcp/search (Smithery, 4,015) | infobip/mcp → `infobip-mcp/` | git shallow clone (enum-listed repo) | FETCHED |
| S-23 | koreafintech/korean-crypto-mcp (Smithery, 3,930) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-24 | arjunkmrm/grep (Smithery, 3,818) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-25 | FlashAlpha/options-analytics (Smithery, 3,787) | — | — | NO SOURCE: remote-only (flashalpha.com) |
| S-26 | qbtlabs/openmm-mcp (Smithery, 3,674) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-27 | logicroomx/crypto-mcp (Smithery, 3,601) | — | — | NO SOURCE: remote-only (logicroomx.com) |
| S-28 | sgroy10/speclock (Smithery, 3,564) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-29 | ralf/fyndling (Smithery, 3,540) | — | — | NO SOURCE: remote-only (fyndling.de) |
| S-30 | vdineshk/dominion-observatory (Smithery, 3,460) | — | — | NO SOURCE: remote-only (dominion-observatory.sgdata.workers.dev) |
| S-31 | shawnnygoh/arxiv-scout (Smithery, 3,426) | shawnnygoh/arxiv-scout → `shawnnygoh-arxiv-scout/` | git shallow clone (enum-listed repo) | FETCHED |
| S-32 | metavolve-labs/intelligence-aeternum (Smithery, 3,350) | — | — | NO SOURCE: remote-only (iaeternum.ai) |
| S-33 | thebrierfox/the-stall (Smithery, 3,348) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-34 | XJTLUmedia/x23 (Smithery, 3,292) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-35 | joelasota/synmerco (Smithery, 3,239) | — | — | NO SOURCE: remote-only (synmerco.com/enterprise) |
| S-36 | lxxmng/ocean-schedules (Smithery, 3,149) | — | — | NO SOURCE: remote-only (schedulesmcp.com) |
| S-37 | cyanheads/openfoodfacts-mcp-server (Smithery, 3,148) | — | — | NO SOURCE: remote-only (openfoodfacts.caseyjhand.com/mcp) |
| S-38 | joshuaogabriel/anchor-compliance (Smithery, 3,121) | — | — | NO SOURCE: remote-only (anchorcompliance.io/mcp) |
| S-39 | mostrecommendedbooks/books (Smithery, 3,060) | — | — | NO SOURCE: remote-only (mostrecommendedbooks.com/developers) |
| S-40 | stexa-ai/voice-mcp (Smithery, 3,012) | — | — | NO SOURCE: remote-only (stexa.ru/en/voice-mcp) |
| S-41 | r-yoshikawa/shirabe-calendar (Smithery, 2,944) | — | — | NO SOURCE: remote-only (shirabe.dev) |
| S-42 | middlebrick/api-security (Smithery, 2,930) | — | — | NO SOURCE: remote-only (middlebrick.com) |
| S-43 | philpof102/mainstreet (Smithery, 2,881) | — | — | NO SOURCE: remote-only (avisradar-production.up.railway.app) |
| S-44 | worldmonitor/wm-mcp (Smithery, 2,840) | — | — | NO SOURCE: remote-only (www.worldmonitor.app) |
| S-45 | agentry/agent-registry (Smithery, 2,795) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-46 | daniel-szerszen/redstone-finance (Smithery, 2,722) | — | — | NO SOURCE: remote-only (redstone.finance) |
| S-47 | cyanheads/orcid-mcp-server (Smithery, 2,713) | — | — | NO SOURCE: remote-only (orcid.caseyjhand.com/mcp) |
| S-48 | bitget-ai/bitget-mcp (Smithery, 2,707) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-49 | benzsevern/devpilot (Smithery, 2,672) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-50 | cyanheads/crossref-mcp-server (Smithery, 2,610) | — | — | NO SOURCE: remote-only (crossref.caseyjhand.com/mcp) |
| S-51 | punitarani/fli (Smithery, 2,595) | punitarani/fli → `punitarani-fli/` | git shallow clone (enum-listed repo) | FETCHED |
| S-52 | dynamoi/music-youtube-marketing-mcp (Smithery, 2,562) | — | — | NO SOURCE: remote-only (dynamoi.com/docs/mcp-server) |
| S-53 | dialogbrain/dialogbrain (Smithery, 2,553) | — | — | NO SOURCE: remote-only (dialogbrain.com) |
| S-54 | ajie-jiebang/jiebang-tools (Smithery, 2,539) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-55 | gigachadtrey/websimm (Smithery, 2,527) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-56 | hamrun/hamrun (Smithery, 2,509) | — | — | NO SOURCE: remote-only (ham.run/mcp) |
| S-57 | zlurp/zlurp (Smithery, 2,458) | — | — | NO SOURCE: remote-only (zlurp.ai) |
| S-58 | cyanheads/faostat-mcp-server (Smithery, 2,410) | — | — | NO SOURCE: remote-only (faostat.caseyjhand.com/mcp) |
| S-59 | hi-10f9/vetted-consumer (Smithery, 2,408) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-60 | underground-district/ucd-mcp (Smithery, 2,406) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-61 | utkarshgupta885/sportiq (Smithery, 2,384) | Ninjabeam20/SportIQ-MCP → `ninjabeam20-sportiq-mcp/` | git shallow clone (enum-listed repo) | FETCHED |
| S-62 | jan-krat-kj4q/tulugar-real-estate (Smithery, 2,365) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-63 | stockfilm/stockfilm-mcp (Smithery, 2,325) | — | — | NO SOURCE: remote-only (stockfilm.com) |
| S-64 | rafa/minhamorada-pt (Smithery, 2,314) | — | — | NO SOURCE: remote-only (minhamorada.pt) |
| S-65 | gautamgb/mcpindex (Smithery, 2,306, local) | — | — | SKIPPED: repo `github.com/gautamgb/mcpindex` not found (one attempt; 404) |
| S-66 | cyanheads/usaspending-mcp-server (Smithery, 2,289) | — | — | NO SOURCE: remote-only (usaspending.caseyjhand.com/mcp) |
| S-67 | mr-gigiliiii/d3vtools (Smithery, 2,272) | — | — | NO SOURCE: remote-only (d3v.tools) |
| S-68 | adam-nntd/sickslip-verify (Smithery, 2,264) | — | — | NO SOURCE: remote-only (www.sickslip.co) |
| S-69 | receiptor-ai/receiptor-mcp (Smithery, 2,260) | — | — | NO SOURCE: remote-only (receiptor.ai) |
| S-70 | vdineshk/sg-company-lookup-mcp (Smithery, 2,235) | — | — | NO SOURCE: remote-only (smithery listing) |
| S-71 | bouch/whatdotheyknow (Smithery, 2,223) | — | — | NO SOURCE: remote-only (bouch.dev/products/whatdotheyknow-mcp/) |
| S-72 | standardaccounting/public-mcp (Smithery, 2,221) | — | — | NO SOURCE: remote-only (www.standardaccounting.co.uk) |
| S-73 | jobly/jobly-mcp (Smithery, 2,218) | — | — | NO SOURCE: remote-only (usejobly.xyz) |
| S-74 | cyanheads/federal-regulations-mcp-server (Smithery, 2,210) | — | — | NO SOURCE: remote-only (federal-regulations.caseyjhand.com/mcp) |
| S-75 | kindrat86/mcp-deal-flow-signal (Smithery, 2,207) | — | — | NO SOURCE: remote-only (gitdealflow.com) |
| P-1 | MotherDuck & DuckDB (PulseMCP, 40.2k/wk) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-2 | AWS Bedrock Knowledge Base Retrieval (PulseMCP, 37.7k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-3 | OpenBrand (PulseMCP, 36.1k) | — | — | SKIPPED: npm `openbrand-mcp` matched ethanjyx/openbrand but owner does not match publisher "OpenBrand" (official) — dropped as unverified |
| P-4 | Zapier (PulseMCP, 35.1k) | — | — | FAILED: npm `@zapier/zapier-sdk-mcp` → gitlab.com/zapier/zapier-sdk; public `git clone` failed ("could not read Username") — auth-gated, public-repo rule forbids proceeding |
| P-5 | Tavily Search (PulseMCP, 34.7k) | tavily-ai/tavily-mcp (lane-E) | — | COVERED: already staged in top-500 lane-E (`~/workspace/skill-egress-work/lane-e/`); GitHub-search hit `apappascs/tavily-search-mcp-server` rejected as community fork |
| P-6 | Better Icons (PulseMCP, 32.9k) | — | — | SKIPPED: npm match `torkay/better-icons8-mcp` — owner mismatch vs publisher "Better Auth Inc." (official); dropped |
| P-7 | CLI Secure (PulseMCP, 31.9k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-8 | Nerve Network (PulseMCP, 31k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-9 | AWS Cloud Development Kit (PulseMCP, 29.7k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-10 | Godot (PulseMCP, 27.9k) | — | — | SKIPPED: npm `@npgamedev/godot-mcp-server` matched NPGameDev/godot-mcp-server but owner does not match publisher "Solomon"; dropped |
| P-11 | Salesforce CLI (PulseMCP, 27.3k) | — | — | SKIPPED: GitHub-search hit `deadanddani/MCPs_for_Salesforce_CLI` — community repo, publisher is Salesforce (official); dropped |
| P-12 | Blender (PulseMCP, 25.5k) | — | — | SKIPPED: npm `blender-mcp-enhanced` has no repository link; no GitHub match |
| P-13 | Chroma (PulseMCP, 25.4k) | chroma-core/chroma-mcp → `chroma-core-chroma-mcp/` | git shallow clone (GitHub search; official org chroma-core matches publisher) | FETCHED |
| P-14 | Zotero (PulseMCP, 24.9k) | — | — | SKIPPED: npm `@xbghc/zotero-mcp` owner mismatch vs publisher "gh-54yyyu"; dropped |
| P-15 | GlobKurier Shipping (PulseMCP, 24.7k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-16 | Pylon (PulseMCP, 23.4k) | — | — | SKIPPED: npm `pylon-mcp` owner JustinBeckwith mismatch vs publisher "Pylon" (official); dropped |
| P-17 | AWS Nova Canvas (PulseMCP, 23.1k) | — | — | SKIPPED: GitHub-search hit `yunwoong7/aws-nova-canvas-mcp` — community repo, publisher AWS (official); dropped |
| P-18 | NotebookLM (PulseMCP, 23k) | PleasePrompto/notebooklm-mcp → `pleaseprompto-notebooklm-mcp/` | git shallow clone (npm metadata; owner == publisher "Please Prompto!") | FETCHED |
| P-19 | Playwright (PulseMCP, 22.7k, Execute Automation) | microsoft/playwright-mcp (lane-E) | — | COVERED: already staged in top-500 lane-E (repo was renamed from playwright-mcp-server) |
| P-20 | Excalidraw (PulseMCP, 22.6k) | — | — | SKIPPED: npm `excalidraw-mcp` has no repository link; no GitHub match |
| P-21 | Database Lookup Protocol (PulseMCP, 22.2k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-22 | MCP Daddy (PulseMCP, 22.1k) | — | — | SKIPPED: GitHub-search hit `alpnix/GoDaddy-MCP` — wrong product (GoDaddy ≠ MCP Daddy); dropped |
| P-23 | Serena (PulseMCP, 21.8k) | — | — | SKIPPED: npm `serena-slim` owner mcpslim mismatch vs publisher "Oraios AI" (official); dropped |
| P-24 | Chrome DevTools (PulseMCP, 21.8k) | — | — | SKIPPED: npm `chrome-devtools-axi` owner kunchenguid mismatch vs publisher "Benjamin Rowell"; dropped |
| P-25 | FreshContext (PulseMCP, 21.7k) | PrinceGabriel-lgtm/freshcontext-mcp → `princegabriel-lgtm-freshcontext-mcp/` | git shallow clone (GitHub search; owner == publisher) | FETCHED |
| P-26 | Toolbox for Databases (PulseMCP, 21.6k) | — | — | SKIPPED: GitHub-search hit `shubhamgoogle/mcp-toolbox-for-databases-implementation` — community, publisher Google (official); dropped |
| P-27 | SparkMango (PulseMCP, 21.5k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-28 | WhatsApp Bridge (PulseMCP, 21.4k) | — | — | SKIPPED: GitHub-search hit `W3JDev/whatsapp-bridge-mcp` — owner mismatch vs publisher "Luke Harries"; dropped |
| P-29 | ZenRows (PulseMCP, 20.8k) | ZenRows/zenrows-mcp → `zenrows-zenrows-mcp/` | git shallow clone (npm metadata; official org matches publisher) | FETCHED |
| P-30 | Windows Desktop Control (PulseMCP, 20.8k) | — | — | SKIPPED: npm `@melpc/windows-desktop-control` has no repository link; no GitHub match |
| P-31 | PostHog (PulseMCP, 20.6k) | — | — | SKIPPED: npm `@posthog/mcp` lists repository `PostHog/posthog-js` (ambiguous package location); dropped |
| P-32 | PostgREST (PulseMCP, 20.5k) | supabase/mcp → `supabase-mcp/` | git shallow clone (npm metadata `@supabase/mcp-server-postgrest`; official org) | FETCHED |
| P-33 | Home Assistant (PulseMCP, 20.5k) | — | — | SKIPPED: npm `home-assistant-mcp` owner aniketbhondave mismatch vs publisher "homeassistant-ai"; dropped |
| P-34 | Clerk Docs (PulseMCP, 20.3k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-35 | Yahoo Finance (PulseMCP, 19.9k) | — | — | SKIPPED: npm `yahoo-finance-mcp-server` owner danishashko mismatch vs publisher "narumi"; dropped |
| P-36 | Exa Web Search (PulseMCP, 19.8k) | exa-labs/exa-mcp-server (lane-E) | — | COVERED: already staged in top-500 lane-E as proxy for the official Exa listing |
| P-37 | dbt (PulseMCP, 19.4k) | — | — | SKIPPED: npm `@us-all/dbt-mcp` owner us-all mismatch vs publisher "dbt Labs" (official); dropped |
| P-38 | Airweave Search (PulseMCP, 19.1k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-39 | DuckDuckGo Search (PulseMCP, 19k) | — | — | SKIPPED: GitHub-search hit `spences10/mcp-duckduckgo-search` — owner mismatch vs publisher "Nick Clyde"; dropped |
| P-40 | Google Workspace (PulseMCP, 18.7k) | — | — | SKIPPED: npm `@presto-ai/google-workspace-mcp` owner jrenaldi79 mismatch vs publisher "Taylor Wilsdon"; dropped |
| P-41 | Qdrant (PulseMCP, 18.1k) | — | — | SKIPPED: npm `@rocklerson/openai-mcp-qdrant` owner rocklerson mismatch vs publisher "Qdrant" (official); dropped |
| P-42 | Chrome Browser Automation (PulseMCP, 18k) | — | — | SKIPPED: GitHub-search hit `JEEVANANTHAMV/mcp-chrome-browser-automation` — owner mismatch vs publisher "hangye"; dropped |
| P-43 | A2ABench (PulseMCP, 17.7k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-44 | Web Research (PulseMCP, 17.2k) | mzxrai/mcp-webresearch (lane-E) | — | COVERED: already staged in top-500 lane-E (same repo; npm package has no repository link) |
| P-45 | Traditional Chinese Text Linting (PulseMCP, 17.1k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-46 | Magic (21st.dev) (PulseMCP, 16.1k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-47 | XcodeBuild (PulseMCP, 15.9k) | getsentry/XcodeBuildMCP → `getsentry-xcodebuildmcp/` | git shallow clone (npm metadata `xcodebuildmcp`; repo under getsentry org, publisher Cameron Cooke is a Sentry dev — accepted with caveat) | FETCHED |
| P-48 | Token Tool (PulseMCP, 15.8k) | — | — | SKIPPED: npm `token-tool-mcp` owner thendrix-eng mismatch vs publisher "Bitbond" (official); dropped |
| P-49 | Browserbase (PulseMCP, 15.7k) | — | — | SKIPPED: npm `@mindstone/mcp-server-browserbase` owner mindstone mismatch vs publisher "Browserbase" (official); dropped |
| P-50 | CoinAPI Real-time Exchange Rates (PulseMCP, 15.7k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-51 | AntV Chart Generator (PulseMCP, 15.4k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-52 | AWS Cost Analysis (PulseMCP, 15.3k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-53 | Lanhu (PulseMCP, 15.1k) | — | — | SKIPPED: npm `@junjan/lanhu-mcp` has no repository link; no GitHub match |
| P-54 | Container Use (PulseMCP, 15.1k) | — | — | SKIPPED: GitHub-search hit `danilo-leal/zed-container-use-mcp` — community, publisher Dagger (official); dropped |
| P-55 | Ghidra (PulseMCP, 15k) | — | — | SKIPPED: npm `@cylixlee/ghidra-mcp` owner cylixlee mismatch vs publisher "Laurie Wired"; dropped |
| P-56 | CircleCI (PulseMCP, 14.7k) | CircleCI-Public/mcp-server-circleci → `circleci-public-mcp-server-circleci/` | git shallow clone (GitHub search; official org CircleCI-Public matches publisher) | FETCHED |
| P-57 | Mastra Docs (PulseMCP, 14.6k) | — | — | SKIPPED: GitHub-search hit `yarnovo/mastra-docs-mcp` — community, publisher Mastra AI (official); dropped |
| P-58 | Unity (PulseMCP, 14.4k) | — | — | SKIPPED: npm `anklebreaker-unity-mcp` has no repository link; no GitHub match |
| P-59 | Generect (PulseMCP, 14.3k) | generect/generect_mcp → `generect-generect_mcp/` | git shallow clone (GitHub search; official org generect matches vendor) | FETCHED |
| P-60 | Reddit (PulseMCP, 14.2k) | — | — | SKIPPED: npm `reddit-mcp-buddy` owner karanb192 mismatch vs publisher "Elias Biondo"; dropped |
| P-61 | Ab Ovo (PulseMCP, 14.2k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-62 | MySQL (PulseMCP, 13.8k) | — | — | SKIPPED: npm `mysql-mcp` has no repository link; no GitHub match |
| P-63 | Templated.io (PulseMCP, 13.8k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-64 | Terraform Registry (PulseMCP, 13.7k) | — | — | SKIPPED: npm `terraform-registry-mcp` owner mrfentmen mismatch vs publisher "HashiCorp" (official); dropped |
| P-65 | Codemogger (PulseMCP, 13.5k) | — | — | SKIPPED: no npm/GitHub match after one attempt each |
| P-66 | DBHub (PulseMCP, 13.5k) | bytebase/dbhub → `bytebase-dbhub/` | git shallow clone (npm metadata `@bytebase/dbhub`; official org matches publisher) | FETCHED |
| P-67 | ArXiv (PulseMCP, 13.4k) | — | — | SKIPPED: npm `@fre4x/arxiv` has no repository link; no GitHub match |
| P-68 | Dynatrace (PulseMCP, 13.2k) | — | — | SKIPPED: npm `dynatrace-mcp` owner manojkumarg mismatch vs publisher "Dynatrace" (official); dropped |
| P-69 | SocratiCode (PulseMCP, 12.6k) | giancarloerra/socraticode → `giancarloerra-socraticode/` | git shallow clone (npm metadata; owner == publisher) | FETCHED |
| P-70 | DaVinci Resolve (PulseMCP, 12.1k) | samuelgursky/davinci-resolve-mcp → `samuelgursky-davinci-resolve-mcp/` | git shallow clone (npm metadata; owner == publisher) | FETCHED |

## Dropped / skipped list (reasons)

- **NO SOURCE, remote-only (69):** S-1–S-20, S-23–S-30, S-32–S-50, S-52–S-64, S-66–S-75 (all `remote: true`, vendor-hosted, no public repo — same convention as lane-E scan-c).
- **Repo not found after one attempt (1):** S-65 `gautamgb/mcpindex` — `github.com/gautamgb/mcpindex` 404.
- **Public clone failed — auth-gated (1):** P-4 Zapier — GitLab repo `zapier/zapier-sdk` prompts for credentials; public-repo-only rule → not fetched.
- **No resolvable public source after one npm + one GitHub-search attempt (28):** P-1, P-2, P-7, P-8, P-9, P-15, P-21, P-27, P-34, P-38, P-43, P-45, P-46, P-50, P-51, P-52, P-61, P-63, P-65 (no matches at all); P-12, P-20, P-30, P-31, P-53, P-58, P-62, P-67 (npm package exists but metadata has no usable repository link — P-31's `@posthog/mcp` points at `PostHog/posthog-js`, an ambiguous package location).
- **Match rejected — owner/publisher mismatch, wrong product (27):** P-3, P-6, P-10, P-11, P-14, P-16, P-17, P-22, P-23, P-24, P-26, P-28, P-33, P-35, P-37, P-39, P-40, P-41, P-42, P-48, P-49, P-54, P-55, P-57, P-60, P-64, P-68. Fetching a community fork or unrelated product would misattribute scan results to the listing; dropped by design.
- **Already covered in top-500 lane-E, not re-fetched (4):** P-5 Tavily (tavily-ai/tavily-mcp), P-19 Playwright (microsoft/playwright-mcp), P-36 Exa (exa-labs/exa-mcp-server), P-44 Web Research (mzxrai/mcp-webresearch).

## Final counts

| bucket | n |
|---|---|
| entries in scope (Smithery §1 + PulseMCP §2) | 145 |
| fetched into `lane-h1/` | **16** |
| NO SOURCE — remote-only | 69 |
| skipped — no resolvable public source | 55 (54 pulse: 19 no-match + 8 no-usable-repo-link + 27 mismatch-rejected; 1 smithery: S-65 not found) |
| failed — auth-gated public clone | 1 (Zapier/GitLab) |
| covered already in top-500 lane-E (no refetch) | 4 |
| **total accounted** | **145** |

Lane dir: `~/workspace/skill-egress-work-1000/lane-h1/` — 16 subdirs, **132 MB**.
Nothing was installed or executed; shallow clones only; no credentials used; no secrets collected.
