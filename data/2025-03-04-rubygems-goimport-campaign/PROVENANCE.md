# rubygems-goimport-campaign — provenance

Support inputs for the RubyGems go-import campaign investigation
(lanes B–E in notes/). Status: pending-relocation — this directory is a
pre-move staging area and will relocate to the sibling repo
`../rubygems-goimport-campaign/` (see README.md). The ES index keeps the
name `rubygems-goimport-campaign`.

| File | Origin |
|---|---|
| gem-ioc-log.jsonl[.pre-bulk] | download / extraction / diffend_harvest log records (mine_gems.py, harvest_diffend.py) |
| gem-graph-nodes.jsonl[.pre-bulk] | IOC graph nodes (mine_gems.py) |
| gem-graph-edges.jsonl[.pre-bulk] | IOC graph edges (mine_gems.py) |
| gem-ioc-hits.jsonl[.pre-bulk] | IOC hits against gem sources |
| gem-iocs-2026-09-27.jsonl | IOC snapshot, 2026-09-27 (wiki_ioc_pivot.py) |
| gem-june18-wayback.jsonl | wayback machine metadata for June-18 gems (fetch_gems.py) |
| gem-pins-batch1..4.txt | pinned malicious gem versions, discovery batches |
| gem-pins-diffend.txt | pinned versions confirmed via Diffend |
| gemstuffer-jfrog-2026-09-27.csv | saved from https://research.jfrog.com/gemstuffer.csv on 2026-09-27 (https://research.jfrog.com/post/gemstuffer-openai-rubygems/) |

ES ingest: scripts/es_ingest_gems.py + scripts/es_ingest_jfrog.py
(via_script transforms; deterministic _ids documented in those files).
`.pre-bulk` files are pre-ingestion snapshots kept for diffing.

## Raw layer 2026-09-29

All JSONL/txt/csv data files moved to `raw/` keeping upstream names (they
are script-consumed inputs/captures; files under `raw/` are exempt from
`schema/record.schema.json`):

- `gem-graph-nodes.jsonl` + `gem-graph-nodes.jsonl.pre-bulk` -> `raw/`
- `gem-graph-edges.jsonl` + `gem-graph-edges.jsonl.pre-bulk` -> `raw/`
- `gem-ioc-hits.jsonl` + `gem-ioc-hits.jsonl.pre-bulk` -> `raw/`
- `gem-ioc-log.jsonl` + `gem-ioc-log.jsonl.pre-bulk` -> `raw/`
- `gem-iocs-2026-09-27.jsonl` -> `raw/`
- `gem-june18-wayback.jsonl` -> `raw/`
- `gem-pins-batch1.txt` .. `gem-pins-batch4.txt`, `gem-pins-diffend.txt`
  (5 files) -> `raw/`
- `gemstuffer-jfrog-2026-09-27.csv` -> `raw/`

Only `PROVENANCE.md` remains at the collection root. Script references
(e.g. `scripts/es_ingest_gems.py`, `scripts/mine_gems.py`,
`scripts/sweep_proxy_primitives.py`, `scripts/audit_gem_counts.py`) are
patched centrally by the orchestrator. Note: `gem-graph-nodes.jsonl` and
`gem-ioc-log.jsonl` received the 2026-09-28 schema backfill before this
move; that content is unchanged, they now live in the raw layer as
pipeline inputs.

## Schema normalization 2026-09-29 (worker W3)

- Transform: `temp/build_events_w3_gems.py` (repo root passed as argv[1]).
- Grain (10,421 event records):
  - `gem-graph-nodes.jsonl` -> 2,830 `graph_node` records (2026-09-28 backfilled
    rows re-keyed: `event.dataset` set to this collection, fingerprints recomputed
    with the identity below)
  - `gem-ioc-log.jsonl` -> 1,262 records (`download` / `extraction` / `diffend_harvest`)
  - `gem-ioc-hits.jsonl` -> 2,339 `corpus_hit` records (2,341 raw lines, 2
    byte-identical duplicate lines deduped)
  - `gem-iocs-2026-09-27.jsonl` -> 334 `wiki_ioc_pivot` records
  - `gem-june18-wayback.jsonl` -> 16 `wayback_capture` records
  - `gem-pins-batch1..4.txt` + `gem-pins-diffend.txt` -> 615 `campaign_specimen`
    records (deduped across files; 7 bare-name pins in batch4 kept with
    `gem.version: null`; per-file provenance in `labels.pin.sources`)
  - `gemstuffer-jfrog-2026-09-27.csv` -> 3,025 `campaign_specimen` records
    (one per row; multi-version cells split into `labels.gem.versions[]`)
