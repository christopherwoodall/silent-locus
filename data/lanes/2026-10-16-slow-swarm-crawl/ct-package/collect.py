#!/usr/bin/env python3
"""Slow passive swarm crawl — CT + package registry tripwire (2026-10-16).

Passive only: public read APIs, low rate. Metadata only; no package
contents downloaded or executed.
"""
import hashlib
import json
import os
import re
import time
import urllib.parse
import urllib.request
import urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, "raw")
os.makedirs(RAW, exist_ok=True)

UA = {"User-Agent": "silent-locus-passive-crawl/2026-10-16 (+research)"}


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return -1, str(e).encode()


def store(name, url, body, note=""):
    path = os.path.join(RAW, name)
    if isinstance(body, str):
        body = body.encode()
    with open(path, "wb") as fh:
        fh.write(body)
    sha = hashlib.sha256(body).hexdigest()
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    prov = (
        f"source URL: {url}\n"
        f"retrieved_at_utc: {ts}\n"
        f"method: python urllib passive GET, {UA['User-Agent']}\n"
        f"sha256: {sha}\n"
        f"bytes: {len(body)}\n"
        f"note: {note}\n"
    )
    with open(os.path.join(RAW, name + ".PROVENANCE.txt"), "w") as fh:
        fh.write(prov)
    print(f"[stored] {name} ({len(body)} bytes, sha256={sha[:16]}...)")


def slug(q):
    return re.sub(r"[^a-z0-9]+", "_", q.lower()).strip("_")[:40]


def main():
    # ---- npm registry search API ----
    npm_queries = ["hysandbox", "uqscan", "uqframe", "uqtag",
                   "akbkyowd9geqr98", "swarm-agent", "agent-coordinator"]
    for q in npm_queries:
        url = ("https://registry.npmjs.org/-/v1/search?"
               f"text={urllib.parse.quote(q)}&size=20")
        status, body = fetch(url)
        store(f"npm_search_{slug(q)}.json", url, body,
              f"npm search, status={status}")
        time.sleep(1.5)

    # ---- RubyGems search API ----
    for q in ["hysandbox", "uqscan", "uqframe", "uqtag", "akbkyowd9geqr98"]:
        url = ("https://rubygems.org/api/v1/search.json?"
               f"query={urllib.parse.quote(q)}&page=1")
        status, body = fetch(url)
        store(f"rubygems_search_{slug(q)}.json", url, body,
              f"rubygems search, status={status}")
        time.sleep(1.5)

    # ---- PyPI recent-updates RSS ----
    url = "https://pypi.org/rss/updates.xml"
    status, body = fetch(url, timeout=90)
    store("pypi_rss_updates.xml", url, body, f"pypi RSS, status={status}")

    # ---- crt.sh targeted queries ----
    crt_queries = [
        "%hysandbox%",
        "%.serveo.net",
        "%.localhost.run",
        "%.bore.pub",
    ]
    for q in crt_queries:
        url = ("https://crt.sh/?q=" + urllib.parse.quote(q, safe="%")
               + "&output=json")
        status, body = fetch(url, timeout=120)
        note = f"crt.sh identity search, status={status}"
        if len(body) > 8_000_000:
            body = b""  # too big; record refusal rather than a truncated dump
            note = f"ABORTED: response too large, status={status}"
        store(f"crtsh_{slug(q)}.json", url, body, note)
        time.sleep(2.0)


if __name__ == "__main__":
    main()
