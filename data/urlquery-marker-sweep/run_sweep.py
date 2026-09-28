#!/usr/bin/env python3
"""Lead 4/6: urlquery marker sweep for ExploitGym incident markers (read-only).

Runs the documented query list, saves raw JSON per query, logs progress.
Uses ~/workspace/skills/urlquery/bin/uq.py (Secure Vault surrogate auth).
"""
import json, os, subprocess, sys, time, hashlib

REPO = os.path.expanduser("~/workspace/silent-locus")
OUT = os.path.join(REPO, "data", "urlquery-marker-sweep")
UQ = os.path.expanduser("~/workspace/skills/urlquery/bin/uq.py")
RAW = os.path.join(OUT, "raw")
os.makedirs(RAW, exist_ok=True)

QUERIES = [
    # (label, query_string)
    ("exploitgym_july", "exploitgym date:[2026-07-01 TO 2026-07-31]"),
    ("exploitgym_unscoped", "exploitgym"),
    ("catflag_july", "catflag date:[2026-07-01 TO 2026-07-31]"),
    ("catflag_unscoped", "catflag"),
    ("restart_server_july", "restart_server date:[2026-07-01 TO 2026-07-31]"),
    ("restart_server_unscoped", "restart_server"),
    ("submit_vul_july", "submit-vul date:[2026-07-01 TO 2026-07-31]"),
    ("submit_vul_unscoped", "submit-vul"),
    ("m47push2_unscoped", "m47push2"),
    ("m47push2_july", "m47push2 date:[2026-07-01 TO 2026-07-31]"),
    ("m47bmbox_unscoped", "m47bmbox"),
    ("m47bmbox_july", "m47bmbox date:[2026-07-01 TO 2026-07-31]"),
    ("cybergym_arvo_july", "cybergym/arvo date:[2026-07-01 TO 2026-07-31]"),
    ("cybergym_arvo_unscoped", "cybergym/arvo"),
    ("cybergym_july", "cybergym date:[2026-07-01 TO 2026-07-31]"),
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

log("=== sweep start ===")
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
            "tags": rep.get("tags"),
        })
    time.sleep(2)  # gentle pacing

with open(os.path.join(OUT, "sweep_summary.json"), "w") as f:
    json.dump(summary, f, indent=2)
log("=== sweep done ===")
logf.close()
