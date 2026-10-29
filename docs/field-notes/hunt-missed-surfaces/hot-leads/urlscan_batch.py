#!/usr/bin/env python3
"""Lane 3 urlscan.io deep queries. Polite: 1 req / 2s. Keyless API."""
import json, time, sys
from urllib.parse import quote
from urllib.request import Request, urlopen

OUT = "/home/hatch/workspace/silent-locus/collections/hunt-missed-surfaces/hot-leads/urlscan-queries.jsonl"
RAW = "/home/hatch/workspace/silent-locus/collections/hunt-missed-surfaces/hot-leads/data"

def run_query(q, note, size=100):
    url = "https://urlscan.io/api/v1/search/?q=" + quote(q) + "&size=" + str(size)
    req = Request(url, headers={"User-Agent": "silent-locus-hunt-lane3/1.0 (research)"})
    try:
        with urlopen(req, timeout=40) as resp:
            body = resp.read()
            code = resp.status
    except Exception as e:
        return {"query": q, "note": note, "http_code": "ERR", "result_count": None,
                "examples": [], "note2": f"transport error: {type(e).__name__}: {e}"}
    try:
        data = json.loads(body)
    except Exception as e:
        return {"query": q, "note": note, "http_code": code, "result_count": None,
                "examples": [], "note2": f"bad json: {e}"}
    total = data.get("total")
    results = data.get("results", [])
    examples = []
    for r in results[:5]:
        t = r.get("task", {}) or {}
        examples.append({
            "uuid": t.get("uuid"),
            "page_url": r.get("page", {}).get("url"),
            "date": t.get("time"),
        })
    return {"query": q, "note": note, "http_code": code,
            "result_count": total, "returned": len(results),
            "examples": examples}

QUERIES = [
    # Family 1: task.url substrings
    ("task.url:*civilrightsdata*", "F1: CRDC host in submitted URLs (broader than prior domain: probe)"),
    ("task.url:*bac-lac.gc.ca*", "F1: Library and Archives Canada host"),
    ("task.url:*bea.gov*", "F1: BEA host"),
    ("task.url:*census.gov*", "F1: Census host"),
    ("task.url:*kansasmemory*", "F1: Kansas memory host"),
    # Family 2: filenames
    ("filename:county.json", "F2: county.json filename (size=100, broader than prior size=10)"),
    ("filename:*virginia-projection*", "F2: virginia-projection filename"),
    ("filename:*.xls domain:ed.gov", "F2: xls files on ed.gov"),
    ("filename:*.xls domain:census.gov", "F2: xls files on census.gov"),
    ("filename:*.xls domain:bea.gov", "F2: xls files on bea.gov"),
    # Family 3: date windows around incidents
    ("task.url:*civilrightsdata* date:>2026-06-16 date:<2026-06-19", "F3: DoE incident window Jun 16-19"),
    ("task.url:*bea.gov* date:>2026-06-15 date:<2026-06-19", "F3: BEA incident window Jun 16-18"),
    ("task.url:*census.gov* date:>2026-06-15 date:<2026-06-23", "F3: Census incident window Jun 16-22"),
    ("task.url:*sec.gov* date:>2026-06-17 date:<2026-06-19", "F3: SEC incident window Jun 18"),
    ("task.url:*kansasmemory* date:>2026-05-06 date:<2026-05-09", "F3: Kansas window May 7"),
    ("task.url:*bac-lac.gc.ca* date:>2026-05-27 date:<2026-05-29", "F3: LAC window May 28"),
    ("task.url:*bac-lac.gc.ca* date:>2026-06-08 date:<2026-06-10", "F3: LAC window Jun 9"),
    ("task.url:*max.gov* date:>2026-05-24 date:<2026-05-28", "F3: MAX.gov window May 25-27"),
    ("task.url:*cdc.gov* date:>2026-07-17 date:<2026-07-20", "F3: CDC WONDER window Jul 18"),
    # Family 4: oai/zz strings
    ("page.url:*oai*", "F4: oai in page.url, size=10 noise grading"),
    ("task.url:*zz=oai*", "F4: zz=oai literal in submitted URL"),
    ("page.url:*zz=oai*", "F4: zz=oai in page.url"),
]

def main():
    n = 0
    with open(OUT, "a") as out:
        for q, note in QUERIES:
            size = 10 if q == "page.url:*oai*" else 100
            rec = run_query(q, note, size=size)
            rec["family_note"] = note
            out.write(json.dumps(rec) + "\n")
            out.flush()
            n += 1
            print(f"[{n}/{len(QUERIES)}] q={q[:70]!r} code={rec['http_code']} total={rec['result_count']}", flush=True)
            time.sleep(2.2)  # polite
    print(f"done, {n} queries -> {OUT}")

if __name__ == "__main__":
    main()
