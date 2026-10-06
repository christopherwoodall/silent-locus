# RANGE-CURATOR — provider IP-range map findings

Event: `data/2026-10-06-wikipedia-top500-infra-scan/`
Worktree branch: `wikipedia-top500-infra-scan-2026-10-06`
Date of curation: 2026-10-06 (all retrieval times UTC)

Deliverables:
- `data/2026-10-06-wikipedia-top500-infra-scan/raw/cidr-provider-map.jsonl` — 73,818 records,
  one JSON object per CIDR: `{cidr, provider, service, source, retrieved, [broader_claims], [also_reported_by]}`
- Builder script: `workers/range-curator/build_cidr_map.py` (reproducible, re-runnable)
- Source caches: all in `raw/`, listed below with retrieval timestamps (15:41–15:52 CDT = 20:41–20:52Z)

## Retrieval log (all via curl, ≤1 req/5s per methodology §pacing)

| # | Source file (raw/) | Origin URL | Status / time | Notes |
|---|--------------------|-----------|---------------|-------|
| 1 | `aws-ip-ranges.json` | https://ip-ranges.amazonaws.com/ip-ranges.json | 200, 2.70 MB, 20:41Z | `createDate` in payload is the file's own version stamp |
| 2 | `gcp-cloud.json` | https://www.gstatic.com/ipranges/cloud.json | 200, 113 KB, 20:41Z | `creationTime` field in payload |
| 3 | `azure-servicetags.json` | resolved LIVE from https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519 | 200, 4.33 MB, 20:42Z | confirmation page (which redirects to details.aspx) linked `https://download.microsoft.com/download/7/1/d/71d86715-5596-4529-9b13-da13a5de5b63/ServiceTags_Public_20261005.json` — **current weekly file dated 2026-10-05**, `changeNumber: 421`. Resolved at ~15:41 CDT, no stale copy substituted |
| 4 | `openai-chatgpt-user.json` | https://openai.com/chatgpt-user.json | 200, 20:43Z | official OpenAI-published; payload `creationTime: 2026-09-25` |
| 5 | `openai-searchbot.json` | https://openai.com/searchbot.json | 200, 20:43Z | official; payload `creationTime: 2026-01-02` |
| 6 | `openai-gptbot.json` | https://openai.com/gptbot.json | 200, 20:43Z | official; payload `creationTime: 2026-09-22` |
| 7 | `anthropic-bots.json` | https://claude.com/crawling/bots.json | 200, 20:43Z | official; payload `creationTime: 2026-10-02` |
| 8 | `anthropic-ip-addresses.md` | https://platform.claude.com/docs/en/api/ip-addresses.md | 200, 20:43Z | official docs page; inbound `160.79.104.0/23` + `2607:6bc0::/48`, outbound tool-call `160.79.104.0/21`, plus 5 phased-out GCP `/32`s |
| 9 | `perplexity-perplexitybot.json` | https://www.perplexity.ai/perplexitybot.json | 200, 20:43Z | official; payload `creationTime: 2025-02-07` (stale, ~20 mo old — flagged in gaps) |
| 10 | `perplexity-user.json` | https://www.perplexity.ai/perplexity-user.json | 200, 20:43Z | official; payload `creationTime: 2025-10-17` |

## Per-provider counts (from built map; exact-deduped, see §Dedup)

| Provider | CIDR records | IPv4 addresses (summed) | IPv6 records | Source feeds |
|----------|-------------:|------------------------:|-------------:|--------------|
| azure | 61,098 | 104,868,614 | 16,905 | azure-servicetags.json (447 service tags) |
| aws | 11,284 | 102,503,544 | 3,462 | aws-ip-ranges.json (22 services; top: AMAZON 9,217, ROUTE53_RESOLVER 638) |
| gcp | 1,107 | 19,216,256 | 95 | gcp-cloud.json (48 scopes) |
| openai | 281 | 40,928 | 0 | 3 official feeds (chatgpt-user 230, searchbot 39, gptbot 18 — overlapping feeds) |
| anthropic | 36 | 3,691 | 1 | bots.json (28) + docs page (3 current + 5 phased-out marked) |
| perplexity | 12 | 32 | 0 | perplexitybot.json (8, stale) + perplexity-user.json (4) |
| **Total** | **73,818** | — | — | — |

Note: IPv4 address sums double-count nested records (e.g. Anthropic inbound `/23` ⊂ outbound `/21`; OpenAI `/28`s ⊂ Azure). Treat sums as "claim volume", not unique address counts.

