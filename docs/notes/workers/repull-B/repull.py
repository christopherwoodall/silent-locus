#!/usr/bin/env python3
"""REPULL-WORKER-B: re-pull revision history for ranks 118-131 via curl.
Python used ONLY for URL encoding and JSON parsing (no Python HTTP).
Pacing: >=5s between requests to en.wikipedia.org.
"""
import json, os, subprocess, sys, time
from urllib.parse import quote

RAW = os.path.expanduser("~/workspace/silent-locus-top500/data/2026-10-06-wikipedia-top500-infra-scan/raw")
TSV = os.path.join(RAW, "missing-g2.tsv")
REVD = os.path.join(RAW, "revisions")
UA = "silent-locus-top500-scan/1.0 (research)"

BASE = ("https://en.wikipedia.org/w/api.php?action=query&prop=revisions"
        "&rvprop=user%7Ctimestamp%7Cids%7Ccomment%7Ctags%7Csize"
        "&rvlimit=500&rvdir=older"
        "&rvstart=2026-10-07T00%3A00%3A00Z&rvend=2020-01-01T00%3A00%3A00Z"
        "&format=json&formatversion=2")

def curl(url):
    r = subprocess.run(["curl", "-sS", "--max-time", "60", "-A", UA, url],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None, r.stderr.strip()
    return r.stdout, None

def extract(article_title, rank, data):
    """Parse API JSON -> list of JSONL lines + rvcontinue token or None."""
    try:
        obj = json.loads(data)
    except json.JSONDecodeError as e:
        return None, "JSON decode error: %s" % e
    pages = (obj.get("query") or {}).get("pages") or []
    lines = []
    for p in pages:
        if p.get("missing"):
            return [], "ARTICLE MISSING from API response: %r" % article_title
        for rev in p.get("revisions", []):
            lines.append(json.dumps({
                "rank": rank, "article": article_title,
                "revid": rev.get("revid"), "parentid": rev.get("parentid"),
                "user": rev.get("user"), "timestamp": rev.get("timestamp"),
                "comment": rev.get("comment"), "tags": rev.get("tags") or [],
                "size": rev.get("size"),
            }, ensure_ascii=False))
    cont = (obj.get("continue") or {}).get("rvcontinue")
    return lines, cont

def pull(rank, title):
    enc = quote(title, safe="")
    url = BASE + "&titles=" + enc
    tmp = os.path.join(REVD, "%d.jsonl.tmp" % rank)
    final = os.path.join(REVD, "%d.jsonl" % rank)
    count = 0
    cont = True
    req = 0
    with open(tmp, "w", encoding="utf-8") as f:
        while cont:
            body, err = curl(url)
            req += 1
            if body is None:
                print("  ERROR rank %d req %d: %s" % (rank, req, err), flush=True)
                return False, count
            lines, res = extract(title, rank, body)
            if lines is None:
                print("  ERROR rank %d req %d: %s" % (rank, req, res), flush=True)
                return False, count
            if isinstance(res, str) and res.startswith("ARTICLE MISSING"):
                print("  %s" % res, flush=True)
                return False, count
            for ln in lines:
                f.write(ln + "\n")
            count += len(lines)
            cont = res if isinstance(res, str) else None
            if cont:
                url = BASE + "&titles=" + enc + "&rvcontinue=" + quote(cont, safe="")
            print("  rank %d: req %d -> %d revs so far" % (rank, req, count), flush=True)
            time.sleep(5.5)
        f.flush()
        os.fsync(f.fileno())
    os.rename(tmp, final)
    print("  rank %d DONE: %d revisions -> %s" % (rank, count, final), flush=True)
    return True, count

def main():
    total = 0
    done = 0
    with open(TSV, encoding="utf-8") as f:
        rows = [ln.rstrip("\n").split("\t") for ln in f if ln.strip()]
    for rank_s, title in rows:
        rank = int(rank_s)
        print("== rank %d: %s" % (rank, title), flush=True)
        ok, n = pull(rank, title)
        total += n
        if ok:
            done += 1
        else:
            print("  FAILED rank %d after %d revs" % (rank, n), flush=True)
        time.sleep(2)
    print("SUMMARY: %d/%d articles ok, %d total revisions" % (done, len(rows), total))

if __name__ == "__main__":
    main()
