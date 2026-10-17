#!/bin/bash
# ANDROID-WORLD submit finisher loop (task spec, 2026-10-17).
# - Uses --lock-timeout 5400: each attempt waits up to 90 min for the writer lock.
# - Retries LOCK_TIMEOUT with 60-90s sleeps, up to 120 attempts.
# - Never kills any process. Does not touch sibling pending batches.
# - Logging is best-effort (EPERM waves hit exec-path writes); on success the
#   full result JSON is printed to stdout so the caller can capture batch_id
#   even if the log/result files fail to write.
set -u
cd ~/workspace/silent-locus || exit 1
export PATH="$HOME/.local/bin:$PATH"
BUNDLE="data/lanes/android-world-trajectories/bundle-android-world.json"
LANEDIR="data/lanes/android-world-trajectories"
RESULT="$LANEDIR/submit-result.json"
OUT="$LANEDIR/submit-out.json"
LOG="$LANEDIR/submit-loop.log"
MAX_ATTEMPTS=120

blog() { echo "[$(date -u +%FT%TZ)] $*" >> "$LOG" 2>/dev/null || true; }

attempt=0
while [ $attempt -lt $MAX_ATTEMPTS ]; do
  attempt=$((attempt + 1))
  blog "finisher attempt $attempt/$MAX_ATTEMPTS"
  OUTTXT=$(uv run skills/factum/scripts/factum.py --repo . --lock-timeout 5400 add --input "$BUNDLE" 2>&1)
  RC=$?
  blog "finisher attempt $attempt rc=$RC: $(echo "$OUTTXT" | tail -c 400)"
  if echo "$OUTTXT" | grep -q '"ok": *true'; then
    echo "$OUTTXT" > "$OUT" 2>/dev/null || true
    BATCH=$(echo "$OUTTXT" | python3 -c "import json,sys
try:
    d=json.load(sys.stdin)
    r=d.get('result',d)
    print(r.get('batch_id') or d.get('batch_id') or '')
except Exception as e:
    print('PARSE-FAIL')")
    SEEN=$(echo "$OUTTXT" | python3 -c "import json,sys
try:
    d=json.load(sys.stdin); r=d.get('result',d); s=r.get('seen_before',{})
    print(len(s) if isinstance(s,dict) else s)
except Exception: print('?')")
    python3 - "$RESULT" "$BATCH" "$attempt" "$SEEN" <<'PY' 2>/dev/null || true
import json,sys,datetime
res={"ok":True,"attempt":int(sys.argv[3]),"batch_id":sys.argv[2],
     "seen_before_count":sys.argv[4],
     "finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
json.dump(res,open(sys.argv[1],"w"),indent=1)
PY
    blog "finisher SUCCESS batch=$BATCH seen_before=$SEEN"
    echo "SUBMIT-SUCCESS batch_id=$BATCH seen_before=$SEEN attempt=$attempt"
    echo "$OUTTXT"
    exit 0
  fi
  if echo "$OUTTXT" | grep -qi "LOCK_TIMEOUT\|Another Factum command is using"; then
    sleep $((60 + RANDOM % 31))
    continue
  fi
  # Non-lock failure: record everything and stop (do not blind-retry).
  echo "$OUTTXT" > "$OUT" 2>/dev/null || true
  blog "finisher NON-LOCK FAILURE attempt $attempt, stopping"
  echo "SUBMIT-NONLOCK-FAILURE attempt=$attempt"
  echo "$OUTTXT"
  exit 1
done
blog "finisher max attempts ($MAX_ATTEMPTS) reached"
echo "SUBMIT-MAX-ATTEMPTS attempt=$MAX_ATTEMPTS"
exit 1
