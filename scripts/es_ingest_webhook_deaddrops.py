#!/usr/bin/env python3
"""Ingest Lane-K webhook dead-drop marker sweep into NEW index `webhook-deaddrops`.

Source: data/webhook-deaddrops/webhook-deaddrop-hits-2026-09-27.jsonl (8 docs).
Schema: shared canonical schema (notes/gems-es-mapping.json) + `marker` and
`evidence_level` keywords, with `event.dataset.keyword` multi-field at creation.

Idempotent: deterministic _id from doc_id, re-runs overwrite.

Usage:
  python3 es_ingest_webhook_deaddrops.py            # create index + bulk load
  python3 es_ingest_webhook_deaddrops.py --verify   # count + sample docs only
"""
import sys, json, urllib.request
from datetime import datetime, timezone
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = "/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus"
INDEX = "webhook-deaddrops"
HITS = BASE + "/data/webhook-deaddrops/webhook-deaddrop-hits-2026-09-27.jsonl"
SCHEMA = BASE + "/notes/gems-es-mapping.json"


def req(method, path, body=None, raw=None):
    url = ES + path
    data = raw.encode() if raw is not None else (
        json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=120) as resp:
        return read_json_response(resp)


def build_mapping():
    mapping = json.load(open(SCHEMA))["mappings"]
    props = mapping["properties"]
    # lane-K additions on top of the shared schema
    props["marker"] = {"type": "keyword"}
    props["evidence_level"] = {"type": "keyword"}
    props["matched_pattern"] = {"type": "keyword"}
    props["jfrog_xray_id"] = {"type": "keyword"}
    props["in_corpus_harvest"] = {"type": "boolean"}
    # belt-and-braces: ensure event.dataset.keyword multi-field exists at creation
    ev = props.setdefault("event", {"properties": {}})["properties"]
    ev.setdefault("created", {"type": "date"})
    ds = ev.setdefault("dataset", {"type": "keyword"})
    ds.setdefault("fields", {})["keyword"] = {"type": "keyword",
                                              "ignore_above": 256}
    return mapping


def create_index():
    try:
        req("GET", "/%s" % INDEX)
        print("index %s exists; PUT mapping to merge" % INDEX)
        req("PUT", "/%s/_mapping" % INDEX, build_mapping())
        return
    except Exception:
        pass
    res = req("PUT", "/%s" % INDEX, {"mappings": build_mapping()})
    print("index created:", res.get("acknowledged"))


def load_docs():
    docs = {}
    with open(HITS) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            doc = json.loads(line)
            doc_id = doc.pop("doc_id")
            docs[doc_id] = doc
    return docs


def bulk_load(docs):
    items = list(docs.items())
    total_ok, total_fail = 0, 0
    for i in range(0, len(items), 400):
        chunk = items[i:i + 400]
        nd = "".join(
            json.dumps({"index": {"_index": INDEX, "_id": _id}}) + "\n" +
            json.dumps(doc) + "\n" for _id, doc in chunk)
        res = req("POST", "/_bulk", raw=nd)
        for it in res.get("items", []):
            st = it.get("index", {}).get("status", 0)
            if st in (200, 201):
                total_ok += 1
            else:
                total_fail += 1
                print("BULK FAIL:", json.dumps(it)[:200])
        print("bulk progress: %d/%d ok=%d fail=%d" %
              (i + len(chunk), len(items), total_ok, total_fail))
    return total_ok, total_fail


def verify():
    c = req("GET", "/%s/_count" % INDEX)
    print("doc count:", c.get("count"))
    r = req("POST", "/%s/_search" % INDEX,
            {"size": 0, "aggs": {"by_kind": {"terms": {"field": "record_kind"}}}})
    print("by record_kind:",
          {b["key"]: b["doc_count"]
           for b in r["aggregations"]["by_kind"]["buckets"]})
    # confirm the event.dataset.keyword multi-field exists
    m = req("GET", "/%s/_mapping" % INDEX)
    kw = m[INDEX]["mappings"]["properties"]["event"]["properties"][
        "dataset"].get("fields", {})
    print("event.dataset multi-fields:", list(kw.keys()))
    s = req("POST", "/%s/_search" % INDEX,
            {"size": 8, "_source": ["record_kind", "gem", "wave", "marker",
                                   "evidence_level", "published_at"],
             "query": {"match_all": {}}})
    for h in s["hits"]["hits"]:
        print(h["_id"], json.dumps(h["_source"]))


def main():
    if "--verify" in sys.argv:
        verify()
        return
    create_index()
    docs = load_docs()
    print("docs to load:", len(docs))
    ok, fail = bulk_load(docs)
    print("DONE ok=%d fail=%d" % (ok, fail))
    verify()


if __name__ == "__main__":
    main()
