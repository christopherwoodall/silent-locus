#!/usr/bin/env python3
"""Timeline analysis for lane 1 (Arquivo.pt collection).

Per steering 2026-10-01: full capture timestamps are first-class evidence.
Builds per-target:
  timeline/<slug>.timeline.csv     - every capture: ISO ts (UTC, second precision),
                                     url, status, mime, digest, collection,
                                     filename, in_incident_window, out_window_side
  timeline/<slug>.perminute.csv    - per-minute rates + unique-URL counts
  timeline/<slug>.perhour.csv      - per-hour rates
  timeline/<slug>.summary.json     - volumes vs Transluce claims, peak rates,
                                     burst flags, out-of-window leads,
                                     status/mime/collection distributions,
                                     nonce-param detections
Run: python3 analyze.py
"""
import csv, json, re, gzip
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse, parse_qsl

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
TL = HERE / "timeline"
TL.mkdir(exist_ok=True)

def open_raw(path):
    # raw captures are stored gzipped (raw/<slug>.cdx.jsonl.gz)
    gz = Path(str(path) + ".gz")
    if gz.exists():
        return gzip.open(str(gz), "rt", encoding="utf-8", errors="replace")
    if path.exists():
        return path.open(encoding="utf-8", errors="replace")
    return None

TARGETS = {
    "kansas-kansasmemory":  ("2026-05-07", "2026-05-07", 36578, 1093),
    "maryland-edstats":     ("2026-05-06", "2026-05-06", 295912, 5594),
    "illinois-iquery":      ("2026-04-19", "2026-05-01", 251, None),
    "lac-collectionsearch": ("2026-05-28", "2026-06-09", 899, None),
    "doe-crdc":             ("2026-06-17", "2026-06-17", 200000, None),
    "bea-api":              ("2026-06-16", "2026-06-18", 3005, None),
    "omb-max":              ("2026-05-25", "2026-05-27", None, None),
    "navy-history":         ("2026-04-23", "2026-05-18", None, None),
    "doj-ojjdp":            ("2026-05-30", "2026-05-31", None, None),
    "sec":                  ("2026-06-18", "2026-06-18", None, None),
    "cdc-wonder":           ("2026-07-18", "2026-07-18", None, None),
    "calaccess":            ("2026-05-26", "2026-05-26", None, None),
    "nysed-enrollment":     ("2026-05-17", "2026-05-17", None, None),
    "texas-dshs":           ("2026-05-17", "2026-05-17", None, None),
}

NONCE_RE = re.compile(r"(uniq\d*|nonce|_t$|timestamp|ts$|rnd|rand|cachebust)", re.I)
EPOCHISH_RE = re.compile(r"^\d{10,13}$")

