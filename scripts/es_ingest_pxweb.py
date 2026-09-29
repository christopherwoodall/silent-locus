#!/usr/bin/env python3
"""Ingest Lane-N stats-API task-target hits into the `pxweb-national-stats` ES index.

Conforms to the canonical shared schema (notes/gems-es-mapping.json): all detail
lives in `labels` (flattened) + `tags`; record_kind=stats_api_target; zero
top-level fields beyond the mapping.

Idempotent (fixed 2026-09-28, workstream A): deterministic _id
"stats:<sha256(record_kind|matched_string|source_url)[:16]>", re-runs
overwrite instead of duplicating. The previous script revision used
auto-generated ES IDs (duplication risk) and had a dead `load()` path
(that sent an empty body); both are retired by this rewrite.

Usage:
  python3 es_ingest_pxweb.py --create   # create index w/ canonical mapping (idempotent)
  python3 es_ingest_pxweb.py --load     # bulk ingest data/2026-09-28-pxweb-national-stats/pxweb-national-stats.jsonl
  python3 es_ingest_pxweb.py --verify   # count + top-level field hygiene vs mapping
"""
import sys, json, hashlib, urllib.request
import os
try:
    sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
    from dynamic_credentials import add_surrogate_to_request, read_json_response
except ImportError:  # local run: no vault on this machine, plain HTTP(S) instead
    def add_surrogate_to_request(request, *args, **kwargs):
        return None
    def read_json_response(response):
        import json as _json
        return _json.load(response)

ES = os.environ.get("SWARMTRACES_ES_URL", "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443")
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = REPO_ROOT
HITS = BASE + "/data/2026-09-28-pxweb-national-stats/pxweb-national-stats.jsonl"
MAPPING_SRC = BASE + "/notes/gems-es-mapping.json"
INDEX = "2026-09-28-pxweb-national-stats"
MAPPING_KEYS = set(json.load(open(MAPPING_SRC))["mappings"]["properties"])


def req(method, path, body=None, raw=None):
    url = ES + path
    data = raw.encode() if raw is not None else (
        json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    if ES.startswith(("http://localhost", "http://127.0.0.1", "http://[::1]")):
        _es_user = os.environ.get("ES_USER")
        if _es_user:
            import base64 as _b64
            r.add_header("Authorization", "Basic " + _b64.b64encode(
                f"{_es_user}:{os.environ.get('ES_PASS', '')}".encode()).decode())
    else:
        add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=300) as resp:
        return read_json_response(resp)


def doc_id(d):
    key = "%s|%s|%s" % (d.get("record_kind", ""), d.get("matched_string", ""),
                        d.get("source_url", ""))
    return "stats:" + hashlib.sha256(key.encode()).hexdigest()[:16]


def create():
    # canonical shared schema: mapping section ONLY (the `index` key in the
    # notes file is the gems index name, not settings).
    mapping = json.load(open(MAPPING_SRC))["mappings"]
    try:
        out = req("PUT", "/" + INDEX, {"mappings": mapping})
        print("index created:", json.dumps(out)[:200])
    except Exception as e:
        body = e.read().decode() if hasattr(e, "read") else str(e)
        if "resource_already_exists_exception" in body:
            print("index exists; updating mapping")
            req("PUT", "/%s/_mapping" % INDEX, mapping)
        else:
            raise


def load():
    docs = [json.loads(l) for l in open(HITS) if l.strip()]
    ids = [doc_id(d) for d in docs]
    assert len(set(ids)) == len(ids), "doc ID collision!"
    ok = fail = 0
    for i in range(0, len(docs), 250):
        body = ""
        for d, _id in zip(docs[i:i + 250], ids[i:i + 250]):
            body += json.dumps({"index": {"_index": INDEX, "_id": _id}}) + "\n"
            body += json.dumps(d) + "\n"
        r = urllib.request.Request(ES + "/_bulk", data=body.encode(), method="POST")
        r.add_header("Content-Type", "application/x-ndjson")
        if ES.startswith(("http://localhost", "http://127.0.0.1", "http://[::1]")):
            _es_user = os.environ.get("ES_USER")
            if _es_user:
                import base64 as _b64
                r.add_header("Authorization", "Basic " + _b64.b64encode(
                    f"{_es_user}:{os.environ.get('ES_PASS', '')}".encode()).decode())
        else:
            add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
        with urllib.request.urlopen(r, timeout=300) as resp:
            out = read_json_response(resp)
        if out.get("errors"):
            for it in out["items"]:
                if "error" in it.get("index", {}):
                    print("ERR", json.dumps(it["index"]["error"])[:300])
                    fail += 1
                    break
        else:
            ok += len(docs[i:i + 250])
    print("indexed ok=%d fail=%d" % (ok, fail))


def verify():
    out = req("GET", "/" + INDEX + "/_count")
    print("count:", out["count"])
    out = req("POST", "/" + INDEX + "/_search",
              {"size": 50, "query": {"match_all": {}}})
    unexpected = set()
    for h in out["hits"]["hits"]:
        unexpected |= (set(h["_source"].keys()) - MAPPING_KEYS)
    print("unexpected top-level fields:", sorted(unexpected) or "none")
    r = req("POST", "/" + INDEX + "/_search",
            {"size": 0, "aggs": {"kinds": {"terms": {"field": "record_kind"}}}})
    print("record_kind:", [(x["key"], x["doc_count"]) for x in r["aggregations"]["kinds"]["buckets"]])
    print("hits:", len(out["hits"]["hits"]), "unique IDs:",
          len({h["_id"] for h in out["hits"]["hits"]}))


if __name__ == "__main__":
    if sys.argv[1] == "--create":
        create()
    elif sys.argv[1] == "--load":
        load()
    elif sys.argv[1] == "--verify":
        verify()
