#!/usr/bin/env python3
"""Timing exclusion baseline for the known uq operator (Chinese Amap fleet).
Reads events.jsonl read-only. Emits JSON profile + prints markdown tables.
Output written ONLY to this persona dir.
"""
import json, re, sys, math
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from statistics import mean, stdev

DATA = "/home/hatch/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/events.jsonl"
OUTD = "/home/hatch/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/metronome"

def classify(note, matched, domain):
    """Task-family classification: domain first, then uq grammar on amap surfaces."""
    d = (domain or "").lower()
    hay = (note or "") + " " + (matched or "")
    if d == "httpbun.com":
        return "httpbun-staging"
    if d == "httpbin.org":
        return "httpbin-staging"
    if d == "livecodes.io":
        return "livecodes-staging"
    if d == "href.li":
        return "hrefli-relay"
    if d == "baidu.com":
        return "baidu-transpage"
    if d == "webhook.site":
        return "webhook-deaddrop"
    if d in ("amap.com", "gaode.com"):
        if re.search(r"[?&]uqscan=", hay):
            return "amap-uqscan"
        m = re.search(r"[?&](uq[a-z0-9]*)", hay)
        if m:
            return "amap-otheruq:" + m.group(1)
        return "amap-plain"
    return "other"

def classify_target(note, labels):
    d = (labels.get("submitted_domain") or "").lower()
    if "amap" in d: return "amap"
    if "lhr" in d or "lhr.life" in (note or ""): return "lhr.life"
    if "webhook" in d: return "webhook.site"
    if "httpbun" in d: return "httpbun"
    return d or "unknown"

records = []
with open(DATA) as f:
    for line in f:
        r = json.loads(line)
        ts = datetime.fromisoformat(r["@timestamp"].replace("Z", "+00:00"))
        labels = r.get("labels", {}) or {}
        note = r.get("note", "")
        matched = r.get("matched_string", "")
        records.append({
            "ts": ts,
            "note": note,
            "matched": matched,
            "family": classify(note, matched, labels.get("submitted_domain")),
            "domain": labels.get("submitted_domain"),
            "target": classify_target(note, labels),
            "report_id": labels.get("report_id"),
        })
records.sort(key=lambda r: r["ts"])
n = len(records)
print(f"records: {n}, span: {records[0]['ts']} .. {records[-1]['ts']}", file=sys.stderr)

profile = {"n": n, "start": records[0]["ts"].isoformat(), "end": records[-1]["ts"].isoformat()}

# 1. hour-of-day curves (UTC and Beijing UTC+8)
hod_utc = Counter(); hod_bj = Counter()
for r in records:
    hod_utc[r["ts"].hour] += 1
    hod_bj[(r["ts"] + timedelta(hours=8)).hour] += 1
profile["hour_utc"] = [hod_utc.get(h, 0) for h in range(24)]
profile["hour_beijing"] = [hod_bj.get(h, 0) for h in range(24)]

# 7. day of week (UTC / Beijing)
dow_utc = Counter(); dow_bj = Counter()
for r in records:
    dow_utc[r["ts"].strftime("%a")] += 1
    dow_bj[(r["ts"] + timedelta(hours=8)).strftime("%a")] += 1
order = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
profile["dow_utc"] = {d: dow_utc.get(d, 0) for d in order}
profile["dow_beijing"] = {d: dow_bj.get(d, 0) for d in order}

# 2. inter-arrival gaps
gaps = []
for a, b in zip(records, records[1:]):
    g = (b["ts"] - a["ts"]).total_seconds()
    gaps.append(max(g, 0))
