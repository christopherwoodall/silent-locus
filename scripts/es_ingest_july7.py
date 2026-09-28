#!/usr/bin/env python3
"""LANE J — ingest the July-7 Diffend sweep results into their own `july7-wave`
Elastic index.

Conforms to the canonical shared schema (notes/gems-es-mapping.json); the
event.dataset.keyword multi-field is included at index creation (uniform with
the other campaign indices). Keep-all policy: every sweep record lands,
found or not, with in_diffend + diffend_wave as the discriminators.

Usage: python3 es_ingest_july7.py   (runs only when the sweep JSONL is final)
"""
import json
import sys
import urllib.request
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
SWEEP = BASE + "/data/july7-wave/diffend_sweep_results_july7.jsonl"
INDEX = "july7-wave"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "july7-wave-sweep", "vendor": "nightingale-collective",
            "type": "dataset"}
CSV_URL = "https://research.jfrog.com/gemstuffer.csv"
REPORT_URL = "https://research.jfrog.com/post/gemstuffer-openai-rubygems/"


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


def diffend_ts_to_iso(ts):
    if not ts:
        return None
    try:
        dt = datetime.strptime(ts, "%B %d, %Y %H:%M")
        return dt.replace(tzinfo=timezone.utc).isoformat()
    except Exception:
        return None


def build_doc(rec):
    name = rec["name"]
    found = rec.get("in_diffend") is True
    first = rec.get("first_publish")
    iso = diffend_ts_to_iso(first)
    wave = rec.get("diffend_wave")
    mechs = rec.get("mechanism_notes") or []
    grams = rec.get("name_grammars") or []
    jvers = rec.get("jfrog_versions") or []
    doc = {
        "record_kind": "diffend_sweep_july7",
        "gem": name,
        "package": name,
        "versions": [v.get("version") for v in (rec.get("versions") or [])],
        "version_count": len(rec.get("versions") or []),
        "diffend_versions": rec.get("versions") or [],
        "first_publish": first,
        "published_at": iso,
        "@timestamp": iso or NOW,
        "wave": wave,
        "in_diffend": found,
        "http_status": rec.get("http_status"),
        "mechanism_notes": mechs,
        "mechanism_version_checked": rec.get("mechanism_version_checked"),
        "diff_error": rec.get("diff_error"),
        "name_grammars": grams,
        "xray_id": rec.get("xray_id"),
        "jfrog_versions": jvers,
        "jfrog_version_count": len(jvers),
        "csv_source_url": CSV_URL,
        "source_url": "https://my.diffend.io/gems/%s" % name,
        "report_url": REPORT_URL,
        "retrieved_via": "my.diffend.io (read-only sweep)",
        "status": "dead",
        "event": {"dataset": INDEX, "created": NOW},
        "observer": dict(OBSERVER),
        "tags": (["status:dead", "source:diffend", "lane:j"] +
                 (["found:in_diffend"] if found else ["found:absent"]) +
                 (["wave:%s" % wave] if wave else []) +
                 ["mechanism:%s" % m.replace(":", "=") for m in mechs] +
                 ["grammar:%s" % g for g in grams]),
        "labels": {"gem.status": "dead",
                   "gem.timestamp_source": "diffend:page_ts" if iso else "none",
                   "lane_j.in_diffend": "true" if found else "false",
                   "lane_j.diffend_wave": wave or "unknown"},
    }
    return doc


def load_docs():
    docs = {}
    with open(SWEEP) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            docs["july7:%s" % rec["name"]] = build_doc(rec)
    return docs


def ensure_index():
    try:
        req("GET", "/%s" % INDEX)
        print("index exists:", INDEX)
        return
    except Exception:
        pass
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
    mapping["properties"]["event"]["properties"]["dataset"]["fields"] = {
        "keyword": {"type": "keyword", "ignore_above": 256}}
    req("PUT", "/%s" % INDEX, {"mappings": mapping})
    print("created index with shared mapping + event.dataset.keyword:", INDEX)


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
    total = r.get("count", 0)
    r = req("POST", "/%s/_count" % INDEX,
            {"query": {"bool": {"must": [
                {"term": {"event.dataset": INDEX}},
                {"term": {"in_diffend": True}}]}}})
    found = r.get("count", 0)
    r = req("POST", "/%s/_count" % INDEX,
            {"query": {"bool": {"must": [
                {"term": {"event.dataset": INDEX}},
                {"term": {"wave": "2026-july-07"}}]}}})
    july = r.get("count", 0)
    print("july7-wave: total=%d in_diffend=%d wave:july-7=%d" % (total, found, july))
    return total, found, july


def main():
    ensure_index()
    docs = load_docs()
    print("docs built:", len(docs))
    ok, fail = bulk_load(docs)
    print("bulk: ok=%d fail=%d" % (ok, fail))
    verify()


if __name__ == "__main__":
    main()
