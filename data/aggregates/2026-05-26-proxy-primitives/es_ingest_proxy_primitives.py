#!/usr/bin/env python3
"""REBUILD SHIM — 2026-05-26-proxy-primitives (kept as es_ingest_proxy_primitives.py).

SUPERSESSION NOTICE (2026-09-29)
-------------------------------
The pre-2026-09-28 version of this script read a `hits.jsonl` whose per-hit
fields sat at TOP LEVEL (primitive, source, host, relation, wikis, n_agents,
hit_sha, context, first_seen_effective) and rebuilt ES docs from them.

The 2026-09-28/29 schema backfill moved every per-hit field under `labels.*`
(post-backfill labels.* dotted keys), kept per-row `record_kind`
(wiki_link / wiki_record_annotation / wiki_ioc_pivot / wiki_shortener /
wiki_revision / corpus_hit / gem_name_fragment), and adopted the identity
sha256 as top-level `fingerprint`. The old `to_doc()` field reads therefore
all returned None:

  * labels -> {} (primitive/source/host/relation/... all moved to labels.*)
  * fingerprint -> None (was h.get("hit_sha"), now top-level "fingerprint")
  * @timestamp -> dropped (was h.get("first_seen_effective"), now labels.*)
  * record_kind -> hardcoded "proxy_primitive_hit" (discards the per-row kind)
  * note -> None (was h.get("context"), now labels.context)

Any --load of the old build emits 1,522 DEGRADED docs that would corrupt the
index. The script is genuinely superseded by the canonical event stream:

    data/aggregates/2026-05-26-proxy-primitives/events.jsonl

which already validates against schema/record.schema.json and is staged
directly by the local loader (scripts/push_to_local_es.py auto-discovery;
no manifest via_script entry remains for this index).

Per Christopher's repair-don't-delete directive (2026-09-29), this file is
kept as a thin, documented rebuild-from-events.jsonl passthrough: it reads
events.jsonl, emits the rows VERBATIM (no transformation, no field reads),
validates them, and can bulk-load them. Default mode touches the network
not at all.

PAYLOAD NOTE: this collection has no raw/ layer — the only per-item
material is already inline (top-level `matched_string`, `labels.context`
on 9 rows). The single wiki_revision row's 1,398-byte revision body lives
in the upstream collusion-wiki corpus (see its doc_id/source_url) and is
not duplicated here. `event.payloads` is NOT used: record.schema.json
declares event with additionalProperties:false (created + dataset only), so
an extra sub-object would fail validation.

Usage:
  python3 es_ingest_proxy_primitives.py --emit /tmp/proxy-primitives-docs.jsonl
  python3 es_ingest_proxy_primitives.py --create   # create index w/ mapping
  python3 es_ingest_proxy_primitives.py --load     # bulk-load verbatim rows
  python3 es_ingest_proxy_primitives.py --verify   # count + record_kind agg
"""
import sys, json, urllib.request, subprocess
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

ES = os.environ.get("SWARMTRACES_ES_URL", "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443")
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
EVENTS = os.path.join(HERE, "events.jsonl")
INDEX = "2026-05-26-proxy-primitives"

# Updated 2026-09-29: covers the canonical fields actually present in
# events.jsonl (labels flattened, per-row record_kind, source_url, tags).
MAPPING = {
    "mappings": {
        "properties": {
            "@timestamp": {"type": "date"},
            "confidence": {"type": "keyword"},
            "description": {"type": "text"},
            "event": {"properties": {
                "created": {"type": "date"},
                "dataset": {"type": "keyword"}}},
            "fingerprint": {"type": "keyword"},
            "labels": {"type": "flattened"},
            "matched_string": {"type": "keyword", "ignore_above": 1024,
                               "fields": {"text": {"type": "text"}}},
            "note": {"type": "text"},
            "observer": {"properties": {
                "product": {"type": "keyword"},
                "type": {"type": "keyword"},
                "vendor": {"type": "keyword"}}},
            "record_kind": {"type": "keyword"},
            "source_url": {"type": "keyword", "ignore_above": 2048},
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

def build_docs():
    """Rebuild = read the canonical events verbatim. No field remapping."""
    docs = []
    with open(EVENTS) as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if line:
                docs.append(json.loads(line))
    return docs

def emit(path):
    docs = build_docs()
    with open(path, "w") as f:
        for d in docs:
            f.write(json.dumps(d) + "\n")
    print("wrote %d docs to %s" % (len(docs), path))
    # canonical validation (stdlib, repo schema)
    v = subprocess.run([sys.executable,
                        os.path.join(REPO_ROOT, "scripts", "validate_schema.py"),
                        path], capture_output=True, text=True)
    print(v.stdout.strip() or v.stderr.strip())
    if v.returncode != 0:
        raise SystemExit("schema validation FAILED")

def create():
    try:
        req("PUT", "/" + INDEX, MAPPING)
        print("index created")
    except Exception as e:
        print("create:", e)

def load():
    docs = build_docs()
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
            "kind": {"terms": {"field": "record_kind", "size": 20}},
            "prim": {"terms": {"field": "labels.primitive", "size": 10}}}})
    print(json.dumps(a["aggregations"], indent=1))

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--emit"
    if mode == "--emit":
        emit(sys.argv[2] if len(sys.argv) > 2 else "/tmp/proxy-primitives-docs.jsonl")
    else:
        {"--create": create, "--load": load, "--verify": verify}[mode]()
