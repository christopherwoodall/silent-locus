# PROVENANCE — lane `urlscan`

## Terms

- **Lane**: a work group in Factum. Records in one lane share the tag `lane`.
- **Factum**: the structured evidence store in `data/`.
- **urlscan.io**: a public web scan service. A scan result page shows what a
  URL returned at scan time.
- **r.jina.ai**: a public reader service. It returns a readable text form of
  a web page.
- **Observable**: a single value in Factum, such as a URL or an IP address.
- **IP address**: a network address for a host. IPv6 is the long form of
  this address. IPv4 is the short form.

## Source

- Scan: urlscan.io result `01a17355-8853-7179-8623-5d2a48a3e0b5`.
- Scan time: 2026-10-25T13:52:41.718Z (from scan metadata).
- Page: `https://r.jina.ai/ec`.
- Page host: `r.jina.ai`.
- Method: urlscan.io anonymous search API, query `domain:r.jina.ai`.
- Retrieved: 2026-10-25T15:00:35Z (from the morning-scan hit file).
- Grade: the scanner gave PRIMARY. The fleet graded the hit LOW and
  SECONDARY. urlscan metadata is SECONDARY by default.
- Claim grades in the records: OBSERVED for the scan facts. The IP
  classification (tier 2, CLOUD_SERVICE, Cloudflare AS13335) is scanner
  output, so it is SECONDARY.

## Files in this lane

- `raw/bundle-20261025T145711Z.original.json`: the original morning-scan
  bundle, copied verbatim. SHA-256:
  `f4c65fe167fcc266134c7d8930a67c7433bb7bc7604d1da34b60a9f59e83193f`.
- `raw/hits-20261025T145711Z.original.jsonl`: the original hit line,
  copied verbatim. SHA-256:
  `90fee9f3786fa1898bbe0dde8d667d6ba1b94a355112f8c199f6623d3c409a4c`.
- `bundle-20261025T145711Z-ingest.json`: the bundle sent to Factum.
  It uses a new idempotency key,
  `urlscan-crawl-2026-10-26/oct25-morning-hit`. It does not reuse the
  original key `swarm-scan/20261025T145711Z`.

## What changed from the original bundle

- The record `ip-0` was removed. See the gap note below.
- One tag was added to the observation `obs-0`. The tag is `ipv6_gap`.
  It states that the IP observable was omitted and that the full IP value
  stays in `tags.ip`.
- No other record changed. Bodies are verbatim. No value was redacted.

## IPv6 gap note (OPEN)

- The original bundle held an observable of type `ipv6` with value
  `2606:4700:20::ac43:4636` (Cloudflare, AS13335, tier 2).
- The installed schema packs reject that type. The command
  `schema assigned observable ipv6` returns:
  `Unknown observable type: ipv6`.
- The installed `factum-web` pack lists only these observable types:
  `url`, `domain`, `hostname`, `ipv4`, `email`.
- The installed `factum-core` pack lists no IP type. Its generic types
  (`term`, `text`) do not describe a network address, so they were not
  used for this IP. A wrong type would hide the gap.
- No corpus record holds an IPv6 observable. A fuzzy text search for the
  full IP value found only short number fragments, not an IPv6 record.
- The full IP value is NOT lost. It stays verbatim in these places:
  the observation tags (`tags.ip`, `tags.ip_asn`, `tags.ip_org`,
  `tags.ip_country`, `tags.ip_city`, `tags.ip_tier`, `tags.ip_label`),
  the raw files in this lane, and the ingest note.
- What is missing: a typed IPv6 observable record for this IP, and a
  typed link from that observable to the observation.
- Fix path: add an `ipv6` observable type through the approved schema
  pack workflow. Do not edit a locked pack in place. Do not hand-edit
  Factum JSONL or SQLite. After a pack adds `ipv6`, submit the omitted
  observable in a new bundle.
- Status: OPEN. Raised to the fleet coordinator as an open item.

## Dedup

- The scan UUID `01a17355-8853-7179-8623-5d2a48a3e0b5` has no corpus
  record. A fuzzy search found only one unrelated record.
- The urlscan result URL has no corpus record (`match --url`:
  `not_found`).
- `r.jina.ai` is known in the corpus from other lanes, but no record
  holds the page `https://r.jina.ai/ec` or this scan.
- The tag `relay-jina-reader` has no exact corpus record. Fuzzy
  searches found only generic jina-reader mentions.
- The sibling batch for 2026-10-26 (result `01a1787e`) was not touched
  and was not re-ingested. It is a different scan.

## Lane note

- This lane dir uses the plain slug `urlscan`. No `data/lanes/urlscan`
  dir existed before this ingest. The tag on every record is
  `urlscan`.
- No commit and no push were made by this ingest worker. The batch
  dir for this ingest was committed by an operator export sweep in
  commit `0c1ef707` during this run. This lane dir itself is still
  uncommitted. The fleet coordinator commits it.
