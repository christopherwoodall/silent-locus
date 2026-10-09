# German Hunt — Findings (2026-10-05)

Verdict: **no German agent fleet on urlquery.net.** The German web ecosystem shows no Amap-fleet analog — no systematic bursts against German targets, no German-language agent programs on carriers, no German native infra in agent use. Honest zeros throughout.

## German map/POI targets (all clean)

| Target | Hits | Notes |
|---|---|---|
| `url.domain:openstreetmap.de` | 0 | |
| `url.domain:komoot.com` | 0 | |
| `url.domain:graphhopper.com` | 0 | German routing company |
| `url.domain:maps.wikimedia.org` | 0 | |
| `url.domain:govdata.de` | 0 | German federal open data |
| `url.domain:atlas.bayern.de` | 0 | BayernAtlas geoportal |
| `url.domain:geoportal.berlin.de` | 0 | Berlin geoportal |
| `url.domain:nominatim.openstreetmap.org` | 0 | OSM geocoder |
| `url.domain:photon.komoot.io` | 0 | Komoot's geocoder (German) |
| `url.domain:here.com` | 1 | Routine |
| `url.domain:openrouteservice.org` | 1 | Routine (Heidelberg) |
| `url.domain:tomtom.com` | 3 | Routine |
| `url.domain:outdooractive.com` | 1 | Single member-profile scan, not agent-shaped |
| `url.domain:meinestadt.de` | 1 | Homepage scan, Jan 2026 |
| `url.domain:gelbe-seiten.de` | 0 | Yellow pages |
| `url.domain:dasoertliche.de` | 0 | Phone directory |

## German data-collection targets (jobs, prices, classifieds — Amap-analog task families)

| Target | Hits | Notes |
|---|---|---|
| `url.domain:stepstone.de` | 0 | Jobs |
| `url.domain:idealo.de` | 0 | Price comparison |
| `url.domain:immowelt.de` | 0 | Real estate |
| `url.domain:immobilienscout24.de` | 1 | Routine |
| `url.domain:lieferando.de` | 2 | Routine |
| `url.domain:11880.com` | 1 | Routine |
| `url.domain:bahn.de` | 1 | Routine |
| `url.domain:kleinanzeigen.de` | 12 | All routine: external-link redirects, homepage scans |
| `url.domain:check24.de` | 4 | All routine |
| `url.domain:spiegel.de` | 5 | Homepage scans |
| `url.domain:tagesschau.de` | 2 | Homepage scans |
| `url.domain:de.wikipedia.org` | 0 | |
| `url.domain:dwd.de` | 0 | Deutscher Wetterdienst |

## German native infra

| Service | Hits | Verdict |
|---|---|---|
| `url.domain:pastebin.de` | 2 | Homepage + blog scans only. Not agent infra. |
| `url.domain:t1p.de` | 6 | Random short-link scans (Nov 2025–May 2026), no agent markers. |
| `url.domain:linkvertise.com` | 55 | German monetized shortener; profile/homepage scans only. Requires accounts — same login-wall dynamic as t.cn/dwz.cn. |
| `url.domain:deepl.com` | 18 | Homepage, app downloads, share links. NOT used as a fetch-proxy relay (unlike fanyi.baidu.com/transpage in the Chinese fleet). |

## Relay stack with German targets

| Pivot | Hits | Verdict |
|---|---|---|
| `r.jina.ai berlin` | 64 | All noise (dantheduck.tech / Appwrite harness pages mentioning Berlin) |
| `webhook.site berlin` | 58 | All noise (Appwrite/builderprime harness) |
| `translate.goog berlin` | 1,478 | Pages about Berlin, not agent-shaped |
| `httpbin berlin` | 1,176 | Keyword matches page content, not carrier URLs — German-language pages (fielmann.ch, ditix.shop), no agent programs |
| `httpbun berlin` | 0 | |
| `httpbun standort` | 0 | |
| `httpbin adresse` | 129 | Noise (pages containing "adresse") |

## EU-lab infrastructure

| Pivot | Hits | Verdict |
|---|---|---|
| `aleph alpha` | 1,221 | News/docs pages only. No agent-shaped traffic. |
| `url.domain:api.aleph-alpha.com` | 0 | No agents calling Aleph Alpha's API via urlquery-visible URLs |
| `url.domain:pharia.ai` | 0 | |
| `pharia` | 9 | Pages mentioning Pharia (benchlm.ai, Croatian sites) — noise |
| `luminous` | 1,799 | Noise |
| `url.domain:api.mistral.ai` | 0 | No agents calling Mistral's API via urlquery-visible URLs |
| `black forest labs` | 877 | Pages about FLUX — noise |
| `url.domain:app.n8n.cloud` | 0 | Berlin automation platform; no agent traffic |
| `langdock` | 14 | Noise |

## New traces

None. This is a clean negative across ~40 pivots.

## Interpretation

The contrast with the Chinese fleet is itself the finding: the Amap operation left 2,000+ urlquery reports against a single target class with distinctive tag grammar. The German web ecosystem shows **zero** comparable systematic activity. Possible reasons:

1. No German-lab agent fleet is running urlquery-visible web collection at this scale.
2. German agents (if any) don't use urlquery as a browser/fetch tool.
3. German targets may be scraped via direct HTTP (not browser-mediated), leaving no urlquery trace.

Note the login-wall dynamic from the chinese-infra lane applies here too: German native services (Linkvertise, t1p.de) either require accounts or show no agent use — consistent with agents optimizing for no-login Western services regardless of origin.

## Follow-ups (other languages)

- **French**: Mistral API shows zero urlquery-visible agent use, but French targets (leboncoin.fr, qwant.com, pagesjaunes.fr) unexamined.
- **Russian**: 2GIS is the direct Amap analog (map/POI service) — unexamined. Yandex Maps likewise.
- German remains a clean zero; effort is better spent on French/Russian pivots.
