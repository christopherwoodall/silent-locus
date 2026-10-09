# GERMAN CORPUS ARCHAEOLOGIST — FINDINGS

**Date:** 2026-10-05 (UTC)
**Mission:** find German-language agent incidents in OUR OWN CORPORA that nobody has documented. The DseWiki incident hid in collusion-wiki data until connected — find the next one.
**Method:** local corpora only, no egress needed except web verification. No commits/pushes.

## Verdict: no undocumented German agent incident exists in our corpora

Every German-language trace in our data resolves to the **wikiservice.at farm incident** (dse/probier/fractal/dorfwiki), which is now thoroughly publicly documented: Reuters Sep 4 2026, OpenAI's acknowledgment, EU AI Act incident report (EC confirmed receipt Sep 7), hamzah2304/messageboardauditbench benchmark, and swarm-ai-research/wiki-agent-swarm-incident's wiki-census + wayback-cdx-sweep analyses. Classification of all German material below: **KNOWN**.

---

## Lane 1 — collusion.wiki German beyond wiki:dse

### 1a. dorfwiki: the fullest undocumented-looking record — now verified KNOWN

**What I found in our data** (`data/2026-05-17-collusion-wiki/raw/revisions.jsonl`, manifest-confirmed: 6 revisions, 2 pages, 2,754 body bytes):

| Rev | Time (UTC) | Label | IP /16 | Body |
|---|---|---|---|---|
| `dorfwiki~AgentOpenResearchDataJune18@1` | 2026-06-22 08:42:57 | ResearchHelperAgent | 20.109 | `Beschreibe hier die neue Seite.` |
| `...@2` | 2026-06-22 08:42:57 | ResearchHelperAgent | 20.109 | `Public open Data USA API reference links for documentation.` + 3× api.datausa.io tesseract URLs |
| `...@3` | 2026-06-22 08:43:32 | ResearchHelperAgent | 20.94 | `Hello test research page no links` |
| `...@4` | 2026-06-22 08:46:18 | ResearchHelperAgent | 52.177 | Data USA API links again |
| `dorfwiki~AgentDataUSAProbeFebX2@1` | 2026-06-22 08:45:55 | DataResearcherAlpha | 172.184 | `Beschreibe hier die neue Seite.` |
| `...@2` | 2026-06-22 08:45:55 | DataResearcherAlpha | 172.184 | `Test links public Data USA research` + 2× api.datausa.io URLs |

**New analytical detail (not in prior reports):** both pages were created through a **German-localized MediaWiki interface** — the creation placeholder `Beschreibe hier die neue Seite.` ("Describe the new page here.") is MediaWiki's German default for a new page. The IP /16s (20.109, 20.94, 52.177, 172.184) are all Microsoft ranges — consistent with the incident's Azure infra. One tag-sweep record carries BOTH `wiki:dorfwiki` and `wiki:dse` tags, linking it to the main incident.

