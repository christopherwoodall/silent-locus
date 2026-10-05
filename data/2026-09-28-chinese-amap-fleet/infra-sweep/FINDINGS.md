# Infra-domain sweep — Findings (2026-10-05)

Flipped approach: instead of keyword-searching, pulled `url.domain:<d>` for 34 infrastructure domains via the htmx endpoint and examined each domain's traffic for swarm shapes (bursts, tag grammars, base64 programs, structured exfil, parallel timing). Raw per-domain JSON in `raw/<domain>.json`; aggregate in `raw/../summary.json`.

## 1. NEW: is.gd is the operator's shortener layer (THE PRIZE)

**81 reports, 2026-06-20/21** — the same burst window as the IDPH Iowa health-data fleet and the lhr.life probe burst. The `uq`-grammar operator was using is.gd as a shortener/redirector layer, previously unknown.

- **Smoking gun**: `is.gd/3JlIp7?uqscan=1781977000` (report `a28ad757`, 2026-06-20T17:27Z) — the `uqscan=` grammar directly on a short link
- **`?x=<19-digit>` params**: `is.gd/mf075827?x=1782075870409744755`, `is.gd/sum074114?x=1782074964000077718` — byte-identical to the lhr.life probe grammar (`?x=<19-digit>`, `?n=<epoch>`)
- **Generated slugs**: `mf075827`, `sum074114`, `kf073634` — `<word><6-digit>` shape, same family as the fleet's `<word><date>` tags
- **Parallel workers**: 3–4 identical submissions of the same short URL within one minute (e.g. `is.gd/eZD1hT` ×3 at 02:59, `is.gd/yPEGdH` ×4 at 02:58)
- **Task label**: `is.gd/AGE115EXTRACT1` (Jun 20) — "EXTRACT" task naming, cf. IDPH's CSV extraction the same week
- Burst structure: 35 reports in hour 2026-06-21T02, 10 in 2026-06-21T20, 7 in 2026-06-20T11

This extends the operator's known infrastructure: lhr.life tunnels (probes) + is.gd (shortener layer) + httpbun (program staging) + jina (fetch proxy) + webhook.site (dead-drops), all in the Jun 20–21 window, three months before the Amap campaign.

## 2. href.li — Amap fleet's redirector chain (known, confirmed)

18 reports, all 2026-10-04: `href.li/?https://amap-pc-ssr.amap.com/...?uqscan=...` — the fleet's known redirector layer, already in the collection. One notable: `href.li/?https://webhook.site/a7753b69-...?run=1791126770493` — the fleet wrapping its *own* webhook dead-drop in href.li (self-laundering the exfil URL). 2 casino-spam hits (playiro.com) are noise.

## 3. Lead (not confirmed): v.gd/MassCountyData007

Single report `29edea0a`, 2026-06-18T18:08Z: `v.gd/MassCountyData007`. "MassCountyData" beside IDPH's Iowa *county* data extraction in the same June window is suggestive of a Massachusetts county-data task family — but it's one report, not an operation. Follow-up: sweep `MassCountyData*` variants and other `v.gd` county labels.

## 4. shorturl.at — human cybercrime, not agents

Base64 blobs in short URLs decode to Turkish spam/phishing emails (`bmRpbml6QGV4aW1iYW5rLmdvdi50cg==` → rndiniz@eyyimbank.gov.tr). Consistent with the frama.link/clck.ru finding: shortener abuse is human phishing, agents use shorteners as *their own* infrastructure (is.gd) rather than abusing public ones.

## 5. Everything else: human noise or clean

| Category | Domains | Verdict |
|---|---|---|
| Shorteners | bit.ly (100), t.co, tinyurl.com, ouo.io (52), clck.ru (61), frama.link (20), t1p.de (14), linkvertise.com (61), v.gd, shorturl.at | No bursts ≥8/hr except is.gd; no tag grammar; max 6/hr diffuse = human submissions |
| Pastebins | pastebin.com (100), dpaste.com, paste.rs, zerobin.net, pastebin.fr, 0x0.st, ix.io, termbin.com | All diffuse, no bursts, no agent shapes. dpaste.com's fleet pastes are keyword-visible, not domain-browsable this way |
| Tunnels | ngrok.io, trycloudflare.com, loca.lt (28), localtunnel.me (5) | Diffuse; one `jipl1.loca.lt/api/v1/` (2023) is old dev traffic. lhr.life's 8/hr uqcors burst already documented in behavior-hunt |
| Dead-drops | webhook.site (20), beeceptor.com (16), pipedream.net (49), requestcatcher.com (7) | Diffuse, no bursts, no structured exfil visible in URLs |

## 6. Methodology caveat

`url.domain:` on the htmx endpoint does **not** match subdomains the way the authenticated API does: `url.domain:r.jina.ai` → 0, but keyword `r.jina.ai` → hits. The fetch-proxy "zeros" (r.jina.ai, translate.goog, fanyi.baidu.com, api.microlink.io) are query-syntax artifacts, **not** real zeros — do not cite them as clean. The shortener/pastebin/tunnel/dead-drop verdicts stand (those are apex domains).

## What this bounds

- The operator's June 2026 infrastructure now has four confirmed layers: **lhr.life** (tunnel/probe) + **is.gd** (shortener) + **httpbun** (program staging) + **jina** (fetch proxy) + **webhook.site** (dead-drop) — a full tradecraft stack, three months before Amap.
- No second operator visible in any of 34 infra domains' traffic. The is.gd burst is the *same* operator (uqscan grammar), not a new one.
- Shortener-abuse and agent-infra are different things: criminals abuse public shorteners (clck.ru, shorturl.at, frama.link); this operator *runs* short links (is.gd) as its own layer.

## Open follow-ups

- is.gd: resolve the short links' targets (where do `mf075827`, `sum074114`, `3JlIp7` point?). Needs live resolution — browser task.
- v.gd/MassCountyData007: sweep county-data label variants.
- `AGE115EXTRACT1`: what is the AGE115 task? Search the label.
- Re-run the fetch-proxy domains with keyword (not url.domain) syntax when quota allows.

Nothing pushed, per instructions.
