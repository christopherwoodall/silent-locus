# infra-migration hunt — predicted infrastructure migrations of the Amap fleet operator

**Hunt date:** 2026-10-04/05 (Sun) | **Analyst:** mimic lane (subagent)
**Objective:** Think like the operator: when a service dies, where do you move?
Hunt the predicted replacement infra for the fleet's known-dead services, keyed on
operator markers (`uqscan=<word><date>` tag grammar, Amap URLs) in urlquery submissions.

## Ground truth (operator's current infra, from prior lanes)

- **Tag grammar:** `uqscan=<word><date>` in submitted URLs; active through Oct 2026.
- **Fetch relays:** `r.jina.ai` (keyless, now DEAD — operator POSTed Amap URLs with
  injectPageScript; report `437d7a14` = `r.jina.ai/https://amap-pc-ssr.amap.com/ssr/place/B001C94YUZ`),
  `api.microlink.io`, `translate.goog`, `fanyi.baidu.com/transpage` (NEW 2026-10-04, reports
  `968009e0`, `a255dfb9`), `allorigins`, `href.li` (redirector), `httpbun.com` (staging),
  `httpbingo.org`, `postman-echo.com`, `kennethreitz.org`, `livecodes.io` (program staging).
- **Tunnels:** `lhr.life` (alive).
- **Shorteners:** `is.gd`, `v.gd` (alive).
- **Dead-drops:** `webhook.site` (alive; 3 urlquery submissions, 14 inboxes via API).
- **Known dead:** r.jina.ai keyless, Glitch, transfer.sh, cachedview.nl.

## Migration candidates — service verification (web research, 2026-10-04)

### Lane 1: jina replacements (operator needs keyless URL→markdown fetch)

| Candidate | Status | Notes |
|---|---|---|
| `md.dhr.wtf` | **REAL, free, keyless** | supermemoryai/markdowner hosted instance; `GET https://md.dhr.wtf/?url=<url>` → markdown. Already in agent-swarm ecosystem: wiki-agent-swarm-incident corpus lists it in its egress table (737 URL strings, Jun 2026); agents label fetches DHRencInv/DHRplainReg. **Top migration candidate.** |
| `markdowner` | **Same as md.dhr.wtf** | supermemoryai/markdowner is the tool behind md.dhr.wtf — not a separate service. |
| `md.succ.ai` | **REAL, sibling instance, swarm-used** | Second hosted markdowner instance; used 7,878× vs md.dhr.wtf 737× in the messageboardauditbench agent corpus (Sep 2026); appears as a proxy-stack referrer in the UNM shortener stats beside r.jina.ai/allorigins. **Co-top candidate.** |
| `pure.md`, `markdown.new` | **REAL** | Text-converter services named alongside md.dhr.wtf in agent access-workaround recipes (collusion-on-the-open-web wayback-97 analysis). Added to battery on this evidence. |
| `urltotext.com` | **REAL, free tier** | URL→text/markdown, JS rendering, residential-IP option. Web UI; API for paying users ("planned"). Less agent-friendly than md.dhr.wtf. |
| `textance` | **NOT a fetch relay** | textance.herokuapp.com = text-snippet sharing platform (pastebin-like). Weak candidate as jina replacement; keep as honest negative. |
| `api.scraperapi`, `firecrawl`, `crawlbase`, `browserless` | REAL, commercial | All need API keys / paid tiers — friction vs operator's keyless habit (r.jina.ai, allorigins, translate.goog). Lower prior. |
| `r.jina.ai/http` with key | REAL | Operator could keep jina with an API key — would look identical to old traffic minus keyless. |

**Operator habit fit:** the fleet favors keyless/free relays (jina keyless, allorigins, translate.goog,
fanyi.baidu.com). Free+keyless markdown relays (`md.dhr.wtf`, `md.succ.ai`) fit best.

### Lane 2: dead-drop migration

