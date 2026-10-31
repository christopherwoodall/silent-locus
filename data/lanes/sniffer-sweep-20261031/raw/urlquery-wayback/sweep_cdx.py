#!/usr/bin/env python3
"""Wayback CDX sweep for sniffer-sweep-20261031 (urlquery-wayback lane).
Port 80 ONLY. Retries on flaky-backend failures with 60/90s spacing.
Saves sanitized rows: timestamp, domain, path (query string dropped),
status, mimetype, plus boolean token-presence flags computed BEFORE
truncation. No query-string values, no token values in any file.
CDX is a URL index only: it cannot search page content, so phrase
matching here covers URL-embedded tokens only.
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse

OUT = os.path.expanduser(
    "~/workspace/silent-locus/data/lanes/sniffer-sweep-20261031/raw/urlquery-wayback")
BASE = "http://web.archive.org/cdx/search/cdx"
FIELDS = "urlkey,timestamp,original,statuscode,mimetype"

QUERIES = [
    ("cdx-dagd-domain", {"url": "da.gd", "matchType": "domain",
                         "from": "20251101", "limit": "50",
                         "collapse": "urlkey"}),
    ("cdx-dagd-zz-filter", {"url": "da.gd", "matchType": "domain",
                            "from": "20251101", "limit": "50",
                            "collapse": "urlkey",
                            "filter": "original:.*zz=.*"}),
    ("cdx-swarmbar-domain", {"url": "swarmbar.com", "matchType": "domain",
                             "from": "20251101", "limit": "50",
                             "collapse": "urlkey"}),
    ("cdx-agentbadge-domain", {"url": "agentbadge.xyz", "matchType": "domain",
                               "from": "20251101", "limit": "50",
                               "collapse": "urlkey"}),
]


def fetch(params):
    q = urllib.parse.urlencode({**params, "output": "json", "fl": FIELDS})
    url = f"{BASE}?{q}"
    for attempt, sleep_s in enumerate([0, 60, 90]):
        if sleep_s:
            print(f"  retry sleep {sleep_s}s", flush=True)
            time.sleep(sleep_s)
        p = subprocess.run(["curl", "-sS", "-m", "120", url],
                           capture_output=True, text=True, timeout=150)
        body = p.stdout
        if "Temporarily Offline" in body or p.returncode != 0:
            print(f"  attempt {attempt}: flaky (rc={p.returncode})", flush=True)
            continue
        try:
            data = json.loads(body)
        except Exception:
            print(f"  attempt {attempt}: non-JSON ({body[:120]!r})", flush=True)
            continue
        return data
    return None


def sanitize(row):
    # row: [urlkey, timestamp, original, statuscode, mimetype]
    original = row[2] if len(row) > 2 else ""
    path = original.split("?", 1)[0].split("#", 1)[0]
    low = original.lower()
    return {
        "timestamp": row[1] if len(row) > 1 else "",
        "path_no_query": path,
        "status": row[3] if len(row) > 3 else "",
        "mimetype": row[4] if len(row) > 4 else "",
        "has_zz_param": "zz=" in low,
        "has_oai_token": bool(re.search(r"oai[-_]", low)),
        "has_agent_token": bool(re.search(
            r"spawn_agent|tooluseblock|thinkingblock|send_msg_to_user|"
            r"gbox-linux|function_call", low)),
        "has_query": "?" in original,
    }


def main():
    for slug, params in QUERIES:
        out_path = os.path.join(OUT, f"{slug}.json")
        if os.path.exists(out_path):
            print(f"SKIP {slug} (exists)", flush=True)
            continue
        print(f"QUERY {slug}: {params}", flush=True)
        data = fetch(params)
        if data is None:
            print(f"FAIL {slug}: all CDX attempts flaky", flush=True)
            with open(out_path, "w") as f:
                json.dump({"query": params, "error": "cdx flaky all attempts",
                           "rows": []}, f, indent=1)
            continue
        rows = data[1:] if data and data[0] == ["urlkey", "timestamp", "original",
                                                "statuscode", "mimetype"] else data
        recs = [sanitize(r) for r in rows if isinstance(r, list)]
        with open(out_path, "w") as f:
            json.dump({"query": params, "rows": recs}, f, indent=1)
        print(f"OK {slug}: {len(recs)} rows", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
