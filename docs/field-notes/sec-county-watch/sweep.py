#!/usr/bin/env python3
"""LANE 4 (sec-county-watch): one-shot/idempotent urlquery sweep for
SEC county.json laundering hits since the watermark date.

Idempotency: hits are deduped by urlquery report_id (state.json 'seen_ids'
+ data/hits.jsonl). Re-running with the same watermark fetches nothing new
(it still re-pages the API to CHECK for new hits, but appends zero rows).
Advancing the watermark is an explicit, recorded action in state.json.

Query = urlquery search keyword 'county.json' (matches against submitted
URLs, so it catches direct sec.gov hits, relay-wrapped hits, double-slash
and path-traversal mutations — all contain the literal string), filtered
client-side to date >= watermark AND the submitted URL actually containing
'county.json' (search also matches page-content mentions).

Polite API use: ~2s between requests; page size 50.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
import dynamic_credentials as dc

BASE = "https://api.urlquery.net"
CRED = "custom.urlquery"
HOSTS = ["api.urlquery.net"]

LANE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(LANE_DIR, "state.json")
DATA_DIR = os.path.join(LANE_DIR, "data")
HITS_PATH = os.path.join(DATA_DIR, "hits.jsonl")
PAGE_SIZE = 50
SLEEP_S = 2.0

# Relay/laundering hosts to flag (from Sep-28 notes + Transluce claim #14)
RELAY_HOSTS = [
    "allorigins", "corsfix", "workers.dev", "r.jina.ai",
    "cors.lol", "corsproxy.io", "api.allorigins.win",
]


def api_get(path):
    req = urllib.request.Request(BASE + path, headers={"Accept": "application/json"})
    dc.add_surrogate_to_request(req, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return dc.read_json_response(resp)


def full_url(rep):
    u = rep.get("url") or {}
    scheme = u.get("schema") or "https"
    addr = u.get("addr") or ""
    return f"{scheme}://{addr}"


def classify(rep):
    """Return list of indicator strings for a county.json URL hit."""
    ind = []
    furl = full_url(rep)
    lower = furl.lower()
    # strip scheme://host to inspect the path+query for // and traversal
    m = re.match(r"^[a-z]+://([^/?#]+)(.*)$", lower)
    host, rest = (m.group(1), m.group(2)) if m else ("", lower)
    if any(r in host for r in RELAY_HOSTS):
        ind.append("cors-laundering")
    rest_noscheme = rest.replace("://", "")
    if "//" in rest_noscheme:
        ind.append("double-slash")
    if "../" in rest or "/./" in rest or "%2e%2e" in rest or "%252e" in rest:
        ind.append("path-traversal")
    if (
        "sec.gov." in host
        or host.endswith(":443")
        or host.startswith("www.sec.gov:")
        or re.search(r"sec\.gov\.[/:?]", rest)
    ):
        ind.append("host-mutation")
    if "sec.gov" in lower or "investor.gov" in lower:
        ind.append("sec-target")
    return ind


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as f:
            return json.load(f)
    return {
        "lane": "sec-county-watch",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "watermark": "2026-09-28T00:00:00Z",
        "items_collected": 0,
        "status": "initialized",
        "last_sweep": None,
        "seen_ids": [],
    }


def main():
    state = load_state()
    watermark = state["watermark"]
    os.makedirs(DATA_DIR, exist_ok=True)

    seen = set(state.get("seen_ids", []))
    # rebuild seen from hits.jsonl (belt and suspenders)
    if os.path.exists(HITS_PATH):
        with open(HITS_PATH) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        row = json.loads(line)
                        seen.add(row.get("report_id"))
                    except Exception:
                        pass

    new_rows = []
    offset = 0
    total = None
    scanned = 0
    while True:
        q = urllib.parse.urlencode(
            {"query": "county.json", "limit": PAGE_SIZE, "offset": offset}
        )
        try:
            d = api_get(f"/public/v1/search/reports/?{q}")
        except Exception as e:  # noqa: BLE001
            state["status"] = f"error: {e}"
            break
        if d.get("error"):
            state["status"] = f"api error: {d['error']}"
            break
        total = d.get("total_hits", total)
        reports = d.get("reports", [])
        for rep in reports:
            scanned += 1
            furl = full_url(rep)
            if "county.json" not in furl.lower():
                continue  # keyword matched page content, not the URL
            rdate = rep.get("date") or ""
            if rdate < watermark:
                continue
            rid = rep.get("report_id")
            if rid in seen:
                continue
            indicators = classify(rep)
            new_rows.append(
                {
                    "url": furl,
                    "report_id": rid,
                    "first_seen": rdate,
                    "source": "urlquery-api",
                    "indicators": indicators,
                    "provenance": (
                        "urlquery public API v1 search 'county.json', "
                        "client-filtered: submitted URL contains "
                        "'county.json' AND date >= watermark"
                    ),
                }
            )
            seen.add(rid)
        if len(reports) < PAGE_SIZE or scanned >= (total or 0):
            break
        offset += PAGE_SIZE
        time.sleep(SLEEP_S)

    if new_rows:
        with open(HITS_PATH, "a") as f:
            for row in new_rows:
                f.write(json.dumps(row) + "\n")

    now = datetime.now(timezone.utc).isoformat()
    state["seen_ids"] = sorted(seen)
    state["items_collected"] = state.get("items_collected", 0) + len(new_rows)
    state["last_sweep"] = now
    state["scanned_reports"] = total
    if "error" not in state.get("status", ""):
        state["status"] = "swept" if new_rows else "swept-no-new-hits"
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)

    print(
        json.dumps(
            {
                "scanned": total,
                "new_hits": len(new_rows),
                "items_collected": state["items_collected"],
                "status": state["status"],
                "watermark": watermark,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
