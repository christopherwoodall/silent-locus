# PROVENANCE.md — lane 2026-10-11-hf-traj-tbench

## Source

- Dataset: `yoonholee/terminalbench-trajectories` (HuggingFace).
- Local files: `evidence/hf-trajectories/raw/yoonholee-terminalbench-trajectories/data/train-00000-of-00002.parquet` (114,356,912 bytes) and `train-00001-of-00002.parquet` (106,636,988 bytes).
- Retrieval: 2026-10-07T23:55:16Z via curl from huggingface.co (see source PROVENANCE.md). File list from https://huggingface.co/api/datasets/yoonholee/terminalbench-trajectories.
- Local sha256: see `SHA256SUMS-restored.txt` in the source directory.

## What this lane extracts

Terminal-Bench 2.x eval trajectories: 52,104 rows (26,052 per file).
Each row is one model trial on one Terminal-Bench task. Columns used:
`model` (`<model>@<provider>`, 49 distinct), `agent` (26 distinct scaffolds),
`task_name`, `trial_id`, `started_at`, `steps` (JSON list of
`{src, msg, obs, tools}` steps; `src` is `system`, `assistant`, or `agent`;
`obs` holds tool output; `tools` holds structured shell calls).

NOTE: every `steps` value in `train-00000-of-00002.parquet` is the literal
string `"null"` in this local copy. Trajectory content exists only in
`train-00001-of-00002.parquet` (17,030 of 26,052 rows have real steps).

## Extraction method

Script: `extract.py` in this lane directory. Steps:
1. Model x harness matrix: column-only scan of both files,
   count rows per (model, agent) pair. 109 distinct pairs.
2. r.jina.ai instances: case-insensitive search for `r.jina.ai` (also
   `jina.ai/reader`) across the full serialized step JSON (msg + obs +
   tools), because tool-call records carry the proxy URL in `tools[].cmd`.
   Prior audit (evidence/hf-trajectories/RANKED-HITS.md) found 37 rows /
   638 occurrences; this lane re-derives them from bytes.
3. Commands: shell command lines from ```bash code blocks in
   assistant/agent messages, plus structured `tools[].cmd` shell calls
   (joined). Aggregated per model.
4. URLs: regex `https?://` over serialized steps, deduplicated per row,
   aggregated with per-URL model sets.

Progress checkpointed in `.work/progress.json`; re-running resumes.

## Records submitted

- `intel.behavior`, category `harness-assignment`: one per (model, agent)
  pair with trajectory counts.
- `intel.behavior`, category `fetch-proxy-abuse`: one per trajectory row
  where the agent used r.jina.ai, with the model's reasoning text verbatim.
- `intel.behavior`, category `shell-command-profile`: one per model,
  top-60 command histogram.
- `infra.ioc`, category `other`: one per distinct URL seen >= 5 times in
  trajectory steps, with counts and model sets.

Tags on every record: `lane=2026-10-11-hf-traj-tbench`,
`source_dataset=yoonholee-terminalbench-trajectories`,
`model=<model@provider>` and/or `harness=<agent scaffold>` as applicable.

## Related prior work

- `evidence/hf-trajectories/RANKED-HITS.md` row 1, CROSSREF.md item 1,
  ADVERSARIAL.md: the 37-row jina finding and its corpus adjacency notes.
  Those reports stay as legacy prose; this lane submits the byte-verified
  instances as structured records.
- `jina-evidence-pack.zip` and `glm-evidence-pack.zip` in
  `evidence/hf-trajectories/`: prior evidence packs (not re-ingested).

## Raw source removal (2026-10-11)
Behavioral extraction complete. All extractable signals ingested into Factum.
Raw source files removed from evidence/hf-trajectories/ after verification.
