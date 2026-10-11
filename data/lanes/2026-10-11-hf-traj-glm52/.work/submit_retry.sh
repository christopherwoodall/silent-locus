#!/bin/bash
cd ~/workspace/silent-locus
export PATH="$HOME/.local/bin:$PATH"
LOG=data/lanes/2026-10-11-hf-traj-glm52/.work/add.log
for i in $(seq 1 40); do
  OUT=$(python3 skills/factum/scripts/factum.py --repo . add --input data/lanes/2026-10-11-hf-traj-glm52/.work/bundle-glm52.json 2>&1)
  echo "attempt $i: $(echo "$OUT" | head -c 300)" >> "$LOG"
  if echo "$OUT" | grep -q '"ok":true'; then
    echo "SUBMIT_OK attempt=$i" >> "$LOG"
    exit 0
  fi
  sleep 55
done
echo "SUBMIT_FAILED after 40 attempts" >> "$LOG"
exit 1
