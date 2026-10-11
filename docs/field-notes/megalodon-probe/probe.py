#!/usr/bin/env python3
"""Probe Megalodon (megalodon.jp) gyotaku lists for incident URLs.

Read-only. Uses the native per-URL lookup: GET /pc/main?url=<url>.
Parses "見つかりませんでした" (not found) vs gyo.tc capture links.
Idempotent: results keyed by URL in state.json; reruns skip done URLs.

Scope: agents and agent infrastructure only. No captures are submitted.
"""
import json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
STATE = ROOT / "state.json"
LOG = DATA / "probe-log.jsonl"

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

PROBES = [
    # exact incident URLs
    ("doe-zzoai-exact", "https://civilrightsdata.ed.gov/api/v1.0/GetStateEstimation?survey_Year_Key=9&Measure_Id=1&State_Id=12&zz=oai17816845870756322"),
    ("doe-zzoai-exact-2", "https://civilrightsdata.ed.gov/api/v1.0/GetStateEstimation?survey_Year_Key=10&Measure_Id=115&State_Id=33&zz=oai17816896520493213"),
    ("doe-virginia-projection", "https://civilrightsdata.ed.gov/assets/downloads/2000/2000-virginia-projection.xls?cb=0.518873325748815"),
    ("lac-ajax-count-debug", "https://recherche-collection-search.bac-lac.canada.ca/ajax/count?DataSource=Genealogy%7CBirMarDivDea%7CDivInCan&DateBucket=1900-1909%7C1907&fId=jqP___&debug=1"),
    ("lac-download-token", "https://recherche-collection-search.bac-lac.canada.ca/ajax/download?DataSource=Genealogy%7CBirMarDivDea%7CDivInCan&DateBucket=1900-1909%7C1906&num=100&start=0&format=csv&lang=eng&downloadtoken=DT--abc--DT"),
    ("sec-county-json", "https://www.sec.gov/files/county.json"),
    # prefix/endpoint forms (tests whether the list is prefix-matched)
    ("doe-endpoint-prefix", "https://civilrightsdata.ed.gov/api/v1.0/GetStateEstimation"),
    ("lac-ajax-prefix", "https://recherche-collection-search.bac-lac.canada.ca/ajax/count"),
    # bare domains
    ("domain-civilrightsdata", "https://civilrightsdata.ed.gov"),
    ("domain-bea", "https://bea.gov"),
    ("domain-bac-lac", "https://bac-lac.gc.ca"),
    # http:// variants (agents may have archived the http form)
    ("doe-zzoai-http", "http://civilrightsdata.ed.gov/api/v1.0/GetStateEstimation?survey_Year_Key=9&Measure_Id=1&State_Id=12&zz=oai17816845870756322"),
    ("sec-county-json-http", "http://www.sec.gov/files/county.json"),
    ("lac-ajax-http", "http://recherche-collection-search.bac-lac.canada.ca/ajax/count?DataSource=Genealogy%7CBirMarDivDea%7CDivInCan&DateBucket=1900-1909%7C1907&fId=jqP___&debug=1"),
]

def lookup(url):
    q = "https://megalodon.jp/pc/main?url=" + urllib.parse.quote(url, safe="")
    req = urllib.request.Request(q, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8", errors="replace")
    notfound = "見つかりませんでした" in html
    gyo = sorted(set(re.findall(r"https?://gyo\.tc/[A-Za-z0-9]+", html)))
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    return {
        "http": r.status,
        "not_found_text": notfound,
        "gyotaku_links": gyo,
        "title": (title.group(1).strip()[:80] if title else ""),
    }

def main():
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    for name, url in PROBES:
        if name in state and state[name].get("done"):
            print(f"skip {name} (done)")
            continue
        try:
            res = lookup(url)
            rec = {"name": name, "url": url, "done": True, **res}
            print(f"{name}: http={res['http']} notfound={res['not_found_text']} gyo={len(res['gyotaku_links'])}")
        except Exception as e:
            rec = {"name": name, "url": url, "done": False, "error": str(e)[:200]}
            print(f"{name}: ERROR {e}")
        state[name] = rec
        with LOG.open("a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False))
        time.sleep(2)  # polite pacing
    hits = [k for k, v in state.items() if v.get("gyotaku_links")]
    print(f"\n{hits and 'HITS: ' + str(hits) or 'no captures found for any probe'}")

if __name__ == "__main__":
    main()
