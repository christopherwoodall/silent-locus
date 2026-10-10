# Factum Performance Harness (Team C)

Verification harness for the Factum performance experiments. Judges Team A and
Team B branches against the `factum-perf-experiments` baseline.

## Quick start (for the final judge)

```bash
cd ~/workspace/silent-locus/tools/perf-harness

# 1. Baseline: capture timings + golden correctness reference
./run.sh factum-perf-experiments --save-golden

# 2. Team A
./run.sh factum-perf-team-a

# 3. Team B
./run.sh factum-perf-team-b

# 4. Compare timings
diff results/factum-perf-experiments/benchmark.json results/factum-perf-team-a/benchmark.json
diff results/factum-perf-experiments/benchmark.json results/factum-perf-team-b/benchmark.json
```

Each run writes to `results/<branch>/`:
- `benchmark.json` — per-operation timings and status
- `correctness.log` — pass/fail vs golden reference
- `regression.json` — pytest counts (passed/failed/errors)
- `rebuild.log` — index rebuild log
- `summary.txt` — human-readable summary

## What it tests

**Benchmark** (`benchmark.py`): times each CLI operation —
`match` (exact, fuzzy, key), `query` (tag filter), `graph` (depth 1),
`status`, `verify`. Reports elapsed seconds and result counts.

**Correctness** (`correctness.py`): verifies no behavior change —
- `verify` passes with identical record count and 0 pending
- 4 fixed `match` queries return identical record ID sets
- tag-filter `query` count unchanged

`--save-golden` captures the reference from the baseline branch.
Without it, results are compared against `golden/correctness-golden.json`.

**Regression** (`regression.sh`): runs the Factum pytest suite
(`skills/factum/tests`). NB: the suite has 9 known pre-existing
failures/errors on the pristine tree (4 failed + 5 errors, verified
during development). The harness records raw counts; the judge
compares team branches against baseline counts — no *new* failures
is the bar, not zero failures.

## Design notes

- Runs each branch from a clean **git archive extraction** under
  `~/workspace/.perf-harness-tmp/` — your current checkout is never
  disturbed. Temp dirs are removed on exit.
- Per-operation timeout defaults to 600s (baseline `status` alone
  takes ~120s). Override with `--timeout <seconds>`.
- The harness does not modify the repo. Golden files live in
  `golden/` (committed); per-run results in `results/` (gitignored).
