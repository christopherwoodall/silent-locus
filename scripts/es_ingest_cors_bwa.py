#!/usr/bin/env python3
"""Ingest the cors-bwa-proxy lane dataset into its own `cors-bwa-proxy` index.

Conforms to the shared schema (notes/gems-es-mapping.json): @timestamp,
event{created,dataset} (event.dataset has the .keyword multi-field at
creation), record_kind, description, source_url, matched_string, observer,
tags, and dataset-specific fields in flattened `labels` only.
Zero new top-level fields.

Record flavors:
  proxied_target  - one per urlquery-incidents URL behind cors.bwa.workers.dev
  proxy_ladder    - one per reconstructed (wrapper -> bwa -> target) edge
  proxy_family    - one per other *.workers.dev CORS-proxy hostname found
  venue_summary   - one per corpus venue with bwa hit counts

Usage:
  python3 es_ingest_cors_bwa.py --create
  python3 es_ingest_cors_bwa.py --load
  python3 es_ingest_cors_bwa.py --verify
"""
import sys, json, hashlib
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
BASE = "data/cors-bwa-proxy"
INDEX = "cors-bwa-proxy"
NOW = datetime.now(timezone.utc).isoformat()
TS = "2026-09-28T05:30:00Z"
OBSERVER = {"product": "cors-bwa-proxy-ingest", "vendor": "swarmtraces-hunt",
            "type": "dataset"}


def req(method, path, body=None):
    r = urllib.request.Request(ES + path,
                               data=json.dumps(body).encode() if body is not None else None,
                               method=method)
    r.add_header("Content-Type", "application/json")
    if ES.startswith(("http://localhost", "http://127.0.0.1", "http://[::1]")):
        pass  # local instance: no vault auth
    else:
        add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=180) as resp:
        return read_json_response(resp)


def build_docs():
    docs = {}
    targets = [json.loads(l) for l in open(f"{BASE}/bwa_targets.jsonl")]
    for t in targets:
        uid = hashlib.sha256((t["source_index"] + t["doc_id"]).encode()).hexdigest()[:12]
        docs[f"cors-bwa-proxy:target:{uid}"] = {
            "@timestamp": t["incident_ts"] or TS,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "proxied_target",
            "description": (f"Live urlquery scan submitted the CORS-proxy-wrapped URL "
                            f"{t['full_proxied_url'][:180]} — decoded target "
                            f"{str(t['decoded_target'])[:180]} "
                            f"(host {t['target_host']}, family {t['task_family']}, "
                            f"chain {t['chain']})."),
            "source_url": "https://urlquery.net/report/" + t["doc_id"],
            "matched_string": t["full_proxied_url"],
            "observer": OBSERVER,
            "tags": [f"proxy:cors.bwa.workers.dev",
                     f"target-host:{t['target_host']}",
                     f"task-family:{t['task_family']}",
                     "venue:urlquery-incidents"],
            "labels": {"source_index": t["source_index"], "doc_id": t["doc_id"],
                       "decoded_target": str(t["decoded_target"])[:500],
                       "target_host": t["target_host"],
                       "task_family": t["task_family"],
                       "chain": t["chain"], "chain_layers": " > ".join(t["chain_layers"]),
                       "incident_ts": t["incident_ts"]},
        }
    for i, l in enumerate(open(f"{BASE}/ladder_edges.jsonl")):
        e = json.loads(l)
        uid = hashlib.sha256(e["edge"].encode()).hexdigest()[:12]
        docs[f"cors-bwa-proxy:ladder:{uid}"] = {
            "@timestamp": TS,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "proxy_ladder",
            "description": (f"Proxy-ladder chain: {e['edge']} "
                            f"({e['occurrences']} occurrences; venues "
                            f"{', '.join(e['venues'])})."),
            "observer": OBSERVER,
            "tags": ["proxy-ladder", "proxy:cors.bwa.workers.dev",
                     f"target-host:{e['layers'][2]}"],
            "labels": {"edge": e["edge"], "outer_wrapper": e["layers"][0],
                       "proxy": e["layers"][1], "target_host": e["layers"][2],
                       "occurrences": str(e["occurrences"]),
                       "venues": ",".join(e["venues"])},
        }
    fam = json.load(open(f"{BASE}/other_workers_dev_hostnames.json"))
    for h, st in fam.items():
        uid = hashlib.sha256(h.encode()).hexdigest()[:12]
        docs[f"cors-bwa-proxy:family:{uid}"] = {
            "@timestamp": TS,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "proxy_family",
            "description": (f"Other workers.dev CORS-proxy hostname in corpora: {h} "
                            f"({st['n_docs']} docs, {st['n_occurrences']} occurrences; "
                            f"top targets {', '.join(list(st['targets'])[:5])})."),
            "observer": OBSERVER,
            "tags": ["proxy-family", f"proxy:{h}"],
            "labels": {"proxy_host": h, "n_docs": str(st["n_docs"]),
                       "n_occurrences": str(st["n_occurrences"]),
                       "docs_per_index": json.dumps(st["docs_per_index"]),
                       "top_targets": json.dumps(dict(list(st["targets"].items())[:10]))},
        }
    venue_hits = {"collusion-wiki": 578, "urlquery-incidents": 113,
                  "urlquery-hunt": 36, "proxy-primitives": 17,
                  "paste-archive-gap": 1, "rmn-re-linktable": 1}
    venue_ctx = {"collusion-wiki": "link_in_selected_agent_related_text / wiki_link+wiki_record+wiki_revision docs referencing bwa as an agent tool",
                 "urlquery-incidents": "live submitted scan URLs behind the bwa proxy",
                 "urlquery-hunt": "graph edges labeled 'cors.bwa.workers.dev laundering'",
                 "proxy-primitives": "matched_string hits (lane caught but never elevated it)",
                 "paste-archive-gap": "lane-M ladder doc (termina.digital DB actor pages)",
                 "rmn-re-linktable": "gem-era shortener decoded target"}
    for v, n in venue_hits.items():
        docs[f"cors-bwa-proxy:venue:{v}"] = {
            "@timestamp": TS,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "venue_summary",
            "description": (f"cors.bwa.workers.dev footprint in {v}: {n} docs. "
                            f"{venue_ctx[v]}."),
            "observer": OBSERVER,
            "tags": ["proxy:cors.bwa.workers.dev", f"venue:{v}"],
            "labels": {"venue": v, "hit_count": str(n), "context": venue_ctx[v]},
        }
    return docs


