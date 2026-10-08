#!/usr/bin/env python3
"""REPULL-WORKER-A: re-pull Wikipedia revision histories for missing-g1.tsv.
HTTP strictly via curl subprocess (VM proxy breaks Python HTTP stacks).
Pacing: >=5s between requests to en.wikipedia.org.
Writes <rank>.jsonl.tmp then fsyncs + atomic rename to <rank>.jsonl.
"""
import json, subprocess, sys, time, os
from urllib.parse import quote

UA = "silent-locus-top500-scan/1.0 (research)"
PACE = 5.5
BASE = "https://en.wikipedia.org/w/api.php"
RAW = os.path.expanduser("~/workspace/silent-locus-top500/data/2026-10-06-wikipedia-top500-infra-scan/raw")
TSV = os.path.join(RAW, "missing-g1.tsv")
OUTDIR = os.path.join(RAW, "revisions")
LOG = os.path.expanduser("~/workspace/silent-locus-top500/workers/repull-A/progress.log")
MAX_REQ_PER_ARTICLE = 6000

os.makedirs(os.path.dirname(LOG), exist_ok=True)
os.makedirs(OUTDIR, exist_ok=True)

def log(msg):
    line = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + " " + msg
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def api_get(params):
    url = BASE + "?" + params
    cmd = ["curl", "-sS", "--max-time", "60", "-A", UA, url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl failed rc={r.returncode}: {r.stderr[:300]}")
    return r.stdout

def pull_one(rank, title):
    enc = quote(title, safe="")
    base_params = (
        "action=query&prop=revisions&titles=" + enc +
        "&rvprop=user%7Ctimestamp%7Cids%7Ccomment%7Ctags%7Csize"
        "&rvlimit=500&rvdir=older&rvstart=2026-10-07T00%3A00%3A00Z"
        "&rvend=2020-01-01T00%3A00%3A00Z&format=json&formatversion=2"
    )
    tmp = os.path.join(OUTDIR, f"{rank}.jsonl.tmp")
    total = 0
    rvcontinue = None
    reqs = 0
    with open(tmp, "w", encoding="utf-8") as fh:
        while True:
            params = base_params
            if rvcontinue:
                params += "&rvcontinue=" + rvcontinue
            reqs += 1
            if reqs > MAX_REQ_PER_ARTICLE:
                raise RuntimeError("exceeded MAX_REQ_PER_ARTICLE; possible stuck continue loop")
            for attempt in range(4):
                try:
                    body = api_get(params)
                    data = json.loads(body)
                    break
                except Exception as e:
                    log(f"  rank {rank}: request error attempt {attempt+1}: {e}")
                    if attempt == 3:
                        raise
                    time.sleep(10 * (attempt + 1))
            # pages: take first page that has revisions
            pages = data.get("query", {}).get("pages", [])
            page = next((p for p in pages if p.get("revisions")), pages[0] if pages else {})
            revs = page.get("revisions", [])
            if not revs and total == 0:
                log(f"  rank {rank} '{title}': WARNING no revisions returned (page missing={page.get('missing', False)})")
            for rev in revs:
                obj = {
                    "rank": rank,
                    "article": title,
                    "revid": rev.get("revid"),
                    "parentid": rev.get("parentid", 0),
                    "user": rev.get("user", ""),
                    "timestamp": rev.get("timestamp", ""),
                    "comment": rev.get("comment", ""),
                    "tags": rev.get("tags", []),
                    "size": rev.get("size", 0),
                }
                fh.write(json.dumps(obj, ensure_ascii=False) + "\n")
            total += len(revs)
            cont = data.get("continue", {}).get("rvcontinue")
            if not cont:
                break
            rvcontinue = cont
            if total % 5000 == 0 or len(revs) < 500:
                log(f"  rank {rank}: {total} revisions so far ({reqs} requests)")
            time.sleep(PACE)
        fh.flush()
        os.fsync(fh.fileno())
    final = os.path.join(OUTDIR, f"{rank}.jsonl")
    os.rename(tmp, final)
    return total, reqs

def main():
    items = []
    with open(TSV, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rank_s, title = line.split("\t", 1)
            items.append((int(rank_s), title))
    log(f"Starting repull of {len(items)} articles")
    for rank, title in items:
        final = os.path.join(OUTDIR, f"{rank}.jsonl")
        if os.path.exists(final):
            log(f"rank {rank} '{title}': already exists, skipping")
            continue
        log(f"rank {rank} '{title}': pulling")
        t0 = time.time()
        try:
            total, reqs = pull_one(rank, title)
        except Exception as e:
            log(f"rank {rank} '{title}': FAILED: {e}")
            continue
        log(f"rank {rank} '{title}': done, {total} revisions, {reqs} requests, {time.time()-t0:.0f}s")
    log("All articles processed")

if __name__ == "__main__":
    main()
