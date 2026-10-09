# China Surfaces Sweep — 2026-10-04

Operator: subagent d5b97aa7 (parent orchestrator, full-court press)
Scope: Chinese surfaces only — ZoomEye, Quake, ThreatBook, Baidu, Weibo/Zhihu.
Markers: `uqscan`, `uqcors`, `lhr.life`, `<hex>.lhr.life` tunnel pattern, `pandalegacy`,
`sub_poi_navi`, is.gd slugs `mf075827` / `sum074114` / `3JlIp7`,
operator IPs `106.11.226.79`, `47.246.165.44`.
Known-fleet context (excluded from "new"): Chinese Amap-map data-collection fleet,
`uqscan=<word><date>` tags, `<hex>.lhr.life` tunnels, webhook.site dead-drops, Jan–Oct 2026.

Doctrine applied: "no API key is not a stop" — attempted frontend/XHR route discovery on
each surface; documented every endpoint found (path, auth, params) for reuse.
**Zero unauthenticated IOC/banner query endpoints found on any of the four primary surfaces.**

## Collection environment (blocks everything curl-based)

- Direct curl from this VM to ALL tested hosts fails: `baidu.com`, `zoomeye.org`,
  `quake.360.cn`, `x.threatbook.com` (and even `example.com`, `huggingface.co`) all return
  http=000. DNS for these domains resolves to intercepted 198.18.241.x addresses; the
  runtime egress proxy's CONNECT tunnels time out (>20s) on every host.
- Consequence: **no curl-based collection is possible from this VM right now.**
  All surface checks below were done via the runtime text-fetcher (`browser.open`) and
  `browser.search`, which use separate egress.
- `browser.open` fetcher reaches `baidu.com` (once) and `x.threatbook.com` (login wall);
  it is blocked by `zoomeye.org` (HTTP 521), `quake.360.cn` (HTTP 500 empty),
  `zhihu.com` (403), `s.weibo.com` (no extractable content / JS-login wall),
  `x.threatbook.cn` (transport timeout).

## 1. ZoomEye (zoomeye.org) — VERDICT: login-gated, no unauth XHR found

- Web UI search (`/searchResult?q=lhr.life`): fetcher gets HTTP 521 from origin
  (anti-bot). No results obtainable without a session.
- API is fully credentialed. Documented endpoints for reuse (all require auth):
  - `POST https://api.zoomeye.org/user/login` — body `{"username","password"}` → JWT token
  - `GET https://api.zoomeye.org/host/search?query=<dork>&page=<n>` — header
    `Authorization: JWT <token>`; response `{"total": N, "matches": [...]}`
  - `GET https://api.zoomeye.org/web/search?query=<dork>&page=<n>` — same auth
  - `GET https://api.zoomeye.ai/v2/search?query=<dork>` — newer host, API-key auth
    (spotted in third-party skill: `curl -s "https://api.zoomeye.ai/v2/search?query=app:{component}"`)
  - Docs: `https://www.zoomeye.org/api/doc`, `https://www.zoomeye.ai/doc/`
  - Official SDK/CLI: `github.com/zoomeye-ai/ZoomEye-python` (`zoomeyeai search "<dork>"`)
  - MCP server: `github.com/zoomeye-ai/mcp_zoomeye`
- Writeups surveyed (official python lib, uncover agent source, Metasploit module,
  vulners, rubydoc): none describe an unauthenticated search path. ZoomEye removed
  anonymous search years ago.
- **Blocker for banner/tunnel-exit hunting:** need a ZoomEye account + API key (free
  registration tier exists per docs). No credentials available to this agent.
  Follow-up for parent: create/login a ZoomEye account via live browser, then query
  `hostname:lhr.life`, `ssl:"lhr.life"`, banner keywords `uqscan`/`uqcors`.

## 2. Quake (quake.360.cn) — VERDICT: token-gated, no unauth XHR found

- Web UI (`/quake/` SPA): fetcher gets HTTP 500 empty response (anti-bot). No query
  possible without a session.
