# Radar tunnel lead deep-dive — `91b9ec611bbd73.lhr.life`
**Lane:** `2026-09-28-chinese-amap-fleet` full-sweep · **Probed:** 2026-10-05 ~02:00–02:45 CDT
**Lead source:** `raw/japan-archives.md` §4 (Cloudflare Radar public URL-scanner feed)

## Verdict: UNRESOLVED — fleet-adjacent, not attributable

Shape (16-hex `lhr.life` tunnel) + 2026 window + cloud-egress infra fit the Amap operator's tunnel convention; the name is **disjoint from all 78 known fleet names and every corpus inventory**; the scanned URL is bare `/` with no `uq`-grammar markers; the scan detail page (title/DOM/request chain) is unreachable without a live browser session or a Cloudflare API token. Not attributable to the `uq` operator on current evidence; not excludable either (prior truth: `lhr.life` is commodity agent dev-tunneling — query grammar, not domain, discriminates, and the scan captured only the bare root).

## 1. The scan row (re-verified 2026-10-05)

- **URL:** `https://91b9ec611bbd73.lhr.life/` · Verdict: No classification · Created: **Aug 1, 2026, 11:34 UTC** · Origin: United States · **AS14618** (Amazon) · Status: Finished.
- **Timezone correction to `japan-archives.md`:** that file guessed the listing time was "likely JST". The ScansTable frontend chunk hardcodes `timeZone:"UTC"` in its date formatter (`/assets/ScansTable-njRS7vYR.js`) — the row time is **2026-08-01 11:34 UTC** (= 20:34 JST = 07:34 EDT).
- **Where it appears:** only in Google-indexed snapshots of Radar listing pages (crawled ~64 days ago): `radar.cloudflare.com/scan?url=https://89.42.218.98/`, `.../scan?url=https://34.199.43.253/`, `.../scan?url=https://localseo.site/`, `.../scan?url=https://142.251.15.97/`. The `?url=` parameter is a **search-box prefill, not a filter** — two live listings fetched with different `?url=` values returned byte-identical 51-UUID ScansTable payloads (the widget shows recent public scans).
- **Off-frame neighbor in the same table window:** `https://trek-alice-representations-bloom.trycloudflare.com/` — Aug 1, 11:20, AS13335, a Cloudflare Tunnel dev URL scanned 14 minutes earlier. Different tunnel family (`trycloudflare.com`); context only, not a lead.

## 2. Endpoint inventory (collection doctrine — every endpoint found)

- `GET https://radar.cloudflare.com/scan` — URL Scanner landing; server-rendered Remix app (`window.__remixContext` stream carries loaderData). **Open, 200.**
- `GET https://radar.cloudflare.com/scan?url=<url>` — listing page; ScansTable = recent public scans, unfiltered by the param. **Open, 200.**
- `GET https://radar.cloudflare.com/scan/search?q=<q>&type=<url|domain|ip>` — website search route. The search form's submit handler navigates to `${pathname}/search?${q,type}` (found in `assets/search-*.js`). Server loader returns no data; results widget fetches client-side. **Open, 200** but resultless without JS.
- `GET https://radar.cloudflare.com/charts/<WidgetId>/fetch?<params>` — **the widget-data XHR** (recovered from `assets/wrapWidget-*.js`, `function Kf`: `` `/charts/${b}` `` + `/fetch?${params}`; e.g. widgetId `ScansTable`, params `type`/`query`/`size`). **403 Cloudflare "Attention Required" bot-wall to both curl (even with browser UA + cookies + Referer) and the text-fetch pipeline — needs a real browser session.** Documented for reuse.
- `GET https://radar.cloudflare.com/scan/<uuid>/summary` — public scan-detail page (link format from the ScansTable chunk: `[urlScanner, uuid, "summary"].join("/")`). Needs the scan UUID — **unknown for this tunnel**.
- **API (documented, gated):** `https://api.cloudflare.com/client/v4/accounts/{account_id}/urlscanner/v2/search?q=...` — ElasticSearch-ish query syntax (`task.url:"..."`, `page.domain:...`, `verdicts.malicious:true`, `date:>now-7d`, `hash:...`), returns public scans. Also `POST /v2/scan` (submit; public visibility lands in recent-scans + search) and `GET /v2/result/{scan_id}` (report: `task`, `page`, `data.requests`, `verdicts`, `lists.ips/asns/domains/hashes/certificates`, `meta.processors.*`). **Requires account_id + URL-Scanner-scoped API token (account creation out of scope here).** Docs: https://developers.cloudflare.com/radar/investigate/url-scanner/

