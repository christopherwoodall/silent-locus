---
configs:
- config_name: default
  data_files:
  - split: full
    path: full.parquet
  - split: hard
    path: hard.parquet
---

# WebArena-Verified

## Dataset description

WebArena-Verified is a curated benchmark dataset of web tasks designed for reproducible
evaluation of web agents across multiple realistic websites.

## Sources

- GitHub repository: [webarena-verified](https://github.com/web-arena-x/webarena-verified)
- Original WebArena benchmark: [webarena.dev](https://webarena.dev)

## Splits

- `full`: 812 rows
- `hard`: 258 rows

## Tasks per site

Counts below are task counts grouped by category. Tasks with more than one site are grouped
under `multi-category` to avoid double-counting.

### Full split

| Site | Tasks |
| --- | ---: |
| `gitlab` | 180 |
| `map` | 109 |
| `reddit` | 106 |
| `shopping_admin` | 182 |
| `shopping` | 187 |
| `wikipedia` | 0 |
| `homepage` | 0 |
| `multi-category` | 48 |

### Hard split

| Site | Tasks |
| --- | ---: |
| `gitlab` | 57 |
| `map` | 0 |
| `reddit` | 42 |
| `shopping_admin` | 55 |
| `shopping` | 56 |
| `wikipedia` | 0 |
| `homepage` | 0 |
| `multi-category` | 48 |

## Schema notes

The table below reflects inferred column types from the `full` split during artifact generation.

| Column | Type |
| --- | --- |
| `sites` | `List(Value('string'))` |
| `task_id` | `Value('int64')` |
| `intent_template_id` | `Value('int64')` |
| `start_urls` | `List(Value('string'))` |
| `intent` | `Value('string')` |
| `intent_template` | `Value('string')` |
| `instantiation_dict` | `Value('string')` |
| `eval` | `Value('string')` |
| `revision` | `Value('int64')` |

## Metadata

- Version: `v1.2.3`
- Git commit: `6473f72db5dcefc97b5725b59e734504edc28a21`
- Generated at (UTC): `2026-02-07T22:44:22Z`
- Dataset hash: `0e90f3feabe68cb9c7285e6989e36862a47622e7ac81b562f3126152350cb5ac`
- License: `Apache-2.0`
- Language: `en`
- Task categories: `web-navigation`, `information-retrieval`

## Notes

- Expected split counts: `full=812`, `hard=258`
- If custom split names are not supported by the Dataset Viewer, use one config per split
  mapped to `train` as a compatibility fallback.
