#!/bin/bash
# Fetch FULL HN thread via curl (firebase item API, passive GET, recursive kids).
# Usage: hn-thread-curl.sh <id> [...]
RAW="$HOME/workspace/silent-locus/data/lanes/agent-bypass-forum-hunt/raw/hn"
mkdir -p "$RAW"
for root in "$@"; do
  tmpdir=$(mktemp -d)
  # BFS over kids using curl; store each item json
  echo "$root" > "$tmpdir/queue.txt"
  declare -A seen=()
  while read -r iid; do
    [ -z "$iid" ] && continue
    [ -n "${seen[$iid]}" ] && continue
    seen[$iid]=1
    curl -s --max-time 60 "https://hacker-news.firebaseio.com/v0/item/$iid.json" -o "$tmpdir/$iid.json" || true
    # extract kids
    python3 - "$tmpdir/$iid.json" "$tmpdir/queue.txt" <<'PY' 2>/dev/null || true
import json,sys
try:
    d=json.load(open(sys.argv[1]))
    if d and d.get("kids"):
        with open(sys.argv[2],"a") as f:
            for k in d["kids"]: f.write(str(k)+"\n")
except Exception: pass
PY
  done < <(cat "$tmpdir/queue.txt"; while read -r _; do :; done) 2>/dev/null
  # The loop above cannot grow queue dynamically; use iterative expansion instead:
  # (fallback: python driver below does the real work)
  rm -rf "$tmpdir"
  python3 - "$root" <<'PY'
import json, os, subprocess, sys, datetime, hashlib
root=sys.argv[1]
raw=os.path.expanduser("~/workspace/silent-locus/data/lanes/agent-bypass-forum-hunt/raw/hn")
def get(iid):
    r=subprocess.run(["curl","-s","--max-time","60",f"https://hacker-news.firebaseio.com/v0/item/{iid}.json"],capture_output=True,text=True)
    try: return json.loads(r.stdout) if r.stdout.strip() else None
    except Exception: return None
seen=set(); out=[]; stack=[int(root)]
while stack:
    iid=stack.pop()
    if iid in seen: continue
    seen.add(iid)
    it=get(iid); out.append(it)
    if it and it.get("kids"): stack.extend(it["kids"])
rec={"item_id":int(root),"retrieved_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
     "method":"GET https://hacker-news.firebaseio.com/v0/item/<id>.json recursive kids via curl",
     "item_count":len(out),"items":out}
data=json.dumps(rec,indent=1).encode()
path=os.path.join(raw,f"thread-{root}.json")
open(path,"wb").write(data)
open(path+".sha256","w").write(hashlib.sha256(data).hexdigest()+f"  thread-{root}.json\n")
open(path+".PROVENANCE.txt","w").write(f"Source URL: https://hacker-news.firebaseio.com/v0/item/{root}.json (recursive kids)\nRetrieved: {rec['retrieved_at']}\nMethod: passive GET via curl, no login, no key\nItems: {len(out)}\n")
print(f"{root}: {len(out)} items -> thread-{root}.json")
PY
done
