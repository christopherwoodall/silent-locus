#!/usr/bin/env python3
"""REVISION-PULLER-07R: RESUME pass for chunk-07 (ranks 296-339).

Skips articles whose raw/revisions/<rank>.jsonl already exists, is non-empty,
AND whose first line's "article" field equals the chunk title. Pulls the rest.
Methodology: docs/methodology.md — curl only; python3 for encoding/JSON only.
Pace: >=5s between requests. UA: silent-locus-top500-scan/1.0 (research)
"""
import json, os, subprocess, sys, time
from urllib.parse import quote

ROOT = os.path.expanduser("~/workspace/silent-locus-top500")
BASE = "https://en.wikipedia.org/w/api.php"
UA = "silent-locus-top500-scan/1.0 (research)"
CHUNK = os.path.join(ROOT, "data/2026-10-06-wikipedia-top500-infra-scan/raw/chunks/chunk-07")
OUTDIR = os.path.join(ROOT, "data/2026-10-06-wikipedia-top500-infra-scan/raw/revisions")
WORK = os.path.join(ROOT, "data/2026-10-06-wikipedia-top500-infra-scan/workers/rev-puller-07")
ERRLOG = os.path.join(WORK, "errors.log")
GAP = 5.0
MAX_ATTEMPTS = 3

def log_err(msg):
    os.makedirs(os.path.dirname(ERRLOG), exist_ok=True)
    with open(ERRLOG, "a") as f:
        f.write(msg + "\n")

def already_done(rank, title):
    p = os.path.join(OUTDIR, f"{rank}.jsonl")
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        return False
    try:
        with open(p) as f:
            first = json.loads(f.readline())
        return first.get("article") == title
    except Exception:
        return False

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
    last = "no attempts"
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
        time.sleep(GAP * attempt)
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
    os.makedirs(WORK, exist_ok=True)
    t0 = time.time()
    counts, failures, skipped = {}, [], []
    with open(CHUNK) as f:
        lines = [l for l in f.read().splitlines() if l.strip()]
    todo = []
    for line in lines:
        rank_s, title = line.split("\t", 1)
        rank = int(rank_s)
        if already_done(rank, title):
            skipped.append((rank, title))
            print(f"[{rank}] {title}: SKIP (cached)", flush=True)
        else:
            todo.append((rank, title))
    print(f"chunk: {len(lines)} articles, skipped={len(skipped)}, to pull={len(todo)}", flush=True)
    for rank, title in todo:
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
        "articles": len(lines), "skipped": len(skipped), "ok": len(counts),
        "failed": len(failures), "total_revisions": total,
        "wall_seconds": round(wall, 1),
        "skipped_list": [{"rank": r, "article": t} for r, t in skipped],
        "per_article": counts, "failures": failures,
    }
    with open(os.path.join(WORK, "summary.json"), "w") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"DONE skipped={len(skipped)} ok={len(counts)} failed={len(failures)} total={total} wall={wall/60:.1f}min", flush=True)

if __name__ == "__main__":
    main()
