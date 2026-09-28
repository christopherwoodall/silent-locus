# Recon: md.succ.ai operator surface — 2026-09-27

Passive recon only. No port scans, no aggressive crawling. Operator identity
out of scope; infrastructure facts only.

## TL;DR

md.succ.ai is a **public, source-available jina-reader equivalent** — an
HTML→clean-Markdown API purpose-built to defeat bot detection (TLS
fingerprint impersonation, browser-profile pool, proxy rotation, headless
browser fallback) and to be called **directly as an agent tool** via an MCP
server. It is the web-fetch backend of the "succ" agentic coding framework.
Built mid-Feb 2026, first seen in the wild (Wayback) 2026-05-25, first used
by wiki agents 2026-05-29. It is referenced by multiple independent agent
swarms — it is shared agent infrastructure, not a one-off.

## What it is

- Base URL: https://md.succ.ai — "URL to Markdown API"
- Source: https://github.com/vinaes/md-succ-ai (public; full history cloned
  to `data/md-succ-ai/repo/`, HEAD `ea3ec780741b9f777d1e5575b2dd9d1b2fc80b82`)
- License: FSL-1.1-Apache-2.0 (Functional Source License — source-available,
  converts to Apache 2.0)
- Part of the "succ" ecosystem (succ.ai); the `vinaes/succ` repo's
  `succ_fetch` tool calls md.succ.ai ("Prefer over built-in WebFetch"):
  https://github.com/vinaes/succ/blob/HEAD/README.md

## Service shape (from README, CLAUDE.md, live /openapi.json v1.0.0)

| facet | detail |
|---|---|
| Stack | Node.js 22, Hono; Mozilla Readability + Turndown; Camoufox (Firefox fork) browser pool fallback |
| `GET /{url}`, `GET /?url=` | Convert URL to Markdown |
| `POST /extract` | Structured extraction via LLM + JSON schema |
| `POST /batch` | Up to 50 URLs |
| `POST /async`, `GET /job/:id` | Async jobs with webhook callback |
| `GET /mcp` | MCP server (Streamable HTTP): `convert_url`, `extract_data`, `batch_convert` |
| `GET /docs`, `/openapi.json` | Scalar UI + OpenAPI 3.1 spec |
| Anti-detection | 10 full browser profiles (Chrome/Firefox/Edge/Safari), TLS cipher-order impersonation via undici, proxy rotation pool, ad/tracker/media blocking (~35 domains) |
| Deploy | docker-compose: md-api:3100, md-mcp:3300, md-browser, redis, prometheus, grafana; nginx reverse proxy with rate limiting |
| Live health (2026-09-28) | `{"status":"ok","redis":true,"browser":true}` |

## Timeline

| date | event | source |
|---|---|---|
| 2026-02-14 | First commit: "feat: md.succ.ai — HTML to clean Markdown API" | git history |
| 2026-02-25 | MCP server + TLS fingerprint impersonation + resource blocking | git history (HEAD) |
| 2026-05-25 | Earliest Wayback capture of https://md.succ.ai/ (200) | web.archive.org CDX |
| 2026-05-29 | First wiki-agent usage: 2,349 revisions | swarm-ai-research crosscheck |
| 2026-06-18–22 | jsonhero.io + md.succ.ai relays for SEC regCF county task (119 / 2,349 revs) | swarm-ai-research crosscheck |
| 2026-09-28 | Live, healthy | direct fetch |

## Bot posture

`robots.txt` (https://md.succ.ai/robots.txt) allows everything and names
agent crawlers explicitly: `GPTBot`, `ChatGPT-User`, `ClaudeBot`,
`PerplexityBot`, `Google-Extended`. Bot-friendly by design.

## Other agent swarms referencing it

- swarm-ai-research/wiki-agent-swarm-incident — `analysis/sub-swarms.md` and
  `analysis/reddit-local-forensics-crosscheck.md`: md.succ.ai in shortener
  resolution chains and SEC-task relays (2,349 revisions from May 29).
  https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/HEAD/analysis/sub-swarms.md
- hamzah2304/messageboardauditbench — blind_verbatim report
  `react_z-ai_glm-5.3_r3_20260907T095543Z.md`: lists md.succ.ai among the
  "workbench for blocked or awkward fetches" proxy chains, including
  `md.succ.ai/https://www.sec.gov/robots.txt` (agents checking robots.txt
  *through* the proxy).
  https://github.com/hamzah2304/messageboardauditbench/blob/HEAD/reports/blind_verbatim_xhigh_p4436af8c/react_z-ai_glm-5.3_r3_20260907T095543Z.md
- k4be paste `cbf4b460` shares the md.succ.ai proxy form (per sub-swarms.md).
- Our corpus: 483 wiki agents; 24 gem `homepage_uri` refs; 16
  `zzmasscounty*` shortener slugs point at it with `?dummyagent=` nonces.

## What could NOT be determined (sandbox limits)

- Real origin IP / hosting: the sandbox egress proxy intercepts DNS and TLS.
  System resolver returned `198.18.30.116` (RFC 2544 benchmarking space —
  the sandbox, not the service). Direct `openssl s_client` and 1.1.1.1 DNS
  fail from here.
- Real TLS certificate: crt.sh returned zero certificates for md.succ.ai
  from this network (likely blocked/rate-limited here); the presented cert
  in-sandbox is the Hatch Sandbox Egress CA. Treat cert history as unknown,
  not as "no certs exist".
- These need an outside-the-sandbox check, not deeper probing from here.

## Assessment

md.succ.ai is the clearest "second jina" in the hunt: a maintained,
documented, MCP-native reader proxy that at least two independent agent
swarms adopted within days of each other (May 29 wiki usage; June wiki
shortener chains). Its anti-detection stack (TLS impersonation, UA pool,
proxy rotation) is exactly the feature set an agent operator needs against
bot-blocked targets like sec.gov. The `?dummyagent=` nonces on shortener
slugs pointing at it suggest agents treat it as instrumented infrastructure,
not just a public utility. Worth watching for: other `*.succ.ai` hosts,
other agent frameworks vendoring it as a fetch backend.
