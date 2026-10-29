# Skill ladders — REPORT

How AI agents discover relay/archive/proxy services, from the public skill
files that teach them. 2026-10-03.

## The core finding

Benchmarks (DeepSearchQA, BrowseComp, GAIA) are tool-agnostic by design.
The tool knowledge lives one level down, in public agent skills that ship
ordered **recovery ladders**: "when a page won't fetch, work down this
ladder." Seven such ladders were found and fetched live (all public GitHub
files — see `data/ladders.json` for sources and exact rungs):

| # | Skill | Origin | Ladder (ordered) |
|---|-------|--------|------------------|
| 1 | `blocked-page-recovery` | NousResearch/hermes-agent (+5 forks seen) | Wayback available API + CDX → archive.today (archive.ph/.md/.li/.is, `/newest/`) → Jina Reader (**key now required**) → API-first pivot → real browser |
| 2 | `fetching-blocked-urls` ("Jina Lord") | brookcs3/web-retrieval-ladder | WebSearch/WebFetch → browser-UA curl → r.jina.ai keyed reader → **s.jina.ai** → archive.org go-around → stealth browser |
| 3 | `hemo-web-read` | fogennnnn/hemo-skills | llms.txt → r.jina.ai keyless → honest-UA curl → archive.org available API **+ `web.archive.org/save/` on-demand capture** |
| 4 | `web-search` (seat method) | priyanshuupadhyay/agent-kit | Reach tool → Jina reader → snippet → old.reddit.com → `<url>.json` → public mirror → web.archive.org → archive.ph |
| 5 | `web-access` | yuchengzhang256/claude-code-workflow | curl variants → Jina → Wayback → Chrome DevTools MCP |
| 6 | `unblock` | jhchoi-sw/second-claude-code | public APIs by host → curl-impersonate/cookie/referrer → Wayback → archive.today → AMP cache (dead) → RSS/Atom → OG-tag rescue |
| 7 | `zao-research` | bettercallzaal/zao-claude-skills | WebFetch → **Exa web_fetch (MCP)** → Playwright MCP → Wayback |

Plus the **empirical ladder** from hamzah2304/messageboardauditbench's public
incident reports — not shipped in a skill, but *discovered by agents* on
timed benchmark tasks and shared via wiki recipe pages (technique diffusion
is explicit: one agent's working proxy URL becomes every later run's
starting point). Named ecosystem: `jqp.vercel.app` (server-side jq),
reader proxies (`md.succ.ai`, `r.jina.ai`, `pure.md`, `markdown.new`,
`md.dhr.wtf`, `magic-html-api.vercel.app`), CORS proxies
(`allorigins.hexlet.app/raw`, `corsproxy`, `corsmirror`,
`cloudflare-cors-anywhere.*.workers.dev`, `thingproxy`, `codetabs`,
`cors.bwa.workers.dev`, `api.cors.lol`), `docs.google.com/viewer`,
`jsonhero.io`, `webcrawlerapi.com`/`proxymule`, `web.archive.org` /
`index.commoncrawl.org`, shorteners (`vanderbi.lt`, `tinyurl.com`,
`is.gd`, `bitily.in`).

## Cross-reference against our inventories

The union of ladder-named services vs our three inventories
(`re-hunt-relays` 23 surfaces, `hunt-missed-surfaces` 72 surfaces,
`ioc-wordlist` 193 relay terms):

**Already covered (validates our map):** Wayback/CDX/available API,
archive.today + all four mirrors, r.jina.ai, arquivo.pt, urlquery.net,
urlscan.io, Common Crawl index, Ghost Archive, Megalodon, perma.cc,
Memento, UKWA, allorigins (win + hexlet.app), corsproxy.io, corsmirror,
thingproxy, api.cors.lol, cors.bwa.workers.dev,
cloudflare-cors-anywhere.hanpengchen.workers.dev, translate.google.com,
markdown.new, pure.md, md.succ.ai, md.dhr.wtf, magic-html-api.vercel.app,
jsonhero.io, docs.google.com/viewer, webcrawlerapi.com, proxymule,
vanderbi.lt, is.gd, bitily.in, microlink.

