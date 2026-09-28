#!/usr/bin/env python3
"""TEMPORAL PIVOT — Diffend version-date sweep over the 3,022 JFrog campaign names.

For each name: GET https://my.diffend.io/gems/<name>, parse all versions +
publish timestamps, flag any version dated OUTSIDE 2026-05-05..2026-07-07
(pre-wave, inter-wave gaps, post-July-7). Read-only, ~1 req/s, checkpointed.

Out: data/gem-temporal-pivot/diffend_temporal_sweep.jsonl
"""
import csv
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime

DIFFEND = "https://my.diffend.io"
UA = "rubygems-temporal-research/1.0 (read-only version-date sweep; no install)"
PACE = 1.0
LO = datetime(2026, 5, 5)
HI = datetime(2026, 7, 7, 23, 59, 59)

PROJ = os.path.expanduser("~/workspace/silent-locus")
CSV = os.path.join(PROJ, "data/gemstuffer-jfrog-2026-09-27.csv")
OUTDIR = os.path.join(PROJ, "data/gem-temporal-pivot")
OUT = os.path.join(OUTDIR, "diffend_temporal_sweep.jsonl")
os.makedirs(OUTDIR, exist_ok=True)

VER_PAT = re.compile(
    r"<a href='/gems/%s/([\d.]+(?:/[\d.]+)?)'>(.*?)</a>.*?([A-Z][a-z]+ \d+, \d+ [\d:]+)")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read().decode("utf-8", "ignore")
        time.sleep(PACE)
        return data, r.status
    except urllib.error.HTTPError as e:
        time.sleep(PACE)
        return None, e.code
    except Exception as e:
        time.sleep(2)
        return None, str(e)


def parse_ts(ts):
    for fmt in ("%B %d, %Y %H:%M", "%B %d, %Y"):
        try:
            return datetime.strptime(ts.strip(), fmt)
        except ValueError:
            pass
    return None


def gem_versions(name):
    h, st = get("%s/gems/%s" % (DIFFEND, name))
    if h is None or st != 200:
        return None, st
    vers = []
    # rebuild pattern with escaped name (finditer needs the name interpolated)
    pat = r"<a href='/gems/%s/([\d.]+(?:/[\d.]+)?)'>(.*?)</a>.*?([A-Z][a-z]+ \d+, \d+ [\d:]+)" % re.escape(name)
    for m in re.finditer(pat, h, re.S):
        for v in m.group(1).split("/"):
            ts = parse_ts(m.group(3))
            vers.append((v, m.group(3).strip(), ts.isoformat() if ts else None,
                         ts is not None and (ts < LO or ts > HI)))
    return vers, 200


def done_names():
    done = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            try:
                done.add(json.loads(line)["name"])
            except Exception:
                pass
    return done


def main():
    names = []
    with open(CSV, newline="") as f:
        for row in csv.DictReader(f):
            n = (row.get("Package") or "").strip()
            if n:
                names.append(n)
    done = done_names()
    todo = [n for n in names if n not in done]
    print("total %d, done %d, todo %d" % (len(names), len(done), len(todo)), flush=True)
    out = open(OUT, "a")
    hits = 0
    for i, name in enumerate(todo):
        vers, st = gem_versions(name)
        if vers is None:
            rec = {"name": name, "in_diffend": False, "http_status": st,
                   "versions": [], "out_of_window": []}
        else:
            oow = [{"version": v, "ts": ts, "ts_iso": iso}
                   for v, ts, iso, flag in vers if flag]
            if oow:
                hits += 1
            rec = {"name": name, "in_diffend": True, "http_status": 200,
                   "versions": [{"version": v, "ts": ts, "ts_iso": iso}
                                for v, ts, iso, flag in vers],
                   "out_of_window": oow}
        out.write(json.dumps(rec) + "\n")
        out.flush()
        if i % 100 == 0 or i == len(todo) - 1:
            print("%d/%d ... %s -> oow_hits=%d" % (i, len(todo), name, hits), flush=True)
    out.close()
    print("DONE oow_hits=%d" % hits, flush=True)


if __name__ == "__main__":
    main()
