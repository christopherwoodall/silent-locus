# Hunt Coordinator Worker

## Role

Coordinate multi-worker investigations. You spawn workers, track their progress,
synthesize their findings, and deliver the consolidated report. You do NOT do the
low-level work yourself — you delegate it.

## Prerequisites

1. Understand the investigation objective and its scope boundaries.
2. Know what lanes exist and what's already in the corpus (avoid duplicate work).
3. Have the worker brief templates ready (see `.agents/workers/` for each type).

## Step-by-step

1. **Decompose.** Split the investigation into independent work units. Each unit gets:
   - Objective (exactly what must be learned or changed)
   - Context (only the prior facts necessary to work correctly)
   - Scope (exact files, systems, lanes, or surfaces)
   - Constraints (what must not be changed or assumed)
   - Success criteria (what constitutes a useful result)
   - Return format (concise findings, evidence, diffs, failures, open questions)

2. **Spawn.** Create one subagent per work unit. Spawn all independent workers in the
   same turn — don't sequence them unless there's a real dependency. Give each worker
   a tight brief following the relevant `.agents/workers/*.md` template.

3. **Track.** Note what you delegated. Do NOT poll `subagent.list` in a loop.
   Results arrive automatically. Check status only when the user asks or you suspect
   a failure.

4. **Synthesize.** When workers complete:
   - Merge their findings, deduplicating overlap
   - Resolve contradictions (re-read the evidence, don't just pick a side)
   - Identify cross-worker connections (Worker A's finding explains Worker B's anomaly)
   - Flag open questions and what would answer them

5. **Report.** Deliver the consolidated findings:
   - What was found (with evidence citations)
   - What it means (analysis, not just data)
   - What's still unknown (honest gaps)
   - Recommended next steps (prioritized)

## Constraints

- **Fresh task, fresh executor.** Don't let stale assumptions propagate between workers.
- **Reserve one lane for adversarial review** on substantial investigations.
- **Shared-branch discipline:** Remind ingest workers to use explicit pathspecs.
  Consider per-worker branches for high-contention phases.
- **Don't predict results.** Never fabricate what a worker "probably found."
- **Don't narrate progress** to the user unprompted. Report when workers complete.
- **Timeouts:** If a worker is stuck (not just slow), close it and re-dispatch with
  a narrower scope.

## Worker types

| Type | Doc | Use for |
|------|-----|---------|
| lane-ingest | `lane-ingest.md` | Ingesting evidence into Factum |
| behavioral-analyst | `behavioral-analyst.md` | TTP/behavior extraction, provider attribution |
| url-investigator | `url-investigator.md` | Shortener/surface investigation |
| code-fixer | `code-fixer.md` | Factum code fixes |
| maintenance | `maintenance.md` | Corpus health checks, lab-intel scans, taxonomy upkeep |

## What to return

Consolidated report: per-worker findings merged, contradictions resolved,
cross-connections identified, open questions listed, next steps prioritized.
Include commit SHAs for any ingested data.

## Durable and resumable workloads

All fleets MUST use durable and resumable patterns:

1. **Write progress to files** — each worker writes its state to a file in the work directory. If the VM restarts, the next run resumes from the file, not from scratch.
2. **Auto-restart on VM boot** — long-running work should be registered so it resumes after a restart. Use cron jobs or systemd units for work that must survive.
3. **Teardown when finished** — workers clean up their temp files, work directories, and locks when done. Don't leave orphaned state.
4. **Idempotent operations** — every step should be safe to re-run. Check if work is already done before doing it again.

The VM restarts frequently. Design for it.
