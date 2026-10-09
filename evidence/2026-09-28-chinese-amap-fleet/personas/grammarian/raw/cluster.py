#!/usr/bin/env python3
"""Cluster htmx param-probe results into candidate grammars.

Reads htmx-params-*.json (+ optional enriched full-URL sidecars
htmx-params-*.enriched.json mapping report_id -> full submitted URL),
writes a cluster summary JSON per probe for the verdict stage.
"""
import json, re, sys, glob, os
from urllib.parse import urlparse, parse_qsl
from collections import defaultdict
from datetime import datetime

RAW = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/grammarian/raw")

def shape_of(v):
    """Return a regex-like shape class for a param value."""
    if re.fullmatch(r"\d{8}", v):
        return r"\d{8}(datelike)"
    if re.fullmatch(r"[0-9a-f]{32}", v, re.I):
        return r"hex{32}"
    if re.fullmatch(r"[0-9a-f]{16}", v, re.I):
        return r"hex{16}"
    if re.fullmatch(r"[0-9a-f]{8,64}", v, re.I):
        return f"hex{{{len(v)}}}"
    if re.fullmatch(r"\d{10}", v):
        return r"\d{10}(epoch?)"
    if re.fullmatch(r"\d{13}", v):
        return r"\d{13}(ms-epoch?)"
    if re.fullmatch(r"\d{5,}", v):
        return f"\\d{{{len(v)}}}"
    if re.fullmatch(r"[A-Za-z]+-?\d+", v):
        return r"word+counter"
    if re.fullmatch(r"[A-Za-z]+-\d{8}", v):
        return r"word-YYYYMMDD"
    if re.fullmatch(r"[A-Za-z]+", v):
        return r"word"
    if re.fullmatch(r"[\w-]{1,40}", v):
        return r"token-ish"
    return "other"

def main():
    out = {}
    for path in sorted(glob.glob(os.path.join(RAW, "htmx-params-*.json"))):
        if path.endswith(".enriched.json"):
            continue
        name = os.path.basename(path)[len("htmx-params-"):-len(".json")]
        data = json.load(open(path))
        reports = data.get("reports", [])
        enr_path = path.replace(".json", ".enriched.json")
        enriched = json.load(open(enr_path)) if os.path.exists(enr_path) else {}
        clusters = defaultdict(list)
        for r in reports:
            rid = r.get("report_id", "")
            full = enriched.get(rid, "")
            if full:
                try:
                    params = parse_qsl(urlparse(full).query, keep_blank_values=True)
                except Exception:
                    params = []
            else:
                params = []
            host = urlparse(full).netloc if full else (r.get("url", "").split("/")[0])
            clusters_key = None
            for k, v in params:
                if k.startswith("uq"):
                    continue  # known-operator grammar, excluded
                clusters[(k, shape_of(v))].append({
                    "rid": rid, "value": v, "host": host, "date": r.get("date", ""),
                    "url": full or r.get("url", ""),
                })
            if not params:
                clusters[("__no_params_visible__", "")].append({
                    "rid": rid, "value": "", "host": host, "date": r.get("date", ""),
                    "url": r.get("url", ""),
                })
        summary = []
        for (k, shp), items in sorted(clusters.items(), key=lambda x: -len(x[1])):
            dates = sorted(i["date"] for i in items if i["date"])
            hosts = sorted(set(i["host"] for i in items if i["host"]))
            summary.append({
                "param": k, "shape": shp, "count": len(items),
                "span": [dates[0], dates[-1]] if dates else [],
                "distinct_hosts": len(hosts), "hosts_sample": hosts[:10],
                "examples": items[:5],
            })
        out[name] = {"n_reports": len(reports), "clusters": summary}
        print(f"{name}: {len(reports)} reports, {len(summary)} clusters")
    json.dump(out, open(os.path.join(RAW, "clusters.json"), "w"), indent=2)
    print("wrote clusters.json")

main()
