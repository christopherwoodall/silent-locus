# LATAM scout — urlquery agent-activity scan (local corpora)

Run: 2026-10-04 ~23:40 CDT (2026-10-05 04:40 UTC).
Scope: LATAM government domains on urlquery.net — `gov.br`, `gob.mx`, `gob.ar`, `gov.co`, `gob.cl`, `gob.pe`.
Hunt posture: agents, not operators. Agent shape = timing + action + grammar, not language.

## Egress outage (method note)

Live urlquery.net queries could not run. The htmx tool (`~/workspace/skills/urlquery/bin/uq_htmx.py`)
failed on every query (urllib proxy-CONNECT timeout, 60s each), and direct curl to both
`urlquery.net/api/htmx/search/` and `https://www.google.com` also timed out (exit 28) while direct TCP
to urlquery.net:443 succeeded — the egress proxy path was down, not DNS. Per instruction, no further
retries were burned. The live queries (7 planned) are NOT run; raw per-query JSONs below encode the
local-corpus substitutes with the outage noted in each.

## Local method

Streamed grep (no full-file loads) over:
- 73× `data/*/events.jsonl` (~1.36 GB total corpus surface)
- 12× `collections/*/data/*.jsonl`

Patterns: `gov\.br|gob\.mx|gob\.ar|gov\.co|gob\.cl|gob\.pe`, plus an expanded LATAM gov pass
(`gob.bo|gov.ec|gov.py|gob.uy|gob.gt|gob.hn|gov.cr|gob.pa|gob.do|gov.ve|gob.sv|gov.ni|gob.cu`).
Raw context lines: `raw/latam-local-matches.txt`; expanded pass: `raw/latam-expanded-matches.txt`
(empty = complete negative).

## Findings

### 1. Three gov.br hits — agent-shaped fetches, one-off (NOT programmatic scanning)

All three live in `data/2026-10-01-oai-tag-sweep/events.jsonl` (source `frozen:urlquery-incidents`),
tagged `urlquery-hunt` + `agent-activity`, campaign `cors-laundering-ops`, indicator
`jina_allorigins_dagd` (jina/allorigins CORS-laundering wrapper detection):

| event_time (UTC) | submitted URL | report |
|---|---|---|
| 2026-07-19T06:04:02 | `anatel.gov.br/` (Brazilian telecom regulator) | `dd4fa017-96a3-4d7a-9753-409a525b99ba` |
| 2026-08-13T13:48:53 | `www.anatel.gov.br` | `b11fd092-3a5b-4fbd-a552-7feae342f9c4` |
| 2026-08-14T23:14:14 | `esporte.gov.br/` (Brazilian Ministry of Sport) | `46e7c66d-c64f-4183-b675-1f10e0b2ca4d` |

Assessment: an agent fetched these pages through an allorigins CORS wrapper and the wrapper
invocation was submitted to urlquery. The `jina_allorigins_dagd` indicator is shared with 1,445
other events in the 2,612-event `cors-laundering-ops` campaign (span 2026-05-01 → 2026-09-23).
Timing is sparse and irregular (25 days apart for the two ANATEL hits; one esportes.gov.br a day
later), URLs are bare domains with no nonce/tag grammar, no tunnel relays, no subdomain or
page-by-page enumeration. Verdict: **one-off agent page reads, not a scanning campaign.**
Raw JSON: `raw/latam-gov.br.json`, `raw/latam-gov.br-recent.json`.

### 2. Zero hits for every other target TLD — clean regional negative

`gob.mx`, `gob.ar`, `gov.co`, `gob.cl`, `gob.pe` and all expanded LATAM gov TLDs: **zero mentions
anywhere** in the 73 events files and 12 collections files. Empty per-query JSONs document this:
`raw/latam-gob.mx.json`, `raw/latam-gob.ar.json`, `raw/latam-gov.co.json`,
`raw/latam-gob.cl.json`, `raw/latam-gob.pe.json`.

### 3. Broader LATAM context inside cors-laundering-ops: generic browsing, no gov sweep

26 LATAM-ccTLD hits exist in the same campaign (e.g. `incorporacion.mil.co`,
`defesacoletiva.org.br`, `antamina.logiflex.pe`, `termasdesanluis.cl`, plus commercial/tourism
sites and one ACME-challenge URL `iglesiamontededios.org.do/.well-known/acme-challenge/...`).
All are single-hit bare domains — the campaign's baseline pattern is agents pulling arbitrary
pages through CORS proxies, not regional or topical targeting. Colombia's `incorporacion.mil.co`
(Colombian military recruitment) is the closest gov-adjacent item but is `.mil`, not `.gov`.

## Bottom line

- **Programmatic agent-shaped scanning of LATAM gov targets: NO.** The only LATAM gov evidence in
  local corpora is three one-off agent reads of Brazilian gov.br domains via CORS-laundering
  wrappers (Jul–Aug 2026). No bursts, no nonce/tag grammars, no relay chains, no enumeration.
- **gob.mx / gob.ar / gov.co / gob.cl / gob.pe: complete negative** in local corpora.
- Live urlquery verification is still owed once egress returns — rerun the 7 htmx queries
  (`gov.br`, `gob.mx`, `gob.ar`, `gov.co`, `gob.cl`, `gob.pe`, `gov.br date:[2026-06-01 TO 2026-10-05]`)
  to confirm.

No commits/pushes made (per instruction).
