#!/usr/bin/env bash
# Wait for VM egress to recover, then run the htmx probe sweep.
# Checks every 3 min (up to ~2h); requires 2 consecutive OKs to avoid flukes.
RAW=~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/grammarian/raw
LOG=$RAW/probe_run.log
ok_streak=0
for i in $(seq 1 40); do
  if curl -s -o /dev/null --max-time 15 https://example.com/ 2>/dev/null; then
    ok_streak=$((ok_streak+1))
    echo "[wait] egress OK streak=$ok_streak try=$i $(date -u +%FT%TZ)" >> "$LOG"
    if [ $ok_streak -ge 2 ]; then
      if curl -s -o /dev/null --max-time 20 https://urlquery.net/ 2>/dev/null; then
        echo "[wait] urlquery.net reachable, launching sweep" >> "$LOG"
        bash "$RAW/run_probes.sh"
        exit 0
      else
        echo "[wait] example.com OK but urlquery.net not; continuing to wait" >> "$LOG"
        ok_streak=0
      fi
    fi
  else
    ok_streak=0
    echo "[wait] egress down try=$i $(date -u +%FT%TZ)" >> "$LOG"
  fi
  sleep 180
done
echo "[wait] EGRESS NEVER RECOVERED after 40 tries" >> "$LOG"
exit 1
