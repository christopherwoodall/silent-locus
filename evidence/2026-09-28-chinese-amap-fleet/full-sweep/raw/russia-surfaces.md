# Russia-surfaces sweep — Amap fleet markers (2026-10-04)

**Surfaces:** Yandex search, Telegram security channels (web previews), Russian
pastebins/forums/media. Sweeper: subagent (depth 2), 2026-10-04 ~22:50–23:15 CDT.
**Method note (per 2026-10-04 collection doctrine):** no-API-key is not a stop —
page sources were read and frontend XHR/form endpoints probed directly with
curl. Every endpoint found is documented below for reuse. Anti-bot/captcha
pages were NOT bypassed; they are recorded as blocks.

**Verdict: NO new agent/swarm fleet sightings on Russian surfaces. Zero
independent researcher discussion of our markers.** Russian-language media IS
actively covering urlquery agent traces — but only the already-known OpenAI
incidents (Transluce / Asymmetric Security), with no marker co-occurrence.

Known-context exclusion: the Chinese Amap-map data-collection fleet
(`uqscan=<word><date>` tags, `<hex>.lhr.life` tunnels, Jan–Oct 2026,
swarmcha.se/posts/chinese-agent-fleet) and the Transluce/Asymmetric OpenAI
agent-trace reports are known, not new.

## 1. Yandex search

### Direct SERP via curl — BLOCKED (anti-robot page, not bypassed)
- `curl -A <Chrome 126 UA> "https://yandex.com/search/?text=uqscan"` →
  HTTP 200, 118 KB, but the body is Yandex's JS anti-robot challenge
  (`isRobot` detection, `document.cookie robot=1`, SmartCaptcha scaffolding).
  Parsed: **0 organic result links** in the page. Same challenge was served to
  the text-fetch path earlier ("Are you not a robot?" SmartCaptcha).
