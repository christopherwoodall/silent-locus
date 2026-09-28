#!/bin/bash
# Slow paced re-pull of the 6 cited reports; 25s spacing avoids urlquery rate-limit 404s.
OUT="$HOME/workspace/muse-home/projects/swarmtraces-hf-corpus/data/dse-wiki-verification-2026-09-27/reports"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
for id in 01fd9706-d9d0-42e4-b813-448a541a2571 d6669745-83d2-4628-82fa-87420ae6a5d7 6fd6d3cb-2d66-408e-91e4-910352cc0cfc c08684cc-3da4-4d53-a288-0d014243c075 1ad9c2e8-96ff-44af-b446-b717bcb995b4 e044dea5-ca3b-4e3c-9083-f422148ffd77; do
  code=$(curl -s -A "$UA" --max-time 25 -o "$OUT/$id.json" -w "%{http_code}" "https://urlquery.net/report/$id/json")
  ok=$(python3 -c "import json; d=json.load(open('$OUT/$id.json')); print('JSON-OK' if d.get('report_id')=='$id' else 'MISMATCH')" 2>/dev/null || echo "NOT-JSON")
  echo "$id -> $code $ok"
  sleep 25
done
