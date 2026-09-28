# Lane T: api.usa.gov / FBI UCR candidate sweep — NULL verdict (2026-09-28)

## Trigger
Lane S (`notes/open-data-api-venues-2026-09-28.md`, commit `a2fb45a`) confirmed
the swarm drinks from the long tail of niche open-data APIs
(api.worldpoverty.io, api.dataafrica.io, nationsreportcard.gov) and left two
**unconfirmed candidates** from a vanderbi.lt stats-leak referrer note:
**api.usa.gov** and **FBI UCR** (crime-data-explorer.fr.cloud.gov / fbi.gov).
Lane T tested both, pattern-level, across every in-repo agent-grammar surface
plus the collusion-wiki ES corpus.

## Verdict: NULL (bounded negative)
No genuine agent-grammar evidence for either candidate anywhere swept.
The only mentions of `api.usa.gov` / `FBI UCR` on disk are the hypothesis
itself: the vanderbi.lt referrer note (`data/vanderbilt-shortener/web_mentions.json`)
and Lane S's provenance documenting them as *unconfirmed candidates*
(`data/open-data-api-venues/PROVENANCE.md`, `build_dataset.py`).

## Method
1. **Local sweep (37 files)**: `data/rmn-re/*` (764-link decoded link table +
   decoded JSON with chains), `data/rmn-re-history/*`, `data/iowacollab-pastes/*.txt|jsonl`,
   `data/paste-archive-gap/bodies/*` + gap JSONs, `data/university-shorteners/*.jsonl`,
   `data/university-shorteners-batch2/*.jsonl`, `data/uoft-shorteners/**/*`,
   `data/vanderbilt-shortener/*`. Case-insensitive regex over raw bytes AND
   deep-URL-decoded content (up to 4 unquote rounds, catching `%2E`/`%252E`-style
   proxy-stacking encodings per `notes/cors-bwa-proxy-2026-09-28.md` primitives).
2. **ES collusion-wiki (80,434 docs, read-only)**: case-insensitive wildcard
   `*pattern*` across keyword fields `external_links`, `matched_string`,
   `source_url`, `meta_homepage`, `download_url`, `diff_url`, plus
   `match_phrase` on text fields `note`, `description`, `meta_summary`.
3. **Greps**: `data/cors-bwa-proxy/`, `data/open-data-api-venues/` (in-repo).

## Patterns tested
`api.usa.gov`, `*.api.usa.gov` (via `*api.usa.gov*`), `fbi.gov`, `ucr`,
`crime-data-explorer`, `cde.ucr.cjis.gov`, `crime_data_explorer`,
`*.fr.cloud.gov` — plus URL-encoded variants (`api%2Eusa%2Egov`,
`api%252Eusa%252Egov`, `fbi%2Egov`, `crime%2Ddata%2Dexplorer`,
`fr%2Ecloud%2Egov`) and broader sanity patterns (`usa.gov`, `cjis`,
`crime_data`, `crime-data`).

## Results
| surface | result |
|---|---|
| local 37 files (raw + decoded) | 0 genuine; only the origin note itself |
| collusion-wiki ES, 12 patterns | 0 genuine |
| `*usa.gov*`, `*cjis*`, `*crime_data*`, `*crime-data*` in collusion-wiki | 0 |
| `*ucr*` in collusion-wiki | 2 hits, both **false positives**: Google Drive `viewerng` URLs whose base64-ish doc IDs contain the substring "UCr" (`...X68UCrARqS9xYw4JBuqE4XMeZoBHB4...`) — no crime-data relation |

No ES index created (no hits, no dataset). No targeted external probes needed.

## Theory-of-mind note
The null is consistent with the venue-selection logic documented in
`notes/cors-bwa-proxy-2026-09-28.md`: agents pick venues with **no auth
required**, generic infra, arbitrary passthrough. api.usa.gov (the federal API
gateway) and the FBI Crime Data API both sit behind API-key signup, while every
open-data venue the swarm *does* touch needs no key: api.worldpoverty.io,
api.dataafrica.io, vizhub.healthdata.org IHME theme APIs, api.datausa.io,
api-la.datausa.io, Yahoo Finance v8. The swarm's data appetite runs health +
econ + finance dashboards, not federal crime stats — the candidate pair looks
like referrer-note noise (or a venue tried once and abandoned for the key
friction), not a live task family.

## Open items
- The vanderbi.lt stats-leak note remains the single source for the candidate
  pair; if raw vanderbi.lt stats ever become passively accessible, re-test.
- `urlquery-incidents` / `urlquery-hunt` ES indices were out of this lane's
  brief (collusion-wiki only) — live submitted scan URLs are the highest-
  fidelity venue evidence and the natural follow-up surface for these two
  candidates.
- If a future lane finds `api.usa.gov`-family hits, check whether they arrive
  via CORS-proxy stacking (bwa/hypnguyen/sirjosh hostnames) like the other
  open-data pulls.