def iso(ts):
    # CDX timestamp YYYYMMDDHHMMSS -> ISO UTC
    dt = datetime.strptime(ts, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    return dt.isoformat()

def analyze(slug, wfrom, wto, claimed_vol, claimed_peak):
    path = RAW / f"{slug}.cdx.jsonl"
    fh = open_raw(path)
    if fh is None:
        return {"slug": slug, "error": "no raw file (collection failed or zero captures)"}
    seen = set()
    recs = []
    with fh as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            key = (r.get("timestamp"), r.get("url"))
            if key in seen:
                continue
            seen.add(key)
            recs.append(r)
    wfrom_d = datetime.strptime(wfrom, "%Y-%m-%d").date()
    wto_d = datetime.strptime(wto, "%Y-%m-%d").date()

    rows = []
    per_min = Counter(); per_min_urls = defaultdict(set)
    per_hour = Counter()
    statuses = Counter(); mimes = Counter(); collections = Counter()
    out_before = 0; out_after = 0; out_dates = set()
    nonce_urls = set(); fuzzish = Counter()
    for r in recs:
        ts = r.get("timestamp", "")
        try:
            dt = datetime.strptime(ts, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        d = dt.date()
        in_win = wfrom_d <= d <= wto_d
        side = ""
        if not in_win:
            side = "before" if d < wfrom_d else "after"
            if side == "before": out_before += 1
            else: out_after += 1
            out_dates.add(str(d))
        url = r.get("url", "")
        status = str(r.get("status", ""))
        per_min[dt.strftime("%Y-%m-%dT%H:%M")] += 1
        per_min_urls[dt.strftime("%Y-%m-%dT%H:%M")].add(url)
        per_hour[dt.strftime("%Y-%m-%dT%H")] += 1
        statuses[status] += 1
        mimes[str(r.get("mime", ""))] += 1
        collections[str(r.get("collection", ""))] += 1
        # nonce-style query params (?uniqN template)
        q = urlparse(url).query
        if q:
            for k, v in parse_qsl(q, keep_blank_values=True):
                if NONCE_RE.search(k) or (NONCE_RE.search(v) if isinstance(v, str) else False):
                    nonce_urls.add(url)
                if EPOCHISH_RE.match(v or ""):
                    fuzzish["epochish_param_value"] += 1
        rows.append({
            "iso_ts": dt.isoformat(), "url": url, "status": status,
            "mime": r.get("mime", ""), "digest": r.get("digest", ""),
            "collection": r.get("collection", ""), "filename": r.get("filename", ""),
            "in_incident_window": in_win, "out_window_side": side,
        })
    rows.sort(key=lambda x: x["iso_ts"])

    with (TL / f"{slug}.timeline.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["iso_ts", "url", "status", "mime",
                                          "digest", "collection", "filename",
                                          "in_incident_window", "out_window_side"])
        w.writeheader(); w.writerows(rows)

    with (TL / f"{slug}.perminute.csv").open("w", newline="") as f:
        w = csv.writer(f); w.writerow(["minute_utc", "n_captures", "n_unique_urls"])
        for m in sorted(per_min):
            w.writerow([m + ":00Z", per_min[m], len(per_min_urls[m])])

    with (TL / f"{slug}.perhour.csv").open("w", newline="") as f:
        w = csv.writer(f); w.writerow(["hour_utc", "n_captures"])
        for h in sorted(per_hour):
            w.writerow([h + ":00Z", per_hour[h]])

    peak_min = per_min.most_common(10)
    peak_hour = per_hour.most_common(5)
    # burst flag: any minute >= 100 captures, or >= claimed peak*0.5
    bursts = [m for m, c in per_min.items() if c >= 100]
    summary = {
        "slug": slug,
        "incident_window": [wfrom, wto],
        "transluce_claimed_volume": claimed_vol,
        "transluce_claimed_peak_per_min": claimed_peak,
        "captures_collected_unique": len(rows),
        "captures_in_incident_window": len([r for r in rows if r["in_incident_window"]]),
        "captures_outside_window_before": out_before,
        "captures_outside_window_after": out_after,
        "out_of_window_dates": sorted(out_dates),
        "volume_vs_claim": (len([r for r in rows if r["in_incident_window"]]) / claimed_vol
                            if claimed_vol else None),
        "peak_minutes_top10": [{"minute_utc": m + ":00Z", "captures": c,
                                 "unique_urls": len(per_min_urls[m])} for m, c in peak_min],
        "peak_hours_top5": [{"hour_utc": h + ":00Z", "captures": c} for h, c in peak_hour],
        "burst_minutes_ge100": len(bursts),
        "burst_minutes_list": sorted(bursts)[:20],
        "status_distribution": dict(statuses.most_common(20)),
        "mime_distribution": dict(mimes.most_common(20)),
        "collection_distribution": dict(collections.most_common(20)),
        "savepagenow_share": (collections.get("SAWP5", 0) / len(rows)) if rows else 0,
        "urls_with_nonce_params": len(nonce_urls),
        "nonce_param_examples": sorted(nonce_urls)[:10],
        "epochish_param_value_count": fuzzish.get("epochish_param_value", 0),
        "notes": [],
    }
    if claimed_vol and summary["captures_in_incident_window"] < claimed_vol * 0.5:
        summary["notes"].append(
            f"collected in-window volume is {summary['volume_vs_claim']:.2%} of Transluce claim; "
            "gap may be collection pagination limits, CDX lag, or claim-methodology difference")
    if out_before or out_after:
        summary["notes"].append(
            "OUT-OF-WINDOW captures found — potential new leads (see timeline.csv out_window_side)")
    if bursts:
        summary["notes"].append(
            f"{len(bursts)} burst minutes (>=100 captures/min) — temporal clustering consistent with automated relay use")
    with (TL / f"{slug}.summary.json").open("w") as f:
        json.dump(summary, f, indent=1)
    return summary

def main():
    results = []
    for slug, (wfrom, wto, vol, peak) in TARGETS.items():
        s = analyze(slug, wfrom, wto, vol, peak)
        results.append(s)
        print(f"{slug}: {s.get('captures_collected_unique', 'ERR')}")
    with (HERE / "timeline_index.json").open("w") as f:
        json.dump(results, f, indent=1)

if __name__ == "__main__":
    main()
