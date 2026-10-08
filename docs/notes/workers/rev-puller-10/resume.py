#!/usr/bin/env python3
"""REVISION-PULLER-10 resume: fetch articles not yet completed.

Completed ranks (parsed from pull.stdout.log): 420-432, 433(second: GDP list),
435-440. Remaining: 433-first (Barry Melrose, overwritten -> 433a.jsonl),
441-458 (441 partial -> refetch fully).
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

# (rank, title, outfile_stem) remaining work
TODO = [
    (441, "Dua Lipa", "441"),
    (442, "Napoleon", "442"),
    (443, "Tim Cook", "443"),
    (444, "Navier\u2013Stokes existence and smoothness", "444"),
    (445, "Scooter Braun", "445"),
    (446, "Jennifer Lawrence", "446"),
    (447, "2026", "447"),
    (448, "Ryan Gosling", "448"),
    (449, "Kayadu Lohar", "449"),
    (450, "2026 Mecklenburg-Vorpommern state election", "450"),
    (451, "The Gentlemen (2019 film)", "451"),
    (452, "Hailee Steinfeld", "452"),
    (453, "Jon Bernthal", "453"),
    (454, "2026 MTV Video Music Awards", "454"),
    (455, "Jason Sudeikis", "455"),
    (456, "Raphinha", "456"),
    (457, "Taylor Hanson", "457"),
    (458, "Enzo Fern\u00e1ndez", "458"),
]

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
    raise RuntimeError("curl failed after 4 attempts")

def fetch_article(rank, title, stem):
    out_path = REVDIR / f"{stem}.jsonl"
    count = 0
    params = {
        "action": "query", "prop": "revisions", "titles": title,
        "rvprop": "user|timestamp|ids|comment|tags|size",
        "rvlimit": "500", "rvdir": "older",
        "rvstart": "2026-10-07T00:00:00Z", "rvend": "2020-01-01T00:00:00Z",
        "format": "json", "formatversion": "2",
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
    log = open(WORKER / "resume.stdout.log", "w", encoding="utf-8")
    results = []
    for rank, title, stem in TODO:
        try:
            n = fetch_article(rank, title, stem)
            results.append({"rank": rank, "title": title, "stem": stem, "count": n, "error": None})
            log.write(f"[{rank}] {title} -> {stem}.jsonl: {n} revisions\n"); log.flush()
        except Exception as e:
            msg = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} [{rank}] {title}: {e}"
            with open(ERRLOG, "a", encoding="utf-8") as el:
                el.write(msg + "\n")
            results.append({"rank": rank, "title": title, "stem": stem, "count": None, "error": str(e)})
            log.write(f"[{rank}] {title}: FAILED: {e}\n"); log.flush()
        time.sleep(5)
    json.dump(results, open(WORKER / "resume-results.json", "w"), indent=1)
    log.write("RESUME DONE\n"); log.flush()

if __name__ == "__main__":
    main()
