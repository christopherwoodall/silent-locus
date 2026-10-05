#!/usr/bin/env python3
"""Background live-probe: retries egress, then runs a small corroboration battery.
Saves to nonce-04-live-probe.json. Bounded: 10 tries x 4 min, then gives up."""
import json, os, re, sys, time, html as htmlmod, urllib.parse, urllib.request

OUT = os.path.expanduser("~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/grammarian/raw/nonce-04-live-probe.json")
BASE = "https://urlquery.net"
HDRS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "HX-Request": "true", "Accept": "text/html"}

def egress_ok():
    try:
        req = urllib.request.Request("https://urlscan.io/", headers={"User-Agent": "curl"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status == 200
    except Exception as e:
        return False

def htmx_search(query, limit=24):
    qs = urllib.parse.urlencode({"q": query, "limit": limit, "offset": 0})
    req = urllib.request.Request(BASE + "/api/htmx/search/?" + qs, headers=dict(
        HDRS, **{"HX-Current-URL": BASE + "/search?q=" + urllib.parse.quote(query)}))
    with urllib.request.urlopen(req, timeout=45) as resp:
        page = resp.read().decode("utf-8", "replace")
    rows = re.findall(r'href="/report/([a-f0-9-]{8,36})"[^>]*>([^<]{1,300})</a>', page)
    dates = re.findall(r'(20\d\d-\d\d-\d\d \d\d:\d\d)', page)
    out, seen = [], set()
    for (rid, url), d in zip(rows, dates):
        if rid in seen: continue
        seen.add(rid)
        out.append({"report_id": rid, "url": htmlmod.unescape(url.strip()),
                    "date": d.replace(" ", "T") + ":00Z"})
    return out

def urlscan_search(q, size=40):
    url = "https://urlscan.io/api/v1/search/?" + urllib.parse.urlencode({"q": q, "size": size})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))

result = {"started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
          "egress": False, "probes": {}}
for attempt in range(10):
    if egress_ok():
        result["egress"] = True
        break
    time.sleep(240)
if not result["egress"]:
    result["note"] = "egress still down after 10 tries (~40 min); no live probes run"
    json.dump(result, open(OUT, "w"), indent=1)
    print("egress still down; wrote", OUT)
    sys.exit(0)

try:
    result["probes"]["htmx_gucheng"] = htmx_search("gucheng-", 24)
    time.sleep(8)
    result["probes"]["htmx_uqscan"] = htmx_search("uqscan", 24)
    time.sleep(8)
    result["probes"]["htmx_epoch_word"] = htmx_search("17911", 24)
    time.sleep(10)
    us = urlscan_search('page.url:"uqscan"', 40)
    result["probes"]["urlscan_uqscan"] = [
        {"url": t.get("page", {}).get("url"), "time": t.get("task", {}).get("time")}
        for t in us.get("results", [])]
    time.sleep(10)
    us2 = urlscan_search('page.url:"livecodes.io" AND page.url:"amap"', 40)
    result["probes"]["urlscan_livecodes_amap"] = [
        {"url": t.get("page", {}).get("url"), "time": t.get("task", {}).get("time")}
        for t in us2.get("results", [])]
except Exception as e:
    result["probes"]["error"] = repr(e)[:500]
result["finished"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
json.dump(result, open(OUT, "w"), indent=1)
print("wrote", OUT, "egress was up; probes:", list(result["probes"].keys()))
