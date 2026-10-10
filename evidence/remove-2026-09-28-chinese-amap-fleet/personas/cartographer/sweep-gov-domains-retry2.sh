#!/bin/bash
# CARTOGRAPHER — final retry pass for gov-domain htmx failures, limit=20 (chunked-reader safe).
set -u
OUT="$HOME/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/cartographer/raw/gov-domains"
UQ="$HOME/workspace/skills/urlquery/bin/uq_htmx.py"
if ! curl -sS --max-time 25 -o /dev/null "https://urlquery.net/" 2>/dev/null; then
  echo "EGRESS DOWN — aborting."
  exit 2
fi
echo "EGRESS UP $(date -u +%FT%TZ)"
for t in gov.vn gov.eg gov.au gov.cn gov.my gov.ph gov.bd gov.za gov.ng gov.ae gov.sa gov.tr gov.ru; do
  n=$(python3 -c "import json;print(len(json.load(open('$OUT/$t.json')).get('reports',[])))" 2>/dev/null || echo BAD)
  if [ "$n" != "BAD" ]; then echo "$t already OK ($n) — skipping"; continue; fi
  for attempt in 1 2 3; do
    python3 "$UQ" search --query "$t" --limit 20 > "$OUT/$t.json" 2>"$OUT/$t.err"
    n=$(python3 -c "import json;print(len(json.load(open('$OUT/$t.json')).get('reports',[])))" 2>/dev/null || echo BAD)
    if [ "$n" != "BAD" ]; then echo "$t -> $n reports (attempt $attempt)"; break; fi
    echo "$t attempt $attempt failed — sleeping 20s"; sleep 20
  done
  sleep 6
done
echo "FINAL RETRY DONE $(date -u +%FT%TZ)"
