#!/usr/bin/env python3
"""LANE C: read-only urlquery HTMX search for reverse-tunnel hostnames."""
import json, os, re, time, urllib.request, urllib.error, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
QUERIES = {
    "pinggy_free_link": "run.pinggy-free.link",
    "pinggy_full_bvryr": "bvryr-16-146-184-55",
    "pinggy_ip_octets": "16-146-184-55",
    "serveo_usercontent": "serveousercontent.com",
    "serveo_full": "70a66b041b7fe0b1-35-95-198-152",
    "serveo_machine_prefix": "70a66b041b7fe0b1",
    "label_handle": "ResearchHelperNovOne",
}

def fetch(url, current_url):
    try:
        r = urllib.request.Request(url, headers={
            "User-Agent": "swarmtraces-hunt/lane-c",
            # HTMX fix (2026-10-06): HX-Current-URL is the header that flips
            # /api/htmx/search/ from 204 No Content to 200 + rows. Verified live
            # (see data/2026-10-06-wikimedia-rogue-agents/htmx-fix/workers/verification/VERIFICATION.md);
            # HX-Request alone does NOT fix it. Mirrors the skill pattern
            # (~/workspace/skills/urlquery/bin/uq_htmx_curl.py).
            "HX-Current-URL": current_url,
        })
        with urllib.request.urlopen(r, timeout=60) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return -1, str(e)

summary = {}
for name, q in QUERIES.items():
    url = "https://urlquery.net/api/htmx/search/?q=" + urllib.parse.quote(q) + "&limit=50&offset=0"
    current_url = "https://urlquery.net/search?q=" + urllib.parse.quote(q)
    status, body = fetch(url, current_url)
    uuids = sorted(set(re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", body)))
    fn = f"{BASE}/htmx_{name}.html"
    open(fn, "w").write(body)
    summary[name] = {"query": q, "http_status": status, "html_bytes": len(body),
                     "uuid_count": len(uuids), "uuids": uuids}
    print(f"{name}: status={status} uuids={len(uuids)}", flush=True)
    time.sleep(5)

open(f"{BASE}/htmx_summary.json", "w").write(json.dumps(summary, indent=2))
print("done")
