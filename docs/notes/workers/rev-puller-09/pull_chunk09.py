#!/usr/bin/env python3
"""Revision puller for wikipedia-top500 chunk-09 (rev-puller-09).
Pulls revision history (2020-01-01 -> 2026-10-07) for each article via
MediaWiki API, paginating on continue.rvcontinue.
HTTP is done exclusively via curl subprocess (Python HTTP stacks break on
the egress proxy). Pacing: >=5.2s between requests to en.wikipedia.org.
UA: silent-locus-top500-scan/1.0 (research).
Never stops the chunk on one failure: failures are logged and the chunk continues.
"""
import json
import os
import subprocess
import sys
import time
import urllib.parse

UA = "silent-locus-top500-scan/1.0 (research)"
PACE = 5.2
RVSTART = "2026-10-07T00:00:00Z"
RVEND = "2020-01-01T00:00:00Z"
RV_LIMIT = 500

ROOT = os.path.expanduser("~/workspace/silent-locus-top500")
RAW = os.path.join(ROOT, "data/2026-10-06-wikipedia-top500-infra-scan/raw")
CHUNK = os.path.join(RAW, "chunks/chunk-09")
REVDIR = os.path.join(RAW, "revisions")
WORKDIR = os.path.join(ROOT, "workers/rev-puller-09")
ERRLOG = os.path.join(ROOT, "workers/rev-puller-10/errors.log")
PROGLOG = os.path.join(WORKDIR, "progress.log")


def log(msg):
    line = "[%s] %s" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), msg)
    print(line, flush=True)
    with open(PROGLOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def log_error(article, rank, reason):
    line = "[%s] rank=%s article=%r FAIL: %s" % (
        time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), rank, article, reason)
    with open(ERRLOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    log("ERROR: " + line)


def curl_json(url):
    """Single curl GET; returns parsed JSON or raises."""
    p = subprocess.run(
        ["curl", "-sS", "--max-time", "90", "-A", UA, url],
        capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        raise RuntimeError("curl exit %d: %s" % (p.returncode, p.stderr.strip()[:300]))
    try:
        return json.loads(p.stdout)
    except Exception as e:
        raise RuntimeError("bad JSON (%s): %.200s" % (e, p.stdout))


def fetch_page(title_enc, rvcontinue=None, retries=4):
    params = {
        "action": "query",
        "prop": "revisions",
        "titles": None,  # appended raw (already encoded)
        "rvprop": "user|timestamp|ids|comment|tags|size",
        "rvlimit": str(RV_LIMIT),
        "rvdir": "older",
        "rvstart": RVSTART,
        "rvend": RVEND,
        "format": "json",
        "formatversion": "2",
    }
    q = "&".join("%s=%s" % (k, urllib.parse.quote(str(v), safe=""))
                 for k, v in params.items() if v is not None)
    q += "&titles=" + title_enc
    if rvcontinue:
        q += "&rvcontinue=" + urllib.parse.quote(rvcontinue, safe="")
    url = "https://en.wikipedia.org/w/api.php?" + q
    last = None
    for attempt in range(retries):
        try:
            data = curl_json(url)
        except Exception as e:
            last = e
            time.sleep(min(2 ** attempt * 10, 60))
            continue
        if "error" in data:
            last = RuntimeError("API error: %s" % data["error"].get("info", data["error"]))
            time.sleep(min(2 ** attempt * 10, 60))
            continue
        return data
    raise RuntimeError("gave up after %d attempts: %s" % (retries, last))


def pull_article(rank, title):
    out_path = os.path.join(REVDIR, "%d.jsonl" % rank)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        with open(out_path, "r", encoding="utf-8") as f:
            n = sum(1 for _ in f)
        return n, "skipped-resume"
    title_enc = urllib.parse.quote(title, safe="")
    rvcontinue = None
    n = 0
    t0 = time.time()
    with open(out_path, "w", encoding="utf-8") as out:
        while True:
            data = fetch_page(title_enc, rvcontinue)
            pages = data.get("query", {}).get("pages", [])
            if not pages:
                raise RuntimeError("no pages in response")
            page = pages[0]
            if page.get("missing"):
                raise RuntimeError("page missing (title not found)")
            for rev in page.get("revisions", []):
                rec = {
                    "rank": rank,
                    "article": page.get("title", title),
                    "revid": rev.get("revid"),
                    "parentid": rev.get("parentid"),
                    "user": rev.get("user"),
                    "timestamp": rev.get("timestamp"),
                    "comment": rev.get("comment"),
                    "tags": rev.get("tags", []),
                    "size": rev.get("size"),
                }
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n += 1
            cont = data.get("continue", {})
            rvcontinue = cont.get("rvcontinue")
            if not rvcontinue:
                break
            time.sleep(PACE)
    dt = time.time() - t0
    return n, "ok %.0fs" % dt


def main():
    os.makedirs(REVDIR, exist_ok=True)
    os.makedirs(WORKDIR, exist_ok=True)
    os.makedirs(os.path.dirname(ERRLOG), exist_ok=True)
    t_start = time.time()
    articles = []
    with open(CHUNK, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            rank, title = line.split("\t", 1)
            articles.append((int(rank), title))
    log("chunk-09: %d articles" % len(articles))
    counts = {}
    failures = []
    for i, (rank, title) in enumerate(articles):
        log("article %d/%d rank=%d %r ..." % (i + 1, len(articles), rank, title))
        try:
            n, note = pull_article(rank, title)
            counts[rank] = (title, n)
            log("  done: %d revisions (%s)" % (n, note))
        except Exception as e:
            counts[rank] = (title, -1)
            failures.append((rank, title, str(e)))
            log_error(title, rank, str(e))
        time.sleep(PACE)
    wall = time.time() - t_start
    total = sum(n for (t, n) in counts.values() if n > 0)
    with open(os.path.join(WORKDIR, "counts.json"), "w", encoding="utf-8") as f:
        json.dump({str(r): {"title": t, "revisions": n} for r, (t, n) in counts.items()},
                  f, ensure_ascii=False, indent=1)
    log("DONE: %d articles, %d revisions, %d failures, wall %.0fs"
        % (len(articles), total, len(failures), wall))
    return total, len(failures), wall


if __name__ == "__main__":
    main()