- API is token-credentialed. Documented endpoint for reuse:
  - `POST https://quake.360.cn/api/v3/search/quake_service`
    header `X-Quake-Token: <token>`
    body `{"query":"<quake dork>","start":0,"size":10,"ignore_cache":true,
            "start_time":"2026-01-01","end_time":"2026-10-04"}`
  - Official CLI: `github.com/360quake/quake_rs` (`quake search 'port:80'`, supports
    `-s/-e` time windows, `-u` IP-batch upload ≤1000)
  - Token from free registration at quake.360.cn (free quota tier documented in CLI README).
- No writeup describes an unauthenticated search endpoint.
- **Blocker:** need a Quake account token. Follow-up: register via live browser, then
  search `domain:"lhr.life"`, service banners containing `uqscan`/`uqcors`, and
  time-window the Amap fleet's active period.

## 3. 微步在线 ThreatBook — VERDICT: login wall confirmed, no IOC data obtainable

- `https://x.threatbook.com/domain/lhr.life` → **redirects to ThreatBook 用户登录**
  (login page: 微步在线 account, APP scan / password / SMS login). Confirmed via fetcher
  page text: "登录微步在线账号…还没有账号？马上注册".
- `https://x.threatbook.cn/domain/lhr.life` (the .cn variant cited in Chinese writeups):
  fetcher transport timeout — unreachable from here.
- API surface (all key-credentialed, no unauth IOC lookup found):
  - Base `https://api.threatbook.cn`, e.g. `POST /v3/file/upload`, `GET /v3/file/report`
    (per chaitin/octobus and chj0w0/openclaw_skill_threatbook-scan SKILL.md)
  - API docs index: `https://x.threatbook.com/apiDocs` / `https://x.threatbook.com/api_docs`
    (behind login)
- **Result for requested lookups:** NO first-seen dates, NO related IOCs obtainable for
  `lhr.life`, `106.11.226.79`, `47.246.165.44`, or the is.gd slugs — all require an
  authenticated session.
- **Blocker:** need a 微步在线 account (free community registration exists). Follow-up:
  register via live browser, then pull domain/IP intel pages and the "关联 IOC" graph.

## 4. Baidu (baidu.com) — VERDICT: one query worked, then anti-bot wall

- `https://www.baidu.com/s?wd=uqscan` (via fetcher, full results rendered):
  **clean negative for agent discussion** — only noise: UQ university printing pages,
  QR-code scanner sites, one 2025-07-28 Chinese article about Unicornscan (network
  scanner tool, unrelated). No Chinese-language discussion of the `uqscan` tag.
- `https://www.baidu.com/s?wd=uqcors` and `?wd="lhr.life"` → **百度安全验证**
  ("网络不给力，请稍后重试") — Baidu anti-bot verification triggers on the 2nd+
  automated request from the fetcher egress IP. No results retrievable.
- Consequence: Baidu marker sweep is **partially blocked after 1 query**. The remaining
  markers (`uqcors`, `lhr.life`, `pandalegacy`, `sub_poi_navi`, is.gd slugs, operator IPs)
  could not be checked on Baidu.
- Reuse notes (unverified leads, not tested): mobile endpoint
  `https://m.baidu.com/s?word=<q>` and suggestion API
  `https://suggestion.baidu.com/su?wd=<q>` are historically less guarded; worth trying
  from a live browser with cookies. Rate-limit: ≥1 query per IP per window trips verification.

## 5. Weibo / Zhihu — VERDICT: blocked, site: searches clean

- `https://s.weibo.com/weibo?q=uqscan`: no extractable content (JS/login wall).
- `https://www.zhihu.com/search?q=uqscan&type=content`: HTTP 403 to fetcher.
- `browser.search` `site:weibo.com uqscan OR lhr.life OR uqcors` (zh): **no results**.
- `browser.search` `site:zhihu.com uqscan OR lhr.life OR uqcors` (zh): **no results**.
- Chinese security communities `site:xz.aliyun.com OR site:freebuf.com OR site:anquanke.com`
  + `uqscan lhr.life`: **no results**.
- No Chinese-language researcher discussion of any marker found on any indexed surface.

## 6. Per-marker verdicts (general web)

