#!/usr/bin/env python3
"""Lane 1: full libraries.io census of campaign gem names. ~1.1s pace, read-only, no key needed.
Writes to workspace (persistent) — /tmp gets wiped."""
import json, time, urllib.request, urllib.parse, os

OUT = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.makedirs(OUT, exist_ok=True)
names = set()
for i in (1, 2, 3, 4):
    p = os.path.join(_REPO, "data", f"gem-pins-batch{i}.txt")
    for line in open(p):
        line = line.strip()
        if line and not line.startswith("#"):
            names.add(line.split("==")[0])
names = sorted(names)
print(f"{len(names)} unique names", flush=True)

def get(url):
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "gemstuff-hunt/1.0 (research)"})
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"  429 -> backoff 60s (attempt {attempt+1})", flush=True)
                time.sleep(60)
                last = e
                continue
            raise
        except Exception as e:
            last = e
            time.sleep(1)
    raise last

out_path = f"{OUT}/census.jsonl"
seen = set()
if os.path.exists(out_path):
    for line in open(out_path):
        try:
            seen.add(json.loads(line)["name"])
        except Exception:
            pass
print(f"resuming: {len(seen)} already done", flush=True)

fout = open(out_path, "a")
n_new = 0
for n in names:
    if n in seen:
        continue
    try:
        d = get(f"https://libraries.io/api/rubygems/{urllib.parse.quote(n, safe='')}")
        rec = {"name": n, "found": True,
               "description": d.get("description"),
               "homepage": d.get("homepage"),
               "latest_release_number": d.get("latest_release_number"),
               "latest_release_published_at": d.get("latest_release_published_at"),
               "versions": [(v.get("number"), v.get("published_at")) for v in (d.get("versions") or [])],
               "package_manager_url": d.get("package_manager_url")}
    except Exception as e:
        rec = {"name": n, "found": False, "error": str(e)[:120]}
    fout.write(json.dumps(rec) + "\n")
    fout.flush()
    n_new += 1
    if n_new % 25 == 0:
        print(f"...{n_new} new ({n})", flush=True)
    time.sleep(1)
fout.close()
print(f"done, {n_new} new queries", flush=True)
