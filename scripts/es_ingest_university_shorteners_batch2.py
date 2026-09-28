#!/usr/bin/env python3
"""Ingest the university-shorteners-batch2 dataset into the `university-shorteners-batch2` index.

Source: data/university-shorteners-batch2/university-shorteners-batch2.jsonl (1 doc).
Idempotent: deterministic _id "yourls:<instance>:<slug>", re-runs overwrite.

Usage:
  python3 es_ingest_university_shorteners_batch2.py            # create index + bulk load
  python3 es_ingest_university_shorteners_batch2.py --verify  # count + mapping checks
"""
import sys, json, os, urllib.request
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DATA = BASE + "/data/university-shorteners-batch2"
INDEX = "university-shorteners-batch2"
EXPECTED_FIELDS = set(json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]["properties"])


def req(method, path, body=None, raw=None):
    url = ES + path
    data = raw.encode() if raw is not None else (
        json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=120) as resp:
        return read_json_response(resp)


def doc_id(d):
    inst = d["labels"]["shortener.instance"]
    slug = d["matched_string"].rstrip("/").split("/")[-1].split("?")[0]
    return "yourls:%s:%s" % (inst, slug)


def load_docs():
    docs = {}
    with open(DATA + "/university-shorteners-batch2.jsonl") as f:
        for line in f:
            line = line.strip()
            if line:
                d = json.loads(line)
                docs[doc_id(d)] = d
    return docs


def create_index():
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
    try:
        res = req("PUT", "/%s" % INDEX, {"mappings": mapping})
        print("index created:", res.get("acknowledged"))
    except Exception as e:
        body = e.read().decode() if hasattr(e, "read") else str(e)
        if "resource_already_exists_exception" in body:
            print("index exists; updating mapping")
            req("PUT", "/%s/_mapping" % INDEX, mapping)
        else:
            raise


def bulk_load(docs):
    items = list(docs.items())
    ok = fail = 0
    for i in range(0, len(items), 400):
        chunk = items[i:i + 400]
        nd = "".join(
            json.dumps({"index": {"_index": INDEX, "_id": _id}}) + "\n" +
            json.dumps(doc) + "\n" for _id, doc in chunk)
        res = req("POST", "/_bulk", raw=nd)
        for it in res.get("items", []):
            st = it.get("index", {}).get("status", 0)
            if st in (200, 201):
                ok += 1
            else:
                fail += 1
                print("BULK FAIL:", json.dumps(it)[:200])
    print("ingest done: ok=%d fail=%d" % (ok, fail))


def verify():
    c = req("GET", "/%s/_count" % INDEX)
    print("doc count:", c.get("count"))
    r = req("POST", "/%s/_search" % INDEX,
            {"size": 0, "aggs": {"datasets": {"terms": {"field": "event.dataset.keyword"}}}})
    b = r["aggregations"]["datasets"]["buckets"]
    print("event.dataset.keyword buckets:", [(x["key"], x["doc_count"]) for x in b])
    s = req("POST", "/%s/_search" % INDEX, {"size": 100, "_source": True})
    unexpected = set()
    for h in s["hits"]["hits"]:
        unexpected |= set(h["_source"]) - EXPECTED_FIELDS
    print("unexpected top-level fields:", sorted(unexpected) or "none")
    r = req("POST", "/%s/_search" % INDEX,
            {"size": 0, "aggs": {"kinds": {"terms": {"field": "record_kind"}}}})
    print("record_kind:", [(x["key"], x["doc_count"]) for x in r["aggregations"]["kinds"]["buckets"]])


def main():
    if "--verify" in sys.argv:
        verify()
        return
    create_index()
    docs = load_docs()
    print("docs to load:", len(docs))
    bulk_load(docs)
    verify()


if __name__ == "__main__":
    main()
