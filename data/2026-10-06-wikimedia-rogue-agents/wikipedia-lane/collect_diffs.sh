#!/bin/bash
# revision-enumerator phase 2: per-revision compare API diffs, paced >=6s.
# Passive public OSINT only. Nothing is edited on any wiki.
set -u
UA="revision-enumerator/2026-10-06 (research; silent-locus hunt)"
LANE="$(dirname "$0")"
DIFFS="$LANE/diffs"
LOG="$LANE/collection.log"
PACE=6

get() { # get <outfile> <url>
  curl -s -m 60 -A "$UA" "$2" -o "$1" -w "%{http_code}" > /tmp/_code2
  code=$(cat /tmp/_code2)
  echo "$(date -u +%FT%TZ) HTTP=$code url=$2" >> "$LOG"
  sleep "$PACE"
  [ "$code" = "200" ]
}

LIST="$LANE/_diff_list.txt"
python3 "$LANE/_emit_list.py" "$LANE/records.json" "$LIST"

while read -r host oldid parentid; do
  out="$DIFFS/${host}_${oldid}.txt"
  if [ "$parentid" -gt 0 ]; then
    url="https://${host}/w/api.php?action=compare&fromrev=${parentid}&torev=${oldid}&format=json&formatversion=2"
    from="fromrev=${parentid}"
  else
    url="https://${host}/w/api.php?action=compare&fromtext=&fromslots=main&torev=${oldid}&format=json&formatversion=2"
    from="fromtext=(empty base)"
  fi
  tmp=$(mktemp)
  if get "$tmp" "$url"; then
    {
      echo "# MediaWiki compare API response (public endpoint) for ${host} oldid=${oldid} ${from}"
      echo "# retrieved: $(date -u +%FT%TZ)"
      cat "$tmp"
    } > "$out"
    echo "OK $host $oldid diff" >> "$LOG"
  else
    echo "FAIL $host $oldid diff HTTP=$(cat /tmp/_code2)" >> "$LOG"
    rm -f "$out"
  fi
  rm -f "$tmp"
done < "$LIST"
echo "$(date -u +%FT%TZ) DIFF PHASE DONE" >> "$LOG"