## Gaps and clean negatives

1. **No Azure gap** — resolved the current weekly file live (20261005, `changeNumber: 421`).
   Documented above so it can be re-resolved next week.
2. **Perplexity company ASN: NOT established (gap).** whois port-43 and Team Cymru DNS
   lookups fail on this VM (egress returns empty), and no authoritative Perplexity ASN
   surfaced in web search. OBSERVED instead: **all 12 Perplexity published egress IPs sit
   inside AWS ranges** (e.g. `44.208.221.197/32`, `34.193.163.52/32`, `18.97.21.0/30` ⊂
   AWS blocks), and Cloudflare's 2025 reporting notes Perplexity rotates across ASNs.
   So ASN-level attribution for Perplexity is coarse by construction — recommend treating
   "perplexity" records as the /32-and-/29-published set, with AWS as the host cloud.
3. **Perplexity perplexitybot.json payload is stale** (`creationTime: 2025-02-07`, ~20 months).
   Official source, but old. Flagged, not substituted.
4. **No OpenAI-published IPv6** (all three feeds IPv4-only; openai search found none published).
   Clean negative with sources checked: openai.com/chatgpt-user.json, searchbot.json, gptbot.json.
5. **OpenAI ranges nest entirely inside Azure**: 281/281 OpenAI CIDRs are subnets of Azure
   ServiceTag ranges. Anthropic crawling-bots are spread across clouds: GCP 24, AWS 3, Azure 5.
   (INFERENCE: consistent with OpenAI-on-Azure infra; Anthropic multi-cloud crawl infra.)
6. **Azure ServiceTags overlap each other** (e.g. `AzureCloud.<region>` ⊂ broader tags; AzureMonitor
   alone has 3,168 records). Exact duplicates merged; nested same-cloud records kept — see §Dedup.
7. **Google bot ranges** (Googlebot, etc.) NOT included — task scoped to cloud infra + OpenAI/
   Anthropic/Perplexity. Noted so the coordinator can extend.
8. Fastly/Cloudflare edge ranges not included (same scoping note).

## Dedup policy (as built)

- **Exact duplicates** (same CIDR string, any providers/services) merged into one record with
  `also_reported_by: [{service, source}, ...]`. The primary `provider/service/source` is kept.
- **Nested overlaps** (e.g. OpenAI `/28` ⊂ Azure `/N`) KEPT BOTH: the more specific record
  carries `broader_claims: ["azure/AzureCloud.westus (x.y.z.0/16)", ...]`. Broad cloud records
  are retained because IPs outside provider-published ranges still need attribution.
  Consumers doing attribution should longest-prefix-match; the most specific record wins.

## Honest caveats (read before attributing a Wikipedia edit IP)

1. **Ranges change over time.** These files are a snapshot of 2026-10-06. A Wikipedia
   revision from 2021 whose IP falls inside a 2026 AWS range may have been a completely
   different AWS customer then — re-assignment is routine. Do NOT back-date attributions
   without period-appropriate range data.
2. **A datacenter IP is NOT proof of AI-agent use.** It proves only "this IP was announced
   by cloud provider P at snapshot time". Any human, script, VPN, or legitimate service
   can live in the same ranges. Provider-published *bot* ranges (openai/anthropic/perplexity
   rows) are the narrowest claim: "this IP belongs to provider P's published fetch/crawl
   infra" — still not proof an *agent* made the edit (their web-fetch features do fetch
   pages on user request, but the requester could be anyone).
3. **ASN-level attribution is coarse** for Perplexity (see gap #2); prefer the published
   /32-and-/29 CIDR rows for Perplexity.
4. **Published bot ranges are self-declared and stale-able** (Perplexity's bot feed is
   20 months old; Anthropic's phased-out list is itself evidence feeds drift).
5. IPv6 coverage is partial (OpenAI/Perplexity publish none; Azure/AWS publish plenty).

## Verification done

- All 10 source fetches returned HTTP 200 with non-trivial bodies; sizes sane
  (AWS 2.7 MB, Azure 4.3 MB).
- Every record's CIDR parsed with Python `ipaddress` (invalid → skipped; none skipped).
- Spot-checked: `136.107.176.208/32` (Anthropic bot) ⊂ `136.107.0.0/16` GCP us-east4;
  `160.79.104.0/21` outbound ⊃ `160.79.104.0/23` inbound (expected nesting, kept both).
- JSONL valid: 73,818 lines, one object per line.

**DO NOT COMMIT/PUSH** — coordinator handles git.
