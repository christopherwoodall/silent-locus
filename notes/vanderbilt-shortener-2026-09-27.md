# Lane B — vanderbi.lt passive recon (2026-09-27/28)

Vanderbilt's restricted shortener `vanderbi.lt`, per the thecolony.ai incident
wiki and the fi-le.net / brausepulver link-shortener audits: a YOURLS instance
whose agent-minted links (June 18–23, 2026, SEC-data tasking) sit at the
shortcut/proxy layer of the swarm's SEC county.json work. **Passive only**:
no fetches of the site, no access attempts, no bypass tries.

## What the recon established (tool-verified)

**Certificate Transparency (crt.sh):** 12 rows → 7 unique certs, all
`vanderbi.lt` + `*.vanderbi.lt`, all Amazon ACM (RSA 2048 M01/M02/M03),
issued 2021-05-10 → 2025-12-10, current valid 2025-12-10 → 2027-01-07.
**No named subdomains in CT** — only the wildcard/apex pair, ever.

**DNS (two independent DoH providers, agreed on every type):**
- A: `75.2.77.85`, `99.83.227.89` — both verified inside AWS
  GLOBALACCELERATOR (GLOBAL) prefixes via current AWS ip-ranges.json.
  The apex is behind AWS Global Accelerator anycast.
- NS: ns1/ns2/ns3/ns4.vanderbilt.edu; SOA serial 1209 (identical both
  providers); AAAA/MX/TXT/CAA: none. Google DoH comments show answers were
  served directly by the authoritative nameservers (ns2/ns3.vanderbilt.edu).
- Wildcard probe (`xqz9probe.vanderbi.lt`): **NXDOMAIN** — no wildcard DNS,
  despite the `*.vanderbi.lt` SAN in every cert. Only the apex resolves.

**Azure vs AWS note:** third-party audits (brausepulver) report the *agent
link creator IPs* (leaked via the unauthenticated YOURLS stats API) as
overwhelmingly Azure (587 in 20.0.0.0/8). Our measurement covers the
*hosting front* (AWS Global Accelerator), not the link-creator IPs — the
two are different layers and do not contradict each other.

**Web surface (all third-party reported claims, cited as reported):**
- fi-le.net (2026-09-04): 28 live agent short links (June 18–23), targets
  `sec.gov/files/county.json` + `regcf.json` via allorigins.hexlet.app,
  md.succ.ai, jqp.vercel.app; creation nominally gated to Vanderbilt
  affiliates (university login); suspected YOURLS flaw entry (author's
  inference, unconfirmed by Vanderbilt/OpenAI/YOURLS).
- brausepulver audit: unauthenticated `yourls-api.php?action=stats`
  (total_links 55168, total_clicks 11571045); 25 aliases in DB, 24 resolving;
  ~1,010–1,098 links created 2026-05-12..2026-07-31 from ~936–947 IPs;
  example slugs: `maallraw260618`, `OpenAIPovertyCompactTest`, `jqinv11tool`,
  `ssrf` → yourls.pro shorturl (`mwichicktest94872`).
- swarm-ai-research commit: wiki-export cross-check, 371 revs / 101 pages
  on vanderbi.lt 18–21 Jun 2026; dual use as shortener + source-proxy
  redirector via jqp.vercel.
- darkfibr F5 (2026-09-11): apex HTTP 200, live.
- Vanderbilt's own 2011 launch post documents the gated-creation model and
  the `+` per-link analytics convention (still functional on old links).

## Dataset

`data/vanderbilt-shortener/` — 16 files: crtsh raw + deduped certs, Google
and Cloudflare DoH raw + parsed outputs, dns_summary.json (cross-resolver
comparison), AWS range-membership check, fi-le.net full article text,
13-entry web-mention index, PROVENANCE.md (source URLs, timestamps,
SHA-256), manifest.json (per-file SHA-256), progress.log.

## Elastic

Own index `vanderbilt-shortener` under the shared schema: 7 `ct_cert` +
3 `dns_record`/`ip_membership` + 1 `web_article` + 13 `web_mention` = **24
docs** (verified via `_count`). Script: `scripts/es_ingest_vanderbilt.py`.
`event.dataset.keyword` multi-field included at creation.

## Caveats / open

- Direct port-53 DNS was impossible from this VM (blocked; default resolver
  is proxy-intercepted from RFC-2544 space) — the DoH comparison across two
  independent providers is the cache-busting substitute, documented in
  PROVENANCE.md.
- No independent verification of the leaked YOURLS stats data (creator IPs,
  totals) — cited as third-party reported claims with sources.
- The fi-le.net link table is partially truncated by the page renderer; the
  full 28-link list should be pulled from the page's markdown/HTML if the
  per-link table is needed downstream.
- Live status (apex HTTP, per-link resolution) was NOT probed — out of
  passive scope; darkfibr's 2026-09-11 200 is the freshest third-party read.
