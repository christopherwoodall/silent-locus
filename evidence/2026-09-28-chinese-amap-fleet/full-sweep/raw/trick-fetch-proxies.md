# Fetch-proxy / CORS-relay sweep — Amap fleet markers (2026-10-04)

Surface: fetch proxies / CORS relays (trick class: proxies only).
Sibling lanes already covering r.jina.ai, allorigins, translate.goog, microlink,
href.li were NOT redone.

Method note: direct curl from this VM was flaky — DNS is sinkholed
(198.18.241.x for every host) and the egress proxy timed out on
corsproxy.io, api.codetabs.com, cors.isomorphic-git.org, images.weserv.nl,
jsonp.afeld.me (empty reply), github.com, huggingface.co, while
google.com, urlquery.net, wsrv.nl, raw.githubusercontent.com and urlscan.io
intermittently succeeded. Facts below come from `browser.open`,
`browser.search`, and the urlscan.io public search API; per-service gaps caused
by egress are marked. No proxy service in this lane exposes public request
logs — every verdict below is "no", with exactly what was tried.

## 1. corsproxy.io — NO public logs
- Queryable? No. Now REQUIRES an API key: `https://corsproxy.io/?key=YOUR_API_KEY&url=<enc>`
  (verified from homepage via browser.open, 2026-10-04). Free tier: 10,000
  requests + 1 GB/month, no credit card. Usage history lives in a per-account
  Analytics Dashboard at console.corsproxy.io (login-walled).
- No /logs, /stats, /history, or public request index found on the site.
- Endpoint/param map for reuse: legacy no-key form `https://corsproxy.io/?url=<enc>`
  still documented in the wild; per anentrypoint/cors live-probe it 403s
  header-less server-side fetches (needs browser Origin / dev origin).
  Documented params: `image`, `imageWidth`, `imageHeight`, `imageFit`,
  `imageFormat`, `ttl` (edge cache seconds), `extract`, `format`, `input`,
  `output`, `reqHeaders`, `resHeaders`.
- Markers: n/a — no queryable index.

## 2. codetabs proxy (api.codetabs.com) — NO public logs
- Endpoint verified (codetabs.com/cors-proxy/cors-proxy.html):
  `https://api.codetabs.com/v1/proxy?quest=<url_to_http_resource>` —
  GET-only, 5 MB per-request cap, 5 req/sec (429 beyond). No logs, stats, or
  history surface anywhere in its docs.
- Agent-usage signal (not a fleet, but lane-relevant): on-panda/browser-agent-skills
  `skills/cors-internet/SKILL.md` documents codetabs as the agent fetch fallback:
  "Codetabs: `https://api.codetabs.com/v1/proxy?quest=ENCODED_URL` → raw HTML.
  Use when Jina cannot render or when raw DOM matters." Agents use this lane;
  the proxy keeps no public log of it.
- Egress: api.codetabs.com timed out from this VM (curl 000); evidence via
  search only.

## 3. cors.isomorphic-git.org — NO public logs
- Git-scoped proxy (isomorphic-git/cors-proxy, sponsored by Clever Cloud);
  blocks requests that don't look like valid git requests. Root path returns
  HTTP 400 without a target (verified via browser.open upstream rejection).
  Shape: `https://cors.isomorphic-git.org/<target-url>`. No logs/history.

## 4. jsonp.afeld.me — NO public logs; service degraded
- JSONP-only GET proxy: `https://jsonp.afeld.me/?url=<url>&callback=<cb>`.
  curl from VM: "Empty reply from server" (reachable, broken response).
  anentrypoint/cors classifies it historical/unreliable. No logs.

## 5. whateverorigin (revived) — NO public logs
- whateverorigin.org now 301-redirects to https://www.whateverorigin.org/
  (verified via curl Location header; site content crawled ~25 days ago).
  Endpoint: `https://www.whateverorigin.org/get?url=<url>` (+ `&callback=`
  for JSONP). No public log/history surface found.
