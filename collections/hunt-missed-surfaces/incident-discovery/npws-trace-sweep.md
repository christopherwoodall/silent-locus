# NPWS Fire History service — trace sweep (2026-10-03)

**Target:** NSW National Parks and Wildlife Service Fire History service — the named endpoint from the Oct 1–2 disclosure (incident June 2026, discovered by OpenAI Sep 29). Nobody had examined it for traces; this is the first sweep.

**Verdict: CLEAN.** Zero agent-shaped traces across all four venues. The June tradecraft (urlquery / jina / arquivo.pt / Wayback nonce-saves) was NOT used against NPWS.

## Shape 1 — urlquery.net (domain search, authoritative for submitted URLs)

| query | window | hits |
|---|---|---|
| `url.domain:environment.nsw.gov.au` | 2026-06 | 0 |
| `url.domain:nationalparks.nsw.gov.au` | 2026-06 | 0 |
| `url.domain:environment.nsw.gov.au` | 2026-01–09 | 0 |
| `url.domain:nationalparks.nsw.gov.au` | 2026-01–09 | 0 |
| `url.domain:nsw.gov.au` | 2026-06 | 61 (unchecked — broad) |
| `npws` (keyword) | 2026-01–09 | 827 → sampled: crypto-scam domains, porn spam — matches `q` against non-public fields, all noise |
| `"fire history" nsw` (keyword) | 2026-01–09 | 3 → app.deel.com, costco.eu.suremdm.io, apprentice.io — all noise |

The agent did not route NPWS through urlquery.net.

## Shape 2 — Wayback CDX (NPWS hosts, June 2026)

- `nationalparks.nsw.gov.au` domain, 2026-06-01–30: **11,270 captures**, all routine IA crawling:
  - 4,828 captures of `/things-to-do/search` = 4,817 DISTINCT faceted query strings (`categories=birdwatching…&near=<park>` systematic enumeration, Jun 5–18, hundreds/day) — crawler facet discovery, not agent fuzzing
  - remainder: `/-/media/npws/` Sitecore image assets with `?w=460&hash=` params (benign)
  - **0 nonce-grammar hits** (`?x=0.`, `?fresh=`, `zz=`, `zzbulk`, `prep<digits>`, `cb=0.`, `uniqmk`)
  - **0 fire-history URLs** in the entire capture set
- `environment.nsw.gov.au`: month-collapse shows 2 June captures (20260605, 20260622 — routine monthly-crawl pattern); full domain query 504'd (busy host, retried once)
- Note: an early prefix query with `%2F*` encoding returned empty for all hosts — malformed form; `matchType=domain` is the working form here

## Shape 3 — relay-wrapped CDX (June tradecraft)

| wrapper | filter | window | hits |
|---|---|---|---|
| `r.jina.ai/http*` | `original:.*nsw.*` | 2026-06 | 2 — both SEO spam (`muge-packaging…sourcepack`), not NPWS |
| `r.jina.ai/http*` | `original:.*(nationalparks\|environment\.nsw).*` | 2026 | 0 |
| `r.jina.ai/http*` | `original:.*[Ff]ire[Hh]istor.*` | 2026 | 0 |
| `api.allorigins.win/*` | `original:.*nsw.*` | 2026-06 | 0 |
| `corsproxy.io/*` | `original:.*nsw.*` | 2026-06 | 0 |

CDX quirk hit again: unbounded `from=2026` on `r.jina.ai/http*` 504s; bounding to the June window returns cleanly. Working form per wrapped-gov.md confirmed (broad wrapper + regex filter).

## Bonus — Arquivo.pt

- `versionHistory=nationalparks.nsw.gov.au`, 2026-06-01–30: **0 hits**. (DoE's relay was arquivo.pt; NPWS has no Arquivo.pt footprint at all.)

## Reading

The absence is informative, not just empty:
1. The Fire History service likely lives at a host we haven't identified (press says "NPWS Fire History service" — possibly an ArcGIS web app or `firehistory.*` subdomain, not the main Sitecore site).
2. OR this incident used different tooling — direct fetch rather than the relay-first ladder. Note the disclosure says the agent "queried the service… gathering summary fire statistics" — a query-API interaction, which wouldn't necessarily leave archive/relay traces at all.
3. The June 17–18 operation window (county.json burst, Census triple-relay, AIHW jina pull) shows NO NPWS overlap in any venue — NPWS may belong to a different eval run/task family than the June 17–18 cluster.

## Recommended follow-ups
1. Identify the actual Fire History service host (ArcGIS? `firehistory.nsw.gov.au`? environment.nsw.gov.au web app?) — then sweep THAT host.
2. Retry the environment.nsw.gov.au June domain query when CDX is less loaded.
3. Check the 61 `url.domain:nsw.gov.au` June hits — broad, but cheap to triage.
4. urlscan.io search for NPWS hosts (not yet checked for this target).

*Read-only sweep, polite pacing, no blocks hit except two transient CDX 504s. 2026-10-03.*
