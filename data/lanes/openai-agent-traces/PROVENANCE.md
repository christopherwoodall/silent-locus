# Provenance — openai-agent-traces

## Capture history

The captures come from the legacy lane `evidence/2026-10-03-openai-agent-traces/`
(now `evidence/remove-2026-10-03-openai-agent-traces/`, tombstone only). The
original lane provenance is kept verbatim in `legacy-PROVENANCE.md`. Key facts:

- Mapped Arquivo.pt CDX captures of OpenAI agent relay traffic across 10
  incident slugs (4 honest-negative empty sources). 589,972 traces.
- Upstream bytes: `data/2026-10-01-arquivo-pt/raw/*.cdx.jsonl.gz` — the
  2026-10-01 Arquivo.pt pull (lane `2026-10-01-arquivo-pt`, already ingested as
  Factum lane with per-slug `dataset.snapshot` records in
  `hidden_files/factum-batches/2026-10-01-arquivo-pt/bundle.json`).
- Build: `openai-agent-traces/map_arquivo.py` — deterministic, idempotent
  (dedup key `timestamp`+`url`; `trace_id = sha256("arquivo-pt|<slug>|<timestamp>|<url>")`).
  `events.jsonl` is a relative symlink to `raw/traces.jsonl` (no copy —
  copies drift). sha256 of `raw/traces.jsonl`:
  `afd22d6d7aa8939b2b691967db3e16df2de41fc9c5df79140517e3cccfa66ee3`
  (matches `SHA256SUMS`).
- 2026-10-10: the `events.jsonl` symlink was dropped from the Factum lane
  directory because the Factum scanner fails on any symlink under `data/`
  (SYMLINK). Canonical byte location is `raw/traces.jsonl` in this lane.
- `raw/traces.jsonl` (893 MB) is git-ignored (GitHub 100 MB limit) and stays
  local-only; only the small artifacts are committed.
- Per-trace attribution rule (from the lane mapper): `provider=openai` and
  `eval_family=deepsearchqa/dsqa_250` only where the captured URL carries
  `zz=oai<digits>`; `agent_instance` never attributed (no row-level evidence).

## Aggregation methodology (2026-10-10, before ingest)

The 589,972-row corpus is too large for per-trace Factum ingest, so this lane
uses census aggregation, not sampling:

1. Streamed `raw/traces.jsonl` once (Python file iteration, no full load)
   and counted: per-slug rows, per-day/hour rows, status/mime/collection
   distributions, distinct `trace_id` check, top domains, top query-param
   names, and per-slug `zz`/`zzbulk`/`prepnonce` marker-param counts
   (scripts in `/tmp`, results cached in the bundle tags).
2. A second streaming pass sampled `zz=` values on the non-`oai` rows to
   characterize the `zz` grammar beyond the `oai<digits>` prefix.
3. No values were redacted or truncated; aggregates are exact row counts.

Record plan (mirrors the `2026-10-01-arquivo-pt` giant-lane precedent):

- 1 `source` record: Arquivo.pt CDX API (upstream of the mapped corpus).
- 1 corpus-level `dataset.snapshot` observation: all 589,972 traces,
  `coverage=complete`, `revision=<sha256 of traces.jsonl>`.
- 10 per-slug `dataset.snapshot` observations (one per incident slug),
  each with trace count, oai-tagged count, time range, host list, status
  and mime distributions in tags.
- 1 `run` record describing the `map_arquivo.py` mapping run.
- 6 `claim` records (OBSERVED x5, INFERENCE x1) citing the snapshots.

Dedup vs the corpus: the `2026-10-01-arquivo-pt` lane already holds
per-slug snapshots of the *upstream CDX pull*. These records describe the
*derived mapped trace corpus* (deduped trace_ids, zz-tag attribution) — a
different dataset. Verified with `match --text "openai-agent-traces"`,
`match --text "doe-crdc"`, and `match --text "oai17816846804506724"`
before ingest; no overlapping records found.

## Factum ingest

- Ingested 2026-10-10 by agent:lane-ingest/openai-agent-traces.
- All records carry `tags.lane = "openai-agent-traces"`.
- Claims are graded OBSERVED / INFERENCE in the record `basis` field and
  cite the snapshot records by `@ref`.

## Batch records

- `data/records/43bd7d95dd174f9c8799dc65586c6ed0/` — 19 records:
  1 `source`, 11 `dataset.snapshot` observations (corpus + 10 slugs),
  1 `run`, 6 `claim` (5 OBSERVED, 1 INFERENCE).
- Bundle: `hidden_files/factum-batches/openai-agent-traces/bundle.json`
  (idempotency key `lane-ingest-openai-agent-traces-v1`).

Lane record: `lane_33298ba30b5846a49bc28a6d6decadaa`.
