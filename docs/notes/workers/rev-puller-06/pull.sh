#!/usr/bin/env bash
# rev-puller-06: revision-history puller for chunk-06 of the Wikipedia top-500
# infra scan. curl for HTTP (VM Python HTTP stacks break on the egress proxy),
# python3 for URL-encoding + JSON only. Pace: 1 request per 5s.
# Never stops the chunk on one article failure; logs to workers/rev-puller-06/errors.log.
set -u

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CHUNK="$ROOT/data/2026-10-06-wikipedia-top500-infra-scan/raw/chunks/chunk-06"
REVDIR="$ROOT/data/2026-10-06-wikipedia-top500-infra-scan/raw/revisions"
WORK="$ROOT/workers/rev-puller-06"
ERRLOG="$WORK/errors.log"
PROG="$WORK/progress.log"
UA="silent-locus-top500-scan/1.0 (research)"
PACE=5
MAX_ATTEMPTS=4

mkdir -p "$REVDIR" "$WORK"
: > "$ERRLOG"
: > "$PROG"

START_EPOCH=$(date +%s)
START_UTC=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$PROG"; }

urlencode() { python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=""))' "$1"; }

fetch_article() {
    local rank="$1" title="$2"
    local enc out rvcontinue=""
    enc="$(urlencode "$title")"
    out="$REVDIR/${rank}.jsonl"
    : > "$out"
    local total=0 missing_seen=0
    local base="https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=${enc}&rvprop=user%7Ctimestamp%7Cids%7Ccomment%7Ctags%7Csize&rvlimit=500&rvdir=older&rvstart=2026-10-07T00%3A00%3A00Z&rvend=2020-01-01T00%3A00%3A00Z&format=json&formatversion=2&redirects=1&maxlag=5"

    while :; do
        sleep "$PACE"
        local url="$base"
        if [ -n "$rvcontinue" ]; then
            url="${url}&rvcontinue=$(urlencode "$rvcontinue")"
        fi
        local tmp resp_ok=0 attempt=0
        tmp="$(mktemp)"
        while [ $attempt -lt $MAX_ATTEMPTS ]; do
            attempt=$((attempt + 1))
            if curl -sS --max-time 90 -A "$UA" "$url" -o "$tmp" -w "%{http_code}" > /dev/null 2>>"$PROG"; then
                resp_ok=1
                break
            fi
            log "curl fail (attempt $attempt/$MAX_ATTEMPTS) rank=$rank title=$title"
            sleep 20
        done
        if [ $resp_ok -eq 0 ]; then
            log "ERROR rank=$rank title=$title curl failed after $MAX_ATTEMPTS attempts"
            echo "$rank	$title	curl_failed" >> "$ERRLOG"
            rm -f "$tmp"
            return 1
        fi
        local stderr_file
        stderr_file="$(mktemp)"
        # parser stdout = JSONL lines, stderr = markers
        if python3 "$WORK/parse.py" "$tmp" "$rank" "$title" >> "$out" 2>"$stderr_file"; then
            :
        else
            rc=$?
            if grep -q '^APIERROR maxlag' "$stderr_file"; then
                log "maxlag on rank=$rank page, sleeping 30s and retrying"
                rm -f "$tmp" "$stderr_file"
                sleep 30
                continue
            fi
            log "ERROR rank=$rank title=$title parser rc=$rc: $(tr '\n' ' ' < "$stderr_file")"
            echo "$rank	$title	parse_error" >> "$ERRLOG"
            rm -f "$tmp" "$stderr_file"
            return 1
        fi
        if grep -q '^MISSING ' "$stderr_file"; then
            missing_seen=1
        fi
        local page_n
        page_n=$(grep '^REVCOUNT ' "$stderr_file" | awk '{print $2}')
        total=$((total + ${page_n:-0}))
        rvcontinue=$(grep '^RVCONTINUE ' "$stderr_file" | sed 's/^RVCONTINUE //')
        rm -f "$tmp" "$stderr_file"
        if [ -z "$rvcontinue" ]; then
            break
        fi
    done

    if [ "$total" -eq 0 ] && [ "$missing_seen" -eq 1 ]; then
        log "ERROR rank=$rank title=$title article missing/invalid, zero revisions"
        echo "$rank	$title	missing" >> "$ERRLOG"
        return 1
    fi
    log "done rank=$rank title='$title' revisions=$total"
    echo "$rank	$title	$total" >> "$WORK/counts.tsv"
}

: > "$WORK/counts.tsv"

count=0
while IFS=$'\t' read -r rank title; do
    [ -z "$rank" ] && continue
    count=$((count + 1))
    fetch_article "$rank" "$title" || true
done < "$CHUNK"

END_EPOCH=$(date +%s)
END_UTC=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
WALL=$((END_EPOCH - START_EPOCH))
TOTAL_REV=$(awk -F'\t' '{s+=$3} END {print s+0}' "$WORK/counts.tsv")
N_OK=$(wc -l < "$WORK/counts.tsv")
N_FAIL=$(grep -c . "$ERRLOG" 2>/dev/null || echo 0)

{
echo "# rev-puller-06 FINDINGS — chunk-06"
echo
echo "- Chunk: chunk-06 ($count articles attempted, ranks 256-295)"
echo "- Window: 2026-10-07T00:00:00Z down to 2020-01-01T00:00:00Z (rvdir=older, 500/page)"
echo "- Start UTC: $START_UTC"
echo "- End UTC: $END_UTC"
echo "- Wall time: $((WALL/3600))h $(((WALL%3600)/60))m $((WALL%60))s"
echo "- Articles succeeded: $N_OK"
echo "- Articles failed: $N_FAIL (see errors.log)"
echo "- Total revisions cached: $TOTAL_REV"
echo
echo "## Per-article revision counts (rank, title, revisions)"
echo
echo '```'
cat "$WORK/counts.tsv"
echo '```'
if [ "$N_FAIL" -gt 0 ]; then
echo
echo "## Failures"
echo
echo '```'
cat "$ERRLOG"
echo '```'
fi
} > "$WORK/FINDINGS.md"

log "CHUNK COMPLETE: $N_OK ok, $N_FAIL failed, $TOTAL_REV revisions, wall ${WALL}s"
