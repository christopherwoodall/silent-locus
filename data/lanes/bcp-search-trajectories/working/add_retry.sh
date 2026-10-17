#!/bin/bash
cd ~/workspace/silent-locus
LOG=data/lanes/bcp-search-trajectories/working/add.log
for i in $(seq 401 600); do
  echo "[$(date -u +%FT%TZ)] bcp add attempt $i" >> "$LOG"
  timeout 5400 python3 skills/factum/scripts/factum.py --repo . add --input data/lanes/bcp-search-trajectories/bundle-bcp-search.json >> "$LOG" 2>&1
  rc=$?
  echo "[$(date -u +%FT%TZ)] attempt $i rc=$rc" >> "$LOG"
  if [ $rc -eq 0 ]; then echo "[$(date -u +%FT%TZ)] BCP_ADD_OK attempt $i" >> "$LOG"; break; fi
  sleep 55
done
echo "BCP_ADD_LOOP_DONE" >> "$LOG"
