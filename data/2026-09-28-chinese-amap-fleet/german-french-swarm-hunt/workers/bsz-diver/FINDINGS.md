# BSZ-DIVER — Findings

**Worker:** bsz-diver (EUROSWARM wave 3)
**Date:** 2026-10-05 (~15:30–15:50 UTC)
**Mission:** (1) BSZ's public Archive-It collections → search for German agent-swarm traces (agent boards/wikis, harness pages, eval pages with agent grammar, Apr–Sep 2026); (2) Arquivo.pt `textsearch` `site:de`/`site:fr` scoped variants of the agent-handle battery; (3) per-host Wayback CDX on any BSZ candidate hosts. Public archive interfaces only — passive throughout. No candidate infrastructure was fetched or probed (none was found to probe).
**Status:** COMPLETE — all executable queries returned. No leads; graded findings below (1 CONFIRMED control, 1 method discovery, remainder HONEST NEGATIVES), new reusable endpoints documented.

## Endpoints documented for reuse (exact)

- BSZ Archive-It partner page: `https://archive-it.org/organizations/1180` ("Bibliotheksservice-Zentrum Baden-Württemberg (BSZ)")
- Archive-It collection page pattern: `https://archive-it.org/collections/<id>` (per-collection "Sites" / "Archived Pages" / "Full Text" tabs; full-text search is the prize endpoint)
- Archive-It replay, collection-scoped: `https://wayback.archive-it.org/<collid>/<timestamp>/<url>` — OBSERVED live in a search-engine snippet: `https://wayback.archive-it.org/8430/*/https://zollernalbkreis.landwirtschaftsverwaltung-bw.de/` (BSZ collection 8430; another BSZ collection id `22406` observed in an archive-it.org search URL). Coll-id-scoped timemap `https://wayback.archive-it.org/<collid>/timemap/link/<url>` exists on the same infra but was not reachable to test (see §1 block).
- BSZ scope documentation (live, fetched via search index): `https://wiki.bsz-bw.de/display/WEBARCHIV/FAQ` — BSZ's web-archiving service is called **SWBregio** (since 2010).
- Arquivo.pt full-text API (no key): `GET https://arquivo.pt/textsearch?q=<query>&maxItems=50` → JSON with `estimated_nr_results`, `response_items[]` (`originalURL`, `title`, `linkToArchive`, `tstamp`, …). **Operator finding (new): the `site:` operator requires a FULL hostname.** Bare-TLD `site:de` / `site:fr` returns `estimated_nr_results: 0` for every query including controls (`Berlin`, `Bundestag`). `site:.de` (leading dot) is NOT TLD scoping — it degrades to a non-scoped query (344,806 mixed-TLD results for `Bundestag`, incl. commons.wikimedia.org and fr.wikipedia.org). Verified working: `site:spiegel.de Bundestag` → 9, all spiegel.de; `site:orf.at Nachrichten` → 2,056, all orf.at; `site:www.dorfwiki.org ErneuerbareEnergien` → 1, the exact page.

## 1. BSZ Archive-It collections — located, scoped, search-blocked

**What BSZ's Archive-It presence is.** Per the BSZ-WIKI FAQ (SWBregio): *"Im Rahmen dieses Dienstes archiviert das BSZ im Auftrag deutscher kommunaler, regionaler und Kreis-Archive öffentliche Webauftritte. SWBregio besteht seit 2010."* — the BSZ archives, on commission, the public websites of **German municipal, regional and district archives** (kommunale, regionale und Kreis-Archive). Explicitly: *"SWBregio steht nicht offen für die Teilnahme privater oder kommerzieller Einrichtungen oder Privatpersonen"* — not open to private individuals, commercial entities, or private institutions. No social media, no intranet. Collections observed via the search index (partner org 1180): document-server collections (SWBdok `swbdok.bsz-bw.de`, BOA `boa-bw.de`, SaarDok, Literatur-im-Netz/DLA Marbach, Zentralarchiv-zur-Erforschung-der-Geschichte-der-Juden webarchiv, Digital Music Library `www2.bsz-bw.de/ibmdl`) plus municipal collections (Stadt Neu-Ulm incl. ZV Kläranlage Steinhäule and schools, Stadt Frankfurt/Main incl. Zoo Frankfurt, Landkreis Zollernalbkreis incl. Zollernalb-Klinikum and communes, MARCHIVUM Mannheim, Stadt Weil der Stadt, Stadt Schramberg, Stadt Renningen, …). ~567–633 sites total, all German institutional.

**INFERENCE (structural):** this corpus is librarian-selected, closed German municipal/library websites — the same class of poor hunt surface as DNB's selective crawls (archive-diver §5). Agent-swarm surfaces (open wiki farms, harness pages, agent boards) cannot enter this corpus by collection policy: there is no open wiki, board, or user-content host among the seeds. BSZ yielded **zero candidate hosts**, so task 3 (per-host Wayback CDX) is moot — nothing to sweep. (Fallback note: Archive-It crawls are additionally indexed in the main Wayback Machine, so a per-host `web.archive.org` CDX query covers BSZ crawls too if a candidate ever arises.)

**HARD STOP — IP-level rate limit on all of Archive-It's web infra.** Five attempts over ~40 min to `archive-it.org` (partner page, collections list) and `wayback.archive-it.org` (collection-8430 timemap + replay) all returned the same 470-byte body, HTTP 200: *"Rate limit reached — You've reached the limit for the number of requests that can be made in a short period of time. Please wait a moment and try again. … contact us at Aitratelimit@archive.org"*. OBSERVED: I made only ~5 requests total — the block predates my work (likely the VM's shared egress IP is flagged). The BSZ full-text search could therefore **not** be executed from this environment. Retry conditions for the coordinator: a different egress IP, a longer cooldown, or the live browser on the parent side (browser.open hit the same block from this IP). **Grade: HONEST NEGATIVE (scope) + BLOCKED (full-text search).** Given the closed-corpus scope finding, the unexecuted search is low expected value, but the block is recorded honestly rather than papered over.

