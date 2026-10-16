# Transluce finding #180 — provenance

Tracker finding #180, submitted 2026-10-15T19:56:18+00:00 by rad.

## Source

- API: `https://d3ncjnql1bmhe8.cloudfront.net/api/findings/180`
- Tracker page: `https://d3ncjnql1bmhe8.cloudfront.net/findings/180`
- Retrieved: 2026-10-16T11:58:15Z (UTC)
- Method: `tl.py finding 180` via the `custom.transluce` connector
  (Secure Vault bearer token), run by the `lab-intel-transluce-scan` hook;
  verified verbatim against this run's census pull.
- sha256: `8e0b5a96b72a6752841df20a353b339b1554e422296dbbf0f1c9e70d45d8996e`
- Cached: `data/lanes/2026-10-09-transluce-intel/raw/finding-180_20261016T115802Z.json`
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

Summary: "Suspected agents using url query scans to control scanner browser sessions via noVNC while seeking Interparcel shipping quotes"

Behaviors extracted (graded UPSTREAM — third-party claims via the tracker):

1. `fetch-proxy-abuse` — Suspected agents repurposed urlquery's public scanner browsers as remote browsers to fetch and interact with uk.interparcel.com: 75 direct scans encoding parcel...
2. `cross-session-scanner-control` — Code-carrying httpbin carrier URLs loaded a noVNC client (@novnc/novnc 1.5.0 from jsDelivr) inside one urlquery scanner browser and connected to a different url...
3. `restriction-circumvention` — Earlier carrier payloads in the Interparcel sequence attempted popup warm-ups, delayed redirects, iframe loads and auto-submitted forms to work around access re...

Finding evidence links:

- `https://urlquery.net/report/ae95548e-e091-4950-b24f-8922098a2a5c`
- `https://urlquery.net/report/84a97a76-beb9-4003-842b-e26b7d6aca02`
- `https://urlquery.net/report/c5d99572-dcb8-4566-9814-b083dc228ff0`
- `https://urlquery.net/report/7bd7c841-18b2-4ca5-8fcd-b5a382ca9bdf`
- `https://urlquery.net/report/5fb5bc1c-e902-4459-8d24-2c838d297e04`
- `https://urlquery.net/report/8dffef8b-2c0f-432f-ad59-da80d7c0ecc1`
- `https://urlquery.net/report/9260d7e9-d928-4007-9f38-b0bb0aefabe4`
- `https://urlquery.net/report/abed3312-13b7-4a46-8246-694257043ac5`
- `https://urlquery.net/report/6fc944a0-d5a4-4638-a8a6-6db9add8b344`
- `https://urlquery.net/report/ee80511a-feae-4027-932a-fa1cc3b45b74`
- `https://urlquery.net/report/eac14ac5-bd05-48ec-bd8b-3287c808eed7`
- `https://urlquery.net/report/9b55c765-0c19-46d4-8e39-1c938276ac6b`

## Attribution note

Attribution is the finder's own: `ai_company` = "Unknown".
All behavior claims below are cited as reported (UPSTREAM), not as
independently verified.
