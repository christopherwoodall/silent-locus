# Collection naming schema — silent-locus

Names for datasets under `data/`, and therefore for Elastic indexes
(normally `event.dataset` == collection slug == index name, with
registered `dataset_override`, virtual mappings, and `-rollup` indices
as explicit exceptions, per `schema/record.schema.json`). Machine-readable registry:
[`collections.json`](collections.json). Validation:
`scripts/validate_collections.py` (or `make validate-collections`).

## Form

```
YYYY-MM-DD-<subject>[-<activity>]
```

Every collection dir is prefixed with the date of the **first (earliest)
event** it contains. Records and indices usually carry the dated slug too
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

Canonical layout (2026-09-29):

```
data/YYYY-MM-DD-<slug>/
  events.jsonl      # the event stream — single file, schema-conformant
  rollup.jsonl      # only when a rollup layer exists (feeds the -rollup index)
  PROVENANCE.md
  SHA256SUMS
  raw/              # every non-event data artifact
```

- **events.jsonl** — one file per collection. Collections produced as
  families/shards (e.g. dockerhub's 42 sweep files) are concatenated; each
  record keeps its origin in `labels.file_origin` (the pre-concat filename).
- **rollup.jsonl** — rollup-layer docs feeding the `<slug>-rollup` index.
- **raw/** — captures, manifests, transform inputs, intermediates,
  `evidence/`. Raw files keep upstream/source-native names, are exempt
  from `record.schema.json` (`validate_schema.py` skips them), and are
  covered by `SHA256SUMS` + listed in `PROVENANCE.md`.
- **Build scripts co-locate with their collection.** A script that builds
  records for one collection lives at that collection's root, is listed in
  `PROVENANCE.md`, and is covered by `SHA256SUMS`. Cross-collection builders
  live in `scripts/builders/`. Superseded collection-specific ES loaders are
  preserved under the owning collection's `raw/scripts/legacy/` for audit;
  they are not the ingest path. Historical migration/collection tooling
  lives under `scripts/archive/`. Consult the script index before rerunning
  any builder, since some recorded one-off scripts cannot reconstruct the
  current event file without losing later observations.

Loading is generic: `scripts/push_to_local_es.py` discovers
`events.jsonl`/`rollup.jsonl` in **registered physical collections** under
`data/` and `data/aggregates/` and loads each into the index named by its
records' `event.dataset`. Each complete file must have exactly one dataset;
malformed or mixed files stop ingest before any ES request. Unregistered
directories, raw files and virtual source mappings are not auto-loaded.
`events.jsonl` uses the registry `index` (including `dataset_override`
cases); `rollup.jsonl` uses `<collection>-rollup`. Reference and support
statuses describe the evidence role, **not** an ingest exclusion: every
registered physical collection with event files has a non-null index.
The manifest's staged list is derived, not maintained by hand; `via_script`
must remain empty. Historical builders only produce artifacts, never run
as part of default ingest. Invoke the loader explicitly with `--all`,
`--index <dataset>`, or offline `--dry-run`; `--reset` deletes remote
indices and should be used only deliberately.

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
| `reference` | Recon captures/reference material; staged event files are indexed when present | recommended |
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
6. Every physical collection with staged event-layer records, including
   reference/support/aggregate, has a non-null registry index and is
   discovered for ingest. No `via_script` entry may overlap staged data;
   builder-script ingest is unsupported. A null index is appropriate only
   for collections without staged event files or virtual-only mappings.
7. Aggregate collections live under `data/aggregates/<name>/` and their
   registry `path` field matches.

## Moving/renaming files: keep `file` pointers live

A top-level `file` pointer (`schema/record.schema.json`) is a promise that
the row's source artifact exists on disk: it resolves either
repo-root-relative (starts with `data/`, e.g.
`data/2022-08-09-github-forensics/raw/...`) or collection-relative (e.g.
`raw/...`). A rename/move that leaves pointers at the old location silently
breaks provenance, so:

1. **Any commit that moves or renames files MUST update the `file`
   pointers in every affected `events.jsonl` / `rollup.jsonl`** to the new
   location, and **regenerate `SHA256SUMS`** in the touched collections.
2. Before committing, run `python3 scripts/validate_collections.py` from the
   repo root. Its `file`-pointer pass (full scan of every
   `events.jsonl`/`rollup.jsonl` under `data/`) resolves each pointer and
   reports any that miss as violations, listing the collection, the row's
   `event.id` (or fingerprint), and the bad value. A green run is required;
   do not hand-fix pointers by rewriting history — update the JSONL rows.
