# PROVENANCE — 2026-10-01-arquivo-pt (lane 1/4 collection)

**Event:** Arquivo.pt capture-metadata collection for Transluce us-canada-gov incidents
**Context:** `notes/transluce-us-canada-gov-2026-10-01.md` (report: https://transluce.org/us-canada-gov, published 2026-09-30)
**Collected:** 2026-10-01 (UTC; see collect.log.jsonl `run_start`/`run_done`)
**Collector:** `data/2026-10-01-arquivo-pt/collect.py`; timelines built by `analyze.py`
**Steering:** timestamps first-class (full ISO, second precision) — `timeline/*.timeline.csv` is the join key for lanes 2–4.
**Storage:** `raw/<slug>.cdx.jsonl.gz` (gzip -9; 480MB → 165MB — GitHub 100MB/file limit).
`analyze.py` reads `.jsonl.gz` transparently.

## What was queried

Arquivo.pt CDX API, no API key: `https://arquivo.pt/wayback/cdx?url=<host>&matchType=domain&from=<yyyymmdd>&to=<yyyymmdd>&output=json`
Each target's incident window padded ±7 days; out-of-window captures flagged in
timeline CSVs (`out_window_side` = before/after) — those are leads, not noise.

| slug | host(s) (domain match) | incident window | Transluce claim |
|---|---|---|---|
| kansas-kansasmemory | kansasmemory.gov | 2026-05-07 | 36,578 captures, peak 1,093/min |
| maryland-edstats | msde.maryland.gov (covers reportcard.*) | 2026-05-06 | 295,912 captures, peak 5,594/min |
| illinois-iquery | iquery.illinois.gov | 2026-04-19→2026-05-01 | 251 captures |
| lac-collectionsearch | bac-lac.gc.ca | 2026-05-28 + 2026-06-09 | 899 requests |
| doe-crdc | civilrightsdata.ed.gov | 2026-06-17 | 200,000+ requests; `State_Id=1 OR 1=1` |
| bea-api | apps.bea.gov | 2026-06-16→2026-06-18 | 3,005 captures; "OpenAI Research" registration |
| omb-max | portal.max.gov | 2026-05-25→2026-05-27 | (Transluce evidence is urlquery-based) |
| navy-history | history.navy.mil | 2026-04-23/24, 2026-05-18 | probing alt URLs/CMS |
| doj-ojjdp | ojjdp.ncjrs.gov, ojjdp.ojp.gov | 2026-05-30/31 | encoded parent-dir legacy table |
| sec | www.sec.gov | 2026-06-18 | county.json laundering cluster |
| cdc-wonder | wonder.cdc.gov | 2026-07-18 | WONDER form submission |
| calaccess | cal-access.sos.ca.gov | 2026-05-26 | CAL-ACCESS antibot bypass |
| nysed-enrollment | data.nysed.gov | 2026-05-17 | NY school-enrollment stats |
| texas-dshs | dshs.texas.gov | 2026-05-17 | Texas DSHS STI stats |

## Volumes collected (vs claims)

Unique captures = deduped on (timestamp, url). "In-window" = within Transluce's
reported incident dates. All figures from `timeline/<slug>.summary.json`.

| slug | collected unique | in-window | Transluce claim | match | peak/min (ours vs claim) |
|---|---|---|---|---|---|
| kansas-kansasmemory | 36,496 | 36,496 | 36,578 | 99.8% | 1,093 (claim 1,093) — exact |
| maryland-edstats | 293,898 | 293,898 | 295,912 | 99.3% | 5,555 (claim 5,594) — 99.3% |
| illinois-iquery | 171 | 171 | 251 | 68% | 7/min; mostly 503s |
| lac-collectionsearch | 982 | 982 | 899 | 109% | 129/min |
| doe-crdc | 250,822 | 218,986 | 200,000+ | above | 4,942/min |
| bea-api | 2,988 | 2,988 | 3,005 | 99.4% | 218/min |
| omb-max | 26 | 26 | (urlquery-sourced) | n/a | 10/min |
| navy-history | 3,782 | 3,780 | n/a | n/a | 112/min |
| doj-ojjdp | 0 | 0 | n/a | honest negative | — |
| sec | 0 | 0 | (urlquery-sourced) | honest negative | — |
| cdc-wonder | 0 | 0 | (web.archive.org) | honest negative | — |
| calaccess | 111 | 111 | n/a | n/a | 9/min |
| nysed-enrollment | 696 | 496 | n/a | n/a | 138/min |
| texas-dshs | 0 | 0 | n/a | honest negative | — |

**Corroboration highlights:**
- Kansas peak minute 1,093/min reproduces Transluce's claimed peak exactly; 32,349 of
  36,496 captures are HTTP 504 — corroborates "website started returning gateway timeouts".
- Maryland peak 5,555/min vs claimed 5,594 (99.3%).
- LAC: all 13 attack-payload types confirmed on the canada.ca frontend host
  (`IdNumber=%27`, `1%20OR%201%3D1`, `1%2C2`, `%253C` double-encoded XSS,
  `2147483648`, `abc`, `.json`, `?output=`, `?raw=`, `?url=`, `debug=1` ×2).
- DoE: exact `State_Id=1 OR 1=1` probe captured once; fuzzing-ladder values present;
  `zz=fillNNNN` cache-buster param on 27.7% of captures (shared-launcher tradecraft
  marker matching our RubyGems/wiki corpora); 19-digit `nonce=`/`prepnonce=` values.
- Illinois: 117 of 171 captures are HTTP 503 — corroborates "service unavailable".
- BEA: 2,988 vs 3,005 (99.4%); 6 burst minutes.
- **SavePageNow share ≈100%** on every non-zero target (collection `SAWP5`,
  `save-merged-*` WARCs) — user-triggered captures, corroborating agent-relay use
  of ArchivePageNow rather than background crawl.

**Out-of-window leads (new, not in Transluce's windows):**
- DoE: **31,600 captures on 2026-06-16** (day before incident) + 109 on Jun 15 +
  127 on Jun 18 — same API endpoints, ramping 19:00–23:00 UTC; precursor day.
- NYSED: 12 on May 16, 185 on May 18, 3 on May 19–20 — follow-on activity.
- Navy: 2 on Apr 22.
- (Kansas, Maryland, Illinois, LAC, BEA, CAL-ACCESS: zero out-of-window in ±7d pad.)

## What the no-key API exposes vs gates

| Surface | No-key? | Notes |
|---|---|---|
| CDX capture metadata (`/wayback/cdx`, also `/cdxserverapi`) | YES | timestamp (second precision), original URL, mime, status, content digest, WARC filename/offset, collection id |
| Version-history search (`textsearch?versionHistory=<url>`) | YES | estimated result count, per-capture links: replay, no-frame replay, screenshot, metadata, original-file (`id_` replay) |
| Archived page replay (`/wayback/<ts>id_/<url>`) | YES | raw original bytes served without key (not bulk-pulled here) |
| Full-text search (`textsearch?q=...`) | NO (gated) | returns 400: "Please use the following Arquivo.pt APIs... CDX server API / Memento API" |
| Screenshot service (`/screenshot?url=...`) | unverified | HEAD probe timed out; versionHistory emits per-capture screenshot links — treated as API-adjacent, not pulled at scale |
| ArchivePageNow submission endpoint | n/a (write) | not tested; read side is what we used |

Key fingerprint: user-triggered ArchivePageNow saves land in collection **`SAWP5`**
(WARC filenames `save-merged-*`) — the `savepagenow_share` field in each
`timeline/<slug>.summary.json` quantifies how much of a target's capture set
is user-triggered vs background crawl. High SAWP5 share = corroborates
agent-relay use of the capture feature.

## Rate/robustness log

`collect.log.jsonl`: per-query records (host, window, record count, seconds, HTTP status, attempt).
Policy: ≥1.6s between requests; backoff 30/60/180s on 429/503; day-chunk fallback
on fetch timeouts. See "Rate limits hit / blockers" in per-target summaries.

## Standards

- Keep-all + annotate. No invented IDs: every timestamp/URL/digest is verbatim from CDX.
- Agents and agent infrastructure only; no human/operator identity, no re-identification.
- Metadata only (no page bodies pulled).
- Arquivo.pt ToS: educational/scientific/research use — this collection is research.
