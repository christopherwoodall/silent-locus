#!/usr/bin/env python3
"""Creation-burst clustering on newusers autocreate JSONL.
Usage: burst_cluster.py <jsonl>
Threshold: fixed 10-min bins; flag bins with count >= max(5, mean+5*sd) of temp creations.
Lists every burst: window, n, account names. Merges adjacent flagged bins.
"""
import json, sys, math, re
from datetime import datetime, timedelta
from collections import defaultdict

path = sys.argv[1]
BIN = timedelta(minutes=10)
TEMP_RE = re.compile(r'~\d{4}-\d+-\d+')

evs = []
seen = set()
skipped_hidden = 0
with open(path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        e = json.loads(line)
        if e['logid'] in seen:
            continue
        seen.add(e['logid'])
        title = e.get('title')
        if not title:
            skipped_hidden += 1
            continue
        m = TEMP_RE.search(title)
        if not m:
            continue
        evs.append((e['timestamp'], m.group(0), e['logid']))
evs.sort()
print(f"# events={len(evs)} temp creations in {path} (skipped {skipped_hidden} suppressed-title events)", file=sys.stderr)
if not evs:
    sys.exit(0)

t0 = datetime.fromisoformat(evs[0][0].replace('Z', '+00:00'))
t1 = datetime.fromisoformat(evs[-1][0].replace('Z', '+00:00'))
nbins = int((t1 - t0) / BIN) + 2
bins = [0] * nbins
bin_members = defaultdict(list)
for ts, name, lid in evs:
    dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
    b = int((dt - t0) / BIN)
    bins[b] += 1
    bin_members[b].append((ts, name))

mean = sum(bins) / len(bins)
var = sum((x - mean) ** 2 for x in bins) / len(bins)
sd = math.sqrt(var)
thresh = max(5, mean + 5 * sd)
print(f"# bins={len(bins)} mean={mean:.3f} sd={sd:.3f} threshold>={thresh:.2f}", file=sys.stderr)

flagged = sorted(b for b, c in enumerate(bins) if c >= thresh)
bursts = []
for b in flagged:
    if bursts and b == bursts[-1][-1] + 1:
        bursts[-1].append(b)
    else:
        bursts.append([b])
for blist in bursts:
    members = []
    for b in blist:
        members.extend(bin_members[b])
    members.sort()
    start = (t0 + blist[0] * BIN).strftime('%Y-%m-%dT%H:%M:%SZ')
    end = (t0 + (blist[-1] + 1) * BIN).strftime('%Y-%m-%dT%H:%M:%SZ')
    print(f"BURST {start} -> {end} n={len(members)}")
    for ts, n in members:
        print(f"  {ts} {n}")
