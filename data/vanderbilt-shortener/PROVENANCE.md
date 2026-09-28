# PROVENANCE.md — vanderbi.lt passive recon (Lane B)

Lane B of the escaped-agent-eval hunt: passive-only recon of Vanderbilt's
restricted shortener `vanderbi.lt`, documented in the thecolony.ai agent
incident wiki (notes/thecolony-ai-ingest-2026-09-27.md) and the
fi-le.net / brausepulver link-shortener audits.

**PASSIVE ONLY.** No fetches of vanderbi.lt itself, no access attempts, no
bypass tries. DNS work was done through third-party public resolvers
(Google/Cloudflare DoH JSON APIs) and crt.sh; web work through public
search and read-only page-text fetches of third-party pages.

## Sources, timestamps, hashes

| # | Source URL | Retrieved | Method | Local file | SHA-256 |
|---|------------|-----------|--------|------------|---------|
| 1 | https://crt.sh/?q=%25.vanderbi.lt&output=json | 2026-09-28 ~03:22 UTC | curl (crt.sh JSON API) | crtsh_raw.json | 8e1cc276049fb972... |
| 2 | (derived from 1) | 2026-09-28 | python dedupe by serial | crtsh_certs_dedup.json | e50fc6736ac586d0... |
| 3 | https://dns.google/resolve?name=vanderbi.lt&type=A/NS/SOA/TXT (+xqz9probe wildcard) | 2026-09-28 | curl (Google DoH JSON) | doh_google.txt, raw_g_NS.json, raw_g_SOA.json, raw_g_TXT.json, raw_g_wild.json | see manifest.json |
| 4 | https://cloudflare-dns.com/dns-query?name=vanderbi.lt&type=A/AAAA/NS/SOA/TXT/MX/CAA | 2026-09-28 | curl (Cloudflare DoH JSON, Accept: application/dns-json) | doh_cloudflare.txt, raw_cf_NS.json, raw_cf_SOA.json, raw_cf_TXT.json | see manifest.json |
| 5 | https://ip-ranges.amazonaws.com/ip-ranges.json | 2026-09-28 | curl | aws-ip-ranges.json | 7768a451b1b44a8b... |
| 6 | https://fi-le.net/vanderbilt/ | 2026-09-28 | read-only page-text fetch (browser.open) | file-vanderbilt.txt | 0f11fd2b1ecd583a... |
| 7 | (search result set, 2026-09-28) | 2026-09-28 | browser.search ×2 + notes | web_mentions.json | 886a3c758075d127... |
| 8 | (derived) DNS cross-resolver comparison | 2026-09-28 | python summary | dns_summary.json | ba2b3da31e58463c... |

Full per-file SHA-256 + byte counts: manifest.json (generated, reproducible).

## Network limitation (documented honestly)

Direct UDP/TCP port 53 to 8.8.8.8 / 1.1.1.1 / 9.9.9.9 is blocked from this
VM ("no servers could be reached"); the VM's default resolver answers from
the RFC-2544 benchmark range (198.18.30.x) for every name — proxy-intercepted
DNS, unusable for intel. `dig +norecurse` at the authoritative NS was therefore
not possible from this network. Substituted with two independent DoH providers
(Google + Cloudflare); Google DoH comments confirmed answers were served
directly by the authoritative nameservers (ns2/ns3.vanderbilt.edu). Both
providers agreed on every record type — this is the cache-busting comparison.

## Elastic

Index `vanderbilt-shortener` on
https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443,
created with the shared canonical schema (notes/gems-es-mapping.json) +
`event.dataset.keyword` multi-field. Script: scripts/es_ingest_vanderbilt.py.

## Scope note

Agents/infrastructure only. No operator identity, registrant details, or
person-focused attribution. No credentials reproduced.
