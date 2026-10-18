#!/bin/bash
cd /home/hatch/workspace/silent-locus
LOG=data/lanes/bcp-search-trajectories/working/lane-new.log
for i in $(seq 1 120); do
  echo "[$(date -u +%FT%TZ)] lane new attempt $i" >> "$LOG"
  timeout 1800 python3 skills/factum/scripts/factum.py --repo . lane new bcp-search-trajectories --tags '{"docs_path":"data/lanes/bcp-search-trajectories/","lane":"bcp-search-trajectories"}' >> "$LOG" 2>&1
  rc=$?
  echo "[$(date -u +%FT%TZ)] attempt $i rc=$rc" >> "$LOG"
  if [ $rc -eq 0 ]; then echo "[$(date -u +%FT%TZ)] LANE_NEW_OK attempt $i" >> "$LOG"; break; fi
  sleep 55
done
echo "LANE_NEW_LOOP_DONE" >> "$LOG"
