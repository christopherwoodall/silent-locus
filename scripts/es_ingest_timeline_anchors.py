#!/usr/bin/env python3
"""Ingest the timeline-anchors lane dataset into its own `timeline-anchors` index.

Conforms to the shared schema (notes/gems-es-mapping.json): @timestamp,
event{created,dataset} (event.dataset has the .keyword multi-field at
creation), record_kind, description, source_url, confidence, observer, tags,
and dataset-specific fields in flattened `labels` only.
Zero new top-level fields.

Record flavors:
  timeline_anchor - one per dated cross-lane event (see data/timeline-anchors)

Usage:
  python3 es_ingest_timeline_anchors.py --create
  python3 es_ingest_timeline_anchors.py --load
  python3 es_ingest_timeline_anchors.py --verify
"""
import sys, json
from datetime import datetime, timezone
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
import urllib.request

ES = os.environ.get("SWARMTRACES_ES_URL", "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443")
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = "data/2026-03-07-timeline-anchors"
INDEX = "2026-03-07-timeline-anchors"
NOW = datetime.now(timezone.utc).isoformat()

MAPPING = {
    "mappings": {
        "properties": {
            "@timestamp": {"type": "date"},
            "confidence": {"type": "keyword"},
            "description": {"type": "text"},
            "event": {"properties": {
                "created": {"type": "date"},
                "dataset": {"type": "keyword",
                            "fields": {"keyword": {"type": "keyword",
                                                   "ignore_above": 256}}}}},
            "labels": {"type": "object", "dynamic": True},
            "observer": {"properties": {
                "product": {"type": "keyword"},
                "vendor": {"type": "keyword"},
                "type": {"type": "keyword"}}},
            "record_kind": {"type": "keyword"},
            "source_url": {"type": "keyword"},
            "tags": {"type": "keyword"},
        }
    }
}


def req(method, path, body=None):
    r = urllib.request.Request(ES + path,
                               data=json.dumps(body).encode() if body is not None else None,
                               method=method)
    r.add_header("Content-Type", "application/json")
    if ES.startswith(("http://localhost", "http://127.0.0.1", "http://[::1]")):
        _es_user = os.environ.get("ES_USER")
        if _es_user:
            import base64 as _b64
            r.add_header("Authorization", "Basic " + _b64.b64encode(
                f"{_es_user}:{os.environ.get('ES_PASS', '')}".encode()).decode())
    else:
        add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=180) as resp:
        return read_json_response(resp)


def docs():
    out = []
    for line in open(f"{BASE}/events.jsonl"):
        row = json.loads(line)
        _id = row.pop("_id")
        out.append((_id, row))
    return out


def create_index():
    print(req("PUT", f"/{INDEX}", MAPPING).get("acknowledged"))


def load():
    body = []
    for _id, doc in docs():
        body.append(json.dumps({"index": {"_index": INDEX, "_id": _id}}))
        body.append(json.dumps(doc))
    body = "\n".join(body) + "\n"
    r = urllib.request.Request(ES + f"/{INDEX}/_bulk", data=body.encode(), method="POST")
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
        res = read_json_response(resp)
    errs = [i for i in res["items"] if i["index"].get("status", 200) >= 300]
    print(f"total={len(res['items'])} errors={len(errs)}")
    for e in errs[:5]:
        print(json.dumps(e)[:400])


def verify():
    n = req("GET", f"/{INDEX}/_count")["count"]
    lines = sum(1 for _ in open(f"{BASE}/events.jsonl"))
    print(f"ES _count={n} jsonl lines={lines} match={n == lines}")
    m = req("GET", f"/{INDEX}/_mapping")[INDEX]["mappings"]["properties"]
    ed = m["event"]["properties"]["dataset"]
    print("event.dataset.keyword present:", "keyword" in ed.get("fields", {}))
    req("POST", f"/{INDEX}/_refresh")
    agg = req("POST", f"/{INDEX}/_search",
              {"size": 0, "aggs": {"clusters": {"terms": {"field": "labels.anchor_cluster.keyword", "size": 10}}}})
    print("anchor clusters:", {b["key"]: b["doc_count"] for b in agg["aggregations"]["clusters"]["buckets"]})


if __name__ == "__main__":
    if "--create" in sys.argv:
        create_index()
    elif "--load" in sys.argv:
        load()
    elif "--verify" in sys.argv:
        verify()
    else:
        print("usage: --create|--load|--verify")
