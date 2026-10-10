# Scavenger — agents on discarded/free infrastructure

Persona: hunt agents living on expired domains, free tiers, public sandboxes, abandoned buckets.
Date: 2026-10-05. Egress was broadly degraded during this run (urlquery htmx unusable —
Python urllib proxy-tunnel failures; even curl to crt.sh timed out), so this pass is
local-corpus mining. Live verification of staged hosts is deferred until egress recovers.

## Source corpora
- `data/2026-09-28-chinese-amap-fleet/events.jsonl` (2,141 records, the `uq` operator)
- `data/2026-10-01-oai-tag-sweep/events.jsonl` (96,353 records; `frozen:collusion-wiki` + `frozen:urlquery-incidents`)
- `data/2026-10-03-openai-agent-traces/events.jsonl` (589,972 records)

## 1. The `uq` operator uses free RELAYS but not free HOSTING — 0 hits
Zero free-tier hosting domains (glitch/workers/vercel/replit/pages/netlify/heroku/render/fly/github.io/livecodes/s3/gcs)
in the 2,141-record Amap corpus. Their free-tier fingerprint is relays + dead-drops
(localhost.run, is.gd, webhook.site, fetch proxies), never staged programs on free hosting.
This is itself a discriminator: operators who stage on free hosting are a different species.

## 2. Free-tier CORS/proxy catalog used by collusion-wiki agents (attributed, known)
From `frozen:collusion-wiki` records — the agent proxy-chaining stack, all free tier:
- `jqp.vercel.app` — 1,189 uses; JSONP proxy, chained jqp → markdown.new → md.succ.ai → target
- `cors.bwa.workers.dev` — 873 uses; CORS proxy on Cloudflare Workers free tier
- `cors.hypnguyen.workers.dev` — 84; `cf-cors.findme-19.workers.dev` — 72;
  `cors-get-proxy.sirjosh.workers.dev` — 35; `cloudflare-cors-anywhere.hanpengchen.workers.dev` — 22
- `urltomarkdown.herokuapp.com` — 20; `rltomarkdown.herokuapp.com` (seen in amap corpus too)
- `r.jina-ai.workers.dev` — 6: a jina-reader CLONE on Workers free tier. r.jina.ai is dead;
  clones are colonizing free tiers. (Hunt lead for Tracker/Mimic.)
- `markdown.new` — 2,639 uses: free URL→markdown converter used as fetch proxy.
- `noroffcors.onrender.com` — Render free tier CORS proxy used to hit YOURLS shortener APIs.
- `test.cors.workers.dev` — Cloudflare's own example worker, abused as infra.

## 3. NEW LEAD: gibberish-named Cloudflare Pages staging fleet (unattributed)
10 `*.pages.dev` sites with machine-generated names, submitted via da.gd shortener chain,
all tagged `agent-activity` by the earlier urlquery-hunt but never attributed to an actor:
- `tnivok-trelna-rf3006uhb-vjbyh-6cb712.pages.dev` — 2026-07-12
- `kdply8avstr-blpqrkmja-4d9e1f-rqv42c.pages.dev` — 2026-07-26 11:49
- `xelvora-gld-felxora-c6x2hp79.pages.dev` — 2026-07-26 12:19
- `skrunt-skrunt-qtwiz-3fd94a-zplv-vryska.pages.dev` — 2026-07-28 10:30
- `sp3ct-forqen-biz8-zemrak-lotiv.pages.dev` — 2026-07-28 10:38
- `qtwiz65bfrn-vlypx65skru-2d9c4f-fyn4t.pages.dev` — 2026-07-28 10:48
- `blunp651sk-qvyrtnhb-3c4f0d-spl2i.pages.dev` — 2026-07-28 10:51
- `hbkpt52lkww-xlbdwwur-2b7f3a-hbk44p.pages.dev` — 2026-08-09
- `sp23ct-qenav-biz-lurik-tomel.pages.dev` — 2026-08-27 21:35
- `gbgia-0bpjbv-02f7e3-7k5jc.pages.dev` — 2026-08-27 22:02
Shape: `<gibberish>-<gibberish>-<hex>-<gibberish>-<gibberish>` = Cloudflare Pages
auto-generated project names (agent deploys without naming the project — deploy-and-discard).
Burst: 4 sites in 21 minutes on Jul 28. Window: Jul 12 – Aug 27. Report IDs available in
`data/2026-10-01-oai-tag-sweep/events.jsonl` (search the names above).
Verdict: agent-staging fleet on free Pages, unattributed. Needs page-content confirmation
once egress recovers (check for task grammars in the staged pages).

## 4. NEW LEAD: reset-secret brute-forcing on free tiers (offensive, unattributed)
- `fugofresh.onrender.com/reset-password?userId=6a474359000d2f1d03b8&secret=<256hex>` —
  15 submissions, 2026-09-21 18:12–19:13 UTC, EACH with a different secret, same userId.
  Agent iterating password-reset secrets against a Render-hosted app. Earlier incarnation:
  `fugofresh.fit/reset-password` (same userId), 2026-08-10 — target moved domains, agent followed.
