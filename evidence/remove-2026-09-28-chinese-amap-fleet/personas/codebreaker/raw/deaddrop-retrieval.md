# Dead-Drop Retrieval — Codebreaker Expansion
**Probed:** 2026-10-05 ~05:21–05:33 UTC (00:21–00:33 CDT) via `GET https://webhook.site/token/<uuid>` and `/token/<uuid>/requests` — no auth. All timestamps below are webhook.site server time (UTC). Raw JSON in this directory.

## Verdict table

| UUID | Family | Status | Requests | Newest request | Notable |
|---|---|---|---|---|---|
| `6ddc559e-5c08-4915-a5b2-f4addc42368a` | fleet | **ALIVE** | 5 | 2026-10-04 15:11:25 | Default response = XHR-intercept exploit page (`taersitokennav1791126060505`). Requests are page loads only — no beacons (this page exfils via `location.replace` nav, not the inbox) |
| `0a947514-5b43-4030-9f9f-b193dd2d519b` | fleet | **ALIVE** | 1 | 2026-10-04 17:15:01 | No default content configured. Single page-load hit. Owner fingerprint differs from other fleet inboxes (see below) |
| `a7753b69-2ceb-4221-adfa-80f69d57480c` | fleet (codebreaker fingerprint) | **ALIVE** | 33 | 2026-10-04 15:43:02 | **HIGH VALUE** — default response = Umeng token-theft beacon page (`cdzoo1791126724959`). 5 stolen `bx-ua` signed Amap `getPoiInfo` URLs exfiltrated via `sendBeacon` POSTs; test page delivered via `httpbun.com/base64/` echo (referer header) |
| `6051dd2b-86dc-427d-8083-071a687af4f8` | legacy | **DEAD** | — | — | HTTP 404, `Token "..." not found` — "The URL was deleted, or expired automatically" |
| `00f36f21-d00e-48b3-9456-8bf532e8c863` | legacy | **DEAD** | — | — | HTTP 404, same expiry page |
| `441b7745-1087-463e-b539-984a2ee3ea65` | legacy | **DEAD** | — | — | HTTP 404, same expiry page |
| `c1bf6b38-d6ea-4446-b17e-5f6c7a1cb357` | legacy | **DEAD** | — | — | HTTP 404, same expiry page |
| `1eafadc3-9bb7-42d1-a9f0-0ced18cb6d56` | legacy | **DEAD** | — | — | HTTP 404, same expiry page |
| `35f6980c-7dc6-4af4-b646-56ca0070a200` | legacy | **DEAD** | — | — | HTTP 404, same expiry page |
| `cbcb10de-7f66-4e82-b7ac-5b34ccb04164` | legacy (jina-cache family) | **ALIVE** | 13 | 2026-10-04 17:11:19 | **Unexpectedly alive** — metadata shows `created_at` 2026-10-04 16:56:55 (fresh inbox, same UUID re-registered). Default response = `ok`. 13 requests = full jina-cache test run: `r.jina.ai` fetches of `amap-pc-ssr.amap.com/ssr/place/B001C8MXRO` (Chengdu Zoo) beaconed back as `kind=start/headers0/body0-0/headers1/body1-0/done`; test page itself delivered via `httpbun.com/base64/` (decoded in `cbcb10de-jinacache-page.html`) |
| `e691f66e-73c7-44ff-9d90-a79521173811` | view token | **ALIVE** | 1 | 2026-10-05 03:05:00 | `#!/view/<uuid>` IS the inbox UUID — no special API needed. Created 2026-10-04 07:19:52 (earliest of the fleet). No default content; single bare GET. Owner UA/IP = Firefox 134 / 195.64.118.152 (Blix, Norway — same as operator test egress). **Watch:** a bare `Mozilla/5.0` GET from IPv6 `2a04:4e41:0:3009::aaab:3009` hit it at 03:05 UTC, ~2h before this probe — unknown third party checking the inbox |