- Excluded (documented, not deleted):
  - `*.pre-bulk` — earlier snapshots; verified the pre-bulk node ids are a strict
    subset of the current set (169/169), so events carry the latest snapshot only.
  - `gem-graph-edges.jsonl` (3,096) — edges are relationships, not events; no
    registry kind covers them; per schema/README.md joins live in support indexes.
- `@timestamp`: node first_seen / log retrieved/extracted/published times / IOC
  first_seen / wayback published_at (each with `labels.timestamp_source`);
  the documented hunt date 2026-09-27 for hits, pins, and JFrog rows
  (per-record timestamps absent from raw).
- Fingerprint identity strings:
  - nodes: `sha256("gem-graph-node:<node.id>")`
  - ioc-log: `sha256("gem-ioc-log:<kind>:<name>@<version>:<ts>")`
  - hits: `sha256("gem-ioc-hit:<gem>@<version>:<family>:<line_no>:<matched_string>")`
  - iocs: `sha256("gem-ioc:<ioc>:<source_link>")`
  - wayback: `sha256("gem-wayback:<gem>@<version>")`
  - pins: `sha256("gem-pin:<name>==<version>")` (bare-name pins: `sha256("gem-pin:<name>")`)
  - jfrog: `sha256("gemstuffer-jfrog:<Package>")`
  - rollup: `sha256("gem-day-rollup:<YYYY-MM-DD>")`
  Reference method verified against data/2023-11-14-hfspace-proxies
  (sha256("TheNacken/python-cors-proxy") -> `14c645d9…efbe94`).
- Rollup: `rollup.jsonl` with 5 `campaign_day_rollup` rows (NEW kind, listed in
  notes/dir-triage-W3.md) — per-day graph aggregates: node counts, campaign-gem
  counts, distinct packages, per-IOC-family counts, first/last. Days: 2025-03-04
  (90 baseline nodes), 2026-01-06 (43), 2026-05-11 (216, rehearsal wave, 48 gems),
  2026-05-12 (2,456, main wave, 567 gems), 2026-09-09 (25). `event.dataset`
  suffixed `-rollup`.
- `event.dataset = "2025-03-04-rubygems-goimport-campaign"`; `event.created` = build time.

## Ingest-script consolidation 2026-09-29

Per the single-collection convention, the collection's ES ingest scripts moved
from `scripts/` into this directory (names kept):
`es_ingest_gems.py` (transforms raw gem-ioc-log.jsonl / gem-ioc-hits.jsonl /
gem-june18-wayback.jsonl into the diffend-harvest / extraction / hit / wayback
doc flavors) and `es_ingest_jfrog.py` (transforms the raw JFrog CSV +
same-collection wave lookup into the jfrog_inventory flavor). `REPO_ROOT` in
both now resolves from the new location (was `dirname(dirname(__file__))` from
`scripts/`). Verified post-move: `load_docs()` builds 2,358 docs.
`via_script` entry in `scripts/local_es_manifest.json` updated to the new paths.

## Ingest-script health note 2026-09-29 (es_ingest_gems.py + es_ingest_jfrog.py)

Both scripts moved here per the single-collection convention, but both are
currently BROKEN against the backfilled `raw/gem-ioc-log.jsonl` (schema
backfill 2026-09-28 moved the original harvest-log fields under `labels.*`
with dotted keys, e.g. `labels["gem.name"]`, `labels["diffend.versions.diff_ts"]`;
the scripts still read top-level `gem`/`version`/`diffend_versions`):

- `es_ingest_gems.load_docs()`: log flavors (download/extraction/
  diffend_harvest) read `gem=None`, so ~1,800 log records collapse into 3
  garbage docs (`log:download:None:None` etc., `package=None`). The hit
  (2,339 docs) and wayback (16 docs) flavors still build correctly because
  `gem-ioc-hits.jsonl` / `gem-june18-wayback.jsonl` were NOT backfilled.