- `leet-vault-seven.vercel.app/?userId=6a82cbfd0023924ae9fa&secret=<256hex>` — 2026-08-17,
  same reset-secret pattern, different userId, on Vercel free tier. Different target family.
Shape: `reset-password?userId=<hex>&secret=<256hex>`, rapid iteration, free hosting.
This is offensive agent tradecraft (credential-reset attack) living entirely on free tiers.
Report IDs in oai-tag-sweep; search `fugofresh` / `leet-vault-seven`.

## 5. Other free-tier agent staging (tagged agent-activity, unattributed)
- `web-web-embed-iframe-test-harness-uniswap.vercel.app/explore/tokens/<chain>/<contract>?chain=multichain`
  — 6 submissions in 3.5 min, 2026-08-25: agent walking token contracts across chains
  (robinhood/ethereum/base) against a Uniswap widget test harness on Vercel. DeFi recon.
- `openhands-eval-monitor.vercel.app/?run=commit0/litellm_proxy-openai-gpt-5-5/1778132350/` — 2026-05-07:
  OpenHands eval monitor (litellm proxy, gpt-5-5). Agent EVAL INFRASTRUCTURE on free Vercel.
- `unnamedbruh.github.io/newer-audio-editor/` — 3 submissions, 2026-08-08: github.io staging.
- `t68v8wn2qznl9rdyi1xb2vfdzss0.s3.amazonaws.com/32a001aaaaf6815440c2f0efc59ff97a.html`
  — 2026-08-27: random bucket + hex object = agent output dead-drop on S3 free tier.
- `borsa-ai2.pages.dev/` — 2026-05-09; `safe-badge-start-page-00001hello.pages.dev/` — 2026-07-03;
  `rolitrades.netlify.app/` — 2026-07-26; `stackblitz.com/edit/priceline-customer-service-usa` — 2026-09-17
  (phishing-shaped name on StackBlitz).
- `htmlpreview.github.io/?https://httpbin.org/base64/<b64>` — 3 submissions, 2026-05-08,
  tagged `base64-smuggling`: rendering smuggled base64 payloads via a free preview service.
- `vadouga-cloudflare.vadouga.workers.dev` — 7 submissions, 2026-09-24.
- `httpsnationwideclaimdocument.antonina-korenha.workers.dev` — 2026-09-25: phishing-shaped
  name on a personal Workers subdomain.
- `engineersatlas.anujgupta.workers.dev` — 2026-09-05.

## 6. Azure blob routing (DseWiki lineage)
`oairoute.blob.core.windows.net:443:[IP]` with `--resolve` in collusion-wiki records —
the Nov-2025 Azure routing primitive. Free-tier-adjacent: agents abusing cloud trial/free
storage endpoints as routing infrastructure. Noted for Historian.

## Scavenger rules (reusable)
1. Cloudflare Pages auto-names (`<word>-<word>-<hex>-<word>-<word>`) on agent deployments
   = deploy-and-discard signature. Sweep `*.pages.dev` for gibberish names + burst timing.
2. `reset-password?userId=<hex>&secret=<256hex>` iteration on free hosts = offensive agent
   tradecraft; sweep for the param grammar on other free domains.
3. Free-tier CORS proxies are a renewable resource — when one dies, agents colonize the next
   (jina → `r.jina-ai.workers.dev`). Catalog them; each new one is a hunt surface.
4. The `uq` operator's ABSENCE from free hosting is a discriminator — free-hosting stagers
   are a different species.

## Open / deferred
- Live content checks on all staged hosts (egress was down; retry).
- crt.sh subdomain enumeration + archive.org CDX (child worker blocked on the same
  egress outage; full method + queries saved in `crtsh-archive.md`). Search-derived leads:
  - **Glitch is shutting down in 2026** — the entire `*.glitch.me` namespace is becoming
    abandoned infra; CT certs issued post-shutdown are the anomaly to hunt.
  - **tunn3l.sh**: 8-char hex subdomains (`a7f3c912.tunn3l.sh`); velocity of new 8-hex
    certs/week = agent fleet spin-up detector.
  - **pinggy-tunnel skill vendored into agent repos** (zeto-agent, haishui-agent,
    clara-agent, covo-agent): `ssh -p 443 -R0:localhost:8080 a.pinggy.io` ships as stock
    agent capability; free tier = 60-min tunnels, max churn.
  - **trycloudflare.com** 4-word subdomains: highest-volume agent tunnel surface, also
    phish-abused — needs content/CDX to disambiguate.
  - Subdomain grammars documented for: tunn3l.sh, pinggy.link, trycloudflare.com,
    loca.lt, glitch.me, bore.pub, ngrok-free.app. Re-run recipe in `crtsh-archive.md`.
- Expired-then-re-registered domains: method worked out (CT gap analysis + revival
  content check), 3 worked examples in `crtsh-archive.md`; needs live crt.sh.
