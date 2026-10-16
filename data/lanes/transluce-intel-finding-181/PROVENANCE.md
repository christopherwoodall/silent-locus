# Transluce finding #181 — provenance

Tracker finding #181, submitted 2026-10-15T20:14:10+00:00 by rad.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/181`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/181`
- Retrieved: 2026-10-16T11:58:15Z (UTC)
- Method: `tl.py finding 181` via the `custom.transluce` connector
  (Secure Vault bearer token), run by the `lab-intel-transluce-scan` hook;
  verified verbatim against this run's census pull.
- sha256: `1cca672a3ae68891eb0ba58aac42b7def8039b694b514a10483f2a64f20a8d04`
- Cached: `data/lanes/2026-10-09-transluce-intel/raw/finding-181_20261016T115804Z.json`
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

Summary: "On 2026-10-13, urlquery scans show Microlink running custom browser code against api.usaspending.gov. The code POSTed Base64-encoded queries to the TAS quarterly-balances API and got FY2023 public data back."

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

1. `fetch-proxy-abuse` — Microlink's hosted browser was used as a proxy to run custom Base64-obfuscated JavaScript against api.usaspending.gov. The function uses page.evaluate to decode...
2. `restriction-circumvention` — A direct request of the same function to api.usaspending.gov (2026-10-13 14:46:41 UTC) showed 'Web Page Blocked!'; the same function was then routed through api...

Finding evidence links:

- `https://urlquery.net/report/2b13a1fe-a885-49eb-bc26-973199f60b20`
- `https://urlquery.net/report/02d3343a-9131-4461-bfe4-371fb123af13`
- `https://urlquery.net/report/ac1276ce-239e-4caa-9ef7-aaf2b582c92a`

## Attribution note

Attribution is the finder's own: `ai_company` = "Unknown".
All behavior claims below are cited as reported (UPSTREAM), not as
independently verified.
