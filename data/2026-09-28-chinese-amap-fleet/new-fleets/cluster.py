#!/usr/bin/env python3
"""Burst/cluster detection over htmx-collected urlquery windows.
Metadata-first: timestamps, burst timing, param grammars, domain clusters."""
import json, sys, re
from collections import defaultdict, Counter
from urllib.parse import urlparse, parse_qs

fp = sys.argv[1]
reps = json.load(open(fp))
print(f"total reports: {len(reps)}")

# dedupe by report_id
seen = {}
for r in reps:
    seen[r['report_id']] = r
reps = list(seen.values())
print(f"unique: {len(reps)}")

KNOWN = re.compile(r'uqscan=|uqtag=|uqvnc=|uqresearch=|uqhs=|uqretry=|uqinteractive=|uqmuseum=|uqpd=|uqdirect=|uqts=|uqprobe=|uqfresh=|uqmobile=|sub_poi_navi|amap\.com|ditu\.amap|idph|iowa\.gov|aihw|lhr\.life|is\.gd/3JlIp7|mf075827|sum074114|kf073634')

def host(u):
    try: return urlparse(u if '://' in u else 'http://'+u).netloc.lower()
    except: return '?'

# --- 1. per-minute burst detection ---
permin = Counter(r['date'][:16] for r in reps if r.get('date'))
print("\n== hottest minutes ==")
for m, n in permin.most_common(15):
    print(f"  {m}  {n}")

# --- 2. host clusters in recent window ---
hosts = Counter(host(r['url']) for r in reps)
print("\n== top hosts ==")
for h, n in hosts.most_common(25):
    print(f"  {n:4d}  {h}")

# --- 3. param-grammar scan: nonce-like / tag-like params ---
pgram = Counter()
epochy = []
for r in reps:
    u = r['url']
    if '?' not in u: continue
    q = u.split('?',1)[1]
    for kv in q.split('&')[:8]:
        k = kv.split('=')[0][:40]
        v = kv.split('=',1)[1] if '=' in kv else ''
        if re.fullmatch(r'\d{10}(\d{3})?', v): epochy.append((r['date'][:16], u[:90]))
        if re.fullmatch(r'[a-zA-Z]{1,4}\d{6,}', v) or re.fullmatch(r'\d{13,}', v):
            pgram[k]+=1
print("\n== nonce-like param keys ==")
for k, n in pgram.most_common(20): print(f"  {n:4d}  {k}=")
print(f"\n== epoch-like values: {len(epochy)} ==")
for t, u in epochy[:20]: print(f"  {t}  {u}")

# --- 4. non-known-operator bursts: minutes with >=3 reports, none matching KNOWN ---
print("\n== candidate NEW-fleet minutes (>=3 reports, no known-operator markers) ==")
for m, n in permin.most_common(40):
    if n < 3: continue
    batch = [r for r in reps if r.get('date','')[:16]==m]
    if any(KNOWN.search(r['url']) for r in batch): continue
    hs = Counter(host(r['url']) for r in batch)
    print(f"  {m}  n={n}  hosts={dict(hs.most_common(5))}")
    for r in batch[:6]:
        print(f"      {r['report_id'][:8]}  {r['url'][:95]}")
