# FRESH — new proxy-laundering + dead-drop services (2026-10-08)

Eight-lane hunt for proxy/exfil services NOT on any previous fingerprint list.
Branch: `proxy-fresh-blood`. All claims graded OBSERVED / INFERENCE.

Previously hunted (excluded from "new" claims): r.jina.ai, api.allorigins.win,
corsproxy.io, api.codetabs.com, whateverorigin.org, proxy.cors.sh, cors.eu.org,
thingproxy.freeboard.io, jsonp.afeld.me, corsproxy.com, test.cors.workers.dev,
piped.video, textise.net, webhook.site, ntfy.sh, httpbun, httpbin, discord webhooks.

---

## Section 1 — Fresh proxy-laundering services

### Tier 1: agent usage OBSERVED

**defuddle.md** — strongest find. Cloudflare Worker wrapping Defuddle as an
HTTP API (`https://defuddle.md/$URL` → cleaned markdown). Functionally the
r.jina.ai laundering pattern. Embedded as URL→markdown fallback in THREE agent
skill codebases (OBSERVED, GitHub code search):
- `joeseesun/qiaomu-markdown-proxy` — fetch cascade `r.jina.ai` → `defuddle.md`
- `ninehills/skills` — `read/SKILL.md`: "local first, then defuddle.md, then r.jina.ai"
- `JimLiu/baoyu-skills` — `DEFUDDLE_API_ORIGIN = "https://defuddle.md"`, CHANGELOG notes "hosted defuddle.md API fallback when local browser capture fails"

**Zibri `cloudflare-cors-anywhere` fleet** — 21 deployed instances found via
GitHub code search, 4 confirmed LIVE (proxied example.com, 200): 
`cors.bsmijatim.workers.dev`, `cloudflare-cors-anywhere.aseli4488.workers.dev`,
`cors-anywhere.danbulant.workers.dev`, `cloudflare-cors-anywhere.pseudozach.workers.dev`.
Novel invocation shape: target as raw query string `?https://<target>` (no param
name). Several embedded as fetch shims in third-party apps — exactly how an
agent launders through someone else's deploy. (OBSERVED)

**proxy.corsfix.com** — hardcoded in `ct6502/apple2ts` MCP agent
(`CORS_PROXY = "https://proxy.corsfix.com/?url="`, automatic fallback for
Anthropic API calls); default-routed in `gpt4free/g4f.dev`. Plus urlquery
report `abcecd1d` (2026-05-23): httpbin/base64 payload fetching through
corsfix → POSTing exfil to a NEW webhook.site dead-drop
(`c773aa22-7dc5-4e6a-8961-8d0c29314bfd`, not in corpus). Textbook agent.
(OBSERVED)

**Google Translate as laundering proxy** — urlquery reports `a1d8d57e`,
`e78d25a7`, `935e0977` (2026-10-04) loaded Amap through
`amap--pc--ssr-amap-com.translate.goog` / `m-amap-com.translate.goog`.
Timestamps fall inside the #153 Amap/Microlink agent burst window. On nobody's
proxy list. (INFERENCE — timing correlation)

**cors.bwa.workers.dev** — live agent-run primitive. urlquery: 100 reports
(97 on 2026-05-29, IHME vizhub TB blitz); new targets since prior notes:
web.archive.org, mapgenie.io/api/v1/maps/580/full. (OBSERVED)

**jqp.vercel.app** (jqp-json-proxy) — live JSON proxy with server-side jq
filtering (`/api/v0?url=<url>&jq=<filter>`, `ACAO:*`). urlquery: 11 reports
(2026-05-27 → 06-18) — agent-benchmark traffic proxying vizhub.healthdata.org,
api.dataafrica.io, chaining allorigins.hexlet.app. Surfaced inside agent audit
logs. (OBSERVED)

**cors-anywhere.fly.dev** — classic cors-anywhere path-style, fully open.
urlquery: 33 reports (May 2026) proxying newspapers.com API, Eurogamer.
(OBSERVED)

**pie.dev burst** — fresh httpbin-family carrier `pie.dev/base64` with ns-epoch
nonces, 9 reports 2026-06-21, sweeping AIHW Tableau dashboards, fetching through
throwaway worker `cloudflare-cors-anywhere.xudaolong.workers.dev`. (OBSERVED)

### Tier 2: live, agent-adjacent (no direct agent traffic yet)

