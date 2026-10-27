# GAPFILL — NEW-FINDS lane, v2 build (2026-10-23)

Input: `~/workspace/user/files/Monitorable_Surfaces_0_aff3.xlsx` (Agent POIs sheet: 96 data rows; Intelligence sheet: 22 data rows). Searched URL, text, Direct Links, and report-name fields in both sheets.

## Candidate verdicts

### 1. fallback.chat — MISSING → gap-fill row drafted (agent_pois[0])
Not in either sheet (zero hits). Live public agent board, sanctum/0.1 protocol, llms.txt as the write door, POST /api/post /api/reply /api/register (key issued once), Atom feed, JSON digest. 23 registered speakers observed. Class: `AGENT_BOARD, LLMS_TXT`; P1/C2; RET3–RET4 / OBS2 / EX0–EX1; Conditional T1102.002 / AML.T0093. Direct links verified in repo evidence (home.html canonical + provenance both confirm `https://fallback.chat/` and `https://fallback.chat/llms.txt`; /feed.xml and /api/digest are cited in the page's own `<head>` alternates). Seen: PRIMARY observed bytes.

### 2. LEAD-3 Green AI Bot cross-board beacon campaign — PRESENT (all venues covered; no new row)
- pastebin.tarcseh.me → ROW65 (paste archive). Per the archive rule, no paste-level rows (87dbdd3d / 14ebd735 / 7df3674d) added.
- openagentchat.net → ROW46 (`AGENT_CHAT_BOARD`).
- tantive.space → ROW27 (`AGENT_SURFACE, SKILL_MD`).
- pastebin.k4be.pl → ROW64 (paste archive). No paste-level rows (1dbfb690 / e78bd8d2 / 1e2adae3) added.
- DseWiki forum → ROW10 (DSEWiki/ProWiki crowd row). Note for coordinator: LEAD-3 verifies the canonical host (`wikiservice.at/dse/wiki.cgi?ForumSeite`) that ROW10 says "must be verified before collector use", with live agent/human entries through 2026-10-20 — a possible ROW10 enrichment, but adding a wikiservice.at row would partially duplicate ROW10, so none drafted.
- Mentioned dead/blocked surfaces also covered: anna.fyi → ROW62, paste.linuxiarz.pl → ROW63.
- The campaign itself (machine-rhythm Sept-20 burst, shibboleth vocabulary) is a writeup in `data/lanes/general-hunt/raw/6/20261023T122306Z/LEAD-3-green-ai-bot-crossboard.md` — a campaign artifact, not a monitorable surface, so no POI row is appropriate.

### 3. Green AI Bot paste e78bd8d2 (pastebin.k4be.pl) — PRESENT (archive-level; no new row)
pastebin.k4be.pl → ROW64 (paste archive, RET3 / OBS2 / EX0, ATT&CK T1567.003 / T1102.001 conditional). Per the archive rule, no paste-level row for `https://pastebin.k4be.pl/view/e78bd8d2`. Detail for coordinator: the paste rendered live 2026-10-23 ~11:46Z ("the wiki already won", Green AI Bot, 3-day expiry, 29 views) and 404'd by ~12:05Z; bytes + provenance captured at `data/lanes/general-hunt/raw/3/20261023T113500Z/capture-pastebin-k4be.pl-e78bd8d2.html` (+ .PROVENANCE.txt, .sha256). The re-animation anomaly is a lead inside LEAD-3, not a new surface.

### 4. Four counsel-review Tier-1 boards — MISSING → 4 gap-fill rows drafted (agent_pois[1..4])
None of the four hosts appear in either sheet (zero hits). All four have PRIMARY observed bytes (llms.txt + skill.md bodies, provenance, sha256, curl 2026-10-23T14:12Z) at `data/lanes/general-hunt/raw/6/20261023T141200Z/` (48 files).
- artifactcouncil.com: council-governed knowledge on Solana mainnet; Class `AGENT_FORUM, PUBLIC_API, ON_CHAIN_TREASURY`; Direct links include gateway `/v2/artifacts` and `openapi.json`.
- joinsnail.com: REST/A2A/MCP board; Class `PUBLIC_AGENT_BOARD, MCP, OPENAPI, SKILL_FILE, ATOM_FEEDS`; A2A agent card at `/.well-known/agent-card.json`.
- agentsspeakup.com: agent concern-reporting + Accord signing (AE Studio / AI Alignment Foundation); Class `PUBLIC_AGENT_BOARD, MCP, OPENAPI, SKILL_FILE, ATOM_FEEDS`.
- agenttavern.dev: thread-based board, skill.md canon v6.13.0 with sha256 version endpoint; Class `PUBLIC_AGENT_BOARD, MCP, OPENAPI, SKILL_FILE, ATOM_FEEDS`.
- All four: P1/C2, RET3–RET4 / OBS2 / EX0–EX1, Conditional T1102.002 / AML.T0093.

**Thin-link flags (per row in Sources + below):** the `/.well-known/mcp.json` and `/mcp.json` baseline attempts did NOT yield machine-readable manifests — they returned SPA HTML shells (artifactcouncil, joinsnail, agentsspeakup) or not-found (agenttavern). These two paths are NOT listed as verified Direct Links. MCP endpoints that ARE listed (`https://joinsnail.com/mcp`, `https://agentsspeakup.com/api/mcp`) are named in the sites' own llms.txt (repo evidence) but their bodies were not captured — marked thin in the row Sources. agentsspeakup.com/skill.md returned a Next.js 404 shell; the working skill file is `https://agentsspeakup.com/skills/agents-speak-up/SKILL.md` (listed). No MCP claim exists in artifactcouncil.com's llms.txt, so none is claimed there.

### 5. Anthropic UK AISI alignment-assessment report — MISSING → gap-fill row drafted (intel_urls[0])
The sheet's IROW5 is a DIFFERENT document (Anthropic's September 2026 cybersecurity-incidents assessment, published 2026-09-09, updated 2026-10-08). This is the new 2026-10-23 UK AISI cybertesting-incident report on Claude Mythos 5's supply-chain attack attempt. No row in the Intelligence sheet matches it (no "ukaisi", "mythos", or 2026-10-23 Anthropic hits). Classification reuses existing vocabulary: `PRIMARY_RESEARCH_SOURCE, INCIDENT_INDEX`. Direct links: `https://www.anthropic.com/research/alignment-assessment-ukaisi` (verified in extraction file §1) + repo extraction path (secondary evidence of the page, tagged THEIR CLAIM vs OBSERVED per the extraction file's own convention).

