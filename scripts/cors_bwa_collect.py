#!/usr/bin/env python3
"""Lane cors-bwa-proxy: pull every doc matching *cors.bwa.workers.dev* across
the corpus indices (read-only), plus a *.workers.dev sweep to find other
CORS-proxy hostnames. Saves raw docs per index to data/aggregates/2025-09-26-cors-bwa-proxy/raw/.
"""
import sys, json, urllib.request, os
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
try:
    sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
    from dynamic_credentials import add_surrogate_to_request, read_json_response
except ImportError:  # local run: no vault on this machine, plain HTTP(S) instead
    def add_surrogate_to_request(request, *args, **kwargs):
        return None
    def read_json_response(response):
        import json as _json
        return _json.load(response)

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
D = "data/aggregates/2025-09-26-cors-bwa-proxy"
os.makedirs(f"{D}/raw", exist_ok=True)

INDICES = ["2026-05-17-collusion-wiki", "urlquery-incidents", "urlquery-hunt",
           "2026-05-26-proxy-primitives", "2026-03-12-paste-archive-gap", "2026-09-27-rmn-re-linktable"]


def req(method, path, body=None):
    r = urllib.request.Request(ES + path,
                               data=json.dumps(body).encode() if body is not None else None,
                               method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, "custom.elastic-cloud", allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=180) as resp:
        return read_json_response(resp)


def pull_all(index, query_string, out):
    docs = []
    r = req("POST", f"/{index}/_search",
            {"size": 2000, "track_total_hits": True,
             "query": {"query_string": {"query": query_string,
                                       "lenient": True}}})
    docs = r["hits"]["hits"]
    total = r["hits"]["total"]["value"] if isinstance(r["hits"].get("total"), dict) else r["hits"]["total"]
    print(f"   ({index} total={total} fetched={len(docs)})")
    with open(out, "w") as f:
        for h in docs:
            f.write(json.dumps({"_id": h["_id"], "_index": index,
                                "_source": h["_source"]}) + "\n")
    return len(docs)


def main():
    totals = {}
    for idx in INDICES:
        n = pull_all(idx, "*cors.bwa.workers.dev*",
                     f"{D}/raw/{idx}.jsonl")
        totals[idx] = n
        print(idx, n, flush=True)
    # workers.dev family sweep: restrict to url-ish fields to keep it tight
    n = pull_all("urlquery-incidents", "*.workers.dev*",
                 f"{D}/raw/urlquery-incidents-allworkersdev.jsonl")
    totals["urlquery-incidents-allworkersdev"] = n
    print("urlquery-incidents allworkersdev", n, flush=True)
    n = pull_all("2026-05-17-collusion-wiki", "*.workers.dev*",
                 f"{D}/raw/collusion-wiki-allworkersdev.jsonl")
    totals["collusion-wiki-allworkersdev"] = n
    print("collusion-wiki allworkersdev", n, flush=True)
    json.dump(totals, open(f"{D}/raw/pull_totals.json", "w"), indent=1)


if __name__ == "__main__":
    main()
