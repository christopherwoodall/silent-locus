# HUNT LANE 15 — abuse.ch (URLhaus + MalwareBazaar)
Date: 2026-09-27
Task: query abuse.ch threat-intel APIs for campaign IOCs (305 URLs, 15 domains, 6 file hashes, IP 20.49.140.101).

## Verdict: API BLOCKED — authentication required (not a data negative)

All 46 API queries returned **HTTP 401 Unauthorized**. Since 2025, abuse.ch requires an
`Auth-Key` header on all its APIs (URLhaus, MalwareBazaar, ThreatFox). The key is free from
https://auth.abuse.ch/ but requires creating an abuse.ch account — not done (no-accounts rule).
This lane is fully re-runnable in minutes once a key exists: IOCs are staged at `/tmp/lane15_iocs.json`
and the query script pattern is documented below.

Queries attempted (all 401):
- URLhaus `/v1/host/` × 15: the 13 campaign domains + `r.jina.ai`, `s.jina.ai`
- URLhaus `/v1/url/` × 25: distinctive r.jina.ai-wrapped URLs, sec.gov/files/county.json, example.com-shaped payloads
- MalwareBazaar `/v1/` `get_info` × 6: all 6 gem file SHA-256 hashes

Raw responses: `/tmp/lane15/results.jsonl` (ephemeral). Evidence: five independent analyst docs
confirm the 2025 auth mandate (valitino/osintoolkit, draugr-dev/draugr, muhammedzuhayr/netforensiq,
overwrite00/emlyzer, arbsec/arbitraitor).

## Keyless fallbacks actually checked

1. **URLhaus `csv_recent` bulk feed** (no key; last ~30 days, 14,510 rows, 2.7 MB):
   grepped for all campaign domains, `sec.gov`, `county.json`, `go-import`, `webhook.site`, `oast.online`.
   **Zero campaign hits.** One `webhook.site` row exists but is an unrelated ActiveMQ malware download
   (2026-09-23, reporter "drewfink") — webhook.site is a public request-bin; the URL is user-unique noise.
2. **ThreatFox `export/json/recent`** (no key; 7.8 MB): grepped for the 6 hashes, all domains, the IP,
   and "gemstuffer". **Zero hits.**

Caveat: both feeds cover only the last ~30 days — a May–July campaign would only appear if its
infrastructure is *still* being reported. Historical data sits behind the keyed API.

## Bottom line for the parent

- No evidence for or against campaign presence in abuse.ch: the APIs are a locked door, not a clean room.
- The keyless bulk feeds show **no campaign IOCs in the last 30 days** — the infrastructure is not
  currently being reported there.
- Unblock path: free abuse.ch account → Auth-Key → re-run the 46 queries with the `Auth-Key` header.
  Recommend the parent ask Christopher; 5-minute signup.
- Suggested follow-on once keyed: ThreatFox full IOC search for "gemstuffer" tag + the 6 hashes
  (ThreatFox is IOC-centric and the most likely abuse.ch service to hold campaign entries).
