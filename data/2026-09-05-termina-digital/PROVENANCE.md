# PROVENANCE — termina.digital incident-DB recovery

Lane L (2026-09-28). Read-only archive recovery of the termina.digital swarm
incident database after its live /db/ went dark.

## What happened

- 2026-09-05: thecolony.ai investigators cite termina.digital /db/ as a
  downloadable incident JSONL database.
- 2026-09-28: live termina.digital /db* all 404; swarm.termina.digital /db/
  404, /db/llms.txt 503 ("public exports are temporarily unavailable").
- Recovery path: Wayback CDX for `termina.digital/db*` returned ZERO captures —
  the /db/ never lived on the main domain in archived form. The blog posts
  (Swarmchasing I/II, archived in the site's WASM binary via static strings
  extraction) revealed the DB lives on the subdomain **swarm.termina.digital**.
- Wayback CDX for `swarm.termina.digital*` (collapse=urlkey): 115 rows,
  captures 2026-09-05 → 2026-09-18. Full DB recovered: incidents, campaigns,
  clusters, venues, actors, trackers, about/api/claims/evidence/tips/scan/
  summary, llms.txt, search-config.json, graph.json, search/index.json.

## Files

- `wayback/` — 99 recovered files (12 wayback connection failures; 7 retried
  OK, 3 permanent: bogus `/db/index.html)` CDX row, `/db/page/dse/` dir
  artifact, `/db/search.html?q=xinhai` 404-in-wayback).
- `wayback_manifest.json` — per-file wayback URL, capture timestamp, SHA-256.
- `wayback_cdx_all_2026-09-27.json` — termina.digital CDX (57 rows, no /db/).
- `wayback_cdx_swarm_2026-09-27.json` — swarm.termina.digital CDX (115 rows).
- `swarmchasing-i_20260907.html`, `swarmchasing-ii_20260907.html` — archived
  blog pages (JS-rendered; content empty in HTML).
- `sanctuary-df8ee5ab7c0cfec7_bg_20260907.wasm` — archived WASM (818,387 B);
  blog content embedded as strings (static extraction only, no execution).
- `rss_live_2026-09-27.xml` — live RSS (10 items, descriptions only).
- `swarm_live_home_2026-09-27.html` — live swarm subdomain homepage (WASM app shell).
- `swarm_live_db_2026-09-27.html` / `swarm_live_llms_2026-09-27.txt` — live
  probe negatives (404 / 503).
- `sweep.json` — pattern battery over recovered pages.

## Negatives (recorded, not retried aggressively)

- `agent-pastes-2026-09-08.tar.gz`: 503 both live and in Wayback.
- archive.today: unreachable from this network (timeout); Wayback-only.
- `/db/api/*.json` structured endpoints: never captured by Wayback.

## Attribution scope

The DB is a third-party investigator artifact (ai-safety-lab / rowan+fable).
Claims inside are cited as reported with the DB's own status words
(verified/inferred/reported). No operator identity pursued.

## Closure 2026-09-28 (workstream C)

Closed: complete Wayback recovery of the swarm.termina.digital incident DB —
99 recovered files + RSS + WASM-extracted blog content + live probes = N=107
docs, covering all 115 CDX rows (3 permanent wayback failures recorded in the
provenance, not retried). The live /db/ is dark and the public tarball is a
placeholder, so nothing further is retrievable. ES `termina-digital`
_count=107 verified, schema-drift clean.

## Normalization 2026-09-29 (events.jsonl + rollup.jsonl)

- `events.jsonl`: 223 rows, all schema-conformant.
  - 104 `wayback_capture` — one per `wayback_manifest.json` entry: 99 OK +
    5 failed (incl. the 43-byte HTTP-503 placeholder body for
    `pub/datasets/agent-pastes-2026-09-08.tar.gz`). Per-file capture times
    are NOT in the manifest; they were joined from
    `raw/wayback_cdx_swarm_2026-09-27.json` via lowercased SURT urlkey
    (`digital,termina,swarm)/` + lowercased relpath); all 99 OK files joined.
  - 105 `corpus_hit` — one per (pattern, file) pair in `sweep.json`
    `pattern_files`; 5 `corpus_grep_negative` — the zero-hit patterns
    (tryzz, go_import, chunk_markers, gmail, tty_bitty), which appear in
    `pattern_totals` but not `pattern_files`.
  - 7 `artifact_observation` — rss feed (9 `<item>` observed on disk;
    PROVENANCE text above says 10), live homepage shell, 2 archived blog
    pages, the WASM bundle, 2 CDX dumps; 2 `surface_negative` — live
    /db/ 404 and /db/llms.txt 503 probes.
  - `wayback_manifest.json` is lane bookkeeping (not an event); its `file`
    values still carry the stale `data/termina-digital/wayback/` prefix from
    before the dated-dir move.
- `rollup.jsonl`: 21 rows, `pattern_sweep_rollup` — per-pattern totals from
  `sweep.json` `pattern_totals` (genuine aggregate layer of the battery).
- Fingerprint identity strings: `wayback/<relpath under raw/wayback/>`
  (captures); `failed:<url>` (failed captures with no body);
  `sweep:<pattern>:<file>` / `sweep:<pattern>` (sweep hits/negatives);
  source filename (lane artifacts); `sweep_rollup:<pattern>` (rollup).
- `labels.timestamp_source`: `labels:capture.ts` (CDX-joined capture time);
  `labels:sweep.date` (=2026-09-28 lane date) for sweep rows;
  `labels:retrieved.date` / `labels:archive.date` for lane artifacts.
- New record_kind: `pattern_sweep_rollup`.

## 2026-09-28: ingest script repaired after co-location (hunt convention)
- `es_ingest_termina.py` was co-located from `scripts/` into this directory
  per Christopher's single-collection convention; it transforms the Wayback
  captures (raw/wayback/ + raw/wayback_manifest.json) plus auxiliary
  captures into shared-schema docs (real transform, not a pure loader).
- Path repairs (the script's load path was broken even before the move, and
  the bare move left `REPO_ROOT` resolving one level short): `REPO_ROOT`
  is now three levels up; wayback manifest / walk root / aux files read
  from `raw/` where they live (`D/wayback_manifest.json`, `D/wayback/`,
  `D/<aux>` no longer exist). The manifest URL lookup was also fixed to
  key on D-relative paths (it previously compared absolute walk paths
  against repo-relative manifest entries and never matched).
- Offline verification: `build_docs()` yields 107 docs; 7/7 manifest entries
  carrying a wayback_url now resolve onto their docs.
- `scripts/local_es_manifest.json` via_script entry points here.
- SHA256SUMS regenerated (script file added to coverage).