profile["gap_stats"] = {
    "min_s": min(gaps), "max_s": max(gaps),
    "median_s": sorted(gaps)[len(gaps)//2], "mean_s": mean(gaps),
    "p10_s": sorted(gaps)[int(len(gaps)*0.10)],
    "p25_s": sorted(gaps)[int(len(gaps)*0.25)],
    "p75_s": sorted(gaps)[int(len(gaps)*0.75)],
    "p90_s": sorted(gaps)[int(len(gaps)*0.90)],
    "p99_s": sorted(gaps)[int(len(gaps)*0.99)],
}
bins = [("<=5s",0,5),("5-15s",5,15),("15-60s",15,60),("1-5min",60,300),
        ("5-30min",300,1800),("30min-2h",1800,7200),("2-12h",7200,43200),(">12h",43200,1e12)]
profile["gap_histogram"] = {b: sum(1 for g in gaps if lo < g <= hi) for b, lo, hi in bins}
# cadence modes: coarse log-histogram peaks
logbins = defaultdict(int)
for g in gaps:
    if g <= 0: logbins["0s"] += 1
    else: logbins[f"10^{math.floor(math.log10(max(g,1))):d}"] += 1
profile["gap_log_modes"] = dict(sorted(logbins.items()))

# 3. metronomic runs: sliding windows, CV<0.3 over >=10 consecutive submissions
runs = []
i = 0
W = 12  # window of submissions (11 gaps)
while i + W - 1 < n:
    win = records[i:i+W]
    wg = [(win[k+1]["ts"]-win[k]["ts"]).total_seconds() for k in range(W-1)]
    m = mean(wg)
    sd = stdev(wg) if len(set(wg)) > 1 else 0.0
    cv = (sd/m) if m > 0 else 0.0
    if m > 0 and cv < 0.3:
        j = i + W
        # extend while local CV stays low
        while j < n:
            win2 = records[j-11:j+1]
            wg2 = [(win2[k+1]["ts"]-win2[k]["ts"]).total_seconds() for k in range(11)]
            m2 = mean(wg2); sd2 = stdev(wg2) if len(set(wg2)) > 1 else 0.0
            if m2 > 0 and (sd2/m2) < 0.35:
                j += 1
            else:
                break
        runs.append((i, j))
        i = j
    else:
        i += 1
run_list = []
for s, e in runs:
    seq = records[s:e]
    gg = [(seq[k+1]["ts"]-seq[k]["ts"]).total_seconds() for k in range(len(seq)-1)]
    fams = Counter(x["family"] for x in seq)
    dom = Counter(x["target"] for x in seq)
    run_list.append({
        "start": seq[0]["ts"].isoformat(), "end": seq[-1]["ts"].isoformat(),
        "count": len(seq), "mean_gap_s": round(mean(gg), 1),
        "cv": round(stdev(gg)/mean(gg), 3) if mean(gg) else 0,
        "min_gap_s": round(min(gg),1), "max_gap_s": round(max(gg),1),
        "families": dict(fams.most_common(3)), "targets": dict(dom.most_common(3)),
    })
profile["metronome_runs"] = run_list

# 4. burst clusters: sliding 1h windows, dedupe by 30min step, top 15
t0 = records[0]["ts"]; t1 = records[-1]["ts"]
bursts = []
t = t0
while t < t1:
    w = [r for r in records if t <= r["ts"] < t + timedelta(hours=1)]
    if len(w) > 20:
        fams = Counter(x["family"] for x in w)
        bursts.append({"window_start": t.isoformat(), "count": len(w),
                       "families": dict(fams.most_common(3))})
    t += timedelta(minutes=30)
# dedupe overlapping: keep max count per non-overlapping hour
bursts.sort(key=lambda b: -b["count"])
kept = []
for b in bursts:
    bs = datetime.fromisoformat(b["window_start"])
    if all(abs((bs - datetime.fromisoformat(k["window_start"])).total_seconds()) >= 3600 for k in kept):
        kept.append(b)
profile["burst_clusters_top15"] = kept[:15]

# 5. parallel execution: same-minute distinct targets
minute_groups = defaultdict(set)
for r in records:
    key = r["ts"].strftime("%Y-%m-%dT%H:%M")
    minute_groups[key].add(r["target"])
multi = {k: v for k, v in minute_groups.items() if len(v) > 1}
profile["parallel"] = {
    "minutes_with_gt1_target": len(multi),
    "max_distinct_targets_one_minute": max((len(v) for v in multi.values()), default=0),
    "example_minutes": [(k, sorted(v)) for k, v in sorted(multi.items())[:5]],
}
# distribution of per-minute distinct-target counts
pdist = Counter(len(v) for v in minute_groups.values())
profile["parallel"]["per_minute_distinct_targets_dist"] = dict(sorted(pdist.items()))

# 6. per-family timing profiles
fams = defaultdict(list)
for r in records:
    fams[r["family"]].append(r)
fam_prof = {}
fam_collapsed = defaultdict(list)
for fam, rs in fams.items():
    key = fam.split(":")[0]
    fam_collapsed[key].extend(rs)
fams = fam_collapsed
for fam, rs in sorted(fams.items()):
    rs.sort(key=lambda r: r["ts"])
    fg = [(rs[k+1]["ts"]-rs[k]["ts"]).total_seconds() for k in range(len(rs)-1)]
    hh = Counter(x["ts"].hour for x in rs)
    fam_prof[fam] = {
        "count": len(rs),
        "span": [rs[0]["ts"].isoformat(), rs[-1]["ts"].isoformat()],
        "median_gap_s": sorted(fg)[len(fg)//2] if fg else None,
        "mean_gap_s": round(mean(fg),1) if fg else None,
        "min_gap_s": min(fg) if fg else None,
        "max_gap_s": max(fg) if fg else None,
        "peak_hours_utc": [h for h, _ in hh.most_common(3)],
        "hour_dist_utc": [hh.get(h, 0) for h in range(24)],
    }
profile["family_profiles"] = fam_prof

with open(f"{OUTD}/baseline_profile.json", "w") as f:
    json.dump(profile, f, indent=1)
print(f"wrote {OUTD}/baseline_profile.json", file=sys.stderr)
print(json.dumps(profile, indent=1))
