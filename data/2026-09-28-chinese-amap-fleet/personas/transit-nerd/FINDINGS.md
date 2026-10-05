# THE TRANSIT NERD — FINDINGS

**Date:** 2026-10-05 (UTC) · **Status:** complete · **Verdict: no agent-shaped transit/GTFS activity found.** Honest negative, but with two useful constraints and one methodological blind spot.

## Verdict

Across all three corpora and both live surfaces, zero confirmed agent-shaped traffic against GTFS-realtime endpoints or transit APIs. The negative is strong: I checked the exact substrings agents would leave (`gtfs`, `vehiclepositions`, `tripupdates`, `servicealerts`, `direction/transit`, provider domains) and every hit was a false positive.

## 1. Local corpus verification (OURS / KNOWN / NEW classification)

| Corpus | Query | Hits | Classification |
|---|---|---|---|
| Amap fleet (2,141 events) | `gtfs`, `transit`, `direction/transit` | 0 | **OURS-clean** — the fleet does map POI queries only |
| openai-agent-traces (589,972) | `gtfs` | 1 | FALSE POSITIVE — digest string `JRXKXYPHN2W7CULVR4UHPGWGTFSY3JMT` contains "GTFS" coincidentally (maryland-edstats arquivo capture, 2026-05-06) |
| openai-agent-traces | `transit\|vehiclepositions\|tripupdates\|servicealerts` | 6 | FALSE POSITIVE — `owl.transitions.css` on data.nysed.gov (doe/crdc incident cluster, same digest `CSGOSUY2RW4QDR2VEVS6H6ISFDK4RH2K`) |
| openai-agent-traces | `mbta` | 30 | FALSE POSITIVE — digest `FMUI227JSFFZMBTAXKVNJVBPZAW67Y2P` contains "MBTA" coincidentally (doe-crdc GetStateEstimation records) |
| openai-agent-traces | `api.511.org`, `trimet.org`, `api-endpoint.mta`, `gtfs.de`, `translink`, `511ny`, `citymapper` | 0 | **clean** |
| oai-tag-sweep | `transit` | 8 | FALSE POSITIVE — collusion-wiki revision `TransitoryAsciiHub` (2026-05-26) |
| Amap fleet raw/analysis, ALL_LINKS.md, infra-watchlist | `gtfs\|transit` | 0 | **clean** |

**Constraint #1 (new, from the negative):** the Amap fleet's task family is POI-only. 2,141 records hit `restapi.amap.com` exclusively via POI paths (`getPoiInfo` carriers, `v3/place/detail` ×1) and never once touched Amap's transit-routing API (`/v3/direction/transit/integrated`). A map-recon fleet that deliberately or incidentally avoids transit is a task-shape constraint — worth feeding to the Evaluator lane.

## 2. Live urlquery htmx (curl variant; urllib variant hit IncompleteRead)

