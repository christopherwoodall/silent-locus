# THE REGISTRAR — agent infrastructure at the registration layer

**Persona brief:** hunt agent infrastructure at the REGISTRATION layer — domains and certificates.
**Run:** 2026-10-05 ~05:47–06:15 UTC (post-VM-restart).
**Method:** machine-generated domain mining across the three canonical corpora (403 unique hosts), free-hosting/tunnel suffix sweeps, hex-label entropy scan, live urlquery htmx, crt.sh (see outage note). Cross-checked every candidate against the infra watchlist and against our own sets.
**Rules held:** no registrant/WHOIS identity work (agents and infrastructure only). No commits/pushes.

## Egress / tool status

- **crt.sh: DOWN.** HTTP 502 on every endpoint (JSON, HTML, wildcard queries) across ~6 attempts over 30 minutes. The cert-transparency leg is blocked, not negative. Documented for retry — bulk-subdomain issuance checks for tunnel domains and the gibberish pages.dev fleet are still owed.
- **urlquery htmx: up but flaky.** `url.domain:pages.dev uqscan` = 0; `url.domain:pages.dev` claims 42 hits but renders "No reports found" (the known htmx weak-negative documented by the Polyglot). Chunked-encoding IncompleteRead errors on multi-page queries.

## Findings

### 1. The gibberish pages.dev fleet — CONFIRMED + 1 new member (UNKNOWN)

All 10 sites from the Scavenger's report verified present in `data/2026-10-01-oai-tag-sweep/events.jsonl`, plus one new:

| host | observed |
|---|---|
| `yrpkw7grzgo-msvlsi-5z4x8b-yrpks45c.pages.dev` | **NEW** — 2026-05-09, `jina_allorigins_dagd`, report `5bcbc942-f4af-4c1a-86db-27292153c28e` |
| `tnivok-trelna-rf3006uhb-vjbyh-6cb712.pages.dev` | known (scavenger) |
| `kdply8avstr-blpqrkmja-4d9e1f-rqv42c.pages.dev` | known |
| `xelvora-gld-felxora-c6x2hp79.pages.dev` | known |
| `skrunt-skrunt-qtwiz-3fd4a-zplv-vryska.pages.dev` | known |
| `sp3ct-forqen-biz8-zemrak-lotiv.pages.dev` | known |
| `qtwiz65bfrn-vlypx65skru-2d9c4f-fyn4t.pages.dev` | known |
| `blunp651sk-qvyrtnhb-3c4f0d-spl2i.pages.dev` | known |
| `hbkpt52lkww-xlbdwwur-2b7f3a-hbk44p.pages.dev` | known |
| `sp23ct-qenav-biz-lurik-tomel.pages.dev` | known |
| `gbgia-0bpjbv-02f7e3-7k5jc.pages.dev` | known |

**Registration-layer read:** the `<gibberish>-<gibberish>-<hex>-<gibberish>-<gibberish>` shape is Cloudflare Pages' auto-generated project name. An agent deploying without naming the project = deploy-and-discard staging. The May 9 member pushes the fleet window back two months (May → Aug). **11 sites, all unattributed (UNKNOWN).**

### 2. Three more pages.dev hosts — phishing-shaped (UNKNOWN)

- `id-project-acceslogin.pages.dev` (2026-07-03, `cors_conversion_proxy`, report `9dcb31e2-445e-4fa0-bf42-9d1c478b8f2d`) — "acceslogin" = phishing-shaped
- `borsa-ai2.pages.dev` (2026-09-05, shortener-ops-dagd) — "borsa" = Turkish stock market; possible Turkish phishing
- `safe-badge-start-page-00001hello.pages.dev` (2026-09-24, epoch_nonce) — human-named, different actor

### 3. Six free-hosting hosts NOT in the infra watchlist — four are agent CORS infra

- `vercel-cors-proxy.vercel.app` (9 hits) — collusion-wiki agents' CORS proxy → **FOREIGN** (not yet in watchlist)
- `cors-proxy-gray.vercel.app` (4) — collusion-wiki CORS proxy → **FOREIGN**
- `proxy-mu-seven-70.vercel.app` (2) — collusion-wiki CORS proxy → **FOREIGN**
- `cors-bypasser-pro.vercel.app` (1) — collusion-wiki CORS proxy, 2026-06-01 → **FOREIGN**
- `pstorage-acs-6854636.s3.amazonaws.com` (1) — S3 bucket fetched via `r.jina.ai/https://pstorage-acs-6854636.s3.amazonaws.com/...`, 2026-05-12, report `12904e6c-9c1b-4165-976a-a59e660863c0` → **UNKNOWN** (agent laundering an S3-hosted file)
- `d3itvsmwj0r86k.cloudfront.net` (2) — CloudFront image CDN inside an omnes.com affiliate clickref URL, 2026-09-12 → likely **NOISE** (affiliate marketing, not agent ops)

