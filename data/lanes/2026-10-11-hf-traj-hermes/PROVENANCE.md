# Provenance — 2026-10-11-hf-traj-hermes

Behavioral indicators extracted from the DJLougen hermes-agent-traces-filtered
dataset into Factum. Lane tags on every record:
`lane=2026-10-11-hf-traj-hermes`, `model=multiple-frontier-models`,
`harness=hermes-agent`, `source_dataset=djlougen-hermes-agent-traces-filtered`.

## Source

- Dataset: `DJLougen/hermes-agent-traces-filtered`
  (https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered),
  apache-2.0. Structurally filtered subset of
  `lambda/hermes-agent-reasoning-traces` (7,646 -> 3,679 rows).
- Local bytes:
  `evidence/hf-trajectories/raw/djlougen-hermes-agent-traces-filtered/data/train.jsonl`
  (349 MB, 3,679 rows). Retrieved 2026-10-07T23:55:16Z via curl; dataset
  revision api_card `lastModified: 2026-04-04T21:21:35Z`.
- Row schema (verified on all rows): keys are exactly
  `category, conversations, id, subcategory, task, tools`. There is NO model
  field in any row. Conversation `from` values are ShareGPT-style:
  `system, human, gpt, tool` (not `user/assistant/tool_response`).

## Model and harness identification (verified, not assumed)

- The dataset card's comparison table states "Source model: Multiple
  frontier models". The traces are therefore NOT uniformly hermes; records
  are tagged `model=multiple-frontier-models`.
- Harness is the Hermes/NousResearch function-calling format: system prompt
  describes function signatures inside `<tools>` XML tags, `<tool_call>`
  JSON invocation blocks, `<tool_response>` result blocks. The dataset card
  tags include `hermes`, `agent`, `function-calling`. Records are tagged
  `harness=hermes-agent`.

## Extraction methodology (2026-10-11, streaming)

Script: `extract.py` (lane-local). One streaming pass, row by row; the 349 MB
file is never loaded into memory. Progress in `.work/progress.json`.

1. Function definitions: parsed from BOTH the row-level `tools` JSON field
   AND the system-prompt `<tools>` XML block (plain JSON; parsed on all
   3,679 rows). Result: 26 distinct function names; the two sources agree
   100% (zero mismatch rows). Each function has exactly one description
   variant.
2. Tool invocations: 67,963 `<tool_call>` JSON blocks parsed, 0 failures.
   Names counted per function.
3. URLs: regex `https?://...` over all conversation values; 93,781 mentions,
   20,651 distinct URLs, present in 2,928 rows.
4. Shell-like commands: from `terminal`, `execute_code`, `shell`
   tool-call arguments (`command`/`script`/`code` keys); 24,911 distinct
   commands from 3,227 rows; aggregated by first token (363 distinct).

Notes:

- The task brief's premise "parse the `<tools>` XML in system prompts" holds
  (the XML block is real), but the row-level `tools` field carries the same
  definitions; both were parsed and cross-checked.
- README claims "55 unique tools"; extraction found 26 distinct function
  names. Recorded as an OBSERVED claim, not corrected.
- Notable: `r.jina.ai/http://en.wikipedia.org/...` URLs appear in the traces
  (jina reader relay pattern), captured in the URL records.

## Aggregation (giant-lane rule)

3,679 rows / 67,963 tool calls are aggregated, not ingested 1:1.

- 26 `intel.behavior` observations: one per function (verbatim description +
  corpus frequency: rows defined, invocations).
- 363 `intel.behavior` observations: one per shell first-token (category
  `shell-command`; invocations, distinct-command count, top 5 verbatim
  exemplars).
- 136 `infra.ioc` observations (category `url-pattern`): full URLs with
  >= 50 mentions.
- 50 `infra.ioc` observations (category `domain`): top 50 hosts by mention
  count.
- 1 `source` record (the HF dataset), 1 `run` record (this extraction),
  3 `claim` records (OBSERVED): model non-uniformity, `<tools>`-XML/field
  agreement, 26-vs-55 tool-count discrepancy.

Pre-ingest dedup: in-batch dedup by key field; single-pass exact-term index
over exported Factum batches (`data/records/*/records.jsonl`). Zero exact
term+type duplicates found; nothing skipped.

## Factum ingest

- Bundle: `bundle.json` (idempotency key
  `factum-lane-ingest-2026-10-11-hf-traj-hermes`), built by
  `build_factum_bundle.py`.
- All 575 observations validated against the installed pack schemas
  (urn:factum:intel:behavior:1, urn:factum:infra:ioc:1) with jsonschema
  before submission: 0 invalid.
- `events.jsonl` in this lane is the extraction-run ledger (5 aggregate
  events), not a duplicate of the Factum observations.
- Do NOT push (task directive). Commit state: <pending; filled at ingest>.
