# Ingest progress — agentprocessbench-trajectories

- [x] 2026-10-16: bundle built (`bundle.json`, 68 records: 4 source, 4
      dataset.snapshot, 20 behavior.tool_sequence, 20 intel.behavior, 20 claim).
- [ ] submit via `add --input bundle.json`
- [ ] `export`, `verify --blobs`
- [ ] commit explicit pathspecs (no push; parent decides)
- [ ] reports: reports/trajectory-ingest/agentprocessbench/REPORT.md +
      EVIDENCE-INDEX.md
- [ ] docs: scripts/trajectory-pipeline-README.md AgentProcessBench section;
      docs/taxonomy/behavior-categories.md new eval-derived categories
- [ ] .gitignore: lane raw/ local-only (39 MB bytes, default local retention)

Bundle design: claim -> intel.behavior -> behavior.tool_sequence ->
trajectory locator -> raw bytes. No edges during ingest (exhibits/uses go
through the edge-builder pass later). Model identity is not recorded in the
dataset; tool_sequence.model = "unrecorded-in-source" (honest, documented).
