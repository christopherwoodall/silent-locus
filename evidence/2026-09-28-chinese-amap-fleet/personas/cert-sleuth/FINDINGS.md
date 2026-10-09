# FINDINGS — CERT SLEUTH

Started 2026-10-05. Sources: crt.sh (Certificate Transparency) + Shodan existing scan data only.
OPSEC: never connect to candidate hosts; LOG with context, don't fetch.
Raw data: `raw/` (shodan_*.json). Resume from these files.

## Lane 1 — crt.sh sweeps
**2026-10-05: crt.sh UNREACHABLE — their outage, not our egress.** Sequence: 4 attempts TCP-timeout
post-proxy-CONNECT (~07:05 UTC), then consistent `502 Bad Gateway` from crt.sh's nginx (~07:30–07:45 UTC).
Their backend is down. Lane BLOCKED (infra). Retry on later runs; no CT-direct data collected this pass.
Pivoted to Shodan CT-equivalent queries (Shodan indexes SSL certs + page content).

## Lane 2 — Shodan pivots
- `http.html:"httpbun"` → **7 hosts** (raw/shodan_httpbun_html.json).
  - **letss.win cluster (2 pivots: same domain + same service/port on 2 IPs):**
    - 95.169.18.20:8443 — nginx title "Httpbun", hostnames letss.win + 95.169.18.20.16clouds.com; Cluster Logic Inc / IT7 Networks, AS25820. Same box: port 2083 "Ncat http proxy".
    - 207.57.145.214:8443 — nginx title "Httpbun", hostname letss.win; NTT America, AS1054; port 22 OpenSSH.
    - Grade: LEAD — mirror cluster exists (2 pivots met); agent USE unproven. Ncat proxy noted, not probed (opsec).
  - Others: 167.71.138.56:8443+8081 (DigitalOcean, no hostname), 104.199.205.41:11000 + 34.140.48.207:8080 (Google Cloud, no hostname) — cloud-hosted httpbun-likes, no attribution.
- `http.html:"r.jina.ai"` → **19 hosts** (raw/shodan_jina_html.json) — see Lane 3.
- `http.html:"webhook.site"` → **144 hosts** (raw/shodan_webhook_html.json): real infra = Hetzner app03/app04.webhook.site (KNOWN); rest incidental page mentions. One own-webhook subdomain: dev.webhook.id360docaposte.com (OVH) — not agent-evidence.

## Lane 3 — Relay-family census
Known family (from intermediary-relays lane + corpora, all KNOWN):
| relay | tag-sweep hits | fleet hits | Shodan html mentions |
|---|---|---|---|
| allorigins | 7,867 | 0 | (pending) |
| r.jina.ai | 3,166 | 0 | 19 hosts |
| markdown.new | 2,645 | 0 | 0 |
| md.succ.ai | 1,724 | 0 | 0 |
| pure.md | 343 | 0 | — |
| lemino.ai | 47 | 0 | — |
| webhook.site | 0 | 2 | 144 (mostly incidental; real infra Hetzner, KNOWN) |
| corsproxy.io | — | — | 11 (all incidental mentions, no mirrors) |
- `ssl:"jina.ai"` → 4 hosts: 3x Google Cloud (jina.ai's own edge, KNOWN footprint) + 139.45.201.13 (RETN Limited, no hostname — mild lead, single pivot, not chased).

**New jina-reader-like candidates (LEADs, absent from all corpora):**
1. **jina.orz.fit** — 43.153.6.76, Tencent AS132203, :443 Cloudflare-challenged, :80 nginx. Hostname literally "jina" + Shodan page hit for r.jina.ai (2 pivots).
2. **jina.qingchuan.cloud** — 47.84.112.179, Alibaba AS45102, :80 404 / :443 nginx. Same 2 pivots.
3. **relay.woaifei.com** — 43.108.48.133, Alibaba SG AS45102, :80 403 / :443 nginx. "relay" hostname + r.jina.ai page hit.
Grade: LEAD (unconfirmed) — self-hosted jina-reader-likes; agent USE unproven, zero corpus co-occurrence. NOT probed (opsec).

## Lane 4 — Corpus cross-reference
- letss.win / 16clouds.com / 95.169.18.20 / 207.57.145.214: ABSENT all corpora.
- jina.orz.fit / jina.qingchuan.cloud / relay.woaifei.com (+ parent domains orz.fit, qingchuan.cloud, woaifei.com, jellycloud.vip, rollday.site): ABSENT all corpora. IPs likewise 0 hits.
- Known relay family: heavily present in tag-sweep corpus (KNOWN), absent from fleet corpus except webhook.site x2.

## Verdicts
**No GENUINELY NEW agent infrastructure this pass.** Two LEAD clusters banked for future
corpus co-occurrence checks (letss.win httpbun mirror; 3x jina-reader-likes: jina.orz.fit,
jina.qingchuan.cloud, relay.woaifei.com). If any of these domains/IPs appear in future
scan corpora, they upgrade to GENUINELY NEW per the brief's rule.

## Null results
- crt.sh down on their side (TCP timeouts then consistent 502s, 2026-10-05 ~07:05–07:45 UTC). Lane blocked, documented.
- `ssl:httpbun.com`, `ssl.cert.subject.cn:httpbun.com`, `hostname:httpbun.com` → 0 in Shodan (indexing gap or syntax; http.html worked).
- `http.html:"markdown.new"` → 0, `http.html:"md.succ.ai"` → 0 (no third-party mirrors indexed).
- `http.html:"uqscan"` → 0, `http.html:"zz=oai"` → 0 (our markers not in Shodan-indexed pages — expected).
- `http.html:"allorigins"` → 3, `http.html:"corsproxy.io"` → 11 (all incidental mentions, no mirrors).
- `hostname:markdown.new` → 0.

## Tooling note
Fixed a bug in `~/workspace/skills/shodan/bin/shodan.py` slim mode: it popped `data` before
reading services, so `host` always returned an empty services list. Now captures the list first.
(Parent agent separately added retries + 90s timeout — Shodan is flaky from this egress.)
