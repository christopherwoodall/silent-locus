#!/usr/bin/env python3
"""
Shodan scan example: hunting exposed AI-harness panels.

This script demonstrates the Shodan query pattern used in the Cairn/Strix/Hermes
panel hunt. It counts matches, then pulls host details for triage.

Usage:
    PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin python3 shodan_scan_example.py

Requires: the custom.shodan credential (already stored).
"""

import json
import subprocess
import sys
import urllib.parse

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/templates/skill/bin")
from dynamic_credentials import url_with_surrogate_query_param

BASE = "https://api.shodan.io"
HOSTS = ["api.shodan.io"]

# Queries from the Cairn hunt (NorForge blog: norforge.com/blog/inside_cairn)
QUERIES = {
    "cairn_title": 'http.title:"Cairn"',
    "strix_title": 'http.title:"Strix"',
    "hermes_title": 'http.title:"Hermes"',  # broad, needs refinement
    "cairn_html": 'http.html:"Cairn"',
}


def call(path, params=None):
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    url = url_with_surrogate_query_param(url, "custom.shodan", allowed_hosts=HOSTS)
    r = subprocess.run(
        ["curl", "-s", "--max-time", "90", "-A", "muse-hunt/1.0", url],
        capture_output=True, text=True, timeout=100,
    )
    return json.loads(r.stdout)


def count(query):
    """Return total match count for a query."""
    data = call("/shodan/host/count", {"query": query})
    return data.get("total", 0)


def host(ip):
    """Return slim host details for triage."""
    data = call(f"/shodan/host/{urllib.parse.quote(ip)}")
    return {
        "ip": data.get("ip_str"),
        "org": data.get("org"),
        "isp": data.get("isp"),
        "asn": data.get("asn"),
        "ports": data.get("ports", []),
        "hostnames": data.get("hostnames", []),
        "last_update": data.get("last_update"),
    }


def main():
    print("=== Shodan query counts ===")
    for name, query in QUERIES.items():
        total = count(query)
        print(f"  {name:15s} {total:6d}  ({query})")

    # Example: pull details for a known host (Google DNS as a safe demo)
    print("\n=== Host detail example (8.8.8.8) ===")
    print(json.dumps(host("8.8.8.8"), indent=2))


if __name__ == "__main__":
    main()
