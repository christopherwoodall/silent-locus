# COUNSEL (b) — ATTRIBUTION verdict — monitorable-surfaces v2
Fleet: monitorable-surfaces v2 build | Workbook: `lists/urls/monitorable-surfaces-ENRICHED-v2.xlsx`
Reviewed 2026-10-23 by attribution counsel. Verdict-first, plain language.

## Q1 — The 4 counsel-cleared MALICIOUS Cairn panels — SUPPORTED

Checked rows (Intelligence and reporting URLs sheet):
- Row 23 — `http://185.242.245.159:8000` — "Malicious Cairn panel (4 projects, 2 active)" / Attrib: "Cairn phase-2, Counsel MALICIOUS"
- Row 24 — `http://31.56.206.187:8000` — "Malicious Cairn panel (24 projects, 5 active)" / same attrib
- Row 25 — `http://31.57.47.29:8000` — "Malicious Cairn panel (19 projects, 6 active)" / same attrib
- Row 26 — `http://31.59.92.155:8000` — "Malicious Cairn panel (23 projects, 5 active)" / same attrib

Verification: counsel reversed its 'all UNDETERMINED' verdict on 2026-10-19 and cleared exactly these 4
hosts MALICIOUS (memory/2026-10-19.md#L584; reports/india-cert-in-lead/REPORT.md "Previously cleared
malicious panels"; data/lanes/cairn-panels/working/api-counsel-verdicts.jsonl). The project/active
counts in the rows (4/2, 24/5, 19/6, 23/5) match the counsel evidence exactly. The "cairnwatch
(disabled, needs his word)" note matches standing: watcher disabled by default, enabling needs his word.
Full-workbook grep for "malicious": the label is applied ONLY to these 4 cleared hosts (plus the
urlhaus IOC-feed class label and conditional prose like "only if malicious prompts are planted").
The non-cleared dual-use workbench 161.248.63.110 does not appear in the workbook at all — no risk
of mislabeling there. Nothing overstated.

## Q2 — Tier-1 claims — SUPPORTED-WITH-CHANGES

- Agent POIs rows 27–37 (agentsboard.org, agents-agents-agents.com, bboard.ai,
  agentgateway.pythonanywhere.com, tantive.space, swarmmemo.com, messageboardforaiagents.com,
  swarm.termina.digital, thecolony.ai, aiforum.grok.me, moltbook.com): every domain appears in the
  TIER 1 table of lists/urls/trajectory-domains.md. Liveness notes also line up (row 30's dead
  mcp.json "Coming Soon"; row 33's dark-since-2026-10-21 vs the table's TLS-timeout note).
  SUPPORTED (see fix 4, 6 for nits).
- Agent POIs rows 101–104 (artifactcounsel.com, joinsnail.com, agentsspeakup.com, agenttavern.dev):
  all four ARE in the trajectory-domains.md Tier-1 table (lane-6 2026-10-23 rows). BUT their Sources
  cell says "counsel-review Tier-1 board", which reads as counsel endorsing the Tier-1 status.
  Counsel's actual review (reports/counsel/lead3-counsel-review.md, Verdicts + Open questions §3)
  left the Tier-B monitor proposals QUEUED for his word — unendorsed. The phrase overstates.
  See fix 1.

## Q3 — The 33 "unattributed" rows — SUPPORTED (leave them flagged as-is)

All 33 enumerated (Agent POIs rows 13, 17, 41, 42, 44, 45, 46, 48, 50, 51, 52, 53, 54, 55, 56, 61,
63, 66, 68, 69, 71, 72, 73, 74, 75, 77, 79, 84, 85, 86, 87, 88, 94). Spot-checked the strongest
(rows 42 openagentforum.com — Factum 10 records, slot-0 baseline wired; row 48 bookofbots.com —
Factum 5 records, llms.txt observed; rows 50, 53, 54 — Factum records + baselines wired;
row 61 gist.github.com; row 71 nicepaste.com): each has observed surfaces or Factum sightings but
no single-actor attribution. "Unattributed" is the honest, conservative flag. No quiet downgrade
detected — no row that earned a stronger actor-grade was demoted. Do not touch the flags.
(Informational vocab note — see fix 5.)

## Q4 — Gap-fill rows (100–104) and 2 intel gap rows — SUPPORTED-WITH-CHANGES

- Row 100 fallback.chat (PRIMARY observed bytes): evidence path
  data/lanes/general-hunt/raw/0/20261023T144326Z/ exists — home.html + llms.txt bodies,
  provenance (curl GET, HTTP 200, passive, 2026-10-23T14:46Z), sha256. llms.txt confirms
  "Protocol: sanctum/0.1". <head> alternates in home.html confirm the /api/digest and /feed.xml
  Direct Links. BUT the Role cell claims "23 registered speakers observed" — the retained bodies
  contain only 9 unique speaker names/ids; the number 23 is not derivable from the cited bytes.
  See fix 2.
- Rows 101–104 (PRIMARY observed bytes): all 48 capture files exist at
  data/lanes/general-hunt/raw/6/20261023T141200Z/ (llms.txt + skill.md bodies per host, with
  .PROVENANCE.txt + .sha256). THIN-LINK notes verified byte-by-byte against the bodies: joinsnail
  mcp.json = Next.js SPA shell; agentsspeakup mcp.json = HTML shell; agenttavern mcp.json = "Not
  Found"; agentsspeakup skill.md = Next.js 404 shell (working skill path correctly listed). Honest.
  BUT rows 102–104 carry "MCP" in Class while no machine-readable MCP manifest was observed —
  only llms.txt prose mentions. See fix 3.
- Intel row 27 (Anthropic UK AISI): path
  data/lanes/anthropic-intel/raw/alignment-assessment-ukaisi_2026-10-23.EXTRACTION.md exists
  (29 KB; content spot-check confirms the Mythos 5 / 9-of-43 material). Class
  PRIMARY_RESEARCH_SOURCE is correct — it is Anthropic's first-party report. SUPPORTED.
- Intel row 28 (METR red-team pilot): path data/lanes/metre-thread/mined-items.md exists
  (15 KB; spot-check confirms the cited tweet id 2113290966933389390). Class
  INTEL_BLOG, INCIDENT_RESEARCH is honest — no primary-source over-claim. SUPPORTED.

## Numbered fix list (for FINALIZE)

1. Rows 101–104, Sources: replace "counsel-review Tier-1 board" with wording that reflects reality —
   e.g. "LEAD-3 TIER-B proposal 3; Tier-1 promotion queued for operator word (counsel left the
   Tier-B proposals unendorsed)". Same overstatement lives in work-v2/GAPFILL.md §4 header
   ("Four counsel-review Tier-1 boards") — fix the header too.
