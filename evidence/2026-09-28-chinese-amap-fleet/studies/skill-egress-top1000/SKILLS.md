# Top-1000 AI Skills Egress Study — ranked skill list (extension: identities 359–1013)

Generated 2026-10-05. Enumeration: lane A-ext (GitHub stars tier 2, `raw/enum-awesome-ext.md`) +
lane B-ext (marketplaces tier 2, `raw/enum-marketplaces-ext.md`). This file covers the NEW identities
only; the first 358 are in `../skill-egress-top500/SKILLS.md`.

## Totals
- Lane A-ext: **450 ranked repos** (stars ~10,595 → ~1,346 cutoff), from 8,724 unique repos across 16 queries × pages 2–10 (13 overlapped the top-500's 216 — deduped). Types: 46 claude-skill · 88 mcp · 316 other (harnesses, CLIs, misc).
- Lane B-ext: **205 unique new identities** (75 smithery tier-2 · 70 PulseMCP ranks 43–126 · 27 VS Code gallery · 13 mcp.so · 8 mcpso.cc · 12 npm).
- **655 new identities enumerated**; **1,013 combined** with the top-500's 358.

## Top-40 by popularity (new identities; metrics differ per source — approximate order)

### GitHub stars lane (tier 2)
1. omnigent-ai/omnigent ~10,595 (other — agent meta-harness) | 2. simonlin1212/a-stock-data ~10,573 (other)
3. Kuberwastaken/claurst ~10,311 | 4. open-gsd/gsd-core ~10,197 | 5. ykdojo/claude-code-tips ~10,191
6. AgriciDaniel/claude-ads ~9,722 | 7. xonsh/xonsh ~9,658 | 8. frankbria/ralph-claude-code ~9,654
9. chuspeeism/dashi-ppt-skill ~9,157 (claude-skill) | 10. backnotprop/plannotator ~9,149
11. revfactory/harness ~9,119 | 12. pacifio/atlas ~9,096 | 13. max-sixty/worktrunk ~8,836
14. Maciek-roboblog/Claude-Code-Usage-Monitor ~8,730 | 15. genspark-ai/genoffice ~8,702
16. smtg-ai/claude-squad ~8,570 | 17. HarnessMD/munder-difflin ~8,469 | 18. automazeio/ccpm ~8,398
19. jnMetaCode/superpowers-zh ~8,258 | 20. YaoApp/yao ~8,077
- Tier-2 claude-skill notables: dashi-ppt-skill and 45 more (all 46 fetched → lane-f1)

### Marketplace lane (tier 2)
1. Cline (saoudrizwan.claude-dev) — 5.54M installs (VS Code) | 2. Qoder CN (Alibaba) — 2.72M
3. CodeGPT — 2.53M | 4. Roo Code — 2.06M | 5. Kilo Code — 1.60M | 6. Azure MCP Server — 1.55M
7. Foundry Toolkit — 1.49M | 8. CodeGeeX — 1.37M | 9. MotherDuck & DuckDB — 40.2k/wk (PulseMCP)
10. AWS Bedrock KB Retrieval — 37.7k/wk | 11. OpenBrand — 36.1k/wk | 12. Zapier — 35.1k/wk
13. Tavily Search — 34.7k/wk | 14. Better Icons — 32.9k/wk | 15. CLI Secure — 31.9k/wk
16. Nerve Network — 31k/wk | 17. AWS CDK — 29.7k/wk | 18. Godot (Solomon) — 27.9k/wk
19. Salesforce CLI — 27.3k/wk | 20. revnuvo-mcp — 8,907 useCount (Smithery)
- VS Code gallery counts drifted sharply vs lane-B's snapshot (Claude Code 9.1M→27.0M).

## Scanned batches (new)
- Lane F1 (GitHub claude-skills): 46 repos fetched, 1,772 skill units → `raw/scan-d1.json`
- Lane F2 (GitHub MCP): 88 repos fetched, 304 skill units → `raw/scan-d2.json`
- Lane F3 (GitHub triaged other): 59 repos fetched, 343 skill units → `raw/scan-d3.json`
- Lane H1 (marketplace smithery+pulse): 16 repos fetched, 27 skill units → `raw/scan-f1.json`
- Lane H2 (marketplace vsc+mcp.so+mcpso+npm): 51 packages fetched, 44 skill units → `raw/scan-f2.json`
- Total new: **260 repos/packages fetched, 2,490 skill units, 741 with egress hits**
- Combined with top-500: **437 repos/packages, 6,343 units, 1,541 with hits**

## Gaps (still open)
- 153 signal-positive GitHub `other` repos below the 60-fetch cap (ranked list in lane-f3 `clone-candidates.tsv`)
- Smithery tier-3 (useCount < 2,207), PulseMCP pages 4–5, npm query tails (cached in /tmp/mkt1000/, documented in enum-marketplaces-ext.md)
- Remote-only Smithery listings with no public source (69 in tier 2 alone) — server-side opaque by construction
- glama.ai (React SPA, undocumented internal API) — still unenumerated
