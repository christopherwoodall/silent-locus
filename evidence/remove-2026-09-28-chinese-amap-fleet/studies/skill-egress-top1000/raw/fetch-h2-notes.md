# Lane H-2 — marketplace batch (fetch-h2): notes

Subagent session 78b32fa9-b543-459f-8bd5-f0c974e2aa7a (FETCH-MKT-2) · 2026-10-05.
Target list: `raw/enum-marketplaces-ext.md` §§3–6 (VS Code ×27, mcp.so ×13, mcpso.cc ×8, npm ×12 = 60 identities).
Staging dir: `~/workspace/skill-egress-work-1000/lane-h2/` (study scratch; never committed).
Scanner: `~/workspace/muse-home/projects/skill-tracer/scan/egress_scan.py` will scan this dir in a later lane.

## Method

- GitHub: `git clone --depth 1` into `<owner>-<repo>`, sequential ~2s pacing; transient failures retried once sequentially.
- npm: `npm view <pkg> dist.tarball` → `curl -sL <tarball> | tar -xz -C <pkgdir>` — static unpack only. Never `npm install`, never ran install scripts.
- VS Code: latest version resolved via public gallery `extensionquery` API (7.1-preview.1), then `.../vsextensions/<ext>/<ver>/vspackage` downloaded and unpacked statically into `vsc-<pub>-<name>/`. Never executed extension code. **Quirk found:** the vspackage endpoint returns gzip-wrapped content (magic `\x1f\x8b`) — downloads must be gunzipped before unzipping as zip. First attempt failed with "File is not a zip file" on 5/5; fixed in `fetch_vsc.py`/`fetch_vsc_b.py` (gunzip-if-gzip then unzip); already-downloaded .vsix files were repaired the same way.
- Remote-only / unresolvable: one GitHub-API attempt + one web-search retry; if still unresolvable, recorded as NO SOURCE (not fetched).
- Public sources only. No auth. Secrets noted, never used. No install or execution of anything fetched.

## §3 — VS Code marketplace: 27/27 fetched (static .vsix unpacks, latest versions as of 2026-10-05)

| # | extension | itemName | version | source fetched | how | status |
|---|---|---|---|---|---|---|
| 1 | Cline | saoudrizwan.claude-dev | 4.1.22 | `vsc-saoudrizwan-claude-dev` | vsix static unpack | ok |
| 2 | Qoder CN (Formerly Lingma) | Alibaba-Cloud.tongyi-lingma | (latest) | `vsc-alibaba-cloud-tongyi-lingma` | vsix static unpack | ok |
| 3 | CodeGPT: AI Coding Agents & Chat | DanielSanMedium.dscodegpt | (latest) | `vsc-danielsanmedium-dscodegpt` | vsix static unpack | ok |
| 4 | Roo Code | RooVeterinaryInc.roo-cline | (latest) | `vsc-rooveterinaryinc-roo-cline` | vsix static unpack | ok |
| 5 | Kilo Code | kilocode.Kilo-Code | (latest) | `vsc-kilocode-kilo-code` | vsix static unpack | ok |
| 6 | Azure MCP Server | ms-azuretools.vscode-azure-mcp-server | (latest) | `vsc-ms-azuretools-vscode-azure-mcp-server` | vsix static unpack | ok |
| 7 | Foundry Toolkit for VS Code | ms-windows-ai-studio.windows-ai-studio | 1.6.15 | `vsc-ms-windows-ai-studio-windows-ai-studio` | vsix static unpack | ok |
| 8 | CodeGeeX | aminer.codegeex | 2.27.6 | `vsc-aminer-codegeex` | vsix static unpack | ok |
| 9 | Bito AI Code Reviews | Bito.Bito | 1.7.0 | `vsc-bito-bito` | vsix static unpack | ok |
| 10 | Agentforce Vibes | salesforce.salesforcedx-einstein-gpt | 4.37.1 | `vsc-salesforce-salesforcedx-einstein-gpt` | vsix static unpack | ok |
| 11 | Fitten Code | FittenTech.Fitten-Code | 1.1.4 | `vsc-fittentech-fitten-code` | vsix static unpack | ok |
| 12 | Augment | augment.vscode-augment | 0.904.0 | `vsc-augment-vscode-augment` | vsix static unpack | ok |
| 13 | Kimi Code | moonshot-ai.kimi-code | 0.8.1 | `vsc-moonshot-ai-kimi-code` | vsix static unpack | ok |
| 14 | Google Antigravity | Google.google-antigravity | 1.7.0 | `vsc-google-google-antigravity` | vsix static unpack | ok |
| 15 | Sixth AI | Sixth.sixth-ai | 0.3.7 | `vsc-sixth-sixth-ai` | vsix static unpack | ok |
| 16 | DeepSeek V4 for Copilot Chat | Vizards.deepseek-v4-for-copilot | 0.9.3 | `vsc-vizards-deepseek-v4-for-copilot` | vsix static unpack | ok |
| 17 | ChatGPT Copilot | feiskyer.chatgpt-copilot | 4.11.0 | `vsc-feiskyer-chatgpt-copilot` | vsix static unpack | ok |
| 18 | Cline Chinese | HybridTalentComputing.cline-chinese | 4.1.22 | `vsc-hybridtalentcomputing-cline-chinese` | vsix static unpack | ok |
| 19 | DBCode | DBCode.dbcode | 1.38.9 | `vsc-dbcode-dbcode` | vsix static unpack | ok |
| 20 | GitHub Copilot upgrade (.NET) | ms-dotnettools.upgrade-agent | 1.1.652 | `vsc-ms-dotnettools-upgrade-agent` | vsix static unpack | ok |
| 21 | Zencoder | ZencoderAI.zencoder | 3.85.9007 | `vsc-zencoderai-zencoder` | vsix static unpack | ok |
| 22 | Azad Coder | kodu-ai.claude-dev-experimental | 25.12.16 | `vsc-kodu-ai-claude-dev-experimental` | vsix static unpack | ok |
| 23 | OpenCode GUI | TanishqKancharla.opencode-vscode | 0.4.4 | `vsc-tanishqkancharla-opencode-vscode` | vsix static unpack | ok |
| 24 | Copilot MCP + Agent Skills Manager | AutomataLabs.copilot-mcp | 0.0.97 | `vsc-automatalabs-copilot-mcp` | vsix static unpack | ok |
| 25 | ChatGPT - Unfold AI | TalDennis-UnfoldAI-ChatGPT-Copilot.unfoldai | 3.3.2 | `vsc-taldennis-unfoldai-chatgpt-copilot-unfoldai` | vsix static unpack | ok |
| 26 | DSH Cline | shengsuan-cloud.cline-shengsuan | 4.2.8 | `vsc-shengsuan-cloud-cline-shengsuan` | vsix static unpack | ok |
| 27 | Zoo Code | ZooCodeOrganization.zoo-code | 3.87.100574 | `vsc-zoocodeorganization-zoo-code` | vsix static unpack | ok |

