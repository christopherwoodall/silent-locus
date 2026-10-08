#!/bin/bash
# REVISION-PULLER-00R: RESUME pass for chunk-00 after runtime infra error.
# Previous worker (pull.sh) completed ranks 1,4,5,6,8,9,10,11,12,13 and died
# mid-pull of rank 14 (14.jsonl is PARTIAL: 500 lines, last ts 2026-09-17).
# This resume script:
#   - re-pulls rank 14 from scratch (overwrite),
#   - pulls all remaining chunk-00 ranks (15..46),
#   - skips any file that already looks complete (non-empty + first-line
#     "article" field equals the expected title).
# HTTP via curl only; python3 only for encoding/JSON processing.
# Pace: <=1 request per 5 seconds to en.wikipedia.org.
set -u
BASE="$HOME/workspace/silent-locus-top500"
SCAN="$BASE/data/2026-10-06-wikipedia-top500-infra-scan/raw"
CHUNK="$SCAN/chunks/chunk-00"
OUTDIR="$SCAN/revisions"
WORKER="$BASE/workers/rev-puller-00"
mkdir -p "$OUTDIR" "$WORKER"
UA="silent-locus-top500-scan/1.0 (research)"
API="https://en.wikipedia.org/w/api.php"
RESP=/tmp/rv00r_resp.json
START=$(date +%s)

log_err() { echo "$(date -u +%FT%TZ) RESUME $*" >> "$WORKER/errors.log"; }
log_prog() { echo "$(date -u +%FT%TZ) RESUME $*" >> "$WORKER/progress.log"; }

RESUME_TOTAL_REV=0
RESUME_FAILURES=0
RESUME_ARTICLES=0
PERFILE="$WORKER/per-article.txt"   # keep first-pass lines; append resume lines

looks_complete() {
  # $1=rank $2=title ; returns 0 if cached file already holds this article
  local f="$OUTDIR/$1.jsonl"
  [ -s "$f" ] || return 1
  python3 - "$f" "$2" <<'EOF' >/dev/null 2>&1
import json,sys
l=open(sys.argv[1],encoding='utf-8').readline()
d=json.loads(l)
sys.exit(0 if d.get("article")==sys.argv[2] else 1)
EOF
}

first=1
while IFS=$'\t' read -r rank title; do
  [ -z "${rank:-}" ] && continue
  if [ "$rank" = "14" ]; then
    log_prog "rank=14: cached file is PARTIAL (500 lines, last ts 2026-09-17) -> re-pulling"
  elif looks_complete "$rank" "$title"; then
    log_prog "SKIP rank=$rank title=$title (already cached)"
    continue
  fi
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
d=json.load(open("/tmp/rv00r_resp.json"))
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
    RESUME_FAILURES=$((RESUME_FAILURES+1))
  else
    echo "$rank"$'\t'"$title"$'\t'"$count" >> "$PERFILE"
    RESUME_TOTAL_REV=$((RESUME_TOTAL_REV+count))
    RESUME_ARTICLES=$((RESUME_ARTICLES+1))
  fi
  log_prog "DONE rank=$rank title=$title revs=$count failed=$failed"
done < "$CHUNK"

END=$(date +%s)
WALL=$((END-START))
# Merge per-article lines: first-pass lines (10) + resume lines (appended)
FIRST_DONE=$(( $(wc -l < "$PERFILE") - RESUME_ARTICLES ))
GRAND_REV=$(awk -F'\t' '{s+=$3} END{print s}' "$PERFILE")
{
  echo "# REVISION-PULLER-00 findings (chunk-00, wikipedia-top500-infra-scan)"
  echo ""
  echo "- First pass: 2026-10-06T20:45:10Z .. 2026-10-06T21:01:50Z (worker 00, died on runtime infra error at START of rank 14)"
  echo "- Resume pass: $(date -u -d @$START +%FT%TZ) .. $(date -u -d @$END +%FT%TZ), wall $((WALL/3600))h $((WALL%3600/60))m $((WALL%60))s"
  echo "- Chunk articles: $(wc -l < "$CHUNK")"
  echo "- Articles cached successfully: $(wc -l < "$PERFILE") (first pass: $FIRST_DONE, resume pass: $RESUME_ARTICLES)"
  echo "- Articles failed: $RESUME_FAILURES (see errors.log)"
  echo "- Total revisions cached (grand): $GRAND_REV"
  echo "- Revision window: 2020-01-01T00:00:00Z .. 2026-10-07T00:00:00Z (rvdir=older, rvlimit=500)"
  echo "- Cache dir: data/2026-10-06-wikipedia-top500-infra-scan/raw/revisions/ (<rank>.jsonl)"
  echo ""
  echo "## Resume pass: per-article revision counts (rank, title, revisions)"
  echo ""
  echo '```'
  tail -n "$RESUME_ARTICLES" "$PERFILE"
  echo '```'
  echo ""
  echo "- Resume pass total revisions: $RESUME_TOTAL_REV, articles completed: $RESUME_ARTICLES, failures: $RESUME_FAILURES"
  echo ""
  echo "## First pass: per-article revision counts (rank, title, revisions)"
  echo ""
  echo '```'
  head -n "$FIRST_DONE" "$PERFILE"
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
log_prog "RESUME FINISHED total=$RESUME_TOTAL_REV articles=$RESUME_ARTICLES failures=$RESUME_FAILURES wall=${WALL}s grand=$GRAND_REV"
echo "RESUME FINISHED total=$RESUME_TOTAL_REV articles=$RESUME_ARTICLES failures=$RESUME_FAILURES wall=${WALL}s grand=$GRAND_REV"
