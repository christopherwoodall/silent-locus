#!/usr/bin/env python3
"""REVISION-PULLER-02: pull revision history for chunk-02 articles (ranks 89-131).

Methodology: docs/methodology.md — curl only (VM Python HTTP stacks break on
the egress proxy); python3 used for URL-encoding and JSON processing only.
Pace: >=5s between requests to en.wikipedia.org.
UA: silent-locus-top500-scan/1.0 (research)
"""
import json, os, subprocess, sys, time
from urllib.parse import quote

BASE = "https://en.wikipedia.org/w/api.php"
UA = "silent-locus-top500-scan/1.0 (research)"
CHUNK = "data/2026-10-06-wikipedia-top500-infra-scan/raw/chunks/chunk-02"
OUTDIR = "data/2026-10-06-wikipedia-top500-infra-scan/raw/revisions"
ERRLOG = "data/2026-10-06-wikipedia-top500-infra-scan/workers/rev-puller-02/errors.log"
GAP = 5.0          # seconds between requests (pace limit)
MAX_ATTEMPTS = 3   # per page before failing the article

def log_err(msg):
    os.makedirs(os.path.dirname(ERRLOG), exist_ok=True)
    with open(ERRLOG, "a") as f:
        f.write(msg + "\n")

def api_url(title, rvcontinue=None):
    p = {
        "action": "query",
        "prop": "revisions",
        "titles": title,
        "rvprop": "user|timestamp|ids|comment|tags|size",
        "rvlimit": "500",
        "rvdir": "older",
        "rvstart": "2026-10-07T00:00:00Z",
        "rvend": "2020-01-01T00:00:00Z",
        "format": "json",
        "formatversion": "2",
    }
    if rvcontinue:
        p["rvcontinue"] = rvcontinue
    return BASE + "?" + "&".join(f"{k}={quote(v, safe='')}" for k, v in p.items())

def fetch(url):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        r = subprocess.run(
            ["curl", "-sS", "--max-time", "60", "-A", UA, url],
            capture_output=True, text=True)
        if r.returncode == 0 and r.stdout:
            try:
                return json.loads(r.stdout)
            except json.JSONDecodeError as e:
                last = f"bad-json attempt={attempt}: {e}"
        else:
            last = f"curl rc={r.returncode} attempt={attempt}: {r.stderr.strip()[:200]}"
        time.sleep(GAP * attempt)  # backoff, also counts toward pacing
    raise RuntimeError(last)

def pull_article(rank, title):
    out = os.path.join(OUTDIR, f"{rank}.jsonl")
    rvcontinue = None
    count = 0
    with open(out, "w") as fh:
        while True:
            data = fetch(api_url(title, rvcontinue))
            if "error" in data:
                raise RuntimeError(f"api error: {data['error'].get('info', data['error'])}")
            pages = data.get("query", {}).get("pages", [])
            if not pages:
                raise RuntimeError("no pages in response")
            page = pages[0]
            if page.get("missing"):
                raise RuntimeError("article missing/redirect-unresolved")
            for rev in page.get("revisions", []):
                fh.write(json.dumps({
                    "rank": rank,
                    "article": title,
                    "revid": rev.get("revid"),
                    "parentid": rev.get("parentid"),
                    "user": rev.get("user"),
                    "timestamp": rev.get("timestamp"),
                    "comment": rev.get("comment", ""),
                    "tags": rev.get("tags", []),
                    "size": rev.get("size"),
                }, ensure_ascii=False) + "\n")
                count += 1
            rvcontinue = data.get("continue", {}).get("rvcontinue")
            if not rvcontinue:
                break
            time.sleep(GAP)
    return count

def main():
    os.makedirs(OUTDIR, exist_ok=True)
    t0 = time.time()
    counts, failures = {}, []
    with open(CHUNK) as f:
        lines = [l for l in f.read().splitlines() if l.strip()]
    print(f"chunk: {len(lines)} articles", flush=True)
    for line in lines:
        rank_s, title = line.split("\t", 1)
        rank = int(rank_s)
        t_a = time.time()
        try:
            n = pull_article(rank, title)
            counts[title] = n
            print(f"[{rank}] {title}: {n} revs ({time.time()-t_a:.1f}s)", flush=True)
        except Exception as e:
            failures.append((rank, title, str(e)))
            log_err(f"{rank}\t{title}\t{type(e).__name__}: {e}")
            print(f"[{rank}] {title}: FAILED ({e})", flush=True)
        time.sleep(GAP)
    wall = time.time() - t0
    total = sum(counts.values())
    summary = {
        "articles": len(lines), "ok": len(counts), "failed": len(failures),
        "total_revisions": total, "wall_seconds": round(wall, 1),
        "per_article": counts, "failures": failures,
    }
    with open("data/2026-10-06-wikipedia-top500-infra-scan/workers/rev-puller-02/summary.json", "w") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"DONE ok={len(counts)} failed={len(failures)} total={total} wall={wall/60:.1f}min")

if __name__ == "__main__":
    main()
