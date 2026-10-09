#!/bin/bash
# revision-enumerator collection: paced MediaWiki API sweep of 54 evidence oldids.
# Passive public OSINT only. Nothing is edited on any wiki.
set -u
UA="revision-enumerator/2026-10-06 (research; silent-locus hunt)"
LANE="$(dirname "$0")"
RAW="$LANE/raw"
DIFFS="$LANE/diffs"
LOG="$LANE/collection.log"
PACE=6

get() { # get <outfile> <url>
  curl -s -m 60 -A "$UA" "$2" -o "$1" -w "%{http_code}" > /tmp/_code
  code=$(cat /tmp/_code)
  echo "$(date -u +%FT%TZ) HTTP=$code url=$2" >> "$LOG"
  sleep "$PACE"
  [ "$code" = "200" ]
}

echo "$(date -u +%FT%TZ) START" > "$LOG"
while read -r host oldid; do
  echo "$host|$oldid"
done < "$LANE/oldids.txt" | awk -F'|' '{print $1}' | sort -u | while read -r host; do
  ids=$(awk -v h="$host" '$1==h{print $2}' "$LANE/oldids.txt" | paste -sd'|' -)
  out="$RAW/${host}_revisions.json"
  url="https://${host}/w/api.php?action=query&prop=revisions&revids=${ids}&rvprop=ids%7Ctimestamp%7Cuser%7Ccomment%7Ctags%7Cflags%7Ccontent&rvslots=main&format=json&formatversion=2"
  if get "$out" "$url"; then echo "OK $host batch" >> "$LOG"; else echo "FAIL $host batch" >> "$LOG"; fi
done

echo "$(date -u +%FT%TZ) BATCH PHASE DONE" >> "$LOG"
