#!/bin/bash
# Gap-fill backfill: sample the 10:52->12:45 UTC coverage gap after the new-fleets agent died.
# Polished polite pacing (delay 10 between paginated requests, 15s between queries).
cd /home/hatch/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/new-fleets || exit 1
i=8
for off in 150 300 450 600 750 900 1050 1200 1350; do
  timeout 300 ~/workspace/skills/urlquery/bin/uq_htmx.py search \
    --query "http" --limit 96 --offset "$off" --delay 10 \
    > "raw/window${i}.json" 2>"raw/window${i}.err" || {
      echo "gapfill: offset $off FAILED" >> raw/gapfill2.log
      i=$((i+1)); sleep 30; continue
    }
  python3 cluster.py "raw/window${i}.json" > "analysis-${i}.txt" 2>&1
  n=$(python3 -c "import json;print(len(json.load(open('raw/window${i}.json'))['reports']))")
  echo "gapfill: window${i}.json offset $off -> ${n} reports" >> raw/gapfill2.log
  i=$((i+1))
  sleep 15
done
echo "gapfill: DONE $(date -u +%FT%TZ)" >> raw/gapfill2.log
