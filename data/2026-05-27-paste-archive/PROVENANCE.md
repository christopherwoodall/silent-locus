# PROVENANCE — paste-archive dataset

**Retrieved:** 2026-09-28 ~03:00–03:10 UTC, read-only live fetches (one normal web read per paste URL, browser UA).
**Retriever:** archive-recovery lane 3 (swarmtraces-hf-corpus hunt).

## Source selection

Paste hosts came from the investigators' `data/collusion-wiki/site-coverage.csv`
(pastebins category). In-scope for this lane (paste.linuxiarz.pl is a separate
running lane):

| host | corpus paste URLs | status 2026-09-28 |
|---|---|---|
| pastebin.k4be.pl | 20 | LIVE (Stikked) — all 20 verified |
| anna.fyi | 55 | LIVE — 53/55 titles verified, 2 unchecked (rate-limited, not retried) |
| infinitypaste.club | 1 (+1 embed URL, same paste) | LIVE — body recovered |
| swarm.termina.digital | 0 rows in site-coverage.csv | NOT in the investigators' coverage; not pursued |

**No archive recovery was needed**: all three hosts are live, so Wayback CDX /
archive.today were not consulted (a CDX probe also failed upstream; per
standing instruction it was not retried).

## What was recovered

- `k4be.pl/`: 6 full paste bodies (EPL relegation tables 1995–2005, presentation-layer
  text — the fetch extractor numbers list lines, so files are NOT byte-exact
  originals), `metadata.jsonl` for all 20 (title, author pseudonym, body status).
  11 ROIETA-series pastes (Roi Et province TH45 health-study data) and 3 reply-form
  pastes expose metadata only — bodies are behind raw/download endpoints the text
  fetch renders as `x`; they need a live-browser render.
- `anna.fyi/`: `titles.jsonl` — 53 verified titles ("Statistical reference N"
  series, "ReplyLink0/1/2", "NSI table reference 2009-2015" ×2, "Official data
  link"). Bodies are JS-gated in text fetch; need a live-browser render.
- `infinitypaste.club/`: full body of `Gf4nRzww` ("LinkNSIDataMay27Final") —
  an official-statistics reference link to site-test.nsi.bg.

## Verification

- Corpus `records.jsonl` carries `original_text_sha256` per paste URL (from the
  investigators' local `agent-text-pack.tar.gz`, not available here). Our
  extracts are presentation-layer and cannot be byte-compared; no sha match claimed.
- Tradecraft battery (jina, web_hooks, go-import, oast, zz/epoch grammars,
  proxy chains, `<img>` beacons) run over all recovered bodies: **zero hits** —
  recovered texts are clean task data.

## Caveats

- k4be ROIETA pastes show `[paste_expire] 4 miesiące` (expire in 4 months) —
  recovery is time-sensitive; re-pull before expiry.
- anna.fyi `93811d8c` ("Official data link") threw a PHP/GeSHi deprecation error
  that leaked the server path `/home/things/domains/anna.fyi/public_html/`
  (CodeIgniter app). Noted as infrastructure fact; not pursued.
- k4be author names are adjective–animal generated pseudonyms
  (e.g. "Abrupt Armadillo", "Chartreuse Sheep") — agent-style naming, recorded
  as-is; no operator attribution pursued.

## Scope

Agents and agent infrastructure only. No person-level attribution.

## Raw layer 2026-09-29

Moved script-consumed transform inputs into raw layer (upstream names preserved, exempt from event schema):
- `data/paste-archive/anna.fyi/titles.jsonl` -> `data/paste-archive/raw/anna.fyi/titles.jsonl` (consumed by scripts/es_ingest_paste_archive.py)
- `data/paste-archive/infinitypaste.club/metadata.jsonl` -> `data/paste-archive/raw/infinitypaste.club/metadata.jsonl` (consumed by scripts/es_ingest_paste_archive.py)
- `data/paste-archive/k4be.pl/metadata.jsonl` -> `data/paste-archive/raw/k4be.pl/metadata.jsonl` (consumed by scripts/es_ingest_paste_archive.py)

## Schema build 2026-09-29 (worker W5)

- events.jsonl: **76 records** (record_kind `pastebin_probe`), one per paste —
  the union of paste ids across the three metadata files and body files:
  55 anna.fyi (all with bodies), 20 pastebin.k4be.pl (17 bodies, 3
  metadata-only), 1 infinitypaste.club (with body). Note: 6 k4be bodies live
  at `raw/k4be.pl/<id>.txt` (EPL series), the other 11 at
  `raw/bodies/k4be.pl/<id>.txt`; both were picked up.
- fingerprint identity string: `paste|<host>|<id>` (e.g.
  `paste|anna.fyi|003a0488`).
- `@timestamp`: 2026-05-27T00:00:00Z (dir date prefix) for all rows —
  per-paste creation dates are not in the raw data (only the infinitypaste
  body header notes "created: 2026-05-27"); `labels.timestamp_source =
  "dir_prefix:no_per_paste_date"`.
- Full paste bodies stay in raw/; records carry `paste.body_path`,
  `paste.body_sha256`, `paste.body_bytes`, a 200-char `paste.body_excerpt`,
  and `paste.tradecraft_battery` (`zero_hits` for recovered bodies,
  `not_run:body_absent` for metadata-only pastes). `retrieved_at`
  2026-09-28T03:15:00Z (recovery window ~03:00–03:15 UTC).
- SHA256SUMS regenerated (sha256sum style, relative paths): covers
  events.jsonl + all 80 raw files. The previous SHA256SUMS referenced the
  pre-raw-layer layout (stale entries for files since moved into raw/) and
  was replaced.
- Verified: all 76 records validate against schema/record.schema.json;
  fingerprint recomputed by hand for Gf4nRzww / 11e9447e / 003a0488;
  body sha256 matches disk for the infinitypaste record.

## Rollup layer 2026-09-29 (worker W5)

- rollup.jsonl: **3 records** (record_kind `paste_venue_rollup`,
  `event.dataset = 2026-05-27-paste-archive-rollup`) — one per venue
  (anna.fyi / pastebin.k4be.pl / infinitypaste.club) with paste counts,
  bodies-recovered vs metadata-only split, live counts, body-status
  breakdown, and the tradecraft-battery result. Same shared schema.
- fingerprint identity string: `paste-venue-rollup|<host>`.
- Covered by SHA256SUMS; verified against the event stream (k4be: 20
  pastes / 17 bodies).
