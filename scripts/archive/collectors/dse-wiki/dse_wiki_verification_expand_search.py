#!/usr/bin/env python3
"""Lane 23 expansion: live urlquery HTMX search for TTP-adjacent indicators."""
import json, os, time, urllib.request, urllib.error, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "expansion")
os.makedirs(OUT, exist_ok=True)

QUERIES = {
    "unm_nmdigital": "nmdigital.unm.edu",
    "unm_tok_expt": "tok=expt",
    "aihw_pp": "pp.aihw.gov.au",
    "bridge_milankarman": "milankarman.github.io",
    "bridge_blogsflow": "blogsflow.liftbrandfulfillment.com",
    "wiki_wikiservice": "wikiservice.at",
    "beacon_setsid": "setsid",
    "beacon_nohup": "nohup",
    "disposable_mailgw": "mail.gw",
    "thai_oncb": "oncb",
    "counterapi": "counterapi.dev",
    "prng_seed": "random.Random",
}

def fetch(url, q):
    # HTMX fix (2026-10-06): HX-Current-URL is the header that flips
    # /api/htmx/search/ from 204 No Content to 200 + rows. Verified live
    # (see data/2026-10-06-wikimedia-rogue-agents/htmx-fix/workers/verification/VERIFICATION.md);
    # the prior HX-Request-only set did NOT fix it. Mirrors the skill pattern
    # (~/workspace/skills/urlquery/bin/uq_htmx_curl.py).
    current_url = "https://urlquery.net/search?q=" + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (research; read-only)",
        "HX-Request": "true",
        "HX-Current-URL": current_url,
        "Referer": "https://urlquery.net/search",
    })
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:
        return -1, str(e)

def main():
    summary = {}
    for name, q in QUERIES.items():
        url = "https://urlquery.net/api/htmx/search/?q=" + urllib.parse.quote(q) + "&limit=50&offset=0"
        status, body = fetch(url, q)
        # extract report UUIDs from the htmx HTML
        import re
        uuids = sorted(set(re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", body)))
        summary[name] = {"query": q, "http_status": status, "html_bytes": len(body), "uuids": uuids, "count": len(uuids)}
        print(f"{name}: status={status} uuids={len(uuids)}")
        time.sleep(5)
    with open(os.path.join(OUT, "search_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    main()
