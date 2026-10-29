# urlquery marker sweep (ExploitGym incident markers)

Work lane for Lead 4/6: read-only sweep of the urlquery.net public report
corpus for ExploitGym incident markers, to test whether any third-party scans
caught ExploitGym incident traffic in the wild.

## Verdict

No verifiable ExploitGym incident traffic found. 966 unscoped `"exploitgym"`
search-index hits are all low-grade (match location not verifiable via the
public report API). The 9 curated graded findings are benign, context-only,
or low-grade.

## Factum records

Ingested 2026-10-10 (16 records, tagged `{"lane":"urlquery-marker-sweep"}`):

- 1 run: sweep extraction run with honest coverage (966/967 pagination).
- 1 source: this lane's artifacts (`events.jsonl` + `raw/`).
- 4 `infra.ioc` marker terms: `exploitgym` (noisy), `cybergym` (noisy),
  `catflag` (candidate), `restart_server` (retired).
- 9 claims: one graded venue-finding verdict per curated finding
  (byte-identical notes).
- 1 claim: aggregate coverage verdict for the 966 bulk hits.

Per-report rows for the 966 bulk hits stay in `events.jsonl` (aggregation
strategy for the bulk; see FINDINGS.md).

## Artifacts

- `events.jsonl` — 975 venue_finding events (legacy schema).
- `raw/` — verbatim search-response JSON per query (74 files).
- `PROVENANCE.md`, `SHA256SUMS` — acquisition history and manifest.
- `build_events.py` — original event builder; `build_factum_bundle.py` —
  Factum bundle builder with cleaner/validator.

Legacy directory: `evidence/remove-2025-12-04-urlquery-marker-sweep/`
(ingested; safe for later removal).