def create_index():
    mapping = json.load(open("notes/gems-es-mapping.json"))["mappings"]
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
    payload = "\n".join(lines) + "\n"
    rq = urllib.request.Request(ES + "/_bulk", data=payload.encode(), method="POST")
    rq.add_header("Content-Type", "application/x-ndjson")
    if ES.startswith(("http://localhost", "http://127.0.0.1", "http://[::1]")):
        pass  # local instance: no vault auth
    else:
        add_surrogate_to_request(rq, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(rq, timeout=300) as resp:
        res = read_json_response(resp)
    print("bulk:", res.get("errors"), "items:", len(res.get("items", [])))
    errs = [i for i in res.get("items", []) if i.get("index", {}).get("status") not in (200, 201)]
    for e in errs[:5]:
        print("ERR:", json.dumps(e)[:300])


def verify():
    r = req("GET", f"/{INDEX}/_count")
    print("count:", r.get("count"))
    r = req("GET", f"/{INDEX}/_mapping")
    tops = set(r[INDEX]["mappings"]["properties"].keys())
    canon = set(json.load(open("notes/gems-es-mapping.json"))["mappings"]["properties"].keys())
    print("extra top-level fields:", tops - canon)
    print("event.dataset.keyword multi-field:",
          "keyword" in r[INDEX]["mappings"]["properties"]["event"]["properties"]["dataset"].get("fields", {}))
    r = req("POST", f"/{INDEX}/_search",
            {"size": 0, "aggs": {"kinds": {"terms": {"field": "record_kind"}}}})
    print("kinds:", [(b["key"], b["doc_count"]) for b in r["aggregations"]["kinds"]["buckets"]])


if __name__ == "__main__":
    if "--create" in sys.argv:
        create_index()
    elif "--load" in sys.argv:
        load()
    elif "--verify" in sys.argv:
        verify()
    else:
        print("usage: --create|--load|--verify")
