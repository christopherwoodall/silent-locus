#!/bin/bash
# Submit the Android-World bundle with patient retry on writer-lock contention.
# Never kills sibling processes. Retries LOCK_TIMEOUT failures with 45-75s sleeps.
# Writes a result stamp to submit-result.json when done.
set -u
cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:$PATH"
BUNDLE="bundle-android-world.json"
RESULT="submit-result.json"
MAX_ATTEMPTS=120
attempt=0
while [ $attempt -lt $MAX_ATTEMPTS ]; do
  attempt=$((attempt + 1))
  echo "[$(date -u +%FT%TZ)] attempt $attempt/$MAX_ATTEMPTS"
  OUT=$(uv run ../../../skills/factum/scripts/factum.py --repo ../../.. add --input "$BUNDLE" 2>&1)
  echo "$OUT" | tail -3
  if echo "$OUT" | grep -q '"ok": *true'; then
    echo "$OUT" > submit-out.json
    python3 -c "
import json
d = json.load(open('submit-out.json'))
r = {'ok': True, 'attempt': $attempt, 'batch': d.get('batch') or d.get('batch_id') or d, 'finished_utc': __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()}
json.dump(r, open('$RESULT', 'w'), indent=1)
print(json.dumps(r, indent=1))
"
    exit 0
  fi
  if echo "$OUT" | grep -qi "lock_timeout\|LOCK_TIMEOUT\|writer.lock"; then
    sleep $((45 + RANDOM % 30))
    continue
  fi
  # Transient empty output (EPERM wave on overlay fs) — retry
  if [ -z "$OUT" ] || echo "$OUT" | grep -qi "JSONDecodeError"; then
    sleep $((45 + RANDOM % 30))
    continue
  fi
  # non-lock failure: record and stop
  echo "$OUT" > submit-out.json
  python3 -c "
import json
r = {'ok': False, 'attempt': $attempt, 'error': open('submit-out.json').read()[:2000]}
json.dump(r, open('$RESULT', 'w'), indent=1)
"
  exit 1
done
python3 -c "
import json
r = {'ok': False, 'attempt': $attempt, 'error': 'max attempts reached'}
json.dump(r, open('$RESULT', 'w'), indent=1)
"
exit 1
