#!/usr/bin/env python3
"""Lane 3: Common Crawl CC-MAIN-2026-25 exact-URL CDX probes. Polite: 1 req / 2s."""
import json, time
from urllib.parse import quote
from urllib.request import Request, urlopen

CRAWL = "CC-MAIN-2026-25"
OUT = "/home/hatch/workspace/silent-locus/collections/hunt-missed-surfaces/hot-leads/cc-cdx-probes.jsonl"

CANDIDATES = [
    # DoE CRDC — fuzz/SQLi/oai fingerprints (incident Jun 17)
    ("https://civilrightsdata.ed.gov/api/v1.0/GetStateEstimation?survey_Year_Key=9&Measure_Id=1&State_Id=1%20OR%201=1", "DoE exact SQLi probe (Transluce headline)"),
    ("https://civilrightsdata.ed.gov/api/v1.0/GetStateEstimation?survey_Year_Key=9&Measure_Id=1&State_Id=12&zz=oai17816845870756322", "DoE zz=oai agent tag"),
    ("https://civilrightsdata.ed.gov/api/v1.0/GetNationalEstimation?survey_Year_Key=9&Measure_Id=130", "DoE Measure_Id=130 SYK=9 (dsqa_250 task params)"),
    ("https://civilrightsdata.ed.gov/assets/downloads/2000/2000-virginia-projection.xls?cb=0.518873325748815", "DoE virginia-projection.xls download"),
    ("https://civilrightsdata.ed.gov/api/v1.0/GetStateNationalEstimation?survey_Year_Key=9&Report_Id=1", "DoE GetStateNationalEstimation SYK=9"),
    ("https://civilrightsdata.ed.gov/api/v1.0/GetStateEstimation?survey_Year_Key=10&Measure_Id=115&State_Id=33&zz=oai17816896520493213", "DoE second zz=oai variant"),
    ("https://civilrightsdata.ed.gov/", "DoE root baseline"),
    # LAC collection search payloads (incidents May 28 + Jun 9; May 28 predates crawl window)
    ("https://recherche-collection-search.bac-lac.canada.ca/eng/Home/Record?app=divincan&IdNumber=1%20OR%201%3D1", "LAC SQLi payload 1 OR 1=1"),
    ("https://recherche-collection-search.bac-lac.canada.ca/eng/Home/Record?app=divincan&IdNumber=%27", "LAC single-quote payload"),
    ("https://recherche-collection-search.bac-lac.canada.ca/eng/Home/Record?app=divincan&IdNumber=2147483648", "LAC int-overflow payload"),
    ("https://recherche-collection-search.bac-lac.canada.ca/eng/Home/Record?app=divincan&IdNumber=91&debug=1", "LAC debug=1 payload"),
    ("https://recherche-collection-search.bac-lac.canada.ca/ajax/download?DataSource=Genealogy%7CBirMarDivDea%7CDivInCan&DateBucket=1900-1909%7C1906&num=100&start=0&format=csv&lang=eng&downloadtoken=DT--abc--DT", "LAC csv downloadtoken fuzz"),
    ("https://recherche-collection-search.bac-lac.canada.ca/eng/Home/Record?app=divincan&IdNumber=abc", "LAC abc payload"),
    # BEA (incident Jun 16-18)
    ("https://apps.bea.gov/api/data?UserID=samplekey&method=GetData&datasetname=Regional&TableName=SAINC4&LineCode=10&GeoFIPS=51000&Year=2013&ResultFormat=json&cb=1781641182277136416", "BEA api/data with epoch-nonce cb"),
    ("https://apps.bea.gov/api/data/?UserID=samplekey&method=GETDATASETLIST&ResultFormat=JSON&cb=1781641183923866536", "BEA GETDATASETLIST with cb nonce"),
    ("https://apps.bea.gov/regional/zip/SAINC.zip", "BEA SAINC.zip download"),
    ("https://apps.bea.gov/api/data/?method=GetData&datasetname=Regional&TableName=SAINC4&LineCode=47&GeoFIPS=51000&Year=2013&ResultFormat=JSON", "BEA api/data no UserID"),
    # SEC county.json (incident Jun 18; laundering cluster corroborated in our corpus)
    ("https://www.sec.gov/files/county.json", "SEC county.json"),
]

def probe(url, note):
    q = "https://index.commoncrawl.org/" + CRAWL + "-index?url=" + quote(url, safe="") + "&output=json"
    req = Request(q, headers={"User-Agent": "silent-locus-hunt-lane3/1.0 (research)"})
    try:
        with urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8", "replace")
            code = resp.status
    except Exception as e:
        return {"candidate_url": url, "note": note, "crawl": CRAWL,
                "http_code": "ERR", "hits": [], "zero": False,
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
            "zero": len(hits) == 0}

def main():
    with open(OUT, "a") as out:
        for i, (url, note) in enumerate(CANDIDATES):
            rec = probe(url, note)
            out.write(json.dumps(rec) + "\n")
            out.flush()
            print(f"[{i+1}/{len(CANDIDATES)}] code={rec['http_code']} hits={rec.get('hit_count')} {url[:90]}", flush=True)
            time.sleep(2.2)
    print(f"done -> {OUT}")

if __name__ == "__main__":
    main()
