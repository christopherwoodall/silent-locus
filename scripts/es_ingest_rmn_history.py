#!/usr/bin/env python3
"""Ingest the rmn.re history reconstruction into its own `rmn-re-history` index.

One ES doc per slug (764): YOURLS-authoritative creation date, June-log
membership, campaign grammar, target host, clicks. Conforms to the shared
schema (notes/gems-es-mapping.json); no new top-level fields.

Usage:
  python3 es_ingest_rmn_history.py --create
  python3 es_ingest_rmn_history.py --load
  python3 es_ingest_rmn_history.py --verify
"""
import sys, json, urllib.request
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
D = BASE + "/data/rmn-re-history"
INDEX = "rmn-re-history"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "rmn-re-history-ingest", "vendor": "swarmtraces-hunt",
            "type": "dataset"}


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


def build_docs():
    docs = {}
    for line in open(f"{D}/slug_evolution.jsonl"):
        e = json.loads(line)
        tags = ["in_june_log" if e["in_june_log"] else "not_in_june_log"]
        tags.append(f"grammar:{e['grammar']}")
        desc = (f"rmn.re short link '{e['slug']}' -> {e['target_host']} "
                f"(created {e['created']}, {e['clicks']} clicks). "
                f"{'Present in the preserved June-2026 log.' if e['in_june_log'] else 'Not in the June-2026 log (organic link).'}")
        labels = {
            "slug": e["slug"], "created": e["created"],
            "grammar": e["grammar"], "target_host": e["target_host"],
            "clicks": str(e["clicks"]), "creator_ip16": e["creator_ip16"],
            "in_june_log": str(e["in_june_log"]).lower(),
        }
        doc = {
            "@timestamp": e["created"],
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "rmn_re_slug",
            "description": desc,
            "source_url": f"https://rmn.re/{e['slug']}",
            "observer": OBSERVER,
            "tags": tags,
            "labels": labels,
        }
        docs[f"rmn-re-history:{e['slug']}"] = doc
    return docs


def create_index():
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
    try:
        req("DELETE", f"/{INDEX}")
        print("deleted existing index")
    except Exception as e:
        print("no existing index:", str(e)[:80])
    r = req("PUT", f"/{INDEX}", {"mappings": mapping})
    print("created:", r.get("acknowledged"))


def load():
    docs = build_docs()
    lines = []
    for _id, doc in docs.items():
        lines.append(json.dumps({"index": {"_index": INDEX, "_id": _id}}))
        lines.append(json.dumps(doc))
    r = req("POST", "/_bulk", raw="\n".join(lines) + "\n")
    errs = [i for i in r.get("items", []) if i.get("index", {}).get("error")]
    print(f"bulk: {len(docs)} docs, errors: {len(errs)}")
    for e in errs[:3]:
        print(json.dumps(e)[:300])


def verify():
    r = req("POST", f"/{INDEX}/_search",
            {"size": 0, "aggs": {
                "grammar": {"terms": {"field": "tags"}},
                "inlog": {"terms": {"field": "labels.in_june_log"}}}})
    print("total:", r["hits"]["total"]["value"])
    for b in r["aggregations"]["grammar"]["buckets"][:8]:
        print(f"  {b['key']}: {b['doc_count']}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--verify"
    {"--create": create_index, "--load": load, "--verify": verify}[mode]()