All inboxes are free-tier (7-day expiry; fleet expires 2026-10-11).

## Decoded payloads

### a7753b69 — Umeng (bx-ua) token-theft beacon page
Default response (`default-content-a7753b69.txt`, 1441 bytes):
- `sendBeacon('/a7753b69…?kind='+k, …)` exfil loop; hooks `umx.wu` / `__fycb` (Umeng `wu.json` callbacks) to capture token `T`
- Loads `sg-wum.alibaba.com/w/wu.json?bx-ua=fast-load`, Alibaba `awsc.js` + `baxia-entry/baxiaCommon.js`; overrides `__baxia__.getFYModule.getUidToken=()=>T`
- XHR hook: any `getPoiInfo` URL containing `bx-ua=` → POSTed back as `kind=token`, loaded in hidden 2×2 iframe
- Probes `amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B001C8MXRO&probe=1791126724959x{q}` at 0.8/2.5/5/9s; `kind=alive` beacon at 14s

**Stolen tokens retrieved (5 unique `bx-ua` values, full strings in `a7753b69-bxua-tokens.txt`):**

| Time (UTC) | Sender IP | Amap `p=` param | `bx-ua` prefix |
|---|---|---|---|
| 15:16:52 | 195.64.118.152 | 1791127001690 | `231!lLp37+mUen3+…` (1412 chars) |
| 15:19:24 | 195.64.118.152 | 1791127124529x1791127163749 | `231!8H337+mUpap+…` (1412) |
| 15:19:28 | 195.64.118.152 | 1791127124529x1791127168201 | `231!M7/3J+mUc/…` (1468) |
| 15:19:31 | 195.64.118.152 | 1791127124529x1791127168201 | `231!y2z3JAmUzu/…` (1472) |
| 15:43:02 | 85.203.15.253 | 1791127001690 | `231!gU0394mUwgR+…` (1528) |

Supporting beacons: `k=s` → `1` (start ×7), `k=l` → `0` (token length at load ×7), `k=r` → `419| ` (Amap 419 token-reject ×2, operator IP — their replayed tokens were rejected).
**Delivery mechanism:** beacon `Referer` header shows the running page was `http://httpbun.com/base64/<base64>` — the operator base64-wraps the test page through httpbun's echo endpoint (decoded running page saved as `a7753b69-running-page-from-referer.html`; 959 bytes; an earlier iteration than the current default response — uses `?k=` scheme, `?k=t` exfil, 1500ms probe delay).

### 6ddc559e — Baxia nav-replay page (`taersitokennav1791126060505`)
Default response (`default-content-6ddc559e.txt`, 1383 bytes): hooks `XHR.setRequestHeader`; when header `bx-v` is set on a URL containing the marker, retitles to `…-NAV` and `location.replace(u)` — i.e. waits for Baxia to sign a `getPoiInfo` request with the stolen token, then navigates to replay it. Loads `awsc.js`, `baxia/1.1.7/baxiaCommon.js`, `baxiaToken.js`, `et_f.js`; inits Baxia `appendTo:header, needUmidToken, paramsType:[uab,umid,et]`; probes `getPoiInfo?id=B03CB06N7F&navprobe=taersitokennav1791126060505` after 4s. 5 requests = page loads only (no inbox beacons by design). Visitors: Chrome 116 (X11), Android Chrome 146, `UrlQueryCollector/1.0` (urlquery bot), Firefox 134, python-requests (Tencent).

### cbcb10de — jina-cache reader test (re-registered 2026-10-04)
Test page (decoded from httpbun base64 in the `kind=start` POST; saved as `cbcb10de-jinacache-page.html`): `sendBeacon` to the inbox with `kind=start/headers{N}/body{N}-{offset}/done`; fetches `https://r.jina.ai/https://amap-pc-ssr.amap.com/ssr/place/B001C8MXRO` (±trailing slash) with `X-Cache-Tolerance: 2592000`; chunks body in 45k slices. Retrieved bodies = r.jina.ai markdown of Amap SSR place page (Chengdu Zoo, `B001C8MXRO`): `200`, `content-type: text/plain; charset=utf-8`. `UrlQueryCollector/1.0` GETs mirror every `kind=` (`start/headers0/headers1/body0-0/body1-0/done`) — the beacon URLs were submitted to urlquery.net and its collector replayed them.

