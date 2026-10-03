#!/usr/bin/env python3
"""CC pattern sweep: machinery grammar across Common Crawl URL indexes.
Read-only. 2s pacing. Logs every query.
"""
import json, subprocess, time, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG = ROOT / "query-log.jsonl"
HITS = ROOT / "hits.jsonl"
ROOT.mkdir(parents=True, exist_ok=True)

CRAWLS = ["CC-MAIN-2026-25", "CC-MAIN-2026-21", "CC-MAIN-2026-30", "CC-MAIN-2026-17"]
DOMAINS = ["ed.gov", "sec.gov", "bea.gov", "census.gov", "gc.ca"]
PATTERNS = {
    "zzoai": r".*zz=oai[0-9]+.*",
    "nonce": r".*x=0\.[0-9]{14,}.*",
    "oai_research": r".*openai_research.*",
}
UA = "Mozilla/5.0 (compatible; incident-research/1.0)"

def query(coll, domain, pname, filt):
    qs = urllib.parse.urlencode({
        "url": domain, "matchType": "domain", "filter": "url:" + filt,
        "output": "json", "limit": 2000, "collapse": "urlkey"})
    url = f"https://index.commoncrawl.org/{coll}-index?{qs}"
    out = subprocess.run(["curl", "-sL", "--max-time", "180", "-A", UA, url],
                         capture_output=True, text=True, timeout=200)
    rows = []
    for line in out.stdout.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try: rows.append(json.loads(line))
            except Exception: pass
    return rows

def main():
    done = set()
    if LOG.exists():
        for l in LOG.read_text().splitlines():
            try:
                r = json.loads(l); done.add((r["crawl"], r["domain"], r["pattern"]))
            except Exception: pass
    total = len(CRAWLS) * len(DOMAINS) * len(PATTERNS)
    n = 0
    for coll in CRAWLS:
        for domain in DOMAINS:
            for pname, filt in PATTERNS.items():
                key = (coll, domain, pname)
                n += 1
                if key in done:
                    print(f"[{n}/{total}] skip {coll} {domain} {pname} (done)")
                    continue
                try:
                    rows = query(coll, domain, pname, filt)
                    rec = {"crawl": coll, "domain": domain, "pattern": pname,
                           "filter": filt, "hits": len(rows), "status": "ok"}
                    print(f"[{n}/{total}] {coll} {domain} {pname}: {len(rows)} hits")
                    for r in rows:
                        with HITS.open("a") as f:
                            f.write(json.dumps({"crawl": coll, "pattern": pname,
                                "timestamp": r.get("timestamp"), "url": r.get("url"),
                                "host": urllib.parse.urlparse(r.get("url","")).netloc,
                                "status": r.get("status")}) + "\n")
                except Exception as e:
                    rec = {"crawl": coll, "domain": domain, "pattern": pname,
                           "filter": filt, "hits": -1, "status": f"error: {e}"[:200]}
                    print(f"[{n}/{total}] {coll} {domain} {pname}: ERROR {e}")
                with LOG.open("a") as f:
                    f.write(json.dumps(rec) + "\n")
                time.sleep(2)
    print("done")

if __name__ == "__main__":
    main()
