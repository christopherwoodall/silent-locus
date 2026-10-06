#!/bin/bash
# One-off re-pull of rank 42 (Alexander Zverev): resume pass cached only the
# newest 1000 of 2883 revisions (tail batches lost to a storage write failure).
set -u
BASE="$HOME/workspace/silent-locus-top500"
SCAN="$BASE/data/2026-10-06-wikipedia-top500-infra-scan/raw"
OUTDIR="$SCAN/revisions"
WORKER="$BASE/workers/rev-puller-00"
UA="silent-locus-top500-scan/1.0 (research)"
API="https://en.wikipedia.org/w/api.php"
RESP=/tmp/rv00r42_resp.json
rank=42; title="Alexander Zverev"
enc=$(python3 -c 'import sys,urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$title")
outfile="$OUTDIR/${rank}.jsonl"
: > "$outfile"
cont=""; count=0; failed=0; first=1
echo "$(date -u +%FT%TZ) REPULL42 START rank=$rank title=$title" >> "$WORKER/progress.log"
while :; do
  if [ "$first" -eq 0 ]; then sleep 5; fi
  first=0
  url="${API}?action=query&prop=revisions&titles=${enc}&rvprop=user|timestamp|ids|comment|tags|size&rvlimit=500&rvdir=older&rvstart=2026-10-07T00:00:00Z&rvend=2020-01-01T00:00:00Z&format=json&formatversion=2"
  [ -n "$cont" ] && url="${url}&rvcontinue=${cont}"
  code=""; attempt=0
  while [ "$attempt" -lt 3 ]; do
    attempt=$((attempt+1))
    code=$(curl -sS --max-time 60 -A "$UA" -w "%{http_code}" -o "$RESP" "$url" 2>>"$WORKER/errors.log") || code="000"
    [ "$code" = "200" ] && break
    echo "$(date -u +%FT%TZ) REPULL42 HTTP $code attempt=$attempt rank=$rank" >> "$WORKER/errors.log"
    sleep $((15*attempt))
  done
  if [ "$code" != "200" ]; then
    echo "$(date -u +%FT%TZ) REPULL42 FAILED rank=$rank after 3 attempts (last http=$code)" >> "$WORKER/errors.log"
    failed=1; break
  fi
  res=$(RANK="$rank" TITLE="$title" OUTF="$outfile" python3 - <<'EOF'
import json,os,urllib.parse,sys
rank=int(os.environ["RANK"]); title=os.environ["TITLE"]; outf=os.environ["OUTF"]
d=json.load(open("/tmp/rv00r42_resp.json"))
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
    echo "$(date -u +%FT%TZ) REPULL42 API/status=$status rank=$rank" >> "$WORKER/errors.log"
    failed=1; break
  fi
  n=$(printf '%s' "$res" | cut -f2)
  cont=$(printf '%s' "$res" | cut -f3)
  count=$((count+n))
  if [ -z "$cont" ]; then break; fi
done
# verify on-disk line count matches before recording
disk=$(wc -l < "$outfile")
if [ "$failed" -eq 0 ] && [ "$disk" -eq "$count" ]; then
  python3 - "$WORKER/per-article.txt" "$rank" "$title" "$count" <<'EOF'
import sys
p,rank,title,count=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
lines=open(p,encoding="utf-8").read().splitlines()
out=[l for l in lines if not l.startswith(rank+"\t")]
out.append("%s\t%s\t%s"%(rank,title,count))
out.sort(key=lambda l:int(l.split("\t")[0]))
open(p,"w",encoding="utf-8").write("\n".join(out)+"\n")
EOF
  echo "$(date -u +%FT%TZ) REPULL42 DONE rank=$rank revs=$count disk=$disk" >> "$WORKER/progress.log"
  echo "REPULL42 DONE rank=$rank revs=$count disk=$disk"
else
  echo "$(date -u +%FT%TZ) REPULL42 MISMATCH rank=$rank counted=$count disk=$disk failed=$failed" >> "$WORKER/errors.log"
  echo "REPULL42 MISMATCH counted=$count disk=$disk failed=$failed"
fi
