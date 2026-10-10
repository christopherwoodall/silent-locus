#!/usr/bin/env python3
"""v3 burst detection for wikipedia-lane burst-analysis.
- Fixes: bgwiki localized namespace (Потребител:), per-window-size baselines.
- Drops the ordinal-run approach (pool/seq is a time-bucketed pool, not creation order).
- Caches parsed per-wiki events to events.npz for reuse.
Output: bursts.json (time bursts only), PROVENANCE.txt
"""
import json, glob, re, os, time
from datetime import datetime, timezone
from collections import defaultdict
import numpy as np

t_start = time.time()
RAW = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/raw")
OUT = os.path.expanduser("~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/burst-analysis/raw")
os.makedirs(OUT, exist_ok=True)

NAME_RE = re.compile(r"(~2026-\d+-\d+)$")
WIKI_RE = re.compile(r"\.(bgwiki|commonswiki|incubatorwiki|mediawikiwiki|simplewiki|test2wiki|testwiki|enwiki|metawiki)(\.resume)?\.jsonl$")

def parse_ts(s):
    return datetime.fromisoformat(s.replace("Z","+00:00")).timestamp()

per_wiki = defaultdict(list)
seen_log = set()
n_lines = 0
for path in sorted(glob.glob(RAW + "/newusers-2026-*.jsonl")):
    wiki = WIKI_RE.search(path).group(1)
    with open(path) as f:
        for line in f:
            n_lines += 1
            if '~2026-' not in line: continue
            try: e = json.loads(line)
            except Exception: continue
            key = (wiki, e.get("logid"))
            if key in seen_log: continue
            seen_log.add(key)
            m = NAME_RE.search(e.get("title",""))
            if not m: continue
            per_wiki[wiki].append((parse_ts(e["timestamp"]), m.group(1)))
print(f"parsed {n_lines} lines -> {len(seen_log)} temp events in {time.time()-t_start:.1f}s", flush=True)

npz = {}
for wiki, evts in per_wiki.items():
    evts.sort()
    npz[wiki+"_t"] = np.array([t for t,_ in evts])
    npz[wiki+"_n"] = np.array([n for _,n in evts])
np.savez_compressed(OUT+"/events.npz", **npz)
print("cached events.npz", flush=True)

def iso(ts): return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat().replace("+00:00","Z")

bursts=[]
for wiki in sorted(per_wiki.keys()):
    T_w = npz[wiki+"_t"]; N_w = npz[wiki+"_n"]; n = len(T_w)
    bins = ((T_w - T_w[0])//600).astype(int)
    bc = np.bincount(bins)
    mean10 = float(bc.mean()) if len(bc) else 0.0
    for winsz, minn, label in [(600,4,"10m"),(3600,12,"1h"),(86400,40,"1d")]:
        baseline = mean10 * (winsz/600)
        thr = max(minn, 8*max(baseline,1.0))
        right = np.searchsorted(T_w, T_w + winsz)
        cnt = right - np.arange(n)
        cand = np.nonzero(cnt >= thr)[0].tolist()
        j=0
        while j < len(cand):
            i = cand[j]
            k = int(np.searchsorted(T_w, T_w[i]+winsz, side='left'))
            bursts.append({"wiki":wiki,"win":label,"t0":float(T_w[i]),"t1":float(T_w[k-1]),
                           "count":k-i,"names":N_w[i:k].tolist(),
                           "mean10":mean10,"threshold":round(thr,1)})
            while j < len(cand) and cand[j] < k: j+=1
    print(f"{wiki}: n={n} mean10={mean10:.2f}", flush=True)

# merge across window sizes: prefer smallest window; drop a larger window fully
# containing an already-kept smaller burst on the same wiki
order = {"10m":0,"1h":1,"1d":2}
bursts.sort(key=lambda b:(b["wiki"],b["t0"],order[b["win"]]))
kept=[]
for b in bursts:
    if any(k["wiki"]==b["wiki"] and k["t0"]<=b["t0"] and k["t1"]>=b["t1"] and order[k["win"]]<=order[b["win"]] for k in kept):
        continue
    kept.append(b)
for b in kept:
    b["t0_iso"]=iso(b["t0"]); b["t1_iso"]=iso(b["t1"])

out={"generated_utc":datetime.now(timezone.utc).isoformat(),
     "method":"sliding windows 10m/1h/1d; threshold=max(min_n, 8*med10*winsz/600); min_n=4/12/40; greedy non-overlap; cross-size merge prefers smallest",
     "bursts":kept}
with open(OUT+"/bursts.json","w") as f: json.dump(out,f)
print(f"BURSTS={len(kept)}", flush=True)
for b in kept:
    print(f"{b['win']:4s} {b['wiki']:14s} {b['t0_iso']}..{b['t1_iso']} n={b['count']:5d} thr={b['threshold']}", flush=True)
with open(OUT+"/PROVENANCE.txt","w") as f:
    f.write("Source: wikipedia-lane/raw/newusers-2026-*.jsonl (25 files incl. metawiki June resume; logid-deduped per wiki)\n")
    f.write(f"Generated: {out['generated_utc']} by detect_bursts.py (v3)\n")
    f.write(f"Input lines: {n_lines}; deduped ~2026-* events: {len(seen_log)}\n")
    f.write("Temp name structure: ~2026-<POOL>-<SEQ>; POOL in [10002,99998] rises with time (global time-bucketed pool, ~70 accts/pool); bgwiki uses localized ns 'Потребител:'.\n")
    f.write("NOTE: v2 ordinal-run approach RETRACTED — (POOL,SEQ) order is not monotonic in creation time; runs were spurious.\n")
print("done in %.1fs" % (time.time()-t_start), flush=True)
