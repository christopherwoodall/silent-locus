#!/usr/bin/env python3
"""Fetch FULL HN thread via public item API (passive GET).
Usage: hn-thread.py <item-id> [...]  -> raw/hn/thread-<id>.json + .PROVENANCE.txt + .sha256
Thread JSON keeps verbatim API bytes (handles inside raw JSON are data, not prose).
"""
import json, os, sys, time, urllib.request, datetime, hashlib
RAW = os.path.expanduser("~/workspace/silent-locus/data/lanes/agent-bypass-forum-hunt/raw/hn")
def get(iid):
    url=f"https://hacker-news.firebaseio.com/v0/item/{iid}.json"
    req=urllib.request.Request(url, headers={"User-Agent":"hn-bypass-lane/1.0 passive-read"})
    with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read().decode())
def walk(iid, seen, out):
    if iid in seen: return
    seen.add(iid)
    try: item=get(iid)
    except Exception as e: print(f"ERR {iid}: {e}"); return
    out.append(item)
    for kid in (item or {}).get("kids") or []:
        time.sleep(0.05); walk(kid, seen, out)
for iid in sys.argv[1:]:
    seen=set(); out=[]
    walk(int(iid), seen, out)
    path=os.path.join(RAW, f"thread-{iid}.json")
    rec={"item_id":int(iid),"retrieved_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "method":"GET https://hacker-news.firebaseio.com/v0/item/<id>.json recursive kids",
         "item_count":len(out),"items":out}
    data=json.dumps(rec,indent=1).encode()
    open(path,"wb").write(data)
    open(path+".sha256","w").write(hashlib.sha256(data).hexdigest()+"  thread-%s.json\n"%iid)
    open(path+".PROVENANCE.txt","w").write(
        f"Source URL: https://hacker-news.firebaseio.com/v0/item/{iid}.json (recursive kids)\n"
        f"Retrieved: {rec['retrieved_at']}\nMethod: passive GET, no login, no key\n"
        f"Items: {len(out)}\n")
    print(f"{iid}: {len(out)} items -> thread-{iid}.json")
