#!/usr/bin/env python3
"""Shape pass 2: (a) mediawiki 1h burst (n=33) uids+contribs; (b) interloper 18396951 lookup;
(c) cross-wiki contribs for testwiki-burst and mediawiki-burst accounts. Paced >=5s."""
import json, os, time, urllib.parse, subprocess

OUT = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/burst-analysis/raw")
DOM = {
    "commonswiki": "commons.wikimedia.org", "mediawikiwiki": "www.mediawiki.org",
    "testwiki": "test.wikipedia.org", "incubatorwiki": "incubator.wikimedia.org",
    "metawiki": "meta.wikimedia.org", "enwiki": "en.wikipedia.org",
    "simplewiki": "simple.wikipedia.org", "test2wiki": "test2.wikipedia.org",
}
UA = "burst-analysis-worker/1.0 (wikimedia rogue-agent hunt research)"
NREQ = [0]
def api(wiki, params):
    params = dict(params); params.update({"action":"query","format":"json","formatversion":"2"})
    url = "https://" + DOM[wiki] + "/w/api.php?" + urllib.parse.urlencode(params, doseq=True)
    out = subprocess.run(["curl","-sS","--max-time","60","-A",UA,url], capture_output=True, text=True)
    NREQ[0]+=1
    if out.returncode != 0: raise RuntimeError(f"curl failed: {out.stderr[:200]}")
    time.sleep(5)
    return json.loads(out.stdout)

def get_users(wiki, names):
    users=[]
    for i in range(0,len(names),50):
        r=api(wiki,{"list":"users","ususers":"|".join(names[i:i+50])})
        users.extend(r["query"]["users"])
    return users

def get_contribs(wiki, names):
    items=[]
    for i in range(0,len(names),50):
        chunk=names[i:i+50]
        r=api(wiki,{"list":"usercontribs","ucuser":"|".join(chunk),"uclimit":"max",
                    "ucprop":"ids|title|timestamp|comment|sizediff|tags"})
        items.extend(r["query"]["usercontribs"])
        while "continue" in r:
            r=api(wiki,{"list":"usercontribs","ucuser":"|".join(chunk),"uclimit":"max",
                        "ucprop":"ids|title|timestamp|comment|sizediff|tags", **r["continue"]})
            items.extend(r["query"]["usercontribs"])
    return items

bursts=json.load(open(OUT+"/bursts.json"))["bursts"]
mw1h=[b for b in bursts if b["wiki"]=="mediawikiwiki" and b["win"]=="1h" and b["t0_iso"].startswith("2026-05-21")][0]
print("mediawiki 1h burst:",mw1h["t0_iso"],"n=",len(mw1h["names"]),flush=True)

# (a) uids + contribs for the 33
users=get_users("mediawikiwiki", mw1h["names"])
json.dump(users, open(OUT+"/uids-mediawikiwiki_2026-05-21_1h.json","w"))
ids=sorted((u["userid"],u["name"]) for u in users if "userid" in u)
print("uid range:",ids[0][0],"..",ids[-1][0],"span=",ids[-1][0]-ids[0][0],"n=",len(ids),flush=True)
gaps=[b for a,b in zip(ids,ids[1:]) if b[0]-a[0]>1]
print("gaps:",[(a[0],b[0]) for a,b in zip(ids,ids[1:]) if b[0]-a[0]>1],flush=True)
contribs=get_contribs("mediawikiwiki", mw1h["names"])
json.dump(contribs, open(OUT+"/contribs-burst-mediawikiwiki_2026-05-21_1h.json","w"))
print("mediawiki 1h contribs:",len(contribs),"by",len(set(c["user"] for c in contribs)),flush=True)

# (b) interloper 18396951 on mediawikiwiki
r=api("mediawikiwiki",{"list":"logevents","letype":"newusers",
    "lestart":"2026-05-21T01:14:30Z","leend":"2026-05-21T01:12:30Z",
    "lelimit":"max","leprop":"ids|title|timestamp"})
ev=r["query"]["logevents"]
json.dump(ev, open(OUT+"/logevents-mediawikiwiki_2026-05-21-interloper.json","w"))
print("logevents around interloper:",[(e["timestamp"],e["title"]) for e in ev],flush=True)

# (c) cross-wiki contribs
tw=[b for b in bursts if b["wiki"]=="testwiki"][0]
sets={"testwiki-burst":tw["names"], "mediawikiwiki-burst":mw1h["names"]}
xwiki={w for w in DOM if w not in ("testwiki","mediawikiwiki")}
xres={}
for sname,names in sets.items():
    for w in sorted(xwiki):
        try:
            items=get_contribs(w, names)
        except Exception as ex:
            print(sname,w,"FAILED",ex,flush=True); continue
        if items:
            xres.setdefault(sname,{})[w]=items
            print(f"{sname} on {w}: {len(items)} edits by {sorted(set(c['user'] for c in items))}",flush=True)
json.dump(xres, open(OUT+"/crosswiki-contribs.json","w"))
print("total API requests:",NREQ[0],flush=True)
