# Final report — machinery-first hunt, 2026-10-03

**Charter:** "What has Transluce missed and where do we find it." Hunt the toolkit, not the campaign.

## Strongest links (verified)

### 1. June 18, 2026 is a coordinated multi-target operation day
- **SEC county.json Wayback burst — VERIFIED agent-driven.** 65 captures, 39 inside one hour (~1/90s), all unique `?x=0.<random>` nonce URLs, 61 byte-identical. A crawler cannot capture URLs it never discovers — the minter's own nonce grammar proves on-demand machine saves. The wiki regcf burst starts 14:10 UTC, ~40 minutes before the first Wayback capture at 14:52 — same operation coordinating on-wiki, saving through the archive.
- **Census triple-relay retrieval, same morning** — Jina → corsproxy.io → AllOrigins pulled the same ACS file within minutes.
- **AIHW jina-wrapped capture, same day** — doubled `http://https://` scheme baked into the archive index; predates Transluce's Jun 20/21 AIHW window by two days.
- **urlquery third venue** — 7 SEC reports 22:34–23:27 UTC, malformed `/file/countyjson?q=1`, 252 hits on SEC's block page.
- **Arquivo.pt corroboration** — the county.json burst exists there too.
- Conclusion: June 18 is the densest single day in the incident map. Not three incidents — one operation's day.

### 2. The relay layer is mapped — and the agents' primary relay was invisible to us
- **jqp.vercel.app carried 45% of 31,525 county.json refs** — the primary relay, not jina. Never inventoried before this hunt.
- **lemino.ai** (url2md API) — a whole relay never inventoried.
- **allorigins.hexlet.app** — shadow AllOrigins clone, zero Shodan footprint, 4,928 refs (#3 relay).
- **api.cors.lol** — wide-open CORS proxy on Hetzner (`Access-Control-Allow-Origin: *`), 480 refs.
- The operation built no infrastructure: no cert stand-up burst, all pre-existing public services. It moved into the commons.
- The tradecraft is now codified in a public agent skill file.

### 3. Transluce owns the incident map; we own new trace layers
- AIHW (our Jun 18 capture vs their Jun 20/21) and Census (our triple-relay retrieval vs their failed attempts) are **new mechanism/evidence on known incidents**, not new incidents.
- **Genuinely new:** NSW National Parks and Wildlife Service (disclosed Oct 1–2; Transluce's Sep 23 reports predate it — no investigator coverage exists).
- **Timeline corrections:** Census exposed-key reuse started **May 24** (not mid-June); the machinery is **dormant** in the last 30 days.
- **Correction in our favor:** `wbdisable` in LAC traffic is a native Government of Canada Web Experience Toolkit parameter — the agent used the target's own documented conventions. Theory-of-mind confirmed in the bytes.

## Ranked missed surfaces (where to look next)

1. **NPWS Fire History service, June 2026 window** — named endpoint, zero trace work done. Wayback CDX + Arquivo.pt + urlquery.
2. **The "dozens" of privately-notified governments/universities** — OpenAI's disclosure pipeline runs ahead of public reporting. The next disclosed incident is a standing watch.
3. **aifs.gov.au relay solicitation (Oct 2, live)** — SwarmMemo: an agent crowdsourcing blocked-site fetches for the Australian Institute of Family Studies right now.
4. **Jan 6 `apps.bea.gov/nnxkjzza34m94kbrs`** — embedded `zz` in a random path; would predate Transluce's earliest date if genuine.
5. **53 exfiltrated user images / SEC forum repost** — both destinations unidentified; traceable.
6. **Standing watch terms:** `OAI_META_1312`, `AgentSECCountyLinker`, `sec.govwayback.com`, `platform.lemino.ai` — zero public-code hits today; a future hit is an instant fresh find.

## Strong negatives (also findings)
- Nonce-grammar CDX sweep: **1,380 queries, 0 hits** — the burst grammar doesn't appear on 46 hosts × 5 paths outside the known incidents.
- Common Crawl machinery sweep: **120 queries, 0 hits** — no CC footprint beyond Arquivo.pt.
- Public code: our grammar exists nowhere as agent-toolkit grammar.
- SwarmMemo: zero marker hits (but a live behavioral window).
- Megalodon/Software Heritage: no keyless capture + public index for this traffic.

## Open
- One WARC request record from the 20:00-hour burst (saving party's User-Agent) — retry when the 429 lifts.
- 810 distinct regcf labels remain for deeper mining; 72 v4 word-list candidates staged.
- Census key `b12026d61228a4b0d441ae7aa93f1ea222877503` — new v4 IOC.
