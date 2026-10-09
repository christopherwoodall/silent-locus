# HTMX re-read results — all 22 queued zero claims

**Worker:** htmx-fix patch-and-rerun · **Run:** 2026-10-06 ~19:45–20:05 CDT (2026-10-07 00:45–01:05 UTC)
**Method:** keyless `GET https://urlquery.net/api/htmx/search/?q=<q>&limit=24&offset=0` via curl,
headers `HX-Request: true` + `HX-Current-URL: https://urlquery.net/search?q=<q>` (+UA/Accept) —
the skill's `uq_htmx_curl.py` pattern, with HTTP code captured via `-w` so a 204 regression
is distinguishable from a genuine zero. **6s pacing**, one retry w/ 20s backoff on failure.
Per-query raw JSON + provenance in `../../raw/reread/q<nn>_<slug>.json`; raw HTML for
resurrected hits in `../../raw/reread/html/`. Counts are page-capped at 24 (limit=24).

## Tally

| queue | queries | ZERO STANDS | RESURRECTED | GAP |
|---|---|---|---|---|
| #1 russian-agent-hunter (`тест`, `проверка`) | 2 | 0 | **2** | 0 |
| #2 `url.domain:gov.ru` | 1 | 1 | 0 | 0 |
| #3 13× `url.domain:gov.{sa,ae,eg,qa,kw,bh,om,jo,iq,lb,ma,tn,dz}` | 13 | 13 | 0 | 0 |
| #4 `url.domain:gov.vn/in/eg`, `url.domain:go.id` | 4 | 4 | 0 | 0 |
| #5 de-linguist q1/q3/q4/q5/q8 | 5 | 5 | 0 | 0 |
| #6 hindi/japanese/korean 22 zeros | 22 | 20 | **2** | 0 |
| #7 polish/turkish/arabic 35 zeros | 35 | 35 | 0 | 0 |
| #8 vietnamese/indonesian/thai 29 zeros | 29 | 28 | **1** | 0 |
| #9 behavior-hunt summary | — | (covered by #6–#8 re-reads) | — | — |
| #10 `url.domain:scaleway.com` | 1 | 0 | **1** | 0 |
| #11 lighthouse (`aisstream`, `marinetraffic`, `mmsi`) | 3 | 2 | **1** | 0 |
| #12 ham-radio 5× `url.domain:` | 5 | 4 | **1** | 0 |
| #13 birdwatcher 3× `url.domain:` | 3 | 3 | 0 | 0 |
| #14 `url.domain:timeapi.io` | 1 | 1 | 0 | 0 |
| #15 `tronzap` | 1 | 1 | 0 | 0 |
| #16 8 ZeroSSL-ish tunnel names | 8 | 8 | 0 | 0 |
| #17 `gov.th` | 1 | 1 | 0 | 0 |
| #18 `url.domain:warnung.bund.de` | 1 | 1 | 0 | 0 |
| #19 `star-vegas.it` | 1 | 0 | **1** | 0 |
| #20 `url.domain:pages.dev uqscan` | 1 | 1 | 0 | 0 |
| #21 `gov.il` (keyword; was IncompleteRead) | 1 | 0 | **1** | 0 |
| #22 5 fileshare domains (were urllib tracebacks) | 5 | 0 | **5** | 0 |
| **TOTAL** | **143** | **128** | **15** | **0** |

**128 confirmed zeros · 15 resurrected · 0 collection gaps.** No 204s were observed on any
request with the fixed header set.

Assumption note (#16): the queue lists "8 ZeroSSL tunnel names (`a7bfa19dd56391`,
`ca990e9a89525d`, …)". Re-ran the 7 verified ZeroSSL names from
`full-sweep/raw/lead-zerossl-followup.md` plus the 8th adjacent programmatic-shape name
`93ca25e80716ce` (multi-CA, same window). All 8 → 200 + 0 rows. The INDEPENDENT verdict stands.

## Resurrected hits — detail

### Load-bearing resurrections (can move verdicts)

