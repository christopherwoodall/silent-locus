#!/usr/bin/env python3
"""Resume the 2026-09-28 Diffend temporal sweep (3,025 campaign gem names).

Reads names from the campaign CSV, skips names already present in
data/2026-09-29-gem-temporal-pivot/events.jsonl (file_origin in
{gem-temporal-pivot-diffend-temporal-sweep.jsonl, diffend_temporal_sweep_resume.py}),
and appends schema-valid diffend_probe rows DIRECTLY to events.jsonl
(checkpoint = the file itself; safe to re-run after interruption).

Key fix vs the 2026-09-28 run: fetch via `curl` (its TLS fingerprint is
accepted by my.diffend.io; Python urllib's is dropped) with a stock browser
UA. Read-only GETs, ~1.5s pace, manual retry with backoff on failures.

Out: appends to data/2026-09-29-gem-temporal-pivot/events.jsonl
Log:  data/2026-09-29-gem-temporal-pivot/raw/run-logs/diffend_temporal_sweep_resume.stdout.log
"""
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
DIFFEND = "https://my.diffend.io"
PACE = 1.5
RETRIES = 3
BACKOFF = (5, 15, 45)
LO = datetime(2026, 5, 5)
HI = datetime(2026, 7, 7, 23, 59, 59)

PROJ = os.path.expanduser("~/workspace/silent-locus")
CSV = os.path.join(PROJ, "data/2025-03-04-rubygems-goimport-campaign/raw/gemstuffer-jfrog-2026-09-27.csv")
COL = os.path.join(PROJ, "data/2026-09-29-gem-temporal-pivot")
EVENTS = os.path.join(COL, "events.jsonl")
LOGDIR = os.path.join(COL, "raw", "run-logs")
os.makedirs(LOGDIR, exist_ok=True)
LOG = os.path.join(LOGDIR, "diffend_temporal_sweep_resume.stdout.log")

FILE_ORIGIN = "diffend_temporal_sweep_resume.py"
DONE_ORIGINS = {"gem-temporal-pivot-diffend-temporal-sweep.jsonl", FILE_ORIGIN}

VER_PAT_TMPL = (r"<a href='/gems/%s/([\d.]+(?:/[\d.]+)?)'>\s*(.*?)\s*</a>"
                r".*?([A-Z][a-z]+ \d+, \d+ [\d:]+)")


def log(msg):
    line = "%s %s" % (datetime.now(timezone.utc).isoformat(timespec="seconds"), msg)
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def curl_get(url):
    """Return (html, http_code, final_url, error_str)."""
    out = "/tmp/diffend_resume_body.html"
    cmd = ["curl", "-sL", "-A", UA, "--max-time", "60", "-o", out,
           "-w", "%{http_code}\n%{url_effective}", url]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=75)
    except Exception as e:
        return None, None, None, "curl failed: %s" % e
    parts = (p.stdout or "").strip().split("\n")
    if len(parts) < 2:
        err = (p.stderr or "").strip()[:200] or "curl wrote no metadata"
        return None, None, None, err
    try:
        html = open(out).read()
    except Exception as e:
        return None, None, None, "body unreadable: %s" % e
    return html, parts[0], parts[1], None


def parse_ts(ts):
    for fmt in ("%B %d, %Y %H:%M", "%B %d, %Y"):
        try:
            return datetime.strptime(ts.strip(), fmt)
        except ValueError:
            pass
    return None


def probe(name):
    """One gem: fetch, parse versions. Returns record dict (raw)."""
    url = "%s/gems/%s" % (DIFFEND, name)
    last_err = None
    for attempt in range(RETRIES):
        html, code, final, err = curl_get(url)
        if err is None:
            break
        last_err = err
        log("retry %d/%d %s: %s" % (attempt + 1, RETRIES, name, err))
        time.sleep(BACKOFF[attempt] if attempt < len(BACKOFF) else 60)
    else:
        return {"name": name, "in_diffend": False,
                "http_status": "fetch-failed: %s" % (last_err or "unknown"),
                "versions": [], "out_of_window": [], "failed": True}
    if code != "200":
        return {"name": name, "in_diffend": False,
                "http_status": code, "versions": [], "out_of_window": [],
                "failed": True, "note": "non-200"}
    if final.rstrip("/") == DIFFEND + "/gems":
        # Diffend 302s unknown gems to the gems index page.
        return {"name": name, "in_diffend": False, "http_status": "302",
                "versions": [], "out_of_window": [],
                "redirect_target": DIFFEND + "/gems"}
    pat = re.compile(VER_PAT_TMPL % re.escape(name), re.S)
    vers = []
    for m in pat.finditer(html):
        for v in m.group(1).split("/"):
            ts = parse_ts(m.group(3))
            vers.append({"version": v, "ts": m.group(3).strip(),
                         "ts_iso": ts.isoformat() if ts else None,
                         "out_of_window": ts is not None and (ts < LO or ts > HI)})
    oow = [{"version": v["version"], "ts": v["ts"], "ts_iso": v["ts_iso"]}
           for v in vers if v["out_of_window"]]
    return {"name": name, "in_diffend": True, "http_status": "200",
            "versions": [{"version": v["version"], "ts": v["ts"], "ts_iso": v["ts_iso"]}
                         for v in vers],
            "out_of_window": oow}


def backfill(rec):
    name = rec["name"]
    fp = hashlib.sha256(("diffend_temporal_sweep|" + name).encode()).hexdigest()
    labels = {
        "gem.name": name,
        "in_diffend": rec["in_diffend"],
        "http_status": rec["http_status"],
        "versions": json.dumps(rec["versions"]),
        "out_of_window": json.dumps(rec["out_of_window"]),
        "timestamp_source": "fallback:no_recoverable_date",
        "file_origin": FILE_ORIGIN,
    }
    if rec.get("failed"):
        labels["ok"] = False
        labels["status"] = rec["http_status"]
    if rec.get("redirect_target"):
        labels["redirect_target"] = rec["redirect_target"]
    return {
        "@timestamp": "1970-01-01T00:00:00Z",
        "event": {"dataset": "2026-09-29-gem-temporal-pivot",
                  "created": datetime.now(timezone.utc).isoformat()},
        "record_kind": "diffend_probe",
        "fingerprint": fp,
        "labels": labels,
    }


def done_names():
    done = set()
    if os.path.exists(EVENTS):
        for line in open(EVENTS):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            lab = r.get("labels", {})
            if lab.get("file_origin") in DONE_ORIGINS and lab.get("gem.name"):
                done.add(lab["gem.name"])
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
    log("total %d, done %d, todo %d" % (len(names), len(done), len(todo)))
    if not todo:
        log("DONE nothing to do")
        return
    out = open(EVENTS, "a")
    hits = 0
    fails = 0
    for i, name in enumerate(todo):
        rec = probe(name)
        if rec.get("failed"):
            fails += 1
        elif rec["out_of_window"]:
            hits += 1
        out.write(json.dumps(backfill(rec)) + "\n")
        out.flush()
        time.sleep(PACE)
        if i % 50 == 0 or i == len(todo) - 1:
            log("%d/%d ... %s -> oow_hits=%d fetch_fail=%d" % (i, len(todo), name, hits, fails))
    out.close()
    log("DONE oow_hits=%d fetch_fail=%d" % (hits, fails))


if __name__ == "__main__":
    main()
