# THE BIRDWATCHER — FINDINGS

**Persona:** citizen-science API surfaces (eBird, iNaturalist, GBIF) as agent-farming grounds.
**Run date:** 2026-10-05 (~06:00 UTC). Egress tested: urlquery.net reachable (200); eBird/iNaturalist/GBIF API hosts timed out from this VM on first attempt.
**Status:** Complete. Nothing committed or pushed.

## Method
1. Grepped all three canonical corpora for ebird/inaturalist/gbif/biodiversity/bird mentions.
2. urlquery htmx domain searches (curl variant, ≤1 req/5s): `ebird.org`, `inaturalist.org`, `gbif.org`, `api.ebird.org`, `api.inaturalist.org`.
3. Pulled full HTTP-transaction data for 3 eBird cluster reports via the keyless `/filter/http` endpoint.
4. urlscan.io public search API (blocked from this egress — lane blocked, not a negative).
5. Web search for the probe marker `x=87789` (no known tool signature).

## Finding 1 — eBird GBBC region-enumeration cluster (NEW, agent-shaped candidate)

**18 urlquery submissions, 2026-05-13 18:18 UTC → 2026-05-14 08:11 UTC**, walking the Great Backyard Bird Count region hierarchy:

| Time (UTC) | Submitted URL | Reports |
|---|---|---|
| May 13 18:18 | ebird.org/gbbc/region/CA/regions | 1 (d550690f) |
| May 13 18:57–18:58 | ebird.org/gbbc/region/CA | 4 (b94bad43, a248c667, cd2fadc6, 46c5089a) |
| May 13 19:36 | ebird.org/gbbc/region/CA-AB?yr=2024 | 1 (2acbfd00) |
| May 13 22:53 | ebird.org/gbbc/region/CA/regions | 2 (1d7e77f1, 93228a9a — same minute) |
| May 13 23:48 | ebird.org/gbbc/region/CA/regions?yr=EBIRD_GBBC_2024 | 3 (b83f5a68, 32cd14a4, 87cfd719 — same minute) |
| May 14 02:05–02:11 | ebird.org/gbbc/region/world/regions?yr=EBIRD_GBBC_2024 | 3, one with `&x=87789` (41deef0a, d9981b24, 6085934d) |
| May 14 02:13 | ebird.org | 1 (2e34fd7e) |
| May 14 02:43 | ebird.org/gbbc/region/CA/regions?yr=2024 | 1 (b263d78a) |
| May 14 03:04 | ebird.org/gbbc/region/CA-AB?yr=2024 | 1 (3ffefac6) |
| May 14 08:11 | ebird.org/gbbc/region/CA/regions | 1 (10fa74f8) |

