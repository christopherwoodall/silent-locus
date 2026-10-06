#!/bin/bash
# REVISION-PULLER-05 re-pull: ranks 217-224 were present and complete after the
# main run (pull.log + counts.tsv + git blobs confirm), but were deleted from
# the worktree by an unidentified external process between 20:48 and 21:02 UTC
# (no other worker's logs reference these ranks; no chunk overlap). Re-pull them.
set -u
BASE="$HOME/workspace/silent-locus-top500"
RAW="$BASE/data/2026-10-06-wikipedia-top500-infra-scan/raw"
CHUNK="$BASE/workers/rev-puller-05/repull_missing.tsv"
REVDIR="$RAW/revisions"
WORK="$BASE/workers/rev-puller-05"
LOG="$WORK/repull.log"
ERRLOG="$WORK/errors.log"
COUNTS="$WORK/recounts.tsv"
PYEXTRACT="$WORK/extract.py"
UA="silent-locus-top500-scan/1.0 (research)"
START_EPOCH=$(date +%s)
: > "$LOG"; : > "$COUNTS"

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
  log "RESTART rank=$rank title='$title'"
  while :; do
    url="$base_url"
    if [ -n "$cont" ]; then
      enc_cont=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$cont")
      url="${base_url}&rvcontinue=${enc_cont}"
    fi
    pace
    if ! curl -sS --max-time 60 -A "$UA" -o "$tmpbody" "$url"; then
      tries=$((tries+1)); log "WARN rank=$rank curl failed (try $tries)"
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
      APIERR) log "WARN rank=$rank API error: ${parsed#APIERR }"
        echo "$(date -u +%FT%TZ) rank=$rank title='$title' error=api_${parsed#APIERR }" >> "$ERRLOG"
        failed=$((failed+1)); count=-1; break ;;
      MISSING) log "WARN rank=$rank article missing"
        echo "$(date -u +%FT%TZ) rank=$rank title='$title' error=article_missing" >> "$ERRLOG"
        failed=$((failed+1)); count=-1; break ;;
      OK) tries=0; n="${2:-0}"; count=$((count+n)); cont="${3:-}"
          if [ -z "$cont" ]; then break; fi ;;
      *) log "WARN rank=$rank unexpected extractor output: $parsed"; sleep 15; continue ;;
    esac
  done
  rm -f "$tmpbody"
  printf '%s\t%s\t%s\n' "$rank" "$title" "$count" >> "$COUNTS"
  if [ "$count" -ge 0 ]; then ok=$((ok+1)); total=$((total+count)); fi
  log "REDONE rank=$rank title='$title' revisions=$count"
done < "$CHUNK"

END_EPOCH=$(date +%s)
WALL=$((END_EPOCH - START_EPOCH))
log "RE-PULL FINISHED ok=$ok failed=$failed total_revisions=$total wall=${WALL}s"
