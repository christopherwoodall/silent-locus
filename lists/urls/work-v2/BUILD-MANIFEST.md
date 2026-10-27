# BUILD-MANIFEST — monitorable-surfaces-ENRICHED-v2.xlsx gap-fill verification

Built 2026-10-23 (FINALIZE lane). One line per gap-fill row: evidence path exists (Y/N);
bytes + PROVENANCE + sha256 present (Y/N). All paths repo-relative under
`~/workspace/silent-locus/`. Byte counts and file names verified against the live tree
2026-10-23 ~12:15 America/Chicago.

## Agent POIs gap-fill rows (sheet rows 100–104)

### Row 100 — fallback.chat
- Evidence path: `data/lanes/general-hunt/raw/0/20261023T144326Z/` — **exists: Y**
- Bytes present: **Y** — `fallback.chat_home.html` (129,266 bytes), `fallback.chat_llms.txt`
  (captured 2026-10-23T14:46–14:47Z, curl passive, HTTP 200)
- PROVENANCE: **Y** — `fallback.chat_home.html.PROVENANCE.txt`, `fallback.chat_llms.txt.PROVENANCE.txt`
  (curl GET, passive, 2026-10-23T14:46Z)
- sha256: **Y** — `fallback.chat_home.html.sha256`, `fallback.chat_llms.txt.sha256`
- Caveat: only the home.html + llms.txt bodies were retained; the "23 registered speakers"
  claim in the workbook is NOT derivable from these bytes (9 distinct speakers rendered) —
  corrected in the workbook 2026-10-23 FINALIZE (adversarial D1).

### Rows 101–104 — Tier-1 board discovery-endpoint baselines (lane-6, 2026-10-23)
- Evidence path: `data/lanes/general-hunt/raw/6/20261023T141200Z/` — **exists: Y**
- 48 capture files total (4 hosts × 4 endpoint bodies × 3 files: body + .PROVENANCE.txt + .sha256)
  — **present: Y** for every host
- Per host (llms.txt + skill.md bodies real content; mcp probes recorded as SPA shells / not-found):
  - artifactcouncil.com (row 101): llms.txt (3,345 bytes), skill.md, mcp.json, .well-known/mcp.json + provenance + sha256 — Y
  - joinsnail.com (row 102): llms.txt (1,178 bytes), skill.md, mcp.json (SPA shell), .well-known/mcp.json (SPA shell) + provenance + sha256 — Y
  - agentsspeakup.com (row 103): llms.txt (33,020 bytes), skill.md (Next.js 404 shell), mcp.json (SPA shell), .well-known/mcp.json (SPA shell) + provenance + sha256 — Y
  - agenttavern.dev (row 104): llms.txt, skill.md (version 6.13.0, updated 2026-09-25), mcp.json (not found), .well-known/mcp.json (not found) + provenance + sha256 — Y
- Caveat: no machine-readable MCP manifest was captured for rows 102–104 (llms.txt-claimed
  only); `ATOM_FEEDS` removed from rows 102–103 Class (zero evidence); rows 101–104 Direct
  Links mix fetched bodies with llms.txt-named-but-unfetched endpoints — disclosed via
  Review flag (adversarial D3/D4/D5), links preserved.

## Intelligence sheet gap-fill rows (sheet rows 27–28)

### Intel row 27 — Anthropic UK AISI alignment assessment
- Evidence path: `data/lanes/anthropic-intel/raw/alignment-assessment-ukaisi_2026-10-23.EXTRACTION.md` — **exists: Y** (29,367 bytes)
- Bytes + provenance: **Y** (extraction file; content spot-check confirms the Mythos 5 / 9-of-43 material)

### Intel row 28 — METR red-team pilot thread
- Evidence path: `data/lanes/metre-thread/mined-items.md` — **exists: Y** (15,757 bytes)
- Bytes + provenance: **Y** (spot-check confirms tweet id 2113290966933389390, 15-post thread, July 21–August 11 embed window)

## Summary

| Gap-fill row | Path exists | Bytes | PROVENANCE | sha256 |
|---|---|---|---|---|
| Agent POIs 100 (fallback.chat) | Y | Y (2 bodies) | Y | Y |
| Agent POIs 101 (artifactcouncil.com) | Y | Y (4 bodies) | Y | Y |
| Agent POIs 102 (joinsnail.com) | Y | Y (4 bodies) | Y | Y |
| Agent POIs 103 (agentsspeakup.com) | Y | Y (4 bodies) | Y | Y |
| Agent POIs 104 (agenttavern.dev) | Y | Y (4 bodies) | Y | Y |
| Intel 27 (Anthropic UK AISI) | Y | Y (extraction md) | n/a (lane extraction file) | n/a |
| Intel 28 (METR thread) | Y | Y (mined-items md) | n/a (lane mined file) | n/a |

All 7 gap-fill evidence paths exist on disk. No row's "PRIMARY observed bytes" assertion
rests on a missing path.
