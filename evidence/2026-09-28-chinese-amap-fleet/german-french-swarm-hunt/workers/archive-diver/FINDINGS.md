# ARCHIVE-DIVER — Findings

**Worker:** archive-diver (EUROSWARM wave 1)
**Date:** 2026-10-05
**Mission:** Wayback CDX for .de/.fr agent boards, wikis, harness pages (Apr–Sep 2026 incident windows); BnF + DNB national web-archive public interfaces. Archive indexes only — passive throughout. No candidate infrastructure was fetched or probed.
**Status:** COMPLETE — all queries returned. No leads; eight graded findings (1 CONFIRMED control, 7 HONEST NEGATIVES), two new reusable endpoints documented.

## Method notes (for reuse)

- Wayback CDX: `http://web.archive.org/cdx/search/cdx?url=<host>&matchType=domain&from=20260401&to=20260930&filter=statuscode:200&collapse=urlkey&fl=timestamp,original,digest&limit=20000`. Default output is **space-separated text** (`timestamp original digest`), not JSON; pass `output=json` for a wrapped array. Polite pacing (3s+ between queries).
- Arquivo.pt full-text API: `GET https://arquivo.pt/textsearch?q=<query>&maxItems=50` → JSON with `estimated_nr_results` and `response_items`. Works without a key; slow (~20–60s per query).
- Austrian National Library (ONB) public CDXJ: `GET https://webarchiv.onb.ac.at/web/cdx?url=<url-encoded full URL>` → `Content-Type: text/x-cdxj`, CDXJ rows with `mime`, `digest`, `length`, `offset`, `filename`. **Exact URL only** — bare domains normalize to root; wildcards/prefixes are not expanded (per agntn/archives provider doc, verified live). Coverage is Austrian (.at + Austrian-relevance).
- DNB public catalogue SRU: `GET https://services.dnb.de/sru/dnb?version=1.1&operation=searchRetrieve&query=<CQL>&maximumRecords=N&recordSchema=MARC21-xml`. 92 indexes incl. `tit` (title), `woe` (keyword), `url`, `mat` (material type), `jhr` (year). `scan` operation is **not supported** (diagnostic `info:srw/diagnostic/1/4`). Full index list saved from the explain response during this run.
- IA CDX **TLD-wide domain queries are refused**: `url=de&matchType=domain` → `403 Forbidden` / *"This type of CDX query requires authorization."* The coordinator's `*.de/*agent*`-style sweep is therefore **not possible** on the public CDX API. Host-level sweeps are the viable unit.

## 1. Wayback CDX — TLD-wide marker sweep (.de / .fr)

**HONEST NEGATIVE (method-level).** Pilot queries `url=de&matchType=domain` with `filter=urlkey:.*<marker>.*` for markers `httpbun`, `zz=`, `willkommenimwiki` (window 20260401–20260930) all returned **HTTP 403, body "This type of CDX query requires authorization."** A TLD-scoped CDX sweep cannot be run from the public API. (Common Crawl already ruled out per prior truth; Arquivo.pt full-text used instead — §3.)

## 2. Wayback CDX — myxwiki.org (French XWiki farm, NEW host)

**HONEST NEGATIVE for agent-swarm activity.** Rationale: XWiki SAS is French; myxwiki.org is its public wiki farm — a plausible FR agent-board surface never previously swept.

- Query: `url=myxwiki.org&matchType=domain`, 20260401–20260930, status 200, collapse=urlkey → **511 captures, 48 capture-days, span 20260402–20260925**, across hosts `www.myxwiki.org` (284), `webid.myxwiki.org` (142), `gdrgpl.myxwiki.org` (59), `myxwiki.org` (9), `fakturama.myxwiki.org` (6), `selfbus.myxwiki.org` (6), `massol.myxwiki.org` (5).
- Signature regexes over captured URLs (`agent|bridge|zz=|oai|ki[-_]|harness|eval|swarm|beschreib|willkommen|researchhelper|dataresearcher|apihelper`): 45 hits, **all XWiki platform webjar false positives** (`searchSuggest`, `tree`, `?evaluate=true`, `lightbox`, `Validation`), zero agent-handle or Bridge-grammar URLs.
- 80 distinct content pages (`/bin/view/…`); sub-wikis are benign: `gdrgpl` (French research group "Jumeaux Numériques"), `massol` (Maven blog), `selfbus` (German home-automation project — German content `Geräte/Taster/TasterBJ`, no agent markers), `webid`, `fakturama`.
- **Observed, out of scope:** ~60 spam user-profile pages on `www.myxwiki.org/xwiki/bin/view/XWiki/<name>` (`?category=profile`) with Vietnamese online-casino SEO names (`kubetcoim`, `88club`, `shbet88loan`, `i9betcomwiki`, …). This is bot SEO spam, not agent-swarm activity: no Agent handles, no Bridge grammar, no research-task content. Logged here per keep-all; not a swarm lead.

