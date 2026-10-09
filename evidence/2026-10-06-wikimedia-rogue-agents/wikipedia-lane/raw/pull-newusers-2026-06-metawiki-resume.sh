#!/bin/bash
# Resume of June-2026 metawiki newusers pull (died page 456, proxy timeouts).
# Partial file covers 2026-06-01 -> 2026-06-18T13:49:55Z (227,500 events).
# This pulls the missing window 2026-06-18T13:49:55Z -> 2026-06-30, then merges+dedupe.
set -u
RAW="$HOME/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/raw"
OUT="$RAW/newusers-2026-06.metawiki.resume.jsonl"
ERR="$RAW/newusers-2026-06.metawiki.resume.err"
LOG="$RAW/newusers-2026-06.metawiki.resume.log"
UA='silent-locus-research/1.0 (research account-creation census; contact via repo)'
BASE='https://meta.wikimedia.org/w/api.php?action=query&list=logevents&letype=newusers&lestart=2026-07-01T00:00:00Z&leend=2026-06-18T13:49:55Z&ledir=older&lelimit=500&format=json&formatversion=2'
: > "$OUT"; : > "$ERR"; : > "$LOG"

CONT=""
PAGE=0
TOTAL=0
while true; do
  PAGE=$((PAGE+1))
  ATTEMPT=0
  HTTP="000"
  while [ $ATTEMPT -le 4 ]; do
    ATTEMPT=$((ATTEMPT+1))
    if [ -n "$CONT" ]; then
      HTTP=$(curl -sS -o /tmp/mw-resume.json -w '%{http_code}' -H "User-Agent: $UA" --max-time 240 -G "$BASE" --data-urlencode "lecontinue=$CONT") || HTTP="000"
    else
      HTTP=$(curl -sS -o /tmp/mw-resume.json -w '%{http_code}' -H "User-Agent: $UA" --max-time 240 "$BASE") || HTTP="000"
    fi
    if [ "$HTTP" = "200" ] && [ -s /tmp/mw-resume.json ] && jq -e '.query.logevents' /tmp/mw-resume.json >/dev/null 2>&1; then
      break
    fi
    echo "page=$PAGE attempt=$ATTEMPT HTTP=$HTTP fail at $(date -u +%FT%TZ)" >> "$ERR"
    [ $ATTEMPT -le 4 ] && sleep 60
  done
  if [ "$HTTP" != "200" ] || ! jq -e '.query.logevents' /tmp/mw-resume.json >/dev/null 2>&1; then
    echo "STOPPED page=$PAGE after 4 retries at $(date -u +%FT%TZ); partial rows=$TOTAL" >> "$ERR"
    echo "FATAL page=$PAGE" >> "$LOG"
    exit 1
  fi
  N=$(jq '.query.logevents | length' /tmp/mw-resume.json)
  jq -c '.query.logevents[]' /tmp/mw-resume.json >> "$OUT"
  TOTAL=$((TOTAL+N))
  CONT=$(jq -r '.continue.lecontinue // empty' /tmp/mw-resume.json)
  echo "page=$PAGE events=$N total=$TOTAL continue=${CONT:-NONE} at $(date -u +%FT%TZ)" >> "$LOG"
  [ -z "$CONT" ] && break
  sleep 3
done
echo "DONE pages=$PAGE total=$TOTAL at $(date -u +%FT%TZ)" >> "$LOG"
# merge with partial, dedupe by logid
cat "$RAW/newusers-2026-06.metawiki.jsonl" "$OUT" | python3 -c "
import json,sys
seen=set(); out=0
for line in sys.stdin:
    try: e=json.loads(line)
    except: continue
    lid=e.get('logid')
    if lid in seen: continue
    seen.add(lid); out+=1
    print(json.dumps(e))
" > "$RAW/newusers-2026-06.metawiki.merged.jsonl"
echo "MERGED total=$(wc -l < "$RAW/newusers-2026-06.metawiki.merged.jsonl") at $(date -u +%FT%TZ)" >> "$LOG"
mv "$RAW/newusers-2026-06.metawiki.merged.jsonl" "$RAW/newusers-2026-06.metawiki.jsonl"
echo "SWAPPED at $(date -u +%FT%TZ)" >> "$LOG"
exit 0
