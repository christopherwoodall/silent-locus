#!/usr/bin/env python3
"""Aggregate the 2026-10-01 oai-tag-sweep lane into per-indicator summaries.

Reads evidence/2026-10-01-oai-tag-sweep/events.jsonl (96,353 annotated events),
re-derives per-indicator prevalence per source, date ranges, and 3 exemplar
evidence snippets per indicator (verbatim from the sweep's evidence sidecar).
Cross-checks totals against sweep_summary.json. Writes agg.json.
"""
import json, os
from collections import Counter, defaultdict

LANE = os.path.expanduser("~/workspace/silent-locus/evidence/2026-10-01-oai-tag-sweep")
SRC = os.path.join(LANE, "events.jsonl")
OUT = "/tmp/oai_agg/agg.json"

per_source = defaultdict(Counter)      # indicator -> source -> count
total = Counter()
first = {}
last = {}
exemplars = defaultdict(list)          # indicator -> list of (indicator_count, source, record_id, event_time, snippet)
n = 0
ge2 = 0

for line in open(SRC):
    e = json.loads(line)
    n += 1
    src = e["source"]
    t = e.get("event_time") or ""
    if e["indicator_count"] >= 2:
        ge2 += 1
    for ind in e["indicators"]:
        total[ind] += 1
        per_source[ind][src] += 1
        if ind not in first or (t and t < first[ind]):
            first[ind] = t
        if ind not in last or (t and t > last[ind]):
            last[ind] = t
        if len(exemplars[ind]) < 3:
            snip = (e.get("evidence") or {}).get(ind, "")
            exemplars[ind].append({
                "indicator_count": e["indicator_count"],
                "source": src,
                "record_id": e["record_id"],
                "event_time": t,
                "snippet": snip,
            })

# cross-check against sweep_summary.json
summ = json.load(open(os.path.join(LANE, "sweep_summary.json")))
mismatches = []
for src, counts in summ["hits_per_indicator_per_source"].items():
    key = "frozen:" + src
    for ind, c in counts.items():
        if per_source[ind].get(key, 0) != c:
            mismatches.append((ind, key, c, per_source[ind].get(key, 0)))
# transluce-dataset key
for ind, c in summ.get("transluce_dataset_hits_per_indicator", {}).items():
    if per_source[ind].get("transluce-dataset", 0) != c:
        mismatches.append((ind, "transluce-dataset", c, per_source[ind].get("transluce-dataset", 0)))

assert n == summ["total_annotated_events"] == 96353, (n, summ["total_annotated_events"])
assert ge2 == summ["events_ge2_indicators"], (ge2, summ["events_ge2_indicators"])
assert not mismatches, mismatches

# prefer exemplars from high indicator_count events, distinct snippets/sources
cands = defaultdict(list)
for ind in exemplars:
    pass
exemplars = defaultdict(list)
for line in open(SRC):
    e = json.loads(line)
    for ind in e["indicators"]:
        snip = (e.get("evidence") or {}).get(ind, "")
        if not snip:
            continue
        cands[ind].append((e["indicator_count"], e["source"], e["record_id"],
                           e.get("event_time") or "", snip))
for ind, cl in cands.items():
    cl.sort(key=lambda x: -x[0])
    seen_snip = set()
    picked = []
    for ic, src, rid, t, snip in cl:
        if snip in seen_snip:
            continue
        seen_snip.add(snip)
        picked.append({"indicator_count": ic, "source": src,
                       "record_id": rid, "event_time": t, "snippet": snip})
        if len(picked) == 6:
            break
    # maximize source diversity, keep top indicator_count order within source
    by_src = defaultdict(list)
    for p in picked:
        by_src[p["source"]].append(p)
    final = []
    while len(final) < 3 and by_src:
        for src in sorted(by_src):
            if by_src[src]:
                final.append(by_src[src].pop(0))
                if len(final) == 3:
                    break
        by_src = {k: v for k, v in by_src.items() if v}
    exemplars[ind] = final

agg = {
    "total_events": n,
    "events_ge2_indicators": ge2,
    "frozen_totals_scanned": summ["frozen_totals_scanned"],
    "overlap_days_ge2_sources": summ["overlap_days_ge2_sources"],
    "indicators": {
        ind: {
            "total_hits": total[ind],
            "per_source": dict(per_source[ind]),
            "first_seen": first[ind],
            "last_seen": last[ind],
            "exemplars": exemplars[ind],
        }
        for ind in sorted(total)
    },
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(agg, open(OUT, "w"), indent=1)
print("indicators:", len(agg["indicators"]))
for ind, d in agg["indicators"].items():
    print(f"{ind:24s} {d['total_hits']:6d}  first={d['first_seen'][:10] if d['first_seen'] else '?'} last={d['last_seen'][:10] if d['last_seen'] else '?'}")
print("cross-check vs sweep_summary.json: PASS (totals, per-indicator-per-source, ge2)")
