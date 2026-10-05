#!/usr/bin/env python3
"""Enrich probe results with full submitted URLs via authenticated uq.py report endpoint.

Usage: enrich.py htmx-params-<name>.json [max_reports]
Writes htmx-params-<name>.enriched.json : {report_id: full_url}
Only fetches reports not already enriched. Polite: 6s between calls.
"""
import json, os, sys, time, subprocess

RAW = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/grammarian/raw")
UQ = os.path.expanduser("~/workspace/skills/urlquery/bin/uq.py")

def main():
    src = sys.argv[1]
    maxn = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    data = json.load(open(src))
    dest = src.replace(".json", ".enriched.json")
    enriched = json.load(open(dest)) if os.path.exists(dest) else {}
    ids = [r["report_id"] for r in data.get("reports", []) if r.get("report_id") not in enriched][:maxn]
    print(f"{len(ids)} reports to enrich -> {dest}")
    for i, rid in enumerate(ids):
        for attempt in (1, 2):
            try:
                p = subprocess.run([UQ, "report", rid], capture_output=True, text=True, timeout=90)
                d = json.loads(p.stdout)
                url = d.get("url") or d.get("report", {}).get("url") or ""
                if url:
                    enriched[rid] = url
                    print(f"[{i+1}/{len(ids)}] {rid} -> {url[:110]}")
                    break
                print(f"[{i+1}/{len(ids)}] {rid}: no url field, keys={list(d.keys())[:8]}")
                break
            except Exception as e:
                print(f"[{i+1}/{len(ids)}] {rid}: attempt {attempt} failed: {e}")
                time.sleep(15)
        json.dump(enriched, open(dest, "w"), indent=1)
        time.sleep(6)
    print(f"done: {len(enriched)} enriched")

main()
