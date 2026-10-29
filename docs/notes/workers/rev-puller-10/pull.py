#!/usr/bin/env python3
"""REVISION-PULLER-10: pull revision history for chunk-10 articles via curl.

Transport rules: curl only for HTTP; python for encoding/JSON. Pace <=1 req/5s
to en.wikipedia.org. UA: silent-locus-top500-scan/1.0 (research).
Never stops the chunk on a single article failure: log to errors.log, continue.
"""
import json, subprocess, sys, time, urllib.parse
from pathlib import Path

UA = "silent-locus-top500-scan/1.0 (research)"
WORKER = Path("/home/hatch/workspace/silent-locus-top500/workers/rev-puller-10")
RAW = Path("/home/hatch/workspace/silent-locus-top500/data/2026-10-06-wikipedia-top500-infra-scan/raw")
CHUNK = RAW / "chunks" / "chunk-10"
REVDIR = RAW / "revisions"
ERRLOG = WORKER / "errors.log"
BASE = "https://en.wikipedia.org/w/api.php"

REVDIR.mkdir(parents=True, exist_ok=True)
WORKER.mkdir(parents=True, exist_ok=True)

def api(params):
    """GET via curl, return parsed JSON or raise."""
    query = urllib.parse.urlencode(params)
    url = f"{BASE}?{query}"
    for attempt in range(4):
        p = subprocess.run(
            ["curl", "-sS", "--max-time", "60", "-A", UA, url],
            capture_output=True, text=True, timeout=90,
        )
        if p.returncode == 0:
            try:
                return json.loads(p.stdout)
            except json.JSONDecodeError:
                pass  # fall through to retry
        if attempt < 3:
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"curl failed after 4 attempts: {url[:120]}")

def fetch_article(rank, title):
    out_path = REVDIR / f"{rank}.jsonl"
    count = 0
    enc = urllib.parse.quote(title, safe="")
    params = {
        "action": "query", "prop": "revisions", "titles": title,
        "rvprop": "user|timestamp|ids|comment|tags|size",
        "rvlimit": "500", "rvdir": "older",
        "rvstart": "2026-10-07T00:00:00Z", "rvend": "2020-01-01T00:00:00Z",
        "format": "json", "formatversion": "2",
    }
    # note: requests lib not used; urlencode handles encoding identically
    with open(out_path, "w", encoding="utf-8") as fh:
        rvcontinue = None
        while True:
            if rvcontinue:
                params["rvcontinue"] = rvcontinue
            data = api(params)
            if "error" in data:
                raise RuntimeError(f"API error: {data['error']}")
            pages = data.get("query", {}).get("pages", [])
            if not pages:
                raise RuntimeError("empty pages in response")
            page = pages[0]
            if "missing" in page:
                raise RuntimeError(f"missing page (titles={title!r})")
            for rev in page.get("revisions", []):
                obj = {
                    "rank": rank, "article": title,
                    "revid": rev.get("revid"), "parentid": rev.get("parentid"),
                    "user": rev.get("user"), "timestamp": rev.get("timestamp"),
                    "comment": rev.get("comment"), "tags": rev.get("tags", []),
                    "size": rev.get("size"),
                }
                fh.write(json.dumps(obj, ensure_ascii=False) + "\n")
                count += 1
            rvcontinue = data.get("continue", {}).get("rvcontinue")
            if not rvcontinue:
                break
            time.sleep(5)  # pace <=1 req/5s
    return count

def main():
    articles = []
    for line in CHUNK.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rank, title = line.split("\t", 1)
        articles.append((int(rank), title))
    results = []  # (rank, title, count or None, error or None)
    for rank, title in articles:
        t0 = time.time()
        try:
            n = fetch_article(rank, title)
            results.append((rank, title, n, None))
            print(f"[{rank}] {title}: {n} revisions", flush=True)
        except Exception as e:
            msg = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} [{rank}] {title}: {e}"
            with open(ERRLOG, "a", encoding="utf-8") as el:
                el.write(msg + "\n")
            results.append((rank, title, None, str(e)))
            print(f"[{rank}] {title}: FAILED: {e}", flush=True)
        # pace between articles too (also covers fetch loop's last request)
        time.sleep(5)
    json.dump(results, open(WORKER / "results.json", "w"), indent=1)
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
