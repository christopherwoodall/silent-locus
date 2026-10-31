#!/usr/bin/env python3
"""Full 98-row da.gd urlquery pull for sniffer-meta-20261031 (uq-wayback lane).
Pages the authenticated uq.py CLI (limit 100, offset 0/100) until total_hits
is covered. Saves ONLY the sanitized projection: report_id, date, domain,
fqdn, path (query string dropped), final path, title (truncated 200),
tags, boolean token-presence flags. Raw API stdout is NOT persisted:
no IPs, no query-string values, no token values in any file.
"""
import json
import os
import re
import subprocess
import sys

OUT = os.path.expanduser(
    "~/workspace/silent-locus/data/lanes/sniffer-meta-20261031/raw/uq-wayback")
UQ = os.path.expanduser("~/workspace/skills/urlquery/bin/uq.py")
QUERY = "url.domain:da.gd date:[2025-11-01 TO 2026-10-31]"


def sanitize(rep):
    url = rep.get("url") or {}
    addr = url.get("addr", "") or ""
    path = addr.split("?", 1)[0].split("#", 1)[0]
    final = ((rep.get("final") or {}).get("url") or {})
    faddr = final.get("addr", "") or ""
    fpath = faddr.split("?", 1)[0].split("#", 1)[0]
    tags = rep.get("tags") or []
    tagstr = " ".join(str(t) for t in tags)
    full = (addr + " " + faddr + " " + tagstr).lower()
    title = ((rep.get("final") or {}).get("title") or "")[:200]
    return {
        "report_id": rep.get("report_id"),
        "date": rep.get("date"),
        "domain": url.get("domain"),
        "fqdn": url.get("fqdn"),
        "path": path,
        "final_path": fpath,
        "final_domain": final.get("domain"),
        "title": title,
        "tags": tags,
        "has_zz_param": "zz=" in full,
        "has_oai_token": bool(re.search(r"oai[-_]", full)),
        "has_dagd": "da.gd" in full,
        "has_query_in_url": "?" in addr or "?" in faddr,
    }


def main():
    all_reps = []
    total = None
    offset = 0
    while True:
        proc = subprocess.run(
            [sys.executable, UQ, "search", "--query", QUERY,
             "--limit", "100", "--offset", str(offset)],
            capture_output=True, text=True, timeout=240)
        if proc.returncode != 0:
            print(f"FAIL offset={offset}: rc={proc.returncode} "
                  f"{proc.stderr[:300]}", flush=True)
            sys.exit(1)
        data = json.loads(proc.stdout)
        if total is None:
            total = data.get("total_hits")
            print(f"total_hits={total}", flush=True)
        reps = data.get("reports") or []
        print(f"offset={offset}: got {len(reps)}", flush=True)
        all_reps.extend(reps)
        if len(reps) == 0 or len(all_reps) >= (total or 0):
            break
        offset += len(reps)
    ids = [r.get("report_id") for r in all_reps]
    print(f"saved={len(all_reps)} unique_ids={len(set(ids))}", flush=True)
    recs = [sanitize(r) for r in all_reps]
    out_path = os.path.join(OUT, "uq-dagd-domain-FULL.json")
    with open(out_path, "w") as f:
        json.dump({"query": QUERY, "total_hits": total,
                   "saved": len(recs), "unique_ids": len(set(ids)),
                   "reports": recs}, f, indent=1)
    print(f"WROTE {out_path}", flush=True)


if __name__ == "__main__":
    main()
