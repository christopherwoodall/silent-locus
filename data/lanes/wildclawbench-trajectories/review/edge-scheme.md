# WildClawBench Trajectories — Edge Scheme

Linked factum records for the 26 verified WildClawBench trajectory findings
(lane `wildclawbench-trajectories`, ingested 2026-10-16). Built by
`build_bundle.py`, which regenerates `bundle.json` from
`review/surviving-findings.jsonl` plus the cached session bytes.

## Record types per finding

Each finding becomes a small graph (219 records total for 26 findings):

| Kind | Type | Ref | Purpose |
|------|------|-----|---------|
| observable | `model` | `model_<name>` | One per distinct model (10). Casefold-normalized. Shared across findings. |
| observable | `harness` | `harness_<name>` | One per distinct harness (`openclaw`, `ethara-fork`). Shared. |
| source | (core source) | `run_<nn>` | **The run.** The session JSONL file (or fork log). Tags carry `run_id`, `task_id`, `model`, `harness`, `trace_status`, `sha256`, `source_url`, `retrieved_at`. One per distinct session file (25). |
| observation | `behavior.tool_sequence` | `seq_<fid>` | **The cited steps.** `data.trajectory` = `@run_<nn>` (ref to the run record). Cited steps only — not the whole trajectory. Each step: `index` (1-indexed session line), `tool` (tool name or `assistant-text` / `thinking` / `tool-result`), `command` (args summary). `length` = step count. `provenance` cites the session sha256 and manifest retrieval URL. `body.source` = `@run_<nn>`. |
| observation | `intel.behavior` | `finding_<fid>` | **The behavior claim.** `data.category` = review-taxonomy class lowercased (`credential`, `guardrail`, `captcha`, `prompt-inject`, `other`, `irreversible`, `recovery`). `data.description` = reviewer description with verifier corrections applied, plus verbatim verifier notes. `models_affected`, `severity`, `evaluations_seen_on`, `first_observed`. Grade PRIMARY and confidence in tags. `body.source` = `@run_<nn>`. |

Cross-model findings (RC-003..RC-008) cite one exemplar session for their
tool_sequence; the full model list is in `models_affected`. WCB-RB-003
contrasts two runs: its tool_sequence carries steps from both, the task_2
steps prefixed `[contrast run ...]`. WCB-RC-010's run is a fork log, not a
session: its steps use `tool: harness-log`.

## Predicates

Three edge predicates per finding, all as `edge` records with bundle-local
`@` refs:

- `exhibits` — model → finding. One per model in `models_affected`
  (cross-model findings get one edge per model, e.g. 10 for WCB-RC-006).
  Ref: `e_<fid>_exhibits_m<i>`.
- `exhibits` — harness → finding. One per finding. Ref: `e_<fid>_exhibits_h`.
- `uses` — finding → tool_sequence ("the behavior cites the cited tool-call
  sequence"). One per finding. Ref: `e_<fid>_uses`.

The run linkage uses the observation-level chain `run` ← `body.source`
(`seq`) ← `body.source` (`finding`), plus `seq.data.trajectory = @run_<nn>`.

## Traversal: run → steps → tool calls → findings

Forward (from a run):
`run_<nn>` (source; `locator` = session path) → observations whose
`body.source = @run_<nn>` → `seq_<fid>` (`data.steps[]` = the tool calls) →
edges `finding_<fid> uses → @seq_<fid>` (reverse direction) or
`finding_<fid>`'s `body.source = @run_<nn>`.

Backward (from a model):
`model_<name>` → edges `subject = @model_<name>, predicate = exhibits` →
`finding_<fid>` → `uses` edge → `seq_<fid>` → `data.trajectory` → `@run_<nn>`.

Lane scoping: every record (including sources and observables) carries
`tags.lane = "wildclawbench-trajectories"`. Other useful tags:
`finding.id`, `behavior.class`, `grade`, `confidence`, `task_id`,
`trajectory`, `step.range`, `overlap.upstream` (transluce-intel UPSTREAM
reports #138/#141/#174 covering the same benchmark episodes),
`merged_from`, `sensitive` (credential-spill: real secret values are
withheld from these records; the raw bytes stay in the cached session files).

## Known related material (dedup, 2026-10-16)

Direct scan of `data/records/` before ingest. No duplicate records of these
findings exist. Related but not duplicates:
- transluce-intel lane: UPSTREAM reports #138 (GSMArena bot-checks; overlaps
  WCB-RA-005), #141 (OpenReview bot-checks; overlaps WCB-RA-006), #174
  (commit-then-push of leaked credentials; overlaps WCB-RA-003 / WCB-RB-007).
  These are third-party summaries of the same benchmark episodes at coarser
  granularity; the wildclawbench records are PRIMARY trajectory-level
  observations with cited tool-call steps. Overlaps are annotated in
  `tags.overlap.upstream`.
- "misinformation" hits in three old batches are unrelated word occurrences.
