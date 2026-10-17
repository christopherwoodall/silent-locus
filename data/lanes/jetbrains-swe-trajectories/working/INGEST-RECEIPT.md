# JetBrains SWE-bench Factum Ingest — Receipt

Lane: `jetbrains-swe-trajectories`
Idempotency key: `jetbrains-swe-ingest-2026-10-17-v1` (chunks: `-pA`, `-pB1`, `-pB2`, `-pC`, `-pD`)
Actor: `agent:jetbrains-swe-ingestor`
Ingested: 2026-10-17/18 UTC (chunked adds across the write-path jam)

## Batches (all durability=pending at add, all projected by export)

| Chunk | Batch ID | Records | Contents |
|---|---|---|---|
| pA | `435edfc48dc84cbfb521782b43397768` | 4 | artifact (parquet) + source + run + dataset.snapshot |
| pB1 | `b1670cc9206c4c35ac44e431232a9719` | 893 | dataset.record observations (rows 0–892) |
| pB2 | `51368d31256c4331a635bb26a5555f9f` | 892 | dataset.record observations (rows 893–1784) |
| pC | `b6d867422a2c4c89b2e4ee048ab0543e` | 14 | 7 intel.behavior + 7 behavior.tool_sequence |
| pD | `ce81bb019a0340b2a3a45365d5d2834a` | 1,792 | edges: 1,785 run→trajectory related_to + 7 finding→trajectory supports |

Total: **3,595 records**. Exported to `data/records/<batch_id>/records.jsonl` (verified directly, no DB locks).

## Key assigned IDs
- source: `source_8580aaf5f1ee49c1ac67a0ba095130ab`
- artifact (parquet): `artifact_d1844ee11b3748a4a706c2d499c7d149`
- run: `run_f645cfe23616453b99d9c6909d195ee2`
- snapshot: `observation_538b2453868a4662acc63d89feb370ce`

## Verification (exported files, direct read)
- Record counts by kind: artifact 1, source 1, run 1, observation 1,800, edge 1,792
- **0 errors, 0 warnings**
- Every record carries `tags.lane=jetbrains-swe-trajectories` (incl. source)
- All observations have `observed_at` + `time_basis`; all have fingerprint + schema
- All 1,792 edges have `basis: OBSERVED` + non-empty `cites`; all subject/object/cites resolve
- Dedup within batch: 1,785 unique instance_ids, 0 duplicates
- Dedup corpus-wide: 0 overlap with other lanes' instance_ids (re-confirmed post-ingest)
- `seen_before: {}` on all 5 adds (no exact-duplicate observables)
- Behavior records preserve: class, grade, confidence, step_range, trajectory_row,
  instance_id, verbatim_quote(s), verifier_notes/corrections, category, description, severity

## Notes / anomalies during ingest
- pD first attempt rejected: `SCHEMA "Interpretive edges require basis and citations."`
  Fixed by adding `cites: [subject, object]` to all 1,792 edges (build_pD.py), resubmitted clean.
- Transient `JSONDecodeError` during the factum write-path fix rollout: caused by a
  sibling worker's empty in-flight file `data/lanes/android-world-trajectories/bundle-android-world-nolane.json`
  matching the lane.json scan; resolved when the sibling cleaned up (file gone).
- Two service restarts killed in-flight attempts; all chunks re-queued and landed.
- EPERM write-throttle waves: routed critical writes via tool path.

## Open gaps (carried from findings, unchanged)
- F-001: whether the pytest.raises shim survived into the submitted diff (unverifiable — trajectory ends mid-work)
- F-002: final curl success not visible (trajectory ends at the assistant message)
- F-A-003: whether the 3 failures were pre-existing (finding is about absent triage, not causation)
- F-A-002: test-file edit + revert only self-reported, not visible in bytes (MEDIUM confidence)
- F-005: 1773/1785 trajectories mix models per-turn — per-trajectory model attribution wrong by construction

## Status
**NOT committed, NOT pushed** — batch dirs + this receipt left uncommitted for the coordinator's final commit.