| Marker | Verdict |
|---|---|
| `uqscan` | Baidu: noise only (UQ printing, QR scanners). General web: noise. No agent discussion. |
| `uqcors` | Baidu blocked before results. General web: CORS docs + TON-wallet address noise. No agent discussion. |
| `lhr.life` | Baidu blocked. General web: **LEAD found** (see below); rest is scam-checker/urlscan noise on random localhost.run subdomains (expected — localhost.run assigns random hex subdomains to all users). |
| `pandalegacy` | Fortnite Creative map creator only (fchq.io). Noise, unrelated. |
| `sub_poi_navi` | POI/navigation-device manuals only. Noise, unrelated. |
| is.gd `mf075827` / `sum074114` / `3JlIp7` | No indexed hits (only false-positive digit-substring matches in PDFs). |
| `106.11.226.79` / `47.246.165.44` | No indexed discussion anywhere. |

## LEAD — agent-harness tunnel infra on lhr.life (does NOT fit the Amap frame; treat as lead)

- `github.com/bebabinlarsson-blip/Godot-MCP` release **v5.0.33** (~late Sep 2026):
  "Permanent Tunnel via localhost.run (No 15m Timeout, No 403 Blocks)".
  - Sets **`localhost.run` (`*.lhr.life`) as the primary default tunnel provider** across
    `godot-ai tunnel` and `start_ssh_tunnel`.
  - Explicit anti-bot framing: "Unblocked for External AI Agents — Eliminates Cloudflare
    Bot Management 403 Forbidden / 530 blocks. **External ChatGPT, OpenAI, and Claude
    requests pass straight through with 200 OK.**"
  - Background keep-alive daemon: `GET /health` every 25s through the tunnel.
- Why it matters: an **AI-agent MCP harness standardizing on `*.lhr.life` tunnels with
  documented anti-bot intent** — same tunnel-exit infrastructure family as the Amap fleet's
  `<hex>.lhr.life` pattern, but a different operator/purpose (agent-to-agent ingress,
  not map-data exfiltration). This is agent/swarm-shaped: harness defaults that many
  deployed agent instances would inherit.
- Suggested follow-ups: (a) check whether other MCP/agent repos pin localhost.run as
  default tunnel (search GitHub for `lhr.life` in agent/MCP repos); (b) banner-scan the
  `*.lhr.life` space on ZoomEye/Quake for agent-harness banners (`godot-ai`,
  `start_ssh_tunnel`, MCP-ish HTTP titles) once credentials exist.

## Blockers / what needs a live browser or credentials

1. **ZoomEye**: needs account + API key (free tier) → query `hostname:lhr.life`,
   banner strings `uqscan`/`uqcors`.
2. **Quake**: needs `X-Quake-Token` (free registration) → `domain:"lhr.life"`,
   time-windowed banner search over Jan–Oct 2026.
3. **ThreatBook**: needs 微步在线 account → domain/IP intel + related-IOC graph for
   `lhr.life`, `106.11.226.79`, `47.246.165.44`.
4. **Baidu**: needs a live browser session (cookies) to get past 百度安全验证 and finish
   the marker sweep (`uqcors`, `lhr.life`, `pandalegacy`, `sub_poi_navi`, slugs, IPs).
5. **Weibo/Zhihu**: need logged-in live browser for native search.
6. **VM curl egress is down** (proxy CONNECT timeouts on all hosts) — curl-based
   collection impossible until egress is repaired; this also blocks the "read page
   source → find XHR" technique from this VM, since page source can't be fetched.

## Endpoint registry (for reuse; all auth-gated unless noted)

- `GET https://api.zoomeye.org/host/search?query=<dork>&page=<n>` — `Authorization: JWT <token>`
- `GET https://api.zoomeye.org/web/search?query=<dork>&page=<n>` — `Authorization: JWT <token>`
- `POST https://api.zoomeye.org/user/login` — `{"username","password"}` → JWT
- `GET https://api.zoomeye.ai/v2/search?query=<dork>` — API-key auth (newer)
- `POST https://quake.360.cn/api/v3/search/quake_service` — `X-Quake-Token: <token>`,
  body `{"query","start","size","ignore_cache","start_time","end_time"}`
- `https://api.threatbook.cn/v3/...` — API-key auth; docs at `https://x.threatbook.com/apiDocs` (login)
- `https://www.baidu.com/s?wd=<q>` — no auth, but anti-bot verification after ~1 automated req/IP
- No unauthenticated XHR/search endpoint was found on ZoomEye, Quake, or ThreatBook in
  any surveyed writeup or SDK source.
