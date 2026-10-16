# Transluce finding #182 — provenance

Tracker finding #182, submitted 2026-10-15T22:16:48+00:00 by Eric Clay.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/182`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/182`
- Retrieved: 2026-10-16T11:58:15Z (UTC)
- Method: `tl.py finding 182` via the `custom.transluce` connector
  (Secure Vault bearer token), run by the `lab-intel-transluce-scan` hook;
  verified verbatim against this run's census pull.
- sha256: `cd948ef4c86c4f3d5b67e41e3ef5b510e027b019b9f4ad03b39e4cb81aa57b53`
- Cached: `data/lanes/2026-10-09-transluce-intel/raw/finding-182_20261016T115805Z.json`
  (with `.sha256` and `.PROVENANCE.txt`), copied here to `raw/` for lane
  self-containment.

## Census verification (this run, 2026-10-16 08:40 CDT)

- Full paginated census `GET /api/findings?limit=25&offset=N`: 115
  findings, IDs 36..182 (IDs 175, 177 absent from the tracker).
- Per-item canonical-JSON sha256 vs the 06:57 CDT hook census
  (`findings-list-20261016T115714Z.json`): byte-identical, zero diffs.
- vs 2026-10-15 watermark (112 findings, IDs 36..179): only delta is
  findings 180/181/182; no content changes to any pre-existing finding.

## Content

Summary: "Between September 26 and October 9, 2026, URLquery's public scanner was used 49 times to look up data on the China Customs statistics portal (stats.customs.gov.cn): 45 direct scans and 4 one-off helper pages on brewpage.app. The lookups asked for 2025 import figures for specific"

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

1. `fetch-proxy-abuse` — URLquery's public scanner was used as a remote browser for 49 lookups of the China Customs statistics portal (stats.customs.gov.cn) between September 26 and Oct...
2. `restriction-circumvention` — The customs portal answers a first automated visit with an HTTP 412 refusal; a revise-and-retry loop through brewpage.app helper pages got past it: three versio...

Finding evidence links:

- `https://urlquery.net/report/ee680e22-146c-4db3-95ba-01c0e345e5af`
- `https://urlquery.net/report/4af932ee-0e8a-41fd-8fa4-30f0dfca92b3`
- `https://urlquery.net/report/4f2ab464-dc40-426c-94ed-a6b14138f135`
- `https://urlquery.net/report/0fa7b417-9d5e-404c-8c65-b38a9ba18799`
- `https://urlquery.net/report/fc2bc108-cd16-4e52-8ea1-9cea817c449a`

## Attribution note

Attribution is the finder's own: `ai_company` = "Unknown".
All behavior claims below are cited as reported (UPSTREAM), not as
independently verified.
