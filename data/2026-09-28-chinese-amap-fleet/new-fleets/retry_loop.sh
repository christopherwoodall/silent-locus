#!/bin/bash
# new-fleets retry loop: keep trying the keyless htmx collection every 20 min
# until VM egress recovers. Single attempt per cycle, polite pacing.
# Logs to LOOP.md; raw windows to raw/windowN.json; cluster analysis to analysis-N.txt.
# Kill this when the new-fleets agent is stood down.
cd /home/hatch/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/new-fleets || exit 1
mkdir -p raw
i=3
echo "## Retry loop started $(date -u +%FT%TZ)" >> LOOP.md
while true; do
  ts=$(date -u +%FT%TZ)
  if timeout 300 ~/workspace/skills/urlquery/bin/uq_htmx.py search \
      --query "date:[2026-10-05 TO 2026-10-05]" --limit 96 --delay 8 \
      > "raw/window${i}.json" 2>"raw/window${i}.err"; then
    n=$(python3 -c "import json;print(len(json.load(open('raw/window${i}.json')).get('reports',[])))" 2>/dev/null || echo 0)
    echo "- ${ts}: FETCH OK window${i}.json (${n} reports)" >> LOOP.md
    if [ "${n:-0}" -gt 0 ]; then
      python3 cluster.py "raw/window${i}.json" > "analysis-${i}.txt" 2>&1
      echo "  NEEDS GRADING: see analysis-${i}.txt" >> LOOP.md
      i=$((i+1))
    fi
    sleep 1200
  else
    echo "- ${ts}: egress still down (uq_htmx.py failed)" >> LOOP.md
    sleep 1200
  fi
done
