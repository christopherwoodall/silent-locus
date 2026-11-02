#!/usr/bin/env python3
"""One-shot cache-timing probe for r.jina.ai activity.

A cache-timing probe tests whether a third party recently proxied a URL
through Jina Reader (https://r.jina.ai/<target-url>). Jina caches proxied
pages. A page fetched recently returns fast and carries an extra
"Published Time:" line. A page not fetched recently returns slow and
lacks the line.

This is an analyst tool, not a monitor. Do not schedule it. Every probe
warms the URL itself, so a repeated check cannot tell "an agent fetched
this" from "we fetched this while checking". Use one shot per URL, only
when you have a reason to test that URL.

Usage:
    jina_cache_probe.py <inner-target-url> [--samples N] [--spacing S]

The inner target URL is the page you want to test, without the
r.jina.ai/ prefix. Example:

    jina_cache_probe.py "https://www.amap.com/place/B001234567"

Verdict rules (from the 2026-10-21 validation run, 15 samples):
  - Sample 1 fast (< 2.0s) WITH the Published Time marker:
    WARM. A third party proxied this URL recently (within the cache
    window, observed >= 14 minutes). This is the signal.
  - Sample 1 slow (>= 2.0s) without the marker, later samples fast with
    the marker: COLD at first touch. Nobody proxied it before us; we
    warmed it ourselves.
  - Anything else: INCONCLUSIVE. Rerun later by hand if it matters.

Evidence is written to
data/lanes/general-hunt/raw/cache-probe/<timestamp>/: full headers,
bodies, and a results.jsonl with one record per fetch. The tool also
appends the URL and verdict to probed_urls.jsonl in the same dir, and
refuses to re-probe a URL probed in the last 6 hours (a re-probe would
always read warm because of our own earlier probe).

Limits (honest):
  - Validated on a tiny static origin only (self-warm). Detecting another
    party's fetch is the same mechanism, but we have not yet caught one
    in the wild.
  - Timing needs repeated samples. One fetch cannot beat network noise.
  - Unauthenticated rate ceiling observed: 20 req/min. This tool stays
    far under it (3 fetches, 15 s apart).
  - Passive GETs only. No logins, no keys, no session creation.
"""
import argparse
import datetime
import json
import os
import subprocess
import sys
import time

BASE = os.path.expanduser(
    "~/workspace/silent-locus/data/lanes/general-hunt/raw/cache-probe")
LEDGER = os.path.join(BASE, "probed_urls.jsonl")
LEDGER_WINDOW_HOURS = 6
WARM_TIME_CUTOFF_S = 2.0  # validated: fastest cold 2.17s, slowest warm 1.85s
CACHE_KEYS = ("cache", "age", "via", "x-jina", "cdn", "cf-", "etag",
              "last-modified", "x-cache", "x-amz-cf", "surrogate")


def ledger_recent(target):
    """Return True if target was probed within the ledger window."""
    if not os.path.exists(LEDGER):
        return False
    cutoff = (datetime.datetime.now(datetime.timezone.utc)
              - datetime.timedelta(hours=LEDGER_WINDOW_HOURS))
    try:
        for line in open(LEDGER):
            rec = json.loads(line)
            if rec.get("target") == target:
                ts = datetime.datetime.fromisoformat(
                    rec["utc"].replace("Z", "+00:00"))
                if ts >= cutoff:
                    return True
    except (json.JSONDecodeError, KeyError, ValueError):
        pass
    return False


def fetch(jina_url, tag, D):
    hdr = os.path.join(D, "hdr_%s.txt" % tag)
    body = os.path.join(D, "body_%s.bin" % tag)
    utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        r = subprocess.run(
            ["curl", "-s", "-D", hdr, "-o", body, "-w",
             "%{time_total} %{time_starttransfer} %{http_code} "
             "%{size_download}", "--max-time", "90", jina_url],
            capture_output=True, text=True, timeout=120)
        tt, tst, code, size = r.stdout.strip().split()
        rec = {"url": jina_url, "attempt": tag, "utc": utc,
               "time_total": float(tt), "time_starttransfer": float(tst),
               "http_code": int(code), "size_download": int(size)}
    except Exception as e:
        rec = {"url": jina_url, "attempt": tag, "utc": utc,
               "time_total": -1.0, "time_starttransfer": -1.0,
               "http_code": -1, "size_download": -1,
               "error": str(e)}
        print("FETCH_ERROR %s: %s" % (tag, e), flush=True)
    cache = {}
    try:
        with open(hdr, errors="replace") as f:
            for line in f:
                if ":" in line:
                    k, v = line.split(":", 1)
                    kl = k.strip().lower()
                    if any(s in kl for s in CACHE_KEYS):
                        cache[kl] = v.strip()
    except FileNotFoundError:
        pass
    rec["cache_headers"] = cache
    try:
        with open(body, errors="replace") as f:
            rec["has_published_time"] = "Published Time" in f.read()
    except FileNotFoundError:
        rec["has_published_time"] = False
    with open(os.path.join(D, "results.jsonl"), "a") as f:
        f.write(json.dumps(rec) + "\n")
    print("[%s] total=%ss code=%s size=%s published_time=%s" % (
        tag, rec["time_total"], rec["http_code"], rec["size_download"],
        rec["has_published_time"]), flush=True)
    return rec


