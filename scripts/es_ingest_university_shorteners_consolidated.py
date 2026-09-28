#!/usr/bin/env python3
"""Consolidated ingest for the university-shorteners family into ONE index.

Workstream A (2026-09-28): batches 1 and 2 are the same dataset family
(shortener public-stats pages, canonical shared schema). Both JSONL files
are ingested into index `university-shorteners`; per-batch provenance is
preserved in each doc's `event.dataset` (batch1 -> "university-shorteners",
batch2 -> "university-shorteners-batch2",
batch3 -> "university-shorteners-batch3") and in `labels.shortener.*`.

Sources (untouched on disk):
  data/university-shorteners/university-shorteners.jsonl                (11 docs)
  data/university-shorteners-batch2/university-shorteners-batch2.jsonl   (1 doc)
  data/university-shorteners-batch3/university-shorteners-batch3.jsonl   (3 docs)

Idempotent: deterministic _id "yourls:<instance>:<slug>", re-runs overwrite.
Index `university-shorteners-batch2` is retired after a verified consolidate
(--retire flag; no Kibana saved objects reference it).

Usage:
  python3 es_ingest_university_shorteners_consolidated.py          # create/update + bulk load + verify
  python3 es_ingest_university_shorteners_consolidated.py --verify  # verify only
  python3 es_ingest_university_shorteners_consolidated.py --retire  # verify, then DELETE the old batch2 index
"""
import sys, json, os, urllib.request
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
INDEX = "university-shorteners"
OLD_INDEX = "university-shorteners-batch2"
JSONLS = [
    BASE + "/data/university-shorteners/university-shorteners.jsonl",
    BASE + "/data/university-shorteners-batch2/university-shorteners-batch2.jsonl",
    BASE + "/data/university-shorteners-batch3/university-shorteners-batch3.jsonl",
]
EXPECTED_FIELDS = set(json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]["properties"])


def req(method, path, body=None, raw=None):
    url = ES + path
    data = raw.encode() if raw is not None else (
        json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=120) as resp:
        return read_json_response(resp)


def doc_id(d):
    inst = d["labels"]["shortener.instance"]
    slug = d["matched_string"].rstrip("/").split("/")[-1].split("?")[0]
    return "yourls:%s:%s" % (inst, slug)


def load_docs():
    docs = {}
    for jf in JSONLS:
        with open(jf) as f:
            for line in f:
                line = line.strip()
                if line:
                    d = json.loads(line)
                    docs[doc_id(d)] = d
    return docs


def create_index():
    # canonical shared schema: mapping section ONLY (the `index` key in the
    # notes file is the gems index name, not settings).
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
    try:
        res = req("PUT", "/%s" % INDEX, {"mappings": mapping})
        print("index created:", res.get("acknowledged"))
    except Exception as e:
        body = e.read().decode() if hasattr(e, "read") else str(e)
        if "resource_already_exists_exception" in body:
            print("index exists; updating mapping")
            req("PUT", "/%s/_mapping" % INDEX, mapping)
        else:
            raise


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
                print("BULK FAIL:", json.dumps(it)[:200])
    print("ingest done: ok=%d fail=%d" % (ok, fail))


def verify():
    c = req("GET", "/%s/_count" % INDEX)
    print("doc count:", c.get("count"))
    # 16 = 7 batch-1 stats pages + 4 goto.unm.edu per-URL referrer/detail docs
    # (workstream C3, 2026-09-28) + 1 u.ethz.ch detail doc (workstream B, 2026-09-28)
    # + 1 batch-2 doc + 3 batch-3 go.uvm.edu docs.
    assert c.get("count") == 16, "expected 16 docs, got %s" % c.get("count")
    r = req("POST", "/%s/_search" % INDEX,
            {"size": 0, "aggs": {"datasets": {"terms": {"field": "event.dataset.keyword"}}}})
    b = r["aggregations"]["datasets"]["buckets"]
    print("event.dataset.keyword buckets:", [(x["key"], x["doc_count"]) for x in b])
    got = {x["key"]: x["doc_count"] for x in b}
    assert got == {"university-shorteners": 12, "university-shorteners-batch2": 1,
                    "university-shorteners-batch3": 3}, got
    s = req("POST", "/%s/_search" % INDEX, {"size": 100, "_source": True})
    unexpected = set()
    for h in s["hits"]["hits"]:
        unexpected |= set(h["_source"]) - EXPECTED_FIELDS
    print("unexpected top-level fields:", sorted(unexpected) or "none")
    assert not unexpected, unexpected
    r = req("POST", "/%s/_search" % INDEX,
            {"size": 0, "aggs": {"kinds": {"terms": {"field": "record_kind"}}}})
    print("record_kind:", [(x["key"], x["doc_count"]) for x in r["aggregations"]["kinds"]["buckets"]])
    ids = sorted(h["_id"] for h in s["hits"]["hits"])
    assert ids == sorted(set(ids)), "duplicate doc IDs!"
    print("VERIFY OK: 16 docs, no drift, unique deterministic IDs")


def retire_old():
    verify()
    print("retiring index %s ..." % OLD_INDEX)
    out = req("DELETE", "/%s" % OLD_INDEX)
    print("delete acknowledged:", out.get("acknowledged"))


def main():
    if "--verify" in sys.argv:
        verify()
        return
    if "--retire" in sys.argv:
        retire_old()
        return
    create_index()
    docs = load_docs()
    print("docs to load:", len(docs))
    bulk_load(docs)
    verify()


if __name__ == "__main__":
    main()
