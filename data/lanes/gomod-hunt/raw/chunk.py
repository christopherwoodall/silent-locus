import json, re, time, urllib.request, sys

PATS = [
    re.compile(r'\d{10}'),
    re.compile(r'try[a-z][0-9]zz'),
    re.compile(r'(^|/)zz'),
    re.compile(r'oai', re.I),
    re.compile(r'(probe|proxy|fetch|yard|jina|go-?import|moderngov|lambeth|wandsworth|southwark|county\.json|builder\.alive)', re.I),
]

chunk = int(sys.argv[1]); start = sys.argv[2]; end = sys.argv[3]
import os
WD = os.path.dirname(os.path.abspath(__file__))  # was /home/hatch/workspace/tmp-gomod; relocated 2026-09-28

def fetch(since):
    url = f"https://index.golang.org/index?since={since}"
    req = urllib.request.Request(url, headers={"User-Agent": "gomod-hunt-research/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return [json.loads(l) for l in r.read().decode().splitlines() if l.strip()]

since = start; total = 0; matches = 0; pages = 0; seen = set()
out = open(f"{WD}/matches_{chunk}.jsonl", "a")
while True:
    try:
        rows = fetch(since)
    except Exception as e:
        time.sleep(5)
        continue
    pages += 1
    if not rows:
        break
    for row in rows:
        total += 1
        path = row.get("Path", "")
        key = (path, row.get("Version"))
        if key in seen:
            continue
        seen.add(key)
        if any(p.search(path) for p in PATS):
            out.write(json.dumps(row) + "\n"); matches += 1
    since = rows[-1]["Timestamp"]
    if pages % 25 == 0:
        open(f"{WD}/progress_{chunk}.txt","w").write(f"pages={pages} total={total} matches={matches} since={since}")
    if since >= end:
        break
    time.sleep(1.0)
out.close()
open(f"{WD}/progress_{chunk}.txt","w").write(f"DONE pages={pages} total={total} matches={matches} end={since}")
print(f"chunk {chunk} DONE pages={pages} total={total} matches={matches}", flush=True)
