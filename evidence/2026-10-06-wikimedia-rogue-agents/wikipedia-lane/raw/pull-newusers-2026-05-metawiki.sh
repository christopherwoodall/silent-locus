#!/bin/bash
# newusers May-2026 metawiki pull — curl only, >=2s between requests,
# descriptive User-Agent, 2 retries at 30s on HTTP error/empty page.
set -u
RAW="$HOME/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/raw"
OUT="$RAW/newusers-2026-05.metawiki.jsonl"
ERR="$RAW/newusers-2026-05.metawiki.err"
LOG="$RAW/newusers-2026-05.metawiki.pull.log"
UA='silent-locus-research/1.0 (research account-creation census; contact via repo)'
BASE='https://meta.wikimedia.org/w/api.php?action=query&list=logevents&letype=newusers&lestart=2026-06-01T00:00:00Z&leend=2026-05-01T00:00:00Z&ledir=older&lelimit=500&format=json&formatversion=2'
: > "$OUT"; : > "$ERR"; : > "$LOG"

CONT=""
PAGE=0
TOTAL=0
while true; do
  PAGE=$((PAGE+1))
  ATTEMPT=0
  HTTP="000"
  while [ $ATTEMPT -le 2 ]; do
    ATTEMPT=$((ATTEMPT+1))
    if [ -n "$CONT" ]; then
      HTTP=$(curl -sS -o /tmp/mw-page.json -w '%{http_code}' -H "User-Agent: $UA" --max-time 180 -G "$BASE" --data-urlencode "lecontinue=$CONT") || HTTP="000"
    else
      HTTP=$(curl -sS -o /tmp/mw-page.json -w '%{http_code}' -H "User-Agent: $UA" --max-time 180 "$BASE") || HTTP="000"
    fi
    if [ "$HTTP" = "200" ] && [ -s /tmp/mw-page.json ] && jq -e '.query.logevents' /tmp/mw-page.json >/dev/null 2>&1; then
      break
    fi
    echo "page=$PAGE attempt=$ATTEMPT HTTP=$HTTP fail at $(date -u +%FT%TZ)" >> "$ERR"
    [ $ATTEMPT -le 2 ] && sleep 30
  done
  if [ "$HTTP" != "200" ] || ! jq -e '.query.logevents' /tmp/mw-page.json >/dev/null 2>&1; then
    echo "STOPPED page=$PAGE: persistent failure after retries at $(date -u +%FT%TZ); partial rows=$TOTAL" >> "$ERR"
    echo "FATAL: stopped page $PAGE after retries" >> "$LOG"
    exit 1
  fi
  N=$(jq '.query.logevents | length' /tmp/mw-page.json)
  jq -c '.query.logevents[]' /tmp/mw-page.json >> "$OUT"
  TOTAL=$((TOTAL+N))
  CONT=$(jq -r '.continue.lecontinue // empty' /tmp/mw-page.json)
  echo "page=$PAGE events=$N total=$TOTAL continue=${CONT:-NONE} at $(date -u +%FT%TZ)" >> "$LOG"
  [ -z "$CONT" ] && break
  sleep 2
done
echo "DONE pages=$PAGE total=$TOTAL at $(date -u +%FT%TZ)" >> "$LOG"
exit 0
