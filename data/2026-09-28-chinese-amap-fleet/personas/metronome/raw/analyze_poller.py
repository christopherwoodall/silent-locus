#!/usr/bin/env python3
"""POLLER timing analysis (completion run): metronomic runs, bursts, parallel
signatures, hour-of-day curves with timezone inference.

Reads raw/htmx_<service>.json AND raw/poller_safe_<service>.json (union by
report_id; sibling fetch_timing.py may overwrite htmx_*.json mid-run).
Tolerates corrupt sibling shapes (e.g. {"reports": ["reports","query"]}).

Known uq-operator exclusion: any report URL containing one of the markers
below is skipped. Writes poller_analysis.json + prints per-service summary
to stdout for the findings report.
"""
import json
import os
import statistics
from collections import Counter
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)

# Exact marker set from the task brief.
UQ_MARKERS = ["uqscan=", "uqtag=", "uqcors", "uqresearch=", "uqmobile=",
              "uqhs=", "uqretry=", "uqinteractive=", "uqvnc=", "uqmuseum=",
              "uqpd=", "uqdirect=", "uqts=", "uqprobe=", "uqfresh="]

METRO_MIN_RUN = 8
METRO_CV_MAX = 0.3
BURST_N = 10
BURST_WIN_S = 1800  # 30 minutes
PARALLEL_N = 3      # distinct target URLs in same minute


def parse_ts(s):
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception:
        return None


def is_uq_operator(url):
    u = str(url).lower()
    return any(m in u for m in UQ_MARKERS)


def load_reports(path):
    try:
        d = json.load(open(path))
    except Exception:
        return []
    if not isinstance(d, dict):
        return []
    rs = d.get("reports", [])
    if not isinstance(rs, list):
        return []
    return [r for r in rs if isinstance(r, dict) and r.get("report_id")]


def collect_service(slug):
    """Union of htmx_<slug>.json + poller_safe_<slug>.json by report_id."""
    union = {}
    for fname in (f"htmx_{slug}.json", f"poller_safe_{slug}.json"):
        for r in load_reports(os.path.join(HERE, fname)):
            union[r["report_id"]] = r
    return list(union.values())


