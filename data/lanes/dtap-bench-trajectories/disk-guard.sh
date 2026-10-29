#!/bin/bash
# DTap-Bench disk-guard watchdog — transient; killed on download completion.
# Checks every 30 min; if free <10 GiB, kills the download cleanly and flags.
LANE="$HOME/workspace/silent-locus/data/lanes/dtap-bench-trajectories"
LOG="$LANE/disk-guard.log"
while true; do
  sleep 1800
  ts=$(date -u +%FT%TZ)
  avail_kb=$(df --output=avail /home/hatch | tail -1)
  avail_gib=$(awk "BEGIN{printf \"%.1f\", $avail_kb/1048576}")
  below=$(awk "BEGIN{print ($avail_kb < 10485760) ? 1 : 0}")
  done_n=$(find "$LANE/raw" -name "*.sha256" 2>/dev/null | wc -l)
  echo "$ts free=${avail_gib}GiB files_done=$done_n" >> "$LOG"
  if [ "$below" = "1" ]; then
    echo "$ts GUARD-TRIP: free <10GiB, killing download" >> "$LOG"
    pkill -TERM -f download-parallel.sh; sleep 5
    pkill -KILL -f download-parallel.sh
    pkill -f "huggingface.co/api/resolve-cache/datasets/AI-Secure"
    echo "PAUSED $ts free=${avail_gib}GiB files_done=$done_n" > "$LANE/DISK-GUARD-PAUSED"
    exit 0
  fi
done
