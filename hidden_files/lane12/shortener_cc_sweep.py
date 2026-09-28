#!/usr/bin/env python3
"""Shortener-stats Common Crawl slice: index query + WARC pull + per-row explosion.

Queued 2026-09-28 by the July-5-6 UNM retry lane (task item b). The lane12
supervisor launches this worker when index.commoncrawl.org recovers
(polled every 10 min through 2026-09-30 12:00 UTC).

Targets: the 5 goto.unm.edu YOURLS `+` stats pages
(7t6-o, discvr, reso, urphy21, vbudg) — exact URL index queries over the
crawls whose windows intersect 2026-06-01..2026-08-15, so any mid-July 2026
stats-page capture becomes a per-row evidence source for the July 5-6
referrer rows that the live YOURLS UI no longer exposes.

Complements (does not compete with) the shortener-cdx retry loop, which
covers the same URLs via Wayback CDX. Both workers append to the same
events JSONL with dedupe on labels.event_id.

STAGED ON DISK ONLY — hosted-Elastic writes are paused (2026-09-28 standing
rule). Read-only against index.commoncrawl.org / data.commoncrawl.org.
Polite pacing (2s between requests).

Resumable: hidden_files/lane12/state_shortener_cc.json tracks processed
(crawl, warc_filename, offset) records. Prints "DONE shortener-cc" to its
log on natural completion; supervisor greps for that line.
"""
import gzip
import hashlib
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", ".."))
OUTDIR = os.path.join(BASE, "data", "university-shorteners", "wayback-cc")
EVENTS_SCRIPT_DIR = os.path.join(BASE, "scripts")
STATE_PATH = os.path.join(BASE, "hidden_files", "lane12", "state_shortener_cc.json")
JOB_PATH = os.path.join(BASE, "hidden_files", "lane12", "shortener_cc_job.json")

PACE = 2.0
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

UA = {"User-Agent": "swarmtraces-research/1.0 (read-only archival research)"}


def log(msg):
    print("[%s] %s" % (datetime.now(timezone.utc).strftime("%H:%M:%S"), msg),
          flush=True)


def fetch(url, headers=None, timeout=60):
    h = dict(UA)
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_range(url, offset, length, timeout=120):
    return fetch(url, {"Range": "bytes=%d-%d" % (offset, offset + length - 1)},
                 timeout=timeout)


def job_spec():
    with open(JOB_PATH) as f:
        return json.load(f)


def select_crawls(job):
    """Crawls from collinfo whose window intersects job['window_from/to']."""
    raw = fetch("https://index.commoncrawl.org/collinfo.json").decode("utf-8")
    crawls = json.loads(raw)
    wf, wt = job["window_from"], job["window_to"]
    picked = []
    for c in crawls:
        name = c.get("id", "")
        cfrom, cto = c.get("from", ""), c.get("to", "")
        if wf <= cto and cfrom <= wt:
            picked.append(name)
    return sorted(set(picked))


def index_records(crawl_index, url):
    q = urllib.parse.urlencode({
        "url": url,
        "output": "json",
        "matchType": "exact",
        "filter": "status:200",
        "filter": "mime:text/html",
        "collapse": "digest",
    })
    # urlencode collapses duplicate keys; build manually
    q = ("url=%s&output=json&matchType=exact&filter=status%%3A200"
         "&filter=mime%%3Atext%%2Fhtml&collapse=digest"
         % urllib.parse.quote(url, safe=""))
    api = "https://index.commoncrawl.org/%s-index?%s" % (crawl_index, q)
    raw = fetch(api, timeout=120).decode("utf-8", errors="replace")
    recs = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        recs.append({
            "url": r.get("url"),
            "timestamp": r.get("timestamp"),
            "filename": r.get("filename"),
            "offset": int(r.get("offset", -1)),
            "length": int(r.get("length", -1)),
            "digest": r.get("digest"),
            "status": r.get("status"),
        })
    return [r for r in recs if r["offset"] >= 0 and r["length"] > 0 and r["filename"]]


def warc_payload(filename, offset, length):
    blob = fetch_range("https://data.commoncrawl.org/" + filename, offset, length)
    try:
        data = gzip.decompress(blob)
    except Exception:
        data = blob  # already plain (shouldn't happen for WARC segments)
    # split WARC headers from payload: first blank line ends WARC headers,
    # then HTTP response headers, then a blank line, then the body
    head_end = data.find(b"\r\n\r\n")
    if head_end < 0:
        head_end = data.find(b"\n\n")
        sep = b"\n\n"
    else:
        sep = b"\r\n\r\n"
    rest = data[head_end + len(sep):]
    # rest starts with HTTP status line + headers
    body_sep = rest.find(b"\r\n\r\n")
    if body_sep >= 0:
        return rest[body_sep + 4:]
    body_sep = rest.find(b"\n\n")
    if body_sep >= 0:
        return rest[body_sep + 2:]
    return rest


def load_state():
    if os.path.exists(STATE_PATH):
        try:
            return json.load(open(STATE_PATH))
        except Exception:
            pass
    return {"processed": []}


def save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=1)


