#!/usr/bin/env python3
"""METRONOME cadence profiler: inter-arrival distributions, burst shapes,
wall-clock boundary alignment (cron vs jittered agent), timezone inference.

Datasets:
  A) amap fleet raw/page_*.json  (reports[].date) — interactive agent baseline
  B) jmail_world.json (872 reports, graded script/cron) — scheduled-script baseline
"""
import json, glob, statistics, math
from collections import Counter
from datetime import datetime, timezone

RAW = "/home/hatch/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet"

def parse_ts(s):
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception:
        return None

def load_amap():
    pts = []
    for f in sorted(glob.glob(RAW + "/raw/page_*.json")):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        for r in d.get("reports", []):
            ts = parse_ts(r.get("date"))
            if ts:
                u = r.get("url", {})
                addr = u.get("addr", "") if isinstance(u, dict) else str(u)
                pts.append((ts, r.get("report_id", ""), addr))
    pts.sort()
    return pts

def load_jmail():
    d = json.load(open(RAW + "/new-fleets/raw/jmail_world.json"))
    pts = []
    for r in (d if isinstance(d, list) else d.get("reports", [])):
        ts = parse_ts(r.get("date"))
        if ts:
            pts.append((ts, r.get("report_id", ""), r.get("url", "")))
    pts.sort()
    return pts

def gaps(ts_list):
    tss = [p[0] for p in ts_list]
    return [(tss[i+1]-tss[i]).total_seconds() for i in range(len(tss)-1)]

def gap_stats(g):
    if len(g) < 2:
        return {"n": len(g)}
    return {
        "n": len(g),
        "median_s": round(statistics.median(g), 2),
        "mean_s": round(statistics.fmean(g), 2),
        "cv": round(statistics.pstdev(g)/statistics.fmean(g), 4) if statistics.fmean(g) > 0 else None,
        "min_s": round(min(g), 2),
        "max_s": round(max(g), 2),
        "p10_s": round(sorted(g)[int(0.1*len(g))], 2),
        "p90_s": round(sorted(g)[int(0.9*len(g))], 2),
    }

def boundary_alignment(pts):
    """Cron scripts fire on boundaries; agents jitter. Count hits at exact
    second==0, minute==0, and 'round' intervals."""
    n = len(pts)
    sec0 = sum(1 for p in pts if p[0].second == 0)
    min0 = sum(1 for p in pts if p[0].minute == 0 and p[0].second == 0)
    return {"n": n, "second_0_share": round(sec0/n, 4),
            "minute_0_share": round(min0/n, 4)}

def mode_gap(g, tol=3.0):
    """Dominant gap: histogram with tolerance; returns (mode_center, share, count)."""
    if not g:
        return None
    bins = Counter()
    for x in g:
        b = round(x / tol) * tol
        bins[b] += 1
    top, cnt = bins.most_common(1)[0]
    return {"mode_gap_s": top, "share": round(cnt/len(g), 4), "count": cnt}

def burst_shapes(pts, win_s=1800, min_n=10):
    """Sliding window bursts; for each, compute within-burst gap CV."""
    bursts = []
    tss = [p[0] for p in pts]
    j = 0
    for i0 in range(len(tss)):
        while j < len(tss) and (tss[j]-tss[i0]).total_seconds() <= win_s:
            j += 1
        n = j - i0
        if n >= min_n:
            bg = [(tss[k+1]-tss[k]).total_seconds() for k in range(i0, j-1)]
            cv = (statistics.pstdev(bg)/statistics.fmean(bg)) if len(bg) > 1 and statistics.fmean(bg) > 0 else None
            bursts.append({"start": tss[i0].isoformat(), "end": tss[j-1].isoformat(),
                           "count": n, "within_cv": round(cv, 4) if cv is not None else None})
    bursts.sort(key=lambda b: -b["count"])
    # dedupe overlapping
    ded = []
    for b in bursts:
        if not any(abs((datetime.fromisoformat(b["start"]) -
                        datetime.fromisoformat(d["start"])).total_seconds()) < win_s
                   for d in ded):
            ded.append(b)
    return ded

def tz_infer(pts):
    hours = Counter(p[0].hour for p in pts)
    n = len(pts)
    best_off, best_share = 0, 0.0
    for off in range(-12, 15):
        inside = sum(c for h, c in hours.items() if 8 <= (h+off) % 24 < 18)
        share = inside/n
        if share > best_share:
            best_share, best_off = share, off
    return {"offset_hours": best_off, "share_in_08_18_local": round(best_share, 3)}

def parallel_tags(pts, n_tags=3):
    """Minutes where >=n_tags distinct fleet tags (uq*) submitted — parallel agents."""
    import re
    by_min = {}
    for ts, rid, url in pts:
        m = ts.replace(second=0, microsecond=0).isoformat()
        tag = None
        mt = re.search(r"uq(?:scan|tag|research|pd|direct|ts|probe|fresh|hs|retry|mobile|cors|interactive|vnc|museum|vnc)=([^&/]+)", url)
        if mt:
            tag = mt.group(1)
        by_min.setdefault(m, set()).add(tag)
    return sum(1 for m, s in by_min.items() if len(s - {None}) >= n_tags)

def profile(name, pts):
    g = gaps(pts)
    res = {
        "name": name,
        "n_events": len(pts),
        "span": {"first": pts[0][0].isoformat(), "last": pts[-1][0].isoformat()} if pts else None,
        "gap_stats": gap_stats(g),
        "mode_gap": mode_gap(g),
        "boundary": boundary_alignment(pts),
        "tz": tz_infer(pts),
        "parallel_minutes_3tags": parallel_tags(pts, 3),
        "bursts": burst_shapes(pts)[:10],
    }
    # gap histogram (log-spaced)
    h = Counter()
    for x in g:
        if x <= 0: b = "0_or_neg"
        elif x < 10: b = "<10s"
        elif x < 60: b = "10-60s"
        elif x < 300: b = "1-5m"
        elif x < 1800: b = "5-30m"
        elif x < 10800: b = "0.5-3h"
        elif x < 86400: b = "3-24h"
        else: b = ">24h"
        h[b] += 1
    res["gap_histogram"] = dict(h)
    # day-of-week shape (UTC)
    dow = Counter(p[0].strftime("%a") for p in pts)
    res["dow_counts"] = dict(dow)
    return res

if __name__ == "__main__":
    out = []
    for name, loader in (("amap_fleet", load_amap), ("jmail_script_baseline", load_jmail)):
        pts = loader()
        r = profile(name, pts)
        out.append(r)
        print(f"== {name}: n={r['n_events']} ==")
        print("  gap_stats:", r["gap_stats"])
        print("  mode_gap:", r["mode_gap"])
        print("  boundary:", r["boundary"])
        print("  tz:", r["tz"])
        print("  gap_histogram:", r["gap_histogram"])
        print("  parallel_3tag_minutes:", r["parallel_minutes_3tags"])
        print("  dow:", r["dow_counts"])
        print("  top bursts:", [(b["start"][:16], b["count"], b["within_cv"]) for b in r["bursts"][:5]])
    json.dump(out, open(RAW + "/personas/metronome/raw/cadence_profile.json", "w"), indent=1)
    print("wrote cadence_profile.json")