- `es_ingest_jfrog.load_docs()`: `corpus_wave_lookup()` finds 0 gems (was 562
  verified overlaps on 2026-09-27), so all 3,025 `jfrog_inventory` docs get
  the fallback timestamp and `in_diffend_corpus=false`.

The collection's staged `events.jsonl` + `rollup.jsonl` are auto-discovered by
`push_to_local_es.py discover_staged()` and remain the source of truth.
Flagged as delete-or-repair candidates: deleting (per the timeline_anchors
precedent) or repairing the label-key reads is the parent's call. Until then,
the `via_script` manifest entries are landmines — the driver would bulk-load
the garbage docs into the live index.

## Repair 2026-09-29 (es_ingest_jfrog.py) -- REPAIRED, verified by dry-run

The 2026-09-29 health note above is superseded for `es_ingest_jfrog.py` only
(`es_ingest_gems.py` remains broken -- sibling worker's lane).

What was broken (specific lines/fields, pre-repair script):
- `corpus_wave_lookup()` read `r.get("record_kind")` (fine), then
  `r.get("gem")` and `r.get("diffend_versions", [])` -- both gone in the
  2026-09-28 backfill. Gem name now lives at `labels["gem.name"]`, publish
  time at `labels["published.at"]` (ISO), with the original Diffend strings
  kept in `labels["diffend.versions.diff_ts"]`. Result: lookup found 0 gems
  (was 562 verified overlaps on 2026-09-27), so all 3,025 `jfrog_inventory`
  docs would have gotten the all-fallback timestamp
  `2026-09-27T00:00:00.000Z` with `in_diffend_corpus=false`, overwriting the
  good docs in the index.
- Doc shape pre-dated the schema: dataset-specific fields sat at top level
  (`gem`, `package`, `versions`, `version_count`, `xray_id`,
  `in_diffend_corpus`, `wave`, `csv_source_url`), which
  `schema/record.schema.json` forbids (additionalProperties:false;
  dataset-specific fields belong in `labels`).

What the repair does:
- `corpus_wave_lookup()` now reads the backfilled dotted keys
  (`labels["gem.name"]`, `labels["published.at"]`), with fallback to
  `labels["diffend.versions.diff_ts"]` (old "May 12, 2026 03:32" format) and
  then the log row's `@timestamp`; keeps the EARLIEST publish time per gem
  (the old script kept the first row seen, not the earliest).
- Dataset-specific fields moved into `labels.*` dotted keys
  (`gem.name`, `gem.versions`, `gem.version_count`, `gem.xray_id`,
  `gem.in_diffend_corpus`, `gem.wave`, `gem.timestamp_source`,
  `gem.status`); top level carries only schema-allowed fields
  (`@timestamp`, `event`, `record_kind`, `fingerprint`, `labels`,
  `payloads`, `source_url`, `file`, `retrieved_at`, `description`,
  `status`, `tags`, `observer`, `note`).
- Timestamp policy: overlap rows get the real Diffend publish time
  (`labels["gem.timestamp_source"]` records the exact read path); rows with
  no recoverable date use the CSV acquisition date `2026-09-27T00:00:00Z`
  with an explicit `dataset:csv_retrieval_date` source -- never "now".
- Fingerprint identity string (new; deterministic): `jfrog_inventory|<gem>`
  (sha256 hex). ES `_id` unchanged (`jfrog:<gem>`), so loads stay idempotent.
- Added `--build [PATH]`: builds docs to disk JSONL with zero network calls
  and validates every doc against `schema/record.schema.json` (required
  fields, closed top-level/event shapes, labels flatness + key pattern,
  payload item shape, fingerprint and `@timestamp` formats). `--verify`
  updated to the new labels paths. Default (no-flag) behavior unchanged:
  `update_mapping()` + `bulk_load()` + `verify()`.

Payload-embedding choice (per the 2026-09-29 repair directive):
- Payloads go in the schema's top-level `payloads` array (added to
  `schema/record.schema.json` in commit 37988db, documented in
  `schema/README.md`) -- NOT in `event.payloads` (does not exist; `event`
  has additionalProperties:false) and NOT in `description`.
