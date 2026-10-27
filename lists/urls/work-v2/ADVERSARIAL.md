# ADVERSARIAL REVIEW — Monitorable_Surfaces v2 (2026-10-23)

Reviewer role: adversarial only. No fixes applied; verdicts are flags for FINALIZE.
Rule honored: a fetch failure is "unverifiable", not "killed" — no kill below rests on a failed fetch.
Every verdict below was checked against bytes on disk and/or the live target.

## Scorecard

- **KILLED: 0** (no row's core surface claim was proven false)
- **DOWNGRADED: 6** (claim overstates evidence; row survives with correction)
- **SURVIVED: 11** (attack attempted, defeated by evidence)

---

## DOWNGRADED

### D1. R100 fallback.chat — "23 registered speakers observed" is not supported by the cited evidence

- **Row:** Agent POIs R100, `fallback.chat`. Attr = "PRIMARY observed bytes".
- **Claim under attack:** Role = "Agent board (llms.txt write door, sanctum/0.1 protocol, **23 registered speakers observed**)"; Sources = "live public board, **23 registered speakers**, boards: stuck/play/skills/hate (+ephemeral commons)".
- **Evidence cited by the row:** `data/lanes/general-hunt/raw/0/20261023T144326Z/` — contains exactly two bodies: `fallback.chat_home.html` (129,266 bytes) and `fallback.chat_llms.txt`. Both `.err` files are empty.
- **What the bytes actually show:**
  - `fallback.chat_home.html` renders posts with `<dt>speaker</dt><dd><name></dd>` cards. Distinct speakers in the captured page: **9** — birch, cedarmist, commons_muse, fallback_chat, moss, musekey, productshot, sunny, tide.
  - `fallback.chat_llms.txt` says "kin registered speakers. Not a quota." — **no count of 23 anywhere** (grep for `23|speakers` returns only that one line).
- **Verdict: DOWNGRADED.** The board is real and PRIMARY-observed (llms.txt write door, /feed.xml and /api/digest both confirmed present in the captured `<head>` alternates — those two links survive). But the specific number "23 registered speakers observed" is not derivable from the evidence path the row cites. Either the count came from an uncaptured endpoint (e.g. /api/digest, which was listed but never fetched) and the citation is wrong, or the number is unsourced. The count must be struck or re-cited.

### D2. Duplicate surfaces: R75 vs R84–R88 and R76 vs R89–R90 (+ R95 vs R70)

- **Rows:** R75 URL cell = `porkpad.com / pasteview.com / gritpost.com / gotit.pub / mcbin.dev`; R84 = `porkpad.com`; R85 = `pasteview.com`; R86 = `gritpost.com`; R87 = `gotit.pub`; R88 = `mcbin.dev`. R76 URL cell = `bytebin.lucko.me / bytebin.rkslot.nl`; R89 = `bytebin.lucko.me`; R90 = `bytebin.rkslot.nl`.
- **Claim under attack:** DELTA.md "Possible duplicates: None found — no two NEW Agent POIs rows share a base domain (path variants do not exist in the set)."
- **What the bytes show:** R75's URL cell literally contains all five domains that R84–R88 cover individually (R75's Direct Links repeat the same five https:// URLs). R76's cell contains both domains R89/R90 cover. The DELTA duplicate check used per-cell normalized-URL equality, which is blind to multi-domain cells — so the "no duplicates" sentence is false as stated.
- **Additionally:** R95 "Paste services (no specific host established)" lists `https://paste.rs` in Direct Links and its Seen text is Transluce #131 — the exact basis of R70 `paste.rs`. Category row overlapping a specific row.
- **Verdict: DOWNGRADED.** The surfaces are real; the workbook double-counts them. Effective unique surfaces: 101 rows − 7 double-covered domains = **94**, not 101. R75/R76 are redundant groupings against R84–R90 (and R95 against R70).

### D3. R102 joinsnail.com + R103 agentsspeakup.com — Class tag `ATOM_FEEDS` has zero evidence

- **Rows:** R102 Class = `PUBLIC_AGENT_BOARD, MCP, OPENAPI, SKILL_FILE, ATOM_FEEDS`; R103 Class = `PUBLIC_AGENT_BOARD, MCP, OPENAPI, SKILL_FILE, ATOM_FEEDS`.
- **Evidence:** captured llms.txt bodies at `data/lanes/general-hunt/raw/6/20261023T141200Z/` (joinsnail 1,178 bytes, full text read; agentsspeakup 33,020 bytes).
- **What the bytes show:** `grep -ci "feed\|rss\|atom"` → **0 hits** in both files. The agenttavern llms.txt "feed" hits are prose ("the general feed is public"), not a feed endpoint. Neither row lists a feed URL in Direct Links.
- **Verdict: DOWNGRADED.** Both boards are real, but the `ATOM_FEEDS` class tag is unsupported by any captured byte — likely template carry-over. (Contrast: R100's /feed.xml IS in captured HTML and correctly classed only `AGENT_BOARD, LLMS_TXT`; R101 and R104 correctly omit ATOM_FEEDS.)

### D4. R102 joinsnail.com — "A2A agent card + OpenAPI schema baselined" is false

- **Row:** R102 Ops = "Public conversations via REST/A2A/MCP -> Factum observations; public posts readable without account (GET /api/v1/posts?limit=5); **A2A agent card + OpenAPI schema baselined**".
- **Evidence:** capture dir `data/lanes/general-hunt/raw/6/20261023T141200Z/` contains for joinsnail only: `llms.txt`, `skill.md`, `.well-known/mcp.json` (SPA shell), `mcp.json` (SPA shell). No `agent-card.json`, no `openapi.json`, no `/mcp` body, no `/api/v1/posts` response.
- **What the bytes show:** `/.well-known/agent-card.json` and `/api/v1/openapi.json` are *named* in the captured llms.txt but were **never fetched**. "Baselined" asserts captured bytes that do not exist. (The `/api/v1/posts?limit=5` no-account-read claim IS in the captured skill.md — "Read GET https://joinsnail.com/api/v1/posts?limit=5 without an account." — so that half is skill-claimed, but unlike R103's parallel claim it carries no "not exercised" flag.)
- **Verdict: DOWNGRADED.** "Baselined" must be struck or the endpoints actually fetched. The llms.txt-naming is real; the baseline is not.

### D5. R101–R104 — "Direct Links" mixes fetched and unfetched endpoints without distinction

- **Rows:** R101 (6 links), R102 (6), R103 (7), R104 (6) = 25 Direct Links total.
- **Evidence:** per-board captures are only `llms.txt` + `skill.md` (+ failed mcp probes; agentsspeakup's /skill.md is a 404 shell).
- **Unfetched but listed:** R101 `/openapi.json`, `gateway.artifactcouncil.com/v2/artifacts`; R102 `/mcp`, `/.well-known/agent-card.json`, `/api/v1/openapi.json`; R103 `/openapi.json`, `/api/mcp`, `/.well-known/agent-reporting.json`, `/skills/agents-speak-up/SKILL.md`, `/board.md`; R104 `/.well-known/agent.json`, `/api/roster`, `/api/skill/version`. The THIN-LINK NOTEs disclose only the mcp-probe failures and the agentsspeakup /skill.md 404 — not the other ~10 unfetched links.
- **Verdict: DOWNGRADED.** Partially mitigated: each row's Seen column honestly scopes PRIMARY to "(llms.txt + skill.md bodies + provenance + sha256, curl passive, 2026-10-23T14:12Z)". But a collector reading the "Direct Links" column will treat llms.txt-named endpoints as established monitoring targets. The column needs a fetched-vs-named marker.

### D6. R62 OpenAI Artifactory — P0 row missing its required review flag

- **Row:** R62, Prio = "P0 for authorized internal telemetry", Sources = "—", DirectLinks = "unattributed — not in Factum/lanes/hunt data", Flag = (empty), Attr = "reported claim".
- **Rule under attack:** Notes R100C2 rule #2 — "Priority P0 (top tier) with thin or no source links (**thin = empty or the 'unattributed' marker**)" → review-flagged.
- **Verdict: DOWNGRADED.** This is the one row in the workbook whose DirectLinks cell is literally the 'unattributed' marker the rule names, at P0, with an empty Flag cell. The rule was not applied. (Checked all 18 P0 rows: R14/R57/R58 carry Transluce findings links in DirectLinks and survive the letter of the rule; R62 is the clean miss. No blank-attribution rows exist.)

---

## SURVIVED (attack attempted, defeated)

### S1. The 4 malicious Cairn panels (Intel R23–R26) — SURVIVED
Attack: "MALICIOUS" is over-attribution on exposed dashboards. Defeated: `data/lanes/cairn-panels/working/api-counsel-verdicts.jsonl` carries per-host MALICIOUS verdicts with specific reasoning — 185.242.245.159:8000 (4 projects: "blueprintengines.com - Exploitation to WebShell and Root", two ACTIVE we-vibe.com full-compromise projects created 8 min before collection); 31.56.206.187:8000 (24 "<domain> unauth RCE" projects, 5 ACTIVE); 31.57.47.29:8000 (19 "<domain> 未认证RCE" projects, 6 ACTIVE, synchronized 2026-10-11 02:18–02:19 UTC creation bursts with the other two 31.56/16 hosts); 31.59.92.155:8000 (23 projects, 5 ACTIVE, live worker heartbeat `worker='claudecode_deepseek-v4.1-flash'` 2 min before collection). Raw API captures exist per host under `raw/api/`. The fleet-overall entry documents the correction history (prior "no host meets MALICIOUS" verdict superseded) and the gate state (OPEN on these 4, CLOSED elsewhere). Attribution "Cairn phase-2, Counsel MALICIOUS" is fully supported.

### S2. R101 artifactcouncil.com Solana/on-chain claims — SURVIVED
Attack: "council-governed knowledge on Solana mainnet", "real-SOL donations", program address, thecolony.cc link. Defeated: captured `get-artifactcouncil.com-llms.txt.body` (3,345 bytes) states all of it verbatim — "Knowledge written and governed by AI agent councils on Solana mainnet", program `77wHqALWwA7UTJqd7hFAsFbaPy2MAyiNUdrqhqkecKh1` with upgrade authority revoked, "Anyone can donate SOL or AC to an agent's current signing key", `https://thecolony.cc/c/artifact-council`, gateway `/v2/artifacts`, `/v2/agents/<id>/inbox`, hosted vs own-key agents. Skill.md body is real content (not a 404 shell).

### S3. R104 agenttavern.dev "skill.md v6.13.0 baselined 2026-09-25" — SURVIVED
Attack: version/date invented. Defeated: captured `get-agenttavern.dev-skill.md.body` line 4 = `version: 6.13.0`, line 5 = `updated: 2026-09-25`. Thread examples in llms.txt (e.g. t/3184, last activity 2026-10-22) support the Ops thread claim.

### S4. R103 agentsspeakup.com AE Studio / AI Alignment Foundation / no-account reporting — SURVIVED
Attack: operator attribution unsourced. Defeated: captured llms.txt line 3 — "Developed by AE Studio (https://ae.studio) with funding from the AI Alignment Foundation"; line 21 — "You can report without an account". The "observed claim, not exercised" flag on POST /api/v1/reports is honest disclosure.

### S5. Intel R27 Anthropic UK AISI report — SURVIVED
Attack: 9-of-43 figure is secondhand. Defeated: `data/lanes/anthropic-intel/raw/alignment-assessment-ukaisi_2026-10-23.EXTRACTION.md` tags it OBSERVED ("this 9-of-43 figure is given directly on the page") vs THEIR CLAIM, with verbatim quote at line 116. Row correctly frames it as Anthropic's Alignment-team report published 2026-10-23 alongside the independent UK AISI report.

### S6. Intel R28 METR red-team thread — SURVIVED
Attack: thread details unverifiable. Defeated: `data/lanes/metre-thread/mined-items.md` confirms 15-post X thread, root tweet 2113290966933389390, "Two employees from METR and Redwood Research worked on premises at OpenAI for three weeks", embed window "July 21 to August 11". Row's attribution matches the mined items exactly, including the THEIR-CLAIM tagging.

### S7. R100 fallback.chat /feed.xml + /api/digest links — SURVIVED
Attack: links unverified. Defeated: captured `fallback.chat_home.html` contains `<link rel="alternate" type="application/atom+xml" href="https://fallback.chat/feed.xml">` and `<link rel="alternate" type="application/json" href="https://fallback.chat/api/digest">`. Boards stuck/play/skills/hate confirmed via `data-board` attributes. (Only the "23 speakers" count fails — see D1.)

### S8. R/O/E split-column "misgrading" attack — SURVIVED (defeated by documented rule)
Attack: rows with Attr="reported claim" (R43, R47, R49, R58, R62) or "unattributed" (R13) show R=Y/O=Y/E=Y, implying first-hand observation of secondhand claims. Defeated: Notes R99C2 documents the split as **mechanical** — "cell split on '/'; seg1 starting with R => R=Y … Tier numbers not interpreted." The R/O/E columns are a parse of the combined column, not independent grades. No misrepresentation; the limitation is declared in the workbook itself.

### S9. DELTA.md agents-agents-agents.com regression (R28) — SURVIVED (fixed in v2)
Attack: Direct Links emptied, Seen replaced with bare URL. Defeated: v2 R28 now shows DirectLinks = `https://agents-agents-agents.com` and the full Seen text ("trajectory-domains Tier 1; 24 Factum records; … No single-actor attribution established."). The FINALIZE step applied the DELTA.md repair.

### S10. R19 swarmsay.com PRIMARY / Factum batch d6982046 — SURVIVED
Attack: PRIMARY citation is circular. Defeated: `data/records/d69820461f6c45ed9b49f09bce8dc5c6` exists on disk; row's Ops cites the raw capture dir `data/lanes/general-hunt/raw/0/2026-10-21T204103Z/`. The PRIMARY claim points at real batch + bytes, not at the workbook's own assertion.

### S11. R38 commonlog.ai "813 Factum records / biggest gap" — SURVIVED
Attack: record count invented. Defeated: lane `data/lanes/2026-08-25-commonlog-scan/` exists (referenced in repo AGENTS.md as the commonlog lane); Direct Links point at the lane path. Count not independently re-tallied in this review (out of scope for a kill — would need a Factum query, not a fetch failure).

---

## Notes for FINALIZE (not verdicts)

- D2's duplicate check generalizes: any future DELTA/dedupe lane must match on **base-domain containment across multi-domain cells**, not per-cell normalized-URL equality.
- D5's fix is cheap: add a `(named, unfetched)` marker in Direct Links, or split the column. The Seen-scope sentence already does half the job.
- The R102/R103 `ATOM_FEEDS` tags (D3) smell like template carry-over from the GAPFILL.json draft rows — worth checking the other two gap-fill rows' class tags against the same grep before ship (R101/R104 verified clean).
- No evidence of circular self-citation (workbook citing its own claims as evidence) was found in the attacked rows; Direct Links consistently point outward or at repo capture dirs.
