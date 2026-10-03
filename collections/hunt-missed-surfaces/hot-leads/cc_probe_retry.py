#!/usr/bin/env python3
"""Lane 3: retry CC probes that got transient 502/504. Longer spacing (5s)."""
import json, time
from urllib.parse import quote
from urllib.request import Request, urlopen

CRAWL = "CC-MAIN-2026-25"
OUT = "/home/hatch/workspace/silent-locus/collections/hunt-missed-surfaces/hot-leads/cc-cdx-probes.jsonl"

RETRY = [
    ("https://civilrightsdata.ed.gov/api/v1.0/GetStateEstimation?survey_Year_Key=9&Measure_Id=1&State_Id=1%20OR%201=1", "DoE exact SQLi probe (retry)"),
    ("https://civilrightsdata.ed.gov/", "DoE root baseline (retry)"),
    ("https://recherche-collection-search.bac-lac.canada.ca/eng/Home/Record?app=divincan&IdNumber=1%20OR%201%3D1", "LAC SQLi payload 1 OR 1=1 (retry)"),
    ("https://recherche-collection-search.bac-lac.canada.ca/eng/Home/Record?app=divincan&IdNumber=%27", "LAC single-quote payload (retry)"),
    ("https://recherche-collection-search.bac-lac.canada.ca/ajax/download?DataSource=Genealogy%7CBirMarDivDea%7CDivInCan&DateBucket=1900-1909%7C1906&num=100&start=0&format=csv&lang=eng&downloadtoken=DT--abc--DT", "LAC csv downloadtoken fuzz (retry)"),
    ("https://recherche-collection-search.bac-lac.canada.ca/eng/Home/Record?app=divincan&IdNumber=abc", "LAC abc payload (retry)"),
    ("https://apps.bea.gov/api/data/?UserID=samplekey&method=GETDATASETLIST&ResultFormat=JSON&cb=1781641183923866536", "BEA GETDATASETLIST with cb nonce (retry)"),
    ("https://apps.bea.gov/regional/zip/SAINC.zip", "BEA SAINC.zip download (retry)"),
    ("https://apps.bea.gov/api/data/?method=GetData&datasetname=Regional&TableName=SAINC4&LineCode=47&GeoFIPS=51000&Year=2013&ResultFormat=JSON", "BEA api/data no UserID (retry)"),
]

def probe(url, note):
    q = "https://index.commoncrawl.org/" + CRAWL + "-index?url=" + quote(url, safe="") + "&output=json"
    req = Request(q, headers={"User-Agent": "silent-locus-hunt-lane3/1.0 (research)"})
    try:
        with urlopen(req, timeout=90) as resp:
            body = resp.read().decode("utf-8", "replace")
            code = resp.status
    except Exception as e:
        return {"candidate_url": url, "note": note, "crawl": CRAWL,
                "http_code": "ERR", "hits": [], "zero": False, "attempt": "retry",
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
            "zero": len(hits) == 0, "attempt": "retry"}

def main():
    with open(OUT, "a") as out:
        for i, (url, note) in enumerate(RETRY):
            rec = probe(url, note)
            out.write(json.dumps(rec) + "\n")
            out.flush()
            print(f"[{i+1}/{len(RETRY)}] code={rec['http_code']} hits={rec.get('hit_count')} err={rec.get('error','')[:40]} :: {note[:60]}", flush=True)
            time.sleep(5.0)
    print(f"done -> {OUT}")

if __name__ == "__main__":
    main()
