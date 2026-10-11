# RECON scout — network infrastructure lay of the land
Date: 2026-10-03. All keyless, read-only. No host was touched; everything below is from already-indexed data (Shodan host pages, crt.sh CT logs, DNS).

## What was looked at
- **crt.sh** (keyless JSON): `corsproxy.io` (735 certs), `jina.ai` (2,912), `allorigins.win` (240), `oai%` prefix (5,277), several wildcard attempts (crt.sh rejects mid-label `%`; rate-limits aggressively — pace ≤1 query/min).
- **Shodan keyless**: web search is JS-rendered (no results via curl); **host pages are server-rendered** and DO include banners — viable keyless route for known IPs.
- **Censys keyless**: effectively login-walled; not usable without auth.
- IPs resolved via DNS-over-HTTPS (dns.google) for the relay census hosts from joshuadavid-mining.md.

## Interesting hosts (IPs redacted to /24)

### 1. api.cors.lol — self-hosted OPEN CORS proxy (Hetzner, DE)
- IP block 195.201.220.0/24 · Hetzner Online GmbH, Nürnberg · AS24940 · Shodan last seen 2026-10-03.
- **Port 6001/tcp banner**: `HTTP/1.1 200 OK` + `Access-Control-Allow-Origin: *` + `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS` + `uWebSockets: 20`, body 2 bytes. That is a wide-open CORS relay by banner.
- **Port 8000/tcp**: nginx, HTML title `[Vafammoc] Coolify` — self-hosted PaaS panel (Coolify) on the same box.
- Self-signed Traefik default cert (`*.traefik.default` SAN) — Coolify's reverse-proxy fingerprint.
- 480 county.json refs in the corpus (`api.cors.lol` CORS-bypass pattern). This is exactly the "odd proxy" shape: one box, open relay, hobbyist PaaS.

### 2. allorigins.hexlet.app — shadow AllOrigins clone, no Shodan footprint
- IP 83.222.9.53 (single, non-CDN) · **Shodan: "No information available"** — unscanned or very new.
- 4,928 county.json refs (`/raw?url=`) — nearly as many as the official `api.allorigins.win`, making it the #3 relay in the corpus relay census, yet it has zero indexed footprint.
- Official `allorigins.win` CT (240 certs): steady low issuance; subdomains `u.`, `api.`, plus `captain.s.` / `api.s.` (shard-style). No 2026 burst.
- A high-volume agent relay running on infra invisible to Shodan is the standout anomaly of this sweep.

### 3. sec.govwayback.com — typo-squat-shaped domain on Vercel
- IP block 216.150.16.0/24 · org "Vercel, Inc", ISP Amazon.com, AS16509 (Miami).
- Appears in the corpus path-canonicalization probes alongside `sec.gov//files//county.json` variants — shaped like `sec.gov` + `wayback`.
- Banner: `server: Vercel`, `HTTP/1.0 308` → `404`. A parked/undeveloped Vercel deployment. Someone registered the name; nothing serves on it now.

### Also checked
- **proxy.corsfix.com** (143.244.50.0/24, Datacamp Limited AS60068): behind BunnyCDN (`Server: BunnyCDN-LA1-1000`, 403s) — not directly inspectable keyless.
- **jqp.vercel.app** (dominant relay, 45% of county.json refs): Vercel edge IPs — shared infra, no per-host signal.
- **md.succ.ai / platform.lemino.ai / proxymule.com / md.dhr.wtf / webcrawlerapi.com**: all Cloudflare-fronted — Shodan shows only CF edge.
- **vanderbi.lt** shortener note: date-stamped link `maallraw260618` (= 2026-06-18, burst day) — worth its own look, not infra.

## Certificate timing — no stand-up burst
- **corsproxy.io**: 735 certs; 2026 issuance 18/29/19/34/25/25/27/44/5 (Jan–Sep). Steady; no May–Jun spike.
- **jina.ai**: 2,912 certs; 2026 issuance ~38–51/mo Jan–Aug, 10 in Sep (partial month). Steady. Notable subdomains: `*.wolf.jina.ai` (405), `*.docsqa.jina.ai` (186), `*.langchain.jina.ai` (84) — product lines, all routine.
- **allorigins.win**: 240 certs, low steady issuance (2–4/mo).
- **`oai%` prefix (5,277 certs)**: dominated by false positives (`oaim.ie`, `oailton.mat.br`, `oaiyr.com`, `.tk` junk — "oai" inside longer words). **Zero** certs matching oai+agent/proxy/eval/worker/bot/relay/swarm patterns, and **none issued in 2026**. No CT footprint of oai-branded agent/proxy infra this year.
- Verdict: the relay infrastructure is all pre-existing public services — no May–Jun 2026 stand-up timing signal anywhere.

## Surprise find (not infra, but tradecraft)
- Public skill repo `dbx0/skills` ships `skills/recon-osint/reconnaissance/egress-waf-evasion/SKILL.md`, which documents the exact agent relay ladder (direct → archive/scan sources → Shodan/Censys/CT as *passive* sources → proxy rotation) and notes archive.org IP-ban behavior. The tradecraft our hunt tracks is now codified in public agent-facing skill files — worth cross-referencing against our skill-ladders inventory.

## Gaps / follow-ups
- Shodan keyless **search** needs JS; only host pages work via curl. A logged-in Shodan search for `ssl:"proxy"` / `http.title:"CORS"` would go further.
- `allorigins.hexlet.app` deserves a closer look (who operates it; when the domain was registered).
- `sec.govwayback.com` WHOIS/registration date would say whether it predates the June probes.
