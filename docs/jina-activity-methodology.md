# Scraping jina.ai for agent activity — methodology

Date: 2026-10-21. Status: phase 1 wired into the pipeline (this doc),
phase 2 experimental.

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

## Phase 2 — experimental (not wired; research spike only)

Cache-timing probes. If r.jina.ai caches proxied pages, fetch latency on
a given `r.jina.ai/<url>` can reveal whether someone else fetched it
recently — live activity detection without server logs. Unproven.
Validate cache behavior on our own URLs first; do not claim signal
before that control passes.

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
