#!/bin/bash
# 6-month temp-account autocreate pull: 2026-04-01..2026-09-30, 9 wikis.
# Endpoint: https://<host>/w/api.php?action=query&list=logevents&letype=newusers
#           &leaction=newusers/autocreate&lelimit=500&leprop=ids|timestamp|title|type
# SCOPE NOTE: leaction=newusers/autocreate only. All ~2026-* temp accounts are
# created via autocreate (verified); regular 'create' signups can never be ~2026-*.
# Fully paged via lecontinue. Pace >=6s per host. Resume via .newusers-pull-state.
set -u
RAW="$HOME/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/raw"
STATE="$RAW/.newusers-pull-state"
mkdir -p "$RAW"; touch "$STATE"
declare -A HOSTS=(
  [enwiki]="en.wikipedia.org" [testwiki]="test.wikipedia.org"
  [test2wiki]="test2.wikipedia.org" [mediawikiwiki]="www.mediawiki.org"
  [commonswiki]="commons.wikimedia.org" [incubatorwiki]="incubator.wikimedia.org"
  [simplewiki]="simple.wikipedia.org" [bgwiki]="bg.wikipedia.org"
  [metawiki]="meta.wikimedia.org"
)
ORDER="enwiki testwiki test2wiki mediawikiwiki commonswiki incubatorwiki simplewiki bgwiki metawiki"
if [ $# -gt 0 ]; then ORDER="$*"; fi
next_month() { date -u -d "$1-01 +1 month" +%Y-%m; }
pull_chunk() {
  local short="$1" host="$2" ym="$3" nm start end cont page total
  nm=$(next_month "$ym"); start="${nm}-01T00:00:00Z"; end="${ym}-01T00:00:00Z"
  local out="$RAW/newusers-2026-04-01_2026-09-30.${short}.jsonl"
  cont=""; page=0; total=0
  while :; do
    sleep 6
    page=$((page+1))
    local resp
    resp=$(curl -s --get "https://$host/w/api.php" \
      --data-urlencode 'action=query' --data-urlencode 'list=logevents' \
      --data-urlencode 'letype=newusers' --data-urlencode 'leaction=newusers/autocreate' \
      --data-urlencode "lestart=$start" --data-urlencode "leend=$end" \
      --data-urlencode 'leprop=ids|timestamp|title|type' --data-urlencode 'lelimit=500' \
      --data-urlencode 'format=json' ${cont:+--data-urlencode "lecontinue=$cont"})
    if ! echo "$resp" | python3 -c "import json,sys; json.load(sys.stdin)" 2>/dev/null; then
      echo "  !! non-JSON response $short $ym p$page (retry once)"; sleep 30
      resp=$(curl -s --get "https://$host/w/api.php" \
        --data-urlencode 'action=query' --data-urlencode 'list=logevents' \
        --data-urlencode 'letype=newusers' --data-urlencode 'leaction=newusers/autocreate' \
        --data-urlencode "lestart=$start" --data-urlencode "leend=$end" \
        --data-urlencode 'leprop=ids|timestamp|title|type' --data-urlencode 'lelimit=500' \
        --data-urlencode 'format=json' ${cont:+--data-urlencode "lecontinue=$cont"})
    fi
    local n lc_token lines
    n=$(python3 - "$resp" <<'EOF'
import json,sys
try:
    d=json.loads(sys.argv[1])
    ev=d['query']['logevents']
    for e in ev: print(json.dumps(e, separators=(',',':')))
except Exception as ex:
    print(f"PARSE_ERROR:{ex}", file=sys.stderr)
EOF
)
    lines=$(echo "$n" | grep -c '^{' || true)
    echo "$n" | grep '^{' >> "$out"
    total=$((total+lines))
    lc_token=$(python3 - "$resp" <<'EOF'
import json,sys
try:
    d=json.loads(sys.argv[1])
    print(d.get('continue',{}).get('lecontinue') or '', end='')
except Exception:
    print('ERR', end='')
EOF
)
    [ "$lc_token" = "ERR" ] && { echo "  !! parse failed twice $short $ym p$page, aborting chunk"; return 1; }
    cont="$lc_token"
    [ -z "$cont" ] && break
    [ "$page" -ge 5000 ] && { echo "  !! page cap 5000 hit $short $ym"; return 1; }
  done
  echo "$short:$ym" >> "$STATE"
  echo "  done $short $ym: $total events ($page pages)"
}
echo "pull started $(date -u +%FT%TZ)"
for short in $ORDER; do
  for ym in 2026-04 2026-05 2026-06 2026-07 2026-08 2026-09; do
    if grep -qx "$short:$ym" "$STATE" 2>/dev/null; then echo "  skip $short $ym (done)"; continue; fi
    echo "== $short $ym =="
    pull_chunk "$short" "${HOSTS[$short]}" "$ym" || echo "  !! chunk failed: $short $ym"
  done
done
echo "pull finished $(date -u +%FT%TZ)"
