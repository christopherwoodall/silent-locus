#!/usr/bin/env python3
"""Background watcher: run the urlquery htmx migration-hunt battery once VM egress recovers.

- Polls egress every 120s (curl https://example.com, 20s timeout).
- When egress is up, runs uq_htmx.py for every query in the battery with >=6s
  between ANY two requests (STRICTLY <=1 req/5s per task).
- Writes results incrementally to OUTPUT_JSON so partial progress survives.
- Exits when the battery is complete or max attempts are exhausted.
"""
import json
import os
import subprocess
import sys
import time

UQ_HTMX = os.path.expanduser("~/workspace/skills/urlquery/bin/uq_htmx.py")
OUTDIR = os.path.expanduser(
    "~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/mimic/raw"
)
OUTPUT_JSON = os.path.join(OUTDIR, "infra-migration-htmx.json")
LOG = os.path.join(OUTDIR, "infra-migration-htmx.log")
BETWEEN_REQS = 6.0          # seconds between any two requests (>=5s required)
EGRESS_POLL = 120           # seconds between egress checks
MAX_POLLS = 45              # ~90 minutes of waiting

# ---- query battery (lane, query) ----
JINA_CANDIDATES = [
    "md.dhr.wtf", "md.succ.ai", "pure.md", "markdown.new", "urltotext",
    "markdowner", "scraperapi", "firecrawl", "crawlbase", "browserless",
    "textance", "r.jina.ai",
]
DEADDROPS = ["ntfy.sh", "requestcatcher", "beeceptor", "pipedream",
             "mocky", "jsonblob", "legible.sh"]
SHORTENERS = ["da.gd", "t.cn", "dwz.cn", "clck.ru", "s.id", "gg.gg",
              "tinyurl", "t.ly"]
TUNNELS = ["ngrok", "bore.pub", "zrok", "trycloudflare", "loca.lt"]

BATTERY = []
for d in JINA_CANDIDATES:
    BATTERY.append(("jina-replacement", f"uqscan {d}"))
    BATTERY.append(("jina-replacement", f"amap {d}"))
for d in DEADDROPS:
    BATTERY.append(("dead-drop", f"uqscan {d}"))
    BATTERY.append(("dead-drop", f"amap {d}"))
for d in SHORTENERS:
    BATTERY.append(("shortener", f"uqscan {d}"))
for d in TUNNELS:
    BATTERY.append(("tunnel", f"uqscan {d}"))


def log(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def egress_up():
    try:
        r = subprocess.run(
            ["curl", "-s", "-m", "15", "-o", "/dev/null", "-w", "%{http_code}",
             "https://example.com"],
            capture_output=True, text=True, timeout=25,
        )
        return r.stdout.strip() == "200"
    except Exception:
        return False


def load_done():
    if os.path.exists(OUTPUT_JSON):
        try:
            with open(OUTPUT_JSON) as f:
                data = json.load(f)
            return {e["query"]: e for e in data.get("entries", [])}
        except Exception:
            return {}
    return {}


def save_all(entries):
    tmp = OUTPUT_JSON + ".tmp"
    with open(tmp, "w") as f:
        json.dump({"entries": entries, "completed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")}, f)
    os.replace(tmp, OUTPUT_JSON)


def run_query(query, delay=BETWEEN_REQS):
    r = subprocess.run(
        [sys.executable, UQ_HTMX, "search", "--query", query,
         "--limit", "30", "--delay", str(delay)],
        capture_output=True, text=True, timeout=300,
    )
    if r.returncode != 0:
        raise RuntimeError(f"uq_htmx failed rc={r.returncode}: {r.stderr[:400]}")
    return json.loads(r.stdout)


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    log("watcher started; waiting for egress")
    polls = 0
    while polls < MAX_POLLS:
        if egress_up():
            log("EGRESS UP - starting battery")
            break
        polls += 1
        log(f"egress down (poll {polls}/{MAX_POLLS}); sleeping {EGRESS_POLL}s")
        time.sleep(EGRESS_POLL)
    else:
        log("ABORT: egress never recovered within poll budget")
        return 2

    done = load_done()
    entries = list(done.values())
    log(f"resuming: {len(entries)} queries already have results")
    for lane, query in BATTERY:
        if query in done:
            continue
        if not egress_up():
            log(f"egress dropped mid-battery at query '{query}'; aborting, partial saved")
            save_all(entries)
            return 3
        try:
            res = run_query(query)
            entry = {"lane": lane, "query": query, "n": len(res.get("reports", [])),
                     "reports": res.get("reports", [])}
            entries.append(entry)
            done[query] = entry
            save_all(entries)
            log(f"OK lane={lane} q='{query}' n={entry['n']}")
        except Exception as e:
            log(f"FAIL lane={lane} q='{query}': {e}")
        time.sleep(BETWEEN_REQS)
    save_all(entries)
    log(f"BATTERY COMPLETE: {len(entries)} queries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