def main():
    job = job_spec()
    os.makedirs(OUTDIR, exist_ok=True)
    state = load_state()
    processed = set(tuple(x) for x in state.get("processed", []))

    log("shortener-cc sweep starting (targets: %d urls)" % len(job["target_urls"]))
    crawls = select_crawls(job)
    log("crawls intersecting window: %s" % (", ".join(crawls) or "NONE"))
    if not crawls:
        log("no crawls in window; exiting for supervisor retry")
        return 1

    sys.path.insert(0, EVENTS_SCRIPT_DIR)
    sys.path.insert(0, os.path.join(BASE, "hidden_files", "shortener-cdx"))
    import build_shortener_events as bse
    import pull_and_explode as pae

    manifest = []
    evidence_files = []
    for crawl in crawls:
        for stats_url in job["target_urls"]:
            slug = job["slug_for_url"][stats_url]
            log("index %s :: %s" % (crawl, stats_url))
            try:
                time.sleep(PACE)
                recs = index_records(crawl, stats_url)
            except Exception as e:
                log("  index failed: %s" % e)
                continue
            log("  %d records" % len(recs))
            slugdir = os.path.join(OUTDIR, slug)
            os.makedirs(slugdir, exist_ok=True)
            for r in recs:
                key = (crawl, r["filename"], r["offset"])
                if tuple(key) in processed:
                    continue
                ts = r["timestamp"] or "unknown"
                fname = "%s_%s.html" % (crawl, ts)
                fpath = os.path.join(slugdir, fname)
                rel = os.path.relpath(fpath, BASE)
                if not os.path.exists(fpath):
                    try:
                        time.sleep(PACE)
                        payload = warc_payload(r["filename"], r["offset"], r["length"])
                    except Exception as e:
                        log("  warc fetch failed %s: %s" % (ts, e))
                        continue
                    with open(fpath, "wb") as f:
                        f.write(payload)
                sha = hashlib.sha256(open(fpath, "rb").read()).hexdigest()
                manifest.append("%s  %s" % (sha, rel))
                ev = pae.parse_stats_html(open(fpath, "rb").read(), stats_url)
                ev_doc = {
                    "slug": slug,
                    "source_url": stats_url,
                    "retrieved_at": ("%s-%s-%sT%s:%s:%sZ" % (
                        ts[0:4], ts[4:6], ts[6:8], ts[8:10], ts[10:12], ts[12:14])
                        if len(ts) >= 14 else NOW),
                    "retrieved_via": "commoncrawl index + WARC range fetch (read-only; hosted-Elastic writes paused)",
                    "long_url": None,
                    "created": None,
                    "traffic_summary": {},
                    "best_day": {},
                    "referrer_hosts": ev["referrer_hosts"],
                    "daily_all_time": [],
                    "daily_last_30": [],
                    "cc_crawl": crawl,
                    "cc_timestamp": ts,
                    "cc_filename": r["filename"],
                    "cc_offset": r["offset"],
                    "cc_digest": r["digest"],
                    "parse_note": ev["parse_note"],
                }
                ev_name = "%s_referrer_urls_daily_cc_%s_%s.json" % (slug, crawl, ts)
                ev_path = os.path.join(slugdir, ev_name)
                with open(ev_path, "w") as f:
                    json.dump(ev_doc, f, ensure_ascii=False, indent=1)
                manifest.append("%s  %s" % (
                    hashlib.sha256(open(ev_path, "rb").read()).hexdigest(),
                    os.path.relpath(ev_path, BASE)))
                evidence_files.append(ev_path)
                processed.add(tuple(key))
                save_state({"processed": sorted(processed)})
                log("  %s %s: %d referrer rows" % (crawl, ts, ev["parse_rows"]))

    with open(os.path.join(OUTDIR, "SHA256SUMS"), "w") as f:
        f.write("\n".join(sorted(set(manifest))) + "\n")
    with open(os.path.join(OUTDIR, "manifest.json"), "w") as f:
        json.dump({
            "built": NOW,
            "generator": "hidden_files/lane12/shortener_cc_sweep.py (queued by July-5-6 UNM retry lane)",
            "job": job,
            "evidence_files": [os.path.relpath(p, BASE) for p in evidence_files],
            "note": "Raw WARC payloads kept per capture. Evidence JSONs follow the "
                    "schema consumed by scripts/build_shortener_events.py. "
                    "Staged on disk only; hosted-Elastic writes paused.",
        }, f, indent=1)
    log("evidence files: %d" % len(evidence_files))

    docs = []
    for ev_path in evidence_files:
        try:
            docs += bse.explode_referrer_json(ev_path)
        except Exception as e:
            log("explode failed for %s: %s" % (ev_path, e))

    out_jsonl = os.path.join(BASE, "data", "university-shorteners-events",
                             "university-shorteners-events.jsonl")
    existing = set()
    if os.path.exists(out_jsonl):
        with open(out_jsonl) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        existing.add(json.loads(line)["labels"]["event_id"])
                    except Exception:
                        pass
    new_docs = [d for d in docs if d["labels"]["event_id"] not in existing]
    allowed = set(json.load(open(os.path.join(BASE, "notes", "gems-es-mapping.json")))["mappings"]["properties"])
    bad = set()
    for d in new_docs:
        bad |= (set(d.keys()) - allowed)
    if bad:
        log("SCHEMA VIOLATION (not writing): %s" % bad)
        return 1
    if new_docs:
        with open(out_jsonl, "a") as f:
            for d in new_docs:
                f.write(json.dumps(d, ensure_ascii=False) + "\n")
        log("appended %d new event docs (%d already present)" % (len(new_docs), len(docs) - len(new_docs)))
    else:
        log("no new event docs (all %d already present)" % len(docs))
    evdir = os.path.join(BASE, "data", "university-shorteners-events")
    sums = []
    for fn in ("university-shorteners-events.jsonl", "PROVENANCE.md"):
        p = os.path.join(evdir, fn)
        if os.path.exists(p):
            sums.append("%s  %s" % (hashlib.sha256(open(p, "rb").read()).hexdigest(), fn))
    with open(os.path.join(evdir, "SHA256SUMS"), "w") as f:
        f.write("\n".join(sums) + "\n")

    print("DONE shortener-cc crawls=%d evidence=%d new_docs=%d %s"
          % (len(crawls), len(evidence_files), len(new_docs), NOW))
    return 0


if __name__ == "__main__":
    sys.exit(main())
