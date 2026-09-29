#!/usr/bin/env python3
"""Ingest the jsonhero archive-recovery dataset into its own `jsonhero-docs-archive` index.

Conforms to the shared schema (notes/gems-es-mapping.json) — one ES doc per
dead doc ID (6: 1 recovered + 5 not archived), dataset detail in `labels`
(flattened) + `tags`. No new top-level fields.

Usage:
  python3 es_ingest_jsonhero_archive.py --create   # create index with canonical mapping
  python3 es_ingest_jsonhero_archive.py --load     # bulk-load the 6 docs
  python3 es_ingest_jsonhero_archive.py --verify   # count + recovery breakdown
"""
import sys, json, os, glob, urllib.request
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


def _resolve_data_dir(slug):
    """Resolve data/*-<slug>/ dynamically so date-prefix renames don't break this."""
    matches = sorted(glob.glob(os.path.join(BASE, "data", "*-" + slug)))
    if not matches:
        raise SystemExit(f'no data dir matches "*-{slug}"')
    return matches[0]


D = _resolve_data_dir("jsonhero-docs-archive")
RAW = os.path.join(D, "raw")
INDEX = "2025-01-13-jsonhero-docs-archive"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "jsonhero-archive-ingest", "vendor": "swarmtraces-hunt",
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
    manifest = json.load(open(os.path.join(RAW, "manifest.json")))
    refs = {}
    with open(BASE + "/data/aggregates/2026-09-29-overlap-analysis/raw/jsonhero_doc_links.jsonl") as f:
        for line in f:
            r = json.loads(line)
            refs.setdefault(r["doc_id"], []).append(r)
    docs = {}
    for m in manifest:
        did = m["doc_id"]
        recovered = m["recovery_status"] == "recovered"
        rl = refs.get(did, [])
        wikis = sorted(set(x["wiki"] for x in rl if x.get("wiki")))
        agents = sorted(set(x["agent_label"] for x in rl if x.get("agent_label")))
        top_keys = []
        if recovered:
            try:
                d = json.loads(open(os.path.join(RAW, f"{did}.json"), encoding="utf-8").read())
                top_keys = list(d.keys())[:12] if isinstance(d, dict) else ["<array>"]
            except Exception:
                pass
        tags = ["recovery:recovered" if recovered else "recovery:not_archived"]
        if recovered:
            tags.append("content:regcf")
            desc = ("Recovered from a 2026-09-12 Wayback capture of the /j/<id> page "
                    f"({m['capture_url']}). SEC Regulation Crowdfunding county dataset, "
                    "OLDER VINTAGE than the live-doc family: created from a 2025-01-13 "
                    "Wayback capture of sec.gov/files/county.json, no regCF_county_2024 "
                    "array. 2021 county records content-identical to the live family "
                    "(e.g. us-md-005 -> offerings 10, usd 3067574.523389335). Payload was "
                    "embedded in window.__remixContext as a JS object literal; "
                    "extracted and converted to strict JSON.")
        else:
            desc = ("Dead on the live site (HTTP 500) and zero Wayback captures "
                    f"({m['note']}). Content unknown; referenced in June-2026 wiki "
                    "revisions so it was live during the campaign.")
        labels = {
            "doc_id": did,
            "recovery_status": m["recovery_status"],
            "archive_source": m.get("archive_source", ""),
            "capture_timestamp": m.get("capture_timestamp", ""),
            "capture_url": m.get("capture_url", ""),
            "sha256": m.get("sha256", ""),
            "byte_size": str(m.get("byte_size", 0)),
            "corpus_url_occurrences": str(m["corpus_url_occurrences"]),
            "n_wiki_refs": str(len(rl)),
            "wikis": ",".join(wikis),
            "agent_labels": ",".join(a for a in agents if a),
            "top_keys": ",".join(top_keys),
        }
        doc = {
            "@timestamp": "2026-09-28T03:05:00Z",
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "jsonhero_doc_archive",
            "description": desc,
            "source_url": f"https://jsonhero.io/j/{did}",
            "observer": OBSERVER,
            "tags": tags,
            "labels": labels,
        }
        docs[f"jsonhero-archive:{did}"] = doc
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
                "recovery": {"terms": {"field": "tags"}},
                "kinds": {"terms": {"field": "record_kind"}}}})
    print("total:", r["hits"]["total"]["value"])
    for b in r["aggregations"]["recovery"]["buckets"]:
        print(f"  {b['key']}: {b['doc_count']}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--verify"
    {"--create": create_index, "--load": load, "--verify": verify}[mode]()
