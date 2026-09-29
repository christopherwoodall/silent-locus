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
