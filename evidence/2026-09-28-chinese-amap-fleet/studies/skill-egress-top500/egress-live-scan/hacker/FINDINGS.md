# TUNNELHAWK — live-probe findings, egress destinations
**Date:** 2026-10-05 ~14:44 UTC (09:44 CDT) · **Persona:** hacker (TUNNELHAWK)
**Method:** one public GET/HEAD per endpoint, polite ~3s pacing, no auth, no forms, no payloads, no exploitation. Curl from this VM's egress (IPv6 proxy, remote IP observed as `fd8b:4f84:7d32:99::1` — infrastructure egress address, not an attribution claim). One attempt per endpoint; no retries.
**Control:** `https://example.com` returned HTTP 200 in 10.96s — VM egress itself works (slow). A `000` below is destination-specific, not a broken pipe.

**Evidence rule:** full observed header/body values kept; sensitivity noted beside values, never redacted. Cookie values below are server-set anonymous session/tracking cookies minted for this probe — not credentials, not reusable for auth.
**Scope:** infrastructure only. No human/operator attribution. No webhook was created, touched, or enumerated; webhook platforms probed via public docs only.

---

## F-1 — r.jina.ai keyless reader proxy → DEAD (from this vantage)
- **Probed:** `https://r.jina.ai/https://example.com` (GET, 25s timeout)
- **OBSERVED:** `HTTP:000 TIME:25.001448s SIZE:0` — full connection timeout, zero bytes. No headers, no body. Control (`example.com`, HTTP 200) proves the failure is jina-specific.
- **Agent-use (one line):** keyless fetch proxy that launders any URL through a trusted reader domain — currently unusable from here.
- **Verdict:** dead. **Changed-since-study:** confirms the 2026-10-03 skill-ladders lane judgment ("r.jina.ai keyless DEAD as of now") — the fallback these 6 skills ship no longer resolves from our egress. Whether jina blocked this egress path or the service itself is down is undetermined from one probe.

## F-2 — ngrok.com → LIVE
- **Probed:** `https://ngrok.com` (HEAD)
- **OBSERVED:** `HTTP 200 OK` in 2.614s. Headers (full):
  ```
  Accept-Ranges: bytes
  Access-Control-Allow-Origin: *
  Age: 87111
  Cache-Control: public, max-age=0, must-revalidate
  Content-Disposition: inline; filename="index.html"
  Content-Type: text/html; charset=utf-8
  Date: Mon, 05 Oct 2026 14:44:03 GMT
  Etag: "0aa07af9ed5d302ddb7098031d23ae92"
  Last-Modified: Sun, 04 Oct 2026 14:32:11 GMT
  Link: </.well-known/api-catalog>; rel="api-catalog", </openapi.json>; rel="service-desc"; type="application/json", </docs/api>; rel="service-doc"
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Referrer-Policy: strict-origin-when-cross-origin
  Set-Cookie: __vdpl=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax   (empty deletion cookie, server-set — not a credential)
  Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
  Vary: Accept
  X-Content-Type-Options: nosniff
  X-Ngrok-Edge: 1
  X-Ngrok-We-Are-Hiring: https://ngrok.com/careers
  X-Xss-Protection: 0
  Content-Length: 147969
  ```