### 4. Already-triaged — not re-claimed

- `amap-nprcusa-primary-vcp-db.postgres.database.azure.com`, `amap-nprcusa-car2x2-cx7-flex-pg...`, `amap-nprcusa-fapcfg-2a588700.wartsila1663840452.zendesk.com` — the urlscan lane already ruled these unrelated Azure-internal name collisions. Left alone.

### 5. Tunnel hosts in the three corpora — nearly absent

`lhr.life`: 2 hits in oai-tag-sweep (`91ef9fc4c82a1b.lhr.life`), 0 in the other two corpora. The tunnel evidence lives in persona raw/reports (tracker, historian, ghost-hunter), not in these three event files. The hex-subdomain tunnel shape (`<16hex>.lhr.life`) is documented there; CT issuance checks for bulk tunnel-subdomain certs are pending the crt.sh recovery.

### 6. Hex-shaped first labels — zero in corpora

No `[0-9a-f]{10,}` first labels among the 403 corpus hosts. Machine-generated names in our sets are the pages.dev auto-names and tunnel hex subdomains (persona-documented), not standalone hex domains.

## Verification summary (ours / known / new)

| candidate | our sets | watchlist | verdict |
|---|---|---|---|
| 11th gibberish pages.dev | oai-tag-sweep ✓ | fleet shape known, this host new | UNKNOWN, new |
| 3 phishing-shaped pages.dev | oai-tag-sweep ✓ | absent | UNKNOWN, new |
| 4 vercel CORS proxies | oai-tag-sweep ✓ (collusion-wiki) | absent | FOREIGN, new |
| pstorage-acs S3 | oai-tag-sweep ✓ | absent | UNKNOWN, new |
| d3itvsmwj0r86k cloudfront | oai-tag-sweep ✓ | absent | NOISE, new |
| amap-nprcusa azure | amap-fleet raw (urlscan lane) | n/a | unrelated (triaged) |

## Pending

1. **crt.sh recovery** — bulk-subdomain issuance for tunnel domains, first-seen dates for the gibberish pages.dev fleet, short-lived cert check on agent staging hosts.
2. Live resolution/liveness of the 4 new pages.dev hosts and the 4 vercel CORS proxies.
3. `pstorage-acs-6854636.s3.amazonaws.com` — bucket listing probe (is it still live? what was the agent pulling?).

## APPENDIX — All observed URLs

### pages.dev fleet (registration layer)
- yrpkw7grzgo-msvlsi-5z4x8b-yrpks45c.pages.dev
- tnivok-trelna-rf3006uhb-vjbyh-6cb712.pages.dev
- kdply8avstr-blpqrkmja-4d9e1f-rqv42c.pages.dev
- xelvora-gld-felxora-c6x2hp79.pages.dev
- skrunt-skrunt-qtwiz-3fd4a-zplv-vryska.pages.dev
- sp3ct-forqen-biz8-zemrak-lotiv.pages.dev
- qtwiz65bfrn-vlypx65skru-2d9c4f-fyn4t.pages.dev
- blunp651sk-qvyrtnhb-3c4f0d-spl2i.pages.dev
- hbkpt52lkww-xlbdwwur-2b7f3a-hbk44p.pages.dev
- sp23ct-qenav-biz-lurik-tomel.pages.dev
- gbgia-0bpjbv-02f7e3-7k5jc.pages.dev
- id-project-acceslogin.pages.dev
- borsa-ai2.pages.dev
- safe-badge-start-page-00001hello.pages.dev

### New free-hosting hosts
- vercel-cors-proxy.vercel.app
- cors-proxy-gray.vercel.app
- proxy-mu-seven-70.vercel.app
- cors-bypasser-pro.vercel.app
- pstorage-acs-6854636.s3.amazonaws.com
- d3itvsmwj0r86k.cloudfront.net

### urlquery report links
- https://urlquery.net/report/5bcbc942-f4af-4c1a-86db-27292153c28e
- https://urlquery.net/report/9dcb31e2-445e-4fa0-bf42-9d1c478b8f2d
- https://urlquery.net/report/12904e6c-9c1b-4165-976a-a59e660863c0

### Triaged (not claimed)
- amap-nprcusa-primary-vcp-db.postgres.database.azure.com
- amap-nprcusa-car2x2-cx7-flex-pg.postgres.database.azure.com
- amap-nprcusa-fapcfg-2a588700.wartsila1663840452.zendesk.com
