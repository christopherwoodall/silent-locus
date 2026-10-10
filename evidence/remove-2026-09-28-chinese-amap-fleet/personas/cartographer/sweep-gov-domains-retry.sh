#!/bin/bash
# CARTOGRAPHER — retry pass for gov-domain htmx queries that failed with IncompleteRead.
set -u
OUT="$HOME/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/cartographer/raw/gov-domains"
UQ="$HOME/workspace/skills/urlquery/bin/uq_htmx.py"
if ! curl -sS --max-time 25 -o /dev/null "https://urlquery.net/" 2>/dev/null; then
  echo "EGRESS DOWN — aborting retry pass."
  exit 2
fi
echo "EGRESS UP $(date -u +%FT%TZ)"
for t in go.id gov.in gov.vn gov.eg gov.au gov.cn gov.my gov.ph gov.bd gov.za gov.ng gov.ae gov.sa gov.tr gov.ru; do
  # skip if already a good file
  if python3 -c "import json;d=json.load(open('$OUT/$t.json'));assert d.get('reports') is not None" 2>/dev/null && [ -s "$OUT/$t.json" ] && ! grep -q '^{}$' "$OUT/$t.json"; then
    # count check below; re-query only empty/failed files
    n=$(python3 -c "import json;print(len(json.load(open('$OUT/$t.json')).get('reports',[])))" 2>/dev/null || echo BAD)
    if [ "$n" != "BAD" ]; then echo "$t already has data ($n) — skipping"; continue; fi
  fi
  for attempt in 1 2 3; do
    python3 "$UQ" search --query "$t" --limit 50 > "$OUT/$t.json" 2>"$OUT/$t.err"
    n=$(python3 -c "import json;print(len(json.load(open('$OUT/$t.json')).get('reports',[])))" 2>/dev/null || echo BAD)
    if [ "$n" != "BAD" ]; then echo "$t -> $n reports (attempt $attempt)"; break; fi
    echo "$t attempt $attempt failed — sleeping 20s"
    sleep 20
  done
  sleep 6
done
echo "RETRY DONE $(date -u +%FT%TZ)"
