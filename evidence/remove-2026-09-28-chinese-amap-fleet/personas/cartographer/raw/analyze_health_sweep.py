#!/usr/bin/env python3
"""Analyze cartographer health-portals sweep: counts, date ranges, bursts,
exclusions, host clustering, and full URL listing."""
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

DIR = (
    Path.home()
    / "workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/cartographer/raw/health-portals-json"
)

EXCL_SUBSTRINGS = ["iowa.gov", "aihw.gov.au", "viz.aihw.gov.au", "uqscan=", "uqtag=", "uqvnc="]


def is_excluded(url):
    return any(s in url.lower() for s in EXCL_SUBSTRINGS)


def burst_report(reps):
    """Find clusters of >=3 reports within a 24h window."""
    dts = sorted(
        datetime.fromisoformat(r["date"].replace("Z", "+00:00"))
        for r in reps if r.get("date")
    )
    bursts = []
    for i, t in enumerate(dts):
        grp = [d for d in dts if timedelta(0) <= d - t <= timedelta(hours=24)]
        if len(grp) >= 3:
            bursts.append((t, len(grp)))
    # dedupe overlapping
    uniq = []
    for t, n in bursts:
        if not uniq or (t - uniq[-1][0]) > timedelta(hours=24):
            uniq.append((t, n))
    return uniq


for f in sorted(DIR.glob("*.json")):
    data = json.loads(f.read_text())
    reps = data["reports"]
    q = data["query"]
    print(f"\n{'='*100}\n{f.name}  query={q!r}  n={len(reps)}")
    if not reps:
        print("  (empty)")
        continue
    dates = sorted(r["date"] for r in reps if r.get("date"))
    print(f"  date range: {dates[0]} .. {dates[-1]}")
    excl = [r for r in reps if is_excluded(r["url"])]
    print(f"  excluded (known operator): {len(excl)}")
    for r in excl:
        print(f"    [EXCL] {r['date']} {r['report_id']} {r['url'][:120]}")
    keep = [r for r in reps if not is_excluded(r["url"])]
    hosts = Counter(urlparse(r["url"]).netloc for r in keep)
    print(f"  top hosts (non-excluded): {hosts.most_common(8)}")
    bursts = burst_report(keep)
    for t, n in bursts:
        print(f"  BURST: {n} reports within 24h starting {t}")
    for r in keep:
        print(f"    {r['date']} {r['report_id']} {r['url'][:160]}")
