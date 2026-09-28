#!/usr/bin/env python3
"""Lane A: read-only proxy capture of ludism.org wikis and ApchemWiki (tmcleod.org).

Read-only recon via public reader proxies ONLY. Gentle pacing (~1 req/5s).
No auth, no submissions, no bypass attempts. Results land in data/ludism-wikis/raw/.
"""
import json, os, time, urllib.request, urllib.parse
from datetime import datetime, timezone

BASE = os.path.expanduser("~/workspace/muse-home/projects/swarmtraces-hf-corpus")
DDIR = BASE + "/data/ludism-wikis"
RAW = DDIR + "/raw"
os.makedirs(RAW, exist_ok=True)
LOG = DDIR + "/progress.log"

def log(msg):
    line = "%s %s" % (datetime.now(timezone.utc).isoformat(), msg)
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

TARGETS = [
    # (short name, direct URL)
    ("ludism_root_http", "http://ludism.org/"),
    ("ludism_root_https", "https://ludism.org/"),
    ("ludism_scwiki_rc", "http://ludism.org/scwiki/?RecentChanges"),
    ("ludism_mentat_rc", "http://ludism.org/mentat/?RecentChanges"),
    ("ludism_gbgwiki_rc", "http://ludism.org/gbgwiki/?RecentChanges"),
    ("ludism_ppwiki_rc", "http://ludism.org/ppwiki/?RecentChanges"),
    ("ludism_gamedesign_rc", "http://ludism.org/gamedesign/?RecentChanges"),
    ("apchem_root", "http://tmcleod.org/cgi-bin/apchem/wiki.cgi"),
    ("apchem_rc", "http://tmcleod.org/cgi-bin/apchem/wiki.cgi?action=rc"),
]

def proxies_for(url):
    enc = urllib.parse.quote(url, safe="")
    return [
        ("jina", "https://r.jina.ai/" + url),
        ("allorigins_raw", "https://api.allorigins.win/raw?url=" + enc),
        ("allorigins_get", "https://api.allorigins.win/get?url=" + enc),
    ]

def fetch(name, via, purl):
    fn = os.path.join(RAW, "%s__%s.txt" % (name, via))
    meta = {
        "target": name, "via": via, "proxy_url": purl,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "ok": False, "error": None, "bytes": 0,
    }
    try:
        req = urllib.request.Request(purl, headers={"User-Agent": "ludism-lane-readonly/1.0 (research recon)"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read()
            meta["ok"] = True
            meta["bytes"] = len(body)
            meta["http_status"] = resp.status
            meta["content_type"] = resp.headers.get("Content-Type")
            with open(fn, "wb") as f:
                f.write(body)
    except Exception as e:
        meta["error"] = "%s: %s" % (type(e).__name__, str(e)[:300])
    with open(fn + ".meta.json", "w") as f:
        json.dump(meta, f, indent=2)
    return meta

def main():
    log("proxy sweep start: %d targets x 3 proxies" % len(TARGETS))
    results = []
    for name, url in TARGETS:
        for via, purl in proxies_for(url):
            m = fetch(name, via, purl)
            status = "OK %d bytes (HTTP %s)" % (m["bytes"], m.get("http_status")) if m["ok"] else "FAIL %s" % m["error"]
            log("fetch %-22s via %-14s -> %s" % (name, via, status))
            results.append(m)
            time.sleep(5)
    ok = [r for r in results if r["ok"]]
    log("proxy sweep done: %d/%d succeeded" % (len(ok), len(results)))
    with open(RAW + "/sweep-summary.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
