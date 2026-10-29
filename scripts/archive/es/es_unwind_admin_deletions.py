#!/usr/bin/env python3
"""Unwind consolidation violation: admin-deletions (workstream E, 2026-09-28).

VIOLATION: primary index `admin-deletions` holds 26 per-day summary docs
(record_kind=admin_cleanup_burst); the 5,217 verbatim delete events in
data/2026-06-04-admin-deletions/raw/hits.jsonl were never indexed.

UNWIND (staged; Elastic writes PAUSED until Christopher says resume):
  1. Create `admin-deletions-rollup` from the canonical mapping
     (notes/gems-es-mapping.json); bulk the 26 per-day docs with their
     ORIGINAL _ids; verify _count=26.
  2. Bulk the 5,217 explicit delete events into `admin-deletions`
     (deterministic _id = event_id); verify _count=5243 (26+5217).
  3. Bulk-delete the 26 rollup _ids from `admin-deletions`;
     verify primary _count=5217, rollup _count=26.
  4. Field check: event.dataset.keyword present on both indexes.

Staged payloads (committed, on disk):
  data/2026-06-04-admin-deletions/events.jsonl (5217)
  data/2026-06-04-admin-deletions/raw/admin-deletions-rollup.jsonl    (26)

Usage:
  python3 scripts/es_unwind_admin_deletions.py --verify-only   # read-only checks
  python3 scripts/es_unwind_admin_deletions.py --execute       # performs the unwind
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
PRIMARY = "2026-06-04-admin-deletions"
ROLLUP = "2026-06-04-admin-deletions-rollup"
PAUSE_SENTINEL = os.path.join(BASE, "notes", "ELASTIC_WRITE_PAUSE")
EXPLICIT = os.path.join(BASE, "data", "2026-06-04-admin-deletions",
                        "events.jsonl")
ROLLUP_DOCS = os.path.join(BASE, "data", "2026-06-04-admin-deletions", "raw",
                           "admin-deletions-rollup.jsonl")
EXPECTED_PRIMARY = 5217
EXPECTED_ROLLUP = 26


def req(method, path, body=None):
    r = urllib.request.Request(ES + path,
        data=json.dumps(body).encode() if body is not None else None, method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=120) as resp:
        return read_json_response(resp)


def count(idx):
    return req("GET", f"/{idx}/_count")["count"]


def bulk(docs, index, id_key="_id"):
    lines = []
    for d in docs:
        _id = d[id_key]
        src = {k: v for k, v in d.items() if k != "_id"}
        if "_source" in d:  # rollup export shape {"_id":..., "_source":...}
            src = d["_source"]
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
    if mode == "--verify-only":
        print(f"primary {PRIMARY} _count =", count(PRIMARY))
        try:
            print(f"rollup  {ROLLUP} _count =", count(ROLLUP))
        except Exception as e:
            print(f"rollup  {ROLLUP} missing ({type(e).__name__})")
        print("staged payloads OK: 5217 explicit + 26 rollup docs, ids unique.")
        return
    if mode != "--execute":
        sys.exit("usage: --verify-only | --execute")
    # 1. rollup index + docs
    mapping = json.load(open(os.path.join(BASE, "notes", "gems-es-mapping.json")))["mappings"]
    try:
        req("PUT", f"/{ROLLUP}", {"mappings": mapping})
        print("created", ROLLUP)
    except Exception as e:
        print("rollup index create skipped/exists:", str(e)[:120])
    n, errs = bulk(rollup, ROLLUP)
    assert not errs, errs[:3]
    req("POST", f"/{ROLLUP}/_refresh")
    assert count(ROLLUP) == EXPECTED_ROLLUP, count(ROLLUP)
    print("rollup bulked:", n, "count verified:", EXPECTED_ROLLUP)
    # 2. explicit events into primary
    n, errs = bulk(explicit, PRIMARY)
    assert not errs, errs[:3]
    req("POST", f"/{PRIMARY}/_refresh")
    assert count(PRIMARY) == EXPECTED_PRIMARY + EXPECTED_ROLLUP, count(PRIMARY)
    print("primary bulked:", n, "interim count verified:", EXPECTED_PRIMARY + EXPECTED_ROLLUP)
    # 3. remove rollup docs from primary (delete by deterministic _ids)
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
    req("POST", f"/{PRIMARY}/_refresh")
    req("POST", f"/{ROLLUP}/_refresh")
    assert count(PRIMARY) == EXPECTED_PRIMARY, count(PRIMARY)
    assert count(ROLLUP) == EXPECTED_ROLLUP, count(ROLLUP)
    # 4. field check
    for idx in (PRIMARY, ROLLUP):
        ag = req("POST", f"/{idx}/_search",
                 {"size": 0, "aggs": {"ds": {"terms": {"field": "event.dataset.keyword", "size": 5}}}})
        b = ag["aggregations"]["ds"]["buckets"]
        assert b and b[0]["key"] == "2026-06-04-admin-deletions", (idx, b)
        print(idx, "event.dataset.keyword OK:", [x["key"] for x in b])
    print("UNWIND COMPLETE: primary=5217 explicit, rollup=26 summaries.")


if __name__ == "__main__":
    main()
