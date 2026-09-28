#!/usr/bin/env python3
"""Ingest the paste-archive dataset into its own `paste-archive` index.

Conforms to the shared schema (notes/gems-es-mapping.json) — one ES doc per
paste URL (76: 20 k4be.pl + 55 anna.fyi + 1 infinitypaste.club), detail in
`labels` (flattened) + `tags`. No new top-level fields.

Usage:
  python3 es_ingest_paste_archive.py --create   # create index with canonical mapping
  python3 es_ingest_paste_archive.py --load     # bulk-load the 76 docs
  python3 es_ingest_paste_archive.py --verify   # count + breakdown
"""
import sys, json, os, hashlib
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
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = REPO_ROOT
D = BASE + "/data/paste-archive"
INDEX = "paste-archive"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "paste-archive-ingest", "vendor": "swarmtraces-hunt",
            "type": "dataset"}


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


def build_docs():
    docs = {}
    # k4be.pl metadata
    for line in open(f"{D}/k4be.pl/metadata.jsonl"):
        m = json.loads(line)
        pid = m["id"]
        body = None
        fpath = f"{D}/k4be.pl/{pid}.txt"
        if os.path.exists(fpath):
            body = open(fpath).read()
        tags = ["host:pastebin.k4be.pl", f"body:{m['body_status']}"]
        if m["body_status"] == "body":
            tags.append("content:epl-relegation-tables")
        elif "ROIETA" in m["title"]:
            tags.append("content:roieta-th45-studies")
        desc = (f"k4be.pl paste '{m['title']}'"
                + (f" by {m['author']}" if m["author"] else "")
                + f". Body status: {m['body_status']}. "
                + ("Full body recovered (presentation-layer text). "
                   if body else "Metadata only — body behind raw/download endpoints; needs live-browser render. "))
        labels = {"paste_id": pid, "host": "pastebin.k4be.pl",
                  "title": m["title"], "author": m["author"] or "",
                  "body_status": m["body_status"], "live_2026_09_28": "true",
                  "byte_size": str(len(body.encode()) if body else 0)}
        doc = {
            "@timestamp": "2026-09-28T03:10:00Z",
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "paste_text", "description": desc,
            "source_url": m["url"], "observer": OBSERVER,
            "tags": tags, "labels": labels,
        }
        if body:
            doc["description"] = body
            doc["file"] = pid + ".txt"
            doc["sha256"] = hashlib.sha256(body.encode()).hexdigest()
            doc["size_bytes"] = len(body.encode())
        docs[f"paste-archive:k4be:{pid}"] = doc
    # anna.fyi titles
    for line in open(f"{D}/anna.fyi/titles.jsonl"):
        m = json.loads(line)
        pid = m["id"]
        live = m["live_2026_09_28"]
        tags = ["host:anna.fyi", f"body:{m['body_status'].split(' ')[0]}"]
        if (m["title"] or "").startswith("Statistical reference"):
            tags.append("content:statistical-reference-series")
        elif (m["title"] or "").startswith("ReplyLink"):
            tags.append("content:reply-link")
        elif "NSI" in (m["title"] or ""):
            tags.append("content:nsi-table-reference")
        desc = (f"anna.fyi paste '{m['title']}'. "
                f"Body status: {m['body_status']}.")
        docs[f"paste-archive:anna:{pid}"] = {
            "@timestamp": "2026-09-28T03:10:00Z",
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "paste", "description": desc,
            "source_url": m["url"], "observer": OBSERVER,
            "tags": tags,
            "labels": {"paste_id": pid, "host": "anna.fyi",
                       "title": m["title"] or "",
                       "body_status": m["body_status"],
                       "live_2026_09_28": str(live)},
        }
    # infinitypaste.club
    for line in open(f"{D}/infinitypaste.club/metadata.jsonl"):
        m = json.loads(line)
        body = open(f"{D}/infinitypaste.club/{m['id']}.txt").read()
        docs[f"paste-archive:inf:{m['id']}"] = {
            "@timestamp": "2026-09-28T03:10:00Z",
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "paste_text",
            "description": body,
            "source_url": m["url"], "observer": OBSERVER,
            "tags": ["host:infinitypaste.club", "body:body", "content:nsi-reference-link"],
            "file": m["id"] + ".txt",
            "sha256": hashlib.sha256(body.encode()).hexdigest(),
            "size_bytes": len(body.encode()),
            "labels": {"paste_id": m["id"], "host": "infinitypaste.club",
                       "title": m["title"], "body_status": "body",
                       "live_2026_09_28": "true",
                       "byte_size": str(len(body.encode()))},
        }
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
    payload = "\n".join(lines) + "\n"
    r = urllib.request.Request(
        ES + "/_bulk", data=payload.encode(), method="POST",
        headers={"Content-Type": "application/x-ndjson"})
    if ES.startswith(("http://localhost", "http://127.0.0.1", "http://[::1]")):
        _es_user = os.environ.get("ES_USER")
        if _es_user:
            import base64 as _b64
            r.add_header("Authorization", "Basic " + _b64.b64encode(
                f"{_es_user}:{os.environ.get('ES_PASS', '')}".encode()).decode())
    else:
        add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=300) as resp:
        out = read_json_response(resp)
    print("errors:", out.get("errors"), "items:", len(out.get("items", [])))


def verify():
    r = req("GET", f"/{INDEX}/_count")
    print("count:", r["count"])
    for field in ["tags", "labels.host", "labels.body_status"]:
        try:
            agg = req("GET", f"/{INDEX}/_search",
                      {"size": 0, "aggs": {"b": {"terms": {"field": field, "size": 30}}}})
            print(field, [(b["key"], b["doc_count"]) for b in agg["aggregations"]["b"]["buckets"]])
        except Exception as e:
            print(field, "agg failed:", str(e)[:100])


if __name__ == "__main__":
    if "--create" in sys.argv:
        create_index()
    elif "--load" in sys.argv:
        load()
    elif "--verify" in sys.argv:
        verify()
    else:
        print("usage: --create | --load | --verify")