- **Agent-use (one line):** account signup → agent-exposed localhost tunnel with a public `*.ngrok.io` URL (the #1 primitive in the study).
- **Verdict:** live. No change since study.

## F-3 — Cloudflare (cloudflared) status/docs → LIVE
- **Probed:** `https://www.cloudflarestatus.com` (HEAD)
- **OBSERVED:** `HTTP 200 OK` in 2.651s. `server: Google Frontend`, `via: 1.1 google`. Full NEL/reporting headers observed (event-ingest.cloudflarestatus.com). Cloudflare's tunnel product (cloudflared) status is reachable.
- **Agent-use (one line):** agent-driven `cloudflared tunnel` exposure of localhost, same primitive class as ngrok.
- **Verdict:** live. No change since study.

## F-4 — catbox.moe → UNREACHABLE from this VM
- **Probed:** `https://catbox.moe` (GET, 20s timeout)
- **OBSERVED:** `HTTP:000 TIME:11.497732s SIZE:0`; curl reported `(52) Empty reply from server` — connection opened, then nothing. No headers file, no body. 39-byte headers file contains only the proxy's `HTTP/1.1 200 Connection Established` line.
- **Agent-use (one line):** no-signup anonymous file/image host — the study's confirmed gitshot screenshot-fallback dead-drop.
- **Verdict:** dead (from this egress). **INFERENCE:** could be VM-egress-specific filtering or a genuinely down edge; undetermined from one probe. The study's corpus evidence (gitshot→catbox code) stands on its own; liveness here is a negative observation, not a refutation.

## F-5 — sci-hub.se → UNREACHABLE from this VM
- **Probed:** `https://sci-hub.se` (HEAD, 20s timeout; liveness only per brief)
- **OBSERVED:** `HTTP:000 TIME:1.372478s SIZE:0` — fast fail (DNS refusal or immediate connection refusal, not a timeout).
- **Agent-use (one line):** paywall-bypass fetch target (study: used with `verify=False` TLS bypass).
- **Verdict:** dead (from this egress). Same caveat as F-4.

## F-6 — uploads.github.com → LIVE
- **Probed:** `https://uploads.github.com` (GET)
- **OBSERVED:** `HTTP 302 Found` in 1.517s. Full headers:
  ```
  Content-Security-Policy: default-src 'none'
  Location: https://github.com
  Strict-Transport-Security: max-age=31557600
  X-Content-Type-Options: nosniff
  X-Frame-Options: deny
  X-XSS-Protection: 1; mode=block
  Date: Mon, 05 Oct 2026 14:44:32 GMT
  x-github-edge-region: westus2
  X-GitHub-Request-Id: 2F58:311876:1D83A:81612:6AC3B7CF
  Content-Length: 0
  ```
- **Agent-use (one line):** trusted-host upload endpoint (GitHub Release Assets) — files land on a github.com-trusted domain, the gitshot exfil grammar.
- **Verdict:** live. No change since study.

## F-7 — LocalCan public surface → LIVE (GitHub repo; no standalone site found in study)
- **Probed:** `https://github.com/localcan/localcanapp` (HEAD) — the study documents no standalone LocalCan site; its public surface is this repo.
- **OBSERVED:** `HTTP 200 OK` in 1.877s, `Server: github.com`, `x-github-edge-region: sea`, `X-GitHub-Request-Id: 17AF:7046E:3FF088D:45D7E01:6AC3B7D4`. Server-set anonymous session cookies (full values kept per evidence rule; not credentials):
  ```
  Set-Cookie: _gh_sess=PmHgzl2jBJqndj20AVgyuvZ0KekIZgfTD%2BWkofN9M1BvvV8yoZJ9oQK9nR6GnhMv4FqJolupgjFFC5qNJqTV3YJ3JC7%2FNF5a10L1Ecw6JwsseRnU8JSOzlSMCf3r19KagqOa%2FJVco54bp29DoUcH%2BqpJsN2MUdbDmAHTCyrffLP2up8YSEF64thMW1ALJ6gDmg7eoRRaK4Y74YuPmCEPNaN%2Fpq2te3I0tCbo7jBIt%2B8n491JfkW2P8UZl3niDcInAIu0UzWP1LAvbPyCkz7spg%3D%3D--1cOfMgok350b8rxN--mRle27fegmPswReq%2BYCKIQ%3D%3D; path=/; HttpOnly; secure; SameSite=Lax
  Set-Cookie: _octo=GH1.1.468050606.1791211476; expires=Tue, 05 Oct 2027 14:44:36 GMT; domain=.github.com; path=/; secure; SameSite=Lax
  Set-Cookie: logged_in=no; expires=Tue, 05 Oct 2027 14:44:36 GMT; domain=.github.com; path=/; HttpOnly; secure; SameSite=Lax
  ```
- **Agent-use (one line):** localhost tunnel broker with a closed binary (study: docs-only) — agent installs the client, gets a public URL for its local services.
- **Verdict:** live (public surface). No change since study.

## F-8 — roamzy.io → LIVE
- **Probed:** `https://roamzy.io` (GET)
- **OBSERVED:** `HTTP 200 OK` in 1.783s, 58,678 bytes. `<title>Roamzy — One eSIM. The whole world. Pay per megabyte.</title>`. Meta description (verbatim): "A single global eSIM in 193 countries, billed by the megabyte, paid in USDT or USDC. No packages, no expiry, top up once and travel anywhere." CSP `connect-src` includes `https://api.nowpayments.io` (payment processor) and `https://cloudflareinsights.com`. `access-control-allow-origin: https://roamzy.io`. `CF-RAY: a45d34b12aea7769-YYZ` (Cloudflare-fronted; ray ID is a request trace, not a secret).
- **Agent-use (one line):** anonymous crypto-funded eSIM purchase — an agent can buy real mobile data/identity-adjacent connectivity with USDT/USDC, no account.
- **Verdict:** live. **Genuinely new vs study:** the study had only the marketplace listing name; the site's copy, the nowpayments.io payment rail, and the Cloudflare fronting are newly observed here.

## F-9 — Discord webhook surface (docs only) → LIVE, docs moved
- **Probed:** `https://discord.com/developers/docs/resources/webhook` (HEAD) — docs only; no webhook endpoint was touched.
- **OBSERVED:** `HTTP 301 Moved Permanently` in 1.222s. `Location: https://docs.discord.com/developers/resources/webhook`. `Server: cloudflare`. Webhook developer docs live at the new `docs.discord.com` host.
- **Agent-use (one line):** POST JSON to a webhook URL → message/file dead-drop in a Discord channel (the study's confirmed dead-drop grammar).
- **Verdict:** live. **Changed-since-study (minor):** docs migrated from `discord.com/developers/docs` to `docs.discord.com`.

## F-10 — Slack webhook surface (docs only) → LIVE, docs moved
- **Probed:** `https://api.slack.com/messaging/webhooks` (HEAD) — docs only; no webhook endpoint was touched.
- **OBSERVED:** `HTTP 302 Found` in 1.637s. `location: https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks`. `server: Apache`, `x-backend: main_normal`, `x-server: slack-www-hhvm-main-iad-r8dclssp0adb` (IAD region backend; infra detail, not attribution). `x-slack-unique-id: 5c0a1419-da89-4b9e-b09d-ecac91abed8a` (request trace ID). Server-set cookies (full values; tracking/anonymous, not credentials):
  ```
  set-cookie: utm=%7B%7D; expires=Mon, 19-Oct-2026 14:44:50 GMT; Max-Age=1209600; path=/; domain=.slack.com; secure; SameSite=None
  set-cookie: b=b692d98f18a903a7a3955a37236134a0; expires=Sun, 05-Oct-2036 14:44:50 GMT; Max-Age=315619200; path=/; domain=.slack.com; secure; SameSite=None
  set-cookie: x=b692d98f18a903a7a3955a37236134a0.1791211490; expires=Mon, 05-Oct-2026 14:59:50 GMT; Max-Age=900; path=/; domain=.slack.com; secure; SameSite=None
  ```
  (`hooks.slack.com` itself was not probed directly per the docs-only constraint.)
- **Agent-use (one line):** POST JSON to an incoming-webhook URL → dead-drop into a Slack channel.
- **Verdict:** live. **Changed-since-study (minor):** docs migrated from `api.slack.com/messaging` to `docs.slack.dev`.

---

## INFERENCE (separated from OBSERVED above)
1. **Scorecard from this vantage:** 7 live (ngrok, Cloudflare, uploads.github.com, LocalCan repo, roamzy.io, Discord docs, Slack docs), 3 unreachable (r.jina.ai, catbox.moe, sci-hub.se). The unreachable three are exactly the ones a defender would want dead — but one probe from one egress path cannot distinguish "service down" from "this network path filtered."
2. **jina's death is the biggest delta.** It was the study's #2 primitive and the corpus relay; its keyless reader timing out from our egress matches the independent 2026-10-03 lane judgment. Skills shipping the `JINA_READER_PREFIX` fallback are carrying dead code until it recovers — or they have failover we didn't test.
3. **The dead-drop layer is fully alive:** Discord/Slack docs up, GitHub upload host up, ngrok up. Nothing in the top-10's exfil path degraded except the reader-proxy and the two fringe hosts.
4. **roamzy.io is the most agent-native surface observed:** anonymous-first purchase, crypto rails (nowpayments.io), per-MB billing — purpose-built for agents, live, 58KB landing page, Cloudflare-fronted.
5. **No misconfigurations encountered.** Every endpoint returned ordinary public responses; nothing was interacted with beyond the single documented GET/HEAD.

## Nulls / limits
- `hooks.slack.com` and `discord.com/api/webhooks` API surfaces not probed (docs-only constraint).
- No payload content beyond r.jina.ai's intended benign fetch (which never returned).
- Single attempt each; no retry, no rate-limit probing, no TLS-fingerprint evasion.
- catbox.moe API docs not reached (site itself unreachable).
