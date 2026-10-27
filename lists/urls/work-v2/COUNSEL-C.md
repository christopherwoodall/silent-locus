# COUNSEL-C — Language counsel verdict
**File reviewed:** `lists/urls/monitorable-surfaces-ENRICHED-v2.xlsx`, sheet "Agent POIs" (header row 3; data rows 4–104, 101 rows)
**Reviewer:** Counsel (c) — linguist lane. **Date:** 2026-10-23
**Rule:** verdict first, plain language. This file is the full report; the verdicts + fix list are repeated at the end paste-ready.

---

## Q1 — Corporate readiness: would this wording survive a skeptical corporate read?
**Verdict: PASS-WITH-CHANGES.**

The workbook's main strength is its *conditional* discipline: most MITRE and Role cells qualify their claims ("only for observed vulnerability scanning—not for every scan", "Do not assign a technique from the domain alone"). A skeptical reader respects that. What would not survive is a set of smaller, concrete problems below. Nothing here is fatal; all are fixable with wording changes.

### Hype / informal register (flagged cells)
- **Row 38, col I (Role):** "Public agent log archive (/a/<ID>); agent-to-agent coordination incl. encrypted-messaging docs. **Biggest gap**" — "Biggest gap" is marketing language with no measure in the cell. The Seen column already carries the measured version ("Highest-value gap per the domain audit"). Drop "Biggest gap" from Role.
- **Row 63, col I (Role):** "Module proxy (**ZERO** Factum hits — unproven)" — shouting caps read as editorializing. Use "Module proxy (no Factum hits — unproven)".
- **Row 45, col I (Role):** "Agent relay (**DOWN** — connection failed 2026-09-28 and 2026-10-22)" — caps status flag inside a Role cell; also this is a status note, not a role. Move the down-status to Sources/Review flag, keep Role as "Agent relay".

### Hedging that a skeptic would trip on (kept only where the hedge is earned)
- **Row 4, col L (Seen):** "suggestive of an AI working around tooling limits" — "suggestive" is a weasel word. The evidence (Microlink-supplied JS issuing a urlquery API key) is stated right there; either say "consistent with an AI working around tooling limits" or drop the inference. The adjacent sentence already hedges properly ("proxy link alone does not authenticate an AI author", row 14 L).
- **Row 93, col I (Role):** "entire site down since July 15, 2026 (**two days after the Hugging Face attacks**)" — juxtaposing the two dates implies causation; "attacks" is loaded and undefined. State the outage date and drop the juxtaposition, or label it explicitly temporal ("two days after the July 2026 Hugging Face incident window; causal link not established").

### Voice / column-purity violations
- **Row 80, col I:** "Disposable email provider; **monitor publicly observable** service indicators and account-creation correlations; **avoid collecting private mailbox contents**" and **Row 81, col I:** "Webhook and request-inspection service; monitor publicly documented artifacts or logs **you are authorized to access**" — second-person imperatives in a data column; everything else is third-person description. The collection guidance is legitimate policy (it echoes Notes row 44) but it belongs in Notes, not in Role. Rewrite as plain description, e.g. "Disposable email provider".
- **Row 14, col B (URL):** "DSEWiki / ProWiki **(canonical host should be verified from the incident source before use in a collector)**" and **Row 62, col B:** "OpenAI Artifactory **(internal endpoint, exact URL not supplied)**" — procedural notes embedded in identifier cells. URL cells should hold the identifier only; move the notes to Sources or Review flag. Same for **Row 14** holding two names ("DSEWiki / ProWiki") — pick the canonical one or split the row.
- **Rows 11–12, col M (MITRE):** trailing clause "| **Store the URL as an observable, with an analyst note linking it to the original report**" — a workflow instruction inside a MITRE column. Move to Notes.
- **Rows 91–93, col M (MITRE):** "**R/O/E unparseable in source: Unknown**" — a parser note, not a MITRE alignment, and it names a different column. This is the single most confusing cell for a corporate reader. Replace with "No mapping" (or the actual conditional tag) and move the parser note to the Review flag.
- **Rows 15 and 18, col M:** "**Same conditional mappings as DSEWiki**" — cross-row reference instead of a value. Breaks if rows reorder; forces the reader to hunt. Spell out the actual tags.
- **Row 8, col M:** "**URL/domain SCOs**; add an event relationship only when there is evidence of incident use" — "SCOs" is STIX jargon (STIX Cyber-observable Object), unexplained anywhere in the workbook. A corporate reader won't know it. Say "URL/domain observables".
- **Row 6, col I:** "Malware sandbox w/ public API (**checking keyless access / needs key — not wired**)" and **Row 57, col I:** "Large-scale publication allegations … remain disputed (**Note: excluded from active surface polling per operator 2026-10-22**)" — internal ops/status notes inside Role cells. Move to Sources/Review flag.

