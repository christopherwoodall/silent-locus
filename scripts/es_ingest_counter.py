#!/usr/bin/env python3
"""Ingest the countapi.mileshilliard.com counter-channel snapshot into its own
`counter-channel` index.

Read-only: named-key GETs only (no increments, no creates). Conforms to the
shared schema (notes/gems-es-mapping.json): detail in `labels` + `tags`.
No new top-level fields.

Usage:
  python3 es_ingest_counter.py --create   # create index with canonical mapping
  python3 es_ingest_counter.py --load     # bulk-load the docs
  python3 es_ingest_counter.py --verify   # count
"""
import sys, json, os, hashlib, urllib.request
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
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = REPO_ROOT
D = BASE + "/data/counter-channel"
INDEX = "counter-channel"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "counter-channel-ingest", "vendor": "swarmtraces-hunt",
            "type": "dataset"}
MAPPING_URL = f"{BASE}/notes/gems-es-mapping.json"


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
    with urllib.request.urlopen(r, timeout=180) as resp:
        return read_json_response(resp)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_docs():
    docs = {}
    ts = "2026-09-28T03:35:00Z"
    snap = json.load(open(f"{D}/snapshot_2026-09-27.json"))
    for key, info in snap["keys"].items():
        docs[f"counter:{key}"] = {
            "@timestamp": ts,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "counter_reading",
            "description": (
                f"countapi.mileshilliard.com counter '{key}' = {info['value']} "
                f"(HTTP {info['http']}, {info['retrieved_at_utc']}). "
                f"CA/TX match the 2026-09-04 investigator report (4/2); "
                f"ZZ=2 on the documented-fake key shows the channel is being "
                f"poked. Read-only GET; no writes made."),
            "source_url": f"https://countapi.mileshilliard.com/api/v1/get/{key}",
            "observer": OBSERVER,
            "tags": ["kind:counter", "surface:counter-channel",
                     f"key:{key}", f"value:{info['value']}"],
            "labels": {
                "counter_key": key,
                "counter_value": str(info["value"]),
                "http_status": str(info["http"]),
                "retrieved_at_utc": info["retrieved_at_utc"],
                "read_only": "true",
            },
        }
    docs["counter:sibling_probe"] = {
        "@timestamp": ts,
        "event": {"dataset": INDEX, "created": NOW},
        "record_kind": "counter_probe",
        "description": (
            "Sibling-key enumeration (read-only GET, 12 candidates): bare "
            "langr5backup4813 + state suffixes NY/FL/WA/OR/IL/OH/PA/GA/MA/US "
            "+ ALL — all 404 'Key not found'. The campaign key family is "
            "exactly the 3 known keys (CA, TX, ZZ). No namespace/info "
            "endpoints exist on this countapi clone (both 404)."),
        "source_url": "https://countapi.mileshilliard.com/api/v1/get/",
        "observer": OBSERVER,
        "tags": ["kind:probe", "surface:counter-channel", "result:all-miss"],
        "labels": {
            "probed_keys": "12",
            "hits": "0",
            "read_only": "true",
        },
    }
    return docs


def cmd_create():
    m = json.load(open(MAPPING_URL))
    try:
        req("DELETE", f"/{INDEX}")
        print("deleted existing index")
    except Exception as e:
        print("no existing index:", str(e)[:80])
    r = req("PUT", f"/{INDEX}", {"mappings": m["mappings"]})
    print("created:", r.get("acknowledged"))


def cmd_load():
    docs = build_docs()
    ndjson = "".join(
        json.dumps({"index": {"_index": INDEX, "_id": k}}) + "\n"
        + json.dumps(v) + "\n" for k, v in docs.items())
    r = req("POST", "/_bulk", raw=ndjson)
    ok = sum(1 for it in r.get("items", [])
             if it.get("index", {}).get("status") in (200, 201))
    print(f"loaded {ok}/{len(docs)}")


def cmd_verify():
    r = req("GET", f"/{INDEX}/_count")
    print("count:", r.get("count"))


if __name__ == "__main__":
    if "--create" in sys.argv:
        cmd_create()
    elif "--load" in sys.argv:
        cmd_load()
    elif "--verify" in sys.argv:
        cmd_verify()
    else:
        print("usage: --create | --load | --verify")
