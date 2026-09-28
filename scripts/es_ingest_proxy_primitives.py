#!/usr/bin/env python3
"""Ingest Lane-F proxy-primitive hits into the `proxy-primitives` ES index.

Conforms to the shared canonical schema (notes/gems-es-mapping.json):
wiki/gem concepts map onto existing fields; primitive-specific detail lives
in `labels` (flattened) + `tags`. event.dataset keyword multi-field is
declared at index creation.

Usage:
  python3 es_ingest_proxy_primitives.py --create   # create index w/ mapping
  python3 es_ingest_proxy_primitives.py --load     # bulk ingest hits.jsonl
  python3 es_ingest_proxy_primitives.py --verify   # count + per-primitive agg
"""
import sys, json, urllib.request
from datetime import datetime, timezone
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = "/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus"
HITS = BASE + "/data/proxy-primitives/hits.jsonl"
INDEX = "proxy-primitives"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "lane-f-proxy-sweep", "vendor": "hunt",
            "type": "transform"}

MAPPING = {
    "mappings": {
        "properties": {
            "@timestamp": {"type": "date"},
            "authors": {"type": "text", "fields": {"raw": {"type": "keyword"}}},
            "confidence": {"type": "keyword"},
            "event": {"properties": {
                "created": {"type": "date"},
                "dataset": {"type": "keyword",
                            "fields": {"keyword": {"type": "keyword",
                                                   "ignore_above": 256}}},
            }},
            "fingerprint": {"type": "keyword"},
            "gem": {"type": "keyword", "fields": {"text": {"type": "text"}}},
            "labels": {"type": "flattened"},
            "matched_string": {"type": "keyword", "ignore_above": 1024,
                               "fields": {"text": {"type": "text"}}},
            "note": {"type": "text"},
            "observer": {"properties": {
                "product": {"type": "keyword"},
                "type": {"type": "keyword"},
                "vendor": {"type": "keyword"}}},
            "published_at": {"type": "date"},
            "record_kind": {"type": "keyword"},
            "retrieved_via": {"type": "keyword"},
            "source_url": {"type": "keyword"},
            "tags": {"type": "keyword"},
        }
    }
}

def req(method, path, body=None, raw=None):
    url = ES + path
    data = raw.encode() if raw is not None else (
        json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=300) as resp:
        return read_json_response(resp)

def flat(d):
    out = {}
    for k, v in (d or {}).items():
        if v is None:
            continue
        if isinstance(v, bool):
            out[k] = "true" if v else "false"
        elif isinstance(v, (list, tuple)):
            out[k] = ", ".join(str(x) for x in v[:20])
        else:
            out[k] = str(v)
    return out

def to_doc(h):
    doc = {
        "record_kind": "proxy_primitive_hit",
        "event": {"dataset": INDEX, "created": NOW},
        "observer": dict(OBSERVER),
        "retrieved_via": "lane-f sweep (scripts/sweep_proxy_primitives.py + "
                         "scripts/extract_wiki_proxy_urls.py)",
        "fingerprint": h.get("hit_sha"),
        "matched_string": h.get("matched_string"),
        "tags": ["source:proxy-primitives",
                 "primitive:" + (h.get("primitive") or "unknown"),
                 "hit_source:" + (h.get("source") or "unknown")],
        "labels": flat({
            "primitive": h.get("primitive"),
            "hit_source": h.get("source"),
            "laundered_target": h.get("laundered_target"),
            "host": h.get("host"),
            "relation": h.get("relation"),
            "wikis": h.get("wikis"),
            "n_agents": h.get("n_agents"),
            "agents_sample": h.get("agents_sample"),
            "record_id": h.get("record_id"),
            "omitted_url_sha256": h.get("omitted_url_sha256"),
            "target_host": h.get("target_host"),
            "doc_id": h.get("doc_id"),
            "line_no": h.get("line_no"),
        }),
        "note": (h.get("context") or "")[:2000] or None,
    }
    ts = h.get("first_seen_effective") or h.get("first_seen")
    if ts:
        doc["@timestamp"] = ts
    return doc

def create():
    try:
        req("PUT", "/" + INDEX, MAPPING)
        print("index created")
    except Exception as e:
        print("create:", e)

def load():
    docs = []
    with open(HITS) as f:
        for line in f:
            line = line.strip()
            if line:
                docs.append(to_doc(json.loads(line)))
    print("bulk loading %d docs" % len(docs))
    for i in range(0, len(docs), 500):
        chunk = docs[i:i + 500]
        body = "".join('{"index":{}}\n' + json.dumps(d) + "\n" for d in chunk)
        r = req("POST", "/%s/_bulk" % INDEX, raw=body)
        if r.get("errors"):
            for it in r["items"]:
                if it["index"].get("error"):
                    print("BULK ERROR:", it["index"]["error"])
                    break
            raise SystemExit("bulk errors")
        print("  %d/%d" % (i + len(chunk), len(docs)))
    req("POST", "/%s/_refresh" % INDEX)
    print("done")

def verify():
    c = req("GET", "/%s/_count" % INDEX)
    print("count:", c["count"])
    a = req("GET", "/%s/_search" % INDEX, {
        "size": 0, "aggs": {
            "prim": {"terms": {"field": "tags", "include": "primitive:.*",
                               "size": 10}},
            "kind": {"terms": {"field": "record_kind", "size": 10}}}})
    print(json.dumps(a["aggregations"], indent=1))
    # event.dataset.keyword multi-field exists?
    m = req("GET", "/%s/_mapping" % INDEX)
    ds = m[INDEX]["mappings"]["properties"]["event"]["properties"]["dataset"]
    print("event.dataset mapping:", json.dumps(ds))

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--verify"
    {"--create": create, "--load": load, "--verify": verify}[mode]()
