#!/bin/bash
cd ~/workspace/silent-locus
for i in $(seq 1 30); do
  OUT=$(python3 skills/factum/scripts/factum.py --repo . verify 2>&1)
  echo "$OUT" | head -12
  if echo "$OUT" | grep -q '"ok": *true'; then
    echo "VERIFY_OK attempt=$i"
    exit 0
  fi
  if echo "$OUT" | grep -qi 'LOCK_TIMEOUT'; then
    echo "lock contention, attempt $i/30, sleeping 60s"
    sleep 60
    continue
  fi
  echo "NON_LOCK_RESULT attempt=$i"
  echo "$OUT" | head -30
  exit 2
done
echo "GAVE_UP after 30 attempts"
exit 3
