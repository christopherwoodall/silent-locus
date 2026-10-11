# Nonce-grammar sweep — incident discovery, play 1

Scout date: 2026-10-03. Method: INVERTED HUNT. Instead of checking known
incidents, sweep Wayback CDX for the toolkit's cache-buster grammar and let
unknown incidents fall out.

## Grammar swept (urlkey regex, matchType=prefix, 2026-06-01..2026-08-01)

| key | pattern | meaning |
|---|---|---|
| zzoai | `zz=oai[0-9]+` | provider marker, DoE fuzz run |
| zzbulk | `zzbulk` | bulk-capture marker (42,677 arquivo.pt hits) |
| x0dec | `x=0.[0-9]{10,}` | county.json burst cache-buster |
| freshx | `fresh=x` | `?fresh=x<epoch>.<random>` probe grammar |
| prepnum | `prep[0-9]{4,}` | prepnonce marker |
| cbdec | `cb=0.[0-9]{10,}` | generic cache-buster (noisy; burst-clustering filters) |

## Method notes (CDX quirks found)

- Exact-URL CDX match does NOT return query-string variants: the county.json
  burst only appears under `matchType=prefix`. All sweep queries use
  `matchType=prefix` + `collapse=urlkey`.
- Regex in `filter=` MUST be fully URL-encoded (`.*` → `.%2A`); unencoded
  asterisks silently return [].
- Mid-URL wildcards (`url=host/*x=0.*`) do NOT work — CDX only honors
  trailing-`*` prefix wildcards. Grammar matching requires the regex filter.
- Cost scales with captures under the prefix: domain-wide regex scans 504 on
  large hosts even in a 2-month window. **Path-scoped prefix
  (`url=<host>/<path>` + `matchType=prefix`) is ~50x cheaper** (1s vs 60s+)
  and is the sweep's primary method. Directory-level prefixes still 504 on
  the busiest hosts (e.g. sec.gov/files); file-level prefixes are instant.
  Path shapes swept: /api, /files, /data, /ajax, /search — covering all four
  known incidents' shapes (DoE /api/v1.0, SEC /files, BEA /api, LAC /ajax).
- 6 parallel shards, 1.5s pacing each, 120s timeout. Idempotent via query log.

## Positive controls

- **county.json burst (SEC, Jun 18 2026):** `url=sec.gov/files/county.json`
  `matchType=prefix` → 74 rows, 41 with `?x=0.<17d>` (validated manually;
  too big for the domain-wide sweep — sec.gov 504s).
- **DoE Jun 17 `zz=oai` (negative control):** `civilrightsdata.ed.gov` +
  `zz=oai[0-9]+` → 0 rows. CORRECT: the fuzz run was never saved to Wayback
  (only arquivo.pt). Confirms the sweep isn't hallucinating the provider marker.

## Coverage

**Final: 1,380 queries, 1,360 clean (HTTP 200), 20 CDX timeouts (504), 0 with
any rows.** 46 hosts x 5 paths (/api, /files, /data, /ajax, /search) x
6 grammars, incident window 2026-06-01..2026-08-01. Query log:
`logs/nonce-query-log-path.jsonl` (1,380 unique qkeys, no dupes). Hits file
was never created — zero hits. Scripts: `nonce_sweep.py` (domain-wide;
superseded — 504s on big hosts), `nonce_sweep_path.py` (path-scoped;
primary; 6 shards, 1.5s pacing, idempotent).

Hosts: civilrightsdata.ed.gov, www.sec.gov, sec.gov, apps.bea.gov, bea.gov,
census.gov, www.census.gov, kansasmemory.gov, bac-lac.gc.ca,
recherche-collection-search.bac-lac.canada.ca, data.nysed.gov, wonder.cdc.gov,
portal.max.gov, ed.gov, www.ed.gov, nces.ed.gov, data.gov, api.data.gov,
whitehouse.gov, justice.gov, cdc.gov, www.cdc.gov, nih.gov, nasa.gov, noaa.gov,
weather.gov, irs.gov, ssa.gov, va.gov, state.gov, dhs.gov, commerce.gov,
treasury.gov, labor.gov, energy.gov, usda.gov, doi.gov, dot.gov, hud.gov,
epa.gov, nps.gov, fbi.gov, bls.gov, fhfa.gov, canada.ca, gc.ca.

## Burst table

(clustered host+path+day; >=10 hits/day threshold)

| hits | host | path | day | example URL |
|---|---|---|---|---|
| _none_ | — | — | — | — |

Zero bursts. Zero single hits. Every clean (HTTP 200) query returned [].

## Unscannable (HTTP 504, even path-scoped)

- `sec.gov/files`, `www.sec.gov/files` — all 6 grammars (busiest path; the
  county.json burst lives here; file-level prefixes work but directory-level
  scans time out)
- `sec.gov/ajax` (zzbulk), `census.gov/data` (zzoai),
  `www.census.gov/ajax` (zzbulk), `civilrightsdata.ed.gov/data` (prepnum),
  `data.gov/search` (x0dec), `www.ed.gov/search` (freshx),
  `ed.gov/search` (cbdec), `dhs.gov/ajax` (x0dec)

These are CDX-side timeouts, not evidence of anything.

## Interpretation: why the negative is informative

The inverted hunt assumed the toolkit's nonce grammar would surface in
Wayback if other incidents existed. It doesn't — and the machinery explains
why: **arquivo.pt is the agents' relay of choice, not Wayback.** The DoE fuzz
run (14,941 `zz=oai` tags) lives ONLY in arquivo.pt; Wayback has zero
`zz=oai` anywhere in the swept .gov surface. Wayback captured exactly one
nonce-grammar event — the county.json burst — most plausibly because those
were deliberate `/save/` creates (hemo-web-read teaches agents to create
Wayback captures) rather than relay traffic.

So: the nonce grammar is a Wayback-visible signal ONLY when the agent
deliberately saves to the Wayback Machine. The sweep's clean negative means
**no other June–July 2026 incident involved Wayback saves with nonce URLs**
across 46 hosts' API/data/file/search paths — not that no other incidents
exist. The fuzz traffic lives in arquivo.pt; the next inverted-hunt play
belongs there, not here.

## Residual leads (unscanned surfaces, NOT incidents — no evidence)

1. **sec.gov/files at directory level** — 504s on all grammars; the burst's
   home turf. Needs file-level enumeration (we know county.json; regcf.json
   checked clean: 4 plain captures, 0 nonce).
2. **census.gov/data, www.census.gov/ajax, sec.gov/ajax** — 504 on select
   grammars; narrower time slices (single weeks) may fit under the timeout.
3. **The two Sep 2026 jina-wrapped county.json captures** (archive-angles
   scout) — WARC peek to rule out agent origin before closing the file.

## Supplementary manual probes (this session)

- `sec.gov/files/regcf.json` (new target from code-packages scout):
  4 captures, 0 nonce grammar (3x 2026-06-18 plain — same day as the
  county.json burst, likely the same saver/crawler; 1x 2026-04-21 plain).
- `apps.bea.gov/api` + zzoai/x0dec, LAC `/ajax` + x0dec,
  `civilrightsdata.ed.gov/api` + zzoai: all clean zeros.
