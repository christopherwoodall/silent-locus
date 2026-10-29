#!/usr/bin/env python3
"""urlquery public API v1 CLI (authenticated via Secure Vault surrogate).

Usage:
    uq.py search --query QUERY [--limit N] [--offset N]
    uq.py report REPORT_ID
    uq.py overview REPORT_ID
    uq.py recent [--limit N]
    uq.py recent-domain DOMAIN [--limit N]

Outputs raw JSON to stdout. Never prints credentials.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/templates/skill/bin")
import dynamic_credentials as dc

BASE = "https://api.urlquery.net"
CRED = "custom.urlquery"
HOSTS = ["api.urlquery.net"]


def call(path):
    req = urllib.request.Request(BASE + path, headers={"Accept": "application/json"})
    dc.add_surrogate_to_request(req, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return dc.read_json_response(resp)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search")
    s.add_argument("--query", required=True)
    s.add_argument("--limit", type=int, default=30)
    s.add_argument("--offset", type=int, default=0)

    r = sub.add_parser("report")
    r.add_argument("report_id")

    o = sub.add_parser("overview")
    o.add_argument("report_id")

    rec = sub.add_parser("recent")
    rec.add_argument("--limit", type=int, default=30)

    rd = sub.add_parser("recent-domain")
    rd.add_argument("domain")
    rd.add_argument("--limit", type=int, default=30)

    a = ap.parse_args()
    try:
        if a.cmd == "search":
            q = urllib.parse.urlencode(
                {"query": a.query, "limit": a.limit, "offset": a.offset}
            )
            out = call(f"/public/v1/search/reports/?{q}")
        elif a.cmd == "report":
            out = call(f"/public/v1/report/{urllib.parse.quote(a.report_id, safe='')}")
        elif a.cmd == "overview":
            out = call(
                f"/public/v1/report/{urllib.parse.quote(a.report_id, safe='')}/overview"
            )
        elif a.cmd == "recent":
            out = call(f"/public/v1/recent/reports/?limit={a.limit}")
        elif a.cmd == "recent-domain":
            d = urllib.parse.quote(a.domain, safe="")
            out = call(f"/public/v1/recent/reports/domain/{d}?limit={a.limit}")
        print(json.dumps(out, indent=2))
    except Exception as e:  # noqa: BLE001 - surface as clean CLI error
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