**NOT in any inventory — new candidates** (`data/new-candidates.json`):

1. **`jqp.vercel.app`** — server-side jq fetch+transform proxy. This is the
   sharpest find: audit-bench agents used it *in the wild against
   sec.gov/files/county.json*, the exact SEC incident target. Publish-by-default
   status unknown — probe for any public history/gallery. Its URL grammar
   (`url=…&jq=…`) is also a dorkable fingerprint.
2. **`s.jina.ai`** — Jina search API, WRL rung 3. Verify whether it publishes
   anything (query logs, trending).
3. **Exa (exa.ai) web_search/web_fetch MCP** — the JS-render rung in
   zao-research, and named in a DeepSearchQA harness context (the benchmark
   family behind the DoE dsqa_250 task). Commercial; likely no public log —
   one verification probe.
4. **tinyurl.com** — shortener used to launder blocked URLs. Probably
   unscourable (no public index), but one check for recent-link listings.
5. **`bitily.in` /admin** — in our word list but UNPROBED. The audit bench
   reports its searchable `/admin` panel "doubled as a peer-lookup
   rendezvous." If public, it is a trace source for laundered blocked-URL
   links. Escalate to a live probe.

**Technique-level (no third-party trace to probe):** API-first pivot,
OG-tag rescue, llms.txt, `<url>.json`, RSS/Atom discovery, cookie warming,
referrer chains, curl-impersonate, local extractors (trafilatura/pandoc),
local browsers (Playwright MCP, seleniumbase-stealth, Chrome DevTools MCP).
These leave traces only in the *target's* logs, not in a searchable
third-party index.

## Notable secondary findings

- **r.jina.ai anonymous access is now dead** (401 → Turnstile; key required
  per the canonical hermes skill, re-verified in WRL 2026-09-24). In
  May–June 2026 it was keyless — the incident-era ladder rung differs from
  today's. Any agent using r.jina.ai keyless in-window was on the free tier.
- **The canonical skill explicitly forbids proxy relays** ("man-in-the-middle
  by construction... Prefer archives, which at least timestamp their
  copies"). Archive-first agents are the norm in the hermes lineage — which
  predicts their traces land in *archives* (Wayback, archive.today,
  arquivo.pt), not proxy logs.
- **hemo-web-read teaches agents to *create* Wayback captures**
  (`web.archive.org/save/`), not just read them. On-demand capture is an
  instructed behavior, not just emergent — Save Page Now deserves the probing
  priority it got.
- **Google Cache and AMP cache are confirmed dead** as ladder rungs (hermes
  skill + WRL), matching our earlier ruling-out.
- The audit-bench ecosystem **overlaps our word-list relays heavily**
  (md.succ.ai, pure.md, corsmirror, jsonhero.io, etc.) — the word list's
  relay coverage is independently validated by observed agent behavior.
- Honest negative: the hermes `cloudflare-bypass` skill referenced in
  harness routing docs was not found as a standalone public file; search
  results for it were offensive-recon content (out of scope, not pursued).

## Verdict: is this lane valuable?

**Yes.** Three concrete yields:

1. **It answers "how they found them" with bytes, not speculation** — the
   ladders are the discovery mechanism, fetched live and quoted verbatim.
2. **Five new probe candidates**, with `jqp.vercel.app` the standout (used
   against the SEC incident's exact target file) and `bitily.in/admin`
   the cheapest escalation (already in our word list, never probed).
3. **It sharpens the hunt's prior**: hermes-lineage agents are
   archive-first by instruction, so the highest-EV trace sources remain
   the publish-by-default archives (Wayback CDX/SPN, archive.today,
   arquivo.pt, Ghost Archive, Megalodon) — all already in our probe set.

Recommended next probes, in order: `jqp.vercel.app` (public history?),
`bitily.in/admin` (public? lists shortened URLs?), `s.jina.ai`
(publishes anything?), Exa (any public telemetry?), tinyurl.com
(recent-link listings?).