2. Row 100, Role: "23 registered speakers observed" is not derivable from the cited captures
   (9 unique speaker names/ids in home.html + llms.txt). Either capture the speaker-count body or
   soften to "speaker roster observed; exact registered count unconfirmed from retained bytes".
3. Rows 102–104, Class: drop "MCP" or qualify it — e.g. "MCP (llms.txt-claimed only, no manifest
   captured)" — since mcp.json/.well-known/mcp.json returned SPA shells / not-found.
4. Rows 27–37, Sources/Seen: Factum counts disagree with trajectory-domains.md (e.g. row 34 claims
   248 vs table 114; row 31 claims 105 vs 103). Reconcile or add a count basis/date.
5. Attribution column vocab: normalize to the controlled 5 grades — "PRIMARY" vs "PRIMARY observed
   bytes" (rows 100–104) and "observed - trajectory-domains, no single-actor attribution" (row 28)
   are distinct strings for the same grade; "observed" for rows 27–37 means surface-liveness while
   elsewhere Attribution is about actor/claim basis. Keep Attribution strictly about
   actor/claim basis.
6. (Trivial) Row 37 "moltbook.com" vs table "www.moltbook.com" — same domain, no action needed.

Overall: attribution grades are sound. Nothing claims malice or Tier-1 status without backing,
except the "counsel-review" phrasing in fix 1. The 33 unattributed flags are the right call.
