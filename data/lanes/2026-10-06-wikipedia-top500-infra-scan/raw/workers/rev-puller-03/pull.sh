#!/usr/bin/env bash
# REVISION-PULLER-03: pull full revision history for chunk-03 articles.
# HTTP via curl ONLY (python3 used solely for URL-encoding + JSON parsing).
# Pace: <=1 request per 5 seconds to en.wikipedia.org.
# UA: silent-locus-top500-scan/1.0 (research)

set -u
BASE="$HOME/workspace/silent-locus-top500/data/2026-10-06-wikipedia-top500-infra-scan/raw"
CHUNK="${1:-$BASE/chunks/chunk-03}"
OUTDIR="$BASE/revisions"
WORKER="$BASE/workers/rev-puller-03"
ERRLOG="$WORKER/errors.log"
UA="silent-locus-top500-scan/1.0 (research)"
START_TS=$(date +%s)
[ -s "$WORKER/walltime_start.txt" ] || echo "$START_TS" > "$WORKER/walltime_start.txt"

enc() { python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$1"; }

# Parse one API response into JSONL lines on stdout, print rvcontinue token on
# fd3 (or the literal string NONE if exhausted). Exit code nonzero on API error.
parse_page() {
  local infile="$1" rank="$2" title="$3"
  python3 - "$infile" "$rank" "$title" <<'PY'
import json,sys
infile, rank, title = sys.argv[1], int(sys.argv[2]), sys.argv[3]
data = json.load(open(infile))
if "error" in data:
    print("API_ERROR: %s" % data["error"].get("info","unknown"), file=sys.stderr)
    sys.exit(2)
pages = data.get("query", {}).get("pages", [])
if not pages:
    print("NO_PAGES", file=sys.stderr); sys.exit(3)
pg = pages[0]
if "missing" in pg:
    print("MISSING_PAGE: %s" % title, file=sys.stderr); sys.exit(4)
for r in pg.get("revisions", []):
    rec = {"rank": rank, "article": title,
           "revid": r.get("revid"), "parentid": r.get("parentid"),
           "user": r.get("user"), "temp": bool(r.get("temp", False)),
           "timestamp": r.get("timestamp"),
           "comment": r.get("comment"), "tags": r.get("tags", []),
           "size": r.get("size")}
    print(json.dumps(rec, ensure_ascii=False))
tok = data.get("continue", {}).get("rvcontinue")
# rvcontinue token goes to fd3 via stderr-prefix trick; instead print with marker:
print("__RVCONTINUE__:" + (tok if tok else "NONE"))
PY
}

if [ "${2:-resume}" = "fresh" ]; then
  : > "$WORKER/counts.tsv"
  : > "$ERRLOG"
fi
touch "$WORKER/counts.tsv" "$ERRLOG"

while IFS=$'\t' read -r rank title; do
  [ -z "$rank" ] && continue
  echo "[$rank] $title"
  outfile="$OUTDIR/${rank}.jsonl"
  : > "$outfile"
  rvcontinue=""
  pages=0
  retries=0
  done_this=0
  while :; do
    enc_title=$(enc "$title")
    url="https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=${enc_title}&rvprop=user%7Ctimestamp%7Cids%7Ccomment%7Ctags%7Csize&rvlimit=500&rvdir=older&rvstart=2026-10-07T00%3A00%3A00Z&rvend=2020-01-01T00%3A00%3A00Z&format=json&formatversion=2"
    [ -n "$rvcontinue" ] && url="$url&rvcontinue=$(enc "$rvcontinue")"
    resp=$(curl -sS -A "$UA" --retry 0 --max-time 60 "$url" 2>>"$ERRLOG") || {
      retries=$((retries+1))
      if [ $retries -ge 3 ]; then
        echo "[$(date -u +%FT%TZ)] rank=$rank title=$title FAILED after 3 curl errors" >> "$ERRLOG"
        break
      fi
      sleep 10; continue
    }
    echo "$resp" > /tmp/rp03_page.json
    parsed=$(parse_page /tmp/rp03_page.json "$rank" "$title" 2>/tmp/rp03_err.txt); pc=$?
    if [ $pc -ne 0 ]; then
      err=$(cat /tmp/rp03_err.txt)
      echo "[$(date -u +%FT%TZ)] rank=$rank title=$title $err" >> "$ERRLOG"
      case "$pc" in 2|3) retries=$((retries+1)); [ $retries -lt 3 ] && { sleep 10; continue; } ;;
                     4) break ;;   # missing page: permanent, move on
                     *) retries=$((retries+1)); [ $retries -lt 3 ] && { sleep 10; continue; } ;;
      esac
      break
    fi
    retries=0
    tok=$(echo "$parsed" | grep '^__RVCONTINUE__:' | cut -d: -f2-)
    echo "$parsed" | grep -v '^__RVCONTINUE__:' >> "$outfile"
    pages=$((pages+1))
    if [ "$tok" = "NONE" ]; then
      done_this=1
      break
    fi
    rvcontinue="$tok"
    sleep 5
  done
  count=$(wc -l < "$outfile")
  printf '%s\t%s\t%s\t%s\n' "$rank" "$title" "$pages" "$count" >> "$WORKER/counts.tsv"
  echo "[$rank] $title -> $count revisions ($pages pages)"
  # pause between articles to keep <=1 req/5s across article boundary
  sleep 5
done < "$CHUNK"

END_TS=$(date +%s)
FIRST_TS=$(cat "$WORKER/walltime_start.txt")
echo "$FIRST_TS $END_TS" > "$WORKER/walltime.txt"
echo "DONE. wall_total=$((END_TS-FIRST_TS))s"