Note: rows 1–6 show "(latest)" — they were fetched by the first worker run whose per-extension versions were lost in the zip-failure restart; their on-disk unpacks are the then-current versions (fetch log only records `present`). Rows 7–27 versions are from the successful run logs (`vsc-fetch-log.tsv` + `vsc-fetch-log-b.tsv`).

## §4 — mcp.so: 5/13 fetched; 8 NO SOURCE

| # | marketplace entry | source fetched | how | status |
|---|---|---|---|---|
| F1 | AQL PropertyCheck (Alpha Quant Labs) | — | — | NO SOURCE: vendor-hosted SaaS, no public repo (GitHub search + web search) |
| F2 | Aard (Braddon Lance) | — | — | NO SOURCE: no public repo found |
| F3 | AIsa | AIsa-public/AIsa-mcp-server | git shallow clone — repo README confirms "Every AIsa data API as MCP tools, behind one endpoint: https://mcp.aisa.one/mcp" | ok |
| F4 | API Direct | — | — | NO SOURCE: remote-only SaaS, no public repo found |
| F5 | AccountHub (One) | — | — | NO SOURCE: remote-only SaaS, no public repo found |
| N1 | Kapa (kapa-ai) | — | — | NO SOURCE: kapa-ai hosted docs-RAG; only a community local provider (npelikan/kapa-mcp-local) exists — not the vendor's code, not fetched |
| N2 | Scribiz (Illyism) | Illyism/scribiz-mcp | git shallow clone — README: "Scribiz: video MCP server for YouTube transcripts, summaries and timestamps"; vendor Illyism matches | ok |
| N3 | ramen (bkraad47) | — | — | NO SOURCE: self-hosted product, no public repo found |
| N4 | InstaVision (InstaVision) | afanasenkoa/instavision-mcp | git shallow clone — README: "InstaVision — Instagram niche discovery for AI agents" | ok |
| N5 | Senso MCP for Joomla (sensomedia) | — | — | NO SOURCE: no public repo found |
| N6 | Bitculator (Bitculator) | Bitculator/bitculator-mcp | git shallow clone — README: "Bitculator MCP Server ... Live and historical crypto market data for AI agents" | ok |
| N7 | JiCo for Jira & Confluence (drkv-com) | drkv-com/jico-mcp | git shallow clone — README: "JiCo for Jira & Confluence — MCP server for Jira Data Center and Jira Cloud" | ok |
| N8 | ipvolt proxy toolkit mcp (ipvolt) | — | — | NO SOURCE: no public repo found (GitHub search + web search) |

## §5 — mcpso.cc: 7/8 fetched; 1 excluded

