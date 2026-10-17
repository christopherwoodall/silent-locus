#!/bin/bash
# Submit bundle with lock-contention retries (40-60s sleeps on LOCK_TIMEOUT).
export PATH="$HOME/.local/bin:$PATH"
cd ~/workspace/silent-locus
LOG=data/lanes/agenterrorbench-trajectories/submit.log
for i in $(seq 1 60); do
  echo "=== attempt $i $(date -u +%FT%TZ) ===" | tee -a "$LOG"
  OUT=$(uv run skills/factum/scripts/factum.py --repo . add --input data/lanes/agenterrorbench-trajectories/bundle.json 2>&1)
  echo "$OUT" | tee -a "$LOG" | tail -3
  if echo "$OUT" | grep -q '"ok":true'; then
    echo "ADD_OK" | tee -a "$LOG"
    exit 0
  fi
  if echo "$OUT" | grep -qi "LOCK_TIMEOUT"; then
    sleep 50
    continue
  fi
  echo "ADD_NONLOCK_FAILURE" | tee -a "$LOG"
  exit 2
done
echo "ADD_RETRIES_EXHAUSTED" | tee -a "$LOG"
exit 3
