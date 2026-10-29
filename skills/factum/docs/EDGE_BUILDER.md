# Edge Builder

`scripts/edge-builder.py` finds connections between records and surfaces
them as edges. It is generic: it works with any observation type and tag
scheme via CLI configuration.

## What it does

For each observation of the configured type:

1. Extracts the configured term field (dot path, e.g. `data.term`).
2. Matches the term against the corpus with fuzzy search.
3. Filters to hits in a different group (per `--group-tag`).
4. Skips pairs where an edge already exists.
5. Creates edge records for new connections.
6. Reports new connections.

## Usage

```bash
# IOCs grouped by lane
edge-builder.py --repo PATH --type infra.ioc --term-field data.term --group-tag lane

# Captured URLs grouped by lane (dry run first)
edge-builder.py --repo PATH --type web.capture --term-field data.final_url --group-tag lane --dry-run
```

## Options

| Flag | Default | Purpose |
|---|---|---|
| `--repo` | (required) | Factum repository path |
| `--type` | (required) | Observation type to process |
| `--term-field` | `data.term` | Dot path to the matchable value inside `body` |
| `--group-tag` | `lane` | Tag key defining groups; only cross-group edges are created |
| `--min-term-len` | `4` | Skip terms shorter than this (noise control) |
| `--limit` | `100` | Max observations to process per run |
| `--dry-run` | off | Print candidates without creating edges |
| `--actor` | `agent:edge-builder` | Actor recorded on edge submissions |

## Scheduling

Run on a cron for continuous connection discovery:

```bash
# Daily at 06:00 — adjust to the host's cron system
edge-builder.py --repo /path/to/repo --type infra.ioc --term-field data.term --group-tag lane
```

Each run is idempotent: existing edges are loaded first and skipped, so
re-running is safe.

## Noise control

- `--min-term-len` drops short generic terms.
- Cross-group filtering prevents self-links within the same lane.
- Fuzzy matching requires enough of the term to hit; very short or very
  common strings produce no useful edges.
- Review `--dry-run` output before enabling scheduled writes.

## Edge record shape

Edges use the `edge` record kind from factum-core. Each edge records the
source record, target record, and the term that connected them, plus the
actor and tags for provenance.
