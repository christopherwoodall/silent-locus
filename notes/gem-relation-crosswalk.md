# Gem↔hunt relation crosswalk — 2026-09-27

The gem corpus (`rubygems-goimport-campaign`, independent Diffend-sourced
collection) uses two edge verbs that are not in the frozen hunt's 30-verb
vocabulary. Per the schema review (notes/gem-schema-review-2026-09-27.md
§A.3) they are **kept as-is** — the hunt's own vocab grew organically and
there is no closed enum to conform to. This doc records the crosswalk for
dashboard faceting across both corpora.

| Gem verb | Triple shape | Hunt analogue | Notes |
|---|---|---|---|
| `exhibits` | gem→indicator, file→indicator | `demonstrates` (12 hunt uses) | "X exhibits indicator Y" ≈ "X demonstrates Y". Gem corpus also uses it gem→indicator directly (metadata IOCs), where the hunt would hang indicators off incidents. |
| `contains` | gem→file | inverse of `part_of` (23 hunt uses) | "gem contains file" ≈ "file part_of gem" reversed. Facet as `part_of⁻¹` when joining. |

Node-type crosswalk (for the same dashboards):

| Gem node type | Hunt mapping (per review §A.1) |
|---|---|
| `gem` (native) | ECS `threat.indicator.type=[software]`; `labels.gem.node_type=gem`. Hunt precedent: its own `gem-package` subtype → `software`. Join key: `package` (bare name) ↔ hunt `gem-package` nodes. |
| `file` (native) | Entity doc, `labels.gem.node_type=file`. No hunt equivalent — do not force into `indicator`. |
| `indicator` | Shared. Campaign-specific subtypes (`go-import`, `council-domain`, …) follow the hunt's campaign-subtype pattern (`yourls-slug`, …). |

Confidence crosswalk (hunt `ecs-mapping.md` §3.2, gem miner now emits hunt words only):

| Gem confidence | STIX scale |
|---|---|
| `confirmed`, `high` | High |
| `likely` (was `medium`) | Medium |
| `lead` (was `low`) | Low |

Status: burst gems are `status=dead` (yanked from rubygems.org), matching the
hunt's `live|dead|unknown` status semantics.
