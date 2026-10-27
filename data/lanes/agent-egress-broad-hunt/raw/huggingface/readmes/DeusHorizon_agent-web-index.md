---
license: cc-by-4.0
language: [en]
pretty_name: Agent Web Index
size_categories: [10K<n<100K]
tags: [web, crawlers, robots-txt, ai-agents, llm, measurement]
configs:
  - config_name: default
    data_files: agent-web-index.csv
---

# Agent Web Index — how much of the web can AI assistants actually read?

**50,448 domains measured live. 26% of them cannot be read by at least one of
ChatGPT, Claude, Perplexity or Gemini.** Updated daily. Live index: <https://shop.lumnika.com/ai-readiness/>

Every row here is the result of real HTTP requests, not an estimate and not a re-publication of
someone else's crawl: each domain's homepage is requested once as a browser and once as each of the
published AI crawler user-agents, its `robots.txt`, `llms.txt` and sitemap are read, and the
answers are compared.

## The number that exists nowhere else

`robots.txt` says the crawler may come in — and the server refuses it anyway. You can only see
this by making the request as that crawler, which is why no robots.txt study reports it.

| Crawler | Domains measured | Served | robots.txt says no | Server says no anyway |
|---|---|---|---|---|
| claudebot | 50,448 | 84% | 2,051 | 7,216 |
| gptbot | 50,448 | 85% | 2,605 | 6,879 |
| oai-searchbot | 50,448 | 90% | 794 | 4,748 |
| perplexitybot | 50,448 | 90% | 1,209 | 4,613 |
| meta-externalagent | 41,707 | 89% | 1,163 | 4,205 |
| amazonbot | 41,707 | 85% | 1,265 | 5,602 |
| bytespider | 24,998 | 86% | 666 | 3,249 |
| applebot | 24,998 | 95% | 101 | 1,115 |

Broken down by whoever answers in front of the site (read from the response headers of the same
request: `cf-ray`, `akamai-grn`, `x-amz-cf-id`, `x-fastly-request-id`…). Unit: one domain ×
one crawler, counted only where that site's robots.txt allows that crawler — so every refusal below
contradicts the site's own stated policy, and is almost always an edge default nobody chose.

| Edge in front of the site | Domains | Requests robots.txt allows | Refused anyway |
|---|---|---|---|
| Akamai | 800 | 4,462 | 39% |
| Google | 805 | 5,093 | 33% |
| Sucuri | 78 | 506 | 22% |
| AWS CloudFront | 3,211 | 17,809 | 16% |
| no known edge | 12,871 | 75,414 | 11% |
| Azure Front Door | 314 | 1,639 | 10% |
| Cloudflare | 28,364 | 198,530 | 10% |
| DDoS-Guard | 311 | 1,802 | 10% |
| Fastly | 1,540 | 8,241 | 9% |
| Varnish | 419 | 2,195 | 9% |

`no known edge` is an upper bound, not a vendor: response headers are not kept, so a domain read before a signature was
added to the table stays in that bucket until it is re-requested (a 250-domain sample on 19 Sep 2026: 14% already carry a
signature the current table recognises). A weekly pass re-reads them, so the named vendors above are undercounts.

## Files

| File | What it is |
|---|---|
| `agent-web-index.csv` | one row per domain: score, grade, per-check breakdown, per-crawler verdict, edge vendor, date |
| `aggregate.json` | today's aggregate, exactly as the live index publishes it |
| `daily/<date>.json` | the immutable daily snapshot of the aggregate — this directory is the series |

## Method, and what it does not cover

- One vantage point (Europe), one page per domain (the homepage), 12-second timeout per request.
- Rank-bearing domains come from the [Tranco](https://tranco-list.eu) research list (30-day average
  of five rankings); the rest come from public e-commerce platform seeds.
- `Google-Extended` and `Applebot-Extended` never make requests — they are robots.txt opt-out
  tokens — so for those only robots.txt is reported and no "served" verdict exists.
- Domains that answer with HTTP 429 are excluded from that pass rather than counted as blocking.
- 16,002 measured hosts are infrastructure (CDNs, telemetry, resolvers) rather than
  sites and are counted apart; 22,694 failed to answer and are excluded from every
  percentage.
- Blocking AI crawlers is a legitimate choice, not a failure. This dataset records what is true,
  not what should be.

## Citing

> Agent Web Index, 2026-10-27. 50,448 domains. <https://shop.lumnika.com/ai-readiness/>

Licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — use it, say where it came from.

Audit a single site live, for free, no signup: <https://aivis.lumnika.com/en?src=agentindex#scan>
