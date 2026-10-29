# openai-agent-traces

Factum lane for the 2026-10-03 OpenAI agent traces corpus: 589,972 mapped
Arquivo.pt CDX traces of agent relay traffic across 10 incident slugs,
2026-04-19 to 2026-06-18.

## Layout

- `legacy-PROVENANCE.md` — original lane provenance (verbatim).
- `PROVENANCE.md` — capture history + aggregation methodology + ingest log.
- `FINDINGS.md` — graded summary claims about the corpus.
- `SHA256SUMS` — manifest (`raw/traces.jsonl` sha256
  `afd22d6d7aa8939b2b691967db3e16df2de41fc9c5df79140517e3cccfa66ee3`).
- `events.jsonl` — symlink to `raw/traces.jsonl` (no copy).
- `raw/traces.jsonl` — 589,972 traces, 893 MB, local-only (git-ignored).
- `lane.json` — Factum lane record (created by `lane new`).

## Factum records

`hidden_files/factum-batches/openai-agent-traces/bundle.json` — 19 records,
all tagged `{"lane":"openai-agent-traces"}`:

- 1 `source` (Arquivo.pt CDX API)
- 1 corpus `dataset.snapshot` + 10 per-slug `dataset.snapshot` observations
- 1 `run` (map_arquivo.py mapping)
- 6 graded `claim` records (5 OBSERVED, 1 INFERENCE)

Only 14,940 traces (2.5%) are attributed to a provider
(`zz=oai<digits>` → OpenAI, deepsearchqa/dsqa_250, all doe-crdc, all
2026-06-17). The rest is unattributed relay traffic.
