#!/usr/bin/env python3
"""Egress watcher: probe urlquery htmx endpoint until reachable, then run full POLLER fetch + analysis.

Probes every 300s (max ~8 probes = 40 min). Single probe = one htmx request, 25s timeout.
On success: runs fetch_poller.py (full 15 services), then analyze_poller.py.
Exits 0 on full success; exits 2 if egress never recovered.
"""
import subprocess
import sys
import time
import urllib.request

HERE = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
PROBE_URL = ("https://urlquery.net/api/htmx/search/?"
             "q=url.domain%3Awebhook.site&limit=1&offset=0")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "HX-Request": "true",
    "Accept": "text/html",
    "HX-Current-URL": "https://urlquery.net/search?q=url.domain%3Awebhook.site",
}


def probe():
    try:
        req = urllib.request.Request(PROBE_URL, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=25) as resp:
            body = resp.read(5000)
            return resp.status == 200 and len(body) > 100
    except Exception as e:
        print(f"  probe failed: {type(e).__name__}: {str(e)[:120]}", flush=True)
        return False


def main():
    print("watcher: probing urlquery htmx endpoint...", flush=True)
    for i in range(8):
        print(f"probe {i+1}/8 @ {time.strftime('%H:%M:%S')}", flush=True)
        if probe():
            print("EGRESS UP — running full fetch", flush=True)
            r1 = subprocess.run([sys.executable, f"{HERE}/fetch_poller.py"])
            if r1.returncode != 0:
                print("fetch_poller failed", flush=True)
                sys.exit(3)
            r2 = subprocess.run([sys.executable, f"{HERE}/analyze_poller.py"])
            sys.exit(0 if r2.returncode == 0 else 4)
        if i < 7:
            time.sleep(300)
    print("EGRESS STILL DOWN after 40 min", flush=True)
    sys.exit(2)


if __name__ == "__main__":
    main()
