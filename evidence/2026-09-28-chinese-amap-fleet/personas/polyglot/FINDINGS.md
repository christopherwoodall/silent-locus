# Polyglot — FINDINGS
## Agent traces in non-English, non-Chinese languages

**Persona brief:** hunt AGENT traces carrying non-English, non-Chinese language — Hindi, Portuguese, Arabic, Bahasa Indonesia, Russian, Spanish, Turkish, Vietnamese. Agents and swarms only — no human/operator identity work.
**Run:** resumed 2026-10-05 ~00:13 CDT after VM restart. Prior run (2026-10-04 ~23:37–23:50 CDT) covered Russian/Ukrainian/Kazakh via urlscan.io + browser.search (egress to urlquery was down then); full notes in `raw/russian-cyrillic.md`.
**Corpus status:** zero native-language markers in our 2,141 fleet records — no Devanagari, Arabic, or Cyrillic anywhere. So the hunt ran on **live surfaces** (urlquery htmx), not the corpus.

## Method
- urlquery keyless htmx (`~/workspace/skills/urlquery/bin/uq_htmx.py search`), ≤1 request per 5–10s.
- Per language: (a) probe-grammar terms an agent would emit (`test/scan/search/check` in-language), (b) gov-domain sweeps on the Global South targets (`url.domain:go.id|gov.br|gov.vn|gov.in|gov.eg`).
- **Egress was severely flaky this session** (proxy-tunnel timeouts, `IncompleteRead` mid-chunk, `RemoteDisconnected`). Of 17 htmx queries, 11 returned valid results, 6 failed at the network level (retried once; failures are infrastructure, not verdicts — see "Could not check").

## Confirmed: no agent-shaped non-English activity found

### gov.br/sheila — candidate (UNCONFIRMED, needs metadata)
`url.domain:gov.br` returned 6 reports. Five are bare `gov.br` homepage fetches (2024–2026, noise). One stands out:

- **2026-06-30 13:10 UTC — `gov.br/sheila`** — report `3c71bb78-3325-46e7-97a2-f36b54b015aa`
- A single bare given-name path on Brazil's federal portal domain is probe-label-shaped (compare the fleet's ASCII name-labels like `claude20261004bailuzhou`). But: one-off, no burst siblings, no nonce/tag grammar, and the report page is a JS SPA — submitter-side metadata (tags, submitter UA) could not be extracted keyless. **Graded candidate, not confirmed.** Do not cite as agent activity without the metadata check.

### taram.blob.core.windows.net/taram/index.html — curiosity (UNCONFIRMED)
Query `taram` (Turkish: "scan") returned mostly noise, but:
- **2026-08-19 15:05 UTC — `taram.blob.core.windows.net/taram/index.html`** — report `239e7836-aa8b-4537-b574-84f5f1772bb7`
- An Azure blob static site literally named "taram" ("scan"). Could be a Turkish speaker's test drop, or coincidence. Report metadata not extractable keyless (JS SPA). **Watch-list only.**

### Honest zeros / noise
- **`url.domain:gov.vn`, `url.domain:gov.in`, `url.domain:gov.eg` — zero live results.** (Global South Scout found these targets in frozen corpora, not live — consistent.)
- **`url.domain:go.id` — zero results, BUT this is a search-coverage gap, not an absence:** the 5 frozen-corpus Indonesia records (`1df03d5a`, `faa48376`, `a9c7e089`, `09195203`, `1e16f79e`) resolve live via curl (HTTP 200, real page sizes), yet neither `url.domain:go.id` nor keyword `pa-gresik` returns them. **The htmx search index does not surface these known records — htmx zero-results are weak negatives.** (Related: urlscan keyless search has the same blind spot for query-param values.)
- `uji` (Bahasa: test) — 10 hits, all SEO/affiliate spam domains (`lucraze.com`, `wearthetoe.shop`, `kitchenwarehouse.com.au`…) — substring noise, no agent shape.
- `kiểm` (Vietnamese) — 10 hits: X/Twitter video hosts (`video.twita.space`, `video2.twimg.bike`), t.co links, Vietnamese spam (`tet.pro.vn`, `cattuongphongthuy.com`) — noise.
- `prueba` (Spanish: test) — 10 hits: SEO spam + throwaway test subdomains (`tablero-prueba-ufil.netlify.app`, `www.es-rodillos-prueba-apuntes.click`) — noise.
- `परीक्षण` (Hindi: test) — 1 hit: `lexstart.in/tag/medikala-pariksana/` (medical-exam SEO tag page) — noise.
- Russian/Cyrillic lane (prior run): 9 urlscan term queries (RU/UK/KZ + Latin translits) all zero; webhook.site + Cyrillic pairing none; `rosstat.gov.ru` ×4 (Oct 2–3, bare homepages — inconclusive monitoring-like polling); `mil.gov.ua` streaming-subdomain cluster (2-request probes — inconclusive); gist/paste searches noise. Full detail in `raw/russian-cyrillic.md`. **Bottom line: no agent-shaped RU/UK/KZ activity.**