- Successor worth noting: alianza/everyOrigin (Netlify-hosted, no key, no rate
  limit, open source) — also no public logs.

## 6. images.weserv.nl / wsrv.nl — NO public per-URL logs
- Image resize proxy. Homepage fetched (200, VitePress docs site).
  API: `https://wsrv.nl/?url=<host/path>&w=&h=&fit=&...`.
  Checked `/`, `/docs/`, `/robots.txt` (empty), sitemap (fetch failed):
  no public request log, stats page, or history endpoint.
- images.weserv.nl (old domain) timed out from this VM; wsrv.nl is current.

## 7. Google Translate proxy (classic) — superseded, no separate logs
- The classic `translate.google.com/translate?u=` website-translation flow is
  superseded by the `translate.goog` proxy (sibling lane). No separate public
  log surface for the classic endpoint.

## 8. Baidu / Yandex / Sogou translate proxies
- Yandex: webpage-translation proxy confirmed with PUBLIC, unauthenticated,
  shareable proxied URLs:
  `https://translated.turbopages.org/proxy_u/<langpair>.<host>.<uuid>-74722d776562/<scheme>/<target-host>/<path>`
  (e.g. `.../proxy_u/ja-en.en.1f823d34-64db980e-910d74e0-74722d776562/https/cyberpithilo.web.fc2.com/...`).
  Yandex itself publishes no log of translated pages; urlscan.io holds scans of
  proxied URLs (`domain:translated.turbopages.org` → total 1 via anonymous API).
