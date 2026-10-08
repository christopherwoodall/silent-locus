#!/bin/bash
# REVISION-PULLER-11: pull revision history for chunk-11 (ranks 459-500)
# HTTP via curl only. Pace: >=5s between requests to en.wikipedia.org.
# Do NOT run requests via python3 (egress proxy breaks python HTTP stacks).
set -u

WORKTREE="$HOME/workspace/silent-locus-top500"
BASE="$WORKTREE/data/2026-10-06-wikipedia-top500-infra-scan/raw"
CHUNK="$BASE/chunks/chunk-11"
REVDIR="$BASE/revisions"
WDIR="$WORKTREE/workers/rev-puller-11"
UA="silent-locus-top500-scan/1.0 (research)"
MANIFEST="$WDIR/completed-ranks.txt"
COUNTS="$WDIR/article-counts.tsv"
ERRORS="$WDIR/errors.log"
TMPPAGE="$(mktemp /tmp/revpull11.XXXXXX.json)"

mkdir -p "$REVDIR" "$WDIR"
touch "$MANIFEST" "$COUNTS" "$ERRORS"

START_TS=$(date -u +%s)
echo "rev-puller-11 started $(date -u +%FT%TZ)" | tee -a "$WDIR/run.log"

while IFS=$'\t' read -r rank title; do
    [ -z "$rank" ] && continue

    # Resume: skip ranks already marked complete
    if grep -qx "$rank" "$MANIFEST" 2>/dev/null; then
        echo "rank $rank already complete, skipping" | tee -a "$WDIR/run.log"
        continue
    fi

    OUTFILE="$REVDIR/${rank}.jsonl"
    : > "$OUTFILE"
    REVCNT=0
    CONTINUE=""
    ATTEMPT=0
    ART_FAIL=""

    while :; do
        ENCTITLE=$(python3 -c 'import sys,urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$title")
        URL="https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=${ENCTITLE}&rvprop=user%7Ctimestamp%7Cids%7Ccomment%7Ctags%7Csize&rvlimit=500&rvdir=older&rvstart=2026-10-07T00%3A00%3A00Z&rvend=2020-01-01T00%3A00%3A00Z&format=json&formatversion=2"
        if [ -n "$CONTINUE" ]; then
            ENCCONT=$(python3 -c 'import sys,urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$CONTINUE")
            URL="${URL}&rvcontinue=${ENCCONT}"
        fi

        HTTP=$(curl -sS --max-time 60 -A "$UA" -w '%{http_code}' -o "$TMPPAGE" "$URL" 2>>"$ERRORS")
        RC=$?

        if [ $RC -ne 0 ] || [ "$HTTP" != "200" ] || ! python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$TMPPAGE" 2>/dev/null; then
            ATTEMPT=$((ATTEMPT+1))
            if [ $ATTEMPT -gt 3 ]; then
                ART_FAIL="HTTP rc=$RC code=$HTTP after 4 attempts"
                echo "$(date -u +%FT%TZ) rank=$rank title=$title ERROR: $ART_FAIL" | tee -a "$ERRORS"
                break
            fi
            sleep 30
            continue
        fi
        ATTEMPT=0

        # Extract revisions -> JSONL; print rvcontinue token (empty when done)
        NEXT=$(python3 - "$TMPPAGE" "$OUTFILE" "$rank" "$title" <<'PY'
import json, sys
page_path, out_path, rank, title = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
with open(page_path) as f:
    data = json.load(f)
pages = data.get("query", {}).get("pages", [])
# API-level error surfaces here, not as missing pages
if "error" in data:
    print("APIERROR:" + json.dumps(data["error"])[:200], file=sys.stderr)
    print("__FAIL__")
    sys.exit(0)
n = 0
with open(out_path, "a", encoding="utf-8") as out:
    for p in pages:
        if p.get("missing"):
            continue
        for r in p.get("revisions", []):
            rec = {
                "rank": rank,
                "article": title,
                "revid": r.get("revid"),
                "parentid": r.get("parentid"),
                "user": r.get("user"),   # None if userhidden
                "timestamp": r.get("timestamp"),
                "comment": r.get("comment"),
                "tags": r.get("tags", []),
                "size": r.get("size"),
            }
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
# record count for the caller
with open(page_path + ".count", "w") as f:
    f.write(str(n))
cont = data.get("continue", {}).get("rvcontinue", "")
print(cont if cont else "__DONE__")
PY
)
        BATCH=$(cat "$TMPPAGE.count" 2>/dev/null || echo 0)
        rm -f "$TMPPAGE.count"
        if [ "$NEXT" = "__FAIL__" ]; then
            ART_FAIL="API returned error payload"
            echo "$(date -u +%FT%TZ) rank=$rank title=$title ERROR: $ART_FAIL" | tee -a "$ERRORS"
            break
        fi
        REVCNT=$((REVCNT + BATCH))
        sleep 5
        if [ "$NEXT" = "__DONE__" ]; then
            break
        fi
        CONTINUE="$NEXT"
    done

    if [ -n "$ART_FAIL" ]; then
        printf '%s\t%s\t%d\tFAILED: %s\n' "$rank" "$title" "$REVCNT" "$ART_FAIL" >> "$COUNTS"
    else
        printf '%s\t%s\t%d\n' "$rank" "$title" "$REVCNT" >> "$COUNTS"
        echo "$rank" >> "$MANIFEST"
    fi
    echo "$(date -u +%FT%TZ) rank=$rank '$title' -> $REVCNT revisions ${ART_FAIL:+($ART_FAIL)}" | tee -a "$WDIR/run.log"
done < "$CHUNK"

rm -f "$TMPPAGE"
END_TS=$(date -u +%s)
WALL=$((END_TS - START_TS))

TOTAL=$(python3 -c "
import sys
tot, fails, n = 0, 0, 0
for line in open('$COUNTS'):
    p = line.rstrip('\n').split('\t')
    if len(p) >= 3:
        n += 1; tot += int(p[2])
        if len(p) > 3: fails += 1
print(f'{tot} {fails} {n}')
")
set -- $TOTAL

{
echo "# REVISION-PULLER-11 findings — chunk-11 (ranks 459–500)"
echo ""
echo "- Run: $(date -u +%FT%TZ)"
echo "- Wall time: ${WALL}s ($((WALL/3600))h $(((WALL%3600)/60))m $((WALL%60))s)"
echo "- Articles attempted: $3"
echo "- Total revisions cached: $1"
echo "- Failed articles: $2"
echo ""
echo "## Per-article revision counts (rank, title, revisions)"
echo ""
echo "| rank | article | revisions |"
echo "|------|---------|-----------|"
awk -F'\t' '{ printf "| %s | %s | %s |\n", $1, $2, $3 }' "$COUNTS"
echo ""
echo "## Failures"
echo ""
if [ "$2" -eq 0 ]; then
  echo "None."
else
  grep FAILED "$COUNTS" || true
fi
echo ""
echo "## Notes"
echo ""
echo "- Endpoint: en.wikipedia.org/w/api.php prop=revisions, rvlimit=500, rvdir=older,"
echo "  rvstart=2026-10-07T00:00:00Z, rvend=2020-01-01T00:00:00Z, formatversion=2."
echo "- Requested fields: user, timestamp, ids, comment, tags, size."
echo "- Cache: raw/revisions/<rank>.jsonl, one JSON object per line."
echo "- Pacing: >=5s between requests (curl, User-Agent silent-locus-top500-scan/1.0)."
echo "- Retry policy: 3 retries at 30s on transport/HTTP/JSON failure."
} > "$WDIR/FINDINGS.md"

echo "rev-puller-11 finished: $1 revisions, $2 failures, wall ${WALL}s" | tee -a "$WDIR/run.log"
