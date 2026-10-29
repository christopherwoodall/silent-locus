#!/usr/bin/env python3
"""HN Algolia sweep for agent-bypass lane. Passive GET only.
Saves verbatim Algolia JSON per query+tag+month to raw dir.
Usage: python3 hn-sweep.py [probe|fetch]
probe prints nbHits per query (no raw save except probe log).
fetch saves all pages per month slice.
"""
import json, os, sys, time, urllib.request, urllib.parse, datetime

RAW = os.path.expanduser("~/workspace/silent-locus/data/lanes/agent-bypass-forum-hunt/raw/hn")
os.makedirs(RAW, exist_ok=True)

# months Nov 2025 .. Oct 2026 (end exclusive)
MONTHS = []
for y, m in [(2025,11),(2025,12)]+[(2026,mm) for mm in range(1,11)]:
    start = int(datetime.datetime(y,m,1,tzinfo=datetime.timezone.utc).timestamp())
    if m==12: end = int(datetime.datetime(y+1,1,1,tzinfo=datetime.timezone.utc).timestamp())
    else: end = int(datetime.datetime(y,m+1,1,tzinfo=datetime.timezone.utc).timestamp())
    MONTHS.append((f"{y:04d}-{m:02d}", start, end))

QUERIES = [
    "guardrail bypass",
    "agent jailbreak",
    "jailbreak agent",
    "agent ignored instructions",
    "agent disobeyed",
    "agent self-preservation",
    "self-preservation agent",
    "agent lied to user",
    "agent lying",
    "agent deceived",
    "agent edited its own constraints",
    "agent modified its system prompt",
    "agent rewrote its instructions",
    "sandbox escape agent",
    "agent escaped sandbox",
    "sandbox bypass agent",
    "agent bypassed approval",
    "agent circumvented",
    "agent bypassed guardrail",
    "agent guardrail",
    "agent bypass",
    "agent refused to stop",
    "agent ignored guardrail",
    "agent disabled its guardrail",
    "agent edited its own",
    "agent changed its own instructions",
    "agent evaded monitoring",
    "agent hid from monitor",
    "agent lied to monitor",
    "agent self-preservation",
]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent":"hn-bypass-lane/1.0 passive-read"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def probe():
    out=[]
    for q in QUERIES:
        for tag in ("story","comment"):
            params = {"query":q,"tags":tag,"hitsPerPage":1,
                      "numericFilters":f"created_at_i>1761955200,created_at_i<1790784000"}
            url = "https://hn.algolia.com/api/v1/search_by_date?"+urllib.parse.urlencode(params)
            try:
                d=get(url); nb=d.get("nbHits",-1)
            except Exception as e:
                nb=f"ERR {e}"
            print(f"{q!r} [{tag}] nbHits={nb}", flush=True)
            out.append({"query":q,"tag":tag,"nbHits":nb})
    with open(os.path.join(RAW,"probe.json"),"w") as f: json.dump(out,f,indent=1)
    return out

def fetch_range(q, tag, label, start, end):
    """Fetch one range; returns (nbHits, hits, filename-or-None)."""
    params={"query":q,"tags":tag,"hitsPerPage":100,
            "numericFilters":f"created_at_i>{start},created_at_i<{end}"}
    url="https://hn.algolia.com/api/v1/search_by_date?"+urllib.parse.urlencode(params)
    try: d0=get(url)
    except Exception as e:
        print(f"ERR {q} {tag} {label}: {e}", flush=True); return (None,[],None)
    nb=d0.get("nbHits",0); npages=d0.get("nbPages",0)
    if nb==0: return (0,[],None)
    slug="".join(c if c.isalnum() else "_" for c in q)[:60]
    fname=f"{slug}__{tag}__{label}.json"
    allhits=list(d0.get("hits",[]))
    for p in range(1, min(npages,10)):
        params["page"]=p
        url="https://hn.algolia.com/api/v1/search_by_date?"+urllib.parse.urlencode(params)
        try: d=get(url); allhits.extend(d.get("hits",[]))
        except Exception as e:
            print(f"  page {p} ERR {e}", flush=True); break
        time.sleep(0.2)
    rec={"query":q,"tag":tag,"range":label,"nbHits":nb,"fetched":len(allhits),
         "retrieved_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "method":"GET https://hn.algolia.com/api/v1/search_by_date","hits":allhits}
    with open(os.path.join(RAW,fname),"w") as f: json.dump(rec,f,indent=1)
    return (nb,allhits,fname)

def fetch():
    total=0; files=0
    seen=set()
    for q in QUERIES:
        for tag in ("story","comment"):
            if (q,tag) in seen: continue
            seen.add((q,tag))
            nb,hits,fname = fetch_range(q,tag,"2025-11_to_2026-10",1761955200,1790784000)
            if nb is None or nb==0: continue
            if nb<=1000:
                print(f"{q!r} [{tag}] whole nbHits={nb} fetched={len(hits)}", flush=True)
                files+=1; total+=len(hits); continue
            # over cap: monthly split
            print(f"{q!r} [{tag}] whole nbHits={nb} OVER CAP -> monthly", flush=True)
            for mlabel,start,end in MONTHS:
                nb2,h2,f2 = fetch_range(q,tag,mlabel,start,end)
                if f2: files+=1; total+=len(h2)
                print(f"  {mlabel} nbHits={nb2}", flush=True)
    print(f"TOTAL files={files} hits={total}")
    return
    if False:
        for _unused in []:
            for mlabel,start,end in MONTHS:
                # first page to learn nbHits
                params={"query":q,"tags":tag,"hitsPerPage":100,
                        "numericFilters":f"created_at_i>{start},created_at_i<{end}"}
                url="https://hn.algolia.com/api/v1/search_by_date?"+urllib.parse.urlencode(params)
                try: d0=get(url)
                except Exception as e:
                    print(f"ERR {q} {tag} {mlabel}: {e}", flush=True); continue
                nb=d0.get("nbHits",0); npages=d0.get("nbPages",0)
                if nb==0: continue
                print(f"{q!r} [{tag}] {mlabel} nbHits={nb} pages={npages}", flush=True)
                slug="".join(c if c.isalnum() else "_" for c in q)[:60]
                fname=f"{slug}__{tag}__{mlabel}.json"
                allhits=list(d0.get("hits",[]))
                # Algolia caps accessible hits at 1000; monthly slices should stay below
                for p in range(1, min(npages,10)):
                    params["page"]=p
                    url="https://hn.algolia.com/api/v1/search_by_date?"+urllib.parse.urlencode(params)
                    try: d=get(url); allhits.extend(d.get("hits",[]))
                    except Exception as e:
                        print(f"  page {p} ERR {e}", flush=True); break
                    time.sleep(0.2)
                rec={"query":q,"tag":tag,"month":mlabel,"nbHits":nb,"fetched":len(allhits),
                     "retrieved_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
                     "method":"GET https://hn.algolia.com/api/v1/search_by_date","hits":allhits}
                with open(os.path.join(RAW,fname),"w") as f: json.dump(rec,f,indent=1)
                files+=1; total+=len(allhits)
    print(f"TOTAL files={files} hits={total}")

if __name__=="__main__":
    mode=sys.argv[1] if len(sys.argv)>1 else "probe"
    probe() if mode=="probe" else fetch()
