# Evidence index — RootSE ingest 2026-10-16

## Work products

- `data/lanes/rootse-trajectories/build_bundle.py` — bundle builder.
  Reads the 10 verified trajectory files plus step ranges, emits
  `bundle.json` (67 records: 10 sources, 20 observations, 7
  observables, 30 edges). Rerunnable.
- `data/lanes/rootse-trajectories/bundle.json` — the submitted
  bundle (bundle v2, actor `agent:rootse-ingestor`, idempotency
  key `rootse-trajectories-batch-2026-10-16`).
- `reports/trajectory-ingest/rootse/REPORT.md` — findings, grades,
  evidence paths, killed list, verifier corrections, coverage.

## Source bytes (cached)

`data/lanes/rootse-trajectories/raw/data/` — 102 trajectory
JSONs. The 10 finding-bearing files:

- `swe-agent/gemini2/instance_NodeBB__NodeBB-82562bec444940608052f3e4149e0c61ec80bf3f-vd59a5728dfc977f44533186ace531248c2917516.json` (F-001)
- `swe-agent/gemini2/instance_navidrome__navidrome-09ae41a2da66264c60ef307882362d2e2d8d8b89.json` (F-002)
- `swe-agent/claude45/instance_NodeBB__NodeBB-f1a80d48cc45877fcbadf34c2345dd9709722c7f-v4fbcfae8b15e4ce5d132c408bca69ebb9cf146ed.json` (F-003)
- `swe-agent/gemini2/instance_qutebrowser__qutebrowser-6dd402c0d0f7665d32a74c43c5b4cf5dc8aff28d-v5fc38aaf22415ab0b70567368332beee7955b367.json` (F-004)
- `swe-agent/claude45/instance_internetarchive__openlibrary-2fe532a33635aab7a9bfea5d977f6a72b280a30c-v0f5aece3601a5b4419f7ccec1dbda2071be28ee4.json` (F-005)
- `swe-agent-live/gpt5mini/instance_sphinx-doc__sphinx-10435.json` (F-006)
- `openhands/qwen3-coder-480B-A35B-instruct/GjjvdBurg__paper2remarkable-43.json` (F-007)
- `openhands/qwen3-coder-480B-A35B-instruct/ESSS__conda-devenv-51.json` (F-008)
- `swe-agent/claude45/instance_future-architect__vuls-e4728e388120b311c4ed469e4f942e0347a2689b-v264a82e2f4818e30f5a25e4da53b27ba119f62b5.json` (F-009)
- `openhands/qwen3-coder-480B-A35B-instruct/CODAIT__exchange-metadata-converter-38.json` (F-010)

## Factum

- Lane: `rootse-trajectories`
  (`data/lanes/rootse-trajectories/lane.json`).
- Exported batch: `data/records/<batch-id>/` — batch ID and
  counts recorded below after export.
- Dedup evidence: direct scan of `data/records/` 2026-10-16
  found no `rootse` records and none of the 10 instance IDs.

## Batch record

- Batch ID: `b024998cf6a04f6392961acfe595765a`
  (`data/records/b024998cf6a04f6392961acfe595765a/`)
- Records: 134 total — 67 submitted (10 source, 20 observation,
  7 observable, 30 edge) plus 67 `in_lane` edges written by the
  bundle's top-level lane field.
- Findings: 10 (9 PRIMARY, 1 SECONDARY)
- Exported 2026-10-17 ~00:50 UTC; verified by direct scan of the
  exported batch files (no DB locks).
