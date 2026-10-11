#!/usr/bin/env python3
"""Lane 3: Common Crawl CC-MAIN-2026-25 index sweep into openai-agent-traces corpus.

Candidate URLs are drawn from the committed arquivo-pt capture lists
(data/2026-10-01-arquivo-pt/raw/<slug>.cdx.jsonl.gz), which are READ-ONLY.
Selection per slug (deterministic, documented):
  1. read raw CDX lines, parse the original `url` field,
  2. dedupe preserving first-seen order,
  3. sort lexicographically, take the first 200 (cap).
Exact-URL index queries ONLY (wildcard queries 504 server-side per prior
probing). Polite rate: >=2s between API calls. Any block (429/403) stops the
run and is recorded. NO WARC downloads unless a hit justifies it (justification
recorded first - none yet; this run only stages index records).

Idempotent: queried URLs and seen (urlkey,timestamp) pairs live in
data/seen.json; re-run resumes and stages only new records.
"""
import gzip
import hashlib
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
RAW_DIR = os.path.join(ROOT, "data", "2026-10-01-arquivo-pt", "raw")
DATA_DIR = os.path.join(ROOT, "openai-agent-traces", "data")
OUT_FILE = os.path.join(DATA_DIR, "commoncrawl.jsonl")
SEEN_FILE = os.path.join(HERE, "data", "seen.json")
PROBE_LOG = os.path.join(HERE, "probe-log.jsonl")
STATE_FILE = os.path.join(HERE, "state.json")

CRAWL = "CC-MAIN-2026-25"          # 2026-06-05 -> 2026-06-18 per prior lanes
BASE = f"https://index.commoncrawl.org/{CRAWL}-index"
RATE_S = 2.0
CAP_PER_SLUG = 200

# eval_family mapping, only where task shape is verified by prior lanes:
# doe-crdc -> DeepSearchQA dsqa_250 (deepsearchqa lane, 2026-10-03).
EVAL_FAMILY_BY_SLUG = {
    "doe-crdc": "deepsearchqa",
}

