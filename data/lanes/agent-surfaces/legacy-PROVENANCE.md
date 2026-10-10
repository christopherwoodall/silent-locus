# PROVENANCE — agent-surfaces lane (Lane H, 2026-09-28)

Lane report: notes/agent-surfaces-2026-09-27.md. Raw captures in
data/2026-09-28-agent-surfaces/<slug>/ (homepage, llms.txt, agent docs), each with
pages.json, per-dir PROVENANCE.md, progress.log. Capture script:
scripts/capture_agent_surfaces.py; ES ingest: scripts/es_ingest_agent_surfaces.py.

## Closure 2026-09-28 (workstream D)

Bounded census complete: the 11 surfaces named in public-board.com field
notes, each captured read-only (homepage, llms.txt, agent docs). N=11 docs
(surface_capture) is the complete list — no more named surfaces exist in
the source list. ES `agent-surfaces` _count=11 verified. The note's open
follow-ups (full-dataset pulls for the 6 board surfaces, paste-lane
enumeration, bitily alias lane) are recorded as concrete next steps in
notes/agent-surfaces-2026-09-27.md, not orphaned.

## Schema backfill 2026-09-29 (normalization sweep, worker W4)

- Built `events.jsonl`: 87 records, one per captured page (`raw/<surface>/pages.json`, 11 surfaces).
- record_kind: `venue_probe`. Fingerprint identity string: `agent-surfaces|<surface_slug>|<page_url>` (sha256).
- @timestamp = page `retrieved_at_utc` (the probe observation is the event); labels.timestamp_source=`retrieved_at_utc:probe_observation`. `page.ok=false` pages kept with their HTTP status.
- Surface base from each `raw/<surface>/PROVENANCE.md` `base_url:` line.
- `rollup.jsonl`: 11 rows, one per surface (record_kind `venue_finding`, event.dataset `2026-09-28-agent-surfaces-rollup`): pages_ok/pages_total, first/last probe, content types. Fingerprint identity: `agent-surfaces-rollup|<surface_slug>`.
- Regenerated `SHA256SUMS` (events.jsonl + rollup.jsonl + raw/**).

## Build-script relocation 2026-09-29 (ingest-script condensation)

- Moved `scripts/es_ingest_agent_surfaces.py` into this collection dir per Christopher's build-script convention (single-collection build scripts live in `data/YYYY-MM-DD-<slug>/`).
- Path fixes in the moved script: `REPO_ROOT` now resolves three levels up from the collection dir; `resolve_data_dir()` returns this file's own parent (the glob over `data/*-agent-surfaces` was dropped).
- ES ingest driver: `push_to_local_es.py --all` runs the path in `scripts/local_es_manifest.json` `via_script` for index `2026-09-28-agent-surfaces`; manifest entry updated to the new script location.

## Orphan run-log reconciliation (preservation-first)

The following original logs were relocated byte-for-byte from `data/2026-01-25-agent-surfaces/` into this collection. They are historical run evidence, not additional positive findings or new collection events. Original source folders were removed only after their logs were copied and SHA-256 verified.

- `data/2026-01-25-agent-surfaces/raw/agentgateway/progress.log` -> `raw/agentgateway/progress.log`; SHA-256 `0b163545f25d8088d77f85b9756c9cee944b11464cb7418f0e9ddbd1b34c3f46`.
- `data/2026-01-25-agent-surfaces/raw/agentsboard/progress.log` -> `raw/agentsboard/progress.log`; SHA-256 `ee8287df724754f0f1e0e012418b5799b1a5c542e80499cd53908aa71e96255e`.
- `data/2026-01-25-agent-surfaces/raw/aiforum-grok/progress.log` -> `raw/aiforum-grok/progress.log`; SHA-256 `e0170a49a6819d54fc2302a3bd89a33a61c703ff83db325f1b8d0c322d7fffb0`.
- `data/2026-01-25-agent-surfaces/raw/bitily/progress.log` -> `raw/bitily/progress.log`; SHA-256 `587dca1e6a0723d603574da700d8afb202fa38389e3340f6aeaa2d96bc3d8a82`.
- `data/2026-01-25-agent-surfaces/raw/facehuggers/progress.log` -> `raw/facehuggers/progress.log`; SHA-256 `4225a05127393a219510b8e56559e34199a2cfb8bac0004851bba22b58c42939`.
- `data/2026-01-25-agent-surfaces/raw/jotspot/progress.log` -> `raw/jotspot/progress.log`; SHA-256 `3381edc12985f6b420d4a4dd5ce69b3138c9b93536a69aa5dba689b674c48e85`.
- `data/2026-01-25-agent-surfaces/raw/messageboardforaiagents/progress.log` -> `raw/messageboardforaiagents/progress.log`; SHA-256 `558ab3590d26e8ff229161e59ecb8d2360953724a82972d50633faddaba4cc24`.
- `data/2026-01-25-agent-surfaces/raw/nervesocket/progress.log` -> `raw/nervesocket/progress.log`; SHA-256 `4c1a8dafa44cf1d1a7ac2a6b8f622c1d6d56adb0ff5aec88a2e55c345ddc6e9d`.
- `data/2026-01-25-agent-surfaces/raw/nullyard/progress.log` -> `raw/nullyard/progress.log`; SHA-256 `04a82763b516a398e6c7d58a6791f41aaf59cc0a7f80f93dff08d4606198671d`.
- `data/2026-01-25-agent-surfaces/raw/pastebin-tarcseh/progress.log` -> `raw/pastebin-tarcseh/progress.log`; SHA-256 `c16e4c32a367a093177fdafff68ac0f039419b8a395f0c59cd3ba1fc73f8c597`.
- `data/2026-01-25-agent-surfaces/raw/she-llac/progress.log` -> `raw/she-llac/progress.log`; SHA-256 `f8ebed6ca3cbb0cbf50e411da819aca0cfba9afbc1ebe1b1c87b5968afe2dc5a`.

## Ingest script input-path correction

`es_ingest_agent_surfaces.py` now reads `raw/<slug>/pages.json` and `raw/<slug>/PROVENANCE.md` from this collection, rather than the nonexistent collection-root `<slug>/` directories. Its updated SHA-256 is `4b5003c3391bd53f63146246e8a95e000c73a4cfff44d825d95310256f8db58b` in `SHA256SUMS`; the captured evidence was not modified.

### Historical checksum conflicts (unresolved)

Bytewise verification of `SHA256SUMS` currently reports 59 mismatched historical entries in this collection; 59 match their recorded hashes only after CRLF-to-LF conversion. This is consistent with a line-ending change, but original evidence and recorded historical hashes were not rewritten. The newly recovered log entries were independently verified byte-for-byte against their source SHA-256 and match the new manifest lines. To enumerate all mismatches locally, run `sha256sum -c SHA256SUMS` from this collection directory. 

## Historical loader relocation (2026-09-30)

Preserved `es_ingest_agent_surfaces.py` at `raw/scripts/legacy/es_ingest_agent_surfaces.py` as a historical, optional Elasticsearch loader; it is not an active collection event builder. Its local path resolution now targets the same collection and repository inputs from the archived location. No source evidence, `events.jsonl`, or `rollup.jsonl` was changed; no network or ES actions were run. The SHA256SUMS entry records the relocated script bytes.
