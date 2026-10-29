#!/usr/bin/env python3
"""Lane 3: final CC retry for the 5 stubborn probes (10s spacing)."""
import json, time
from urllib.parse import quote
from urllib.request import Request, urlopen

CRAWL = "CC-MAIN-2026-25"
OUT = "/home/hatch/workspace/silent-locus/collections/hunt-missed-surfaces/hot-leads/cc-cdx-probes.jsonl"

RETRY = [
    ("https://civilrightsdata.ed.gov/api/v1.0/GetStateEstimation?survey_Year_Key=9&Measure_Id=1&State_Id=1%20OR%201=1", "DoE exact SQLi probe (retry2)"),
    ("https://civilrightsdata.ed.gov/", "DoE root baseline (retry2)"),
    ("https://recherche-collection-search.bac-lac.canada.ca/eng/Home/Record?app=divincan&IdNumber=%27", "LAC single-quote payload (retry2)"),
    ("https://recherche-collection-search.bac-lac.canada.ca/ajax/download?DataSource=Genealogy%7CBirMarDivDea%7CDivInCan&DateBucket=1900-1909%7C1906&num=100&start=0&format=csv&lang=eng&downloadtoken=DT--abc--DT", "LAC csv downloadtoken fuzz (retry2)"),
    ("https://apps.bea.gov/regional/zip/SAINC.zip", "BEA SAINC.zip download (retry2)"),
]

def probe(url, note):
    q = "https://index.commoncrawl.org/" + CRAWL + "-index?url=" + quote(url, safe="") + "&output=json"
    req = Request(q, headers={"User-Agent": "silent-locus-hunt-lane3/1.0 (research)"})
    try:
        with urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8", "replace")
            code = resp.status
    except Exception as e:
        return {"candidate_url": url, "note": note, "crawl": CRAWL,
                "http_code": "ERR", "hits": [], "zero": False, "attempt": "retry2",
                "error": f"{type(e).__name__}: {e}"}
    hits = []
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            hits.append(json.loads(line))
        except Exception:
            hits.append({"raw": line[:300]})
    return {"candidate_url": url, "note": note, "crawl": CRAWL,
            "http_code": code, "hits": hits[:10], "hit_count": len(hits),
            "zero": len(hits) == 0, "attempt": "retry2"}

def main():
    with open(OUT, "a") as out:
        for i, (url, note) in enumerate(RETRY):
            rec = probe(url, note)
            out.write(json.dumps(rec) + "\n")
            out.flush()
            print(f"[{i+1}/{len(RETRY)}] code={rec['http_code']} hits={rec.get('hit_count')} err={rec.get('error','')[:40]} :: {note[:60]}", flush=True)
            time.sleep(10.0)
    print(f"done -> {OUT}")

if __name__ == "__main__":
    main()