| # | marketplace entry | source fetched | how | status |
|---|---|---|---|---|
| 1 | wcgw (shell + coding agent) | — | — | NOT FETCHED: microsoft/wcgw exists but is a full coding-agent repo — out of scope for the egress-lane batch per lane-E precedent (scan-c-notes) |
| 2 | iTerm (iterm-mcp) | ferrislucas/iterm-mcp | git shallow clone | ok |
| 3 | TaskManager (@kazuph/mcp-taskmanager) | kazuph/mcp-taskmanager | git shallow clone | ok |
| 4 | Dice Roller (mcp-dice) | yamaton/mcp-dice | git shallow clone — not on npm or Smithery (404/"Namespace not found"); GitHub `yamaton/mcp-dice` = "A MCP server enabling LLMs to roll dice" — verified match | ok |
| 5 | Obsidian Reader (mcp-obsidian) | npm tarball mcp-obsidian@1.0.0 | curl + static unpack (4 files) | ok |
| 6 | MySQL Server (@f4ww4z/mcp-mysql-server) | f4ww4z/mcp-mysql-server | git shallow clone | ok |
| 7 | Shodan Server (@burtthecoder/mcp-shodan) | burtthecoder/mcp-shodan | git shallow clone — egress-relevant (network recon) | ok |
| 8 | Audiense Insights (@AudienseCo/mcp-audiense-insights) | AudienseCo/mcp-audiense-insights | git shallow clone | ok |

## §6 — npm: 12/12 fetched (4 source units cover all 12 packages)

| # | npm package | source fetched | how | status |
|---|---|---|---|---|
| 1 | @transcend-io/mcp-server-assessment | transcend-io/tools | git shallow clone — covers all 8 @transcend-io packages | ok |
| 2 | @transcend-io/mcp-server-preferences | transcend-io/tools | covered by same clone | ok |
| 3 | @transcend-io/mcp-server-consent | transcend-io/tools | covered by same clone | ok |
| 4 | @transcend-io/mcp-server-discovery | transcend-io/tools | covered by same clone | ok |
| 5 | @transcend-io/mcp-server-docs | transcend-io/tools | covered by same clone | ok |
| 6 | @transcend-io/mcp-server-inventory | transcend-io/tools | covered by same clone | ok |
| 7 | @transcend-io/mcp-server-dsr | transcend-io/tools | covered by same clone | ok |
| 8 | @transcend-io/mcp-server-base | transcend-io/tools | covered by same clone | ok |
| 9 | scryfall-mcp-server | npm tarball scryfall-mcp-server-0.1.1.tgz | curl + static unpack (7 files) — no repo link in registry | ok |
| 10 | tiny-http-mcp-server | npm tarball tiny-http-mcp-server-0.1.130.tgz | curl + static unpack (524 files) — repo link points at the poe-platform/poe-code monorepo, whose shallow clone timed out (>300s); package tarball used instead (the exact published artifact, better for this study) | ok |
| 11 | @hubspot/mcp-server | npm tarball mcp-server-0.4.0.tgz | curl + static unpack (38 files) — no repo link in registry | ok |
| 12 | @zencoderai/slack-mcp-server | zencoderai/slack-mcp-server | git shallow clone | ok |

## Dropped / skipped list with reasons

| entry | lane | reason |
|---|---|---|
| AQL PropertyCheck, Aard, API Direct, AccountHub, Kapa, ramen, Senso MCP for Joomla, ipvolt proxy toolkit | mcp.so §4 | NO SOURCE — vendor-hosted/remote-only SaaS; no public repo on GitHub search + web search |
| wcgw | mcpso.cc §5 | NOT FETCHED — microsoft/wcgw is a full coding-agent repo, out of scope for the egress-lane batch (lane-E precedent) |
| poe-platform/poe-code (as repo) | npm §6 | NOT FETCHED as repo — monorepo too large (clone timed out >300s); the actual published artifact `tiny-http-mcp-server` was unpacked from its npm tarball instead |
| mcp-dice initial "not found" | mcpso.cc §5 | resolved on retry — found as `yamaton/mcp-dice` on GitHub (verified match), fetched |

## Final count

| lane | identities | fetched | skipped/failed |
|---|---|---|---|
| §3 VS Code marketplace | 27 | 27 | 0 |
| §4 mcp.so | 13 | 5 | 8 (NO SOURCE) |
| §5 mcpso.cc | 8 | 7 | 1 (out of scope) |
| §6 npm | 12 | 12 | 0 |
| **Total** | **60** | **51** | **9** |

**51/60 marketplace identities fetched; 0 hard failures** (9 skipped with documented reasons: 8 remote-only/no public source, 1 out-of-scope per precedent).
Lane-h2 dir: `~/workspace/skill-egress-work-1000/lane-h2/` — **2.9 GB** (dominated by VS Code extension unpacks; largest: Alibaba Qoder CN 207MB compressed).
Fetch artifacts: `fetch_vsc.py` (27 workers A), `fetch_vsc_b.py` (worker B), `fetch_git.py`, `git-fetch-log.tsv`, `vsc-fetch-log.tsv`, `vsc-fetch-log-b.tsv`.

*Fetch log written 2026-10-05. All fetches: public sources only, no auth, no install/execution — static files only.*
