#!/usr/bin/env python3
"""Lead 4/6 v2: corrected syntax per https://urlquery.net/help/search.
Quoted exact phrases + explicit AND with date ranges, plus http.url.addr
wildcard searches for marker strings in HTTP traffic paths.
"""
import json, os, subprocess, sys, time

REPO = os.path.expanduser("~/workspace/silent-locus")
OUT = os.path.join(REPO, "data", "urlquery-marker-sweep")
UQ = os.path.expanduser("~/workspace/skills/urlquery/bin/uq.py")
RAW = os.path.join(OUT, "raw")
os.makedirs(RAW, exist_ok=True)

QUERIES = [
    ("v2_exploitgym_july", '"exploitgym" AND date:[2026-07-01 TO 2026-07-31]'),
    ("v2_exploitgym_unscoped", '"exploitgym"'),
    ("v2_catflag_july", '"catflag" AND date:[2026-07-01 TO 2026-07-31]'),
    ("v2_catflag_unscoped", '"catflag"'),
    ("v2_restart_server_july", '"restart_server" AND date:[2026-07-01 TO 2026-07-31]'),
    ("v2_restart_server_unscoped", '"restart_server"'),
    ("v2_submit_vul_july", '"submit-vul" AND date:[2026-07-01 TO 2026-07-31]'),
    ("v2_submit_vul_unscoped", '"submit-vul"'),
    ("v2_m47push2", '"m47push2"'),
    ("v2_m47bmbox", '"m47bmbox"'),
    ("v2_m47bbox_variant", '"m47bmbox/"'),
    ("v2_cybergym_arvo_july", '"cybergym/arvo" AND date:[2026-07-01 TO 2026-07-31]'),
    ("v2_cybergym_arvo_unscoped", '"cybergym/arvo"'),
    ("v2_cybergym_july", '"cybergym" AND date:[2026-07-01 TO 2026-07-31]'),
    # HTTP-traffic lens: markers in scanned URLs / request paths
    ("v2_http_restart_server", 'http.url.addr:*restart_server*'),
    ("v2_http_submit_vul", 'http.url.addr:*submit-vul*'),
    ("v2_http_catflag", 'http.url.addr:*catflag*'),
    ("v2_http_m47bmbox", 'http.url.addr:*m47bmbox*'),
    ("v2_http_cybergym", 'http.url.addr:*cybergym*'),
]

log_path = os.path.join(OUT, "progress.log")
logf = open(log_path, "a")

def log(msg):
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%S%z')} {msg}"
    print(line, flush=True)
    logf.write(line + "\n"); logf.flush()

def run_query(label, query):
    raw_file = os.path.join(RAW, f"{label}.json")
    if os.path.exists(raw_file):
        log(f"SKIP {label} (cached)")
        with open(raw_file) as f:
            return json.load(f)
    r = subprocess.run([sys.executable, UQ, "search", "--query", query, "--limit", str(30)],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        log(f"ERROR {label}: {r.stdout.strip()[:200]}")
        return {"error": r.stdout.strip()}
    data = json.loads(r.stdout)
    with open(raw_file, "w") as f:
        json.dump(data, f)
    return data

log("=== sweep v2 start ===")
summary = []
for label, query in QUERIES:
    data = run_query(label, query)
    if "error" in data:
        summary.append({"label": label, "query": query, "error": data["error"]})
        continue
    reps = data.get("reports") or []
    log(f"QUERY {label}: total_hits={data.get('total_hits')} returned={len(reps)}")
    for rep in reps:
        submit_url = rep.get("submit", {}).get("url", {})
        final_url = rep.get("final", {}).get("url", {})
        summary.append({
            "label": label, "query": query,
            "report_id": rep.get("report_id"),
            "date": rep.get("date"),
            "submit": f"{submit_url.get('schema','')}://{submit_url.get('addr','')}",
            "final": f"{final_url.get('schema','')}://{final_url.get('addr','')}",
            "title": rep.get("final", {}).get("title"),
        })
    time.sleep(2)

with open(os.path.join(OUT, "sweep_summary_v2.json"), "w") as f:
    json.dump(summary, f, indent=2)
log("=== sweep v2 done ===")
logf.close()