## 2. Arquivo.pt — `site:de`/`site:fr` scoping is unsupported; unscoped battery all zero (calibrated)

**Method result (reusable):** bare-TLD `site:de` / `site:fr` scoping does not exist in Arquivo.pt's textsearch. Controls: `site:de Berlin` → 0 (unscoped `Berlin` → 88,596,803); `site:fr Berlin` → 0; `site:de Bundestag` → 0; `q=Bundestag&siteSearch=de` (param variant) → 0. `site:.de` is a trap — it returns non-scoped results (see endpoint section). Only `site:<full-host>` scopes. **Grade: HONEST NEGATIVE (method)** — the requested TLD-scoped variants cannot be executed; nearest viable equivalent below.

**Battery (unscoped `textsearch?q=`, `maxItems=5`/`50`, all `estimated_nr_results: 0`, `response_items: []`):**

| # | Query | estimated |
|---|---|---|
| 1 | `AgentDataUSAProbeFebX2` | 0 |
| 2 | `ApiDataHelperBridge` | 0 |
| 3 | `DataPdfBridgeThree` | 0 |
| 4 | `DataQuarterBridgeTwo` | 0 |
| 5 | `AgentDataUSA` | 0 |
| 6 | `httpbun` | 0 |
| 7 | `"zz=oai"` | 0 |
| 8–14 | archive-diver base battery (re-verified scope): `"Beschreibe hier die neue Seite"`, `ResearchHelperAgent`, `DataResearcherAlpha`, `ApiHelperPerson`, `ResearchVisitor`, `WillkommenImWiki`, `AgentOpenResearchData` | 0 (all) |

INFERENCE: every unscoped marker query is zero, so any host-scoped variant would necessarily also be zero — the TLD-scoping gap changes nothing about the conclusion.

**Calibration (makes the zeros meaningful — CONFIRMED control):**
- `q=dorfwiki` → **235 results**, including `http://www.dorfwiki.org/wiki.cgi?ErneuerbareEnergien` and `http://wikiservice.at/wiki.cgi` — OBSERVED: Arquivo.pt's index **does** contain the incident hosts' pages.
- Positive control `q=site:www.dorfwiki.org ErneuerbareEnergien` → **1 result**, the exact page — specific-page findability confirmed.
- Therefore the 15 zero-results are genuine index negatives, not a findability artifact. Caveat (standard): absence in Arquivo.pt's crawl corpus, not proof of nonexistence on the live web.

**Grade: HONEST NEGATIVE (all 15 markers).**

## 3. Per-host Wayback CDX on BSZ candidate hosts

**Not applicable — no candidate hosts.** BSZ's corpus contains no open wikis, boards, or harness-like surfaces by collection policy (§1). Logged per keep-all; not skipped, just empty input.

## 4. Graded findings summary

| # | Finding | Grade |
|---|---|---|
| 1 | BSZ Archive-It = SWBregio: German municipal/regional/district-archive websites only, closed to private/commercial/individuals; no open wiki/board/harness surfaces by policy → zero candidate hosts | HONEST NEGATIVE (scope) |
| 2 | archive-it.org + wayback.archive-it.org IP-level rate-limited from this VM (5 attempts / ~40 min, ~5 requests made) — BSZ full-text search not executable here; retry needs different egress IP | BLOCKED (method) |
| 3 | Arquivo.pt `site:` requires full hostname; bare-TLD `site:de`/`site:fr` unsupported (0 on all controls); `site:.de` degrades to non-scoped (mixed-TLD results) — do not use | HONEST NEGATIVE (method) / new reusable finding |
| 4 | Arquivo.pt: 15 agent-swarm markers (7 base + 8 extended) → all 0 results | HONEST NEGATIVE |
| 5 | Calibration: Arquivo.pt indexes dorfwiki.org/wikiservice.at (235 `dorfwiki` hits; exact-page control returns 1) → zeros are genuine index negatives | CONFIRMED (control) |
| 6 | No BSZ candidate hosts → per-host Wayback CDX lane moot | n/a (empty input) |

## 5. Open items / recommended follow-ups for the coordinator

- **BSZ full-text search** (agent handles + `httpbun` + `zz=oai` against collections on org 1180) remains unexecuted due to the IP block — retry from a non-flagged egress IP or the live browser. Low expected value given the closed-corpus scope finding, but it is the one unchecked box.
- **Arquivo.pt `site:` host-scoped queries** are available for any concrete .de/.fr/.at candidate hosts sibling workers surface (e.g. `site:<host> AgentDataUSAProbeFebX2`) — syntax verified working.
- Note for future workers: do **not** use `site:de`, `site:fr`, or `site:.de` on Arquivo.pt — they silently produce wrong/empty results.

## Raw evidence locations

- `raw/ap_test_sitede.json`, `raw/ap_ctl_*.json` (site: syntax controls), `raw/ap_b2_*.json` (marker battery + `site:.de` trap demo), `raw/ap_cal_*.json` (dorfwiki/orf.at calibration + positive control)
- `/tmp/bsz_collections.html`, `/tmp/bsz_coll2.html`, `/tmp/bsz_org3.html`, `/tmp/bsz_org4.html` (rate-limit bodies), `/tmp/wait_timemap.txt`
- NOTE: evidence kept at worker `raw/` per convention; full observed values retained, nothing redacted.
