#!/usr/bin/env python3
"""Push rmn.re decoded link table to ES index rmn-re-linktable (shared schema)."""
import json, sys, urllib.request
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
INDEX = "rmn-re-linktable"
SRC = REPO_ROOT + "/data/rmn-re/link_table_decoded_2026-09-27.json"

def req(method, path, body=None):
    r = urllib.request.Request(ES + path,
        data=json.dumps(body).encode() if body is not None else None, method=method)
    r.add_header("Content-Type", "application/json")
    if ES.startswith(("http://localhost", "http://127.0.0.1", "http://[::1]")):
        _es_user = os.environ.get("ES_USER")
        if _es_user:
            import base64 as _b64
            r.add_header("Authorization", "Basic " + _b64.b64encode(
                f"{_es_user}:{os.environ.get('ES_PASS', '')}".encode()).decode())
    else:
        add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=120) as resp:
        return read_json_response(resp)

def parse_ts(s):
    # "Sep 25, 2026 12:28"
    try:
        return datetime.strptime(s, "%b %d, %Y %H:%M").replace(
            tzinfo=timezone.utc).isoformat()
    except Exception:
        return None

def doc(l):
    now = datetime.now(timezone.utc).isoformat()
    tags = ["source:rmn-re", f"status:{l['status']}"]
    tags += [f"grammar:{g}" for g in l["grammars"]]
    tags += [f"proxy:{w}" for w in l["chain_wrappers"]]
    if l["board_markers"]:
        tags.append("board-surface")
    return {
        "@timestamp": parse_ts(l.get("created")) or now,
        "event": {"dataset": "rmn-re-linktable", "created": now},
        "record_kind": "shortlink",
        "package": l["slug"],
        "source_url": f"https://rmn.re/{l['slug']}",
        "description": l["target"],
        "meta_description": l["decoded_target"],
        "labels": {
            "clicks": l["clicks"],
            "creator_ip16": l["creator_ip16"],
            "chain_depth": l["chain_depth"],
            "chain_wrappers": ",".join(l["chain_wrappers"]),
            "final_encodings": ",".join(l["final_encodings"]),
            "grammars": ",".join(l["grammars"]),
            "link_status": l["status"],
        },
        "tags": tags,
        "observer": {"product": "rmn-re-linktable-crawl", "vendor": "hunt",
                     "type": "dataset"},
        "retrieved_via": "https://rmn.re/admin/",
        "retrieved_at": now,
    }

def main():
    rows = json.load(open(SRC))
    print("mapping:", req("PUT", f"/{INDEX}", {"mappings": json.load(
        open(REPO_ROOT + "/notes/gems-es-mapping.json"))["mappings"]}).get("acknowledged"))
    bulk = []
    for l in rows:
        d = doc(l)
        bulk.append(json.dumps({"index": {"_index": INDEX, "_id": f"rmn:{l['slug']}"}}))
        bulk.append(json.dumps(d))
    body = "\n".join(bulk) + "\n"
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
        res = read_json_response(resp)
    errs = [i for i in res["items"] if i["index"].get("error")]
    print(f"indexed {len(rows)}, errors {len(errs)}")
    for e in errs[:3]:
        print(json.dumps(e["index"]["error"])[:200])
    print("count:", req("GET", f"/{INDEX}/_count")["count"])

main()