**Why agent-shaped:** region-hierarchy walk (world → CA → CA-AB), triple/quadruple re-submissions of identical URLs within the same minute (machine cadence — humans don't re-scan the same page 3× in 60s), and a probe/cache-buster parameter `x=87789` on one world/regions fetch.

**Full-report inspection:** page loads are normal eBird renders (S3 static assets, Cornell CAS login flow); submitter side shows the stock scanner UA. **No agent self-labels** in URLs or payloads. One report fetch returned empty (transport flake, not evidence).

**Web check:** `x=87789` has no public tool signature — consistent with a one-off probe nonce, not a known scraper.

**Classification: GENUINELY NEW** — zero hits in all three corpora (see verification below).

**Grade: probable programmatic submission, unconfirmed agent.** Honest alternative: a vendor, researcher, or QA harness regression-testing the GBBC region pages. The cadence is the evidence; there is no content-level agent marker. Worth watching for recurrence.

## Finding 2 — iNaturalist: 2 hits, both non-agent

- `1056a39c-…`: bare `inaturalist.org` homepage submitted 2026-09-24 — single ordinary scan.
- `a86a5c2c-…`: `forum.inaturalist.org/t/how-to-fix-quickbooks-payroll-support/75701` (2026-02-13) — forum spam, human cybercrime, not agent-shaped.

**Classification: KNOWN-pattern noise. Not a find.**

## Finding 3 — GBIF and the API endpoints: honest zeros

- `url.domain:gbif.org` → 0 reports.
- `url.domain:api.ebird.org` → 0 reports.
- `url.domain:api.inaturalist.org` → 0 reports.

**No evidence of agents farming the actual biodiversity APIs in urlquery-visible traffic.**

## Local-corpus verification (mandatory lane)

- Amap fleet `events.jsonl` (2,141): **0** biodiversity mentions.
- `openai-agent-traces` (589,972): 16 grep hits — **all false positives** (the string "GBIF" inside record digest `OKLKEUZWGBIF6YV46VXOXGC3FPXJKWRN`). Zero real mentions.
- `oai-tag-sweep`: 1 grep hit — **false positive** ("littlebird" URL fragment).

**Our sets are clean of biodiversity-API agent activity. The eBird cluster is genuinely new to us.**

## Method note

Citizen-science APIs are nearly invisible to urlquery *by construction*: agents that farm APIs pull JSON, they don't submit API URLs to web scanners. The observable surface is **web-page enumeration** (what we caught: region-page walks), not API farming. Hunting actual API abuse would need a different surface — eBird's public hotspot/recent-observation outputs checked for mirrored copies, GitHub code search for bulk-pull scripts, or GBIF download-DOI logs. Recommended follow-up lane.

## Blocked lanes (not negatives)

- urlscan.io public search API returned empty/non-JSON from this egress (blocked or rate-limited). The eBird cluster was NOT cross-checked on urlscan.
- eBird/iNaturalist/GBIF API hosts timed out on direct curl from this VM (first attempt only); no API-shape comparison was possible.

## URLs observed (appendix)

### eBird cluster (18)
- https://urlquery.net/report/10fa74f8-2956-43d2-09eed4f8f6c5 (ebird.org/gbbc/region/CA/regions, 2026-05-14)
- https://urlquery.net/report/3ffefac6-2603-400a-904c-6e9cd37ebad3 (ebird.org/gbbc/region/CA-AB?yr=2024)
- https://urlquery.net/report/b263d78a-0027-4ae1-b1d0-bbc0c2f20a46 (ebird.org/gbbc/region/CA/regions?yr=2024)
- https://urlquery.net/report/2e34fd7e-08af-4287-bb10-0a8b1d62a6d8 (ebird.org)
- https://urlquery.net/report/6085934d-f240-4003-80af-5f383ef6458d (ebird.org/gbbc/region/world/regions?yr=EBIRD_GBBC_2024&x=87789)
- https://urlquery.net/report/d9981b24-7b52-4877-a416-295b80f1fec7 (ebird.org/gbbc/region/world/regions?yr=EBIRD_GBBC_2024)
- https://urlquery.net/report/41deef0a-df02-4da8-a532-732b67fab533 (ebird.org/gbbc/region/world/regions?yr=EBIRD_GBBC_2024)
- https://urlquery.net/report/b83f5a68-b8c1-4eeb-8738-ce901abb55ce (ebird.org/gbbc/region/CA/regions?yr=EBIRD_GBBC_2024)
- https://urlquery.net/report/32cd14a4-242e-4d26-8e6a-9a01dbb35a3e (ebird.org/gbbc/region/CA/regions?yr=EBIRD_GBBC_2024)
- https://urlquery.net/report/87cfd719 (ebird.org/gbbc/region/CA/regions?yr=EBIRD_GBBC_2024)
- https://urlquery.net/report/1d7e77f1 (ebird.org/gbbc/region/CA/regions)
- https://urlquery.net/report/93228a9a (ebird.org/gbbc/region/CA/regions)
- https://urlquery.net/report/2acbfd00 (ebird.org/gbbc/region/CA-AB?yr=2024)
- https://urlquery.net/report/cd2fadc6 (ebird.org/gbbc/region/CA)
- https://urlquery.net/report/46c5089a (ebird.org/gbbc/region/CA)
- https://urlquery.net/report/b94bad43 (ebird.org/gbbc/region/CA)
- https://urlquery.net/report/a248c667 (ebird.org/gbbc/region/CA)
- https://urlquery.net/report/d550690f (ebird.org/gbbc/region/CA/regions)

### iNaturalist
- https://urlquery.net/report/1056a39c-7769-459e-a7e7-fedfc1808865 (inaturalist.org homepage)
- https://urlquery.net/report/a86a5c2c-0b8e-4a37-a455-abf1d4d9908c (forum.inaturalist.org spam thread)

### Reference
- https://ebird.org/gbbc/region/world/regions (enumerated target)
- https://api.ebird.org/v2/data/obs/US/recent (keyless public output, unreachable from VM this run)
- https://api.inaturalist.org/v1/observations (unreachable from VM this run)
- https://api.gbif.org/v1/occurrence/search (unreachable from VM this run)
