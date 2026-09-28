#!/usr/bin/env python3
"""Ingest the jsonhero.io shared-docs dataset into its own `jsonhero-docs` index.

Conforms to the shared schema (notes/gems-es-mapping.json) — one ES doc per
jsonhero document (17: 11 live + 6 dead), dataset detail in `labels` (flattened)
+ `tags`. No new top-level fields.

Usage:
  python3 es_ingest_jsonhero.py --create   # create index with canonical mapping
  python3 es_ingest_jsonhero.py --load     # bulk-load the 17 docs
  python3 es_ingest_jsonhero.py --verify   # count + status breakdown
"""
import sys, json, os, urllib.request
from datetime import datetime, timezone
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = "/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus"
D = BASE + "/data/jsonhero-docs"
INDEX = "jsonhero-docs"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "jsonhero-docs-ingest", "vendor": "swarmtraces-hunt",
            "type": "dataset"}


def req(method, path, body=None, raw=None):
    url = ES + path
    data = raw.encode() if raw is not None else (
        json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=180) as resp:
        return read_json_response(resp)


def classify(did, body):
    """Content family + summary for one fetched doc."""
    if body is None:
        return (["status:dead"], "Document no longer served (HTTP 500). "
                "Referenced in June-2026 wiki revisions; died since.")
    try:
        d = json.loads(body)
    except Exception:
        return (["status:live", "content:unknown"], "Unparseable payload.")
    tags = ["status:live"]
    if isinstance(d, dict) and "regCF_county_methodology" in d:
        tags.append("content:regcf")
        yrs = [k for k in d if k.startswith("regCF_county_20")]
        desc = ("SEC Regulation Crowdfunding county dataset: methodology + "
                f"filters + yearly arrays {sorted(yrs)}. "
                f"{len(d.get('regCF_county_2021', []))} county records in 2021 array. "
                "Deep-linked ?path= params (e.g. regCF_county_2021.91) resolve "
                "to county records {code, offerings, usd, color_code}. "
                "10-digit numbers are SEC CIK identifiers, not epoch nonces.")
    elif isinstance(d, dict) and d.get("type") == "FeatureCollection":
        tags.append("content:geojson")
        desc = (f"County boundary GeoJSON ({len(d.get('features', []))} features, "
                "hc-transform present — Highcharts map payload), census.gov attribution.")
    elif isinstance(d, dict) and d.get("source", "").startswith("https://www.sec.gov"):
        tags.append("content:extract")
        desc = ("Agent-authored working extract: Massachusetts county entries copied "
                f"from SEC county map JSON ({d.get('note', '')}). us-ma-* codes with raw USD amounts.")
    else:
        tags.append("content:test")
        desc = ("Small test-shaped payload (country/ageGroup/internetPoorFemales rows) — "
                "not referenced from any wiki revision; likely a probe doc.")
    return tags, desc


def build_docs():
    manifest = json.load(open(f"{D}/manifest.json"))
    # wiki ref counts per doc
    refs = {}
    with open(BASE + "/data/jsonhero_doc_links.jsonl") as f:
        for line in f:
            r = json.loads(line)
            refs.setdefault(r["doc_id"], []).append(r)
    docs = {}
    for m in manifest:
        did = m["doc_id"]
        body = None
        fpath = f"{D}/{did}.json"
        if os.path.exists(fpath):
            body = open(fpath, "rb").read()
        tags, desc = classify(did, body)
        rl = refs.get(did, [])
        wikis = sorted(set(x["wiki"] for x in rl if x.get("wiki")))
        agents = sorted(set(x["agent_label"] for x in rl if x.get("agent_label")))
        top_keys = []
        if body:
            try:
                d = json.loads(body)
                top_keys = list(d.keys())[:12] if isinstance(d, dict) else ["<array>"]
            except Exception:
                pass
        labels = {
            "doc_id": did,
            "http_status": str(m["http_status"]),
            "sha256": m.get("sha256", ""),
            "byte_size": str(m.get("byte_size", 0)),
            "corpus_url_occurrences": str(m["corpus_url_occurrences"]),
            "n_wiki_refs": str(len(rl)),
            "wikis": ",".join(wikis),
            "agent_labels": ",".join(a for a in agents if a),
            "top_keys": ",".join(top_keys),
        }
        doc = {
            "@timestamp": "2026-09-28T02:55:00Z",
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "jsonhero_doc",
            "description": desc,
            "source_url": f"https://jsonhero.io/j/{did}",
            "observer": OBSERVER,
            "tags": tags,
            "labels": labels,
        }
        docs[f"jsonhero:{did}"] = doc
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
                "status": {"terms": {"field": "tags"}},
                "kinds": {"terms": {"field": "record_kind"}}}})
    print("total:", r["hits"]["total"]["value"])
    for b in r["aggregations"]["status"]["buckets"]:
        print(f"  {b['key']}: {b['doc_count']}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--verify"
    {"--create": create_index, "--load": load, "--verify": verify}[mode]()
