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

## Closure 2026-09-28 (workstream C)

Naturally small: passive-only recon of one restricted shortener (vanderbi.lt) —
7 crt.sh certs, DNS via two independent DoH providers, AWS range check,
fi-le.net audit, 13 web mentions. N=24 docs is the complete retrievable public
surface; the shortener itself is login-walled and passive-only by lane rule, so
no per-slug stats are pullable. ES `vanderbilt-shortener` _count=24 verified,
schema-drift clean (all fields within the canonical mapping).

## Schema normalization 2026-09-29 (W2)

Built `events.jsonl` (38 rows) from `raw/` on the canonical record schema
(`scripts/validate_schema.py`: 38/38 clean).
- 7 × `venue_finding` — one per deduped crt.sh cert; `@timestamp` =
  cert.not_before; identity `vanderbi.lt|crtsh-cert|<serial_number>`.
- 14 × `venue_probe` — one per (DoH provider, record type) from
  dns_summary.json (google_doh / cloudflare_doh × A/AAAA/MX/TXT/CAA/NS/SOA);
  `@timestamp` = 2026-09-28 retrieval date, `labels.timestamp_source="retrieved_at"`.
- 1 × `venue_probe` — wildcard probe (xqz9probe.vanderbi.lt → NXDOMAIN).
- 2 × `venue_probe` — apex-IP AWS range membership (one per IP).
- 13 × `venue_finding` — web mentions; 12 with no recoverable date use the
  sentinel 1970-01-01T00:00:00Z with
  `labels.timestamp_source="fallback:no_recoverable_date"`.
- 1 × `venue_finding` — fi-le.net researcher audit artifact
  (file-vanderbilt.txt, sha256 carried on the record); identity
  `vanderbi.lt|file-audit|fi-le.net/vanderbilt`.
Fingerprint = sha256 hex of the documented identity string (verified against
the 2023-11-14-hfspace-proxies reference implementation before writing).
SHA256SUMS regenerated (events.jsonl + all raw contents); `sha256sum -c` OK.

## Rollup review 2026-09-29 (W8)

rollup: none — 38 heterogeneous census artifacts (7 certs, 17 DNS probes all at
a single 2026-09-28 retrieval date, 13 web mentions mostly undated/sentinel
1970, 1 audit file) with no time-series, burst, or per-actor structure; a
count summary would add nothing the closure note doesn't already state.

## Ingest script relocated 2026-09-29 (single-collection convention)

`es_ingest_vanderbilt.py` moved from `scripts/es_ingest_vanderbilt.py` into
this collection dir (its single-collection home). It reads only this
collection's `raw/` captures (crtsh_certs_dedup.json, dns_summary.json,
file-vanderbilt.txt, web_mentions.json) and builds ES docs via `base_doc()`;
repo-root paths are resolved from the script's own location, so it runs
unchanged from the repo root:
`python3 data/lanes/2021-05-10-vanderbilt-shortener/raw/scripts/legacy/es_ingest_vanderbilt.py`.
(Root cause: the 2026-09-30 relocation moved the script from the collection
root to `raw/scripts/legacy/` without updating this command; corrected at
Factum ingest 2026-10-09, lane `2021-05-10-vanderbilt-shortener`.)
`scripts/local_es_manifest.json` via_script entry updated to the new path.

CAUTION — superseded output format: the staged `events.jsonl` (38 docs) is the
newer venue-census generation (W8, 2026-09-29: `record_kind` venue_finding /
venue_probe, `cert.*` / `venue.*` labels, sha256-of-identity fingerprints).
This Lane-B script builds the PREVIOUS generation (`record_kind`
ct_cert / dns_record / ip_membership / web_article / web_mention,
`labels.annotated_by="es_ingest_vanderbilt"`, `tags` source:vanderbilt-shortener).
Re-running it via the via_script track would load old-format docs into index
`2021-05-10-vanderbilt-shortener` alongside the staged venue-census docs.
SHA256SUMS regenerated to include the script.

## Historical loader relocation (2026-09-30)

Preserved `es_ingest_vanderbilt.py` at `raw/scripts/legacy/es_ingest_vanderbilt.py` as a historical, optional Elasticsearch loader; it is not an active collection event builder. Its local path resolution now targets the same collection and repository inputs from the archived location. No source evidence, `events.jsonl`, or `rollup.jsonl` was changed; no network or ES actions were run. The SHA256SUMS entry records the relocated script bytes.

## Factum ingest (2026-10-09, lane `2021-05-10-vanderbilt-shortener`)

Ingested into Factum as 21 records (5 sources, 7 artifacts, 1 passive-recon
run, 4 observations, 4 claims), all tagged
`{"lane": "2021-05-10-vanderbilt-shortener"}`; idempotency key
`lane-ingest:2021-05-10-vanderbilt-shortener`. Lane dir moved from
`evidence/` to `data/lanes/2021-05-10-vanderbilt-shortener/`; SHA256SUMS
re-verified OK after the move; legacy dir renamed
`evidence/remove-2021-05-10-vanderbilt-shortener/`. Stale script path in the
CAUTION note corrected (see above). No edges created at ingest (separate
edge pass). The 28 fi-le.net agent-minted alias destinations are truncated
(ellipsis) in the page-text capture — preserved verbatim in the ingest
claim, not promoted to infra.shortcut records.
