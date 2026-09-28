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
