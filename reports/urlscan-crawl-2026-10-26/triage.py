#!/usr/bin/env python3
import json, os, re
BASE = os.path.expanduser("~/workspace/silent-locus/reports/urlscan-crawl-2026-10-26")
MARKERS = ["getpoiinfo", "uqscan=", "uqframe=", "hysandbox"]
for label in ["relay-jina-reader", "title-amap"]:
    data = json.load(open(os.path.join(BASE, "raw", label, "search.json")))
    print(f"== {label} total={data['total']} fetched={len(data['results'])}")
    for r in data["results"]:
        page = r.get("page") or {}
        task = r.get("task") or {}
        url = page.get("url") or task.get("url") or ""
        title = page.get("title") or ""
        low = (url + " " + title).lower()
        matched = [m for m in MARKERS if m in low]
        # fleet POI shape heuristic
        poi = bool(re.search(r"amap-pc-ssr|/ssr/place|getpoiinfo", low))
        print(f"  uuid={(r.get('_id') or task.get('uuid'))} domain={page.get('domain')} ip={page.get('ip')} asn={page.get('asn')} markers={matched} poi_shape={poi} title={title[:80]!r}")
        print(f"    url_host_path={url.split('?')[0][:180]}")
