#!/bin/bash
# archivist: CDX coverage for the 54 WMF evidence diff URLs.
# Paced: one request per ~5s. http:// CDX endpoint (443 times out on this VM).
CDX="http://web.archive.org/cdx/search/cdx"
OUTDIR="$(dirname "$0")"
CSV="$OUTDIR/../../../../raw/openai-wikimedia-edits-2026-10-04.csv"
RESULTS="$OUTDIR/diff-coverage-results.txt"
: > "$RESULTS"
i=0
while IFS= read -r url || [ -n "$url" ]; do
  [ -z "$url" ] && continue
  i=$((i+1))
  # URL-encode the query string part for the CDX url= param (python for encoding only, no HTTP)
  q=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$url")
  for scheme in "" "http"; do
    if [ -z "$scheme" ]; then
      qurl="$q"; label="as-given"
    else
      q2=$(python3 -c "import urllib.parse,sys; u=sys.argv[1].replace('https://','http://',1); print(urllib.parse.quote(u, safe=''))" "$url")
      qurl="$q2"; label="http-scheme"
    fi
    resp=$(curl -s --max-time 60 "$CDX?url=$qurl&matchType=exact&output=text&fl=timestamp,original,statuscode,digest&collapse=digest")
    count=$(printf '%s' "$resp" | grep -c .)
    first=$(printf '%s' "$resp" | head -1 | awk '{print $1}')
    last=$(printf '%s' "$resp" | tail -1 | awk '{print $1}')
    printf '%02d | %-9s | count=%s | first=%s | last=%s | %s\n' "$i" "$label" "$count" "${first:-none}" "${last:-none}" "$url" | tee -a "$RESULTS"
    [ "$count" -gt 0 ] && printf '%s\n' "$resp" >> "$RESULTS"
    sleep 5
  done
done < "$CSV"
echo "done: $i URLs x2 scheme forms" | tee -a "$RESULTS"