1. **`тест` → 23 reports** / **`проверка` → 20 reports** (#1, load-bearing YES).
   Old verdict: filed as `HTTP 204 / {"reports": []}` — Lane 1 of russian-agent-hunter's
   "no Russian agent find". New: the endpoint returns real rows. Content is generic
   Russian-language noise (oledtest.org, konstruktortestov.ru, minecraft-club.ru mods,
   meet-google-plus.com lookalikes) — NOT agent-shaped. Net effect: the lane's Lane-1
   *evidence* was a 204 artifact, but the *conclusion* (no Russian agent fleet) is not
   contradicted by the hit content. Recommend the lane re-grade Lane 1 as
   "searched, noise only" rather than "HTTP 204".
   Raw: `raw/reread/q01_______.json`, `raw/reread/q01__________.json` (+html).

2. **`httpbin.org/base64` → 2 reports** (#6, load-bearing YES).
   Overturns the lane's "known tool limitation" claim ("ltzh-family httpbin programs do not
   surface through this endpoint — 0 via htmx"). Both hits are FRESH — scanned
   2026-10-07 00:04 and 00:14 UTC (hours before this re-read):
   - `ddb41ac5` — `httpbin.org/base64/PHNjcmlwdD5xPSdodHRwczovL3VrLmludGVycGFyY3VsLmNvbS9xdW90ZS9zZWxlY3Qtc2VydmljZT9wP` → decodes to `<script>q={https://uk.interparcel.com/quote/select-servi…`
   - `06fc099d` — `httpbin.org/base64/PGh0bWw%2BPGhlYWQ%2BPHRpdGxlPlJlbGF5VGVzdDwvdGl0bGU%2BPC9oZWFkPjxib2R5PjxzY3JpcHQ…` → decodes to `<html><head><title>RelayTest</title>…<script…`
   httpbin base64 *program* tradecraft with a "RelayTest" title hours old is worth a
   look — not Amap-fleet-shaped, but adjacent to the June-incident tradecraft family.
   Raw: `raw/reread/q06_httpbin.org_base64.json` (+html).

3. **`mmsi` → 23 reports (page-capped)** (#11, load-bearing YES).
   Lighthouse-keeper's "no agent-shaped maritime activity found" rested partly on this
   zero. Hits are keyword matches (page content), mixed: `cruisemapper.com`
   (maritime-relevant), `meansindustries.com`, `flrdrop.vip` ×2 (2026-08-26, odd),
   `geometrylitepc.net`. Needs content triage before the lane verdict is re-stated —
   the honest-zero claim for `mmsi` is dead.
   Raw: `raw/reread/q11_mmsi.json` (+html).

4. **`zenrin` → 5 reports** (#6, load-bearing YES).
   All 2023–2024 phishing `.top` domains (`arena.choreen.top`, `mnium.choreen.top`,
   `esb.forable.top`, `velox.eattion.top`, `site.enkido.org`) — matches the lane's old
   "phishing .top domains only" note. Zero's *content* was right; now verified real.
   No agent shape.
   Raw: `raw/reread/q06_zenrin.json` (+html).

5. **`research kompas` → 3 reports** (#8, load-bearing YES).
   `kompas.ge` pharmacy page (noise, as the lane already noted), `biztoc.com`,
   `kompas.ai` settings page. Noise — lane conclusion unaffected.
   Raw: `raw/reread/q08_research_kompas.json` (+html).

### Partial / non-load-bearing resurrections

6. **`url.domain:scaleway.com` → 3 reports** (#10, partial): `status.scaleway.com`
   (2026-09-03), `scaleway.com` ×2 (2026-05-08, 2025-03-06). Ordinary submissions; the
   OVH/Scaleway section's "no French agent fleet" is unaffected.
7. **`url.domain:satnogs.org` → 1 report** (#12, partial): `db.satnogs.org`,
   scanned 2026-10-06. Ordinary.
8. **`star-vegas.it` → 1 report** (#19, no): `star-vegas.it/`, 2026-09-22.
   Lead stays "flagged, not claimed".
9. **`gov.il` (keyword) → 24 reports, page-capped** (#21, no — first real search;
   old file was a 0-byte IncompleteRead error): page-content noise
   (everythingarboriculture.com, artvoice.com, homecadet.com…), not gov.il submissions.
   Tradecraft note only, as before.
10–14. **Fileshare-farmer five — all first real searches** (#22, partial; old "zeros"
   were urllib tracebacks, nothing was ever searched):
   - `gofile.io` → 24 (page-capped): `gofile.io/d/zJ6m4kpw` (2026-10-04),
     `api.gofile.io/contents/…` API-shaped submissions.
   - `catbox.moe` → 24 (page-capped): `litter.catbox.moe/25us02.html?v={1,2,3}`
     cluster (2026-10-06 12:17), `litter.catbox.moe/9y3neg.html`.
   - `filebin.net` → 23: `filebin.net/8z95uz7i6tc008fb/shellcode.enc` (2026-08-01),
     `…/dled0m8xu0f4l4j5/placement.core` (2026-07-20) — malware-adjacent filenames.
   - `temp.sh` → 24 (page-capped): `temp.sh/IumxA/bridge.html`,
     `temp.sh/XuExV/test.txt`, `temp.sh/julnh/gas.mp4` (2026-09-01 cluster).
   - `mirrorace.com` → 3: `mirrorace.org` (2026-02-25), two 2023 `mirrorace.com/m/…` links.
   The lane's "clean honest negatives across five major share domains" was never earned —
   these are first-look results and need triage (the `shellcode.enc` / `placement.core`
   filenames especially).

### Confirmed zeros that matter

- **#15 `tronzap` → 200 + 0.** The "urlscan-visible only" characterization of the
  TronZap campaign holds.
- **#16 all 8 tunnel names → 200 + 0.** The ZeroSSL INDEPENDENT verdict holds
  (zero urlquery presence, zero overlap with the 78 fleet names).
- **#5 de-linguist q1/q3/q4/q5/q8 → 200 + 0.** The EUROSWARM honest negatives stand.
- **#7 all 35 PL/TR/AR zeros → 200 + 0.** The "no PL/TR/AR fleet" verdict is now
  verified-real.
- **#17 `gov.th` → 200 + 0.** The Thailand "clean live negative" is verified-real.

## Bottom line

The 204 bug invalidated 15 of 143 queued zero claims (10.5%) — heavily concentrated in
items that were *never actually searched* (#21/#22 error-as-zero misfiles: 6 of the 15)
and in two genuine 204-artifact zeros (#1's Russian test words, #11's `mmsi`).
Of the 15 resurrections, 3 deserve follow-up on their content: `mmsi` (lighthouse lane,
load-bearing), `httpbin.org/base64` (two fresh RelayTest/interparcel program reports),
and the fileshare-farmer five (first-look, malware-adjacent filenames). The remaining
12 are noise that leaves the original lane conclusions intact — but the lanes should
re-grade those items from "204/error" to "searched, noise only".
