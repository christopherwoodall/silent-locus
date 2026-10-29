#!/bin/bash
# REVISION-PULLER-07: Wikipedia top-500 infra scan, chunk-07 (ranks 296-339)
# Methodology: docs/methodology.md. curl ONLY for HTTP. python3 for URL-encoding + JSON only.
# Pace: >=5s between requests to en.wikipedia.org. UA per task.
set -u
BASE="$HOME/workspace/silent-locus-top500"
RAW="$BASE/data/2026-10-06-wikipedia-top500-infra-scan/raw"
CHUNK="$RAW/chunks/chunk-07"
REVDIR="$RAW/revisions"
WORK="$BASE/workers/rev-puller-07"
LOG="$WORK/pull.log"
ERRLOG="$WORK/errors.log"
COUNTS="$WORK/counts.tsv"
PYEXTRACT="$WORK/extract.py"
UA="silent-locus-top500-scan/1.0 (research)"
START_EPOCH=$(date +%s)
: > "$LOG"; : > "$ERRLOG"; : > "$COUNTS"

cat > "$PYEXTRACT" <<'PYEOF'
import sys, json
bodyfile, outpath, rank, title = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
try:
    with open(bodyfile, encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print("JSONERR " + str(e)); sys.exit(0)
pages = (data.get("query") or {}).get("pages") or []
for p in pages:
    if p.get("missing"):
        print("MISSING"); sys.exit(0)
revs = []
for p in pages:
    for r in (p.get("revisions") or []):
        revs.append({"rank": int(rank), "article": title,
                     "revid": r.get("revid"), "parentid": r.get("parentid"),
                     "user": r.get("user"), "timestamp": r.get("timestamp"),
                     "comment": r.get("comment"), "tags": r.get("tags", []),
                     "size": r.get("size")})
with open(outpath, "a", encoding="utf-8") as f:
    for o in revs:
        f.write(json.dumps(o, ensure_ascii=False) + "\n")
cont = ((data.get("continue") or {}).get("rvcontinue")) or ""
print("OK", len(revs), cont)
PYEOF

log() { echo "$(date -u +%FT%TZ) $*" | tee -a "$LOG"; }
last_req=0
pace() {
  now=$(date +%s); elapsed=$((now - last_req))
  if [ "$elapsed" -lt 5 ]; then sleep $((5 - elapsed)); fi
  last_req=$(date +%s)
}

total=0; ok=0; failed=0

while IFS=$'\t' read -r rank title; do
  [ -z "${rank:-}" ] && continue
  out="$REVDIR/${rank}.jsonl"
  : > "$out"
  tmpbody=$(mktemp)
  enc_title=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$title")
  base_url="https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=${enc_title}&rvprop=user%7Ctimestamp%7Cids%7Ccomment%7Ctags%7Csize&rvlimit=500&rvdir=older&rvstart=2026-10-07T00%3A00%3A00Z&rvend=2020-01-01T00%3A00%3A00Z&format=json&formatversion=2"
  cont=""; count=0; tries=0
  log "START rank=$rank title='$title'"
  while :; do
    url="$base_url"
    [ -n "$cont" ] && url="${base_url}&rvcontinue=${cont}"
    pace
    if ! curl -sS --max-time 60 -A "$UA" -o "$tmpbody" "$url"; then
      tries=$((tries+1))
      log "WARN rank=$rank curl failed (try $tries)"
      if [ "$tries" -ge 3 ]; then
        echo "$(date -u +%FT%TZ) rank=$rank title='$title' error=curl_failed_3x" >> "$ERRLOG"
        failed=$((failed+1)); count=-1; break
      fi
      sleep 15; continue
    fi
    parsed=$(python3 "$PYEXTRACT" "$tmpbody" "$out" "$rank" "$title")
    set -- $parsed
    case "${1:-}" in
      JSONERR) log "WARN rank=$rank JSON parse failed"; tries=$((tries+1))
        if [ "$tries" -ge 3 ]; then
          echo "$(date -u +%FT%TZ) rank=$rank title='$title' error=json_parse_failed_3x" >> "$ERRLOG"
          failed=$((failed+1)); count=-1; break
        fi; sleep 15; continue ;;
      MISSING) log "WARN rank=$rank article missing"
        echo "$(date -u +%FT%TZ) rank=$rank title='$title' error=article_missing" >> "$ERRLOG"
        failed=$((failed+1)); count=-1; break ;;
      OK) tries=0; n="${2:-0}"; count=$((count+n)); cont="${3:-}"
          if [ -z "$cont" ]; then break; fi ;;
      *) log "WARN rank=$rank unexpected extractor output: $parsed"; sleep 15; continue ;;
    esac
  done
  rm -f "$tmpbody"
  echo -e "${rank}\t${title}\t${count}" >> "$COUNTS"
  if [ "$count" -ge 0 ]; then ok=$((ok+1)); total=$((total+count)); fi
  log "DONE rank=$rank title='$title' revisions=$count"
done < "$CHUNK"

END_EPOCH=$(date +%s)
echo "elapsed_seconds=$((END_EPOCH-START_EPOCH)) articles_ok=$ok articles_failed=$failed total_revisions=$total" | tee -a "$LOG"