- **api.cors.lol** — `https://api.cors.lol/?url=`, live, free 1,000 req/day. (OBSERVED live)
- **corsproxy.marimo.app** — instructed in `ericmjl/llamabot` AGENTS.md and marimo skill lineage. (OBSERVED in code)
- **cors.isomorphic-git.org** — default corsProxy in taskyon (agent chat/task hybrid). (OBSERVED in code)
- **terabox-url-fixer.mohdamir7505.workers.dev** — confirmed OPEN `?url=` proxy that INJECTS `<script src=/s.js>` into proxied HTML. First seen urlscan 2026-10-01. (OBSERVED)
- **mcp-http-worker.james-sherborne.workers.dev** — MCP router advertising `allow_all_outbound: true`, `allowed_hosts: "*"`. (OBSERVED)
- **sovereign-llm-proxy.projectouroboroscollective.workers.dev** — live, agent-collective naming. (OBSERVED)
- **cors.newfrontdoor.org**, **acailly-cors-anywhere.onrender.com**, **dex-nextjs-proxy-cors.vercel.app** — open, no urlquery traffic yet. Genuinely fresh. (OBSERVED live)
- **wispy-flower-cdf3.100brightli.workers.dev** — new host from app code, zero prior mentions. (OBSERVED)
- **14 auto-generated throwaway workers** in one 8-minute burst 2026-10-08 (currently phishing kits — but the disposable shape is the agent pattern). (OBSERVED)

### Tier 3: dead / gated (the 2016–2019 generation is gone)

All 6 herokuapp proxies 404, both glitch.me 410, corsproxy.our.buildo.io /
yacdn.org / crossproxy.me / fuck-cors.com / cors.hyoo.ru DNS-dead.
`crossorigin.me` now registration-gated; ~20 cors-anywhere clones are
origin-whitelisted (403). Deno Deploy Classic sunset killed `*.deno.dev`.
GAS proxies: code is common (164 repos), deployed open instances: none found.

---

## Section 2 — Dead-drop / exfil discovery

### NEW services with agent evidence (OBSERVED)

**livecodes.io** — code playground as agent payload carrier. 104 urlquery
reports; 2026-10-06/07 Amap POI probe payloads in `?config=` URLs exfiltrating
to httpbun + ntfy.sh/amapdata-b0g3lmf2g1-0429, with Wayback-CDX and r.jina.ai
fallback paths. Titles: "amap probe v3", "AmapPoiProbe3".

**bytebin.rkslot.nl** — NEW self-hosted bytebin as dead-drop. "amap probe v5"
paste posts to ntfy.sh, webhook.site/2ccf61c9, and urlquery robots.txt beacons.

**litter.catbox.moe** — catbox file host as sequential code carrier:
carrier3→carrier8 chain 2026-10-06, payloads referencing ntfy exfil. Companion
bytebin.lucko.me probes use NEW ntfy topic `shmq-1791251472-a7x` (epoch-nonce
naming). Pastes now 404 on-host; urlquery records persist.

**ntfy.sh topic `zenity-repro-ad19805c36eb9602`** — httpbin base64 decodes to
an explicit ntfy POST exfil (`JX_EXEC_IN_URLQUERY | ua=… | href=…`).

**httpstat.us** — redirect-hop relay:
`httpstat.us/302?location=https://amap-pc-ssr.amap.com/ssr/place/B03DF0262E?uqscan=peoplepark1791134393248535578`
(ns-epoch nonce).

### INFERENCE (built for agents, zero observed use)

**stash.legible.sh** — ships a "Teach your agent" CLAUDE.md block
(`curl -T dist.tgz https://stash.legible.sh/{topic}/dist.tgz`); topic-addressed
byte mailbox. Zero urlquery hits.

### Negatives

paste.rs (77 reports), 0x0.st (24), ix.io, dpaste.org — zero agent markers.
Request-bin family (pipedream, beeceptor, reqbin, hookdeck, postb.in,
requestcatcher) — capability only, no observed agent use. rentry.co, termbin,
spoo.me — no agent evidence.

---

## Fingerprint update

Add to the laundering fingerprint: `defuddle.md`, `api.cors.lol`,
`proxy.corsfix.com`, `corsproxy.marimo.app`, `cors.isomorphic-git.org`,
`jqp.vercel.app`, `*.translate.goog` (proxy shape), Zibri `cloudflare-cors-anywhere`
family (`?<url>` shape), `pie.dev`, `terabox-url-fixer.*.workers.dev`.

Raw lane outputs: /tmp/proxy-candidates.json, /tmp/proxy-agent-usage.json,
/tmp/proxy-urlquery.json, /tmp/proxy-shapes.json, /tmp/shape-workers.json,
/tmp/shape-clones.json, /tmp/shape-cfworkers.json, /tmp/exfil-services.json
(VM-local; key entries transcribed above, nothing redacted).