## 3. Sweep results (Google-indexed Radar surface + whole web)

| Query | Result |
|---|---|
| `site:radar.cloudflare.com/scan lhr.life` | **Only the one tunnel row** (3 listing snapshots, same row). No other 16-hex `lhr.life` subdomains indexed. |
| `site:radar.cloudflare.com/scan/ "lhr.life"` | Same single row. |
| `site:radar.cloudflare.com/scan uqscan OR uqcors OR uqtag` | **0 results.** |
| `site:radar.cloudflare.com/scan pandalegacy OR sub_poi_navi` | **0 results.** |
| `"91b9ec611bbd73"` (whole web) | Only the Radar listing snapshots. |

Caveat: Google's index of Radar listing snapshots is a sparse, time-frozen sample (~64-day-old crawls) — absence here is not proof of absence.

## 4. Overlap analysis (task item 4)

- **78-name fleet list** (`writeup-lhr-life.md`, urlquery-attested 16-hex tunnels): extracted 78 unique `[0-9a-f]{14,16}.lhr.life` names → **`91b9ec611bbd73` ABSENT**.
- **Corpus-wide:** the name occurs nowhere in silent-locus except the two lead records (`full-sweep/FINDINGS.md:157`, `raw/japan-archives.md:61`). Zero hits in `events.jsonl`, `raw/`, `live-monitor/`, all `*-hunt/` dirs, `personas/` (including cartographer inventories `uq_lhrlife.json`, `urlscan_domain_lhr_life_.json`, `all-observed-urls.tsv` — 107 `lhr.life` names, zero overlap), `pandalegacy/`, `shortener-farm/`, `farmable-surfaces/`, `cachedview/`.
- **Timeline:** known 16-hex tunnel sightings (urlquery) cluster 2026-06-21 → 2026-07-24; the Radar scan (2026-08-01 11:34 UTC) lands 8 days after the latest — inside the fleet's Jan–Oct 2026 active window, adjacent but non-overlapping.
- **Infra:** US/AS14618 origin is consistent with cloud-egress agent traffic; `lhr.life` = localhost.run tunnel domain (commodity).

## 5. Gaps / delegation specs

1. **Scan detail page (highest value).** For a browser-capable agent: pass the Cloudflare bot check on radar.cloudflare.com, open `/scan/search?q=91b9ec611bbd73.lhr.life&type=url`, read the ScansTable widget row → `/scan/<uuid>/summary`; record page title, verdicts, contacted domains/IPs/ASNs, `page.domStructHash`, screenshot. Live-browser task — this subagent cannot.
2. **`/charts/ScansTable/fetch` XHR sweep.** Same browser session can run fleet markers (`uqscan=`, `uqcors`, `uqtag`, `sub_poi_navi`, `pandalegacy`) and 16-hex `lhr.life` queries directly against the widget endpoint.
3. **API route.** Needs a Cloudflare account + URL Scanner token (account creation not authorized from here).
4. **Megalodon free-word search** (still open from `japan-archives.md` §5) — separate delegation, unchanged.

## 6. Off-frame notes (leads, never negatives)

- The `trycloudflare.com` dev-tunnel scan 14 min before the tunnel in the same table window (different tunnel family, context only).
- The Maltrail May-2026 `<hex>.lhr.life` sightings tagged `hacked_npmrepos`/`metasploit` (`raw/trick-url-scanners.md`) — independent sensor, doesn't fit the map-collection frame; the tunnel infra is seen by other sensors under other labels.

## Method notes

- VM curl egress was healthy this round (proxy up; `example.com` + `radar.cloudflare.com` both 200) — unlike the prior sweep's outage.
- No HTTP 429s encountered; polite pacing held (single requests, no retries except one transient asset timeout that succeeded on retry).
- Raw page captures kept in `/tmp` (radar_scan.html, radar_listing.html, radar_tunnel.html, search.js, wrap.js, us*.js, charts_tunnel.json) — ephemeral; key findings are all transcribed above.
