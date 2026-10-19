# Ingest progress — agentprocessbench-trajectories

- [x] 2026-10-16: bundle built (`bundle.json`, 68 records: 4 source, 4
      dataset.snapshot, 20 behavior.tool_sequence, 20 intel.behavior, 20 claim).
- [x] 2026-10-16/17: submitted via `add --input bundle.json` after ~30
      LOCK_TIMEOUT retries (fleet-wide writer-lock contention). ACCEPTED:
      batch `61f91caffbc84ed4983ad231165bdd28`, all 68 records assigned
      IDs, schema-pack validation passed with zero errors. Batch sits in
      `data/.local/pending/` (durable).
- [ ] `export` — blocked on continued fleet-wide lock contention
      (telbench/rootse/wildclawbench/agenterrorbench/longrca sibling
      workers submitting). Retry loop running in background.
- [ ] `verify` after export.
- [x] commit 835baad1 (docs, lane files, reports, taxonomy — explicit
      pathspecs; no Factum records yet, no push).
- [ ] second commit: `data/records/61f91caffbc84ed4983ad231165bdd28/`
      after export+verify. Do NOT push; parent decides.
- [ ] left uncommitted (sibling-shared files, do not sweep):
      `.gitignore` (my raw/ local-only line + sibling longrca line),
      `scripts/trajectory-pipeline-README.md` (new file, fleet sections +
      my AgentProcessBench section).

Resume: `export`, `verify`, then
`git add data/records/61f91caffbc84ed4983ad231165bdd28 && git commit --only data/records/61f91caffbc84ed4983ad231165bdd28`.

Bundle design: claim -> intel.behavior -> behavior.tool_sequence ->
trajectory locator -> raw bytes. No edges during ingest (exhibits/uses go
through the edge-builder pass later). Model identity is not recorded in the
dataset; tool_sequence.model = "unrecorded-in-source" (honest, documented).