def analyze_service(slug, reports):
    excl = [r for r in reports if is_uq_operator(r.get("url", ""))]
    kept = []
    for r in reports:
        ts = parse_ts(r.get("date", ""))
        if ts is None:
            continue
        kept.append({"ts": ts, "id": r.get("report_id"), "url": r.get("url", "")})
    kept.sort(key=lambda x: x["ts"])

    out = {
        "service": slug,
        "total_fetched": len(reports),
        "excluded_uq_operator": len(excl),
        "kept": len(kept),
        "excluded_samples": [{"id": r.get("report_id"), "url": r.get("url", "")[:140]}
                             for r in excl[:5]],
    }
    if len(kept) < 2:
        out["note"] = "fewer than 2 timestamped reports; no timing analysis"
        return out

    gaps = [(kept[i+1]["ts"] - kept[i]["ts"]).total_seconds() for i in range(len(kept)-1)]

    # --- metronomic runs: >=8 consecutive gaps with CV < 0.3
    metro_runs = []
    i = 0
    while i < len(gaps):
        best = None
        window = []
        j = i
        while j < len(gaps):
            window.append(gaps[j])
            if len(window) >= METRO_MIN_RUN:
                mean = statistics.fmean(window)
                cv = (statistics.pstdev(window) / mean) if mean > 0 else float("inf")
                if cv < METRO_CV_MAX:
                    best = (i, j + 1, list(window), mean, cv)
                else:
                    break
            j += 1
        if best:
            s_idx, e_gap, w, mean, cv = best
            metro_runs.append({
                "start_ts": kept[s_idx]["ts"].isoformat(),
                "end_ts": kept[e_gap]["ts"].isoformat(),
                "report_count": e_gap - s_idx + 1,
                "gap_count": len(w),
                "median_gap_s": statistics.median(w),
                "mean_gap_s": mean,
                "cv": round(cv, 4),
                "report_ids": [r["id"] for r in kept[s_idx:e_gap+1]],
                "urls": sorted({r["url"][:120] for r in kept[s_idx:e_gap+1]}),
            })
            i = e_gap
        else:
            i += 1
    out["metronomic_runs"] = metro_runs

    # --- bursts: sliding 30-min window with >= 10 submissions
    bursts = []
    j = 0
    for i0 in range(len(kept)):
        while j < len(kept) and (kept[j]["ts"] - kept[i0]["ts"]).total_seconds() <= BURST_WIN_S:
            j += 1
        n = j - i0
        if n >= BURST_N:
            bursts.append({
                "start_ts": kept[i0]["ts"].isoformat(),
                "end_ts": kept[j-1]["ts"].isoformat(),
                "count": n,
                "distinct_urls": len({kept[k]["url"] for k in range(i0, j)}),
                "report_ids": [kept[k]["id"] for k in range(i0, j)][:25],
                "urls": sorted({kept[k]["url"][:120] for k in range(i0, j)}),
            })
    bursts.sort(key=lambda b: -b["count"])
    deduped = []
    for b in bursts:
        if not any(abs((parse_ts(b["start_ts"]) - parse_ts(d["start_ts"])).total_seconds()) < BURST_WIN_S
                   for d in deduped):
            deduped.append(b)
    out["burst_clusters"] = deduped

    # --- parallel signatures: >= 3 distinct target URLs in the same minute
    by_minute = {}
    for r in kept:
        m = r["ts"].replace(second=0, microsecond=0).isoformat()
        by_minute.setdefault(m, []).append(r)
    parallel = []
    for m, rs in sorted(by_minute.items()):
        urls = {r["url"] for r in rs}
        if len(urls) >= PARALLEL_N:
            parallel.append({
                "minute_utc": m,
                "submissions": len(rs),
                "distinct_urls": len(urls),
                "report_ids": [r["id"] for r in rs],
                "urls": sorted(u[:140] for u in urls),
            })
    out["parallel_signatures"] = parallel

    # --- hour-of-day curve (UTC)
    hours = Counter(r["ts"].hour for r in kept)
    out["hour_utc_curve"] = [hours.get(h, 0) for h in range(24)]
    out["peak_hour_utc"] = max(hours.items(), key=lambda x: x[1])[0] if hours else None
    out["share_outside_08_18_utc"] = round(
        sum(c for h, c in hours.items() if h < 8 or h >= 18) / len(kept), 3)
    # crude timezone inference: assume activity = local 08:00-18:00, pick offset
    # maximizing overlap of traffic with the assumed business window.
    best_off, best_share = 0, 0.0
    for off in range(-12, 15):
        inside = sum(c for h, c in hours.items() if 8 <= (h + off) % 24 < 18)
        share = inside / len(kept)
        if share > best_share:
            best_share, best_off = share, off
    out["tz_inference"] = {"offset_hours": best_off,
                           "share_in_08_18_local": round(best_share, 3)}

    out["first_ts"] = kept[0]["ts"].isoformat()
    out["last_ts"] = kept[-1]["ts"].isoformat()
    out["median_gap_s_all"] = statistics.median(gaps) if gaps else None
    out["gap_cv_all"] = (statistics.pstdev(gaps) / statistics.fmean(gaps)
                         if gaps and len(gaps) > 1 and statistics.fmean(gaps) > 0 else None)
    out["sample_reports"] = [{"id": r["id"], "date": r["ts"].isoformat(), "url": r["url"][:160]}
                             for r in kept[:10]]
    return out


def main():
    slugs = set()
    for fname in sorted(os.listdir(HERE)):
        for prefix in ("htmx_", "poller_safe_"):
            if fname.startswith(prefix) and fname.endswith(".json"):
                slugs.add(fname[len(prefix):-len(".json")])
    results = []
    for slug in sorted(slugs):
        res = analyze_service(slug, collect_service(slug))
        results.append(res)
        print(f"{slug}: fetched={res['total_fetched']} kept={res['kept']} "
              f"excl={res['excluded_uq_operator']} metro={len(res.get('metronomic_runs', []))} "
              f"bursts={len(res.get('burst_clusters', []))} parallel={len(res.get('parallel_signatures', []))}")
    out_path = os.path.join(PARENT, "poller_analysis.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=1)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
