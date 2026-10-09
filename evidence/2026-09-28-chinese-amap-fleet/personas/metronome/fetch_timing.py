#!/usr/bin/env python3
"""Metronome persona: fetch timing data from urlquery htmx for candidate agent-infra surfaces.
Saves raw per-query JSON to personas/metronome/raw/. Polite: 6s between requests,
retries with backoff. Run in background."""
import json, os, sys, time, urllib.parse
sys.path.insert(0, os.path.expanduser("~/workspace/skills/urlquery/bin"))
import importlib.util
spec = importlib.util.spec_from_file_location("uq_htmx", os.path.expanduser("~/workspace/skills/urlquery/bin/uq_htmx.py"))
uq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uq)

OUT = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/metronome/raw")
os.makedirs(OUT, exist_ok=True)

QUERIES = [
    "lhr.life", "localhost.run", "webhook.site", "httpbun", "r.jina.ai",
    "translate.goog", "is.gd", "tinyurl", "v.gd", "cachedview.nl",
    "archive.ph", "ngrok", "trycloudflare", "herokuapp", "glitch.me",
    "replit", "vercel.app", "netlify.app", "workers.dev", "pages.dev",
    "requestbin", "pipedream", "ntfy.sh", "file.io", "transfer.sh",
    "0x0.st", "paste.rs", "hastebin", "rentry", "telegra.ph",
    "shorturl", "bit.ly", "t.co", "goo.gl", "da.gd",
]

def fetch_all(query, limit=200):
    out = []
    offset = 0
    while len(out) < limit:
        try:
            rs = uq.search(query, limit=50, offset=offset, delay=0)
        except Exception as e:
            print(f"  [{query}] fetch error @{offset}: {e}", flush=True)
            time.sleep(20)
            try:
                rs = uq.search(query, limit=50, offset=offset, delay=0)
            except Exception as e2:
                print(f"  [{query}] retry failed: {e2}", flush=True)
                break
        if not rs:
            break
        out.extend(rs)
        if len(rs) < 50:
            break
        offset += 50
        time.sleep(6)
    return out[:limit]

for q in QUERIES:
    path = os.path.join(OUT, "htmx_" + q.replace(".", "_").replace("/", "_") + ".json")
    if os.path.exists(path):
        try:
            d = json.load(open(path))
            if len(d.get("reports", [])) >= 150:
                print(f"[{q}] cached ({len(d['reports'])})", flush=True)
                continue
        except Exception:
            pass
    print(f"[{q}] fetching...", flush=True)
    rs = fetch_all(q)
    json.dump({"query": q, "reports": rs}, open(path, "w"), indent=1)
    print(f"[{q}] got {len(rs)}", flush=True)
    time.sleep(6)
print("DONE", flush=True)
