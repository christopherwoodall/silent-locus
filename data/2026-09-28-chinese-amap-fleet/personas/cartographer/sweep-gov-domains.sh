#!/bin/bash
# CARTOGRAPHER LANE — Gov domains by country: live urlquery htmx sweep.
# Run when egress is up. Writes durable JSON per TLD.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/raw/gov-domains"
mkdir -p "$OUT"

echo "== egress watch (retry until up, max 6h) =="
TRIES=0
while ! curl -sS --max-time 25 -o /dev/null "https://urlquery.net/" 2>/dev/null; do
  TRIES=$((TRIES+1))
  if [ "$TRIES" -ge 72 ]; then
    echo "EGRESS STILL DOWN after 6h — giving up."
    exit 2
  fi
  echo "egress down, try $TRIES/72 — sleeping 300s"
  sleep 300
done
echo "EGRESS UP $(date -u +%FT%TZ)"

UQ="$HOME/workspace/skills/urlquery/bin/uq_htmx.py"
q() { # query, limit, outfile
  python3 "$UQ" search --query "$1" --limit "$2" > "$OUT/$3.json" 2>"$OUT/$3.err"
  n=$(python3 -c "import json;d=json.load(open('$OUT/$3.json'));print(len(d.get('reports',[])))" 2>/dev/null || echo ERR)
  echo "$1 -> $3.json : $n reports"
  sleep 6   # polite pacing: <=1 req / 5s
}

for t in go.id gov.br gov.in gov.vn gov.eg gov.uk gov.au gov.ca gov.cn gov.tw gov.hk gov.sg gov.my gov.ph gov.th gov.pk gov.bd gov.za gov.ng gov.ke gob.mx gov.ae gov.sa gov.tr gov.ru; do
  q "$t" 50 "$t"
done
echo "DONE $(date -u +%FT%TZ)"
