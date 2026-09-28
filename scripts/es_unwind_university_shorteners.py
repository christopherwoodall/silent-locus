#!/usr/bin/env python3
"""Unwind consolidation violation: university-shorteners (workstream E, 2026-09-28).

VIOLATION: primary index `university-shorteners` holds 16 docs; 5 of them are
`yourls_stats_detail` docs that each bundle N per-URL referrer rows into one
doc (740 / 57 / 285 / 77 / 28 = 1,187 rows), plus 305 daily traffic points,
all collapsed inside slug-level summary docs.

UNWIND (staged; Elastic writes PAUSED until Christopher says resume):
  1. Create `university-shorteners-rollup` from the canonical mapping
     (notes/gems-es-mapping.json); bulk the 16 slug-summary docs with their
     ORIGINAL _ids; verify _count=16.
  2. Bulk the 1,492 explicit events into `university-shorteners`:
       - 1,187 shortener_referrer_row docs
         (_id = yourlsref:<instance>:<slug>:<sha16(host|url)>#<occurrence>)
       - 305 shortener_daily_hits docs
         (_id = yourlsdaily:<instance>:<slug>:<series>:<date>)
     verify _count=1508 (16+1492).
  3. Bulk-delete the 16 rollup _ids from `university-shorteners`;
     verify primary _count=1492, rollup _count=16.
  4. Field check: event.dataset.keyword present on both indexes.

Staged payloads (committed, on disk):
  data/university-shorteners/staged_primary/university-shorteners_explicit.jsonl (1492)
  data/university-shorteners/staged_rollup/university-shorteners-rollup.jsonl    (16)
Source of truth: the *_referrer_urls_daily_*.json evidence files (raw rows).

Usage:
  python3 scripts/es_unwind_university_shorteners.py --verify-only   # read-only checks
  python3 scripts/es_unwind_university_shorteners.py --execute       # performs the unwind
"""
import sys, json, os, urllib.request
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
try:
    from dynamic_credentials import add_surrogate_to_request, read_json_response
except ImportError:
    def add_surrogate_to_request(request, *a, **k): return None
    def read_json_response(response):
        import json as _j; return _j.load(response)

ES = os.environ.get("SWARMTRACES_ES_URL",
     "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443")
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PRIMARY = "university-shorteners"
ROLLUP = "university-shorteners-rollup"
PAUSE_SENTINEL = os.path.join(BASE, "notes", "ELASTIC_WRITE_PAUSE")
EXPLICIT = os.path.join(BASE, "data", "university-shorteners", "staged_primary",
                        "university-shorteners_explicit.jsonl")
ROLLUP_DOCS = os.path.join(BASE, "data", "university-shorteners", "staged_rollup",
                           "university-shorteners-rollup.jsonl")
EXPECTED_PRIMARY = 1492
EXPECTED_ROLLUP = 16


def req(method, path, body=None):
    r = urllib.request.Request(ES + path,
        data=json.dumps(body).encode() if body is not None else None, method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=120) as resp:
        return read_json_response(resp)


def count(idx):
    return req("GET", f"/{idx}/_count")["count"]


def bulk(docs, index):
    lines = []
    for d in docs:
        _id = d["_id"]
        src = d["_source"] if "_source" in d else {k: v for k, v in d.items() if k != "_id"}
        lines.append(json.dumps({"index": {"_index": index, "_id": _id}}))
        lines.append(json.dumps(src))
    data = "\n".join(lines) + "\n"
    r = urllib.request.Request(ES + "/_bulk", data=data.encode(), method="POST")
    r.add_header("Content-Type", "application/x-ndjson")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=300) as resp:
        res = read_json_response(resp)
    errs = [i for i in res["items"] if i["index"].get("error")]
    return len(res["items"]), errs


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--verify-only"
    if mode == "--execute" and os.path.exists(PAUSE_SENTINEL):
        sys.exit("REFUSED: notes/ELASTIC_WRITE_PAUSE exists. "
                 "Elastic writes are paused until Christopher says resume.")
    explicit = [json.loads(l) for l in open(EXPLICIT)]
    rollup = [json.loads(l) for l in open(ROLLUP_DOCS)]
    assert len(explicit) == EXPECTED_PRIMARY and len({d["_id"] for d in explicit}) == EXPECTED_PRIMARY
    assert len(rollup) == EXPECTED_ROLLUP and len({d["_id"] for d in rollup}) == EXPECTED_ROLLUP
    kinds = {}
    for d in explicit:
        kinds[d["record_kind"]] = kinds.get(d["record_kind"], 0) + 1
    assert kinds == {"shortener_referrer_row": 1187, "shortener_daily_hits": 305}, kinds
    if mode == "--verify-only":
        print(f"primary {PRIMARY} _count =", count(PRIMARY))
        try:
            print(f"rollup  {ROLLUP} _count =", count(ROLLUP))
        except Exception as e:
            print(f"rollup  {ROLLUP} missing ({type(e).__name__})")
        print("staged payloads OK: 1492 explicit (1187 referrer rows + 305 daily) + 16 rollup docs.")
        return
    if mode != "--execute":
        sys.exit("usage: --verify-only | --execute")
    mapping = json.load(open(os.path.join(BASE, "notes", "gems-es-mapping.json")))["mappings"]
    try:
        req("PUT", f"/{ROLLUP}", {"mappings": mapping})
        print("created", ROLLUP)
    except Exception as e:
        print("rollup index create skipped/exists:", str(e)[:120])
    n, errs = bulk(rollup, ROLLUP)
    assert not errs, errs[:3]
    assert count(ROLLUP) == EXPECTED_ROLLUP, count(ROLLUP)
    print("rollup bulked:", n, "count verified:", EXPECTED_ROLLUP)
    n, errs = bulk(explicit, PRIMARY)
    assert not errs, errs[:3]
    assert count(PRIMARY) == EXPECTED_PRIMARY + EXPECTED_ROLLUP, count(PRIMARY)
    print("primary bulked:", n, "interim count verified:", EXPECTED_PRIMARY + EXPECTED_ROLLUP)
    lines = []
    for d in rollup:
        lines.append(json.dumps({"delete": {"_index": PRIMARY, "_id": d["_id"]}}))
    r = urllib.request.Request(ES + "/_bulk", data=("\n".join(lines) + "\n").encode(), method="POST")
    r.add_header("Content-Type", "application/x-ndjson")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=300) as resp:
        res = read_json_response(resp)
    derrs = [i for i in res["items"] if i["delete"].get("error")]
    assert not derrs, derrs[:3]
    import time; time.sleep(2)
    assert count(PRIMARY) == EXPECTED_PRIMARY, count(PRIMARY)
    assert count(ROLLUP) == EXPECTED_ROLLUP, count(ROLLUP)
    for idx in (PRIMARY, ROLLUP):
        ag = req("POST", f"/{idx}/_search",
                 {"size": 0, "aggs": {"ds": {"terms": {"field": "event.dataset.keyword", "size": 10}}}})
        b = ag["aggregations"]["ds"]["buckets"]
        assert b and all(x["key"].startswith("university-shorteners") for x in b), (idx, b)
        print(idx, "event.dataset.keyword OK:", [x["key"] for x in b])
    print("UNWIND COMPLETE: primary=1492 explicit, rollup=16 summaries.")


if __name__ == "__main__":
    main()