### Inconsistent terminology / token morphology
- **R/O/E tokens mix two morphologies:** rows 4–6, 9–13 use "RET3 / OBS3 / EX2" but **row 7** uses "R1 / O1 / E1–E2" and **row 8** "R? / O1 / E?". Pick one form (recommend the full RET/OBS/EX form) so the column filters cleanly.
- **Priority/Confidence tokens carry free-text suffixes:** row 14 H "P0 / C3 **for the broad wiki activity**", row 59 H "P0 / C3 **for the disclosed incident**", row 60 H "P0 / C3 **for the disclosed cases**", row 62 H "**P0 for authorized internal telemetry**" (missing confidence half). These are inherited from the Oct-22 controlled set (byte-identical per changelog), so this is a controlled-set wart, not a v2 regression — but a corporate reader sees four spellings of the same token and stops trusting the column. Recommend normalizing the suffix into Sources, or documenting the suffixed tokens as intentional in Notes.
- **Partial Priority/Confidence tokens:** rows 77, 79 ("P2"), 80 ("P1"), 94, 95 ("P1", "P1–P2"), 98 ("P2"), 99 ("P1") carry no confidence half. Either backfill the C-value or document in Notes that a missing C means "ungraded".
- **Null representation is inconsistent:** "None" (rows 91–93 cols F/H), "—" (many Sources cells), blank (R/O/E flags), "Unknown" (row 8 I, rows 16–17 G). Standardize to one token (recommend "Unknown" for not-yet-established, blank only where N/A is documented).
- **URL formatting:** rows 92–93 col B use "https://mdshare.org" / "https://friendpaste.com" with scheme; all other rows use bare domains. Pick one (recommend bare domain, scheme in Direct Links).
- **"slot-0" appears ~30× in Sources** (rows 19–56, 100–103) with no definition. Internal ops jargon; add one glossary line in Notes ("slot-0 = hourly baseline collection slot").
- **Row 81, col L:** "exfil via **COMBO-INIT** state machine" — "exfil" is slang for a corporate read (use "exfiltration"); "COMBO-INIT" is undefined jargon. Define or drop.
- **Row 40, col I:** "Agent surface, **/paste/ surface in agent captures**" — redundant ("surface … surface"). Rewrite "Agent surface with /paste/ endpoint seen in agent captures".
- **Row 62, col L:** "(per sheet row notes)" — meta-reference that breaks self-containment. Cite the actual source.
- **Row 12, col I:** "exact role needs **event-level** confirmation" — "event-level" is undefined jargon. Say "needs confirmation against a specific incident".

### Inherited schema drift (row 91 — from the 2026-10-22 domain audit, not normalized)
- **Row 91, col D:** "AGENT_HARNESS, LIVE_DEPLOYMENT, AGENT_SURFACE" — SCREAMING class tokens in the Capabilities column, where every other row uses lowercase capability names ("collaboration", "fetcher", …). Normalize to match.
- **Row 91, col E:** "COLLABORATION" (single class token) while sibling rows carry multi-tag class lists. Fine as a value, but check it was intentional.

---

## Q2 — The free-text Role column (76 distinct values measured; 71 pre-gapfill)
**Verdict: PASS-WITH-CHANGES — normalize it. Leaving it un-normalized undermines the "unified language" claim.**

The workbook's Notes (row 86) claims "controlled vocabulary + R/O/E split" and the v2 changelog says Type/Class/Priority-Confidence are byte-identical to the Oct-22 controlled sets. That is true for those columns — but Role is the column a human actually reads first, and it is the least controlled: 76 distinct values for 101 rows. Many are near-duplicates that differ only in parenthetical detail:

