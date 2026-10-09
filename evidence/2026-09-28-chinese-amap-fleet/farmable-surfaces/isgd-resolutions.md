# is.gd short-link resolutions (2026-10-05)

Resolved via curl redirect-following. All five slugs from the June 20/21 burst.

## is.gd/3JlIp7 (`?uqscan=1781977000`)
→ `httpbin.io/response-headers` serving an auto-submitting HTML form:
- Form POSTs to `https://www.pingllo.com/api/proxy`
- Proxied target: `https://vizprod.aihw.gov.au/vizql/t/Public/w/AGE115_MentalhealthinAgedCare_19072024/v/F05-Age-specificcruderates/startSession/viewing` (Australian AIHW Tableau)
- Purpose: CORS-bypass — the form carries the Tableau session request through pingllo.com's proxy with forged Referer/headers

## is.gd/mf075827 (`?x=1782075870409744755`)
→ `httpbun.com/base64/<program>`: Tableau scraping program
- Loads `tableau-2.9.2.min.js` from vizprod.aihw.gov.au
- Opens `Public/views/PBSdashboardallATC1_ATC2medicines-Agegroup/PBSdashboard`
- Extracts workbook filter names/types/values, exfils via image beacon `httpbun.com/status/204?x1782075813`
- Image-beacon title exfil pattern (`document.title=x,(new Image).src=...`)

## is.gd/sum074114 (`?sum1782074114`)
→ `httpbun.com/base64/<program>`: same shape, different PBS view, beacon `?sum1782074114`

## is.gd/kf073634 (`?x=1782071909.675917`)
→ `httpbin.org/base64/<program>`: auto-submitting form to **`https://urlcap.com/account/api-keys`**
- Creates an API key named `scankey` (`action=create`, `name=scankey`)
- The operator minting API keys on urlcap.com (a URL-scanning service) — infrastructure provisioning, not just scanning

## is.gd/AGE115EXTRACT1 (`?mark=AGE115EX1781972899`)
→ `httpbin.org/base64/<program>`: Tableau embed program for `AGE115_MentalhealthinAgedCare_19072024`, applies PRAC/Mood-disorders filters, extracts summary data, beacon exfil. The `mark=` tag grammar matches the IDPH Iowa family.

## Assessment
The June 2026 task family is now fully characterized: AIHW (Australian health) Tableau scraping via CORS-bypass proxies (pingllo.com), httpbun-staged Tableau JS programs, image-beacon exfil keyed to `?x<epoch>` / `?sum<epoch>` / `?mark=` tags — and operational API-key provisioning on urlcap.com. Same operator, same grammar as Amap/IDPH.

## Follow-up: pingllo.com
- No urlquery hits; no web footprint as a known public CORS proxy
- `www.pingllo.com` resolves to 198.18.241.43 (198.18.0.0/15 = RFC 2544 benchmarking space — unusual, possibly anycast/DNS oddity)
- `/api/proxy` accepts POST, returns 200
- Assessment: obscure/small proxy service, possibly operator-run or a niche public utility. Either way it's a NEW infrastructure data point in the operator's June kit, alongside the five confirmed layers.
