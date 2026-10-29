# FINDINGS — Wikipedia top-500 infra scan: matcher (2026-10-06)

## IMPORTANT CAVEAT (read first)
**A datacenter-IP match is NOT proof of AI-agent use.** The CIDR map covers
provider-published ranges (AI labs' crawlers/tool IPs, cloud providers, VPNs,
hosting ASNs). A revision whose editor IP falls in one of these ranges shows
only that the edit came from infrastructure space — it is consistent with a
human on a VPN, a corporate NAT, a misattributed range, or crawler traffic, and
it says nothing about the edit's authorship. Treat every match as a *candidate
lead for further review*, never as attribution.

## Method
- Loaded 73,818 CIDR records from `raw/cidr-provider-map.jsonl`
  (0 skipped as unparsable), grouped by (address family, prefix length).
- Within one prefix length, ranges are aligned networks, hence disjoint except
  for exact duplicates — so each query is a single `bisect` per prefix length,
  tried longest-first. The first containing network is the most specific match;
  if several records share that exact network, all providers/services recorded.
- Query complexity is O(distinct-prefixlens x log n); exact, no walk, no
  truncation. Per-IP results cached across revisions.
- Classification of `user` is strict full-string: `ipaddress.ip_address()`
  success → IP (IPv4 + IPv6); else `^~\d{4}-` → temp account; else named user.

## Volume
- Revision files processed: 489
- Total revisions scanned: 677,635
- IP-editor revisions: 61,179 (9.03%)
- Temp-account revisions: 21,922 (3.24%)
- Named-user revisions: 594,534 (87.74%)
- Distinct editor IP strings seen: 37,152
- IP-editor revisions matching the CIDR map: 90
- IP-editor revisions with NO match (unmatched): 61,089

## Match counts per provider
- aws: 62
- azure: 28

## Match counts per provider/service (top 25)
- aws / AMAZON: 62
- azure / AzureCloud.malaysiasouth: 13
- azure / AzureCloud.mexicocentral: 4
- azure / AzureCloud.uksouth: 4
- azure / AzureCloud.malaysiawest: 3
- azure / AzureCloud.eastus2: 3
- azure / AzureCloud.westus2: 1

## Top unmatched IPv4 /16s
- 82.32.0.0/16: 532
- 77.239.0.0/16: 263
- 185.176.0.0/16: 255
- 82.40.0.0/16: 181
- 96.76.0.0/16: 109
- 74.67.0.0/16: 103
- 64.191.0.0/16: 101
- 111.92.0.0/16: 95
- 182.18.0.0/16: 80
- 116.68.0.0/16: 79
- 223.178.0.0/16: 76
- 125.26.0.0/16: 69
- 142.113.0.0/16: 69
- 64.228.0.0/16: 68
- 148.252.0.0/16: 67

## Top unmatched IPv6 /48s
- 2603:6081:6a03::/48: 192
- 2600:1702:7ec0::/48: 153
- 240d:1a:4b5::/48: 150
- 2405:201:a804::/48: 112
- 2603:7080:8600::/48: 96
- 2001:1388:111::/48: 80
- 240f:7a:6253::/48: 61
- 2600:1001:a010::/48: 60
- 2001:1388:110::/48: 58
- 2a02:8070:e180::/48: 55
- 2607:fea8:e365::/48: 55
- 2001:f40:925::/48: 53
- 2601:8c:4b80::/48: 52
- 2a02:810d:1340::/48: 52
- 2001:569:78ba::/48: 45

## Outputs
- `raw/ip-matches.jsonl` — one record per matched IP-editor revision
  (rank, article, revid, timestamp, ip, providers, services, comment, tags)
- `raw/article-aggregates.tsv` — per-article counts: total/ip/temp/named revisions

## Runtime
Matcher ran in 8.8s (pure local computation, python3 stdlib only).

## Limitations
- Provider names are whatever the upstream CIDR source claimed; overlaps between
  cloud ranges and lab-published tool ranges are both recorded (most-specific
  network wins).
- Temp-account regex `^~\d{4}-` matches MediaWiki's temporary-account grammar;
  IP editors behind masked accounts are not recoverable from this data.
