#!/usr/bin/env python3
"""Ingest Lane-N stats-API task-target hits into the `pxweb-national-stats` ES index.

Conforms to the canonical shared schema (notes/gems-es-mapping.json): all detail
lives in `labels` (flattened) + `tags`; record_kind=stats_api_target; zero
top-level fields beyond the mapping.

Usage:
  python3 es_ingest_pxweb.py --create   # create index w/ canonical mapping
  python3 es_ingest_pxweb.py --load     # bulk ingest data/pxweb-national-stats/hits.jsonl
  python3 es_ingest_pxweb.py --verify   # count + top-level field hygiene vs mapping
"""
import sys, json, urllib.request
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = "/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus"
HITS = BASE + "/data/pxweb-national-stats/hits.jsonl"
MAPPING_SRC = BASE + "/notes/gems-es-mapping.json"
INDEX = "pxweb-national-stats"

def req(method, path, body=None):
    url = ES + path
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=300) as resp:
        return read_json_response(resp)

def create():
    mapping = json.load(open(MAPPING_SRC))["mappings"]  # canonical shared schema
    body = {"mappings": mapping["mappings"] if "mappings" in mapping else mapping}
    out = req("PUT", "/" + INDEX, body)
    print(json.dumps(out)[:200])

def load():
    docs = [json.loads(l) for l in open(HITS)]
    n = 0
    for i in range(0, len(docs), 250):
        bulk = ""
        for d in docs[i:i+250]:
            bulk += json.dumps({"index": {"_index": INDEX}}) + "\n" + json.dumps(d) + "\n"
        out = req("POST", "/_bulk", None)
        # send raw bulk body
        n += len(docs[i:i+250])
    print("queued", n)

def load_raw():
    docs = [json.loads(l) for l in open(HITS)]
    n = 0
    for i in range(0, len(docs), 250):
        body = ""
        for d in docs[i:i+250]:
            body += json.dumps({"index": {"_index": INDEX}}) + "\n" + json.dumps(d) + "\n"
        url = ES + "/_bulk"
        r = urllib.request.Request(url, data=body.encode(), method="POST")
        r.add_header("Content-Type", "application/x-ndjson")
        add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
        with urllib.request.urlopen(r, timeout=300) as resp:
            out = read_json_response(resp)
        if out.get("errors"):
            for it in out["items"]:
                if "error" in it.get("index", {}):
                    print("ERR", it["index"]["error"])
                    break
        n += len(docs[i:i+250])
    print("indexed", n)

def verify():
    out = req("GET", "/" + INDEX + "/_count")
    print("count:", out["count"])
    mapping = json.load(open(MAPPING_SRC))["mappings"]["properties"]
    allowed = set(mapping.keys()) | {"_index", "_id", "_score", "_source", "sort"}
    out = req("POST", "/" + INDEX + "/_search",
              {"size": 50, "query": {"match_all": {}}})
    unexpected = set()
    for h in out["hits"]["hits"]:
        unexpected |= (set(h["_source"].keys()) - set(mapping.keys()))
    print("unexpected top-level fields:", sorted(unexpected) or "none")

if __name__ == "__main__":
    if sys.argv[1] == "--create": create()
    elif sys.argv[1] == "--load": load_raw()
    elif sys.argv[1] == "--verify": verify()