### Could not check (network failures, retry on calm window)
`pindai` (Bahasa: scan), `pesquisa` + `verificar` (Portuguese), `اختبار` (Arabic), `go.id` keyword, `kkp.go.id`. Also: report-page submitter metadata for `gov.br/sheila` and the `taram` blob (JS SPA; the undocumented endpoints below may help).

## New tooling found (document for reuse)
urlquery report pages expose keyless htmx data endpoints (need `HX-Request: true` header):
- `/api/htmx/report/{id}/filter/http` — full HTTP transaction log
- `/api/htmx/report/{id}/filter/javascript/scripts`
- `/api/htmx/report/{id}/related/{asn,domain,ip,screenshot,similar}`
Note: base `/api/htmx/report/{id}` 404s; overview metadata is not in the static HTML.

## Bottom line
- **No confirmed agent-shaped non-English, non-Chinese activity on urlquery this session.** Two watch-list candidates (`gov.br/sheila`, `taram` blob site) need submitter-metadata checks.
- The Global South language angle (Bahasa/Portuguese/Vietnamese/Hindi/Arabic probe grammar) produced only SEO-spam noise — consistent with the fleet's established ASCII-only convention (Linguist-Chinese: zero CJK in 1,243 tags). If these agents operate in the Global South, they do it in ASCII/English, not in the local language.
- **Methodological warning:** htmx search misses known-live records — treat every htmx zero as provisional.

## Pending
1. Retry failed queries on a calm window: `pindai`, `pesquisa`, `verificar`, `اختبار`, `go.id` keyword.
2. Extract submitter metadata for `3c71bb78` (gov.br/sheila) and `239e7836` (taram blob) — try the `/related/*` endpoints or an authenticated session.
3. urlscan API-key pass over `gov.br/sheila` siblings and `taram.blob.core.windows.net` related scans.

---
## APPENDIX — All observed URLs

### urlquery htmx queries (raw JSON in raw/htmx/)
- Query `url.domain:gov.br`: gov.br (2026-09-24, 2026-07-23, 2024-04-23, 2024-08-08), gov.br/sheila (2026-06-30)
- Query `url.domain:go.id`: zero results (search-coverage gap — known records live but unindexed)
- Queries `url.domain:gov.vn`, `url.domain:gov.in`, `url.domain:gov.eg`: zero results

