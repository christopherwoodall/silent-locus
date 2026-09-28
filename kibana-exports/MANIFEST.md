# Kibana Dashboard Exports — Manifest

Exported: **2026-09-28 02:19 UTC** via `export_dashboards.py` (Kibana Saved Objects `_export` API, `includeReferencesDeep: true`).

## Dashboards (7)

| Dashboard | Export file | Objects | ES index pattern |
|---|---|---|---|
| Graph & IOCs | `dashboard-graph---iocs-2026-09-28T021937Z.ndjson` | 1 index-pattern, 7 visualizations, 1 search, 1 dashboard | `urlquery-hunt*` |
| 01 · Scope & Tempo | `dashboard-01---scope---tempo-2026-09-28T021937Z.ndjson` | 1 index-pattern, 5 visualizations, 1 dashboard | `urlquery-hunt*` |
| 02 · The Laundering Machine | `dashboard-02---the-laundering-machine-2026-09-28T021937Z.ndjson` | 1 index-pattern, 2 visualizations, 1 search, 1 dashboard | `urlquery-hunt*` |
| 03 · Targets & Evidence | `dashboard-03---targets---evidence-2026-09-28T021937Z.ndjson` | 1 index-pattern, 2 visualizations, 1 search, 1 dashboard | `urlquery-hunt*` |
| 04 · The Incident Archive | `dashboard-04---the-incident-archive-2026-09-28T021937Z.ndjson` | 1 index-pattern, 4 visualizations, 1 search, 1 dashboard | `urlquery-incidents*` |
| Gem Burst — Overview | `dashboard-gem-burst---overview-2026-09-28T021937Z.ndjson` | 1 index-pattern, 7 visualizations, 1 dashboard | `rubygems-goimport-campaign*` |
| Gem Payloads — Mechanism | `dashboard-gem-payloads---mechanism-2026-09-28T021937Z.ndjson` | 1 index-pattern, 5 visualizations, 1 dashboard | `rubygems-goimport-campaign*` |

Also included: `all-dashboards-2026-09-28T021937Z.ndjson` (all 7 dashboards + deep references, single file, 114,765 bytes) and `export-summary-2026-09-28T021937Z.json`.

## Verification

- Every NDJSON line parses as JSON.
- Every dashboard's `references` resolve to object IDs present in the same export file — **zero missing references** on all 7.
- Export trailers report `missingRefCount: 0`, `excludedObjectsCount: 0` on all 7.
- The final line of each NDJSON is the export summary trailer (`exportedCount`, `missingRefCount`, `missingReferences`) — expected, not an error.

## Pending

- **collusion-wiki dashboards**: not yet built (wiki-ingest lane still running). Re-run `export_dashboards.py` when they land; it uses fresh timestamped filenames and never overwrites.

## Restore

Import any file via Kibana → Stack Management → Saved Objects → Import, or `POST /api/saved_objects/_import`. Index patterns are included, so dashboards restore against the same index names.