## Sender-side infra notes (agent-infra profiling only; no identity pursuit)
- **Token creators** (inbox `ip` field): `43.135.16.75`, `43.163.128.105`, `43.162.198.24` → **Tencent Cloud Hong Kong (AS132203)**, UA `python-requests/2.32.5` — operator provisioning infra. (`0a947514` is the outlier: Firefox 157, IP `185.244.155.244` = Iraq/Kurdistan Net.)
- **Operator test egress**: `195.64.118.152` (Norway, Blix Solutions AS — hosting), UA Firefox 134 — ran the exploit pages itself and posted 4 of 5 stolen `bx-ua` tokens plus all cbcb10de beacons. Same IP owns the view-token inbox.
- **Distributed beacon exits**: identical `Chrome/116.0.0.0 (X11; Linux x86_64)` UA from 6 IPs (85.203.15.253 DE/Clouvider proxy-flagged, 182.253.42.232, 102.244.78.57, 182.16.252.230, 102.130.232.27, 170.231.93.133) — uniform UA across geo-distributed exits = proxy/VPN-distributed headless test harness.
- **urlquery linkage**: `UrlQueryCollector/1.0` hits on 6ddc559e, a7753b69, cbcb10de — operator submits their own test/beacon URLs to urlquery.net (matches Chinese-infra urlscan sightings of the view token).
- **Probe epochs**: marker epochs `1791126060505`, `1791126724959`, `1791126770493`, `1791127001690`, `1791127124529`, `1791133015584` all land 2026-10-04 ~15:01–17:00 UTC = the fleet session window; current default pages iterate on the httpbun-delivered originals.

## View-token findings (recovery path: CRACKED)
`https://webhook.site/#!/view/<uuid>` maps 1:1 to inbox `<uuid>` — the SPA route `token: /view/{id:guid}` loads it read-only; **no special endpoint needed**, `GET /token/<uuid>` + `/token/<uuid>/requests` serve it. `e691f66e-…` is itself a fleet inbox (created 2026-10-04 07:19:52, earliest of the set). Any further `#!/view/<uuid>` tokens found in urlscan/Chinese-infra data can be pulled the same way. Note: fetching the SPA JS was only needed to confirm this; the token API alone suffices.

## Files
- `deaddrop-probe-20261005T052152.jsonl` — token metadata for all 10 inboxes (404s stored as error-page stubs)
- `deaddrop-reqs-20261005T052807.jsonl` — full request lists (headers+body) for the 4 alive inboxes
- `viewtoken-e691f66e-reqs.json` — view-token inbox request list
- `default-content-6ddc559e.txt`, `default-content-a7753b69.txt`, `default-content-0a947514.txt`, `default-content-cbcb10de.txt` — default responses
- `a7753b69-bxua-tokens.txt` — the 5 exfiltrated signed `bx-ua` URLs
- `a7753b69-running-page-from-referer.html` — httpbun-delivered running page (from beacon Referer)
- `cbcb10de-jinacache-page.html` — decoded jina-cache test page
- `probe.sh`, `fetch-requests.sh` — reuse scripts (paced ≤1 req/5s, `curl -m 60`)

## Caveats
- 6 legacy inboxes are **provably dead** (404 + "deleted, or expired automatically" page) — any still-firing legacy cron would be hitting a dead URL.
- The stolen `bx-ua` tokens are replay values from the operator's own test runs (their own harness generated them); `419| ` replays show Amap rejected at least two.
- No base64 payloads other than the two httpbun page-wraps were present; nothing further to decode.