### Report URLs (urlquery.net/report/…)
- https://urlquery.net/report/21383bf2-adb6-4ed1-b7c5-dcb4c3ba3bc3 (gov.br)
- https://urlquery.net/report/83955b1e-0279-43f2-a133-95de56494a81 (gov.br)
- https://urlquery.net/report/3c71bb78-3325-46e7-97a2-f36b54b015aa (gov.br/sheila — CANDIDATE)
- https://urlquery.net/report/16ec018f-ce43-4dcb-a1b2-1301e8574f14 (gov.br/)
- https://urlquery.net/report/c0c94d4d-3221-4de8-873d-d8b533187c7e (gov.br)
- https://urlquery.net/report/a28598f7-9fc7-4d94-9375-94e7abb48a61 (gov.br)
- https://urlquery.net/report/239e7836-aa8b-4537-b574-84f5f1772bb7 (taram.blob.core.windows.net/taram/index.html — WATCH)
- https://urlquery.net/report/7ffb83d2-33a1-46ee-b965-f3b1bf23abfe (lexstart.in/tag/medikala-pariksana/)
- https://urlquery.net/report/d6ee6ce0-76f4-48d6-9e19-271552a70762 (shanmao-douyin-live.com/)
- https://urlquery.net/report/b48c5d16-deab-4ced-b4bf-7f61342496e4 (bellottoutou.com)
- https://urlquery.net/report/69c30d86-c3d4-46f3-82f7-11b5d8f6d4cd (fa4.net/)
- https://urlquery.net/report/1831c7e2-c7c4-4e9f-a591-370d66c1deaa (lucraze.com)
- https://urlquery.net/report/946daf72-c9dc-43b2-9b60-8a6039d52a0e (euroking.buzz)
- https://urlquery.net/report/1e2f0769-9e45-42fb-ac82-e0aa945b7868 (workink.biz)
- https://urlquery.net/report/6bdd42e1-7fa6-4cb5-97af-898229eff2c3 (cartuneparts.com/)
- https://urlquery.net/report/c0985d28-3253-4c0e-a514-fa009e7659e6 (creativeshoppers.com)
- https://urlquery.net/report/6cbdfc0e-85d9-4b91-8680-fdd85ace1017 (kitchenwarehouse.com.au)
- https://urlquery.net/report/93492f5f-8b1d-4414-82b0-4ddf35c4ca05 (wearthetoe.shop)
- https://urlquery.net/report/d8bf03c3-7fce-43da-9918-6717a54db099 (tet.pro.vn)
- https://urlquery.net/report/10b3b4f9-8ebf-4418-9997-a0a2f724af1c (anchoi.cc/)
- https://urlquery.net/report/cbf4f914-3d3c-4f97-8b18-701bd19f78c7 (t.co/agIEKsZ3o0)
- https://urlquery.net/report/0f1a1360-7281-4fe0-80d3-f91a997ae11c (cattuongphongthuy.com)
- https://urlquery.net/report/42883dda-77a5-4b5c-a715-8c7c8267e592 (t.co/XPNzdIVLoA)
- https://urlquery.net/report/4beef755-065d-434c-9e8d-97a4c2f4ff4c (t.co/p6WKmpou31)
- https://urlquery.net/report/c93f5f40-ea23-4492-bc99-30a9b488e76b (mediasx.twitb.ink/)
- https://urlquery.net/report/903458f1-c825-4de4-9a46-69d656cb2d9f (video.twita.space/SwABEgnmj.mp4)
- https://urlquery.net/report/8d405b50-5727-456b-b0c0-d59d8dce728f (t.co/MGuW6pcmwr)
- https://urlquery.net/report/a99bbdff-1bc6-43ba-aa2d-6d92116af27c (video2.twimg.bike/C0CG0zMP1.mp4)
- https://urlquery.net/report/45747031-e619-4886-8ed6-6eacbf9c8d3d (calirenacio.com)
- https://urlquery.net/report/a376f3c4-0b71-467d-a4c9-4dd5e89caf02 (capitalquintanaroo.com.mx)
- https://urlquery.net/report/130685bb-c122-459b-82ea-7a36fa0f923f (coenfeba.com)
- https://urlquery.net/report/99bcb82b-b07f-40ba-aeb7-6c51df136a39 (bios.pe)
- https://urlquery.net/report/7030ca00-d6f7-4c62-9061-04ef9da1ef4e (foto-r3.com)
- https://urlquery.net/report/85342799-d146-4d38-90d9-6ec72dfa0741 (repagas.com)
- https://urlquery.net/report/8c07a7da-f88e-477c-9a7a-01149d7426a8 (solva-89007722-30317088.jimdosite.com/)
- https://urlquery.net/report/4b551bf3-a479-4003-9380-8a1eaf352516 (www.es-rodillos-prueba-apuntes.click/)
- https://urlquery.net/report/530b2b71-7f10-4790-b75e-e8de9a31123c (slome.es/)
- https://urlquery.net/report/99b6a249-b8a0-472e-96e7-cecc323cf9d4 (tablero-prueba-ufil.netlify.app/)
- https://urlquery.net/report/a05d466c-eb88-4f14-acc7-5cba8b3ee393 (cricbtqk.world/)
- https://urlquery.net/report/c4e1d079-07e0-4c01-a0f2-16f023651092 (hollywoodcasino.com)
- https://urlquery.net/report/96e3e789-06c8-41d0-83c9-642b525acb5e (www.vextrasoft.com/downloads/vextr670demo.exe)
- https://urlquery.net/report/041cfa3d-9794-4257-85ef-ddeb1a0b0745 (www.vextrasoft.com/downloads/vextr650demo.exe)
- https://urlquery.net/report/0c950ff1-057f-44d2-b69d-fb25e5f7408b (www.vextrasoft.com/downloads/vextr630demo.exe)
- https://urlquery.net/report/17f65483-485f-4a02-aa78-3a41d216554a (managerlinking.ionanalytics.com)
- https://urlquery.net/report/94f3dc04-fc6c-41af-9001-d150a6921fa0 (mangareader.cc/)
- https://urlquery.net/report/1df03d5a-ba13-474d-8036-26fe31526ee7 (pa-gresik.go.id — verified live 200 via curl, unindexed by htmx search)
- https://urlquery.net/report/dd4fa017-96a3-4d7a-9753-409a525b99ba (anatel.gov.br — verified live 200 via curl)

### Undocumented urlquery htmx endpoints (keyless, HX-Request header)
/api/htmx/report/{id}/filter/http · /api/htmx/report/{id}/filter/javascript/scripts · /api/htmx/report/{id}/related/{asn,domain,ip,screenshot,similar}
