#!/usr/bin/env python3
"""INGEST LANE G: fetch jsonhero.io shared docs (read-only, paced, browser UA)."""
import json, hashlib, time, urllib.request, sys, os
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "data/jsonhero/usage_patterns.json")
OUT = os.path.join(BASE, "data/jsonhero-docs")
os.makedirs(OUT, exist_ok=True)

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
PACING_S = 3.5

with open(SRC) as f:
    doc_ids = list(json.load(f)["doc_id_counts"].keys())

manifest = []
for i, did in enumerate(doc_ids):
    url = f"https://jsonhero.io/j/{did}.json"
    rec = {"doc_id": did, "source_url": url,
           "retrieved_at_utc": datetime.now(timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
            rec["http_status"] = r.status
            rec["byte_size"] = len(body)
            rec["sha256"] = hashlib.sha256(body).hexdigest()
            path = os.path.join(OUT, f"{did}.json")
            with open(path, "wb") as f:
                f.write(body)
            rec["file"] = f"data/jsonhero-docs/{did}.json"
            # sanity: is it JSON?
            try:
                json.loads(body)
                rec["parses_as_json"] = True
            except Exception as e:
                rec["parses_as_json"] = False
                rec["parse_error"] = str(e)[:200]
    except urllib.error.HTTPError as e:
        rec["http_status"] = e.code
        rec["error"] = f"HTTPError {e.code}"
    except Exception as e:
        rec["error"] = f"{type(e).__name__}: {str(e)[:200]}"
    manifest.append(rec)
    print(f"[{i+1}/{len(doc_ids)}] {did}: {rec.get('http_status', rec.get('error'))} "
          f"({rec.get('byte_size', 0)} bytes)", flush=True)
    if i < len(doc_ids) - 1:
        time.sleep(PACING_S)

mpath = os.path.join(OUT, "manifest.json")
with open(mpath, "w") as f:
    json.dump(manifest, f, indent=2)
ok = sum(1 for r in manifest if r.get("http_status") == 200)
print(f"\nDONE: {ok}/{len(manifest)} fetched OK -> {mpath}")
