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
