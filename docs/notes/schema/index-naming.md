# Index and collection naming schema

One dataset gets one base name. Every processing layer is a suffix on that
base name. Same convention applies to Elastic indexes and to on-disk
collections (`data/<dataset>/`).

## Layers

| Suffix | Layer | Contents |
|---|---|---|
| `-raw` | 0 | Raw captures exactly as retrieved (HTML snapshots, API response bodies). Immutable — never edited after capture. |
| `-events` | 1 | **Explicit events.** One document per observable source event/row. This is the canonical primary layer. Never consolidated, never summarized. |
| `-enriched` | 2 | Events plus derived fields: decoded payloads, joins against other datasets, enrichment annotations. Optional — only built when a lane needs it. |
| `-rollup` | 3 | Summaries and aggregations for dashboards (per-day, per-slug, per-campaign). Support indexes only. |
| `-graph` | 4 | Graph projections: nodes and edges for network views. |

## Rules

- `-events` is the canonical layer. It holds explicit events only, per the
  standing explicit-events policy ("we eat explicit events; we consolidate
  in support indexes").
- Summaries live **only** in `-rollup`, never in `-events`.
- Dataset-specific fields go under `labels`. No new top-level fields without
  updating the schema file (`schema/`).
- Every document carries `event.dataset` set to its full index/collection
  name, so a doc is self-describing about which layer it belongs to.
- Disk layout mirrors the index names: `data/<dataset>/raw/`,
  `data/<dataset>/<dataset>-events.jsonl`, etc.

## Migration

Today's bare primaries predate this convention and become `-events` at the
planned remote index rebuild:

| Today | After rebuild |
|---|---|
| `admin-deletions` | `admin-deletions-events` |
| `admin-deletions-rollup` | `admin-deletions-rollup` (unchanged) |
| `university-shorteners` | `university-shorteners-events` |
| `university-shorteners-rollup` | `university-shorteners-rollup` (unchanged) |
| `rubygems-goimport-campaign` | `rubygems-goimport-events` |

`-rollup` names are already correct and stay as-is.
