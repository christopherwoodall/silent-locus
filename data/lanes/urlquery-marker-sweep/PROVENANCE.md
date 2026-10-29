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

## Continuation 2026-09-29: full pagination of the unscoped `"exploitgym"` query
- Retrieved: 2026-09-29 ~09:55–10:00 UTC (04:55–05:00 CDT), single operator session.
- Method: `uq.py search --query '"exploitgym"' --limit 30 --offset N` for
  N = 30, 60, ..., 960 (32 pages), saved verbatim as
  `raw/v2_exploitgym_unscoped_off<N>.json` in the same response format as the
  original sweep. Polite pacing: 3s sleep between requests (~7s/request wall).
- `total_hits` stayed 967 on every page; no rate limiting, no failures.
- Coverage: the off-0 page returns only 29 rows despite limit=30, so
  pagination covers 966 distinct report IDs out of the reported 967. A probe
  fetch at offset 966 (`raw/v2_exploitgym_unscoped_off966.json`, 1 row)
  returned an ID already seen on the off-960 page (result-window drift) — the
  remaining 1 hit is not addressable via stable pagination. Recorded honestly:
  966/967 distinct captured.
- No cross-page duplicates among the 32 new pages; the v1 and v2 off-0 copies
  are the same 29 rows.
- events.jsonl extended: 966 one-per-hit `venue_finding` events added via
  `build_events.py` (marker=exploitgym, evidence_grade=low — search-index
  match, match location not verifiable via the public report API, per the
  collection caveat). Fingerprint = sha256(report_id), same as the backfill.
  9 original curated events preserved; 975 events total, all report_ids distinct.
- Scope unchanged: read-only, public search API only, no submissions.

## Schema backfill 2026-09-29
- Transform: `temp/backfill_w2.py`. Pre-schema flat records brought onto the
  shared schema. Renames: `report_url` -> `source_url`, `notes` -> `note`;
  `report_id`, `marker`, `location`, `evidence_grade` -> `labels`.
- `@timestamp` = original `date` field (report scan time, UTC Z);
  `labels.timestamp_source = "labels:date"`.
- record_kind: `venue_finding` (a marker finding surfaced from the
  urlquery.net public report corpus; no more specific registry kind exists).
- fingerprint identity string: `sha256(report_id)` — the urlquery report UUID
  is the natural unique key per record.
- event.dataset = `urlquery-marker-sweep`; event.created = backfill run time.