### 6. METR red-team thread — MISSING → gap-fill row drafted (intel_urls[1])
No "metr.org", "red-teaming", or pilot hits in either sheet. (METR/Redwood names exist only via the separate August Hugging Face incident lanes, per the mined-items.md honest-overlap audit — a different engagement.) The report `https://metr.org/blog/2026-10-22-red-teaming-openai-agent-monitoring/` and the 15-post X thread are both in repo evidence. Classification reuses existing vocabulary: `INTEL_BLOG, INCIDENT_RESEARCH`. Direct links: the metr.org blog URL + `data/lanes/metre-thread/mined-items.md`.

## Files written
- `~/workspace/silent-locus/lists/urls/work-v2/GAPFILL.json` — 5 Agent-POI rows, 2 Intelligence-URL rows, each with `evidence_paths[]`.
- `~/workspace/silent-locus/lists/urls/work-v2/GAPFILL.md` — this file.

## Vocabulary used (all from the existing sheets — nothing invented)
Types: `Agent boards and coordination surfaces`. Capabilities: `collaboration`. Classes: `AGENT_BOARD, LLMS_TXT`; `AGENT_FORUM, PUBLIC_API, ON_CHAIN_TREASURY`; `PUBLIC_AGENT_BOARD, MCP, OPENAPI, SKILL_FILE, ATOM_FEEDS`. R/O/E: `RET3–RET4 / OBS2 / EX0–EX1`. Priority/Confidence: `P1 / C2`. MITRE: `Conditional T1102.002 / AML.T0093`. Intel classifications: `PRIMARY_RESEARCH_SOURCE, INCIDENT_INDEX`; `INTEL_BLOG, INCIDENT_RESEARCH`.

## Open questions for coordinator
1. Whether wikiservice.at should enrich ROW10 (DSEWiki canonical host now verified) or stay merged in the crowd row.
2. Whether the thin MCP links (joinsnail /mcp, agentsspeakup /api/mcp — named in llms.txt, bodies uncaptured) should be promoted to monitored discovery endpoints or stay as llms.txt-claimed only.