| Query | Result | Assessment |
|---|---|---|
| `gtfs` | 15 reports (vlkvh.com, lihi1.me, jojobet-*.vip ×8, monitrexai.live, etc.) | FALSE POSITIVES — Turkish gambling/phishing noise; htmx keyword search matches scan content, not just URLs |
| `vehiclepositions` | 0 | clean |
| `api.511.org` | 0 | clean |
| `realtime.mbta.com` | 0 | clean |
| `gtfs-realtime` | 4 reports | turlocktransit.com (2025-12-27), cascadeseasttransit.com (2025-10-06) — ordinary agency-site scans; `b.ntyx.dev` ×2 (2026-03-07, 2026-03-11) — dev subdomain, **could not inspect** (report-page fetches time out from VM; search API works, page fetches don't) |
| `url.domain:trimet.org` | 3 bare-domain homepage scans (2025-06-28, 2025-10-25, 2025-11-19) | ordinary |

## 3. Live urlscan.io (search API works; result API is 403 for anonymous)

| Query | Result | Assessment |
|---|---|---|
| `page.url:gtfs` | 8 results | ALL dev/infra self-scans, not agent-shaped: `gtfs-tracker-app.pages.dev`, `gtfs-tracker-ui.pages.dev` (automatic), `gtfs-tools-*.vercel.app` (api), `gtfs-zip-download.bonanza.workers.dev` ×3 (api, Sep 7/20/24), `gtfs-nmbs-rt-trip.ingestion.production.stoomlink.io` (api, Sep 19 — Belgian-rail realtime ingestion endpoint), `gtfs-data-exchange.com` (api) |
| `page.url:vehiclepositions` | 0 | clean |
| `page.url:tripupdates` | 0 | clean |
| `filename:gtfs` | trimet.org scan (2026-10-04, ordinary) | context |

**Constraint #2 (new):** transit-data infrastructure IS programmatically scanned on a cadence (the bonanza Cloudflare worker 3× in September; the stoomlink NMBS ingestion pipeline) — but the submitters are the projects' own developers (api-submitted deploy scans). The surface the brief hypothesized is real; the actors are human devs. If an agent ever does use GTFS tooling as staging, it will hide inside exactly this dev-infra noise — watch-list the pattern, not the current actors.

## 4. Methodological blind spot (the actually important finding)

**GTFS-RT endpoints return protobuf, not HTML.** urlquery's scanner is page-oriented: an agent pulling `.../gtfs-realtime/vehiclepositions.pb` every 30 seconds produces no meaningful "report" — no DOM, no screenshot, no JS. The same applies to urlscan. **Both of our live surfaces are structurally blind to GTFS-RT-as-cover-traffic.** A negative on urlquery/urlscan does not rule out agents using transit feeds as cover traffic or live-data sources. The places that *would* see it — feed access logs, CDN logs, the agents' own dead-drop payloads referencing transit data — are not public. Recommendation: add "transit-data references inside dead-drop payloads / beacon bodies" as a check for the dead-drop-retrieval lane (codebreaker has live webhook.site inboxes; grep retrieved payloads for gtfs/transit strings).

## Steps taken

1. Egress test: urlquery.net reachable via search API (page fetches time out — flaky, not dead); urlscan search API works, result API 403-anon.
2. Grepped all three corpora for gtfs/transit/vehiclepositions/tripupdates/servicealerts + 8 provider domains; classified every hit (all false-positive substrings).
3. Grepped Amap fleet for transit-routing API paths; enumerated actual restapi.amap.com paths used.
4. Ran 8 urlquery htmx searches (curl variant after urllib IncompleteRead); 4 urlscan searches.
5. Attempted report-detail inspection for b.ntyx.dev ×2 and the bonanza worker scans — blocked by VM→urlquery fetch timeouts and urlscan 403-anon.

## Open items

- `b.ntyx.dev` (urlquery reports `320d5689-1628-419c-9b7a-0541cb4d867a`, `4dc811a4-5a53-49c3-bf19-b4a47211b6a5`, Mar 2026): only "gtfs-realtime"-matched dev host found; worth one look when urlquery page fetches work from the VM.
- Dead-drop payload grep for transit strings (recommendation above) — needs codebreaker lane, not this one.

## Observed URLs (appended)

### urlquery htmx search hits
- https://urlquery.net/report/b89e9e2b-c0ba-4b0a-978b-5a8a0e2fc33a (vlkvh.com — gtfs keyword false positive)
- https://urlquery.net/report/0e164b63-4407-4647-9356-fae8b8c9d0a3 (turlocktransit.com)
- https://urlquery.net/report/306ab9a1-6351-44b8-95da-7ee387dd9030 (cascadeseasttransit.com)
- https://urlquery.net/report/320d5689-1628-419c-9b7a-0541cb4d867a (b.ntyx.dev — uninspected)
- https://urlquery.net/report/4dc811a4-5a53-49c3-bf19-b4a47211b6a5 (b.ntyx.dev — uninspected)
- https://urlquery.net/report/70e36f03-7b00-4a98-b7d6-c00353809bc7 (trimet.org)
- https://urlquery.net/report/cac3adc8-55f7-456a-babf-2e3ede13ddb6 (trimet.org)
- https://urlquery.net/report/4adb9440-d68e-42f6-98e7-2faf1ee0882e (trimet.org)

### urlscan hits
- https://urlscan.io/result/01a10917-4732-77a7-969f-6638ca6784dc/ (trimet.org, 2026-10-04)
- gtfs-tracker-app.pages.dev (urlscan 2026-10-02)
- gtfs-tracker-ui.pages.dev (urlscan 2026-09-30)
- gtfs-tools-g5y080hqu-tmdincs-projects.vercel.app (urlscan 2026-09-29)
- gtfs-zip-download.bonanza.workers.dev (urlscan 2026-09-07 / 09-20 / 09-24)
- gtfs-nmbs-rt-trip.ingestion.production.stoomlink.io (urlscan 2026-09-19)
- gtfs-data-exchange.com (urlscan 2026-09-09)

### Reference (checked, no agent activity)
- https://api.511.org (zero urlquery submissions)
- https://realtime.mbta.com (zero urlquery submissions)
- https://restapi.amap.com/v3/direction/transit/integrated (zero fleet usage — POI-only confirmed)
