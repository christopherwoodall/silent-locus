#!/usr/bin/env python3
"""Lane 23 expansion B: grep frozen urlquery cache (read-only) for TTP-adjacent indicators."""
import json, os, glob, gzip, re, sys

CACHE = os.path.expanduser("~/workspace/muse-home/projects/urlquery-api-hunt/artifacts/raw")
INDICATORS = {
    "beacon_setsid": [r"setsid"],
    "beacon_nohup": [r"nohup"],
    "wiki_wikiservice": [r"wikiservice\.at"],
    "unm_nmdigital": [r"nmdigital\.unm\.edu"],
    "unm_tok_expt": [r"tok=expt"],
    "aihw_pp": [r"pp\.aihw\.gov\.au"],
    "bridge_milankarman": [r"milankarman\.github\.io"],
    "bridge_blogsflow": [r"blogsflow\.liftbrandfulfillment"],
    "disposable_mailgw": [r"mail\.gw"],
    "xss_xssmark": [r"XSSMARK"],
    "prng_random": [r"random\.Random"],
    "yourls_rmnre": [r"rmn\.re"],
}

def load_records(path):
    try:
        opener = gzip.open if path.endswith(".gz") else open
        with opener(path, "rt", encoding="utf-8", errors="replace") as f:
            d = json.load(f)
        if isinstance(d, dict):
            for k in ("reports", "rows", "data", "items"):
                if isinstance(d.get(k), list):
                    return d[k]
            return []
        return d if isinstance(d, list) else []
    except Exception as e:
        return []

def rid_of(r):
    for k in ("report_id", "id", "uuid"):
        if r.get(k):
            return str(r[k])
    return None

def main():
    files = sorted(glob.glob(os.path.join(CACHE, "*.json"))) + sorted(glob.glob(os.path.join(CACHE, "*.json.gz")))
    hits = {name: [] for name in INDICATORS}
    seen = set()
    n = 0
    for path in files:
        for r in load_records(path):
            rid = rid_of(r)
            if not rid or rid in seen:
                continue
            seen.add(rid)
            n += 1
            blob = json.dumps(r, ensure_ascii=False)
            for name, pats in INDICATORS.items():
                if any(re.search(p, blob, re.I) for p in pats):
                    hits[name].append({
                        "report_id": rid,
                        "url": r.get("url") or r.get("submitted_url"),
                        "final_url": r.get("final_url"),
                        "date": r.get("date") or r.get("scan_date"),
                    })
    print(f"scanned {n} unique reports across {len(files)} files")
    out = {k: {"count": len(v), "sample": v[:25]} for k, v in hits.items()}
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "expansion", "cache_indicator_hits.json"), "w") as f:
        json.dump(out, f, indent=2)
    for k, v in hits.items():
        print(f"{k}: {len(v)}")

if __name__ == "__main__":
    main()
