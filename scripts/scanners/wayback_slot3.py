#!/usr/bin/env python3
"""Slot-3 — Wayback CDX sweep of Tier-2/3 dead-drop and relay domains.

Rebuilt 2026-10-24 (A58): the A34/A51/A52 runner existed but was never
committed and was lost. This restores it as a committed script.

Passive, read-only. CDX via http://web.archive.org (port 80, per TOOLS.md).
Never-downgrade: baseline keeps max(prior high-water, sweep newest), so a
query-mode flip or index churn can never move the high-water backwards.
Header-aware CDX parsing (A51). New-URL capture bodies fetched for rows
newer than the high-water (A34 capture-content diffing).

Usage: wayback_slot3.py [--out <dir>]
Writes cdx-<domain>.json + slot3-deltas.json + slot3-sweep-stdout into <dir>
(default: data/lanes/general-hunt/raw/3/<UTC ts>/).
Baseline: scripts/scanners/state/wayback_slot3_baseline.json (updated in
place with never-downgrade semantics).
"""
from __future__ import annotations

import datetime
import gzip
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import USER_AGENT  # noqa: E402

REPO = os.path.expanduser("~/workspace/silent-locus")
BASELINE_PATH = os.path.join(REPO, "scripts/scanners/state/wayback_slot3_baseline.json")
CDX_BASE = "http://web.archive.org/cdx/search/cdx"  # port 80, NOT 443
FIELDS = "urlkey,timestamp,original,mimetype,statuscode,digest,length"
RETRY_SLEEPS = (60, 90)  # flaky backend: 45-90 s spacing per TOOLS.md

DOMAINS = [
    "telegra.ph", "paste.linuxiarz.pl", "pastebin.k4be.pl",
    "pastebin.tarcseh.me", "nervesocket.com", "pure.md", "anna.fyi",
    "jsonhero.io", "md.succ.ai", "jqp.vercel.app", "r.jina.ai",
    "api.cors.lol", "corsmirror.com", "allorigins.hexlet.app",
    "api.allorigins.win", "cors.bwa.workers.dev",
    "cors.hypnguyen.workers.dev", "cors-get-proxy.sirjosh.workers.dev",
    "test.cors.workers.dev", "cf-cors.findme-19.workers.dev",
    "cloudflare-cors-anywhere.hanpengchen.workers.dev",
    "www.proxymule.com", "webcrawlerapi.com",
]


def _get(url: str, binary: bool = False):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    if binary:
        return data
    return data.decode("utf-8")


def cdx(dom: str):
    """Fetch CDX rows for a domain; returns list of dicts or {'__error__': msg}."""
    params = {"url": dom, "matchType": "domain", "output": "json",
              "fl": FIELDS, "collapse": "urlkey", "limit": 2000}
    url = CDX_BASE + "?" + urllib.parse.urlencode(params)
    last_err = "unknown"
    for wait in (0,) + RETRY_SLEEPS:
        if wait:
            time.sleep(wait)
        try:
            rows = json.loads(_get(url))
            break
        except Exception as e:  # noqa: BLE001
            last_err = f"{type(e).__name__}: {e}"
    else:
        return {"__error__": last_err}
    if not rows or not rows[0]:
        return []
    hdr = rows[0]
    idx = {c: hdr.index(c) for c in ("timestamp", "original", "mimetype",
                                    "statuscode", "digest")}
    return [{c: r[idx[c]] for c in idx} for r in rows[1:]]


def fetch_capture_body(timestamp: str, original: str) -> bytes | None:
    """Fetch one archived capture body (id_ = original bytes)."""
    url = (f"http://web.archive.org/web/{timestamp}id_/"
           + urllib.parse.quote(original, safe=":/"))
    for wait in (0,) + RETRY_SLEEPS:
        if wait:
            time.sleep(wait)
        try:
            return _get(url, binary=True)
        except Exception:  # noqa: BLE001
            continue
    return None


def main() -> int:
    outdir = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--out" else os.path.join(
        REPO, "data/lanes/general-hunt/raw/3",
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    os.makedirs(outdir, exist_ok=True)
    baseline = json.load(open(BASELINE_PATH))["high_water"]

    deltas = []
    errors = {}
    now_newest = {}
    for dom in DOMAINS:
        rows = cdx(dom)
        if isinstance(rows, dict):
            errors[dom] = rows["__error__"]
            continue
        if rows:
            with open(os.path.join(outdir, f"cdx-{dom}.json"), "w") as f:
                json.dump(rows, f)
            newest = max(r["timestamp"] for r in rows if r["timestamp"])
            now_newest[dom] = newest
            hw = baseline.get(dom)
            if hw and newest > hw:
                newrows = [r for r in rows if r["timestamp"] > hw]
                deltas.append({"domain": dom, "high_water": hw,
                               "now": newest, "new_rows": newrows})
        else:
            now_newest[dom] = baseline.get(dom)
        time.sleep(3)

    # capture bodies for new rows (A34)
    bodies = os.path.join(outdir, "bodies")
    for d in deltas:
        for r in d["new_rows"]:
            body = fetch_capture_body(r["timestamp"], r["original"])
            if body:
                os.makedirs(bodies, exist_ok=True)
                slug = urllib.parse.quote(r["original"], safe="")[:80]
                with open(os.path.join(bodies, f"{d['domain']}__{slug}.raw"),
                          "wb") as f:
                    f.write(body)
            time.sleep(3)

    # never-downgrade: keep max(prior, sweep) (A52)
    for dom in DOMAINS:
        n = now_newest.get(dom)
        hw = baseline.get(dom)
        baseline[dom] = max([x for x in (n, hw) if x] or [None])

    json.dump({"updated": datetime.datetime.now(
        datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "note": "never-downgrade keeps preserved",
        "high_water": baseline}, open(BASELINE_PATH, "w"), indent=2)
    json.dump({"deltas": deltas, "errors": errors},
              open(os.path.join(outdir, "slot3-deltas.json"), "w"), indent=2)
    print("BASELINE_DOMAINS", len(DOMAINS))
    print("ERRORS", list(errors))
    print("DELTAS")
    for d in deltas:
        print("  ", d["domain"], d["high_water"], "->", d["now"],
              "new_rows=", len(d["new_rows"]))
        for r in d["new_rows"]:
            print("     ", r["timestamp"], r["statuscode"], r["mimetype"],
                  r["original"][:140])
    if not deltas:
        print("   none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
