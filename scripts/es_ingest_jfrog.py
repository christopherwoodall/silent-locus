#!/usr/bin/env python3
"""Ingest JFrog's public GemStuffer inventory CSV into `rubygems-goimport-campaign`.

record_kind := "jfrog_inventory" (sixth flavor in the shared schema).
Source: data/gemstuffer-jfrog-2026-09-27.csv (Package, Versions, Xray ID),
saved from https://research.jfrog.com/gemstuffer.csv on 2026-09-27.
Provenance: https://research.jfrog.com/post/gemstuffer-openai-rubygems/

The CSV carries no per-row dates, so wave/@timestamp are inherited from our
dated Diffend corpus where the package overlaps; jfrog-only rows get the
harvest-date fallback (never "now"), per the schema review P0 rule.

Idempotent: deterministic _id "jfrog:<package>", re-runs overwrite.

Usage:
  python3 es_ingest_jfrog.py            # update mapping + bulk load
  python3 es_ingest_jfrog.py --verify  # count + sample docs only
"""
import sys, json, csv, urllib.request
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
INDEX = "rubygems-goimport-campaign"
NOW = datetime.now(timezone.utc).isoformat()
FALLBACK_TS = "2026-09-27T00:00:00.000Z"  # CSV acquisition date; never "now"
REPORT_URL = "https://research.jfrog.com/post/gemstuffer-openai-rubygems/"
CSV_URL = "https://research.jfrog.com/gemstuffer.csv"
OBSERVER = {"product": "jfrog-inventory-ingest", "vendor": "independent-research",
            "type": "script"}


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
    with urllib.request.urlopen(r, timeout=120) as resp:
        return read_json_response(resp)


def parse_diff_ts(ts):
    try:
        return datetime.strptime(ts.strip(), "%b %d, %Y %H:%M").replace(
            tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
    except Exception:
        return None


def wave_for(published_at):
    if not published_at:
        return None
    d = published_at[:10]
    if d == "2026-06-18":
        return "june-18"
    if d in ("2026-05-26", "2026-05-27"):
        return "may-26"
    if d.startswith("2026-05-"):
        return "may-12"
    return None


def corpus_wave_lookup():
    """gem name -> (published_at ISO, wave) from our dated Diffend corpus."""
    lookup = {}
    with open(BASE + "/data/gem-ioc-log.jsonl") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("record_kind") != "diffend_harvest":
                continue
            gem = r.get("gem")
            if not gem or gem in lookup:
                continue
            for v in r.get("diffend_versions", []) or []:
                iso = parse_diff_ts(v.get("diff_ts") or "")
                if iso:
                    lookup[gem] = (iso, wave_for(iso))
                    break
    return lookup


def parse_versions(raw):
    parts = [p.strip() for p in (raw or "").replace(";", ",").split(",")]
    return [p for p in parts if p]


def load_docs():
    lookup = corpus_wave_lookup()
    print("corpus wave lookup: %d gems" % len(lookup))
    docs = {}
    overlap = 0
    with open(BASE + "/data/gemstuffer-jfrog-2026-09-27.csv", newline="") as f:
        for row in csv.DictReader(f):
            gem = (row.get("Package") or "").strip()
            if not gem:
                continue
            versions = parse_versions(row.get("Versions"))
            xray = (row.get("Xray ID") or "").strip()
            in_corpus = gem in lookup
            if in_corpus:
                overlap += 1
                published_at, wave = lookup[gem]
                ts_source = "diffend:diff_ts"
            else:
                published_at, wave = FALLBACK_TS, None
                ts_source = "fallback:jfrog_csv_no_per_row_date"
            doc = {
                "record_kind": "jfrog_inventory",
                "gem": gem,
                "package": gem,
                "versions": versions,
                "version_count": len(versions),
                "xray_id": xray or None,
                "source_url": REPORT_URL,
                "csv_source_url": CSV_URL,
                "in_diffend_corpus": in_corpus,
                "@timestamp": published_at,
                "event": {"dataset": "rubygems-goimport-campaign",
                          "created": NOW},
                "observer": dict(OBSERVER),
                "status": "dead",
                "tags": ["status:dead", "source:jfrog",
                         "corpus:overlap" if in_corpus else "corpus:jfrog_only"]
                        + (["wave:%s" % wave] if wave else []),
                "labels": {"gem.status": "dead",
                           "gem.timestamp_source": ts_source,
                           "jfrog.in_diffend_corpus": "true" if in_corpus
                           else "false"},
            }
            if wave:
                doc["wave"] = wave
            docs["jfrog:%s" % gem] = doc
    print("jfrog rows: %d, overlap with our corpus: %d" % (len(docs), overlap))
    return docs


def update_mapping():
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
    try:
        req("PUT", "/%s/_mapping" % INDEX, mapping)
        print("mapping updated on live index")
    except Exception as e:
        body = e.read().decode() if hasattr(e, "read") else str(e)
        print("mapping PUT failed:", body[:300])
        raise


def bulk_load(docs):
    items = list(docs.items())
    total_ok, total_fail = 0, 0
    for i in range(0, len(items), 400):
        chunk = items[i:i + 400]
        nd = "".join(
            json.dumps({"index": {"_index": INDEX, "_id": _id}}) + "\n" +
            json.dumps(doc) + "\n" for _id, doc in chunk)
        res = req("POST", "/_bulk", raw=nd)
        for it in res.get("items", []):
            st = it.get("index", {}).get("status", 0)
            if st in (200, 201):
                total_ok += 1
            else:
                total_fail += 1
                print("BULK FAIL:", json.dumps(it)[:200])
        print("bulk progress: %d/%d ok=%d fail=%d" %
              (i + len(chunk), len(items), total_ok, total_fail))
    return total_ok, total_fail


def verify():
    c = req("GET", "/%s/_count" % INDEX)
    print("doc count:", c.get("count"))
    r = req("POST", "/%s/_search" % INDEX,
            {"size": 0, "query": {"term": {"record_kind": "jfrog_inventory"}}})
    print("  jfrog_inventory:", r["hits"]["total"]["value"])
    r = req("POST", "/%s/_search" % INDEX,
            {"size": 0, "query": {"term": {"in_diffend_corpus": True}}})
    print("  overlap (in_diffend_corpus=true):", r["hits"]["total"]["value"])
    s = req("POST", "/%s/_search" % INDEX,
            {"size": 3, "_source": ["record_kind", "gem", "versions",
                                    "xray_id", "wave", "in_diffend_corpus",
                                    "@timestamp"],
             "query": {"term": {"record_kind": "jfrog_inventory"}}})
    for h in s["hits"]["hits"]:
        print(json.dumps(h["_source"]))


def main():
    if "--verify" in sys.argv:
        verify()
        return
    update_mapping()
    docs = load_docs()
    ok, fail = bulk_load(docs)
    print("ingest done: ok=%d fail=%d" % (ok, fail))
    verify()


if __name__ == "__main__":
    main()
