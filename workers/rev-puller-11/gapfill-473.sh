#!/bin/bash
# One-off gap fill: rank 473 'George VI' (left partial when the worker died).
# Writes to /tmp first, then moves atomically into revisions/473.jsonl.
# No race: the replacement script's RANKS list excludes 473.
set -u
WORKTREE="$HOME/workspace/silent-locus-top500"
REVD="$WORKTREE/data/2026-10-06-wikipedia-top500-infra-scan/raw/revisions"
WDIR="$WORKTREE/workers/rev-puller-11"
UA="silent-locus-top500-scan/1.0 (research)"
RANK=473
TITLE="George VI"
TMPOUT="/tmp/473-final.jsonl"
TMPPAGE="$(mktemp /tmp/rv473.XXXXXX.json)"

: > "$TMPOUT"
ENC=$(python3 -c 'import sys,urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$TITLE")
CONT=""
TOTAL=0
ATTEMPT=0
while :; do
  URL="https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=${ENC}&rvprop=user%7Ctimestamp%7Cids%7Ccomment%7Ctags%7Csize&rvlimit=500&rvdir=older&rvstart=2026-10-07T00%3A00%3A00Z&rvend=2020-01-01T00%3A00%3A00Z&format=json&formatversion=2"
  if [ -n "$CONT" ]; then
    EC=$(python3 -c 'import sys,urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$CONT")
    URL="${URL}&rvcontinue=${EC}"
  fi
  HTTP=$(curl -sS --max-time 60 -A "$UA" -w '%{http_code}' -o "$TMPPAGE" "$URL" 2>/dev/null)
  RC=$?
  if [ $RC -ne 0 ] || [ "$HTTP" != "200" ] || ! python3 -c 'import json,sys; json.load(open(sys.argv[1]))' "$TMPPAGE" 2>/dev/null; then
    ATTEMPT=$((ATTEMPT+1))
    if [ $ATTEMPT -gt 3 ]; then
      echo "$(date -u +%FT%TZ) rank=$RANK GAPFILL_FAIL transport" | tee -a "$WDIR/errors.log"
      exit 1
    fi
    sleep 30; continue
  fi
  ATTEMPT=0
  NEXT=$(python3 - "$TMPPAGE" "$TMPOUT" "$RANK" "$TITLE" <<'PY'
import json, sys
pp, outp, rank, title = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
d = json.load(open(pp))
if "error" in d:
    print("__FAIL__"); sys.exit(0)
n = 0
with open(outp, "a", encoding="utf-8") as out:
    for p in d.get("query", {}).get("pages", []):
        for r in p.get("revisions", []):
            out.write(json.dumps({"rank": rank, "article": title, "revid": r.get("revid"),
                "parentid": r.get("parentid"), "user": r.get("user"),
                "timestamp": r.get("timestamp"), "comment": r.get("comment"),
                "tags": r.get("tags", []), "size": r.get("size")},
                ensure_ascii=False) + "\n")
            n += 1
open(pp + ".count", "w").write(str(n))
c = d.get("continue", {}).get("rvcontinue", "")
print(c if c else "__DONE__")
PY
)
  BATCH=$(cat "$TMPPAGE.count" 2>/dev/null || echo 0); rm -f "$TMPPAGE.count"
  if [ "$NEXT" = "__FAIL__" ]; then
    echo "$(date -u +%FT%TZ) rank=$RANK GAPFILL_FAIL api-error" | tee -a "$WDIR/errors.log"
    exit 1
  fi
  TOTAL=$((TOTAL + BATCH))
  sleep 5
  [ "$NEXT" = "__DONE__" ] && break
  CONT="$NEXT"
done
rm -f "$TMPPAGE"
mv "$TMPOUT" "$REVD/$RANK.jsonl"
echo "$(date -u +%FT%TZ) rank=$RANK 'George VI' GAPFILL complete -> $TOTAL revisions" | tee -a "$WDIR/run.log"
printf '473\tGeorge VI\t%d\tgapfill\n' "$TOTAL" >> "$WDIR/article-counts.tsv"
