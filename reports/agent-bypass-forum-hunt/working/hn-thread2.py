#!/usr/bin/env python3
"""Fetch FULL HN thread via curl (firebase item API, passive GET, recursive kids)."""
import json, os, subprocess, sys, datetime, hashlib
RAW = os.path.expanduser("~/workspace/silent-locus/data/lanes/agent-bypass-forum-hunt/raw/hn")
def get(iid):
    r = subprocess.run(["curl","-s","--max-time","60",f"https://hacker-news.firebaseio.com/v0/item/{iid}.json"],
                       capture_output=True, text=True)
    try: return json.loads(r.stdout) if r.stdout.strip() else None
    except Exception: return None
for root in sys.argv[1:]:
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
    path=os.path.join(RAW,f"thread-{root}.json")
    open(path,"wb").write(data)
    open(path+".sha256","w").write(hashlib.sha256(data).hexdigest()+f"  thread-{root}.json\n")
    open(path+".PROVENANCE.txt","w").write(
        f"Source URL: https://hacker-news.firebaseio.com/v0/item/{root}.json (recursive kids)\n"
        f"Retrieved: {rec['retrieved_at']}\nMethod: passive GET via curl, no login, no key\nItems: {len(out)}\n")
    print(f"{root}: {len(out)} items -> thread-{root}.json", flush=True)
