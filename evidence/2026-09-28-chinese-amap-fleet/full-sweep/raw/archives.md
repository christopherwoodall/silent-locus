# Web-archive sweep — operator markers (2026-10-04/05)

Surface: Wayback Machine CDX (primary), Arquivo.pt (CDX + full-text), Common Crawl Index (secondary).
Scope: hunt for NEW agent/swarm fleets via operator URL markers in archived URLs.
Known operator (excluded from "new"): Chinese Amap-map data-collection fleet, `uqscan=<word><date>` tags,
localhost.run (`<hex>.lhr.life`) tunnels, is.gd shorteners, active Jan–Oct 2026.

## Endpoint inventory (collection doctrine — reusable, no keys needed)

1. **Wayback CDX** — `GET https://web.archive.org/cdx/search/cdx?url=*MARKER*&output=json&limit=300&collapse=urlkey`
   - No key, no special headers. Mid-string `*` wildcard substring match works on the URL key.
   - `matchType=domain` form (`url=lhr.life&matchType=domain`) is far cheaper than `*lhr.life*` (which 504'd).
   - RATE BEHAVIOR (verified this run): first query fast (~2–30s); 8 parallel queries → all timed out /
     proxy-aborted (curl 28 / 56). Sequential queries with ~45s spacing succeed reliably. Budget ~1 req/45s.
2. **Arquivo.pt wayback-cdx-server** — `GET https://arquivo.pt/wayback/cdx?url=<url>&matchType=domain|prefix&limit=N&output=json`
   - No key. `matchType=domain|prefix` verified. `filter=original:.*re.*` is SILENTLY IGNORED
     (returns unfiltered fuzzy matches flagged `is_fuzzy:1`) — never trust filtered results here.
   - No mid-string wildcards. `lhr.life` domain query → HTTP 200, 0 records (no coverage).
3. **Arquivo.pt full-text** — `GET https://arquivo.pt/textsearch?q=<kw>&maxItems=50` (Accept: application/json)
   - Returns `{"estimated_nr_results":N,"response_items":[...]}` with `originalURL`, `tstamp`,
     `linkToArchive`, `linkToExtractedText`, snippet. Host is slow from this VM (~40–50s/query).
   - The site's own search is a server-rendered form, NOT XHR — `/js/search-tools.js` only rewrites form
     fields, so there is no lighter frontend endpoint to replicate; direct `textsearch?q=` is the endpoint.
   - Queries containing dots (`uqcors.html`, `lhr.life`) → HTTP 400
     `{"message":"Please use the following Arquivo.pt APIs to search for URLs: URL search: CDX server API:
     https://arquivo.pt/cdxserverapi / Memento API: https://arquivo.pt/memento"}` — route those to CDX.
4. **Common Crawl Index** — `GET https://index.commoncrawl.org/<COLL>-index?url=<prefix>&output=json&limit=N`
   - No key. `collinfo.json` lists collections (latest at sweep: CC-MAIN-2026-39, 2026-09-04→17).
   - `filter=url:.*regex.*` on a broad prefix is UNRELIABLE: identical query shape returned 404-empty on
     CC-MAIN-2026-39 and 504-gateway-timeout on 2026-34/30/25 and on a known-present sanity term.
     Use only unfiltered prefix/domain queries; treat filtered CC results as inconclusive.

## Per-marker verdicts

### 1. `uqscan=` — CLEAN NEGATIVE
- Wayback `url=*uqscan=*` → `[]` (HTTP 200, 3 bytes).
- Arquivo textsearch `q=uqscan` → 1 hit, false positive: `http://www.freewebtown.com/mioera/hqscan.html`
  archived 2008-10-25 (fuzzy token match on "h_q_s_c_a_n"). No operator content.
- CC `restapi.amap.com/*` + uqscan filter: 2026-39 → 404 "No Captures found"; 2026-34/30/25 → 504 (inconclusive).
- Read: Amap API URLs with rotating query params are essentially never web-crawled; absence in archives
  is expected, not exculpatory. No new fleet signal.

### 2. `uqcors.html` — CLEAN NEGATIVE
- Wayback `url=*uqcors.html*` → `[]` (HTTP 200, 56s).
- Arquivo textsearch → HTTP 400 (dot rule; routed to CDX, no URL-form hits possible via textsearch).

### 3. `lhr.life` — HITS, but NOT a new fleet (4 unrelated localhost.run exposures)
- Wayback `url=lhr.life&matchType=domain&limit=100&collapse=urlkey` → 100 captures, 4 hex subdomains
  (raw: `/tmp/archivesweep/wb_lhr_domain.json`):
  | host | caps | window | what it is |
  |---|---|---|---|
  | `02e05dc4ba9134.lhr.life` | 77 | 2023-05-21 14:29:03→30 (27s burst) | Stable Diffusion WebUI (`/content/stable-diffusion-webui/...`, `?__theme=dark`) — Colab SD instance tunneled publicly |
  | `040aa4f2653ad9.lhr.life` | 11 | 2022-01-16 14:43:55→50:41 | Snapchat cookie-consent page assets (`snapchat.com/home/cookie-*.svg`, `accounts/static/...`) |
  | `000bc54d7ac2a6.lhr.life` | 7 | 2025-04-13 12:35:47→48 | **Hikka Userbot** (Telegram userbot) web UI — "Heroku userbot", `/check_session`, sakura css/js (archived root fetched and read) |
  | `02027d0371c0b0.lhr.life` | 5 | 2024-12-13 02:46:55→56 | qBittorrent WebUI login page (`/css/login.css?v=hgm8p9`, `/scripts/login.js`) |
- Burst shapes are crawler page+asset fetches (seconds), not fleet parallelism. None in the Amap fleet's
  Jan–Oct 2026 window; none carry agent/swarm markers (no tag grammars, no API-call bursts, no harness infra).
- Arquivo CDX domain query → 0 records. Arquivo textsearch → 400 (dot rule).
- Verdict: confirms the surface WORKS for tunnel exposures (lead, not negative — localhost.run exposures
  do get archived), but these four are individual hobbyist/consumer exposures, not an agent fleet.

### 4. `pandalegacy` — CLEAN NEGATIVE (operator sense)
- Wayback `url=*pandalegacy*` → `[]` (HTTP 200).
- Arquivo textsearch `q=pandalegacy` → 53 results, ALL the unrelated Fortnite creator PandaLegacy
  (deviantart.com/pandalegacy, Tribal Wars player rankings, wallpaper blogs), 2007–2020. Zero operator use.
- Context: `pandalegacy20261004` / `pandalegacy1791089321` are OUR OWN 2026-10-04 probe markers
  (attribution retracted, see `../pandalegacy/FINDINGS.md`); neither our probes nor organic operator use
  appear in any archive.

### 5. `sub_poi_navi` — CLEAN NEGATIVE
- Wayback `url=*sub_poi_navi*` → `[]` (HTTP 200, 23s).
- Arquivo textsearch → 0 results.

### 6. `mf075827` — CLEAN NEGATIVE
- Wayback `url=*mf075827*` → `[]` (HTTP 200, 20s).
- Arquivo textsearch → 0 results.

### 7. `sum074114` — CLEAN NEGATIVE
- Wayback `url=*sum074114*` → `[]` (HTTP 200, 22s).
- Arquivo textsearch → 0 results.

### 8. `3JlIp7` — CLEAN NEGATIVE
- Wayback `url=*3JlIp7*` → `[]` (HTTP 200, 15s).
- Arquivo textsearch → 0 results.

### 9. `webhook.site` + amap — CLEAN NEGATIVE
- Wayback `url=*webhook.site*&filter=original:.*amap.*&limit=100&collapse=urlkey` → `[]` (HTTP 200).
  (Wayback CDX `filter=` honored here, unlike Arquivo's.)

## Bottom line
No undiscovered agent/swarm fleet found in web archives for any of the 9 marker queries. The one
surface-positive (`lhr.life`) resolved to four unrelated consumer localhost.run exposures, the largest a
Stable Diffusion WebUI tunneled in May 2023 — a genuine exposure class worth noting (tunnel URLs DO get
archived, so the surface has recall for future tunnel-using fleets), but no fleet behavior attached.

## Raw evidence (ephemeral, /tmp/archivesweep/)
`wayback_uqscan_.json` (`[]`), `wb_pandalegacy.json` (`[]`), `wb_uqcors_html.json` (`[]`),
`wb_sub_poi_navi.json` (`[]`), `wb_mf075827.json` (`[]`), `wb_sum074114.json` (`[]`),
`wb_3JlIp7.json` (`[]`), `wb_webhook_amap.json` (`[]`), `wb_lhr_domain.json` (100 rows, the 4 hosts),
`lhr_checksession.html` (Hikka userbot root), `cc_basic.json`, `cc_collinfo.json`,
`arq_ts_*.json` (textsearch per marker), `arq_cdx_*.json` (unfiltered false positives — filter ignored),
`arquivo_home.html`, `search-tools.js`.

## Open / blocked (not skipped)
- Megalodon (megalodon.jp) — keyless-capture archive with public index, highest-EV unprobed archive per
  2026-10-03 research; anti-bot checkbox → needs live-browser session, out of scope for this subagent.
- Common Crawl regex-filter queries remain unreliable (404/504 flip-flop); unfiltered prefix queries work.
- Wayback wildcard for very broad markers (`*lhr.life*`) 504s — always prefer `matchType=domain`.
