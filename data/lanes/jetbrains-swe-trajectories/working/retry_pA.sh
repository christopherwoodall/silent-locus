#!/bin/bash
# Resilient retry loop for the JetBrains SWE pA bundle add.
LOG=/home/hatch/workspace/silent-locus/data/lanes/jetbrains-swe-trajectories/working/add-pA.log
n=0
while [ $n -lt 1000 ]; do
  n=$((n+1))
  echo "[$(date '+%F %T %Z')] add attempt $n (heartbeat)" >> "$LOG"
  python3 skills/factum/scripts/factum.py --repo . add --input data/lanes/jetbrains-swe-trajectories/working/bundle-pA.json > /tmp/jbswe-pA.out 2>&1
  rc=$?
  cat /tmp/jbswe-pA.out >> "$LOG"
  if [ $rc -eq 0 ]; then
    echo "[$(date '+%F %T %Z')] ADD_OK attempt $n" >> "$LOG"
    break
  fi
  echo "[$(date '+%F %T %Z')] attempt $n rc=$rc" >> "$LOG"
  sleep 55
done
echo "LOOP_DONE" >> "$LOG"
