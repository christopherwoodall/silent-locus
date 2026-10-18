#!/bin/bash
# Submit the SS-41 factum bundle with retry under writer-lock contention.
# Log-persistent; survives session drops. Idempotent via the bundle's
# idempotency key (swe-smith-mini-ingest-2026-10-17-v1).
cd ~/workspace/silent-locus
LOG=data/lanes/swe-smith-mini-trajectories/working/add-ss41.log
BUNDLE=data/lanes/swe-smith-mini-trajectories/bundle-ss41-swe-smith-mini.json
n=0
while [ $n -lt 200 ]; do
  n=$((n+1))
  echo "[$(date -u +%FT%TZ)] ss41 add attempt $n" >> "$LOG"
  timeout 5400 python3 skills/factum/scripts/factum.py --repo . add --input "$BUNDLE" >> "$LOG" 2>&1
  rc=$?
  echo "[$(date -u +%FT%TZ)] attempt $n rc=$rc" >> "$LOG"
  if [ $rc -eq 0 ]; then
    echo "[$(date -u +%FT%TZ)] ADD_OK ss41 attempt $n" >> "$LOG"
    break
  fi
  sleep 55
done
echo "SS41_LOOP_DONE rc=$rc attempts=$n [$(date -u +%FT%TZ)]" >> "$LOG"