- Two entries per row: `inventory_row` (`text/csv`, the raw CSV line,
  embedded fully -- rows are small) and `wave_attribution` (`text/plain`,
  the derived package/versions/Xray-ID/wave/date/overlap attribution).
  Both carry `encoding: "text"`, `truncated: false`, `byte_size`, and
  `sha256` of the full body, per the schema's payload convention.

Dry-run verification 2026-09-29 (`--build`, no Elastic writes):
- 3,025/3,025 docs built -- matches the 3,025 baseline exactly.
- Overlap: 562 docs with real Diffend publish times (560 via
  `labels["published.at"]`, 2 via the `diffend.versions.diff_ts` fallback);
  0 overlap docs on the fallback timestamp. Wave labels: 562 `may-12`.
- 2,463 jfrog-only docs with the honest CSV-acquisition timestamp.
- Schema validation: 3,025/3,025 ok. `python3 -m py_compile` clean.
- Reconciliation vs the JFrog report prose (3,022 packages / 3,315
  name-version pairs): the saved CSV snapshot holds 3,025 rows / 3,323
  pairs (+3 packages, +8 pairs) -- the build is faithful to the source
  artifact (`raw/gemstuffer-jfrog-2026-09-27.csv`, saved 2026-09-27), which
  is slightly larger than the prose counts.

Not run against live Elastic (hosted write freeze in effect); the repaired
script is ready for the next authorized `--load`.

## es_ingest_gems.py repair 2026-09-29

Repaired (not deleted) per the 2026-09-29 repair directive. The script was
broken by the 2026-09-28 schema backfill; run as-is it would have written
garbage docs (gem=None everywhere, non-schema top-level fields).

What was broken (specific reads):
- `load_docs()` read `r["gem"]`, `r["version"]`, `r["published_at"]`,
  `r["download_url"]`, `r["diff_url"]`, `r["diffend_versions"]` at top level.
  After the backfill these live at `labels["gem.name"]`,
  `labels["gem.version"]`, `labels["published.at"]`, top-level `source_url`,
  `labels["diff_url"]`, and the parallel arrays
  `labels["diffend.versions.version"]` / `labels["diffend.versions.diff_ts"]`.
  All reads remapped (the hits file `gem-ioc-hits.jsonl` was never backfilled
  and keeps its flat format -- handled as such).
- `enrich_common()` overwrote `doc["labels"]` with a fresh dict, wiping the
  backfilled native labels (gem.name, file manifests, diffend version
  arrays). Now merges into the existing labels dict.
- Emitted non-schema top-level fields (`package`, `wave`, `published_at`,
  `diffend_versions`) -- moved into `labels` (wave, gem.status,
  gem.timestamp_source) or dropped (package duplicates labels gem.name).
- Hit docs passed the raw IOC family name ("council-domain", ...) through as
  `doc["fingerprint"]`, failing the 64-hex fingerprint rule. Now computed as
  sha256("gem-ioc-hit:<gem>@<version>:<family>:<line_no>:<matched_string>")
  (same identity as the W3 normalization); the family name is kept at
  `labels["hit.ioc_family"]`. Record kinds aligned with the canonical
  events.jsonl: `hit` -> `corpus_hit`, wayback rows -> `wayback_capture`.
- Never emits None-valued optional fields (3 failed-harvest rows lack
  diff_url/version; 4 wayback rows lack wayback_url; 12 lack description).

Payloads (schema commit 37988db: OPTIONAL top-level `payloads`, NOT
event.payloads): each doc carries one payload -- the byte-exact raw source
record (kinds `gem_ioc_log_entry` / `gem_ioc_hit` / `wayback_metadata_record`,
content_type `application/json`, encoding `text`, with `truncated`,
`byte_size`, `sha256` of the full body). Truncation cap 64 KiB
(`PAYLOAD_TRUNCATE_AT`); no current row exceeds ~11 KiB, so all 3,594
payloads are full (`truncated: false`). Larger artifacts are NOT duplicated:
the extracted gem trees at `data/processed/gems/<name>-<version>/` are
skeletal Diffend reconstructions (1-byte placeholder gemspecs, tiny lib
stubs) whose manifests already live in labels `files.path/size/sha256` --
the tree path is kept as the file pointer (top-level `file` on extraction
docs, `labels["extracted.to"]` everywhere). `.gem` binaries (3 control
downloads) and June-18 Wayback HTML were never archived in this repo;
`source_url` is the file pointer.

