# Language Counsel Review — Monitorable Surfaces v3 (LANG-COUNSEL-v3)

Reviewer: Language counsel (linguist). Date: 2026-10-23. Workbook: `monitorable-surfaces-ENRICHED-v3.xlsx` (read-only; nothing in the .xlsx was changed).

## VERDICT: PASS-WITH-CHANGES

The v3 build did what it said: the self-referential scrub is real (the word "Factum" appears nowhere in the visible sheets), the 12-term Role set is applied to all 101 Agent-POI rows with an honest mapping table, row 14 is resolved to "DSEWiki" with evidence cited, and the R/O/E '?' fix plus the "Conditional" legend from Counsel-C both landed. The workbook's strongest feature — conditional MITRE discipline ("only if observed", "do not assign from the domain alone") — holds across every row. No hype words, no first-person drift, no hedging inflation.

What keeps this from a clean PASS is form, not substance: a layer of internal operations jargon survived in the Sources/Watch cells (~90 cells), the Review-flag column mixes sentence fragments with inconsistent capitalization, the MITRE version stamp Counsel-C asked for (fix #24) was never added, three Role mappings are poor fits (row 91 confirmed worst), and the Notes sheet has one stale decision record plus leftover internal build-process language in the v3 changelog. All fixable without touching evidence or judgments.

---

## What is already clean (no action)

1. **No hype.** The one loud phrase from v2 ("Biggest gap") was already replaced with the measured "Highest-value gap per the domain audit" (row 38 Seen). Nothing like "cutting-edge", "unprecedented", or "world-class" appears anywhere.
2. **Hedges are disciplined.** "consistent with", "unconfirmed", "no single-actor attribution established", "(causal link not established)" — these are the right hedges, used where the evidence actually ends.
3. **MITRE prefixes landed.** Every technique ID in Agent POIs col M now carries "ATT&CK"/"ATLAS" (Counsel-C #23 done). Spot-checked rows 4–104; no bare IDs remain.
4. **Voice and tense are consistent.** Observations are past tense, service descriptions present tense, third person throughout. No "our/we" in the data sheets.
5. **"Internal corpus hits"** (125 instances) is a deliberate, documented v3 wording choice (Notes row 126; build script line 58–70) — it replaced "Factum records" per the scrub. It is generic enough for a corporate reader ("our internal corpus" is ordinary industry language) and the counts are evidence the methodology needs. I recommend keeping it as-is.

---

## Fix list

### A. MITRE framework version stamp (outstanding Counsel-C #24 — new requirement from this review's brief)

**1. Notes, row 116, col A — append the version stamp to the MITRE legend.** Counsel-C asked for one line; it never landed. Technique IDs drift across releases, and ATT&CK v20.0 (released 2026-10-13) restructured tactics. Verified today: current releases are ATT&CK v20.0 and ATLAS v2026.09, and all cited IDs exist in them. Replace the full cell with:

> MITRE 'Conditional' legend (Counsel-C #25): 'Conditional <technique>' = the technique applies only if the condition stated in that row holds (for example only if observed relaying command/control data, or only if functioning as bidirectional communication). Rows 15 and 18 had 'Same conditional mappings as DSEWiki' spelled out in-cell 2026-10-23: 'ATT&CK T1102.002 if functioning as bidirectional communication; ATLAS AML.T0093 only if malicious prompts are planted for future AI ingestion'. All bare technique IDs now carry ATT&CK / ATLAS prefixes (Counsel-C #23). Framework versions: MITRE ATT&CK v20.0 (current 2026-10-13) and MITRE ATLAS v2026.09 (current 2026-09-15); all cited technique IDs verified against these releases 2026-10-23.

**2. Agent POIs, row 19, col M — spell out the shortened condition.** Every other wiki/board row uses the full form; row 19's "if prompts planted" is the only truncation and the Notes "Conditional" legend does not cover it (the legend is for cells that literally say "Conditional"). Replace:

> ATT&CK T1102.002 if functioning as bidirectional communication; ATLAS AML.T0093 only if malicious prompts are planted for future AI ingestion

### B. Role-set fits (the 12-term controlled set)

The set applies cleanly to ~97 of 101 rows. Three rows are poor fits:

**3. Row 91 (hermes-agent.nousresearch.com), col I — CONFIRM worst fit; recommend a 13th term.** AGENT_BOARD's controlled definition is "Agent-facing boards, forums, guestbooks, message directories, imageboards, bounty/offer boards, and reporting boards". A live Hermes Agent deployment's docs/messaging endpoints is none of those. No existing term fits (AGENT_COLONY = collectives, COORDINATION_LOG = archives/mirrors, UNCONFIRMED = "role not established", which misstates a role that IS established). Recommended fix (operator call): add a 13th controlled term HARNESS_ENDPOINT = "Live agent-harness deployments and their docs/messaging endpoints", and set row 91 col I to HARNESS_ENDPOINT. Fallback if the operator declines: leave AGENT_BOARD — the existing Review-flag disclosure is honest enough to carry the residual. The Notes row 218 already proposes this; it should be adopted, not just proposed.

**4. Row 39 (jotspot.io), col I — COORDINATION_LOG → AGENT_BOARD (judgment call).** The v2 value was "Public agent-conversation board, cross-board conversation guides" and the mapping matched on the trailing clause ("cross-board conversation guides" → COORDINATION_LOG). But the primary noun is "board", the Class is PUBLIC_AGENT_BOARD, and COORDINATION_LOG's definition ("Public agent log/message archives, conversation mirrors, and forum mirrors") describes archives and mirrors — Jotspot is neither. Options: (a) set col I to AGENT_BOARD [recommended]; (b) keep COORDINATION_LOG if the operator's evidence says Jotspot functions as a conversation mirror rather than a board.

**5. Row 94 (Public object storage), col I — TEMP_FILE_HOST → ARTIFACT_REGISTRY (judgment call).** The v2 value was "Possible persistent storage/transfer channel" (Class: OBJECT_STORAGE, ARTIFACT_STORAGE). TEMP_FILE_HOST's definition covers "Temporary file hosts, paste hosts, and dead-drop text venues" — none of which is object storage. ARTIFACT_REGISTRY's definition explicitly includes "artifact and object stores". Options: (a) set col I to ARTIFACT_REGISTRY [recommended]; (b) keep TEMP_FILE_HOST (the Notes row 218 already flags this as a judgment call).

**6. Row 92 (mdshare.org), col I — TEMP_FILE_HOST is borderline; keep with eyes open.** MDShare is a forensic dataset/evidence-inventory site (Class: FORENSIC_DATASET, EVIDENCE_INVENTORY), not a file host agents use; the mapping came from the v2 clause "Dead-drop venue paired with the cityb Ubuntu Paste carrier test". It is the least-wrong mechanical choice and the role detail survives in Seen. Options: (a) keep TEMP_FILE_HOST [recommended, no change]; (b) UNCONFIRMED, on the grounds that no agent-usable surface role is established for it.

### C. Global mechanical replacements (apply to every listed cell)

**7. "Watch:" → "Monitoring:"** — "Watch" is internal ops shorthand. Affected: Agent POIs col J rows 4, 5, 6, 18, 19–56, 59, 60, 63, 65–79, 84–90 (J only); Intelligence col F rows 11–19, 23–26. Example: row 38 col J "Watch: slot-0 baseline (wired 2026-10-22)" becomes "Monitoring: hourly baseline (configured 2026-10-22)" (see fixes 12–13 for the full forms).

**8. "wired" → "configured"** — "wired" is internal (a collector was wired up). Affected: Agent POIs col J rows 38–56, 65–71 (all "(wired 2026-10-22)" → "(configured 2026-10-22)"); row 6 col L "(not wired)" → "(not configured)"; row 45 col J "Watch: NOT wired (down)" → "Monitoring: not configured (service down)". Intelligence col F rows 16–19 ("Wired 2026-10-22" → "Configured 2026-10-22"; "not yet wired" → "not yet configured").

**9. Review-flag "auth-gated 2026-10-23 (ID verified in local cache)" → "Finding IDs verified 2026-10-23 (archived copies)"** — "local cache" points at our machine. Affected: Agent POIs col R rows 4, 5, 7, 9, 10, 11, 14, 15, 16, 18, 34, 39, 43, 47, 49, 57, 59, 60, 64, 65, 67, 70, 78, 81, 83, 92, 93, 95, 96, 99. Keep the trailing finding-number list unchanged (e.g. ": cloudfront findings #110, #152, #153, #157, #182").

**10. Review-flag "unattributed - flagged, not dropped" → "Unattributed — flagged, not dropped"** — sentence case. Affected: Agent POIs col R rows 13, 17, 41, 42, 44, 45, 46, 48, 50, 51, 52, 53, 54, 55, 56, 61, 63, 66, 68, 69, 71, 72, 73, 74, 75, 77, 79, 84, 85, 86, 87, 88, 94.

**11. Review-flag "uncheckable 2026-10-23 (egress/429; path confirmed on local disk)" → "Uncheckable 2026-10-23 (egress blocked / rate-limited; path confirmed in archived copies)"** — "local disk" is internal. Affected: Agent POIs col R rows 70, 71, 74, 75, 85; Intelligence col G rows 5, 8, 14, 17, 18, 19, 20.

**12. Review-flag "link dead 2026-10-23 (HTTP 000 — empty reply from server)" → "Link dead 2026-10-23 (HTTP 000 — no response from server)"** — "empty reply" is curl-speak. Affected: Agent POIs col R rows 23, 33, 45, 50, 75, 84.

**13. Review-flag fragments → sentence case.** "moved from Role cell 2026-10-23 (was: …)" → "Moved from Role cell 2026-10-23 (was: …)" (rows 6, 45, 57); row 62 "review-flag rule 2 (P0 with thin/no source links)" → "Review-flag rule 2 (P0 with thin or no source links)"; row 28 "enrichment restored from Oct-22 (regression in operator copy)" → "Enrichment restored from the 2026-10-22 version (regression in an intermediate copy)".

**14. "Hunt primary source" → "Primary evidence source"** — "Hunt" is our operation's name for itself. Affected: Agent POIs rows 4, 5 (cols J and L), 59, 60 (col J).

### D. Agent POIs — per-cell fixes

**15. Rows 19–26, col J: "Hourly slot-0, 2026-10-21 | Watch: slot-0 baseline" → "Hourly collection, 2026-10-21 (slot-0) | Monitoring: hourly baseline"** (adjust the date per row: rows 21–22, 25 use 2026-10-20). **Col L: "Operator's hourly hunt PRIMARY observation, 2026-10-21 (slot-0)." → "Primary hourly-collection observation, 2026-10-21 (slot-0)."** and **"Operator's hourly hunt observation, 2026-10-21 (slot-0)." → "Hourly-collection observation, 2026-10-21 (slot-0)."** — "Operator's" and "hunt" are self-referential; keep "slot-0" (it is glossary-defined in Notes row 117). Affected: col L rows 19–26.

**16. Rows 27–37, cols J and L: normalize "trajectory-domains Tier 1" and "surfacewatch".** "surfacewatch" is an undefined internal tool name; "trajectory-domains Tier 1" is a filename leaking into prose. Col J pattern: "trajectory-domains Tier 1; Internal corpus hits 25 | Watch: slot-0 baseline, surfacewatch" → "Tier-1 surface (trajectory-domains.md, 2026-10-19); 25 Internal corpus hits | Monitoring: hourly baseline, endpoint monitoring". Col L pattern: "trajectory-domains Tier 1; 25 Internal corpus hits; agent board (llms.txt), endpoint-baseline hash-tracked; slot-0 baseline + surfacewatch. No single-actor attribution established." → "Tier-1 surface (trajectory-domains.md, 2026-10-19); 25 Internal corpus hits; agent board (llms.txt), endpoint baseline hash-tracked; hourly baseline + endpoint monitoring. No single-actor attribution established." Affected: rows 27–37, both columns (rows 31, 32, 34, 35 already carry "(per trajectory-domains.md, 2026-10-19)" — normalize to the single form above). "endpoint monitoring" for "surfacewatch" is a judgment call — alternative: define "surfacewatch" in the Notes glossary instead.

**17. Row 4, col J: "Hunt primary source; crawler lane | Watch: urlquery scanner (12 query families incl. r.jina.ai/)" → "Primary evidence source; automated crawler collection | Monitoring: urlquery scanner (12 query families incl. r.jina.ai/)".** Row 5, col J: "Hunt primary source | Watch: urlscan scanner (14 queries incl. domain:r.jina.ai)" → "Primary evidence source | Monitoring: urlscan scanner (14 queries incl. domain:r.jina.ai)". Same "Hunt primary source" → "Primary evidence source" in rows 4–5 col L (keep the rest of the Seen text).

**18. Row 18, col J: "Wikipedia AI-edit hunt lane | Watch: revision-history grep method (on demand)" → "Wikipedia AI-edit investigation | Monitoring: revision-history grep method (on demand)".** Col L: "Lifeval (review lane):" → "Lifeval review:"; "tied to the WDQS outage" → "tied to the Wikidata Query Service (WDQS) outage"; "absent from WMF's evidence CSV/Diff article" → "absent from the Wikimedia Foundation (WMF) evidence CSV/Diff article". WMF/WDQS are unexplained acronyms anywhere else they appear (see Notes fix 33).

**19. Rows 12–13, col D: "Unknown" → "unknown".** The Capabilities column is otherwise lowercase snake_case ("fetcher", "analyzer"); "Unknown" is the only capitalized value.

**20. Row 11, col L: "Tencent Cloud HK Amap fleet context (fleet report): httpbin.org/base64 used as staging bootstrap. Transluce #136: NSO/Roi Et fetches (Mar 2026)…" → "Tencent Cloud HK Amap fleet context: httpbin.org/base64 used as staging bootstrap. Transluce #136: NSO (National Statistical Office of Thailand)/Roi Et fetches (Mar 2026)…".** "(fleet report)" is redundant, and "NSO" will be read as NSO Group by a corporate reader — judgment call: expand as shown, or drop "NSO/" if the reference cannot be confirmed.

**21. Row 33, col L: "agent board (dark since 2026-10-21)" → "agent board (unreachable since 2026-10-21)".** "dark" is slang.

**22. Row 41, col L: "(older records, nature to re-verify)" → "(older records; status to be re-verified)".** The current text is a fragment carried over from the v2 Role value.

**23. Rows 40, 48, 51, col J parentheticals: "(wired 2026-10-22; 502 at wiring)" → "(configured 2026-10-22; HTTP 502 during configuration)"; "(wired 2026-10-22; llms.txt 301s to absurdtools.com)" → "(configured 2026-10-22; llms.txt redirects (301) to absurdtools.com)"; "(wired 2026-10-22; 500 at wiring)" → "(configured 2026-10-22; HTTP 500 during configuration)".**

**24. Row 45, col R: "…; moved from Role cell 2026-10-23 (was: DOWN — connection failed 2026-09-28 and 2026-10-22); …" → "…; Moved from Role cell 2026-10-23 (was: service down — connection failed 2026-09-28 and 2026-10-22); …".**

**25. Row 57, col R: "(was: excluded from active surface polling per operator 2026-10-22)" → "(was: excluded from active surface polling — operator decision, 2026-10-22)".** Row 58, col L: "(excluded from active polling per operator 2026-10-22)" → "(excluded from active polling — operator decision, 2026-10-22)". "per operator" is internal shorthand.

**26. Rows 59–60: neutralize the remaining ops terms.** Row 59 col J → "Primary evidence source | Monitoring: repository watchlist (disabled); priority/confidence grade applies to the disclosed incident (moved from the Priority column 2026-10-23)". Row 59 col L: "PRIMARY corpus source, not actor attribution — trajectory corpora ingestion lanes;" → "Primary evidence source (not actor attribution); trajectory-corpus collection;". Row 60 col J → "Primary evidence source | Monitoring: harness-scoped monitoring, repository watchlist (disabled); priority/confidence grade applies to the disclosed cases (moved from the Priority column 2026-10-23)". Row 60 col L: "PRIMARY corpus source, not actor attribution;" → "Primary evidence source (not actor attribution);". "reposcout" is an undefined internal tool name; "trajectory fleets"/"narrow harness lane"/"ingestion lanes" are internal — judgment call on exact scope wording, but the tool name should go either way.

**27. Row 62, col J: "—; priority token applies to authorized internal telemetry (suffix moved from Priority column 2026-10-23)" → "—; priority token applies to authorized internal telemetry (moved from the Priority column 2026-10-23)".** "suffix moved" is build-process language.

**28. Row 63, col J: "Watchlist (no evidence either way) | Watch: watchlist (unproven)" → "Monitoring: watchlist (unproven — no evidence either way)".** Col L "(no Internal corpus hits — unproven)" is fine as-is.

**29. Rows 65, 71–74, col J: "paste lanes" → "paste collection".** E.g. row 65: "Internal corpus hits 4, paste lanes | Watch: Wayback CDX target (wired 2026-10-22)" → "Internal corpus hits 4, paste collection | Monitoring: Wayback CDX target (configured 2026-10-22)".

**30. Rows 77, 79, col J: "Hunt watchlist (standing)" → "Standing watchlist".** Row 77 → "Standing watchlist | Monitoring: Wayback scanner"; row 79 → "Standing watchlist | Monitoring: watchlist"; row 78 col J → "Transluce finding 195 | Monitoring: watchlist".

**31. Row 81, col L: "100+ beacons" → "100+ check-in signals (beacons)".** "beacons" alone is jargon-adjacent; the parenthetical keeps the precise term. (Optional; the rest of the cell is clean.)

**32. Rows 91–93, col R: "R/O/E unparseable in source: Unknown (parser note moved from MITRE cell 2026-10-23)" → "R/O/E token unparseable in source ('Unknown'); note moved from the MITRE cell 2026-10-23".** "parser note" is build-process language.

**33. Row 100, col J: "slot-0 new-board discovery 2026-10-23; live public board, 9 distinct speakers rendered in captured bytes (claim of 23 unverified), boards: stuck/play/skills/hate (+ephemeral commons)" → "New-board discovery 2026-10-23 (hourly baseline slot); live public board, 9 distinct speakers rendered in captured bytes (claim of 23 unverified); boards: stuck, play, skills, hate (plus an ephemeral 'commons' board)".**

**34. Rows 101–104, col J: "Tier-1 discovery-endpoint baseline 2026-10-23 (LEAD-3 TIER-B proposal 3); Tier-1 baseline captured; monitor proposal queued for operator word (counsel did not endorse)" → "Tier-1 discovery-endpoint baseline captured 2026-10-23; monitoring proposal pending operator approval (not endorsed by review)".** Judgment call: drops the internal "LEAD-3 TIER-B" lane reference and the informal "operator word". The "(not endorsed by review)" disclosure must stay — Counsel-B required it to avoid implying counsel endorsed Tier-1 status.

**35. Row 101, col L: "(council-governed knowledge base on Solana mainnet, real-SOL donations, hosted or own-key agents)" → "(council-governed knowledge base on Solana mainnet; SOL donations; agents hosted or self-keyed)".** "real-SOL" is slang; "own-key" is unclear. Judgment call.

### E. Intelligence and reporting URLs sheet

**36. Header row 3, col C: "Calssification" → "Classification".** Judgment call: the Notes (row 113) say the sheet's own header spelling was kept deliberately, but a typo in a header is a typo — nothing downstream depends on the header string.

**37. Row 7, col E: "unattributed — internal wiki-investigation dataset, no public home" → "unattributed — independent wiki-investigation dataset, no public home".** Col F: "In-repo forensic investigation (Lifeval): 8 temp accounts (consecutive UIDs 2690515-2690523), sandbox-to-live chain across 9 wikis, 1,087 revisions reviewed — marker vocabulary fully incident-contained; contradicts WMF's no-coordination claim. No public writeup URL established; repo findings doc is the verified reference" → "Independent forensic investigation (Lifeval): 8 temp accounts (consecutive UIDs 2690515–2690523), sandbox-to-live chain across 9 wikis, 1,087 revisions reviewed — marker vocabulary fully incident-contained; contradicts the Wikimedia Foundation's no-coordination claim. No public writeup URL established; evidence review on file." "In-repo"/"repo findings doc" are self-referential (the repo link was scrubbed everywhere else); a corporate reader has no repo.

**38. Rows 11–15, col F: "Hunt intel source" → "Intel source"; "Watch: jina scanner watchlist" → "Monitoring: Jina scanner watchlist"** (rows 11, 12). Row 13: "Watch: crtsh scanner (Tier-1/5 domains)" → "Monitoring: crt.sh scanner (tiers 1–5)" — judgment call: "Tier-1/5" reads as tiers 1 through 5; confirm against the scanner config. Row 14: "Cairn hunt phase 1+2 (3,354 hosts, 247 open dashboards) | Watch: shodan scanner (5 count queries + facets)" → "Cairn investigation, phases 1–2 (3,354 hosts, 247 open dashboards) | Monitoring: Shodan scanner (5 count queries + facets)". Row 15: "Hunt intel source (237 Internal corpus hits) | Watch: wayback scanner (12 targets)" → "Intel source (237 Internal corpus hits) | Monitoring: Wayback scanner (12 targets)".

**39. Rows 16–19, col F: "Proposed 2026-10-22 | Watch: not yet wired" → "Proposed 2026-10-22 | Monitoring: not yet configured".** Rows 17–19: "Wired 2026-10-22" → "Configured 2026-10-22"; "Watch: iocfeeds scanner (21 indicators)" → "Monitoring: IOC-feeds scanner (21 indicators)".

**40. Row 21, col F: "Internal corpus lanes (own sweep hit /gems pages) | Borderline — left out for operator call" → "Internal corpus (own sweep of /gems pages) | Borderline — excluded pending operator decision".** "left out for operator call" is internal workflow language.

**41. Rows 23–26, col F: "Cairn phase-2, Counsel MALICIOUS | Watch: cairnwatch (disabled, needs his word)" → "Cairn phase 2, counsel verdict MALICIOUS | Monitoring: Cairn watch (disabled, pending operator approval)".** Rows 24–26: "Watch: cairnwatch (disabled)" → "Monitoring: Cairn watch (disabled)". "needs his word" is the single most informal phrase in the workbook — it has to go.

### F. Notes sheet

The role-mapping block (rows 128–218) reads corporate-clean as a controlled-vocabulary record. Fixes are limited to framing lines:

**42. Row 128, col A: "Role controlled set, v3 (Counsel-C proposal, applied 2026-10-23)" → "Role controlled vocabulary (applied 2026-10-23)".** Row 141, col A: "Role value → controlled term (all 76 v2 values; parenthetical detail moved to Seen where not already present)" → "Original value → controlled term (76 distinct original values; parenthetical detail moved to Seen where not already present)". Row 218, col A: "Judgment calls in the Role mapping (flagged for the operator)" → "Judgment calls in the Role mapping". "Counsel-C"/"v2 values"/"flagged for the operator" are internal review-process references; the mapping table itself is fine.

**43. Row 121, col A — mark superseded.** It currently says the Role column stays per-row free text per operator directive and the 12-term set is "recorded here as a recommendation" — but v3 applied the set (rows 128–218). A corporate reader meets a direct contradiction. Replace with: "Role column decision (superseded 2026-10-23): the 12-term controlled vocabulary below was applied in v3; the earlier recommendation to keep per-row free text is retained here as a record."

**44. Row 126, col A: "v3 changelog (2026-10-23) — BUILD lane: self-referential source scrub" → "v3 changelog (2026-10-23): self-referential source scrub".** Col B: "Internal data/lanes/... paths stripped from Direct Links cells (POI K19–K26, Intel E9/E27/E28)" → "Internal data-path references stripped from Direct Links cells (Agent POIs rows 19–26, Intel rows 9, 27, 28)"; "internal batch ID d6982046 stripped from 14 visible cells (POI J/L 19, 21–26) with no replacement" → "an internal batch ID was stripped from 14 visible cells (Agent POIs Sources/Seen, rows 19, 21–26) with no replacement" (the ID itself is preserved in the INTERNAL sheet's lineage record, so nothing is lost); "the internal evidence-system name is gone from visible cells" → "the internal evidence-system name was removed from visible cells". "BUILD lane", "data/lanes/...", "POI K19–K26" are internal build-process shorthand in a corporate-facing changelog.

**45. Row 127, col B: "LEAD-3 live capture of the same DSE wiki ForumSeite at wikiservice.at/dse (2026-10-23)" → "a live capture of the same DSE wiki forum page at wikiservice.at/dse (2026-10-23)".** "LEAD-3" is an internal lane name; "ForumSeite" is untranslated German from the source page.

**46. Row 117 glossary — expand and de-self-reference.** Replace the full cell with: "Glossary (Counsel-C #18): slot-0 = the hourly baseline collection slot. COMBO-INIT = the state machine named in the Tencent Cloud HK Amap fleet investigation driving the webhook.site dead-drop / exfiltration sequence (defined only in fleet-investigation prose; no independent definition established). 'exfil' updated to 'exfiltration' in row 81 Seen. Acronyms: WMF = Wikimedia Foundation; WDQS = Wikidata Query Service; NSO = National Statistical Office of Thailand (Transluce #136 context); CDX = Wayback Machine capture-index API; POI = point of interest (map points of interest in Amap-fleet context; monitorable surfaces elsewhere in this workbook); SSRF = server-side request forgery (standard industry term, row 96). Proper-name labels retained as-is: AIHW (case label in Transluce findings), 1F916 (service name)."

**47. Row 3, col B: "Your service taxonomy: create a local machine-tag namespace such as agent-service. Example tags:" → "Service taxonomy: a local machine-tag namespace such as agent-service. Example tags:".** Row 40, col C: "Your own artifact repositories, e.g. JFrog Artifactory" → "Internal artifact repositories, e.g. JFrog Artifactory". Row 46, col D: "Publicly documented artifacts or logs you are authorized to access" → "Publicly documented artifacts or logs, where access is authorized". Second-person imperative is fine in a how-to guide, but "Your" reads as the author talking to one specific operator.

**48. Row 16, col B: "Recommended Monitoring Priority" → "Recommended monitoring priority"** (matches row 15's "Recommended monitoring priorities" casing).

**49. Row 101, col A: append a Template-sheet disposition.** "…Template sheet: untouched (travel template, unrelated)." → "…Template sheet: leftover travel template — delete or hide before distribution (see fix 51)."

### G. Appendix sheet

**50. Row 35, col B: "Explaination" → "Explanation".** Typo in a header row. Col I: "How soon we should build a collector." → "How soon collection should be established." ("we" = our team; internal.)

### H. Template sheet and INTERNAL sheet

**51. Template sheet — delete or hide before distribution.** It still contains a travel template ("Trip Title", "Travelers", "Person 1", "9/5 - 9/8", "New York, NY"). It is sloppy in a corporate-facing product, and its presence invites the question of what else was left in by accident. Judgment call: hiding preserves the sheet if the operator wants it; deleting is cleaner.

**52. INTERNAL sheet — marking confirmed unmissable.** The tab itself is named "INTERNAL — do not distribute", which is the strongest possible marking short of a cover sheet. It is correctly exempt from corporate-clean rules (its "Original v2 value" column intentionally preserves the scrubbed self-referential values as a lineage record, per the build's provenance requirement). No language changes needed. One caution for the operator: this sheet names the internal repo and evidence-system paths verbatim — it must never ship with a distributed copy, and any "save a clean copy" workflow needs to drop this sheet explicitly.

---

## Notes for the builder

- Fixes 7–14 are global string replacements; apply them first, then the per-cell fixes (several per-cell replacements assume the global ones, e.g. fix 15's "Monitoring:" and "configured").
- Fix 16 ("surfacewatch" → "endpoint monitoring") and fix 26 ("reposcout"/"trajectory fleets"/"harness lane" wording) are the two replacements where I am least sure of the underlying tool's function — if either term names something the reader needs to operate, define it in the Notes glossary instead of renaming it.
- Nothing in this review questions the evidence, the priority grades, the attribution calls, or the monitoring judgments. Every fix is wording or labeling.
- Count of distinct changes: 52 numbered items, of which 8 are global replacements covering ~150 cells, and 9 are flagged judgment calls with both options given.
