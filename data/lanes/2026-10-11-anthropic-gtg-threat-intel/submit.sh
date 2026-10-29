#!/bin/bash
# Submit the GTG Family A bundle with LOCK_TIMEOUT retry/backoff.
cd ~/workspace/wt-ingest-gtg
LOG=data/lanes/2026-10-11-anthropic-gtg-threat-intel/submit.log
for i in $(seq 1 12); do
  echo "=== attempt $i $(date -u +%FT%TZ) ===" | tee -a "$LOG"
  OUT=$(python3 skills/factum/scripts/factum.py --repo . add --input data/lanes/2026-10-11-anthropic-gtg-threat-intel/bundle.json 2>&1)
  echo "$OUT" | tail -c 4000 >> "$LOG"
  echo "$OUT" | tail -c 2000
  if echo "$OUT" | grep -q '"ok": *true'; then
    echo "SUBMIT OK on attempt $i" | tee -a "$LOG"
    exit 0
  fi
  if echo "$OUT" | grep -qi 'lock\|timeout\|LOCK'; then
    sleep 55
    continue
  fi
  echo "NON-LOCK FAILURE — stopping for inspection" | tee -a "$LOG"
  exit 1
done
echo "GAVE UP after 12 attempts" | tee -a "$LOG"
exit 1
