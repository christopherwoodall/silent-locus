#!/bin/bash
# worker 3 export retry loop for evidence/processed ingest (lane processed-gems)
cd ~/workspace/silent-locus || exit 1
export PATH="$HOME/.local/bin:$PATH"
LOG=.work-ingest/export-processed-w3.log
echo "$(date -u +%FT%TZ) | w3 export loop started (30 attempts x 60s)" >> "$LOG"
for i in $(seq 1 30); do
  OUT=$(timeout 1800 python3 skills/factum/scripts/factum.py --repo . export 2>&1)
  echo "$OUT" >> "$LOG"
  if echo "$OUT" | grep -q '"ok"[[:space:]]*:[[:space:]]*true'; then
    echo "$(date -u +%FT%TZ) | w3 export attempt $i SUCCEEDED" >> "$LOG"
    echo "W3-EXPORT-SUCCESS attempt $i"
    exit 0
  fi
  echo "$(date -u +%FT%TZ) | w3 export attempt $i failed, sleeping 60s" >> "$LOG"
  sleep 60
done
echo "$(date -u +%FT%TZ) | w3 export loop EXHAUSTED 30 attempts" >> "$LOG"
echo "W3-EXPORT-EXHAUSTED"
exit 1
