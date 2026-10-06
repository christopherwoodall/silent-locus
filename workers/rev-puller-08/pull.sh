#!/usr/bin/env bash
# REVISION-PULLER-08 — Wikipedia top-500 infra scan, chunk 08 (ranks 340-377)
# Paces at >=5s per request to en.wikipedia.org. HTTP via curl only.
set -u
BASE=~/workspace/silent-locus-top500/data/2026-10-06-wikipedia-top500-infra-scan/raw
CHUNK="$BASE/chunks/chunk-08"
OUTDIR="$BASE/revisions"
LOGDIR=~/workspace/silent-locus-top500/workers/rev-puller-08
ERRLOG="$LOGDIR/errors.log"
UA="silent-locus-top500-scan/1.0 (research)"
START_TS="2026-10-07T00:00:00Z"
END_TS="2020-01-01T00:00:00Z"
START_EPOCH=$(date -u +%s)
: > "$ERRLOG"

enc() { python3 -c 'import sys,urllib.parse; print(urllib.parse.quote(sys.argv[1]))' "$1"; }

total_revs=0; ok=0; fail=0
while IFS=$'\t' read -r rank title; do
  [ -z "${rank:-}" ] && continue
  outfile="$OUTDIR/${rank}.jsonl"
  if [ -s "$outfile" ]; then
    echo "rank $rank ($title): already cached, skipping"
    continue
  fi
  echo "rank $rank ($title): pulling..."
  enc_title=$(enc "$title")
  continue_token=""
  count=0
  fail_this=0
  : > "$outfile.tmp"
  while true; do
    url="https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=${enc_title}&rvprop=user%7Ctimestamp%7Cids%7Ccomment%7Ctags%7Csize&rvlimit=500&rvdir=older&rvstart=${START_TS}&rvend=${END_TS}&format=json&formatversion=2"
    [ -n "$continue_token" ] && url="${url}&rvcontinue=${continue_token}"
    if ! curl -sS -m 60 -A "$UA" "$url" -o /tmp/rev08_resp.json; then
      echo "$(date -u +%FT%TZ) rank=$rank title=$title ERROR curl-failed" >> "$ERRLOG"
      fail_this=1; break
    fi
    parse_out=$(python3 - "$outfile.tmp" "$rank" "$title" <<'EOF'
import json,sys
tmp, rank, title = sys.argv[1], int(sys.argv[2]), sys.argv[3]
d = json.load(open('/tmp/rev08_resp.json'))
if 'error' in d:
    print("APIERROR:"+d['error'].get('info','?')); sys.exit(2)
pages = d.get('query',{}).get('pages',[])
n = 0
with open(tmp,'a') as f:
    for p in pages:
        if p.get('missing'):
            print("MISSING"); sys.exit(3)
        for r in p.get('revisions',[]):
            f.write(json.dumps({"rank":rank,"article":title,
                "revid":r.get('revid'),"parentid":r.get('parentid'),
                "user":r.get('user'),"timestamp":r.get('timestamp'),
                "comment":r.get('comment'),"tags":r.get('tags',[]),
                "size":r.get('size')},ensure_ascii=False)+"\n")
            n += 1
print("OK:"+str(n))
c = d.get('continue',{}).get('rvcontinue','')
print("CONT:"+c)
EOF
)
    rc=$?
    status=$(echo "$parse_out" | head -1)
    if [ $rc -ne 0 ] || [[ "$status" == MISSING* || "$status" == APIERROR* ]]; then
      echo "$(date -u +%FT%TZ) rank=$rank title=$title ERROR $status" >> "$ERRLOG"
      fail_this=1; break
    fi
    n=$(echo "$parse_out" | sed -n 's/^OK://p')
    count=$((count + n))
    continue_token=$(echo "$parse_out" | sed -n 's/^CONT://p')
    if [ -z "$continue_token" ]; then break; fi
    sleep 5
  done
  if [ $fail_this -eq 0 ]; then
    mv "$outfile.tmp" "$outfile"
    echo "rank $rank ($title): $count revisions cached"
    ok=$((ok+1)); total_revs=$((total_revs+count))
  else
    echo "rank $rank ($title): FAILED (see errors.log)"
    rm -f "$outfile.tmp"
    fail=$((fail+1))
  fi
  sleep 5
done < "$CHUNK"
END_EPOCH=$(date -u +%s)
echo "$START_EPOCH $END_EPOCH $ok $fail $total_revs" > "$LOGDIR/stats.txt"
echo "DONE ok=$ok fail=$fail total_revs=$total_revs wall=$((END_EPOCH-START_EPOCH))s"