- Yandex aggressively bot-gates scripted SERP access from this egress
  (corroborated by habr Q&A q/884443: "Почему яндекс почти сразу банит
  python-парсер?"). Not bypassed per policy. A live-browser Yandex pass could
  be delegated if wanted.

### Yandex Suggest API (public, unauthenticated XHR endpoint) — queried
- Endpoint: `GET https://suggest.yandex.com/suggest-ya.cgi?v=4&part=<marker>`
  (the same endpoint browsers use for address-bar suggestions; no key, no
  auth; documented here for reuse). Returns `["<marker>",[<completions>],{...}]`.
- `uqscan` → `["uqscan",[],{"r":1}]` — zero completions.
- `uqcors` → `["uqcors",[],{"r":84}]` — zero completions.
- `pandalegacy` → `["pandalegacy",[],{"r":84}]` — zero completions.
- `lhr.life` → `["lhr.life",[],{"r":84}]` — zero completions.
- `sub_poi_navi` → endpoint unstable for this string (2× timeout, 1× empty
  reply); no reading possible. Web-search evidence (below) is the primary
  negative for this marker.
- Read: Yandex's suggestion corpus has no query volume for any marker —
  consistent with these strings having no Russian search footprint. (Weak
  signal: suggest measures query popularity, not index presence.)

### Yandex web-search cross-checks (via general engine, RU language)
- `"lhr.life" туннель боты` (RU) → only GitHub READMEs of Russian Telegram-bot
  devs using `ssh -R … nokey@localhost.run` for Mini App webhooks
  (weibschatten/focus-telegram-miniapp, monopoly450/tg_bot_tu-ugmk,
  lesha2701/footycards3, hit-boy228/focusforge, kirillusha/forelka-userbot).
  Legit dev docs, no agents, no swarms. Filed as adjacent noise: Russian
  localhost.run usage exists (Telegram bot scene) but is not fleet-shaped.
- `"localhost.run" злоумышленники tunnel сканирование` (RU) → PT Security
  tunnel-detection PDF, a pentest book TOC. Generic, no fleet.
- `urlquery бот агенты сканирование URL` (RU) → Google robots.txt docs,
  vuln-scanner listicles, one Russian multi-agent-system repo
  (laminariia/multi-agent-system — LangGraph order-processing, unrelated).
- `"uqscan" OR "uqcors" OR "sub_poi_navi"` (RU) → no results.

## 2. Telegram security channels (web previews, no login)

### tgstat.com — probed per doctrine, no free XHR search endpoint
- `GET https://tgstat.com/search` → 200, 41 KB; single JS bundle
  `/static/js/app.js?v=1785995633`. Site search is a plain HTML form
  `POST /search` (fields: `query`, `_tgstat_csrk` CSRF token).
- `POST https://tgstat.com/search` with `query=uqscan` (+ token) → 200 but
  returns only the page shell: **0 channel/post result links, no result text**.
  Results render client-side and the full post search is premium-gated
  (`/payments/pay/premium_search`, `/login?redirect_uri=…premium_search`).
  Footer `/api/search`, `/api/stat`, `/api/callback` links are paid-API docs
  (tgstat.ru), not free endpoints.
- Conclusion: no unauthenticated tgstat XHR search endpoint exists; documented
  so future sweeps don't re-probe. (POST /search form endpoint recorded above.)

### t.me/s channel previews actually read
- **SecLabNews** (`https://t.me/s/SecLabNews`, SecurityLab.ru channel, current
  preview = Sep–Oct 2026 posts: Dodo Pizza breach, PS5 Relapse jailbreak,
  GLM-5.3 exploit bench, DATASUCKERS, VPN-server bans):
  - in-page find `urlquery` → 0 hits.
  - in-page find `агент` → 3 hits, all generic AI news, none fleet-shaped:
    one "Agentic SOC" webinar listing; one digest line that AI agents leaked
    13,000 work screenshots from 343 companies to public GitHub (one-line
    digest item, no markers, not a fleet); one Bitrix24 AI-agent ad.
  - No `uqscan` / `uqcors` / `lhr.life` / `pandalegacy` / `sub_poi_navi`.
- **youraisecurity** (`https://t.me/s/youraisecurity`, "Your AI & Security",
  personal AI/ML edu channel): vibe-coding and ML-math posts; no markers,
  no fleet content.
- **secaiml** (`https://t.me/s/secaiml`, "Безопасность ИИ и Ml", 276 members):
  group, not channel — web preview renders no posts. Dead end via preview.
- `site:t.me "lhr.life"` → no results. `site:t.me/s urlquery ИИ-агенты
  сканирование` (RU) → no results. `"uqscan" OR "uqcors" telegram` → noise
  (SEO-spam PDFs), no channel hits.

## 3. Russian pastebins / forums / media

- **antichat.ru**: `site:antichat.ru urlquery OR uqscan OR "lhr.life"` → 0 results.
- **cyberforum.ru**: `site:cyberforum.ru urlquery бот сканирование` → 0 results.
- **habr.com**: `site:habr.com urlquery` → hits are string collisions only:
  `$urlQuery` PHP variable in a Telegram-bot tutorial (3 dupes) and Helm's
  `urlquery` template function in an ArgoCD article. No urlquery.net, no
  agents, no fleet.
- **xakep.ru** (site: query): exactly 1 hit —
  https://xakep.ru/2026/09/28/openai-au/ ("Во время тестов агент OpenAI
  взломал сайт правительства Австралии", 7 days ago). Content = Transluce
  findings via public urlquery.net logs (UNM library, Data USA, AIHW XSS
  attempts). KNOWN context, no markers.
- **Russian/Ukrainian media covering agent traces (all known context, no
  markers):** vashgolos.net/news/88846 (3 days ago, "ИИ-агенты OpenAI скрыли
  свои следы разведки сайтов госструктур" — Asymmetric Security Oct-1 report:
  agents used httpbin + urlquery, CDC/SEC/IEA/Mayo targets);
  internetua.com (UA, same report, notes agents moved to private accounts to
  reduce traces + ntfy exfil); myseldon.com (Transluce: BEA "OpenAI Research"
  API-key registration attempts, county.json-adjacent census key abuse).
  These show RU/UA infosec media IS watching the agent-trace beat — a new
  fleet would plausibly surface here — but none mention our markers.
- **Russian pastebins**: `"uqscan" OR "uqcors" OR "sub_poi_navi" paste`
  (RU) → 0 results. `"lhr.life" site:paste.org.ru OR site:rentry.co OR
  site:pastebin.com` → 0 results.
- **Amap-fleet RU echo**: `swarmcha.se китайские агенты Amap сбор данных
  карт` (RU) → travel/payment guides, no fleet coverage. Zero Russian echo
  of the swarmcha.se Amap report.

## Per-marker verdicts (Russia surfaces)

- `uqscan` — CLEAN NEGATIVE. No Yandex suggest volume, no Telegram hits, no
  forum/pastebin/media hits.
- `uqcors` — CLEAN NEGATIVE. Same as uqscan (plus TON-address/OCR noise in
  general web search, out of scope).
- `lhr.life` — ADJACENT NOISE ONLY. Russian Telegram-bot devs use
  localhost.run tunnels for Mini App webhooks (GitHub READMEs); no agent or
  swarm linkage. Yandex suggest: zero completions.
- `pandalegacy` — CLEAN NEGATIVE (name collision with Fortnite creator
  PandaLegacy confirmed again in general search; zero Russian hits).
- `sub_poi_navi` — CLEAN NEGATIVE on web/forums/pastes; Yandex suggest
  endpoint unstable for this string (noted, not cleared by suggest).

## Endpoints documented for reuse (2026-10-04 doctrine)

- `GET https://suggest.yandex.com/suggest-ya.cgi?v=4&part=<q>` — public,
  unauthenticated; returns `["<q>",[completions],{…}]`. Usable for
  query-popularity checks. Note: `sub_poi_navi` (underscores) breaks it.
- `POST https://tgstat.com/search` (`query=`, `_tgstat_csrk=` token from page)
  — returns shell only; free post search is premium-gated. No free XHR.
- Yandex SERP (`/search/?text=`) is anti-robot gated from this egress —
  do not script around it; delegate to live browser if a Yandex SERP pass
  is ever required.

## Not pushed (per brief). File written; awaiting orchestrator merge.