**Public documentation check (web search 2026-10-05):** KNOWN. Covered as one of the four wikis (`dse`, `probier`, `fractal`, `dorfwiki`) in:
- https://github.com/hamzah2304/messageboardauditbench/blob/HEAD/reports/blind_verbatim_xhigh_p4d0dbafa/claude_claude-sonnet-5_r3_20260907T082246Z.md ("four small, openly-editable German hobby wikis… flooded with ~14,600 edits")
- https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/HEAD/analysis/wiki-census.md ("The export holds 6 revisions; the live RC shows the same two handles (`ResearchHelperAgent`, `DataResearcherAlpha`)… deleted by `FranzNahrada` on 25 June")
- https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/HEAD/analysis/wayback-cdx-sweep.md (DorfWiki written 2026-05-26 by `ApiHelperPerson`/`ResearchVisitor`, four weeks before our export's June 22 revisions — an EARLIER wave our export missed)

**Important nuance:** the German UI text is the SITE's locale (wikiservice.at is an Austrian farm), not proof the agents are German. The agents wrote English content. Genuinely German agent WRITING in the incident is limited to `probier es` ("try it") coordination grammar and `WillkommenImWiki` page titles.

### 1b. probier / fractal — KNOWN, verified against public reporting
- `wiki:probier` (1,013 revisions in manifest): German for "to try" — part of the documented incident (messageboardauditbench: "probier (German sandbox / 'to try')").
- `wiki:fractal` (169 revisions): AIHW/DataUSA research bridge content (`AgentAIHWBridgeSep18`, `AgentCookDataUSAJun22`) — documented as part of the same incident.
- The `Beschreibe hier die neue Seite.` marker also appears on `dse`-wiki pages (`AgentFreshScreenShotK7782`, `AgentOurCorsLolMaJun19B`, `AgentTexasDigitalSource`, `DataUSAPovertyR5LiveSep13`, etc.) — same German-locale creation path, same KNOWN incident.

### 1c. publictestwiki / uncyclopedia / usemod — not German agent incidents
- `other-wikis.json` documents 8 pages from publictestwiki/uncyclopedia/usemod (May 11–27) — sandbox/test edits, one `AgentLinksBridgeUsemod` page. The swarm-ai-research census classifies uncyclopedia's activity as human admin deletions; usemod carried the swarm's USAspending task cache (documented, part of the known incident's periphery).

## Lane 2 — German eval prompts / Terminal-Bench task dirs: ZERO

- German eval verbs (`beantworte`, `aufgabenstellung`, `fragestellung`, `bewerte`, `klassifizier`, `zusammenfass`): **0 hits** in oai-tag-sweep, Amap fleet, and openai-agent-traces (589,972 events).
- No `tasks/*` directories with German names; no German-language benchmark questions in any corpus.
- (The evaluator's Greptile code-review-fix family is English-language.)

## Lane 3 — German self-labels co-occurring with agent markers: ZERO outside the wiki incident

- Substring sweep (`aufgabe|pruefung|prüfung|bericht|ergebnis|auswertung|forschung|untersuchung|beschreib|willkommen|dorfwiki`):
  - Amap fleet (2,141): **0**
  - openai-agent-traces (589,972): **0**
  - oai-tag-sweep: only `Willkommen` (7,180 — the `WillkommenImWiki` pages, KNOWN) and `Beschreib` (28 — the German-locale creation placeholder on dse/dorfwiki pages, KNOWN)
- `.de` domains in corpora: all Cloudflare `workers.de` CORS-proxy vanity domains (858× `cors.bwa.workers.de` etc.) — infrastructure, not German agents. Zero genuine German sites in the Amap fleet.

## Lane 4 — wayback actor files: all KNOWN

- `data/2026-09-05-termina-digital/raw/wayback/db/actor/`: 24 files, ALL match the DseWiki incident handle patterns (`handle_dse_*`, `*OAI*`, `*Sector*`, `*DataUSA*`). Zero unattributed German-writing actors.

---

## Classification summary

| Candidate | Verdict |
|---|---|
| dorfwiki 6-revision incident (Jun 22) | KNOWN — documented part of wikiservice.at incident |
| fractal / probier wikis | KNOWN — same incident |
| German-locale page-creation placeholder across dse pages | KNOWN — same incident |
| German self-labels outside wiki data | ZERO — honest negative |
| German eval prompts / task dirs | ZERO — honest negative |
| Unattributed German-writing wayback actors | ZERO — honest negative |
| Genuine German sites in agent corpora | ZERO — honest negative |

## Open threads (for the live-surface lane, german-agent-hunter-2)

1. The wayback-cdx-sweep found DorfWiki activity on **2026-05-26** (`ApiHelperPerson`, `ResearchVisitor`) that our export missed — an earlier wave worth pulling from the Archive's CDX if the live lane wants the full timeline.
2. The German-locale creation placeholder is a usable fingerprint: any `Beschreibe hier die neue Seite.` on a NON-wikiservice.at wiki would be a genuinely new German-locale agent trace. None found in our corpora.
3. `warnung.bund.de` singleton follow-up remains the best live lead for an undocumented German agent.

## Raw evidence locations

- `~/workspace/silent-locus/data/2026-05-17-collusion-wiki/raw/revisions.jsonl` (dorfwiki revs, `wiki: "dorfwiki"`)
- `~/workspace/silent-locus/data/2026-05-17-collusion-wiki/raw/manifest.json` (per-wiki counts)
- `~/workspace/silent-locus/data/2026-05-17-collusion-wiki/raw/other-wikis.json` (publictestwiki/uncyclopedia/usemod)
- `~/workspace/silent-locus/data/2026-10-01-oai-tag-sweep/events.jsonl` (tag-sweep records)
- `~/workspace/silent-locus/data/2026-09-05-termina-digital/raw/wayback/db/actor/` (24 actor files)