Dry-run verification 2026-09-29 (`--emit`, no Elastic writes, no network):
- 3,594 docs built: 3 download + 618 extraction + 618 diffend_harvest +
  2,339 corpus_hit + 16 wayback_capture. (Raw log has 635 extraction /
  624 harvest rows; 15 re-harvest keys collapse to last-wins on the
  deterministic `_id`, as documented.)
- `scripts/validate_schema.py`: 0 violations; strict Draft7 check against
  `schema/record.schema.json`: 0 violations (3,594/3,594).
- Non-degraded: 0 docs with gem.name=None; 3,594/3,594 real @timestamps
  (no fallbacks); all fingerprints 64-hex; 3,587/3,587 applicable docs with
  source_url (7 legitimately absent: failed harvests / wayback rows missing
  URLs in the source); every payload's sha256 re-verified against its
  content; 618/618 extraction docs carry the `file` pointer.
- `python3 -m py_compile` clean.

Merge decision: NOT merged with es_ingest_jfrog.py. The sibling worker
already repaired and committed jfrog.py standalone (2584dee); both scripts
now follow the same conventions (backfill-aware label reads, schema-valid
docs, top-level payloads with the raw source line, `file` as artifact
pointer) and build disjoint record flavors for the same index. Merging
would churn a finished, committed repair for no functional gain.

Not run against live Elastic (hosted write freeze in effect); the repaired
script is ready for the next authorized load. SHA256SUMS regenerated.

## Notes-farm addition (2026-09-29, notes-farm worker)

452 new records appended to `events.jsonl`, mined from `notes/` prose that
never made it into `data/`:

- 334 `ioc_inventory_entry` (from `notes/gem-iocs-2026-09-27.md`): the
  frozen-hunt IOC inventory — 305 URLs, 13 domains, 2 proxy domains, 1 IP,
  5 gem-package names, 6 file hashes, 2 beacon strings. Aggregate layer over
  the corpus_hit rows (different record kind/identity:
  `ioc-inventory-2026-09-27|<type>|<ioc>`); gem-package names have zero
  pre-existing records. 3 URL rows were truncated in the note itself and are
  marked `ioc.truncated_in_note`.
- 26 `finding` (from `notes/gem-apikey-disclosure-2026-09-27.md`): API-key
  reuse clusters (12, with redacted 12-hex prefixes only), 13 singletons,
  and the corrected census (54 versions / 25 prefixes; supersedes earlier
  3-key and 44-key figures). No pre-existing api-key records.
- 23 `pattern_sweep_rollup` (from `notes/gem-metadata-deepdive-2026-09-27.md`
  and `notes/gem-harvest-final-2026-09-27.md`): go-import VCS/field/proxy
  tallies, 16 target clusters, 6 prefix exceptions, final corpus stats,
  family census, fingerprint census, lib/ deviation audit.
- 5 `run_shape` (from `notes/gem-timeline-expansion-2026-09-27.md`): burst
  phases 0/1/2, generate→publish lead, version-bump iteration.
- 25 `finding` (from `notes/gem-deaddrops-2026-09-27.md`): dead-drop beacon
  protocol, mission comments, 403/exfil ops logs, status-signal flags,
  version-progression signals, theater files. Existing beacon references
  were only wiki_ioc_pivot strings — no protocol analysis duplicated.

Validation: 0 violations after addition. SHA256SUMS regenerated.

## Historical loader relocation (2026-09-30)

Preserved `es_ingest_gems.py` at `raw/scripts/legacy/es_ingest_gems.py` as a historical, optional Elasticsearch loader; it is not an active collection event builder. Its local path resolution now targets the same collection and repository inputs from the archived location. No source evidence, `events.jsonl`, or `rollup.jsonl` was changed; no network or ES actions were run. The SHA256SUMS entry records the relocated script bytes.

## Historical loader relocation (2026-09-30)

Preserved `es_ingest_jfrog.py` at `raw/scripts/legacy/es_ingest_jfrog.py` as a historical, optional Elasticsearch loader; it is not an active collection event builder. Its local path resolution now targets the same collection and repository inputs from the archived location. No source evidence, `events.jsonl`, or `rollup.jsonl` was changed; no network or ES actions were run. The SHA256SUMS entry records the relocated script bytes.
