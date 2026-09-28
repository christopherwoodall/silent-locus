#!/usr/bin/env python3
"""Shortener-stats Wayback slice: CDX pull + per-row explosion, staged to disk.

Standing retry worker (launched by shortener_cdx_retry.sh). When the Wayback
CDX backend is reachable, pulls archived captures of 12 shortener stats-page
URLs (May-Jul 2026 priority, all captures kept), saves raw HTML with SHA-256
manifests, parses each capture into the evidence-JSON schema consumed by
scripts/build_shortener_events.py, and re-runs that script to append explicit
per-event docs to data/university-shorteners-events/.

STAGED ON DISK ONLY — hosted-Elastic writes are paused (2026-09-28 standing
rule). No es_ingest calls, no index creates, no deletes.

Read-only against web.archive.org. Polite pacing (2s between requests).
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", ".."))
OUTDIR = os.path.join(BASE, "data", "university-shorteners", "wayback")
EVENTS_SCRIPT = os.path.join(BASE, "scripts", "build_shortener_events.py")

# (instance, slug, stats_url) — the 12 stats-page URLs (UNCLAIMED slice:
# lane12's wb_sweep.py covers gem pages only, not shortener stats URLs)
TARGETS = [
    ("goto.unm.edu",   "7t6-o",      "https://goto.unm.edu/7t6-o+"),
    ("goto.unm.edu",   "discvr",     "https://goto.unm.edu/discvr+"),
    ("goto.unm.edu",   "reso",       "https://goto.unm.edu/reso+"),
    ("goto.unm.edu",   "urphy21",    "https://goto.unm.edu/urphy21+"),
    ("goto.unm.edu",   "vbudg",      "https://goto.unm.edu/vbudg+"),
    ("u.ethz.ch",      "nB1nv",      "https://u.ethz.ch/nB1nv+"),
    ("url.popcat.xyz", "5vtSk2RG2f", "https://url.popcat.xyz/5vtSk2RG2f/info"),
    ("url.popcat.xyz", "IRZTIxDlZ",  "https://url.popcat.xyz/IRZTIxDlZ/info"),
    ("go.uvm.edu",     "-4s0q",      "https://go.uvm.edu/-4s0q+"),
    ("go.uvm.edu",     "tgmtq",      "https://go.uvm.edu/tgmtq+"),
    ("go.uvm.edu",     "xc26",       "https://go.uvm.edu/xc26+"),
    ("vanderbi.lt",    "agentdamacosh777", "https://vanderbi.lt/agentdamacosh777+"),
]

CDX = "https://web.archive.org/cdx/search/cdx"
PACE = 2.0
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg):
    print("[%s] %s" % (datetime.now(timezone.utc).strftime("%H:%M:%S"), msg),
          flush=True)


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "swarmtraces-research/1.0 (read-only archival research)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def cdx_captures(stats_url):
    q = urllib.parse.urlencode({
        "url": stats_url,
        "output": "json",
        "fl": "timestamp,original,statuscode,digest",
        "filter": "statuscode:200",
        "collapse": "digest",
    })
    raw = fetch(CDX + "?" + q).decode("utf-8", errors="replace")
    rows = json.loads(raw)
    if not rows or rows[0][0] != "timestamp":
        return []
    out = []
    for r in rows[1:]:
        out.append({"timestamp": r[0], "original": r[1], "digest": r[3]})
    # May-Jul 2026 priority, then everything else, newest first within group
    def prio(c):
        return (0 if c["timestamp"].startswith(("202605", "202606", "202607")) else 1,
                c["timestamp"])
    return sorted(out, key=prio)


class ReferrerTableParser(HTMLParser):
    """Best-effort YOURLS 'Traffic sources' table extractor.

    Strategy: within each <tr>, collect anchor hrefs (absolute http URLs)
    and integers; a row with >=1 URL and >=1 integer yields (url, hits)
    pairs using the largest integer in the row as the hit count.
    """
    def __init__(self):
        super().__init__()
        self.in_tr = False
        self.row_urls = []
        self.row_ints = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.in_tr = True
            self.row_urls, self.row_ints = [], []
        elif tag == "a" and self.in_tr:
            for k, v in attrs:
                if k == "href" and v.startswith(("http://", "https://")):
                    self.row_urls.append(v)

    def handle_endtag(self, tag):
        if tag == "tr" and self.in_tr:
            self.in_tr = False
            if self.row_urls and self.row_ints:
                hits = max(self.row_ints)
                for u in self.row_urls:
                    self.rows.append((u, hits))
            self.row_urls, self.row_ints = [], []

    def handle_data(self, data):
        if self.in_tr:
            for m in re.finditer(r"\b(\d{1,7})\b", data.replace(",", "")):
                self.row_ints.append(int(m.group(1)))


def parse_stats_html(html, source_url):
    """-> evidence dict in the schema build_shortener_events.py consumes."""
    text = html.decode("utf-8", errors="replace") if isinstance(html, bytes) else html
    p = ReferrerTableParser()
    try:
        p.feed(text)
    except Exception:
        pass
    # group rows by host, keep max hits per (host, url)
    per_host = {}
    for url, hits in p.rows:
        try:
            host = urllib.parse.urlparse(url).netloc.lower()
        except Exception:
            continue
        if not host or host in ("goto.unm.edu", "u.ethz.ch", "go.uvm.edu",
                                "url.popcat.xyz", "vanderbi.lt", "web.archive.org"):
            continue  # skip self-links / archive chrome
        per_host.setdefault(host, {})
        per_host[host][url] = max(hits, per_host[host].get(url, 0))
    referrer_hosts = []
    for host in sorted(per_host):
        urls = [{"url": u, "hits": h} for u, h in
                sorted(per_host[host].items(), key=lambda kv: -kv[1])]
        referrer_hosts.append({
            "host": host,
            "total_hits": sum(u["hits"] for u in urls),
            "url_count": len(urls),
            "urls": urls,
        })
    return {
        "referrer_hosts": referrer_hosts,
        "parse_note": ("table-row parse, %d rows" % sum(len(h["urls"]) for h in referrer_hosts)
                       if referrer_hosts else "no referrer rows parsed from this capture"),
        "parse_rows": sum(len(h["urls"]) for h in referrer_hosts),
    }


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    manifest = []
    evidence_files = []
    total_captures = 0
    for instance, slug, stats_url in TARGETS:
        log("CDX: %s" % stats_url)
        try:
            caps = cdx_captures(stats_url)
        except Exception as e:
            log("  CDX failed: %s" % e)
            continue
        log("  %d captures" % len(caps))
        slugdir = os.path.join(OUTDIR, slug)
        os.makedirs(slugdir, exist_ok=True)
        for c in caps:
            ts = c["timestamp"]
            fname = "%s.html" % ts
            fpath = os.path.join(slugdir, fname)
            rel = os.path.relpath(fpath, BASE)
            if not os.path.exists(fpath):
                dl = "https://web.archive.org/web/%sid_/%s" % (ts, c["original"])
                try:
                    time.sleep(PACE)
                    raw = fetch(dl)
                except Exception as e:
                    log("  download failed %s: %s" % (ts, e))
                    continue
                with open(fpath, "wb") as f:
                    f.write(raw)
            sha = hashlib.sha256(open(fpath, "rb").read()).hexdigest()
            manifest.append("%s  %s" % (sha, rel))
            total_captures += 1
            # parse -> evidence JSON in the build_shortener_events.py schema
            ev = parse_stats_html(open(fpath, "rb").read(), stats_url)
            ev_doc = {
                "slug": slug,
                "source_url": stats_url,
                "retrieved_at": "%s-%s-%sT%s:%s:%sZ" % (ts[0:4], ts[4:6], ts[6:8], ts[8:10], ts[10:12], ts[12:14]),
                "retrieved_via": "wayback CDX archived capture (read-only; hosted-Elastic writes paused)",
                "long_url": None,
                "created": None,
                "traffic_summary": {},
                "best_day": {},
                "referrer_hosts": ev["referrer_hosts"],
                "daily_all_time": [],
                "daily_last_30": [],
                "wayback_timestamp": ts,
                "wayback_original": c["original"],
                "wayback_digest": c["digest"],
                "parse_note": ev["parse_note"],
            }
            ev_name = "%s_referrer_urls_daily_wayback_%s.json" % (slug, ts)
            ev_path = os.path.join(slugdir, ev_name)
            with open(ev_path, "w") as f:
                json.dump(ev_doc, f, ensure_ascii=False, indent=1)
            manifest.append("%s  %s" % (
                hashlib.sha256(open(ev_path, "rb").read()).hexdigest(),
                os.path.relpath(ev_path, BASE)))
            evidence_files.append(ev_path)
            log("  %s: %d referrer rows (%s)" % (ts, ev["parse_rows"],
                                                "parsed" if ev["parse_rows"] else "raw-only"))
    # manifest
    with open(os.path.join(OUTDIR, "SHA256SUMS"), "w") as f:
        f.write("\n".join(sorted(set(manifest))) + "\n")
    minfo = {
        "built": NOW,
        "generator": "hidden_files/shortener-cdx/pull_and_explode.py (standing wayback retry)",
        "targets": [{"instance": i, "slug": s, "stats_url": u} for i, s, u in TARGETS],
        "captures_downloaded": total_captures,
        "evidence_files": [os.path.relpath(p, BASE) for p in evidence_files],
        "note": "Raw HTML kept per capture (capture-first). Evidence JSONs follow the "
                "schema consumed by scripts/build_shortener_events.py. Staged on disk only; "
                "hosted-Elastic writes paused.",
    }
    with open(os.path.join(OUTDIR, "manifest.json"), "w") as f:
        json.dump(minfo, f, indent=1)
    log("captures=%d evidence=%d" % (total_captures, len(evidence_files)))

    # explode per-row via the canonical script (import, not subprocess, so its
    # hardcoded inputs stay untouched; we call explode_referrer_json directly)
    sys.path.insert(0, os.path.join(BASE, "scripts"))
    import build_shortener_events as bse
    import importlib
    importlib.reload(bse)
    docs = []
    for ev_path in evidence_files:
        try:
            docs += bse.explode_referrer_json(ev_path)
        except Exception as e:
            log("explode failed for %s: %s" % (ev_path, e))
    # dedupe on event_id against the existing events jsonl, then append
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
    # schema check (same as canonical script)
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
    # re-verify SHA256SUMS of the events dir
    evdir = os.path.join(BASE, "data", "university-shorteners-events")
    sums = []
    for fn in ("university-shorteners-events.jsonl", "PROVENANCE.md"):
        p = os.path.join(evdir, fn)
        if os.path.exists(p):
            sums.append("%s  %s" % (hashlib.sha256(open(p, "rb").read()).hexdigest(), fn))
    with open(os.path.join(evdir, "SHA256SUMS"), "w") as f:
        f.write("\n".join(sums) + "\n")
    # DONE marker
    with open(os.path.join(OUTDIR, "DONE"), "w") as f:
        f.write("completed %s UTC; captures=%d new_event_docs=%d\n" % (NOW, total_captures, len(new_docs)))
    log("DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
