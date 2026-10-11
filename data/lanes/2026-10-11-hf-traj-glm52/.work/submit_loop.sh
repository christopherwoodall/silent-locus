#!/bin/bash
# Sustained submit loop: retries add --input until ok:true or 24 attempts.
# Idempotent: same idempotency_key returns original IDs on retry.
cd ~/workspace/silent-locus
export PATH="$HOME/.local/bin:$PATH"
LOG=data/lanes/2026-10-11-hf-traj-glm52/.work/add2.log
BUNDLE=data/lanes/2026-10-11-hf-traj-glm52/.work/bundle-glm52.json
for i in $(seq 1 24); do
  echo "=== loop attempt $i @ $(date -u +%H:%M:%S) ===" >> "$LOG"
  OUT=$(timeout 1700 python3 skills/factum/scripts/factum.py --repo . add --input "$BUNDLE" 2>&1)
  echo "$OUT" | head -c 400 >> "$LOG"; echo >> "$LOG"
  if echo "$OUT" | grep -q '"ok":true'; then
    echo "SUBMIT_OK attempt=$i @ $(date -u +%H:%M:%S)" >> "$LOG"
    # export + verify while we hold momentum
    timeout 1700 python3 skills/factum/scripts/factum.py --repo . export >> "$LOG" 2>&1
    echo "EXPORT_EXIT:$?" >> "$LOG"
    timeout 1700 python3 skills/factum/scripts/factum.py --repo . verify >> "$LOG" 2>&1
    echo "VERIFY_EXIT:$?" >> "$LOG"
    exit 0
  fi
  sleep 90
done
echo "SUBMIT_LOOP_EXHAUSTED @ $(date -u +%H:%M:%S)" >> "$LOG"
exit 1
