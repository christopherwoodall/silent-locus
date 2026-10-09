# FETCH-GH-2 fetch notes — lane-f2 (MCP batch, enum-awesome-ext tier)

Generated: 2026-10-05 (CDT) · worker: FETCH-GH-2
Source: `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top1000/raw/enum-awesome-ext.md`
Rows parsed: 450 total · 88 with type `mcp` (parsed with python `re` on the `| # | repo | stars | type |` markdown table, filtered `type == "mcp"`).

## Method
- `git clone --depth 1 https://github.com/<owner>/<repo>` → `~/workspace/skill-egress-work-1000/lane-f2/<owner>-<repo>`
- 4-way parallel via `xargs -P4` (GitHub tolerated it; no rate-limit blocks observed).
- Per-clone timeout 300s; transient failures retried once sequentially (immediate re-run in the same slot).
- No auth used anywhere; nothing executed — repos staged statically for the scanner.
- Platform-monorepo review: no n8n/ActivePieces-scale workflow-automation platform monorepos present in this batch — nothing dropped. (Closest candidates `A9T9/RPA`, `apioo/fusio`, `rulego/rulego` are all single-purpose tools/frameworks, kept in scope.)

## Fetch log

| # | repo | stars | status |
|---|---|---|---|
| 146 | [xpf0000/FlyEnv](https://github.com/xpf0000/FlyEnv) | ~3,253 | fetched (attempt 1) |
| 147 | [cortex-docs/cortex](https://github.com/cortex-docs/cortex) | ~3,231 | fetched (attempt 1) |
| 148 | [punitarani/fli](https://github.com/punitarani/fli) | ~3,207 | fetched (attempt 1) |
| 150 | [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) | ~3,192 | fetched (attempt 1) |
| 168 | [deedy5/ddgs](https://github.com/deedy5/ddgs) | ~3,000 | fetched (attempt 1) |
| 169 | [silexlabs/Silex](https://github.com/silexlabs/Silex) | ~2,996 | fetched (attempt 1) |
| 178 | [zhizhuodemao/js-reverse-mcp](https://github.com/zhizhuodemao/js-reverse-mcp) | ~2,888 | fetched (attempt 1) |
| 183 | [zinja-coder/jadx-ai-mcp](https://github.com/zinja-coder/jadx-ai-mcp) | ~2,853 | fetched (attempt 1) |
| 184 | [Vexa-ai/vexa](https://github.com/Vexa-ai/vexa) | ~2,851 | fetched (attempt 1) |
| 190 | [rusq/slackdump](https://github.com/rusq/slackdump) | ~2,809 | fetched (attempt 1) |
| 191 | [opensolon/solon](https://github.com/opensolon/solon) | ~2,793 | fetched (attempt 1) |
| 194 | [sparfenyuk/mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) | ~2,771 | fetched (attempt 1) |
| 195 | [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) | ~2,747 | fetched (attempt 1) |
| 198 | [jgravelle/jcodemunch-mcp](https://github.com/jgravelle/jcodemunch-mcp) | ~2,730 | fetched (attempt 1) |
| 206 | [metatool-ai/metamcp](https://github.com/metatool-ai/metamcp) | ~2,692 | fetched (attempt 1) |
| 207 | [crbnos/carbon](https://github.com/crbnos/carbon) | ~2,683 | fetched (attempt 1) |
| 211 | [brightdata/brightdata-mcp](https://github.com/brightdata/brightdata-mcp) | ~2,660 | fetched (attempt 1) |
| 214 | [chrisryugj/korean-law-mcp](https://github.com/chrisryugj/korean-law-mcp) | ~2,638 | fetched (attempt 1) |
| 216 | [go-nunu/nunu](https://github.com/go-nunu/nunu) | ~2,607 | fetched (attempt 1) |
| 226 | [samanhappy/mcphub](https://github.com/samanhappy/mcphub) | ~2,494 | fetched (attempt 1) |
| 228 | [nitrocloudofficial/nitrostack](https://github.com/nitrocloudofficial/nitrostack) | ~2,467 | fetched (attempt 1) |
| 235 | [redhat-et/ripwire](https://github.com/redhat-et/ripwire) | ~2,400 | fetched (attempt 1) |
| 239 | [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana) | ~2,382 | fetched (attempt 1) |
| 241 | [0xMassi/webclaw](https://github.com/0xMassi/webclaw) | ~2,366 | fetched (attempt 1) |
| 250 | [jnMetaCode/agency-orchestrator](https://github.com/jnMetaCode/agency-orchestrator) | ~2,326 | fetched (attempt 1) |
| 263 | [MCPJam/inspector](https://github.com/MCPJam/inspector) | ~2,235 | fetched (attempt 1) |
| 264 | [AmoyLab/Unla](https://github.com/AmoyLab/Unla) | ~2,234 | fetched (attempt 1) |
| 265 | [777genius/agent-teams-ai](https://github.com/777genius/agent-teams-ai) | ~2,231 | fetched (attempt 1) |
| 269 | [duty1g/x64dbg-mcp-server](https://github.com/duty1g/x64dbg-mcp-server) | ~2,195 | fetched (attempt 1) |
| 270 | [martin-ger/esp32_nat_router](https://github.com/martin-ger/esp32_nat_router) | ~2,194 | fetched (attempt 1) |
| 272 | [vibheksoni/stealth-browser-mcp](https://github.com/vibheksoni/stealth-browser-mcp) | ~2,176 | fetched (attempt 1) |
| 274 | [atomicstrata/llm-wiki-compiler](https://github.com/atomicstrata/llm-wiki-compiler) | ~2,161 | fetched (attempt 1) |
| 277 | [mcp-router/mcp-router](https://github.com/mcp-router/mcp-router) | ~2,145 | fetched (attempt 1) |
| 278 | [cjo4m06/mcp-shrimp-task-manager](https://github.com/cjo4m06/mcp-shrimp-task-manager) | ~2,145 | fetched (attempt 1) |
| 279 | [alpic-ai/skybridge](https://github.com/alpic-ai/skybridge) | ~2,139 | fetched (attempt 1) |
| 284 | [apioo/fusio](https://github.com/apioo/fusio) | ~2,120 | fetched (attempt 1) |
| 289 | [chongdashu/unreal-mcp](https://github.com/chongdashu/unreal-mcp) | ~2,090 | fetched (attempt 1) |
| 291 | [A9T9/RPA](https://github.com/A9T9/RPA) | ~2,065 | fetched (attempt 1) |
| 292 | [CYB3RMX/Qu1cksc0pe](https://github.com/CYB3RMX/Qu1cksc0pe) | ~2,065 | fetched (attempt 1) |
| 298 | [doobidoo/mcp-memory-service](https://github.com/doobidoo/mcp-memory-service) | ~1,984 | fetched (attempt 1) |
| 299 | [forloopcodes/contextplus](https://github.com/forloopcodes/contextplus) | ~1,983 | fetched (attempt 1) |
| 315 | [Joooook/12306-mcp](https://github.com/Joooook/12306-mcp) | ~1,887 | fetched (attempt 1) |
| 321 | [anysearch-ai/anysearch-mcp-server](https://github.com/anysearch-ai/anysearch-mcp-server) | ~1,859 | fetched (attempt 1) |
| 322 | [zzet/gortex](https://github.com/zzet/gortex) | ~1,859 | fetched (attempt 1) |
| 323 | [korotovsky/slack-mcp-server](https://github.com/korotovsky/slack-mcp-server) | ~1,856 | fetched (attempt 1) |
| 324 | [timescale/pg-aiguide](https://github.com/timescale/pg-aiguide) | ~1,855 | fetched (attempt 1) |
| 325 | [AminForou/mcp-gsc](https://github.com/AminForou/mcp-gsc) | ~1,848 | fetched (attempt 1) |
| 330 | [OpenAgentPlatform/Dive](https://github.com/OpenAgentPlatform/Dive) | ~1,826 | fetched (attempt 1) |
| 332 | [Mcp-Brasil/mcp-brasil](https://github.com/Mcp-Brasil/mcp-brasil) | ~1,802 | fetched (attempt 1) |
| 335 | [ravitemer/mcphub.nvim](https://github.com/ravitemer/mcphub.nvim) | ~1,784 | fetched (attempt 1) |
| 337 | [jau123/MeiGen-AI-Design-MCP](https://github.com/jau123/MeiGen-AI-Design-MCP) | ~1,778 | fetched (attempt 1) |
| 341 | [mex-memory/mex](https://github.com/mex-memory/mex) | ~1,753 | fetched (attempt 1) |
| 343 | [glidea/zenfeed](https://github.com/glidea/zenfeed) | ~1,714 | fetched (attempt 1) |
| 351 | [OpenOSINT/OpenOSINT](https://github.com/OpenOSINT/OpenOSINT) | ~1,692 | fetched (attempt 1) |
| 358 | [lucasastorian/llmwiki](https://github.com/lucasastorian/llmwiki) | ~1,664 | fetched (attempt 1) |
| 364 | [patrickchugh/terravision](https://github.com/patrickchugh/terravision) | ~1,646 | fetched (attempt 1) |
| 367 | [f/mcptools](https://github.com/f/mcptools) | ~1,625 | fetched (attempt 1) |
| 369 | [vybenetwork/solana-mcp-vybe](https://github.com/vybenetwork/solana-mcp-vybe) | ~1,621 | fetched (attempt 1) |
| 370 | [modelcontextprotocol/php-sdk](https://github.com/modelcontextprotocol/php-sdk) | ~1,619 | fetched (attempt 1) |
| 372 | [rulego/rulego](https://github.com/rulego/rulego) | ~1,617 | fetched (attempt 1) |
| 373 | [matlab/matlab-mcp-server](https://github.com/matlab/matlab-mcp-server) | ~1,617 | fetched (attempt 1) |
| 377 | [isaacphi/mcp-language-server](https://github.com/isaacphi/mcp-language-server) | ~1,604 | fetched (attempt 1) |
| 379 | [svnscha/mcp-windbg](https://github.com/svnscha/mcp-windbg) | ~1,603 | fetched (attempt 1) |
| 380 | [datagouv/datagouv-mcp](https://github.com/datagouv/datagouv-mcp) | ~1,600 | fetched (attempt 1) |
| 382 | [MiniMax-AI/MiniMax-MCP](https://github.com/MiniMax-AI/MiniMax-MCP) | ~1,582 | fetched (attempt 1) |
| 385 | [miscusi-peek/cheatengine-mcp-bridge](https://github.com/miscusi-peek/cheatengine-mcp-bridge) | ~1,565 | fetched (attempt 1) |
| 389 | [Prismer-AI/PrismerCloud](https://github.com/Prismer-AI/PrismerCloud) | ~1,554 | fetched (attempt 1) |
| 390 | [BlackSnufkin/LitterBox](https://github.com/BlackSnufkin/LitterBox) | ~1,544 | fetched (attempt 1) |
| 392 | [PaperDebugger/paperdebugger](https://github.com/PaperDebugger/paperdebugger) | ~1,543 | fetched (attempt 1) |
| 393 | [qdrant/mcp-server-qdrant](https://github.com/qdrant/mcp-server-qdrant) | ~1,542 | fetched (attempt 1) |
| 397 | [mxsm/rocketmq-rust](https://github.com/mxsm/rocketmq-rust) | ~1,522 | fetched (attempt 1) |
| 399 | [Azure/data-api-builder](https://github.com/Azure/data-api-builder) | ~1,518 | fetched (attempt 1) |
| 401 | [NPC-Worldwide/npcpy](https://github.com/NPC-Worldwide/npcpy) | ~1,510 | fetched (attempt 1) |
| 405 | [nduckmink/arkon](https://github.com/nduckmink/arkon) | ~1,486 | fetched (attempt 1) |
| 407 | [robotmcp/ros-mcp-server](https://github.com/robotmcp/ros-mcp-server) | ~1,484 | fetched (attempt 1) |
| 410 | [inkeep/agents](https://github.com/inkeep/agents) | ~1,451 | fetched (attempt 2) |
| 412 | [chunkhound/chunkhound](https://github.com/chunkhound/chunkhound) | ~1,441 | fetched (attempt 1) |
| 414 | [mohitagw15856/pm-claude-skills](https://github.com/mohitagw15856/pm-claude-skills) | ~1,424 | fetched (attempt 1) |
| 415 | [mnemox-ai/tradememory-protocol](https://github.com/mnemox-ai/tradememory-protocol) | ~1,423 | fetched (attempt 1) |
| 422 | [designcomputer/mysql_mcp_server](https://github.com/designcomputer/mysql_mcp_server) | ~1,399 | fetched (attempt 1) |
| 426 | [taielab/awesome-hacking-lists](https://github.com/taielab/awesome-hacking-lists) | ~1,390 | fetched (attempt 1) |
| 427 | [mbailey/voicemode](https://github.com/mbailey/voicemode) | ~1,387 | fetched (attempt 1) |
| 429 | [heymrun/heym](https://github.com/heymrun/heym) | ~1,385 | fetched (attempt 2) |
| 435 | [Dataojitori/nocturne_memory](https://github.com/Dataojitori/nocturne_memory) | ~1,375 | fetched (attempt 1) |
| 436 | [ridafkih/keeper.sh](https://github.com/ridafkih/keeper.sh) | ~1,373 | fetched (attempt 1) |
| 438 | [sourcey/sourcey](https://github.com/sourcey/sourcey) | ~1,371 | fetched (attempt 1) |
| 446 | [joey-zhou/xiaozhi-esp32-server-java](https://github.com/joey-zhou/xiaozhi-esp32-server-java) | ~1,359 | fetched (attempt 1) |
| 447 | [thetahealth/mirobody](https://github.com/thetahealth/mirobody) | ~1,358 | fetched (attempt 1) |

## Retries (transient failures, recovered)
| repo | attempt 1 failure (verbatim) | attempt 2 |
|---|---|---|
| [inkeep/agents](https://github.com/inkeep/agents) | `Cloning into 'inkeep-agents'... ` then the `timeout 300` fired (large repo, transfer did not finish within 300s) | OK |
| [heymrun/heym](https://github.com/heymrun/heym) | `Cloning into 'heymrun-heym'... fetch-pack: unexpected disconnect while reading sideband packet ` | OK |

## Skipped / dropped — NONE
- Skipped (404 / credentials / >300s after one retry): 0.
- Dropped as out-of-skill-scope platform monorepos: 0 — no n8n/ActivePieces-scale workflow-automation platform monorepos among the 88 `mcp` rows. Reviewed candidates kept: `A9T9/RPA` (RPA tool), `apioo/fusio` (API gateway), `rulego/rulego` (Go rule engine) — all single-purpose, in scope.

## Final count
- Fetched: **88/88**
- Skipped: 0
- Failed: 0
- Staging dir: `~/workspace/skill-egress-work-1000/lane-f2/` — 4.2G, all 88 `<owner>-<repo>` dirs verified to contain `.git`.
- Raw per-clone log: `~/workspace/skill-egress-work-1000/lane-f2/clone.log`; repo list: `repos-mcp.txt`.
