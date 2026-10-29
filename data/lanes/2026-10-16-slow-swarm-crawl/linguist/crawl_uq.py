#!/usr/bin/env python3
"""Linguist executor: slow passive urlquery API crawl for fresh grammars.

Passive: read-only public search API, ~3s+ spacing, small limits.
Writes one JSON per query under raw/ with provenance header line in
a sidecar PROVENANCE entry (handled by writer script).
"""
import datetime, hashlib, json, subprocess, sys, time

UQ = "/home/hatch/workspace/skills/urlquery/bin/uq.py"
RAW = "/home/hatch/workspace/silent-locus/data/lanes/2026-10-16-slow-swarm-crawl/linguist/raw"
DELAY = 15  # ~4 requests/min max

QUERIES = [
    ("trycloudflare",  "trycloudflare.com", 60),
    ("ngrokfree",      "ngrok-free", 40),
    ("bore",           "bore.pub", 30),
    ("localhostrun",   "localhost.run", 30),
    ("zrok",           "zrok.io", 30),
    ("pinggy",         "pinggy.io", 30),
    ("smee",           "smee.io", 30),
    ("verb-start",     "-start", 40),
    ("verb-init",      "-init", 40),
    ("verb-probe",     "-probe", 30),
    ("verb-check",     "-check", 30),
    ("verb-setup",     "-setup", 30),
]

def prov_record(fname, query, method):
    with open(f"{RAW}/{fname}", "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    return {
        "file": fname,
        "source_url": f"https://api.urlquery.net (search query: {query})",
        "retrieved_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "method": method,
        "sha256": sha,
    }

def main():
    datef = "date:[2026-01-01 TO 2026-10-16]"
    prov = []
    for slug, q, limit in QUERIES:
        query = f"{q} {datef}"
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        fname = f"uq_{slug}_{ts}.json"
        p = subprocess.run(
            [sys.executable, UQ, "search", "--query", query, "--limit", str(limit)],
            capture_output=True, text=True, timeout=240)
        if p.returncode != 0:
            print(f"[warn] {slug}: uq.py failed: {p.stderr[:200]}", file=sys.stderr)
            time.sleep(DELAY)
            continue
        with open(f"{RAW}/{fname}", "w") as f:
            f.write(p.stdout)
        prov.append(prov_record(fname, query, "urlquery authenticated search API via skills/urlquery/bin/uq.py"))
        n = len((json.loads(p.stdout) or {}).get("reports") or [])
        print(f"[ok] {slug}: {n} rows -> {fname}", flush=True)
        time.sleep(DELAY)
    with open(f"{RAW}/PROVENANCE.txt", "w") as f:
        for rec in prov:
            f.write(json.dumps(rec) + "\n")
    print(f"done: {len(prov)} files")

if __name__ == "__main__":
    main()
