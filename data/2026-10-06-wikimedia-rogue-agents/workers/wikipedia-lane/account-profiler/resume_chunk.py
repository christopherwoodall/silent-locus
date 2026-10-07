#!/usr/bin/env python3
"""Resume ONE partial newusers chunk: continues newest-first paging from a given
lestart timestamp and appends to the wiki's JSONL, then marks the chunk done.
Usage: resume_chunk.py <short> <host> <YYYY-MM> <lestart> <leend> [pace_s]
curl only (VM Python HTTP stacks break on the egress proxy), paced >=5s.
Duplicates against the existing file tail are expected and harmless (dedupe by logid at analysis).
"""
import json, subprocess, sys, time, urllib.parse

short, host, ym, lestart, leend = sys.argv[1:6]
pace = float(sys.argv[6]) if len(sys.argv) > 6 else 5.0
RAW = "/home/hatch/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/raw"
OUT = f"{RAW}/newusers-2026-04-01_2026-09-30.{short}.jsonl"
STATE = f"{RAW}/.newusers-pull-state"

def fetch(cont):
    q = [
        ("action", "query"), ("list", "logevents"), ("letype", "newusers"),
        ("leaction", "newusers/autocreate"), ("lestart", lestart), ("leend", leend),
        ("leprop", "ids|timestamp|title|type"), ("lelimit", "500"), ("format", "json"),
    ]
    if cont:
        q.append(("lecontinue", cont))
    url = f"https://{host}/w/api.php?" + urllib.parse.urlencode(q)
    r = subprocess.run(["curl", "-s", "--max-time", "60", url], capture_output=True, text=True)
    return r.stdout

cont = None
total = 0
page = 0
with open(OUT, "a") as out:
    while True:
        time.sleep(pace)
        page += 1
        resp = fetch(cont)
        try:
            d = json.loads(resp)
            evs = d["query"]["logevents"]
        except Exception:
            print(f"  !! non-JSON {short} {ym} p{page}, retry once", flush=True)
            time.sleep(30)
            resp = fetch(cont)
            try:
                d = json.loads(resp)
                evs = d["query"]["logevents"]
            except Exception:
                print(f"  !! parse failed twice {short} {ym} p{page}, ABORT (chunk left unmarked)", flush=True)
                sys.exit(1)
        for e in evs:
            out.write(json.dumps(e, separators=(",", ":")) + "\n")
        total += len(evs)
        cont = d.get("continue", {}).get("lecontinue")
        if page % 20 == 0:
            print(f"  {short} {ym}: p{page} +{total} events, oldest={evs[-1]['timestamp'] if evs else '?'}", flush=True)
        if not cont:
            break
        if page >= 20000:
            print(f"  !! page cap {short} {ym}, ABORT", flush=True)
            sys.exit(1)

with open(STATE, "a") as st:
    st.write(f"{short}:{ym}\n")
print(f"resume done {short} {ym}: +{total} events ({page} pages)", flush=True)
