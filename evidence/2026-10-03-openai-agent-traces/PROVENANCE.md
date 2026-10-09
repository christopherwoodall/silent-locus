# PROVENANCE — 2026-10-03-openai-agent-traces

**Collection:** `2026-10-03-openai-agent-traces` (index `openai-agent-traces` via
`dataset_override`)

**What:** Mapped Arquivo.pt CDX captures of OpenAI agent relay traffic across
10 incident slugs (4 honest-negative empty sources). 589,972 traces.

**Upstream bytes:** `data/2026-10-01-arquivo-pt/raw/*.cdx.jsonl.gz` — the
2026-10-01 Arquivo.pt pull (adopted from `collections/arquivo-pt`, lane commit
`c0d190d`). Upstream collection is read-only; nothing there was modified.

**Build:** `openai-agent-traces/map_arquivo.py` — deterministic, idempotent
(dedup key `timestamp`+`url`; `trace_id = sha256("arquivo-pt|<slug>|<timestamp>|<url>")`).
`events.jsonl` is a relative symlink to
`openai-agent-traces/data/traces.jsonl` (no copy — copies drift). Re-running
the mapper with unchanged sources rewrites nothing except `state.json`
timestamps.

**Records carry** `event.dataset = "openai-agent-traces"` (registered as
`dataset_override` in `schema/collections.json`). Ingest:
`python3 scripts/push_to_local_es.py --index openai-agent-traces`
(local ES only; hosted ES frozen).

**Per-slug reconciliation** (source rows → deduped → mapped) lives in
`openai-agent-traces/state.json`. Totals: 618,075 source rows → 589,972
deduped/mapped traces, of which 14,940 are `zz=oai<digits>`-tagged DoE captures
(14,941 raw lines; one duplicate key).

**Grading context:** `notes/transluce-us-canada-gov-2026-10-01.md` (incl.
2026-10-03 addendum); hypothesis "Same provider, different agents, different
evals." Scope: agents and agent infrastructure only.
