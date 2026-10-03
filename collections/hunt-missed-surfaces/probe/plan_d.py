#!/usr/bin/env python3
"""Lane 2 plan D: archive.org availability API + Wayback CDX exact-URL probes.

Exact incident URLs (reconstructed from the arquivo-pt CDX bytes, read-only):
- DoE CRDC fuzz URL with zz=oai<digits> cache-buster
- LAC collection-search ajax/count URL with debug=1 payload
- SEC county.json (known laundering cluster)"""
import sys, urllib.parse
sys.path.insert(0, ".")
from probe import probe

DOE_URL = ("https://civilrightsdata.ed.gov/api/v1.0/GetStateEstimation"
           "?survey_Year_Key=10&Measure_Id=1&State_Id=1&zz=oai17816834089056622")
LAC_URL = ("https://recherche-collection-search.bac-lac.canada.ca/ajax/count"
           "?DataSource=Genealogy%7CBirMarDivDea%7CDivInCan"
           "&DateBucket=1900-1909%7C1907&fId=jqP___&debug=1")
SEC_URL = "https://www.sec.gov/files/county.json"

# --- archive.org availability API: closest IA snapshot of the exact URL ---
for url, pid, note in [
    (DOE_URL, "ia-avail-doe",
     "availability API for exact CRDC fuzz URL (zz=oai cache-buster); "
     "shows closest IA snapshot, not agent-traffic evidence"),
    (LAC_URL, "ia-avail-lac",
     "availability API for exact LAC ajax/count debug=1 payload URL"),
    (SEC_URL, "ia-avail-sec",
     "availability API for exact SEC county.json URL (known Jun-18 cluster)"),
]:
    probe("archive.org (availability API)", pid,
          "https://archive.org/wayback/available?url=" + urllib.parse.quote(url, safe=""),
          note=note, timeout=60)

# --- Wayback CDX exact-URL: statuscode 200 only, collapsed ---
for url, pid, note in [
    (DOE_URL, "cdx-exact-doe",
     "CDX exact-URL for CRDC fuzz URL; filter=statuscode:200; grepped for "
     "State_Id/Measure_Id/survey_Year_Key/zz=oai fingerprints"),
    (LAC_URL, "cdx-exact-lac",
     "CDX exact-URL for LAC debug=1 payload URL; filter=statuscode:200"),
    (SEC_URL, "cdx-exact-sec",
     "CDX exact-URL for www.sec.gov/files/county.json; filter=statuscode:200; "
     "narrower rerun of re-hunt cdx-sec-county for this lane's own record"),
]:
    probe("web.archive.org (Wayback CDX)", pid,
          ("https://web.archive.org/cdx/search/cdx?url=" +
           urllib.parse.quote(url, safe="") +
           "&output=json&filter=statuscode:200&collapse=urlkey"),
          note=note, timeout=90)
