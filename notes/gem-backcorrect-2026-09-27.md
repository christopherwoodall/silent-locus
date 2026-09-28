# Gem corpus back-correction — 2026-09-27

**Directive (Christopher):** the gem corpus is OUR separate Diffend
collection, NOT part of the SwarmTraces dataset. Every record must say so.
Audit + corrections applied 2026-09-27. Bulk harvest still running at time
of writing — nothing was moved; relocation happens after it finishes.

## Corrections applied (in place)

1. **README.md** — added "RubyGems go-import campaign collection
   (SEPARATE — pending relocation)" section: declares the gem files an
   independent Diffend-sourced collection, names the future project home
   and the `rubygems-goimport-campaign` Elastic index.
2. **notes/rubygems-rescan-2026-09-27.md** — provenance banner at top:
   independent Diffend-sourced collection (May 11–12, 2026 go-import
   meta-tag injection campaign); SwarmTraces referenced only as a
   comparison corpus for bridge checks (all negative).
3. **notes/gem-pipeline-test.md** — provenance header: tooling/data serve
   the independent Diffend collection, not SwarmTraces.
4. **notes/gems-es-mapping.json** — already carried the rename note
   (bulk agent applied); index field = `rubygems-goimport-campaign`.
5. **scripts/es_ingest_gems.py** — docstring said `swarmtraces-gems`;
   fixed to `rubygems-goimport-campaign` (INDEX constant was already
   correct).
6. **scripts/fetch_gems.py** + **scripts/harvest_diffend.py** — HTTP
   User-Agent was `swarmtraces-research/1.0` (sent on every request to
   rubygems.org/Diffend, externally attributing our traffic to
   SwarmTraces research). Renamed to `rubygems-goimport-research/1.0`.
   Note: harvest_diffend.py was mid-run; the edit takes effect on future
   invocations only — the running process already imported the old UA.
7. **data/gem-pins-diffend.txt** — added `# PROVENANCE:` comment
   (harvester skips `#` lines; verified at scripts/harvest_diffend.py:205).

Audit method: full-text grep for `swarmtraces` across all gem files.
Remaining hits are legitimate: the new disclaimers themselves, one
bridge-check negative ("No evidence connects it to the SwarmTraces agent
corpus"), the factual BASE path in es_ingest_gems.py (updated at move
time), and the README's own description of the actual SwarmTraces project.

## Name verdict: `rubygems-goimport-campaign` — BLESSED

- **ES naming rules:** 25 chars, all lowercase `[a-z-]`, no leading
  `-`/`_`, under 255 bytes — fully valid.
- **Collision check (live, 2026-09-27 via elastic-cloud skill,
  `_cat/indices`):** only `urlquery-incidents` and `urlquery-hunt`
  exist. No collision; no gem/ruby/diffend near-matches.
- **Semantics:** names the source registry (`rubygems`), the payload
  mechanism (`goimport`), and the entity type (`campaign`). Kebab-case
  matches existing indices (`urlquery-incidents`, `urlquery-hunt`).
- **Provenance:** carries no `swarmtraces` token — satisfies the
  correction structurally.
- **Rejected alternatives:** `swarmtraces-gems` (provenance violation);
  `diffend-gems` (Diffend is the retrieval source, not the subject —
  the campaign is a RubyGems phenomenon).

Approved for: dataset name, Elastic index name, project directory name.

## Relocation manifest (AFTER the bulk run finishes — do not move early)

Target: `../rubygems-goimport-campaign/`
(mirror the current layout: `data/`, `scripts/`, `notes/`).

**data/ → data/**
- `data/raw/gems/` — 608 reconstructed `.gem` tarballs (~5 MB)
- `data/processed/gems/` — pilot static-extraction trees
- `data/gem-ioc-log.jsonl` — per-gem JSON log (download/extraction/diffend_harvest)
- `data/gem-ioc-hits.jsonl` — per-file + per-metadata IOC hits
- `data/gem-graph-nodes.jsonl` / `data/gem-graph-edges.jsonl` — hunt-schema graph
- `data/gem-pins-diffend.txt` — the 608-pin target list (supersedes batches)
- `data/gem-pins-batch1.txt` … `batch4.txt` — pilot batches (superseded, keep-all)

**scripts/ → scripts/**
- `scripts/fetch_gems.py` (rubygems.org path; kept for method record)
- `scripts/harvest_diffend.py` (the working Diffend harvester)
- `scripts/mine_gems.py` (static miner)
- `scripts/es_ingest_gems.py` (Elastic ingest)
- Leave `scripts/__pycache__/` behind (regenerable).

**notes/ → notes/**
- `notes/rubygems-rescan-2026-09-27.md`
- `notes/gem-pipeline-test.md`
- `notes/gems-es-mapping.json`
- `notes/gem-backcorrect-2026-09-27.md` (this file)

**Post-move fixups (do at relocation):**
1. `scripts/es_ingest_gems.py` line 24: hardcoded
   `BASE = ".../swarmtraces-hf-corpus"` → new project path.
   (Other scripts compute BASE from `__file__` — they adapt automatically.)
2. `data/gem-ioc-log.jsonl`: 15 pilot `extraction` records embed the old
   absolute `extracted_to` path (`.../swarmtraces-hf-corpus/data/processed/gems/...`).
   NOT touched now (bulk agent is writing this file). At relocation:
   rewrite to the new path or reduce to relative — a one-line sed/python pass.
3. New project gets its own `README.md` + provenance record
   (source: my.diffend.io; seed: Christopher's 2026-09-27 screenshots;
   method: read-only diff harvest; corpus: 555 gems / 608 pins).
4. Remove the "SEPARATE — pending relocation" section from the old
   README.md once the move is done (or convert it to a pointer).
5. `.pre-bulk` backup files (`data/gem-*.pre-bulk`) are pilot-era
   snapshots — move with the corpus, not the old project.

## Outstanding (not mine to do in this pass)

- The running bulk agent's UA for its current harvest is the old
  `swarmtraces-research/1.0` string (imported before the edit). Cosmetic
  only; future runs use the corrected UA.
- ES ingest targets `rubygems-goimport-campaign` (already steered).