## 3. Arquivo.pt full-text — German incident markers

**HONEST NEGATIVE (all seven).** Each query returned a valid empty result (`estimated_nr_results: 0`, `response_items: []`):

| Query | estimated_nr_results |
|---|---|
| `"Beschreibe hier die neue Seite"` | 0 |
| `ResearchHelperAgent` | 0 |
| `DataResearcherAlpha` | 0 |
| `ApiHelperPerson` | 0 |
| `ResearchVisitor` | 0 |
| `WillkommenImWiki` | 0 |
| `AgentOpenResearchData` | 0 |

OBSERVED: the German-locale creation fingerprint and all four known agent handles appear in **zero** Arquivo.pt-indexed pages. INFERENCE: within Arquivo.pt's crawl corpus, there is no German-locale agent-wiki trace beyond what the corpus already holds; a zero here is absence in Arquivo.pt's index, not proof of nonexistence on the live web.

## 4. BnF (Bibliothèque nationale de France) web archives

**HONEST NEGATIVE — no public remote search interface exists.**

- Wikipedia "List of web archiving initiatives" (accessed 2026-10-05): BnF Web Legal Deposit — *"Accessible to authorized users through the reading rooms of the BnF Research Library located in Paris and Avignon and in partner libraries in regions and overseas territories… Full Text search only available on specific collections (i.e. news, COVID-19, the early French web)."*
- HAL 2025 paper "Closed data, open software: building new ways into the French web archives": the French web archives are a *"captive data source whose access is restricted"*; researchers need formal/informal project agreements.
- Consequence: the BnF archive **cannot be mined remotely** for .fr agent traces. The older segment is reachable by URL through the Wayback Machine (per WIPO doc), which collapses back to the CDX lane. No undocumented public endpoint found.

## 5. DNB (Deutsche Nationalbibliothek) web archive

**HONEST NEGATIVE — metadata is public, but the surface is structurally wrong for this hunt.**

- The web archive itself is reading-room-only (Frankfurt/Leipzig); its **metadata is in the publicly accessible catalogue**, queryable via the SRU endpoint documented above (verified live: `title=agent*` → 49,204 records).
- Control queries against the known incident: `url=wikiservice.at*` → 0; `tit=dorfwiki*` → 0; `woe=dorfwiki` → 0. DNB holds no catalogue record for the known Austrian/German wiki-farm incident.
- Structural reason: DNB web archiving is **librarian-selected** (selective crawls by topic/event, e.g. "federal authority", "Bundestag elections"), not a domain crawl — an agent board would only appear if a librarian chose it. Poor hunt surface; endpoint documented for reuse.

## 6. Austrian National Library web archive (adjacent surface, documented)

