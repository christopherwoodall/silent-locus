#!/usr/bin/env python3
"""Ingest the Lane-E 83-gem June-18 reconciliation table into its own
`gem83-reconciliation` Elastic index, under the canonical shared schema
(notes/gems-es-mapping.json). Zero new top-level fields: reconciliation
fields land in existing `gem`, `package`, `labels`, `tags`, `note`,
`record_kind` concepts.

event.dataset.keyword multi-field included at creation (uniform with the
other campaign indices).

Usage: python3 es_ingest_gem83.py --create | --load | --verify
"""
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
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = REPO_ROOT
PDIR = SCRIPT_DIR
INDEX = "2026-09-28-gem83-reconciliation"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "gem83-reconciliation-ingest", "vendor": "nightingale-collective",
            "type": "dataset"}


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


def create_index():
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
    try:
        res = req("PUT", "/%s" % INDEX, {"mappings": mapping})
        print("created:", res.get("acknowledged"))
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        print("create failed:", str(e)[:200], body[:300])
        sys.exit(1)


def build_docs():
    docs = []
    for line in open(SCRIPT_DIR + "/raw/gem83-reconciliation.jsonl"):
        r = json.loads(line)
        doc = {
            "record_kind": "gem_reconciliation",
            "event": {"dataset": INDEX, "created": NOW},
            "observer": dict(OBSERVER),
            "gem": r["gem"],
            "package": r["gem"],
            "versions": r["jfrog_versions"],
            "xray_id": r["jfrog_xray_id"],
            "in_diffend_corpus": r["in_diffend_corpus"],
            "wave": "june-18",
            "labels": {
                "name_family": r["name_family"],
                "identification_source": r["identification_source"],
                "in_wayback_june_metadata": str(r["in_wayback_june_metadata"]),
                "in_wiki_gem_bridge": str(r["in_wiki_gem_bridge"]),
                "wayback_recovery_status": r["wayback_recovery_status"] or "none",
                "wiki_bridge_info": r["wiki_bridge_info"] or "",
            },
            "note": ("83-gem June-18 segment reconciliation. Identification: %s. "
                     "Wave/date inferred from name grammar + external reports "
                     "(JFrog GemStuffer report, thecolony.ai centaur post); "
                     "JFrog CSV carries no per-row dates." % r["identification_source"]),
            "tags": ["gem83", "june-18", "lane-e", "gemstuffer",
                     "wave:june-18", "in-jfrog",
                     "in-diffend" if r["in_diffend_corpus"] else "diffend-absent",
                     "wayback" if r["in_wayback_june_metadata"] else "wayback-absent",
                     "wiki-bridge" if r["in_wiki_gem_bridge"] else "wiki-bridge-absent"],
            "@timestamp": "2026-06-18T00:00:00Z",
        }
        docs.append(doc)
    return docs


def load():
    docs = build_docs()
    ok, fail = 0, 0
    for d in docs:
        try:
            req("POST", "/%s/_doc" % INDEX, d)
            ok += 1
        except Exception as e:
            fail += 1
            print("doc failed:", d["gem"], str(e)[:150])
    print("loaded ok=%d fail=%d" % (ok, fail))


def verify():
    r = req("GET", "/%s/_count" % INDEX)
    print("count:", r.get("count"))
    r = req("GET", "/%s/_search" % INDEX,
            {"size": 0, "aggs": {"in_diffend": {"terms": {"field": "in_diffend_corpus"}},
                                 "wiki_bridge": {"terms": {"field": "in_wiki_gem_bridge"}}}})
    print(json.dumps(r["aggregations"], indent=1))
    r = req("GET", "/%s/_mapping" % INDEX)
    props = r[INDEX]["mappings"]["properties"]
    print("event.dataset.keyword at creation:",
          "keyword" in props.get("event", {}).get("properties", {}).get("dataset", {}).get("fields", {}))


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--verify"
    if mode == "--create":
        create_index()
    elif mode == "--load":
        load()
    else:
        verify()
