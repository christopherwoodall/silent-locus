#!/bin/bash
cd /home/hatch/workspace/silent-locus
LOG=data/lanes/bcp-search-trajectories/working/export.log
for i in $(seq 1 120); do
  echo "[$(date -u +%FT%TZ)] bcp export attempt $i" >> "$LOG"
  timeout 1800 python3 skills/factum/scripts/factum.py --repo . --lock-timeout 120 export >> "$LOG" 2>&1
  rc=$?
  echo "[$(date -u +%FT%TZ)] attempt $i rc=$rc" >> "$LOG"
  if [ $rc -eq 0 ]; then echo "[$(date -u +%FT%TZ)] BCP_EXPORT_OK attempt $i" >> "$LOG"; break; fi
  sleep 55
done
echo "BCP_EXPORT_LOOP_DONE" >> "$LOG"
