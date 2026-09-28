#!/usr/bin/env python3
"""LANE C: ingest the reverse-tunnel dataset into its own `reverse-tunnels` Elastic index.

Conforms to the canonical shared schema (notes/gems-es-mapping.json):
tunnel concepts map onto existing fields; tunnel-specific detail lives in
`labels` (flattened) + `tags`. Zero new top-level fields.
event.dataset.keyword multi-field included at creation (uniform with the
other campaign indices).

Record kinds:
  tunnel_hostname  - one per exact tunnel hostname (corpus-verified,
                     urlquery-scanned, candidate-same-format)
  tunnel_evidence  - one per collusion-wiki revision row carrying a tunnel URL
  uq_report        - one per urlquery scan report touching a tunnel string

Usage: python3 es_ingest_reverse_tunnels.py
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
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = "/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus"
PDIR = BASE + "/data/reverse-tunnels"
INDEX = "reverse-tunnels"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "reverse-tunnels-ingest", "vendor": "nightingale-collective",
            "type": "dataset"}


def req(method, path, body=None, raw=None):
    url = ES + path
    data = raw.encode() if raw is not None else (
        json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    if ES.startswith(("http://localhost", "http://127.0.0.1", "http://[::1]")):
        pass  # local instance: no vault auth
    else:
        add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=180) as resp:
        return read_json_response(resp)


def flat(d):
    out = {}
    for k, v in d.items():
        if v is None:
            continue
        elif isinstance(v, (list, tuple)):
            out[k] = ", ".join(str(x) for x in v[:20])
        else:
            out[k] = str(v)
    return out


def base_doc(kind, ts=None):
    doc = {
        "record_kind": kind,
        "event": {"dataset": INDEX, "created": NOW},
        "observer": dict(OBSERVER),
        "tags": ["source:reverse-tunnels-lane-c"],
    }
    if ts:
        doc["@timestamp"] = ts
        doc["published_at"] = ts
    return doc


def build_docs():
    docs = {}

    hosts = json.load(open(PDIR + "/tunnel_hostnames.json"))["hostnames"]
    for h in hosts:
        doc = base_doc("tunnel_hostname", h["first_seen_utc"])
        doc["source_url"] = "https://" + h["hostname"]
        doc["matched_string"] = h["hostname"]
        doc["description"] = (
            "Reverse-tunnel hostname (%s). %s. %s" %
            (h["provider"], h["classification"], h["evidence"]))
        doc["confidence"] = h["classification"]
        doc["tags"] += ["provider:" + h["provider"], "class:" + h["classification"]]
        doc["labels"] = flat({
            "hostname": h["hostname"],
            "provider": h["provider"],
            "classification": h["classification"],
            "first_seen_utc": h["first_seen_utc"],
            "embedded_client_ip": h["embedded_ip"],
            "agent_label": h["label"],
            "wiki_pages": h["pages"],
            "ingested_by": "es_ingest_reverse_tunnels",
        })
        docs["tunnel:" + h["hostname"]] = doc

    evid = json.load(open(PDIR + "/corpus_tunnel_records.json"))
    for e in evid:
        doc = base_doc("tunnel_evidence", e["time"])
        doc["source_url"] = "https://collusion.wiki/explorer"
        doc["description"] = (
            "collusion-wiki revision %s on %s (%s) carries tunnel URL(s): %s" %
            (e["label"], e["page_id"], e["time"], ", ".join(e["tunnels"])))
        doc["matched_string"] = ", ".join(e["tunnels"])
        doc["tags"] += ["source:collusion-wiki-export", "wiki:" + e["page_id"].split("/")[0]]
        doc["labels"] = flat({
            "agent_label": e["label"],
            "page_id": e["page_id"],
            "revision_time": e["time"],
            "tunnels": e["tunnels"],
            "ingested_by": "es_ingest_reverse_tunnels",
        })
        docs["tunnel-evidence:%s:%s:%s" % (e["time"], e["label"], e["page_id"])] = doc

    uq = json.load(open(PDIR + "/uq_report_summary.json"))
    for query, block in uq.items():
        for r in block["reports"]:
            rid = r["report_id"]
            doc = base_doc("uq_report", r["date"])
            doc["source_url"] = "https://urlquery.net/report/" + rid
            doc["description"] = (
                "urlquery scan report matching '%s': submitted %s (scan %s)" %
                (query, r["submitted_url"], r["date"]))
            doc["matched_string"] = r["submitted_url"]
            doc["tags"] += ["source:urlquery", "query:" + query]
            doc["labels"] = flat({
                "report_id": rid,
                "scan_date": r["date"],
                "submitted_url": r["submitted_url"],
                "urlquery_query": query,
                "ingested_by": "es_ingest_reverse_tunnels",
            })
            docs["uq-report:%s:%s" % (query, rid)] = doc

    return docs


def ensure_index():
    try:
        req("GET", "/%s" % INDEX)
        print("index exists:", INDEX)
        return
    except Exception:
        pass
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
    # uniform event.dataset.keyword multi-field (matches other campaign indices)
    mapping["properties"]["event"]["properties"]["dataset"]["fields"] = {
        "keyword": {"type": "keyword", "ignore_above": 256}}
    req("PUT", "/%s" % INDEX, {"mappings": mapping})
    print("created index with shared mapping:", INDEX)


def bulk_load(docs):
    items = list(docs.items())
    ok = fail = 0
    for i in range(0, len(items), 400):
        chunk = items[i:i + 400]
        nd = "".join(
            json.dumps({"index": {"_index": INDEX, "_id": _id}}) + "\n" +
            json.dumps(doc) + "\n" for _id, doc in chunk)
        res = req("POST", "/_bulk", raw=nd)
        for it in res.get("items", []):
            st = it.get("index", {}).get("status", 0)
            if st in (200, 201):
                ok += 1
            else:
                fail += 1
                print("BULK FAIL:", json.dumps(it)[:250])
    return ok, fail


def verify():
    req("POST", "/%s/_refresh" % INDEX)
    r = req("POST", "/%s/_count" % INDEX,
            {"query": {"term": {"event.dataset": INDEX}}})
    return r.get("count", 0)


if __name__ == "__main__":
    ensure_index()
    docs = build_docs()
    print("docs built:", len(docs))
    ok, fail = bulk_load(docs)
    print("bulk ok:", ok, "fail:", fail)
    print("verified count in index:", verify())
