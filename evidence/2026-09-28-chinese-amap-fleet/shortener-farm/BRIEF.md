# BRIEF — SHORTENER FARM COORDINATOR (durable, respawnable)

## Mission
Find and farm self-hosted URL shorteners with PUBLIC stats pages worldwide. YOURLS proved the concept: public shortener stats pages leak the swarm's proxy stack as referrers and surfaced the Vietnam statistics API task family — a passive operator-side fingerprint and new detection surface.

## Targets (non-exhaustive — discover more)
- **YOURLS** instances (the template: `?stats`, `/public-stats`, admin-ajax leaks)
- **Polr**, **Shlink** (public front enabled), **Kutt**, **liteshort**, **Sinatra-based shorteners**, **ouo.io-likes** — any self-hosted shortener with public analytics
- University/org shorteners (proven: UNM, ETH Zürich leaked the swarm's proxy stack as referrers)
- Government shorteners worldwide (go.id-style, gov.* short domains)

## Method (2 workers max)
- **Worker 1 — DISCOVERY:** Google-dork + certificate-transparency + GitHub code search for YOURLS/Polr/Shlink/Kutt deployments. Dorks like `inurl:yourls "stats"`, `"Powered by YOURLS"`, Shlink default titles, Kutt instances. crt.sh for shortener-shaped subdomains (`go.*`, `s.*`, `t.*`). Log every candidate to `targets.txt` with status.
- **Worker 2 — FARMING:** For each live candidate, pull public stats pages (curl, ≤1 req/5s per host, polite). Extract: shortlink targets, referrers, timestamps, click counts. Flag agent-shaped patterns: proxy-stack referrers (corsproxy/allorigins/jina), machine-cadence clicks, epoch nonces, probe-label grammars. Cross-check hits against OUR corpora (data/2026-09-28-chinese-amap-fleet/events.jsonl, data/2026-10-03-openai-agent-traces/events.jsonl).

## Standing rules
- Passive recon only on restricted instances — never attempt admin access, never brute-force.
- Respect rate limits; one host at a time per worker.
- No commits/pushes.
- Test egress first; if down, pivot to discovery via local sources (crt.sh may also be down — then work the existing target list).
- **Durability:** all state lives here — `targets.txt` (candidate list + status), `hits.jsonl` (agent-shaped hits), `FARM_LOG.md` (what was tried). If interrupted, resume from these files — never redo completed hosts.

## Output
`~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/shortener-farm/FINDINGS.md` — new agent-shaped shortener hits, evidence-graded, all observed URLs appended. Feed confirmed operational infra into `../infra-watchlist/INFRASTRUCTURE-WATCHLIST.md`.
