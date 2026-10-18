#!/bin/bash
# Export (all pending batches incl. siblings') + verify, with lock retries.
export PATH="$HOME/.local/bin:$PATH"
cd ~/workspace/silent-locus
LOG=data/lanes/agenterrorbench-trajectories/export.log
for i in $(seq 1 30); do
  echo "=== export attempt $i $(date -u +%FT%TZ) ===" | tee -a "$LOG"
  OUT=$(uv run skills/factum/scripts/factum.py --repo . export 2>&1)
  echo "$OUT" | tee -a "$LOG" | tail -3
  if echo "$OUT" | grep -q '"ok":true'; then
    echo "EXPORT_OK" | tee -a "$LOG"
    break
  fi
  echo "$OUT" | grep -qi "LOCK_TIMEOUT" || { echo "EXPORT_NONLOCK_FAILURE"; exit 2; }
  sleep 50
done
for i in $(seq 1 30); do
  echo "=== verify attempt $i $(date -u +%FT%TZ) ===" | tee -a "$LOG"
  OUT=$(uv run skills/factum/scripts/factum.py --repo . verify 2>&1)
  echo "$OUT" | tee -a "$LOG" | tail -3
  if echo "$OUT" | grep -q '"ok":true'; then
    echo "VERIFY_OK" | tee -a "$LOG"
    exit 0
  fi
  echo "$OUT" | grep -qi "LOCK_TIMEOUT" || { echo "VERIFY_NONLOCK_FAILURE"; exit 2; }
  sleep 50
done
echo "RETRIES_EXHAUSTED"; exit 3
