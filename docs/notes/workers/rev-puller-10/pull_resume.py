#!/usr/bin/env python3
"""REVISION-PULLER-10 RESUME pass: resume chunk-10 after the failed worker died.

Skip logic: if raw/revisions/<rank>.jsonl exists, is non-empty, and its first
line's "article" equals the chunk title -> SKIP. If it exists but holds a
DIFFERENT article (rank-433 collision) -> write to <rank>_<slug>.jsonl.
Otherwise pull fresh.

Transport: curl only for HTTP; python for encoding/JSON only.
Pace <=1 req/5s to en.wikipedia.org. UA silent-locus-top500-scan/1.0 (research).
"""
import json, re, subprocess, sys, time, urllib.parse
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

def slug(title):
    s = title.lower().replace(" ", "_")
    s = re.sub(r"[^a-z0-9_]", "", s)
    return s[:30].strip("_") or "x"

def first_article(path):
    try:
        with open(path, encoding="utf-8") as fh:
            line = fh.readline().strip()
            if not line:
                return None
            return json.loads(line).get("article")
    except Exception:
        return None

def target_path(rank, title):
    """Return (out_path, skip_reason_or_None)."""
    plain = REVDIR / f"{rank}.jsonl"
    cur = first_article(plain)
    if cur == title:
        n = sum(1 for _ in open(plain, encoding="utf-8"))
        return plain, f"SKIP (exists, {n} revisions)"
    if cur is not None and cur != title:
        # filename collision: different article holds this rank file
        alt = REVDIR / f"{rank}_{slug(title)}.jsonl"
        cur2 = first_article(alt)
        if cur2 == title:
            n = sum(1 for _ in open(alt, encoding="utf-8"))
            return alt, f"SKIP-collision (exists {alt.name}, {n} revisions)"
        return alt, None  # pull into slugged file
    return plain, None  # missing/empty -> pull into plain file

def api(params):
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
                pass
        if attempt < 3:
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"curl failed after 4 attempts: {url[:120]}")

def fetch_article(rank, title, out_path):
    count = 0
    params = {
        "action": "query", "prop": "revisions", "titles": title,
        "rvprop": "user|timestamp|ids|comment|tags|size",
        "rvlimit": "500", "rvdir": "older",
        "rvstart": "2026-10-07T00:00:00Z", "rvend": "2020-01-01T00:00:00Z",
        "format": "json", "formatversion": 2,
    }
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
            time.sleep(5)
    return count

def main():
    articles = []
    for line in CHUNK.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rank, title = line.split("\t", 1)
        articles.append((int(rank), title))
    results = []
    for rank, title in articles:
        out_path, skip = target_path(rank, title)
        if skip:
            print(f"[{rank}] {title}: {skip}", flush=True)
            results.append({"rank": rank, "article": title, "status": "skipped",
                            "path": out_path.name, "note": skip})
            continue
        try:
            n = fetch_article(rank, title, out_path)
            msg = f"[{rank}] {title}: {n} revisions -> {out_path.name}"
            print(msg, flush=True)
            results.append({"rank": rank, "article": title, "status": "pulled",
                            "revisions": n, "path": out_path.name})
        except Exception as e:
            emsg = (f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} "
                    f"[{rank}] {title}: {e}")
            with open(ERRLOG, "a", encoding="utf-8") as el:
                el.write(emsg + "\n")
            print(f"[{rank}] {title}: FAILED: {e}", flush=True)
            results.append({"rank": rank, "article": title, "status": "failed",
                            "error": str(e)})
        time.sleep(5)
    with open(WORKER / "results-resume.json", "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False)
    print("RESUME DONE", flush=True)

if __name__ == "__main__":
    main()