SLUGS = [
    "bea-api", "calaccess", "doe-crdc", "illinois-iquery",
    "kansas-kansasmemory", "lac-collectionsearch", "maryland-edstats",
    "navy-history", "nysed-enrollment", "omb-max",
]


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def api_get(url):
    # 30s timeout: hanging requests are logged as failed and retried by a
    # later re-run (never marked queried), so a shorter timeout only costs
    # time, never data.
    req = urllib.request.Request(url, headers={"User-Agent": "silent-locus-research/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", "replace")[:500]
        except Exception:
            # error body itself unreadable (broken chunked encoding) -
            # return the status with empty body; caller treats a 404
            # without the "No Captures" marker as a transient failure
            body = ""
        return e.code, body
    except Exception as e:  # noqa: BLE001
        return 0, repr(e)


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def candidate_urls(slug):
    """Distinct URLs from the raw CDX file, lexicographically sorted, capped."""
    path = os.path.join(RAW_DIR, f"{slug}.cdx.jsonl.gz")
    seen = set()
    order = []
    raw_lines = 0
    if not os.path.exists(path):
        return order, 0, False
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            raw_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                doc = json.loads(line)
            except Exception:  # noqa: BLE001
                continue
            u = doc.get("url")
            if u and u not in seen:
                seen.add(u)
                order.append(u)
    order.sort()
    return order[:CAP_PER_SLUG], len(seen), True


def parse_cc_ts(t):
    # "20260617201637" -> ISO-8601 UTC
    try:
        dt = datetime.strptime(t, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:  # noqa: BLE001
        return "1970-01-01T00:00:00Z"


def map_record(hit, slug):
    ts = parse_cc_ts(hit.get("timestamp"))
    urlkey = hit.get("urlkey", "")
    digest = hit.get("digest", "")
    url = hit.get("url", "")
    labels = {
        "cc.crawl": CRAWL,
        "cc.urlkey": urlkey,
        "cc.status": str(hit.get("status", "")),
        "cc.mimetype": hit.get("mime") or hit.get("mimetype") or "",
        "cc.digest": digest,
        "cc.warc_file": hit.get("filename", ""),
        "cc.offset": hit.get("offset", ""),
        "cc.length": hit.get("length", ""),
        "cc.capture_timestamp": hit.get("timestamp", ""),
        "source.slug": slug,
        "retrieved_from": "Common Crawl index API",
    }
    if slug in EVAL_FAMILY_BY_SLUG:
        labels["attribution.eval_family"] = EVAL_FAMILY_BY_SLUG[slug]
    if ts.startswith("1970"):
        labels["timestamp_source"] = "fallback:no_recoverable_date"
    rec = {
        "@timestamp": ts,
        "event": {"dataset": "openai-agent-traces", "created": now_utc()},
        "record_kind": "commoncrawl_index_record",
        "fingerprint": sha(f"cc:{CRAWL}:{urlkey}:{hit.get('timestamp', '')}:{digest}"),
        "labels": labels,
        "title": f"Common Crawl {CRAWL} capture: {url}",
        "description": (f"{CRAWL} index record for arquivo.pt-captured URL {url} "
                        f"@ {ts} ({labels['cc.mimetype']}/{labels['cc.status']})"),
        "source_url": url,
        "retrieved_at": now_utc(),
        "retrieved_via": "commoncrawl-index-api",
        "file": f"data/2026-10-01-arquivo-pt/raw/{slug}.cdx.jsonl.gz",
        "observer": {"product": "Common Crawl Index API", "vendor": "Common Crawl", "type": "service"},
        "tags": ["commoncrawl", CRAWL, "sweep-2026-10-03", slug],
        "confidence": "high",
        "note": ("Index-record hit only; no WARC downloaded. attribution.provider not set "
                 "(no direct evidence). WARC fetch would need a recorded justification."),
    }
    return rec


def probe_log(entry):
    with open(PROBE_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return json.load(f)
    return {"urlscan_uuids": [], "cc_urls_queried": [], "cc_index_pairs": []}


def save_seen(seen):
    os.makedirs(os.path.dirname(SEEN_FILE), exist_ok=True)
    tmp = SEEN_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump({
            "urlscan_uuids": sorted(seen.get("urlscan_uuids", [])),
            "cc_urls_queried": sorted(seen.get("cc_urls_queried", [])),
            "cc_index_pairs": sorted(seen.get("cc_index_pairs", [])),
        }, f, indent=1)
    os.replace(tmp, SEEN_FILE)


def checkpoint(seen, queried, pairs):
    seen["cc_urls_queried"] = sorted(queried)
    seen["cc_index_pairs"] = sorted(pairs)
    save_seen(seen)


def update_state(patch):
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            state = json.load(f)
    state.update(patch)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=1)


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    seen = load_seen()
    queried = set(seen.get("cc_urls_queried", []))
    pairs = set(seen.get("cc_index_pairs", []))
    slug_report = []
    new_records = 0
    blocked = None
    for slug in SLUGS:
        urls, distinct, ok = candidate_urls(slug)
        to_query = [u for u in urls if u not in queried]
        hits_staged = 0
        failed = 0
        error = None
        for u in to_query:
            qurl = BASE + "?url=" + urllib.parse.quote(u, safe="") + "&output=json"
            status, body = api_get(qurl)
            if status in (429, 403):
                # genuinely blocked: do NOT mark queried, stop everything
                failed += 1
                error = f"blocked:http_{status}"
                probe_log({"ts": now_utc(), "api": BASE, "slug": slug,
                           "url": u, "hits": 0, "error": error})
                break
            if status == 200:
                # definitive answer (may be "No Captures found" -> zero hits)
                queried.add(u)
                n = 0
                for line in body.splitlines():
                    line = line.strip()
                    if not line or line.startswith('{"message"'):
                        continue
                    try:
                        hit = json.loads(line)
                    except Exception:  # noqa: BLE001
                        continue
                    pair = f"{hit.get('urlkey','')}|{hit.get('timestamp','')}"
                    if pair in pairs:
                        continue
                    rec = map_record(hit, slug)
                    with open(OUT_FILE, "a") as f:
                        f.write(json.dumps(rec) + "\n")
                    pairs.add(pair)
                    n += 1
                    new_records += 1
                hits_staged += n
                probe_log({"ts": now_utc(), "api": BASE, "slug": slug,
                           "url": u, "hits": n, "error": None})
            elif status == 404 and "No Captures found" in body:
                # definitive zero: CC index 404s on exact-URL queries with no captures
                queried.add(u)
                probe_log({"ts": now_utc(), "api": BASE, "slug": slug,
                           "url": u, "hits": 0, "error": None})
            else:
                # transient server failure (502/504/http_0/...): do NOT mark
                # queried, so a later re-run retries it
                failed += 1
                error = f"error:http_{status}"
                probe_log({"ts": now_utc(), "api": BASE, "slug": slug,
                           "url": u, "hits": 0, "error": error})
            time.sleep(RATE_S)
            if (hits_staged + failed) % 25 == 0:
                checkpoint(seen, queried, pairs)
        slug_report.append({
            "slug": slug, "raw_file_ok": ok, "distinct_urls": distinct,
            "cap_applied": CAP_PER_SLUG, "urls_queried_this_run": len(to_query),
            "hits_staged_new": hits_staged, "failed_queries": failed,
            "error": error,
        })
        checkpoint(seen, queried, pairs)  # per-slug checkpoint: survives interruption
        if error and error.startswith("blocked"):
            blocked = error
            break
    save_seen({"urlscan_uuids": seen.get("urlscan_uuids", []),
               "cc_urls_queried": sorted(queried),
               "cc_index_pairs": sorted(pairs)})
    update_state({
        "lane": "urlscan-cc-feeds",
        "commoncrawl": {
            "crawl": CRAWL,
            "slugs_completed": len(slug_report),
            "urls_queried_total": len(queried),
            "index_pairs_staged_total": len(pairs),
            "records_staged_new_this_run": new_records,
            "output": "openai-agent-traces/data/commoncrawl.jsonl",
            "blocked": blocked,
            "selection_method": ("distinct URLs per slug from read-only raw CDX lists, "
                                 "lexicographically sorted, first 200 taken (cap). "
                                 "Exact-URL queries only."),
            "warc_downloads": 0,
            "warc_justifications": [],
            "last_run_utc": now_utc(),
        },
        "status": "complete" if not blocked else "cc-blocked",
        "updated_utc": now_utc(),
    })
    print(json.dumps({"slugs": slug_report, "new_records": new_records, "blocked": blocked}, indent=1))


if __name__ == "__main__":
    main()
