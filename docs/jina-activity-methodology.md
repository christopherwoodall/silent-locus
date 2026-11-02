# Scraping jina.ai for agent activity — methodology

Date: 2026-10-21. Status: phase 1 wired into the pipeline (this doc),
phase 2 validated as a one-shot analyst tool (not a monitor).

## What jina.ai is in this hunt

Jina Reader (`https://r.jina.ai/<target-url>`) is a public text-extraction
proxy: it fetches a page server-side and returns clean text/markdown.
Agents use it for access bypass ("Accessing the HF Space directly was
blocked, but using r.jina.ai to proxy the README worked" — terminalbench
trajectory, Nov 2025), origin laundering (the target sees jina's servers,
not the agent's), and scraping behind bot defenses. In the Tencent Cloud
HK fleet (Amap POI scraping, Sep–Oct 2026) jina was one of 7 fetch relays
and the only one that produced results: all 5 successful extractions out
of 2,600+ attempts came via Jina.

Scale in our evidence: 8,521 wiki-corpus lines co-occur with r.jina.ai
alongside fleet indicators (oai tags, epoch nonces, zz labels); 44
distinct inner domains fetched through it; 37 byte-verified proxy uses
in yoonholee/terminalbench-trajectories (10 models x 4 harnesses).

## Hard limit

We cannot read jina's server logs. No public endpoint exposes what other
parties proxy. The methodology below reconstructs *observed* jina use
from third-party records — never total jina use.

## Phase 1 — harvest jina-proxied URL observations (wired)

Every `r.jina.ai/<inner-url>` fetch leaves copies in places we can read.
Each observed copy = one agent fetch event with a timestamp. Strip the
`r.jina.ai/` prefix to recover the inner target; the inner target is the
attribution signal.

| Source | How | What it yields | Pipeline hook |
|---|---|---|---|
| urlquery reports | search `r.jina.ai/` (no target filter); extract inner URL, report timestamp, submitter tags, tag grammar | one observed fetch per hit; submitter tags link to known fleets | `uq_scan_query_families` += relay family `r.jina.ai/` |
| urlscan.io | query `domain:r.jina.ai` | scans of jina-proxied URLs, second corpus independent of urlquery | urlscan query `relay-jina-reader`, LOW cap, PRIMARY |
| Wayback CDX | `url=r.jina.ai/*`, matchType=domain | archived jina fetches with capture timestamps; historical timeline independent of scanners | wayback target `r.jina.ai` (domain) |
| Code in the wild | grep `r.jina.ai` in agent frameworks/skills (narrow GitHub harness lane) | which harnesses hardcode jina as fetch fallback | reposcout / manual; last30days-skill already found this way |

Attribution rule: cluster by inner target class. Amap POI pages = the
Tencent fleet; sec.gov fetches = the wiki-board crowd; `piped.video/api`
chained behind jina = YouTube double-laundering. Cross inner-target
class with the submitter's tag grammar (uqscan=, zz=) to separate
populations sharing one piece of infra — the "same provider, different
agents" problem. Jina is commodity infrastructure, not an operation
signature.

## Phase 2 — validated cache-timing probe (tool, not a monitor)

Result 2026-10-21: r.jina.ai caches proxied pages. The hypothesis holds.

Validation run (15 passive GETs, tiny static origin, full evidence at
`data/lanes/general-hunt/raw/cache-probe/2026-10-21T214823Z/`):

- Cold fetches (n=6): mean 2.40 s.
- Warm re-fetches (n=9): mean 1.53 s.
- Clean split: slowest warm (1.85 s) was still faster than fastest cold
  (2.17 s).
- Warm responses carry an extra `Published Time:` line (47 bytes) that
  cold fetches lack.
- No cache headers to lean on. Cloudflare reports DYNAMIC on all
  fetches. Detection is timing + the Published Time line, not headers.
- Warm state persisted at least 14 minutes.
- Unauthenticated rate ceiling: 20 req/min.

Tool: `scripts/scanners/jina_cache_probe.py`. One-shot analyst use only.

The tool takes one inner target URL and runs N samples (default 3, 15 s
apart). Verdict rules:

- First fetch fast (< 2.0 s) WITH the Published Time marker: WARM. A
  third party proxied the URL recently (within the cache window,
  observed at least 14 minutes). This is the signal.
- First fetch slow (>= 2.0 s) without the marker, later fetches warm:
  COLD at first touch. Nobody proxied it before us; we warmed it.
- Else: INCONCLUSIVE.

Hard rules for use (his call, 2026-10-21):

- Never schedule this. A monitor would poison its own signal: every poll
  warms the URL, so a scheduled check cannot tell "an agent fetched
  this" from "we fetched this while checking".
- One shot per URL, only when there is a reason to test that URL.
- The tool keeps a ledger (`probed_urls.jsonl`) and refuses re-probes
  within 6 hours.
- Repeat samples per URL, not single fetches, to beat network noise.

Honest limits:

- Validated on self-warm only. The mechanism is the same for a third
  party's fetch, but we have not yet caught someone else's warm URL in
  the wild.
- Warm means "proxied within the cache window". Cold means "not within
  the window", nothing more.

Related: hunt open self-hosted reader deployments (Shodan http.html
reader markers; `r.jina-ai.workers.dev` pattern). Some may expose logs
or lack auth. In scope under the reversed Shodan rule (agent infra
only, passive GET, counsel clears hosts before log scraping).

## Known gaps

- Selection bias: we only see agents that touch scanners, archives, or
  public code.
- Wayback coverage on the `r.jina.ai/*` prefix may be thin (baseline run
  will tell).
- Jina key-gated its free tier in late 2025 per public docs; live
  keyless status not re-verified from this environment.

## Sources

- `data/lanes/2026-10-01-intermediary-relays/WRITEUP.md` (relay corpus study)
- `reports/chinese-agent-fleet-findings-2026-10-14.md` (only-successes-via-Jina)
- HF trajectory audit (37 terminalbench uses, Nov 2025)
- skill-tracer v1 (last30days-skill fetch fallback)
