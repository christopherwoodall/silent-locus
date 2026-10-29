#!/usr/bin/env python3
"""Paginated urlquery.net collector. Saves raw search pages + full reports.

Usage:
    collect_uq.py --out DIR --query QUERY --date-from YYYY-MM-DD --date-to YYYY-MM-DD
    collect_uq.py --out DIR --reports id1,id2,...
"""
import argparse, json, os, subprocess, sys, time

UQ = os.path.expanduser("~/workspace/skills/urlquery/bin/uq.py")
SLEEP = 2.0

def uq(args):
    r = subprocess.run([sys.executable, UQ] + args, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"uq.py failed: {r.stderr[:300]}")
    return json.loads(r.stdout)

def collect_pages(out, base_query, date_from, date_to, limit=100):
    q = f"({base_query}) date:[{date_from} TO {date_to}]"
    first = uq(["search", "--query", q, "--limit", "1"])
    total = first.get("total_hits", 0)
    print(f"query={q} total_hits={total}", flush=True)
    pages = (total + limit - 1) // limit
    got = 0
    for p in range(pages):
        off = p * limit
        try:
            data = uq(["search", "--query", q, "--limit", str(limit), "--offset", str(off)])
        except Exception as e:
            print(f"PAGE {p} offset {off} FAILED: {e}", flush=True)
            with open(os.path.join(out, "FAILED_PAGES.txt"), "a") as f:
                f.write(f"{p} {off} {e}\n")
            time.sleep(SLEEP * 3)
            continue
        n = len(data.get("reports", []))
        got += n
        with open(os.path.join(out, f"page_{p:03d}.json"), "w") as f:
            json.dump(data, f)
        print(f"page {p}/{pages-1} offset {off}: {n} reports (cum {got})", flush=True)
        time.sleep(SLEEP)
    return total, got

def collect_reports(out, ids):
    for rid in ids:
        rid = rid.strip()
        if not rid: continue
        dest = os.path.join(out, f"report_{rid}.json")
        if os.path.exists(dest):
            print(f"skip {rid} (exists)", flush=True); continue
        try:
            data = uq(["report", rid])
        except Exception as e:
            print(f"REPORT {rid} FAILED: {e}", flush=True)
            continue
        with open(dest, "w") as f:
            json.dump(data, f)
        print(f"report {rid}: ok ({len(json.dumps(data))} bytes)", flush=True)
        time.sleep(SLEEP)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--query", default=None)
    ap.add_argument("--date-from", default=None)
    ap.add_argument("--date-to", default=None)
    ap.add_argument("--reports", default=None)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if a.query:
        total, got = collect_pages(a.out, a.query, a.date_from, a.date_to)
        with open(os.path.join(a.out, "COLLECT_STATS.json"), "w") as f:
            json.dump({"query": a.query, "date_from": a.date_from, "date_to": a.date_to,
                       "api_total_hits": total, "reports_saved": got}, f, indent=2)
    if a.reports:
        collect_reports(a.out, a.reports.split(","))

if __name__ == "__main__":
    main()