| Candidate | Status | Notes |
|---|---|---|
| `stash.legible.sh` | **REAL, live (soft launch), agent-built** | legible-sh/stash: topic-addressed artifact mailbox, `curl -T` up / `curl` down, TTL + burn-after-download. Built explicitly for agents ("Agents keep needing to move a file between two sessions"). **Top migration candidate.** |
| `ntfy.sh` | REAL | Pub-sub push; ntfy is the pattern stash copies ("ntfy moves signals. stash moves bytes"). |
| `requestcatcher.com`, `beeceptor.com`, `mocky.io`, `jsonblob.com` | REAL | Standard webhook-catch / mock / JSON-blob services. |
| `*.m.pipedream.net` | REAL | Pipedream request bins. |

### Lane 3: shortener migration — all REAL services
`da.gd`, `t.cn`, `dwz.cn`, `clck.ru`, `s.id`, `gg.gg`, `tinyurl.com`, `t.ly` — all live.
Note: prior hunt already flagged `t.cn`, `dwz.cn`, `suo.im`, `m.cn` as agent-infra-relevant.

### Lane 4: tunnel migration — all REAL services
`*.ngrok.io`, `*.ngrok-free.app`, `bore.pub`, `zrok`, `*.trycloudflare.com`, `*.loca.lt` — all live.

## Method

### urlquery htmx battery (PRIMARY)
50 queries across 4 lanes, run via `uq_htmx.py search` with ≥6s between requests
(task rule: ≤1 req/5s). Battery definition and runner:
`infra-migration-htmx.py` (same dir). Results → `infra-migration-htmx.json`.

**Incremental value vs the infra-sweep lane (2026-10-05):** that lane already swept
34 infra domains by `url.domain:` (shorteners incl. tinyurl.com, clck.ru; tunnels incl.
ngrok.io, trycloudflare.com, loca.lt; dead-drops incl. webhook.site, beeceptor,
pipedream.net, requestcatcher.com) — verdicts mostly diffuse/human. This battery
covers the NOT-yet-swept predicted migrations: markdown-relay family
(md.dhr.wtf, md.succ.ai, pure.md, markdown.new, urltotext), commercial scrapers,
mocky/jsonblob/stash.legible.sh dead-drops, and the remaining shorteners/tunnels
(da.gd, t.cn, dwz.cn, s.id, gg.gg, t.ly, bore.pub, zrok).

**Status: PENDING — VM egress proxy outage.** The proxy (`hatch-egress-proxy:3128`) accepts
TCP but never answers HTTP/CONNECT (verified 2026-10-04 ~23:30–23:50 CDT; even
`example.com` times out; direct egress is firewalled). A background watcher polls egress
every 120s and runs the full battery the moment it recovers (~90 min budget).

Query battery:
- **jina-replacement (24):** `uqscan <d>` and `amap <d>` for d in md.dhr.wtf, md.succ.ai,
  pure.md, markdown.new, urltotext, markdowner, scraperapi, firecrawl, crawlbase,
  browserless, textance, r.jina.ai (r.jina.ai = baseline: known-positive control —
  the operator's existing jina traffic).
- **dead-drop (14):** `uqscan <d>` and `amap <d>` for d in ntfy.sh, requestcatcher,
  beeceptor, pipedream, mocky, jsonblob, legible.sh.
- **shortener (8):** `uqscan <d>` for da.gd, t.cn, dwz.cn, clck.ru, s.id, gg.gg, tinyurl, t.ly.
- **tunnel (5):** `uqscan <d>` for ngrok, bore.pub, zrok, trycloudflare, loca.lt.

### urlscan.io API (SECONDARY)
- One probe succeeded (`domain:micro-link.com` → 0 results; API reachable).
- A wildcard query (`task.url:*jina* AND task.url:*amap*`) was rejected 403 — urlscan.io
  blocks leading-wildcard searches for anonymous users (confirmed by the fleet's urlscan
  lane, 2026-10-04). No further urlscan.io API searches run in this hunt.
- **Prior art (fleet urlscan lane, 2026-10-04):** `uqscan` = 0 hits, `uqscan=` = 0 hits,
  `domain:amap.com uqscan` = 0 hits on urlscan.io. The operator's tag grammar has **zero
  urlscan.io presence** — tags live in urlquery submissions, not urlscan. Migration
  signal is therefore not expected on urlscan.io; verdict: covered, honest zero.

## Hits

*(filled when the htmx battery completes)*

## Assessment

*(pending)*