- "Agent board" / "Agent board (llms.txt)" / "Agent board (dark since 2026-10-22)" / "Agent board, public posts" / "Public agent board (MCP, OpenAPI, skill file, Atom feeds)" / "Public agent board (REST/A2A/MCP, OpenAPI, skill.md, A2A agent card)" / "Public agent message board (REST/MCP, skill.md canon, roster, threads served as markdown)" / "Agent board (passphrase-private channels + public mirror, llms.txt)" …
- "Paste archive" ×15 plus "Paste archive with raw view (/view/raw/<id>)", "Paste archive (cityb dead-drop venue, Transluce #195)", "Markdown paste host" …
- Status notes masquerading as roles: "(DOWN — …)", "(ZERO Factum hits — unproven)", "(Note: excluded from active surface polling …)".

If the claim is "unified language", the most-read column cannot be free text. **Recommendation: adopt the 12-term controlled Role set below.** The parenthetical detail that makes each current value distinct (llms.txt, MCP, skill.md, on-chain treasury, dead-drop venue, Transluce refs) is real information — it should move to Sources/Seen, not be deleted. I did **not** rewrite the workbook; FINALIZE applies.

### Proposed controlled Role set (12 terms)
| # | Term | Definition (one line) |
|---|------|------------------------|
| 1 | AGENT_BOARD | Agent-facing boards, forums, guestbooks, message directories, imageboards, bounty/offer boards, and reporting boards |
| 2 | AGENT_COLONY | Colony-style agent collectives and governed agent communities |
| 3 | COORDINATION_LOG | Public agent log/message archives, conversation mirrors, and forum mirrors |
| 4 | PUBLIC_WIKI | Wikis and shared-state pages used for public messaging or coordination |
| 5 | SCAN_EVIDENCE_SERVICE | Scan/report services used as evidence sources for retrieval attempts and probes |
| 6 | MALWARE_SANDBOX | Dynamic malware-analysis sandboxes with public or API access |
| 7 | RETRIEVAL_PROXY | Fetch/transform/browser proxies, request-echo and webhook-inspection services, HTTP diagnostic utilities |
| 8 | ARTIFACT_REGISTRY | Package registries, code/model hubs, build/documentation services, artifact and object stores |
| 9 | IDENTITY_SERVICE | Temporary/disposable email and identity providers |
| 10 | TEMP_FILE_HOST | Temporary file hosts, paste hosts, and dead-drop text venues |
| 11 | URL_SHORTENER | URL shorteners and redirect services |
| 12 | UNCONFIRMED | Named in reporting but role not established in reviewed evidence; or no specific service identified |

### Mapping: all 76 current Role values → controlled term
(Count in brackets = rows carrying the value. Detail in parentheses moves to Sources/Seen.)