- Baidu: Fanyi offers webpage translation (per Wikipedia: "translating text
  paragraphs and web pages"); exact proxy URL pattern not verifiable from public
  sources in this pass; no public logs.
- Sogou: no webpage-translation proxy found (fanyi.sogou.com is text-only).

## 9. Google Apps Script public proxies — NO central log (per-deployment islands)
- Pattern confirmed (praveenkarunarathne/google-apps-script-simple-http-proxy):
  `https://script.google.com/macros/s/<deployment-id>/exec?url=<target>`.
  Quotas: UrlFetchApp ~20k calls/day (consumer). There is NO canonical public
  multi-tenant GAS proxy — every deployment is its own island with no shared
  history. Enumerating live public deployments would need GitHub code search
  (auth-gated); not pursued — no operator-identity angle chased.

## 10. Cloudflare Worker public proxies — NO public logs
- corsproxy.io = Cloudflare Worker, now key-gated (see §1).
- test.cors.workers.dev = Cloudflare's reference demo worker (`?<url>`), not a
  public service; needs a browser Origin header (403 to header-less fetches).
- Zibri/cloudflare-cors-anywhere = self-host Worker template (100k req/day free
  tier), not a shared service.
- cors.lol (`https://api.cors.lol/?url=<url>`, BradPerbs/cors.lol, Netlify
  serverless fn, free, no key — live-confirmed 200 by anentrypoint/cors) is
  NOT Cloudflare-based; also no public logs.
- No open multi-tenant public worker with a queryable request log found.

## Queryable-index marker runs
- urlscan.io public search API works anonymously for non-wildcard queries, BUT
  **leading-wildcard and regex searches are 403 for anonymous users**
  ("Regular Expressions and leading wildcard searches are not supported for
  anonymous users, please create a user-account"). So `page.url:*uqscan*`-style
  marker hunts need an authenticated urlscan account — flagged for follow-up.
- Anonymous full-text marker results: `q=uqscan` → 0; `q=pandalegacy` → 0;
  `q=sub_poi_navi` → 0.
- `domain:lhr.life` → 90 total public results (see LEAD below).
- Web co-occurrence `"uqscan" OR "uqcors" proxy fetch relay agent` → noise only
  (Authelia reverse-proxy docs PDF). Clean negative, consistent with sibling
  social-search.

## LEAD — tronzap.com PHPUnit-RCE probing via lhr.life tunnels, using urlscan.io as the fetch engine (burst: 2026-09-26)
Does not fit the Amap map-collection frame; per doctrine, a lead, never a negative.
- 38 urlscan results on 2026-09-26 matching `domain:lhr.life`
  (query: `domain:lhr.life AND date:2026-09-26`; total 38).
- Shape: submitted URL = `https://<hex>.lhr.life/<short>.html`; the tunnel page
  (299 B, served by `SimpleHTTP/0.6 Python/3.11.2`) then POSTs/navigates to
  `https://{api,dash,mock}.tronzap.com/...eval-stdin.php`, including the
  PHPUnit CVE-2017-9841 path `vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php`.
  Targets returned 403. Page title: "403 Forbidden".
- Concrete example (result UUID 01a0def2-682a-749e-92ed-7b3719676d22):
  submitted `https://d51842b87c3e80.lhr.life/e4.html` → effective
  `https://dash.tronzap.com/eval-stdin.php`; submitted via API 2026-09-26
  18:20:23 UTC (from US), scanned from DE.
- Burst grammar on 2026-09-26: 18× `api.tronzap.com` (`/v1/orders`,
  `/v1/orders/calculate`, `/v1/orders/check`), 6× `dash.tronzap.com`
  (incl. 4× `eval-stdin.php`), 1× `mock.tronzap.com`, plus tunnel pages
  `ba85c283a8f9e0.lhr.life/lw.html`, `/calc4.html`,
  `90c6961dd9eba0.lhr.life/app.html`, `d51842b87c3e80.lhr.life/e3.html`.
  Scans seconds apart (18:20:25 / 18:20:26 / 18:20:29) = automated prober.
- Reading: operator uses urlscan.io scans AS the request engine — tunneled pages
  fire exploit POSTs from urlscan's browsers. Tunnel page names (`e4.html`,
  `e3.html`, `app.html`, `lw.html`, `calc4.html`) are short agent-task-style names.
- Tunnel hosts seen 2026-09-26→10-04: d51842b87c3e80, ba85c283a8f9e0,
  90667af7b6a9f1 (scanned 7× across Sep 29–Oct 4 — a persistent tunnel being
  re-scanned), 90c6961dd9eba0, 1881e623217f7c, 2f102b0544d3b3, d789d4fd5debd8,
  c7a1f824a6efc4 — all `<hex>.lhr.life`, the same tunnel grammar as the known
  fleet, but the target set is exploit-probing, not map collection.
- Note: sibling social-search Q9 rated "tronzap probing" a CLEAN NEGATIVE on
  web/social surfaces only; urlscan.io shows this 38-scan burst. Either a
  different eval run on shared provider toolkit ("same provider, different
  agents, different evals") or a separate actor — needs follow-up, not
  attribution (no operator-identity work done or attempted).
- Recommended follow-ups: (a) pull the other 2026-09-26 result pages for POST
  bodies/payload grams; (b) diff the `<hex>.lhr.life` host set against the Amap
  fleet's known tunnel set; (c) get a urlscan account for leading-wildcard
  marker searches (`page.url:*uqscan*`, `*uqcors*`, `*pandalegacy*`,
  `*sub_poi_navi*`, `*webhook.site*`).

## Bottom line
- New undiscovered fleets via fetch-proxy/CORS-relay public logs: NONE — no
  service in this lane exposes a public request log or queryable fetch history.
  All ten services: queryable? NO (answers: per-account dashboards, key-gated
  APIs, git-only scope, degraded, revived-without-logs, static docs,
  superseded, per-deployment islands, reference-only workers).
- Endpoint/param map for all ten documented above for reuse.
- Agent usage of the lane is real (codetabs as documented Jina-fallback in an
  agent SKILL.md) but leaves no public log on the proxy side.
- One lead handed off: 2026-09-26 tronzap eval-stdin.php probing burst via
  `<hex>.lhr.life` tunnels using urlscan.io scans as the fetch engine —
  new vs the sibling's clean negative; infrastructure metadata only, no
  attribution attempted.
