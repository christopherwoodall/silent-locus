# LINKS.md — Chinese agent fleet hunt (2026-10-05)

Running link log. Format: URL, one-line description, phase/lane that found it.
Updated as the hunt progresses.

## urlquery reports
- (n-gram pivots, Phase 2: `sub_poi_navi` → 24 fleet programs on httpbin.org/httpbun.com/amap.com; `clk_ratio` → 6; `bailuzhou` → 8; program-title grammar `<place>-<descriptor>-<epoch>` — see PATTERN.md)
- `https://urlquery.net/report/aa75ca67` — first Amap scan (28 Sep 20:57 UTC, Summer Palace `B000A7O1CU`) (seed: swarmcha.se report)
- `https://urlquery.net/report/3cf2d5ed` — first Amap scan batch (28 Sep) (seed: swarmcha.se report)
- `https://urlquery.net/report/9e70c844` — first Amap scan batch (28 Sep) (seed: swarmcha.se report)
- `https://urlquery.net/report/957ce4ae` — first "claude" label (30 Sep 23:36 UTC) (seed: swarmcha.se report)
- `https://urlquery.net/report/97f0619b` — Ta'er Temple inbox timing evidence (seed: swarmcha.se report)
- `https://urlquery.net/report/563ba9f6` — Chengdu Zoo readout (North Gate 71%) (seed: swarmcha.se report)
- `https://urlquery.net/report/f2a45ccb` — second readout via r.jina.ai → httpbun (seed: swarmcha.se report)
- `https://urlquery.net/report/f79e94fb` — LiveCodes "Amap Baxia JSONP" anti-bot program (seed: swarmcha.se report)
- `https://urlquery.net/report/6694c078` — microlink Puppeteer intercepting getPoiInfo (seed: swarmcha.se report)
- `https://urlquery.net/report/7517916e` — httpbingo redirect to Amap place page (seed: swarmcha.se report)

## webhook inboxes
- (pending Phase 2 mining — webhook.site addresses from collected programs)

## paste sites
- `https://dpaste.com/H49755QXK` — fleet paste, used by the fleet itself (seed: swarmcha.se report)
- `https://paste.page/amap-wangshan-6s3kvk5i` — fleet paste (seed: swarmcha.se report)
- `https://paste.c-net.org/EventRefined` — fleet paste (seed: swarmcha.se report)

## relay URLs
- `https://r.jina.ai/` — text-extraction relay used as fleet route (seed: swarmcha.se report)
- `https://api.microlink.io/` — Puppeteer relay for anti-bot interception (seed: swarmcha.se report)
- `https://href.li/` — redirector to jina-fetched programs (seed: swarmcha.se report)
- `https://translate.goog/` — relay class cited in report taxonomy (seed: swarmcha.se report)
- `https://allorigins.win/` — relay class cited in report taxonomy (seed: swarmcha.se report)
- `https://fanyi.baidu.com/transpage?query=https%3A%2F%2Famap-pc-ssr.amap.com%2Fssr%2Fapi%2FgetPoiInfo%3Fid%3DB021307ZAY&from=zh&to=en&source=url&render=1` — Baidu Translate as fetch proxy, NEW relay class (Phase 2 pivot: `968009e0`, `a255dfb9`, both 2026-10-04)

## target endpoints
- `https://amap-pc-ssr.amap.com/ssr/place/<POI_ID>` — Amap place SSR pages (seed: swarmcha.se report)
- `https://www.amap.com/ssr/api/getPoiInfo?id=<POI_ID>` — Amap POI info API incl. sub_poi_navi/clk_ratio (seed: swarmcha.se report)

## external references
- `https://swarmcha.se/posts/chinese-agent-fleet` — preliminary fleet report, Rowan Howard-Jones (seed)
- `https://swarmchase.alecto.dev` — Misaligned Agent Activity Survey (data source cited by report)
- `https://transluce.org` — "Early rogue AI agent activity" disclosure (report source)

## n-gram pivot hits (Phase 2)
- `sub_poi_navi` (24 urlquery hits, zero web hits — perfect fleet fingerprint): 21× httpbin.org programs, 2× amap.com, 1× httpbun.com (Phase 2 pivot)
- `clk_ratio` (6 hits, all httpbin.org fleet programs) (Phase 2 pivot)
- `bailuzhou` (8 hits: 7 httpbun.com program titles + 1 amap.com) — place-anchored program titles (Phase 2 pivot)
- Program title grammar `<place>-<descriptor>-<epoch>`: `dalian-jsapi-1791135514199`, `bailuzhou-pulseiframe-1791131179`, `Amap popup boot 1791130764` (Phase 2 program mining)

## predicted surfaces (Phase 2 — technique-based prediction)
- beeceptor.com / pipedream.net / requestcatcher.com: 0 hits in-window — fleet stays on webhook.site (clean zeros)
- codepen.io / jsfiddle.net / observablehq.com: 0 hits in-window — fleet stays on LiveCodes + httpbun (clean zeros)
- pastebin.com ×2 in-window (`8494423a`, `5c1acef1`): fetched, zero fleet markers — not fleet-related
- `fanyi.baidu.com/transpage` — HIT: Baidu Translate as fetch proxy (see relay URLs)

## ltzh program family (Phase 2 follow-up — Zhipu-hunt lead)
- `https://urlquery.net/report/1a7e1f20` — `ltzh-jina-post-inject-20261004a`: jina POST API + injectPageScript + image-beacon exfil (2026-10-04)
- `https://urlquery.net/report/4540d7da` — `ltzh-jina-json-cache7d-20261004b` (2026-10-04)
- `https://urlquery.net/report/00aa3bf5` — `ltzh-jina-json-cache7d-20261004a` (2026-10-04)
- `https://urlquery.net/report/c5cd6bdb` — `ltzh-iframe-ssr-20261004a` (2026-10-04)
- `https://urlquery.net/report/4a37563c` — `ltzh-iframe-ssr-big-20261004a` (2026-10-04)
- `https://urlquery.net/report/1846108e` — `ltzh-iframe-www-20261004a` (2026-10-04)
