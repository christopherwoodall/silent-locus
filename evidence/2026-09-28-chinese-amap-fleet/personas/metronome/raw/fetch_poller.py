#!/usr/bin/env python3
"""POLLER persona fetch: 15 dead-drop/relay services via urlquery htmx endpoint.

Usage: python3 fetch_poller.py
Saves raw JSON per service to this dir as htmx_<service>.json.
Politeness: 6s between service calls, --delay 6 within calls (max ~1 req/5s).
On 429/empty: sleep 30s, retry once, move on.
"""
import json
import os
import subprocess
import sys
import time
import urllib.parse

BIN = os.path.expanduser("~/workspace/skills/urlquery/bin/uq_htmx.py")
OUT = os.path.dirname(os.path.abspath(__file__))

SERVICES = {
    "webhook_site":  "url.domain:webhook.site",
    "ntfy_sh":       "url.domain:ntfy.sh",
    "requestbin":    "url.domain:requestbin.com",
    "pipedream":     "url.domain:pipedream.net",
    "telegra_ph":    "url.domain:telegra.ph",
    "file_io":       "url.domain:file.io",
    "0x0_st":        "url.domain:0x0.st",
    "paste_rs":      "url.domain:paste.rs",
    "rentry":        "url.domain:rentry.co",
    "hastebin":      "url.domain:hastebin.com",
    "temp_sh":       "url.domain:temp.sh",
    "catbox_moe":    "url.domain:catbox.moe",
    "litterbox":     "url.domain:litterbox.catbox.moe",
    "transfer_it":   "url.domain:transfer.it",
    "filebin_net":   "url.domain:filebin.net",
}

LOG = os.path.join(OUT, "fetch_poller.log")


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def run_query(query, limit=50):
    """Returns parsed JSON dict or raises on failure."""
    cmd = [sys.executable, BIN, "search", "--query", query, "--limit", str(limit), "--delay", "6"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        raise RuntimeError(f"exit {p.returncode}: {p.stderr[:400]}")
    return json.loads(p.stdout)


def main():
    log(f"POLLER fetch start: {len(SERVICES)} services")
    for i, (slug, query) in enumerate(SERVICES.items()):
        out_path = os.path.join(OUT, f"htmx_{slug}.json")
        tries = 0
        while tries < 2:
            tries += 1
            try:
                data = run_query(query)
                n = len(data.get("reports", []))
                with open(out_path, "w") as f:
                    json.dump(data, f, indent=1)
                log(f"[{i+1}/{len(SERVICES)}] {slug}: {n} reports -> {out_path}")
                break
            except Exception as e:
                log(f"[{i+1}/{len(SERVICES)}] {slug}: attempt {tries} FAILED: {e}")
                if tries >= 2:
                    log(f"  moving on (no data saved for {slug})")
                else:
                    log("  backing off 30s...")
                    time.sleep(30)
        # politeness: 6s between service calls
        if i < len(SERVICES) - 1:
            time.sleep(6)
    log("POLLER fetch done.")


if __name__ == "__main__":
    main()
