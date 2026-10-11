# openai-agent-traces

A queryable corpus of **OpenAI agent traces** — Arquivo.pt web-archive captures
of requests that agents issued through the archive's capture feature as a
request relay, collected in the 2026-10-01 pull.

## The working hypothesis (three levels)

> **"Same provider, different agents, different evals."**
>
> - **Same provider = OpenAI.** The common launcher and shared toolkit point
>   here: the `oai*` tags, the `zz=oai<digits>` cache-buster params, the epoch
>   nonces, and the relay choices (Arquivo.pt capture, disposable-email
>   registrations, CORS-laundering proxies).
> - **Different agents = not the same agent instances across incidents.** Each
>   incident cluster is its own set of agent runs; nothing in the bytes lets us
>   tie one incident's runs to another's.
> - **Different evals = different evaluation runs/tasks driving each incident
>   cluster.** E.g. the DoE civilrightsdata cluster is confirmed DeepSearchQA
>   task `dsqa_250` traffic; other incidents' eval/task attributions remain open.

This replaces the earlier "same agents" framing. Per-record attribution fields
(`attribution.provider`, `attribution.eval_family`, `attribution.agent_instance`)
are populated **only where the bytes evidence them** — everywhere else they are
explicitly null. Scope is agents and agent infrastructure only; no human or
operator identity is pursued or recorded.

## What this corpus contains

Mapped from `data/2026-10-01-arquivo-pt/raw/*.cdx.jsonl.gz` (the 2026-10-01
Arquivo.pt pull — read-only, adopted from `collections/arquivo-pt`, commit
`c0d190d`). One record per unique CDX capture (dedup key: `timestamp` + `url`).

| incident slug | what it is | source rows | deduped/mapped | oai-tagged |
|---|---|---|---|---|
| `doe-crdc` | DoE civilrightsdata.ed.gov SQLi/fuzz cluster, Jun 16–18 | 251,778 | 250,822 | **14,940** |
| `kansas-kansasmemory` | Kansas kansasmemory.gov flood, May 7 | 60,842 | 36,496 | 0 |
| `maryland-edstats` | Maryland edu-stats flood, May 6 | 295,963 | 293,898 | 0 |
| `bea-api` | BEA API-key registration flow, Jun 16–18 | 3,006 | 2,988 | 0 |
| `lac-collectionsearch` | Library and Archives Canada probes, May 28 + Jun 9 | 987 | 982 | 0 |
| `navy-history` | Navy history.navy.mil CMS probing, Apr–May | 3,806 | 3,782 | 0 |
| `nysed-enrollment` | NY school-enrollment data, May 17 | 718 | 696 | 0 |
| `illinois-iquery` | Illinois IQuery portal, Apr 19–May 1 | 838 | 171 | 0 |
| `calaccess` | California CAL-ACCESS, May 26 | 111 | 111 | 0 |
| `omb-max` | OMB MAX.gov FY2023 PDFs, May 25–27 | 26 | 26 | 0 |
| `doj-ojjdp`, `sec`, `cdc-wonder`, `texas-dshs` | honest-negative (empty in this pull) | 0 | 0 | 0 |
| **total** | | **618,075** | **589,972** | **14,940** |

Source-row total is 618,075 (the 589,972 figure in the arquivo-pt lane's
`items_collected` is the deduped count; see `state.json` for the per-slug
reconciliation: source rows → deduped → mapped). One note on the DoE oai-tag
count: the raw pull holds **14,941** lines carrying `zz=oai<digits>` (the
addendum's figure), but exactly one of them shares a `(timestamp, url)` key
with another, so the deduped corpus carries **14,940** oai-tagged traces.

The 14,941 `zz=oai<digits>` raw DoE lines (all dated 20260617, 14,449 distinct
tag values; 14,940 after dedup) are the OpenAI-attributed core and are emitted
first in `data/traces.jsonl`. Transluce reported "10,000+" — the bytes hold
14,941 raw / 14,940 unique.

### Incident → Transluce claim mapping

- `doe-crdc` → Transluce claims 3 (SQLi cluster) and 16 (`oai*` tags):
  CORROBORATED in our bytes (was ABSENT before the Arquivo.pt lane).
- `lac-collectionsearch` → claim 4: the 982 captures include the 13 documented
  payloads (`sqli_probe`, `xss_probe`, `integer_overflow_probe`, `fuzz_probe`
  flags in `features.probe_flags`).
- `kansas-kansasmemory`, `maryland-edstats`, `bea-api` → claims 5, 8, 12:
  volumes reproduce Transluce's published counts within expected raw/dedup deltas.
- `omb-max`, `nysed-enrollment`, `illinois-iquery`, `navy-history`, `calaccess`
  → claims 9, 6, 8, 10, 8.
- `doj-ojjdp` (claim 11), `sec` (claim 14), `cdc-wonder` (claim 15),
  `texas-dshs` (claim 7): honest negatives — 0 captures in this pull.

## Files

- `map_arquivo.py` — idempotent mapper (re-runs resume from `state.json`,
  never duplicate, never invent rows; deterministic `trace_id`).
- `data/traces.jsonl` — the mapped corpus (one JSON object per line).
- `state.json` — per-slug watermarks and counts (source rows → deduped →
  mapped), run status.
- `SCHEMA.md` — CDX → corpus field mapping and divergences.
- `../data/2026-10-03-openai-agent-traces/` — collection wrapper for the repo
  ES loader: `events.jsonl` is a symlink to `data/traces.jsonl` here; records
  carry `event.dataset = "openai-agent-traces"`.

## Elasticsearch

Index: **`openai-agent-traces`** (records' `event.dataset`; registry
`dataset_override` on collection `2026-10-03-openai-agent-traces`).

Ingest command (local ES only — hosted is frozen):
`python3 scripts/push_to_local_es.py --index openai-agent-traces`

Status 2026-10-03: local ES unavailable in this session (no Docker daemon, no
local ES binaries, empty `elk/data`) — staged files + exact commands left in
place; see report. No doc-count verification performed yet.

## Provenance

- Bytes: Arquivo.pt CDX API, pulled 2026-10-01 (`collections/arquivo-pt`,
  `PROVENANCE.md` there).
- Grading context: `notes/transluce-us-canada-gov-2026-10-01.md` (incl.
  2026-10-03 addendum).
- DeepSearchQA linkage: `collections/deepsearchqa` (dsqa_250 confirmed).
- All existing corpora/exports treated as read-only.
