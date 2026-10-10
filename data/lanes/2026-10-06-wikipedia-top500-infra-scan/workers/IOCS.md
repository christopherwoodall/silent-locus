# workers/IOCS.md — Wikipedia top-500 infra scan (2026-10-06)

## Surviving IOCs

**None.** All 90 candidate attributions were killed by reviewer-1 on range currency
(see killed-by-review appendix below). There are no IPs in this scan that can be
attributed to any AI provider or datacenter operator with evidence that survives
review. Publishing the 90 candidate IPs as IOCs would be publishing false positives.

## Killed-by-review appendix (the 90 candidates, and why each class died)

The matcher's 90 records (67 distinct IPs) are retained as evidence in
`raw/ip-matches.jsonl` — flagged, not endorsed:

- **62 aws-attributed** (49 IPs, 40 articles, 2020-01-16 → 2023-09-14): KILLED. Every
  underlying CIDR (88.108.0.0/14, 88.104.0.0/15, 88.106.0.0/15, 86.112.0.0/15,
  99.200.0.0/13, 72.242.0.0/15, 182.30.0.0/16) first appeared in the AWS feed
  1–6 years AFTER the edits. Per-IP check against edit-era snapshots: 0/49 in any
  AWS range at edit date.
- **28 azure-attributed** (18 IPs, 16 articles, 2020-04-11 → 2023-01-28): KILLED.
  Every underlying CIDR (172.197.0.0/17, 172.197.128.0/17, 172.195.0.0/16,
  172.193.0.0/17, 172.193.128.0/17, 85.211.0.0/17, 85.211.128.0/17, 85.210.0.0/16)
  first appeared in ServiceTags after the edits. Per-IP check: 0/18 in any Azure
  range at edit date.

Content of the killed set: ordinary human IP editing (mobile edits, vandalism,
reverts, typos). No AI-lab range matched anywhere in 677,635 revisions.

## Candidate leads (unattributed, for future work — not IOCs)

- 61,089 unmatched IP-editor revisions (37,152 distinct IPs): top ranges
  residential/mobile-ISP-shaped — weak inference, unverified per-IP.
- Temp-account revisions (21,922, concentrated 2025–2026): unattributable by IP
  from public data; this is where the agent era lives and this method can't see it.
- Lab egress coverage gap: only 329/73,818 CIDRs are lab-specific (all crawler
  ranges); no published agent-egress ranges for Anthropic/OpenAI; Perplexity
  AWS-hosted with no established company ASN.
