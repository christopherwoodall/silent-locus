# THE LIGHTHOUSE KEEPER — FINDINGS

Persona: maritime/AIS agent-shape hunt. Run 2026-10-05 ~06:00–06:15 UTC. Egress flapping (urlquery.net intermittent); htmx via curl variant worked between outages. Nothing pushed.

## Verdict: no agent-shaped maritime activity found — clean negative on our corpora, thin-and-human on public surfaces

## 1. Local corpus verification (CLEAN NEGATIVE)

Word-boundary grep for `mmsi|aisstream|marinetraffic|vesselfinder|vesseltracker|fleetmon|shipxplorer|myShipTracking` across:
- `data/2026-09-28-chinese-amap-fleet/events.jsonl` (2,141 records): **0 hits**
- `data/2026-10-03-openai-agent-traces/events.jsonl` (589,972 events): **0 hits**
- `data/2026-10-01-oai-tag-sweep/events.jsonl`: **0 hits**

No maritime terms in any of our three corpora. Classification: OURS — negative, nothing to reclassify.

## 2. urlquery htmx — homepage-level only, no deep vessel activity

| Query | Results |
|---|---|
| `url.domain:marinetraffic.com` | 2 reports, both bare homepages (2026-02-24, 2026-06-15). No `/en/ais/details`, no MMSI/IMO URL patterns. |
| `url.domain:vesselfinder.com` | 7 reports, all bare homepages (2024-02 → 2026-01). |
| `url.domain:aisstream.io` | 0 reports. |
| keyword `marinetraffic.com/en/ais` | 0 reports. |
| keyword `mmsi` | 0 reports. |
| keyword `vessel tracking` | 10 reports — see §4. |

No bulk MMSI enumeration, no grid-walk query patterns, no machine-cadence AIS pulls visible in urlquery. (Caveat: htmx search is a weak negative per the Polyglot's finding — known-live records don't always surface.)

## 3. urlscan.io — human-shaped, two curiosities

`domain:marinetraffic.com` → 23 results:
- Mostly bare homepage scans (Sep 5–30, 2026).
- One map-view URL: `www.marinetraffic.com/fr/ais/home/centerx:1.6/centery:49.1/zoom:9` (2026-09-30) — single, human-shaped.
- **Curiosity A:** `dyr63-baaaa-aaaal-ai6zq-cai.icp0.io/vessels-and-surveillance.html` + `/radar.html` — an Internet Computer canister hosting an "iCare." template site with a vessel-surveillance page, submitted in PAIRS ~20–40s apart on Sep 7, 14, 21, 28. Machine-cadence-shaped but content is a static template site (no AIS API calls found in HTML). Reads as site-owner self-checks or an uptime monitor, not agent-shaped. Filed as KNOWN-context, not a find.
- **Curiosity B:** `www.ww3tracker.co` (Sep 13, 16) — war-tracking hobby site, human-shaped.

`domain:aisstream.io` → 1 result, and it's `secretparisien.com` (false positive). No agent-shaped AIS API consumption on urlscan.

## 4. "vessel tracking" keyword hits — weak leads only

- `xplore-atx-a6279178.base44.app` (2026-10-04) — base44 is an AI no-code app builder; an agent-built vessel-tracking app would be exactly our shape. But the report's HTTP traffic shows no maritime content and stock Firefox 134 UA; the keyword match is in report metadata, not page content. **Weak watch item, not a find.**
- `regs4.ships.com` (2026-10-04), `tradlinx.com` (2026-09-22) — shipping-industry sites, no agent grammar visible. Watch items.

## 5. AIS-as-dead-drop angle — untested vector, no evidence found

The hypothesis (vessel name/destination free-text fields as globally-visible dead-drops, à la the codebreaker's HTTP beacons) produced no hits on public surfaces. No encoded-payload-shaped vessel metadata found in urlquery/urlscan. This remains an open research vector, not a negative — the right test surface is a live AIS aggregator feed, not scan archives.

## Evidence grading summary

- **GENUINELY NEW agent-shaped maritime finds: 0**
- KNOWN (human browsing / site-owner checks): the urlscan marinetraffic corpus, the ICP canister pairs, ww3tracker
- WATCH (weak, needs a live look): base44 vessel-tracking app, regs4.ships.com

## Observed URLs (full list)

- https://urlquery.net/report/f5315b45-ea0d-4114-ab93-659ee3de5ba8 (xplore-atx-a6279178.base44.app)
- https://www.marinetraffic.com/ (urlquery reports 7c5c6149-e728-41fe-853f-85bd3335d363, 1d8ae00b-3188-435a-836f-c54b71cacca6)
- https://www.vesselfinder.com/ (urlquery reports 62c8d4d8-e687-4b33-b95f-62e0716d8254, d7725bd1-290a-4e17-85a8-234db939c988, 8bdf5e49-e602-4e8b-9ecc-8f11fc860652, 8acc2057-bff7-4bdf-8420-5f69ce032db2, 4248b885-d54d-413b-8f18-4ab368ab5494, ab857d97-73f1-4d34-8e96-3c4d0ff26387, b16a7d8b-8ec7-4961-8525-32b2929fa3eb)
- https://www.marinetraffic.com/fr/ais/home/centerx:1.6/centery:49.1/zoom:9
- https://dyr63-baaaa-aaaal-ai6zq-cai.icp0.io/vessels-and-surveillance.html
- https://dyr63-baaaa-aaaal-ai6zq-cai.icp0.io/radar.html
- https://www.ww3tracker.co/
- https://xplore-atx-a6279178.base44.app
- https://regs4.ships.com
- https://tradlinx.com/
- https://www.myshiptracking.com/
- https://containerstrack.net/
- https://www.schiffstracking.de/
- https://secretparisien.com/
