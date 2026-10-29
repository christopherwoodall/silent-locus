#!/bin/bash
# $1 = list file
fetch_one() {
  f="$1"
  base=$(echo "$f" | sed 's|misp_tf|https://threatfox.abuse.ch/downloads/misp|; s|misp_urlhaus|https://urlhaus.abuse.ch/downloads/misp|; s|misp_bazaar|https://bazaar.abuse.ch/downloads/misp|')
  # skip if already valid
  python3 -c "import json,sys; json.load(open('$f'))" 2>/dev/null && return 0
  rm -f "$f"
  for i in 1 2 3 4; do
    curl -s --max-time 180 --retry 2 -C - -o "$f" "$base" 2>/dev/null
    python3 -c "import json; json.load(open('$f'))" 2>/dev/null && return 0
    sleep 2
  done
  echo "STILL-BAD: $f"
  return 1
}
export -f fetch_one
cat "$1" | xargs -P 2 -I{} bash -c 'fetch_one "$@"' _ {}
echo "REDL DONE"
