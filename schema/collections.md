# Collection naming schema — silent-locus

Names for datasets under `data/`, and therefore for Elastic indexes
(`event.dataset` == collection slug == index name, per
`schema/record.schema.json`). Machine-readable registry:
[`collections.json`](collections.json). Validation:
`scripts/validate_collections.py` (or `make validate-collections`).

## Form

```
YYYY-MM-DD-<subject>[-<activity>]
```

Every collection dir is prefixed with the date of the **first (earliest)
event** it contains. Because `event.dataset` == collection slug == index
name, records and indices carry the dated slug too
(`2026-09-28-commonlog-scan`). Lowercase, hyphens only — no underscores,
no dots. ES index names may start with a digit.

Date derivation chain (first hit wins, recorded in the registry `date`
field and PROVENANCE.md):

1. earliest non-sentinel `@timestamp` in the event files
2. earliest `event.created`
3. earliest date found in the collection's `raw/` files
4. date of the collection's `notes/<slug>-YYYY-MM-DD.md` or PROVENANCE.md
5. none of the above — flagged and dated manually

Legacy date *suffixes* fold into the prefix: what would have been
`yourls-resweep-2026-09-28` is `2026-09-28-yourls-resweep`. Re-runs of
the same activity get their own dated dir; the registry `series` field
groups runs of one subject.

## Activity suffixes

The suffix says what kind of work produced the collection. Registry in
`collections.json` (`activities`); add new ones there and here together.

| Suffix | Use for | Examples |
|---|---|---|
| `-scan` | Point-in-time pattern match over a fixed corpus | `commonlog-scan` |
| `-sweep` | Iterative enumeration across a surface or set | `agents-relay-sweep`, `nsi-venue-sweep` |
| `-hunt` | Open-ended search across external sources | `gomod-hunt`, `forged-flag-hunt` |
| `-pivot` | Following one IOC/fingerprint into a new surface | `pastebin-pivot`, `gem-temporal-pivot` |
| `-check` | Verifying a specific hypothesis | `hf-tampering-check` |
| `-capture` | Archived external content (Wayback, snapshots) | `wayback-gem-capture` |
| `-census` | Counting/enumerating a population | `xss-ssti-census`, `dockerhub-trojan-images` |
| `-forensics` | Deep reconstruction of a specific artifact set | `github-forensics`, `july7-gem-forensics` |
| `-test` | Pipeline/mechanism probes | `separate-eval-test`, `transfer-test-family` |

A **bare subject** (no activity suffix) is a canonical primary dataset:
`collusion-wiki`, `counter-channel`, `webhook-deaddrops`, …

## Layer suffixes

Processing layers append after the collection name and are defined by
`notes/schema/index-naming.md`: `-raw`, `-events`, `-enriched`, `-rollup`,
`-graph`. They always come last; an activity suffix comes before them
(`university-shorteners-events`, not `university-shorteners-events-sweep`).

## Date prefix

Superseded by the date-prefix form above (2026-09-29): every collection
dir is `YYYY-MM-DD-<subject>[-<activity>]`, dated by its first event.

## File layout inside a collection

Two layers per collection directory:

- **Event layer** — JSONL records conforming to `schema/record.schema.json`,
  loadable into ES. Event files are named `<dataset>.jsonl` or
  `<dataset>-<variant>.jsonl` (variant = shard/family, lowercase,
  hyphens): `proxy-primitives.jsonl`, `dockerhub-trojan-images-final-n132-arvo.jsonl`.
- **Raw layer** — `data/<collection>/raw/` holds pre-event source material:
  script-consumed transform inputs, upstream captures, source tables. Raw
  files **keep their upstream/source-native names** (provenance stays
  traceable) and are exempt from `record.schema.json`
  (`validate_schema.py` skips them), but they must be covered by the
  collection's `SHA256SUMS` and listed in its `PROVENANCE.md`.

Decision rule for a pre-schema file: if a script consumes it as input, or
it is an upstream capture, it is raw layer → `raw/`. Otherwise it is a
final output → backfill it onto the event schema in place.

## Aggregates

Multi-source conglomerates (records aggregated from other datasets, not a
primary source) live under `data/aggregates/<name>/` with registry
`"class": "aggregate"` and `"path": "data/aggregates/<name>"`. Current:
`proxy-primitives`, `cors-bwa-proxy`, `overlap-analysis`,
`gem83-reconciliation`. Aggregate indexes keep the plain collection slug
(no `aggregates-` prefix in ES).

## Reserved directories

- `data/raw/` — datasets as published, untouched.
- `data/processed/` — normalized working copies.
- `data/site-captures/<host>/` — read-only surface captures keyed by host
  (the old `*_llms.txt` dirs live here now). Not datasets: no slug rules,
  no index. Each capture keeps its `surface_capture.json` metadata.
- `data/aggregates/` — container for aggregate collections (above). Not a
  dataset itself.
- `<collection>/raw/` — raw layer (above).

## Statuses (registry `status` field)

| Status | Meaning | PROVENANCE/SHA256SUMS |
|---|---|---|
| `canonical` | Primary corpus collection, has (or will have) an index | required |
| `support` | Rollups, graph projections, link tables, source tables | required |
| `reference` | Recon captures/reference material, no index planned | recommended |
| `pending-relocation` | Owned by another project (the RubyGems go-import collection); tracked here until it moves | n/a |

## Rules validated by `scripts/validate_collections.py`

1. Every `data/` entry is a registered collection, a reserved dir, or a
   registered loose file. Nothing unregistered.
2. Collection names match the form above.
3. Canonical/support collections carry `PROVENANCE.md` + `SHA256SUMS`
   (warning-level until the backfill lands).
4. No loose JSONL at `data/` root unless registered in `loose_files`.
5. Sampled records' `event.dataset` equals the collection name (or its
   `dataset_override`). Records with no `event.dataset` yet are reported
   as "pending backfill", not failures. Files under `raw/` are exempt
   (raw layer).
6. Every collection with event-layer records is loadable: registered in
   `scripts/local_es_manifest.json` or explicitly `index: null`
   (support/aggregate collections are exempt from this warning).
7. Aggregate collections live under `data/aggregates/<name>/` and their
   registry `path` field matches.