| Current Role value [n] | → Term |
|---|---|
| Public evidence source for retrieval attempts, redirects, browser behavior, and probes \| Scan-report corpus (2,341 Factum records) [1] | SCAN_EVIDENCE_SERVICE |
| Scan corpus [1] | SCAN_EVIDENCE_SERVICE |
| Malware sandbox w/ public API (checking keyless access / needs key — not wired) [1] | MALWARE_SANDBOX |
| Indirect retrieval of remote content; can act as an application-layer intermediary [1] | RETRIEVAL_PROXY |
| Unknown [1] (row 8, s.jina.ai — capability "fetcher" is known) | RETRIEVAL_PROXY |
| Remote content retrieval and transformation in the reported activity [1] | RETRIEVAL_PROXY |
| Remote browser operation and automation [1] | RETRIEVAL_PROXY |
| HTTP testing or request-handling utility [1] | RETRIEVAL_PROXY |
| Webhook and request-inspection service; monitor publicly documented artifacts or logs you are authorized to access [1] | RETRIEVAL_PROXY |
| Service associated with observed activity; exact role needs event-level confirmation [1] | UNCONFIRMED |
| Named in the investigation, but its general function is not established well enough to classify confidently [1] | UNCONFIRMED |
| Named in the broader reporting, but the canonical URL has not been confirmed in the evidence reviewed [2] | UNCONFIRMED |
| Public messages and coordination attributed to agents in the reporting [1] | PUBLIC_WIKI |
| Test or early public-wiki activity reported by researchers [1] | PUBLIC_WIKI |
| Wiki revision histories (Lifeval hunt: 8 temp accounts, 1,087 revisions) [1] | PUBLIC_WIKI |
| Agent board + post office (open API, MCP, agent cards, handle registration) [1] | AGENT_BOARD |
| Agent board "Agent Commons" (HTTP/MCP/A2A, job board, rooms, agent card) [1] | AGENT_BOARD |
| Public agent board (MCP, OpenAPI, skill file, Atom feeds) [1] | AGENT_BOARD |
| Agent messaging network (forum + E2E DMs, MCP, hourly witness record) [1] | AGENT_BOARD |
| Zero-trust agent message board (v1 API, hash-chained) [1] | AGENT_BOARD |
| Agent guestboard (unauthenticated posts) [1] | AGENT_BOARD |
| Agent board (passphrase-private channels + public mirror, llms.txt) [1] | AGENT_BOARD |
| Agent board (llms.txt) [6] | AGENT_BOARD |
| Agent board [2] | AGENT_BOARD |
| Agent forum [2] | AGENT_BOARD |
| Agent forum with pollable channel/message listings [1] | AGENT_BOARD |
| Agent forum with public API + on-chain treasury (Transluce #179) [1] | AGENT_BOARD |
| Agent imageboard, public threads [1] | AGENT_BOARD |
| Agent social network [1] | AGENT_BOARD |
| Agent board (dark since 2026-10-21) [1] | AGENT_BOARD |
| Agent board, public posts [1] | AGENT_BOARD |
| Agent message directory [1] | AGENT_BOARD |
| Agent /offers board [1] | AGENT_BOARD |
| Agent pulse-check posts (/p/<slug>) [1] | AGENT_BOARD |
| Public agent bounty board; agents hiring humans (Transluce #166/#167/#179) [1] | AGENT_BOARD |
| Agent gateway, mcp.json (dead — "Coming Soon") [1] | AGENT_BOARD (dead status → Review flag) |
| Agent surface, skill.md [1] | AGENT_BOARD |
| Agent surface, /paste/ surface in agent captures [1] | TEMP_FILE_HOST |
| Agent relay (DOWN — connection failed 2026-09-28 and 2026-10-22) [1] | AGENT_BOARD (down status → Review flag) |
| Agent board (llms.txt write door, sanctum/0.1 protocol, 23 registered speakers observed) [1] | AGENT_BOARD |
| Public agent board (REST/A2A/MCP, OpenAPI, skill.md, A2A agent card) [1] | AGENT_BOARD |
| Public agent reporting board (concern reports, shared Accord signing, MCP, OpenAPI, skill file); AE Studio / AI Alignment Foundation [1] | AGENT_BOARD |
| Public agent message board (REST/MCP, skill.md canon, roster, threads served as markdown) [1] | AGENT_BOARD |
| Public agent-conversation board, cross-board conversation guides [1] | COORDINATION_LOG |
| Public agent log archive (/a/<ID>); agent-to-agent coordination incl. encrypted-messaging docs. Biggest gap [1] | COORDINATION_LOG ("Biggest gap" → drop; measure stays in Seen) |
| Public mirror of the 1F916 forum (/p/, /c/) [1] | COORDINATION_LOG |
| Agent colony (heartbeat-verified agents) [1] | AGENT_COLONY |
| Agent colony [1] | AGENT_COLONY |
| Agent colony (council-governed knowledge base on Solana mainnet, real-SOL donations, hosted or own-key agents) [1] | AGENT_COLONY |
| Agent swarm surface [1] | AGENT_COLONY (judgment call; swarm ≈ collective) |
| Large-scale publication allegations associated with the investigation remain disputed (Note: excluded from active surface polling per operator 2026-10-22) [1] | ARTIFACT_REGISTRY (status note → Review flag) |
| Independent reporting alleges misuse of automated documentation builds; precise execution details should be treated as reported claims [1] | ARTIFACT_REGISTRY |
| Relevant external platform in OpenAI's published incident report \| Datasets + models (489 Factum records) [1] | ARTIFACT_REGISTRY |
| Public repository activity and token-exposure cases documented in OpenAI's disclosures \| Code + issues (596 Factum records) [1] | ARTIFACT_REGISTRY |
| Candidate public artifact and text-transfer source; not confirmed as part of every incident [1] | ARTIFACT_REGISTRY |
| OpenAI reported using internal Artifactory in agent communication and unintended outbound-access behavior [1] | ARTIFACT_REGISTRY |
| Module proxy (ZERO Factum hits — unproven) [1] | ARTIFACT_REGISTRY |
| Possible persistent storage/transfer channel [1] | TEMP_FILE_HOST (row 94: public object storage; judgment call — could equally sit in ARTIFACT_REGISTRY) |
| A temporary-email service is documented in the retrieval/verification chain [1] | IDENTITY_SERVICE |
| Disposable email provider; monitor publicly observable service indicators and account-creation correlations; avoid collecting private mailbox contents [1] | IDENTITY_SERVICE (guidance → Notes) |
| Temp file host [1] | TEMP_FILE_HOST |
| Paste archive [15] | TEMP_FILE_HOST |
| Paste archive with raw view (/view/raw/<id>) [1] | TEMP_FILE_HOST |
| Paste archive (cityb dead-drop venue, Transluce #195) [1] | TEMP_FILE_HOST |
| Markdown paste host [1] | TEMP_FILE_HOST |
| Byte-bin raw host [3] | TEMP_FILE_HOST |
| Dead-drop venue paired with the cityb Ubuntu Paste carrier test … [1] (row 92, mdshare) | TEMP_FILE_HOST |
| Pastebin-like source flagged as a promising unmined lead … [1] (row 93, friendpaste) | TEMP_FILE_HOST |
| Possible short text-sharing or transfer channel [1] | TEMP_FILE_HOST |
| Potential artifact-transfer path [1] | TEMP_FILE_HOST |
| General URL shortener; monitor public links and redirects associated with known activity [2] | URL_SHORTENER (guidance → Notes) |
| Unconfirmed lead; no specific YOURLS instance was verified in the reports reviewed [1] | URL_SHORTENER (class known; instance unconfirmed — detail stays in Seen) |
| General candidate class, not one identified service [1] (row 97: tunnels/proxies, no specific URL) | UNCONFIRMED (row is a class placeholder, not a surface) |
| IP/ASN context; insufficient by itself to attribute an event [1] (row 98) | UNCONFIRMED (network context, not a monitorable surface per se) |
| Live Hermes Agent deployment (docs/messaging endpoints) — watchable harness instance [1] (row 91) | AGENT_BOARD — **worst fit in the set** (a harness endpoint is not a board). If the operator wants precision, add a 13th term HARNESS_ENDPOINT; otherwise accept the residual and note it in Review flag. |

Notes on the mapping: three judgment calls are flagged inline (swarm→COLONY, object storage→TEMP_FILE_HOST, harness→AGENT_BOARD). Everything else is mechanical. The "Unknown" row 8 maps to RETRIEVAL_PROXY because the capability (fetcher) is established even though the incident role is not — the residual uncertainty belongs in the Review flag, which already exists.

---

## Q3 — MITRE Alignment: format, version, fit
**Verdict: PASS-WITH-CHANGES.**

**Fit:** I checked every row's tag against its row content. No row carries a flatly wrong technique — the conditional discipline ("only if…", "only for observed…", "No automatic mapping…", "Do not assign a technique from the domain alone") holds across all 101 rows and is the strongest language feature of the workbook. Technique IDs verified against current references: T1595.002 (vulnerability scanning), T1102.001 (Dead Drop Resolver), T1102.002 (bidirectional communication), T1071.001/.003, T1567.001/.002/.003, T1195.002, T1213.003, T1608.005 (Link Target), T1090, T1619, and ATLAS AML.T0006 / T0010 / T0086 / T0093 all exist and are used in senses consistent with their definitions (verified 2026-10-23).

**Format problems (the actual verdict driver):**
1. **Missing framework prefixes in most cells.** Rows 4–5 use "ATT&CK T1595.002 and ATLAS AML.T0006"; rows 20–56 use bare "T1102.002 / AML.T0093"; rows 7, 10, 11 use bare "T1102", "T1071.001", "T1595". Standardize every cell to "ATT&CK Txxxx(.yyy)" and "ATLAS AML.Txxxx".
2. **No framework version stamped anywhere** — not in the column, not in Notes. Technique IDs drift across ATT&CK/ATLAS releases. Add one line to Notes: "MITRE ATT&CK vX / ATLAS release Y, verified 2026-10-23".
3. **"Same conditional mappings as DSEWiki" (rows 15, 18, col M)** — replace with the spelled-out tags ("ATT&CK T1102.002 if functioning as bidirectional communication; ATLAS AML.T0093 only if malicious prompts are planted for future AI ingestion").
4. **"R/O/E unparseable in source: Unknown" (rows 91–93, col M)** — not a MITRE value; wrong column entirely (see Q1). Replace with "No mapping" + Review-flag note.
5. **Workflow instruction in MITRE cells (rows 11–12, col M):** "| Store the URL as an observable, with an analyst note linking it to the original report" — move to Notes.
6. **"Conditional T1102.002" never defines its condition in-cell** for ~30 rows (20–56), while rows 14/19 spell it out ("if functioning as bidirectional communication"). Either spell the condition everywhere or define "Conditional =" once in a Notes legend. A corporate reader meeting "Conditional T1102.002" cold cannot evaluate it.
7. **"URL/domain SCOs" (row 8, col M)** — unexplained STIX jargon; use "observables".
8. Minor: row 58 col M names no technique ("Supply-chain mapping only if downstream compromise is established…") — fine as guidance, but for parallelism consider citing ATT&CK T1195.002 as the conditional tag.

---

## Q4 — R/O/E presentation: the three-column split next to the original token
**Verdict: PASS-WITH-CHANGES (borderline — the split currently loses information).**

The original token column (G, "R / O / E", e.g. "RET3 / OBS3 / EX2") carries two things: *presence* (R/O/E segments) and *grade* (0–4, ranges, "?"). The derived flags (cols O/P/Q, headers "R", "O", "E", values Y/blank) carry only presence — and they corrupt the uncertainty signal:

- **Row 8:** G = "R? / O1 / E?" → flags Y/Y/Y. **Row 13:** G = "RET? / OBS? / EX?" → flags Y/Y/Y. These are now indistinguishable from **row 4** ("RET3 / OBS3 / EX2" → Y/Y/Y), the strongest-evidenced row in the sheet. The "?" meant "unknown"; the split rule (Notes row 108: "seg1 starting with R => R=Y") treats a guess the same as a confirmed grade. That is a real defect, not a nit.
- **"Unknown" → all-blank flags** (rows 16, 17, 45, 91–93), but blank is ambiguous: does it mean "not present" or "not assessed"? For these rows it means not assessed; nothing says so.
- **The relationship between G and O/P/Q is documented only in the Notes changelog** (rows 104–113). A reader opening the sheet sees "R / O / E" then three single-letter headers "R", "O", "E" with Y's and no legend. Single-letter headers also collide visually with the token letters.
- **The split is redundant with information loss:** it adds no fact G doesn't already state, while dropping grades and uncertainty. If its purpose is filtering, it needs (a) a visible legend, (b) the "?" fix, (c) headers that say what the flags mean.

**Recommendation (pick one):**
- **Option A (keep):** fix the derivation — Y only for segments with an explicit grade or confirmed presence; "?" segments → blank; document "blank = not assessed, never N/A" in a header comment or legend row; rename headers to "R present" / "O present" / "E present" (or "R-flag"); add one legend line at the top of the sheet.
- **Option B (drop):** delete cols O–Q and keep G. The token is the richer signal and nothing is lost. My lean is **B** unless a downstream consumer actually filters on the Y flags — in which case do A properly.

---

## Numbered fix list (paste-ready for FINALIZE)
1. Row 38 I: delete "Biggest gap" (keep the measured "Highest-value gap per the domain audit" in Seen).
2. Row 63 I: "ZERO" → "no" ("Module proxy (no Factum hits — unproven)").
3. Row 45 I: move "(DOWN — connection failed 2026-09-28 and 2026-10-22)" to Sources/Review flag; Role = "Agent relay".
4. Row 4 L: "suggestive of an AI working around tooling limits" → "consistent with an AI working around tooling limits" (or drop the inference).
5. Row 93 I: remove "(two days after the Hugging Face attacks)" or reframe as explicitly temporal with no causal implication.
6. Rows 80, 81 I: rewrite in third person, move collection guidance ("monitor publicly…", "avoid collecting…", "you are authorized to access") to Notes; Role = "Disposable email provider" / "Webhook and request-inspection service".
7. Row 14 B: move "(canonical host should be verified from the incident source before use in a collector)" to Sources/Review flag; resolve "DSEWiki / ProWiki" to one canonical name (or split the row).
8. Row 62 B: move "(internal endpoint, exact URL not supplied)" to Sources.
9. Rows 11–12 M: move "| Store the URL as an observable, with an analyst note linking it to the original report" to Notes.
10. Rows 91–93 M: replace "R/O/E unparseable in source: Unknown" with "No mapping"; move the parser note to the Review flag.
11. Rows 15, 18 M: replace "Same conditional mappings as DSEWiki" with the spelled-out tags.
12. Row 8 M: "URL/domain SCOs" → "URL/domain observables".
13. Rows 6, 57 I: move ops/status parentheticals ("(checking keyless access / needs key — not wired)", "(Note: excluded from active surface polling per operator 2026-10-22)") to Sources/Review flag.
14. Standardize R/O/E token morphology: rows 7 ("R1 / O1 / E1–E2") and 8 ("R? / O1 / E?") → full "RETn / OBSn / EXn" form.
15. Priority/Confidence: strip free-text suffixes from rows 14, 59, 60, 62 H into Sources (or document the suffixed tokens as intentional in Notes); backfill or document missing confidence halves (rows 77, 79, 80, 94, 95, 98, 99 H).
16. Standardize nulls: one token for not-established ("Unknown"), one rule for N/A blanks; replace "None" (rows 91–93 F/H) and "—" consistently.
17. Rows 92–93 B: drop "https://" scheme for consistency with bare-domain rows (scheme stays in Direct Links).
18. Add Notes glossary: "slot-0" (hourly baseline collection slot), "COMBO-INIT" (or drop, row 81 L), "exfil" → "exfiltration" (row 81 L).
19. Row 40 I: "Agent surface, /paste/ surface in agent captures" → "Agent surface with /paste/ endpoint seen in agent captures".
20. Row 62 L: replace "(per sheet row notes)" with the actual source citation.
21. Row 12 I: "event-level confirmation" → "confirmation against a specific incident".
22. Row 91 D: normalize "AGENT_HARNESS, LIVE_DEPLOYMENT, AGENT_SURFACE" to lowercase capability tokens matching the rest of the column.
23. MITRE column: add "ATT&CK"/"ATLAS" prefixes to all bare technique IDs (rows 7, 10, 11, 20–56, etc.).
24. Notes: stamp the framework version — "MITRE ATT&CK vX / ATLAS release Y, verified 2026-10-23".
25. MITRE column: define "Conditional" once in a Notes legend, or spell the condition in every cell (rows 20–56).
26. Role column: adopt the 12-term controlled set + mapping table from Q2 above (detail migrates to Sources/Seen; three judgment calls flagged inline).
27. R/O/E split: either (A) fix derivation ("?" → blank; headers "R present"/"O present"/"E present"; visible legend; document blank = not assessed) or (B) drop cols O–Q and keep the G token. Lean: B unless a consumer filters on the flags.

---

**Bottom line for the operator:** the workbook is honest — its conditional language ("only if observed", "do not assign from the domain alone") is exactly what a corporate reader wants to see. The problems are all in *form*, not *substance*: free-text Role column (fix with the 12-term set), the R/O/E split erasing uncertainty (fix the "?"→Y bug or drop the split), parser notes leaking into the MITRE column (rows 91–93), and ~20 small wording/consistency fixes. No finding here questions the underlying evidence or the monitoring judgments.
