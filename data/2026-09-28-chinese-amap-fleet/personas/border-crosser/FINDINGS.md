# BORDER CROSSER — persona findings (2026-10-05)

Hunt lens: agents operating across jurisdictions in single sessions, joined by grammar/timing. Single-country agents are the reported ones; the unreported ones work everywhere at once.

## 1. Known pipeline is already a border-crosser (verified from local files)

The `uq` pipeline crosses three countries on one submitter identity (2 `settings.exit_node` values across 2,159 reports):

| Date (UTC) | Country | Target | Grammar | n |
|---|---|---|---|---|
| 2026-06-20 12:52–13:02 | Australia | `vizprod.aihw.gov.au` (AIHW, gov health Tableau module, via httpbun/base64 payloads) | `uqtag=AGEDATA23` | 4 |
| 2026-06-21 06:08–09:45 | USA (Iowa) | `data.idph.state.ia.us` (IDPH Tableau, county-by-county asthma ED CSVs: Dubuque, OBrien, Tama, Marion, Page, Kossuth, Greene, Calhoun) | `mark=<county><epoch>` e.g. `mark=dub1782035071`; `validation=v<epoch>_<counter>` e.g. `validation=v1782022195_6_1` | 48 |
| 2026-09-27 | USA (Iowa) | IDPH Scott County via `r.jina.ai` | second wave | 3 |
| 2026-09-28 → 10-05 | China | `amap.com` / `gaode.com` (place scraping), museums | `uqscan=<word><YYYYMMDD>[suffix]` + 35 exotic `uq*` params | ~2,000 |

- The June 20/21 strands are ~18 hours apart: Australian gov health Tableau module extraction, then Iowa county-by-county health CSVs. Same task family (health-data), two countries, one day.
- IDPH nonces are real session epochs (e.g. `1782035071` → 2026-06-21 09:44 UTC, matching submission time) — the nonces are session timestamps, not random.
- The Sep 27 IDPH re-touch (via r.jina.ai) lands the day before the Amap campaign starts — the pipeline touched US health data immediately before pivoting to China maps.
- Source: `writeup-idph-iowa.md`, `behavior-hunt/raw/idph_burst.json`, `full-sweep/raw/corpus-remine.md`.

**Open lead — ltzh casino stratum:** 6 casino domains submitted at the exact minutes of the operator's 2026-10-04 ltzh R&D burst (12:58/13:08/13:15): `star-vegas.it` (IT), `cinevo.nl` (NL), `casibom90998.com`, `flrdrop.vip`, `juntanacional.co` (CO), `jojobet-resmi-gir.vip`. Bare domains, no grammar markers on public pages; attribution unresolvable keylessly. If those share the operator's exit node, this is the same agent working a casino vertical across Italy/Netherlands/Colombia in the same hour as its R&D. Flagged, not claimed. Source: `full-sweep/raw/corpus-remine.md` §uqtag.

## 2. New-agent sweeps (children)

- gov-domain sweep (non-Western govs, urlquery htmx): raw notes → `raw/gov-sweep.md`
- urlscan.io multi-country sweep: raw notes → `raw/urlscan-sweep.md`

>Status: two child agents crawling; htmx endpoint throttled under persona-swarm load, retries pending.

## 3. Doctrine notes

- Join on the grammar, not the flag: a global agent's session looks like several local agents until nonces/tags/timing are joined.
- urlquery's public schema has NO submitter-IP; ASN/country diversity in `ip`/`asn` is target-side. True submitter-side joins are `useragent`, `exit_node`, tag grammar, timestamp.
- Agents only; no human/operator identity work.
