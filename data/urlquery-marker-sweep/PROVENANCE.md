# Provenance — urlquery marker sweep (Lead 4/6)

## What
Read-only sweep of the urlquery.net public report corpus (via the urlquery
skill CLI (`skills/urlquery/bin/uq.py`, relative to the operator's workspace), Secure Vault surrogate
auth to `api.urlquery.net` only) for ExploitGym incident markers, to test
whether any third-party scans caught ExploitGym incident traffic in the wild.

## Retrieval
- Retrieved: 2026-09-28 23:36–23:41 UTC (18:36–18:41 CDT).
- Method: `uq.py search --query <Q> --limit 30 [--offset N]` against
  `https://api.urlquery.net/public/v1/search/reports/`; full report bodies
  fetched only for candidate hits (`uq.py report <id>`), 3 bodies total.
- No submissions, no writes to the service. No raw credentials handled;
  auth via the skill's surrogate helpers only.

## Source
- urlquery.net public report corpus (reports visible to the account; public
  + team-accessible). Search semantics per https://urlquery.net/help/search
  (fetched 2026-09-28): plain text searches captured HTML documents and
  JavaScript; `http.url.addr` covers URLs seen in HTTP transactions.

## Query list
Documented in full in `notes/analyst-note-urlquery-marker-sweep-2026-09-28.md`
(sweep v1: 15 queries; sweep v2 with corrected quoted/explicit-AND syntax:
19 queries; v3: 1 query; pagination: 4 requests).

## Artifacts in this directory
- `raw/` — verbatim search-response JSON per query (cache of API results).
- `sweep_summary.json`, `sweep_summary_v2.json` — per-query candidate lists.
- `hits.jsonl` — candidate hits: report_id, report URL, date, marker,
  match location, evidence grade.
- `progress.log` — run log with timestamps.
- `run_sweep.py`, `run_sweep_v2.py` — the exact scripts run (reproducible).
- `SHA256SUMS` — this manifest.

## Caveats
- Search-hit locations for plain-text matches are not always verifiable:
  the search index covers captured HTML/JS text that the public report API
  does not always return. Such hits are graded low and labeled explicitly.
- `hits.jsonl` covers July-relevant candidates plus the single verifiable
  marker-in-URL hit; aggregate counts (e.g. the 134 Appwrite exploitgym
  content hits) are documented in the analyst note, not enumerated per report.