def verdict(recs):
    first = recs[0]
    if first["http_code"] != 200:
        return ("INCONCLUSIVE",
                "first fetch did not return 200 "
                "(code=%s)" % first["http_code"])
    if (first["time_total"] < WARM_TIME_CUTOFF_S
            and first["has_published_time"]):
        return ("WARM",
                "first fetch was already warm: %.2fs with the "
                "Published Time marker. A third party proxied this URL "
                "recently (within the cache window, observed >= 14 min)."
                % first["time_total"])
    rest = recs[1:]
    if (first["time_total"] >= WARM_TIME_CUTOFF_S
            and not first["has_published_time"]
            and rest
            and all(r["has_published_time"] and r["http_code"] == 200
                    for r in rest)):
        return ("COLD",
                "first fetch cold (%.2fs, no marker); later fetches warm. "
                "Nobody proxied this URL before us; we warmed it "
                "ourselves." % first["time_total"])
    return ("INCONCLUSIVE",
            "pattern did not match cold or warm. Do not trust a single "
            "run; rerun by hand later if this URL matters.")


def main():
    ap = argparse.ArgumentParser(
        description="One-shot jina cache-timing probe (analyst tool).")
    ap.add_argument("target", help="inner target URL to test (no r.jina.ai/ "
                                  "prefix)")
    ap.add_argument("--samples", type=int, default=3,
                    help="fetches per probe (default 3)")
    ap.add_argument("--spacing", type=int, default=15,
                    help="seconds between fetches (default 15)")
    args = ap.parse_args()

    target = args.target.strip()
    if target.startswith("https://r.jina.ai/"):
        print("Pass the INNER target URL, without the r.jina.ai/ prefix.",
              file=sys.stderr)
        sys.exit(1)
    if ledger_recent(target):
        print("Refusing: this URL was probed in the last %d hours. "
              "A re-probe would read warm because of our own earlier "
              "probe." % LEDGER_WINDOW_HOURS, file=sys.stderr)
        sys.exit(1)

    jina_url = "https://r.jina.ai/" + target
    ts = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H%M%SZ")
    D = os.path.join(BASE, ts)
    os.makedirs(D, exist_ok=True)
    with open(os.path.join(D, "PROVENANCE.txt"), "w") as f:
        f.write("Source: passive GETs to %s\n" % jina_url)
        f.write("Retrieved: %s (UTC), by jina_cache_probe.py\n"
                % datetime.datetime.now(datetime.timezone.utc).isoformat())
        f.write("Method: one-shot analyst probe; not scheduled.\n")
    print("RESULT_DIR=" + D, flush=True)
    print("TARGET=" + jina_url, flush=True)

    recs = []
    for n in range(1, args.samples + 1):
        r = fetch(jina_url, "s%d" % n, D)
        if r["http_code"] == 429:
            print("RATE LIMITED (429). Backing off; run incomplete.",
                  file=sys.stderr)
            break
        recs.append(r)
        if n < args.samples:
            time.sleep(args.spacing)

    label, note = verdict(recs) if recs else ("INCONCLUSIVE", "no fetches")
    print("VERDICT=%s" % label, flush=True)
    print(note, flush=True)

    entry = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "target": target, "jina_url": jina_url,
             "verdict": label, "note": note,
             "result_dir": D,
             "first_fetch_time": recs[0]["time_total"] if recs else None}
    with open(LEDGER, "a") as f:
        f.write(json.dumps(entry) + "\n")
    with open(os.path.join(D, "VERDICT.txt"), "w") as f:
        f.write("VERDICT: %s\n%s\n" % (label, note))
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
