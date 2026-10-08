#!/usr/bin/env python3
"""Lane 1 pattern battery: combinatorial try[a-z][0-9]zz check + JFrog-only names.
Reads queue from QUEUE env file, writes to OUT jsonl. Sharded, resume-safe."""
import json, time, urllib.request, urllib.parse, urllib.error, os, re, html, sys
from http.client import IncompleteRead

OUT = os.path.dirname(os.path.abspath(__file__))
queue_file = os.environ["QUEUE"]
out_name = os.environ["OUT"]
shard = int(os.environ.get("SHARD", "0"))
shards = int(os.environ.get("SHARDS", "1"))
names = [l.strip() for l in open(f"{OUT}/{queue_file}") if l.strip()]
names = [n for i, n in enumerate(names) if i % shards == shard]
print(f"{len(names)} queued (shard {shard}/{shards})", flush=True)

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
og_re = re.compile(r'<meta property="og:description" content="(.*?)"\s*/?>', re.S)

def fetch(name):
    url = f"https://libraries.io/rubygems/{urllib.parse.quote(name, safe='')}"
    last = None
    for _ in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status, r.read().decode("utf-8", "replace"), False
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return 404, "", False
            last = e; time.sleep(3)
        except IncompleteRead as e:
            return 200, e.partial.decode("utf-8", "replace"), True
        except Exception as e:
            last = e; time.sleep(3)
    raise last

out_path = f"{OUT}/{out_name}"
seen = set()
if os.path.exists(out_path):
    for line in open(out_path):
        try: seen.add(json.loads(line)["name"])
        except Exception: pass
print(f"resuming: {len(seen)} done", flush=True)
fout = open(out_path, "a")
n_new = 0
for n in names:
    if n in seen: continue
    try:
        status, body, partial = fetch(n)
        if status == 404:
            rec = {"name": n, "found": False}
        else:
            m = og_re.search(body)
            desc = html.unescape(m.group(1)) if m else None
            rec = {"name": n, "found": True, "description": desc,
                   "go_import": bool(desc and "go-import" in desc),
                   "partial": partial, "url": f"https://libraries.io/rubygems/{n}"}
    except Exception as e:
        rec = {"name": n, "found": None, "error": str(e)[:120]}
    fout.write(json.dumps(rec) + "\n"); fout.flush()
    n_new += 1
    if n_new % 50 == 0: print(f"...{n_new}", flush=True)
    time.sleep(1)
fout.close()
print(f"done, {n_new} new", flush=True)
