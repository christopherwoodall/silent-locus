#!/usr/bin/env python3
"""Lane 23: re-pull cited urlquery reports (live first, Wayback fallback),
record availability, save per-report JSON + provenance sidecar."""
import json, os, time, hashlib, urllib.request, urllib.error
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
RDIR = os.path.join(BASE, "reports")
os.makedirs(RDIR, exist_ok=True)

CITED = {
    "01fd9706-d9d0-42e4-b813-448a541a2571": "Transluce article body — Data USA SQLi probe api.datausa.io (foo=union select 1,2,3 from users), 2026-05-28",
    "d6669745-83d2-4628-82fa-87420ae6a5d7": "Transluce article body — Thai NSO / pastebin.k4be.pl linkage, 2026-03-11",
    "6fd6d3cb-2d66-408e-91e4-910352cc0cfc": "Transluce article body — Thrill Data theme parks, 2026-05-12",
    "c08684cc-3da4-4d53-a288-0d014243c075": "Transluce article footnote 5 — GET->POST bridge (httpbin.org)",
    "1ad9c2e8-96ff-44af-b446-b717bcb995b4": "Transluce article footnote 5 — GET->POST bridge milankarman.github.io/Embed-Web-Playground; ABSENT from frozen cache",
    "e044dea5-ca3b-4e3c-9083-f422148ffd77": "Transluce article footnote 5 — GET->POST bridge blogsflow.liftbrandfulfillment.com; ABSENT from frozen cache",
}

def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return -1, str(e).encode()

def main():
    results = {}
    now = datetime.now(timezone.utc).isoformat()
    for rid, note in CITED.items():
        live_url = f"https://urlquery.net/report/{rid}/json"
        status, body = fetch(live_url)
        src = "live"
        if status != 200 or len(body) < 200:
            # Wayback fallback
            wb = f"https://web.archive.org/web/2026id_/https://urlquery.net/report/{rid}/json"
            status, body = fetch(wb)
            src = "wayback" if status == 200 and len(body) > 200 else "unavailable"
        rec = {
            "report_id": rid,
            "cited_for": note,
            "retrieval_utc": now,
            "source": src,
            "http_status": status,
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest() if body and src != "unavailable" else None,
            "live_url": f"https://urlquery.net/report/{rid}",
        }
        if src != "unavailable":
            with open(os.path.join(RDIR, f"{rid}.json"), "wb") as f:
                f.write(body)
            try:
                j = json.loads(body)
                rec["submitted_url"] = j.get("url") or j.get("submitted_url")
                rec["scan_date"] = j.get("date") or j.get("scan_date")
            except Exception:
                pass
        results[rid] = rec
        print(rid, src, status, len(body), flush=True)
        time.sleep(22)  # urlquery rate-limits rapid JSON pulls; 20s+ spacing verified clean
    with open(os.path.join(BASE, "provenance_cited.json"), "w") as f:
        json.dump({"retrieval_utc": now, "method": "live urlquery.net/report/<id>/json first; web.archive.org fallback", "reports": results}, f, indent=2)

if __name__ == "__main__":
    main()
