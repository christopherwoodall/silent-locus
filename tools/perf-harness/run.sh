#!/bin/bash
# Factum performance experiment harness - main entry point.
#
# Usage:
#   ./run.sh <branch> [--save-golden] [--timeout <seconds>]
#
# What it does:
#   1. Extracts <branch> to a clean temp dir via git archive (does not disturb your checkout)
#   2. Rebuilds the Factum search index in the extracted tree
#   3. Runs benchmarks (timed CLI operations)
#   4. Runs correctness checks (--save-golden captures reference, otherwise compares)
#   5. Runs the regression test suite
#   6. Cleans up the worktree
#   7. Writes results to results/<branch>/
#
# For the final judge:
#   ./run.sh factum-perf-experiments --save-golden   # baseline + golden
#   ./run.sh factum-perf-team-a                      # team A (compares to golden)
#   ./run.sh factum-perf-team-b                      # team B (compares to golden)
# Then diff results/factum-perf-experiments/benchmark.json against each team's.
set -u

HARNESS_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$HARNESS_DIR/../.." && pwd)"

BRANCH="${1:-}"
if [ -z "$BRANCH" ]; then
  echo "Usage: $0 <branch> [--save-golden] [--timeout <seconds>]" >&2
  exit 2
fi
shift

SAVE_GOLDEN=0
TIMEOUT=600
while [ $# -gt 0 ]; do
  case "$1" in
    --save-golden) SAVE_GOLDEN=1; shift ;;
    --timeout) TIMEOUT="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

export PATH="$HOME/.local/bin:$PATH"

# Verify the branch exists
if ! git -C "$REPO_ROOT" rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
  echo "ERROR: branch '$BRANCH' does not exist" >&2
  exit 2
fi

WORKTREE="$HOME/workspace/.perf-harness-tmp/$(echo "$BRANCH" | tr '/' '-')-$$"
RESULTS_DIR="$HARNESS_DIR/results/$BRANCH"
GOLDEN_FILE="$HARNESS_DIR/golden/correctness-golden.json"

mkdir -p "$RESULTS_DIR"

echo "=== Perf harness: branch $BRANCH ==="
echo "Worktree: $WORKTREE"
echo "Results:  $RESULTS_DIR"

cleanup() {
  echo "Cleaning up extracted tree..."
  rm -rf "$WORKTREE"
}
trap cleanup EXIT

# 1. Extract branch to a clean directory via git archive
# (git worktree is broken on this repo; archive+tar is fast and reliable)
echo "--- [1/5] Extracting branch $BRANCH ---"
mkdir -p "$WORKTREE"
if ! git -C "$REPO_ROOT" archive "$BRANCH" | tar -x -C "$WORKTREE"; then
  echo "ERROR: failed to extract branch archive" >&2
  exit 1
fi
if [ ! -f "$WORKTREE/skills/factum/scripts/factum.py" ]; then
  echo "ERROR: extracted tree missing factum.py" >&2
  exit 1
fi
# factum.py shells out to git (HEAD for provenance); init a throwaway repo
git -C "$WORKTREE" init -q
git -C "$WORKTREE" add -A
git -C "$WORKTREE" -c user.email=harness@local -c user.name=harness \
  commit -qm "perf harness snapshot of $BRANCH"

# 2. Rebuild the search index (needed for match/graph; also warms the tree)
# NB: rebuild is slow on baseline (~11 min); give it a generous timeout
echo "--- [2/5] Rebuilding Factum index ---"
REBUILD_TIMEOUT=1800
REBUILD_START=$(date +%s)
if ! timeout "$REBUILD_TIMEOUT" python3 "$WORKTREE/skills/factum/scripts/factum.py" \
    --repo "$WORKTREE" rebuild >"$RESULTS_DIR/rebuild.log" 2>&1; then
  echo "ERROR: rebuild failed (see $RESULTS_DIR/rebuild.log)" >&2
  tail -20 "$RESULTS_DIR/rebuild.log" >&2
  exit 1
fi
REBUILD_END=$(date +%s)
echo "Rebuild took $((REBUILD_END - REBUILD_START))s"

# 3. Benchmarks
echo "--- [3/5] Running benchmarks ---"
if ! python3 "$HARNESS_DIR/benchmark.py" --repo "$WORKTREE" \
    --output "$RESULTS_DIR/benchmark.json" --timeout "$TIMEOUT"; then
  echo "WARNING: one or more benchmark operations failed (see benchmark.json)" >&2
fi

# 4. Correctness
echo "--- [4/5] Running correctness checks ---"
CORRECTNESS_ARGS=(--repo "$WORKTREE" --golden "$GOLDEN_FILE" --timeout "$TIMEOUT")
if [ "$SAVE_GOLDEN" -eq 1 ]; then
  CORRECTNESS_ARGS+=(--save-golden)
else
  CORRECTNESS_ARGS+=(--compare)
  if [ ! -f "$GOLDEN_FILE" ]; then
    echo "ERROR: golden file not found: $GOLDEN_FILE" >&2
    echo "Run with --save-golden on the baseline branch first." >&2
    exit 1
  fi
fi
CORRECTNESS_OK=1
if ! python3 "$HARNESS_DIR/correctness.py" "${CORRECTNESS_ARGS[@]}" \
    >"$RESULTS_DIR/correctness.log" 2>&1; then
  CORRECTNESS_OK=0
  echo "CORRECTNESS CHECKS FAILED (see $RESULTS_DIR/correctness.log)" >&2
fi
cat "$RESULTS_DIR/correctness.log"

# 5. Regression tests
echo "--- [5/5] Running regression test suite ---"
REGRESSION_OK=1
if ! bash "$HARNESS_DIR/regression.sh" "$WORKTREE" "$RESULTS_DIR/regression.json"; then
  # NB: the suite has 9 known pre-existing failures (4 failed + 5 errors on
  # pristine tree). The numbers are recorded; the judge compares to baseline.
  echo "NOTE: pytest exited nonzero (see results/regression.json for counts)" >&2
  REGRESSION_OK=0
fi

# Summary report
{
  echo ""
  echo "================ SUMMARY: $BRANCH ================"
  echo ""
  echo "--- Benchmark timings ---"
  python3 - "$RESULTS_DIR/benchmark.json" <<'EOF'
import json, sys
with open(sys.argv[1]) as f:
    d = json.load(f)
for name, op in d.get("operations", {}).items():
    status = op.get("status", "?")
    t = op.get("elapsed_seconds", "?")
    extra = f" (n={op['result_count']})" if "result_count" in op else ""
    print(f"  {name:18s} {str(t):>10}s  [{status}]{extra}")
EOF
  echo ""
  echo "--- Correctness ---"
  if [ "$CORRECTNESS_OK" -eq 1 ]; then echo "  PASS"; else echo "  FAIL"; fi
  echo ""
  echo "--- Regression ---"
  python3 - "$RESULTS_DIR/regression.json" <<'EOF'
import json, sys
with open(sys.argv[1]) as f:
    d = json.load(f)
print(f"  passed={d['passed']} failed={d['failed']} errors={d['errors']} "
      f"({d['elapsed_seconds']}s) [{d['status']}]")
EOF
  echo "=================================================="
} | tee "$RESULTS_DIR/summary.txt"

echo ""
echo "Results written to $RESULTS_DIR"

# Exit nonzero if correctness failed (benchmarks/regression recorded for comparison)
[ "$CORRECTNESS_OK" -eq 1 ]
