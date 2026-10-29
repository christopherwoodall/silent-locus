#!/usr/bin/env python3
"""Lane 2 plan E: Lane-1 grade-A/B surfaces + one CDX retry (503 was transient)."""
import sys, urllib.parse
sys.path.insert(0, ".")
from probe import probe

# --- A1. Wayback Save Page Now: interface shape only (NO submission) ---
probe("Wayback Save Page Now (web.archive.org/save)", "spn-interface",
      "https://web.archive.org/save",
      note=("interface-shape probe ONLY (no capture submitted): confirm keyless "
            "SPN page exists; CDX is the queryable log side (see cdx-exact-* probes)"),
      timeout=60)

# --- A2. archive.org item search: fingerprint hunt in the item corpus ---
for q, pid in [("civilrightsdata", "ia-search-civilrightsdata"),
               ("\"county.json\"", "ia-search-countyjson"),
               ("openai_research", "ia-search-openairesearch"),
               ("virginia-projection", "ia-search-vaproj")]:
    probe("archive.org (advancedsearch)", pid,
          ("https://archive.org/advancedsearch.php?q=" +
           urllib.parse.quote(q, safe="") +
           "&fl[]=identifier,title,date&rows=20&output=json"),
          note=(f"item-corpus search for fingerprint {q}: agents could stage data "
                f"as items or mine prior captures; numFound=0 = honest negative"),
          timeout=60)

# --- B1. Bibliotheca Alexandrina Wayback mirror ---
probe("Bibliotheca Alexandrina Wayback mirror", "bibalex-live",
      "https://web.archive.bibalex.org/",
      note="liveness of the IA mirror host (alternate Wayback entry point)",
      timeout=60)

# --- B2. cors.lol ---
probe("cors.lol (api.cors.lol)", "corslol-live",
      "https://api.cors.lol/?url=https://example.com",
      note="liveness: free CORS proxy; no published logs -> unscourable-by-design; "
           "check response shape only",
      timeout=60)

# --- B3. jsonp.afeld.me ---
probe("jsonp.afeld.me", "jsonpafeld-live",
      "https://jsonp.afeld.me/?url=https://example.com",
      note="liveness: keyless JSONP CORS proxy; no logs -> unscourable-by-design",
      timeout=60)

# --- B4. Yandex translated-pages proxy: shape verification ---
probe("Yandex translated-pages proxy", "yandex-turbo-home",
      "https://translated.turbopages.org/",
      note="verify endpoint exists / 2026 URL shape; pure fetch relay class, "
           "no log interface expected",
      timeout=60)

# --- retry: CDX exact-URL for the DoE fuzz URL (503 transient in plan D) ---
DOE_URL = ("https://civilrightsdata.ed.gov/api/v1.0/GetStateEstimation"
           "?survey_Year_Key=10&Measure_Id=1&State_Id=1&zz=oai17816834089056622")
probe("web.archive.org (Wayback CDX)", "cdx-exact-doe-retry",
      ("https://web.archive.org/cdx/search/cdx?url=" +
       urllib.parse.quote(DOE_URL, safe="") +
       "&output=json&filter=statuscode:200&collapse=urlkey"),
      note=("SINGLE retry of plan-D 503 ('Internet Archive: Temporarily Offline'); "
            "sibling queries succeeded in same window so outage was transient"),
      timeout=90)
