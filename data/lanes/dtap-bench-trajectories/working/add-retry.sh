#!/usr/bin/env bash
# DTap-Bench factum add retry loop — durable, bounded, polite.
# Tries `factum add` for bundle-dtap-bench.json; on success runs `export`
# and records the batch id. Then exits. Safe to re-run (idempotent key).
set -u
LANE="$HOME/workspace/silent-locus/data/lanes/dtap-bench-trajectories"
LOG="$LANE/working/add-dtap.log"
export PATH="$HOME/.local/bin:$PATH"
cd "$HOME/workspace/silent-locus" || exit 1
n=0
while [ "$n" -lt 120 ]; do
  n=$((n + 1))
  echo "[$(date -u +%FT%TZ)] add attempt $n" >> "$LOG"
  out=$(timeout 280 python3 skills/factum/scripts/factum.py --repo . add \
    --input "$LANE/bundle-dtap-bench.json" 2>&1)
  rc=$?
  echo "$out" | tail -2 >> "$LOG"
  if [ $rc -eq 0 ] && echo "$out" | grep -q '"ok":[ ]*true'; then
    echo "[$(date -u +%FT%TZ)] ADD_OK attempt $n" >> "$LOG"
    exp=$(timeout 280 python3 skills/factum/scripts/factum.py --repo . export 2>&1 | tail -3)
    echo "$exp" >> "$LOG"
    echo "[$(date -u +%FT%TZ)] EXPORT_DONE" >> "$LOG"
    break
  fi
  sleep 55
done
echo "LOOP_DONE n=$n" >> "$LOG"