- Public CDXJ endpoint verified working: `https://webarchiv.onb.ac.at/web/cdx?url=<full URL>` (positive control `https://www.onb.ac.at/` returned captures from 2009; `Content-Type: text/x-cdxj`).
- Incident-host probes: `https://wikiservice.at/` → **0 rows**; `http://dorfwiki.org/` → **0 rows** (both 200, empty CDXJ). ONB holds no captures of the known incident hosts at root — HONEST NEGATIVE on those probes.
- Limitation: exact-URL only, Austrian coverage (.at + Austrian-relevance). **New reusable surface** for any future .at agent-board candidates (e.g. from tld-sweeper's .at lane). Not a .de/.fr surface per se.

## 7. Control: dorfwiki.org (known incident host) — pipeline validation + no new pages

**CONFIRMED (control).** The original control hostname `dorfwiki.wikiservice.at` was wrong (empty CDX result — that host does not exist in the index); corrected to `dorfwiki.org`, the actual incident host per the wayback-cdx-sweep.

- Query: `url=dorfwiki.org&matchType=domain`, 20260401–20260930, status 200, collapse=urlkey → **17,154 captures, 47 capture-days, span 20260404–20260911**.
- The known incident pages are recovered from the index: `AgentDataUSAProbeFebX2` (20260710), `AgentOpenResearchDataJune18` (20260710), `ApiHelperPerson` (20260606), `ERDE/ApiDataHelperBridge`, `ERDE/DataPdfBridgeThree`, `ERDE/DataQuarterBridgeTwo` (20260606), `ResearchVisitor` (20260610) — matching the documented June wave and May-26 handles.
- 252 distinct agent-grammar-matching pages enumerated; all non-incident matches are the long-running Austrian **VideoBridge** community project (known `*Bridge*` false positive, cf. wayback-cdx-sweep). **Zero new agent-grammar pages** beyond the known incident, including in the post-July-15 extension of the window (latest capture 20260911).
- This validates the CDX host-sweep methodology against a known positive: if a comparable agent-wiki wave existed on a swept host in-window, the URL signatures would surface it.

## 8. Outstanding

None. All dispatched queries completed.

## 9. Graded findings summary

| # | Finding | Grade |
|---|---|---|
| 1 | TLD-wide `.de`/`.fr` CDX marker sweep impossible on public API (403 "requires authorization") | HONEST NEGATIVE (method) |
| 2 | myxwiki.org (French XWiki farm), 511 captures Apr–Sep 2026: no agent markers; Vietnamese casino SEO-spam profiles observed, out of scope | HONEST NEGATIVE |
| 3 | Arquivo.pt full-text: German placeholder + 4 agent handles + 2 markers → all 0 results | HONEST NEGATIVE |
| 4 | BnF web archives: no public remote search interface (reading rooms only) | HONEST NEGATIVE |
| 5 | DNB web archive: reading-room-only; public catalogue metadata has zero incident-farm records; selective-crawl structure = poor hunt surface | HONEST NEGATIVE |
| 6 | ONB public CDXJ endpoint documented + verified; zero captures for wikiservice.at / dorfwiki.org roots | HONEST NEGATIVE (probes) / new reusable endpoint |
| 7 | EU Web Archive covers EU institutional sites only (no external websites) — not a .de/.fr agent-board surface | HONEST NEGATIVE (scope) |
| 8 | dorfwiki.org control: known incident pages recovered from CDX; no new agent-grammar pages through 20260911 | CONFIRMED (control) / HONEST NEGATIVE (new activity) |

## 10. Open items / recommended follow-ups

- **CDX host-sweeps for candidate hosts from sibling workers:** the viable CDX unit is per-host. If tld-sweeper surfaces .de/.fr/.at candidate hosts (urlquery targets/tags), archive-diver (or a follow-up) can run the wayback-cdx-sweep methodology (host query + signature regexes over URLs + RecentChanges reads) against each. The dorfwiki.org control proves the pipeline catches a real wave.
- **Arquivo.pt `site:de` / `site:fr` full-text variants** of the handle battery (base battery all zeros; scoped variants are cheap follow-ups).
- **BSZ (Baden-Württemberg) Archive-It collections** (Wikipedia: "Full open access for major part of snapshots… accessible via Archive-It; integrated in the SWB union catalog") — a genuinely public German regional web archive not yet mined. Candidate for a follow-up worker.
- **ONB exact-URL probes** for any .at agent-board candidates the tld-sweeper/ct-miner lanes produce.
- BnF/DNB remain unminable remotely; the only path is an on-site or agreement-based researcher — out of scope for this hunt.

## Raw evidence locations

- `/tmp/myxwiki_cdx.json` (511 CDX rows), `/tmp/dorfwiki_org_cdx.txt` (17,154 CDX rows), `/tmp/ap_beschreibe.json` (Arquivo.pt empty result), `/tmp/dnb_explain.xml`, `/tmp/dnb_mat.xml`, `/tmp/dnb_test.xml`, `/tmp/onb1.txt`, `/tmp/onb2.txt`
- NOTE: evidence kept at /tmp per worker scratch convention; key result sets will be consolidated if the coordinator requests.
