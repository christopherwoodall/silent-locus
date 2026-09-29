#!/usr/bin/env python3
"""Ingest the Lane-S open-data-api-venues dataset into its own
`open-data-api-venues` Elastic index, under the canonical shared schema
(notes/gems-es-mapping.json). Zero new top-level fields.

event.dataset.keyword multi-field included at creation (uniform with the
other hunt indices).

Usage: python3 es_ingest_open_data_api_venues.py --create | --load | --verify
"""
import json, sys, urllib.request

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
PDIR = BASE + "/data/2026-09-28-open-data-api-venues"
INDEX = "2026-09-28-open-data-api-venues"


def req(method, path, body=None):
    url = ES + path
    data = json.dumps(body).encode() if body is not None else None
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


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--verify"
    if mode == "--create":
        mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
        res = req("PUT", "/%s" % INDEX, {"mappings": mapping})
        print("created:", res.get("acknowledged"))
    elif mode == "--load":
        docs = [json.loads(l) for l in open(PDIR + "/hits.jsonl")]
        allowed = set(json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]["properties"])
        ok, fail = 0, 0
        for d in docs:
            extra = set(d) - allowed
            if extra:
                fail += 1
                print("SCHEMA DRIFT:", extra)
                continue
            try:
                req("POST", "/%s/_doc" % INDEX, d)
                ok += 1
            except Exception as e:
                fail += 1
                print("doc failed:", d.get("matched_string", "")[:60], str(e)[:150])
        print("loaded ok=%d fail=%d" % (ok, fail))
    elif mode == "--verify":
        n_jsonl = sum(1 for _ in open(PDIR + "/hits.jsonl"))
        res = req("GET", "/%s/_count" % INDEX)
        n_es = res["count"]
        print("jsonl=%d es=%d match=%s" % (n_jsonl, n_es, n_jsonl == n_es))
        # top-level field hygiene: sample 5 docs
        res = req("GET", "/%s/_search" % INDEX, {"size": 5, "_source": True})
        allowed = set(json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]["properties"])
        drift = set()
        for h in res["hits"]["hits"]:
            drift |= set(h["_source"]) - allowed
        print("top-level drift:", drift or "none")
    else:
        sys.exit("usage: --create | --load | --verify")


main()
