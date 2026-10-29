#!/bin/bash
# REVISION-PULLER-00: pull 2020-01-01..2026-10-07 revision history for chunk-00 articles.
# HTTP via curl only; python3 only for encoding/JSON processing. <=1 req / 5s to en.wikipedia.org.
set -u
BASE="$HOME/workspace/silent-locus-top500"
SCAN="$BASE/data/2026-10-06-wikipedia-top500-infra-scan/raw"
CHUNK="$SCAN/chunks/chunk-00"
OUTDIR="$SCAN/revisions"
WORKER="$BASE/workers/rev-puller-00"
mkdir -p "$OUTDIR" "$WORKER"
UA="silent-locus-top500-scan/1.0 (research)"
API="https://en.wikipedia.org/w/api.php"
RESP=/tmp/rv00_resp.json
START=$(date +%s)

log_err() { echo "$(date -u +%FT%TZ) $*" >> "$WORKER/errors.log"; }
log_prog() { echo "$(date -u +%FT%TZ) $*" >> "$WORKER/progress.log"; }

TOTAL_REV=0
FAILURES=0
PERFILE="$WORKER/per-article.txt"
: > "$PERFILE"

first=1
while IFS=$'\t' read -r rank title; do
  [ -z "${rank:-}" ] && continue
  enc=$(python3 -c 'import sys,urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$title")
  outfile="$OUTDIR/${rank}.jsonl"
  : > "$outfile"
  cont=""
  count=0
  failed=0
  log_prog "START rank=$rank title=$title"
  while :; do
    if [ "$first" -eq 0 ]; then sleep 5; fi
    first=0
    url="${API}?action=query&prop=revisions&titles=${enc}&rvprop=user|timestamp|ids|comment|tags|size&rvlimit=500&rvdir=older&rvstart=2026-10-07T00:00:00Z&rvend=2020-01-01T00:00:00Z&format=json&formatversion=2"
    [ -n "$cont" ] && url="${url}&rvcontinue=${cont}"
    code=""
    attempt=0
    while [ "$attempt" -lt 3 ]; do
      attempt=$((attempt+1))
      code=$(curl -sS --max-time 60 -A "$UA" -w "%{http_code}" -o "$RESP" "$url" 2>>"$WORKER/errors.log") || code="000"
      [ "$code" = "200" ] && break
      log_err "HTTP $code attempt=$attempt rank=$rank title=$title"
      sleep $((15*attempt))
    done
    if [ "$code" != "200" ]; then
      log_err "FAILED rank=$rank title=$title after 3 attempts (last http=$code)"
      failed=1
      break
    fi
    res=$(RANK="$rank" TITLE="$title" OUTF="$outfile" CONT="$cont" python3 - <<'EOF'
import json,os,urllib.parse,sys
rank=int(os.environ["RANK"]); title=os.environ["TITLE"]; outf=os.environ["OUTF"]
d=json.load(open("/tmp/rv00_resp.json"))
if "error" in d:
    print("APIERROR:"+str(d["error"].get("code","?"))); sys.exit(0)
pages=d.get("query",{}).get("pages",[])
if not pages:
    print("NOMATCH"); sys.exit(0)
p=pages[0]
if p.get("missing"):
    print("MISSING"); sys.exit(0)
revs=p.get("revisions",[])
with open(outf,"a",encoding="utf-8") as f:
    for r in revs:
        obj={"rank":rank,"article":title,"revid":r.get("revid"),"parentid":r.get("parentid"),
             "user":r.get("user"),"timestamp":r.get("timestamp"),
             "comment":r.get("comment","") or "","tags":r.get("tags",[]),"size":r.get("size")}
        f.write(json.dumps(obj,ensure_ascii=False)+"\n")
nxt=d.get("continue",{}).get("rvcontinue","")
print("OK\t%d\t%s"%(len(revs),urllib.parse.quote(nxt,safe="")))
EOF
)
    status=$(printf '%s' "$res" | cut -f1)
    if [ "$status" != "OK" ]; then
      log_err "API/status=$status rank=$rank title=$title"
      failed=1
      break
    fi
    n=$(printf '%s' "$res" | cut -f2)
    cont=$(printf '%s' "$res" | cut -f3)
    count=$((count+n))
    if [ -z "$cont" ]; then break; fi
  done
  if [ "$failed" -eq 1 ]; then
    FAILURES=$((FAILURES+1))
  else
    echo "$rank"$'\t'"$title"$'\t'"$count" >> "$PERFILE"
    TOTAL_REV=$((TOTAL_REV+count))
  fi
  log_prog "DONE rank=$rank title=$title revs=$count failed=$failed"
done < "$CHUNK"

END=$(date +%s)
WALL=$((END-START))
{
  echo "# REVISION-PULLER-00 findings (chunk-00)"
  echo ""
  echo "- Started: $(date -u -d @$START +%FT%TZ), ended: $(date -u -d @$END +%FT%TZ)"
  echo "- Wall time: $((WALL/3600))h $((WALL%3600/60))m $((WALL%60))s"
  echo "- Articles attempted: $(wc -l < "$CHUNK")"
  echo "- Articles cached successfully: $(wc -l < "$PERFILE")"
  echo "- Articles failed: $FAILURES (see errors.log)"
  echo "- Total revisions cached: $TOTAL_REV"
  echo "- Revision window: 2020-01-01T00:00:00Z .. 2026-10-07T00:00:00Z (rvdir=older, rvlimit=500)"
  echo "- Cache dir: data/2026-10-06-wikipedia-top500-infra-scan/raw/revisions/ (<rank>.jsonl)"
  echo ""
  echo "## Per-article revision counts (rank, title, revisions)"
  echo ""
  echo '```'
  cat "$PERFILE"
  echo '```'
  echo ""
  echo "## Errors"
  echo ""
  if [ -s "$WORKER/errors.log" ]; then
    echo '```'
    cat "$WORKER/errors.log"
    echo '```'
  else
    echo "None."
  fi
} > "$WORKER/FINDINGS.md"
log_prog "FINISHED total=$TOTAL_REV failures=$FAILURES wall=${WALL}s"
echo "FINISHED total=$TOTAL_REV failures=$FAILURES wall=${WALL}s"
