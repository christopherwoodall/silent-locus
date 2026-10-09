# Kaspersky OpenTIP surface mapping

Date: 2026-10-05 ~01:55–02:00 CDT. Lane: full-sweep / Chinese Amap agent-fleet.
Prior context: regional-surfaces.md §1 "opentip.kaspersky.com — BLOCKED (needs registration; fetch failed)".
This pass fetched the site successfully (egress healthy for this host this time), mapped the frontend,
and empirically tested every keyless path.

## VERDICT: GATED — no keyless/anonymous programmatic path exists

- REST API without `x-api-key` → **HTTP 401** (empty 1-byte body), tested 2026-10-05 01:57 CDT on
  `/api/v1/search/domain?request=lhr.life` and `/api/v1/search/url?request=https://lhr.life/x`.
  A syntactically-valid dummy key also → 401 (invalid token rejected the same way).
- Web UI *may* permit anonymous lookups (a 2019 Kaspersky article states "no need to log in" for
  pasting a URL; current frontend shows an hCaptcha-gated flow), but the web UI's lookup XHR
  endpoint could NOT be extracted: the app's lazy JS chunks are not served by the origin from
  this egress (every `chunk-*.js` returns the SPA fallback index.html, HTTP 200 / 2853 bytes),
  and hCaptcha cannot be solved headless. This is a GAP (needs live-browser pass), not a negative.
- **No account was created** (out of scope for this lane).

## Endpoint inventory

### REST API (documented, token-required)
Base: `https://opentip.kaspersky.com/api/v1` — auth header `x-api-key: <token>`.

| Method | Path | Params / body | Auth | Notes |
|---|---|---|---|---|
| GET | `/search/hash` | `?request=<md5\|sha1\|sha256>` | `x-api-key` | — |
| GET | `/search/ip` | `?request=<ip>` | `x-api-key` | — |
| GET | `/search/domain` | `?request=<domain>` | `x-api-key` | bare domains OK here |
| GET | `/search/url` | `?request=<web address>` | `x-api-key` | URL must include a path; bare hosts → 400 |
| POST | `/scan/file` | query `?filename=<name>`; raw file bytes as body, `Content-Type: application/octet-stream` | `x-api-key` | submits to Kaspersky Cloud Sandbox; returns basic report |
| POST | `/getresult/file` | `?request=<file hash>` | `x-api-key` | full analysis report for a previously submitted file |

Verified live 2026-10-05: `/api/v1/search/domain`, `/api/v1/search/url` return 401 with no/dummy key.
Guessed alternates (`/api/v1/search/domains`, `/api/v1/domain`, `/api/search/domain`,
`/api/v1/public/search/domain`) all return the SPA fallback — not real endpoints.
`/api/v1/` itself → SPA fallback. Community client confirming this inventory:
`seifreed/opentip` (github.com/seifreed/opentip) — `DEFAULT_BASE_URL = "https://opentip.kaspersky.com/api/v1"`,
header `x-api-key`, same six endpoints (`client.py` fetched 2026-10-05).

### Web-UI (frontend-discovered, undocumented XHR)
The site is a Vite SPA: `/` → `index.html` (2853 bytes) → module `/public/app-Dhy7oeKq.js`
(~4.8 MB). From the main bundle only:

| Method | Path | Auth | Notes |
|---|---|---|---|
| GET | `/ui/checksession` | session cookie | returns session/user info; 401 → forces re-login |
| POST | `/ui/login` | — | body `{token: ...}` (UIS/Kaspersky-Account token flow) |
| GET | `/ui/login` | — | login state probe |
| GET | `/ui/changepass` | session cookie | — |
| GET | `/token` | session cookie | in-app route: "Request Tokens" page (token management) |

Frontend status enum found in bundle (axios interceptor): **401 = CAPTCHA**, **403 = RATE_LIMIT**,
409 = FORBIDDEN_EMAIL. CSP headers confirm hCaptcha integration
(`script-src ... https://hcaptcha.com https://*.hcaptcha.com ...`); the bundle references a
`handleCaptcha` lazy chunk + CSS, which the origin does not serve to us (see gap below).
Vite env in bundle: `VITE_SITE_ORIGIN="https://opentip.kaspersky.com"`. Docs for the web UI live at
`/Help/Doc_data/en-US/*.htm` (e.g. `ManagingToken.htm`, `SignInKLaccount.htm` fetched live).

## Query results against fleet markers

None — **no queries were executed**. Every programmatic lookup path requires the `x-api-key`
token; web-UI anonymous lookup requires solving hCaptcha. Markers queued for a follow-up once a
token exists: `uqscan`, `uqcors`, `pandalegacy`, `sub_poi_navi`, `uqtag`, `lhr.life`, `agedata23`,
`vizprod.aihw.gov.au` (domain + URL variants, since bare hosts are rejected by `/search/url`).

## Registration requirements (exact, from official help docs)

Per `/Help/Doc_data/en-US/ManagingToken.htm` and `SignInKLaccount.htm` (fetched live):

1. **Kaspersky Account** required — the same account used for My Kaspersky / Kaspersky Technical
   Support. Existing account works; otherwise "Create a new account" (email + password), or
   sign in with Facebook.
2. Must accept **Terms of Use** + **Privacy Statement** checkboxes (the "Sign in with Kaspersky
   Account" button stays inactive until accepted).
3. After sign-in: user menu (`<email>` dropdown) → **Request token** → set validity (default 1 year,
   **maximum 1 year**, immutable after generation) → token displayed (copy via eye icon).
4. Token is sent as the `x-api-key` header. Tokens can be revoked/regenerated at any time on the
   Request Tokens page; revocation invalidates immediately.
5. Quotas: a 2019 Kaspersky article states **100 threat-intelligence requests/day** for free users
   (unverified against current limits; current docs do not publish a number in the fetched pages).
   Frontend treats 403 as RATE_LIMIT.

Note: Kaspersky is a Russian-origin vendor; the hunt scope here is the OpenTIP surface only.
Registering an account was explicitly out of scope for this lane — a follow-up agent/user decision
is needed before creating one.

## Gaps (not negatives)

1. **Web-UI anonymous lookup endpoint unmapped.** The lazy JS chunks (`chunk-*.js`) that would
   contain the lookup XHR calls are not served by the origin to this egress (all return the SPA
   fallback). If the web UI allows anonymous lookups, a live-browser pass (solve hCaptcha, watch
   network) is needed to capture the endpoint. Cannot confirm or deny a keyless web path.
2. **Registration itself** — out of scope for this lane; follow-up decision required.
3. **Free-tier quota** — the 100 req/day figure is from 2019; current limit unconfirmed.
4. One runtime note: a `POST` probe to `/api/v1/search/url` (no key) was declined by a runtime
   confirmation guard at 2026-10-05 02:00 CDT — not retried, per policy. GET probes were unaffected.
