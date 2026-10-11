#!/bin/bash
# Submit with retry on writer-lock contention. Never deletes pending work.
cd ~/workspace/silent-locus
for i in $(seq 1 30); do
  OUT=$(python3 skills/factum/scripts/factum.py --repo . add --input data/lanes/2026-10-11-hf-traj-swenext/.work/bundle.json 2>&1)
  echo "$OUT" | head -5
  if echo "$OUT" | grep -q '"ok": *true'; then
    echo "SUBMIT_OK attempt=$i"
    exit 0
  fi
  if echo "$OUT" | grep -qi 'LOCK_TIMEOUT\|lock'; then
    echo "lock contention, attempt $i/30, sleeping 60s"
    sleep 60
    continue
  fi
  echo "NON_LOCK_FAILURE attempt=$i"
  echo "$OUT" | head -30
  exit 2
done
echo "GAVE_UP after 10 attempts"
exit 3
