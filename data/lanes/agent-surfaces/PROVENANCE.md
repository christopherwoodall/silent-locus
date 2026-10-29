# Provenance

## Capture history

The captures come from the legacy lane `evidence/2026-09-28-agent-surfaces/`
(now `evidence/remove-2026-09-28-agent-surfaces/`). The original lane
PROVENANCE.md is kept in this lane directory. Key facts:

- Captured 2026-09-28 with scripts/capture_agent_surfaces.py. Read-only GET
  probes of 11 surfaces named in public-board.com field notes.
- 87 probes in events.jsonl. Each probe has a page URL, an HTTP status, a
  SHA-256 hash, and a byte count where the page loaded.
- 11 rows in rollup.jsonl. One per surface. Each row gives pages_ok,
  pages_total, first and last probe times, and content types.

## Factum ingest

- Ingested 2026-10-10 by agent:lane-ingest/agent-surfaces.
- `venue_probe` records became `reachability.check` observations. The probe
  target is the requested page URL. The outcome uses the installed enum
  (response, connect_failure, timeout). The 4 probes with no HTTP status
  keep their exact error text from raw/*/pages.json.
- `venue_finding` rows became `dataset.snapshot` observations. The
  dataset_uri is the surface base URL. Coverage is complete for the bounded
  page set. The row count is pages_total.
- All observed values are verbatim from raw/*/pages.json. The doubled
  charset parameter in some content types is the observed value, not an
  error. No values were redacted.

## Batch records

- data/records/87583a3389394850b8e74c0a03fc440b (probes 1-44)
- data/records/3f00e10a03e44186aeeae115d7123c87 (probes 45-87)
- data/records/dc755db70cc141c095e426d4f0a4b623 (11 rollup snapshots)

Lane record: lane_7d10547c0de34948bb56cbbc232fe221.
