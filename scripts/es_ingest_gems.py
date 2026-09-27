#!/usr/bin/env python3
"""Bulk-ingest the gem IOC corpus into the hosted `rubygems-goimport-campaign` ES index.

Sources (all in the project data/ dir):
  - gem-ioc-log.jsonl   : download / extraction / diffend_harvest records
  - gem-ioc-hits.jsonl  : per-file + per-metadata IOC hits (record_kind := "hit")

Idempotent: deterministic _id per doc, so re-runs overwrite rather than duplicate.
Diffend re-harvest duplicates in the log are deduped (last wins) before ingest.

Usage:
  python3 es_ingest_gems.py            # create index (if needed) + bulk load
  python3 es_ingest_gems.py --verify  # count + 3 sample docs only
"""
import sys, json, urllib.request
from datetime import datetime, timezone
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
sys.path.insert(0, "/home/hatch/workspace/skills/elastic-cloud/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = "/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus"
INDEX = "rubygems-goimport-campaign"
NOW = datetime.now(timezone.utc).isoformat()


def req(method, path, body=None, raw=None):
    url = ES + path
    if raw is not None:
        data = raw.encode()
    else:
        data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=120) as resp:
        return read_json_response(resp)


def parse_diff_ts(ts):
    """'May 12, 2026 03:32' -> ISO, or None."""
    try:
        return datetime.strptime(ts.strip(), "%B %d, %Y %H:%M").replace(
            tzinfo=timezone.utc).isoformat()
    except Exception:
        return None


def load_docs():
    docs = {}  # _id -> doc (dedupe: last wins)
    pub_lookup = {}  # (gem, version) -> published_at ISO

    def put(_id, doc):
        docs[_id] = doc

    with open(BASE + "/data/gem-ioc-log.jsonl") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except ValueError:
                continue
            rk = r.get("record_kind", "?")
            gem, ver = r.get("gem"), r.get("version")
            if rk == "diffend_harvest" and gem and ver:
                # published_at from the version's own diff timestamp
                for v in r.get("diffend_versions", []) or []:
                    if v.get("version") == ver and v.get("diff_ts"):
                        iso = parse_diff_ts(v["diff_ts"])
                        if iso:
                            pub_lookup[(gem, ver)] = iso
                            r["published_at"] = iso
                        break
                r.setdefault("retrieved_at", NOW)
                put("log:%s:%s:%s" % (rk, gem, ver), r)
            elif rk in ("download", "extraction"):
                if gem and ver:
                    if r.get("published_at"):
                        pub_lookup[(gem, ver)] = r["published_at"]
                    r.setdefault("retrieved_at", NOW)
                    put("log:%s:%s:%s" % (rk, gem, ver), r)
            # other record kinds: pass through keyed on content hash
            elif gem:
                put("log:%s:%s:%s" % (rk, gem, ver), r)

    with open(BASE + "/data/gem-ioc-hits.jsonl") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                h = json.loads(line)
            except ValueError:
                continue
            gem, ver = h.get("gem"), h.get("version")
            val = str(h.get("matched_string", ""))[:4000]
            doc = {
                "record_kind": "hit",
                "gem": gem, "version": ver,
                "file": h.get("file"),
                "ioc_fingerprint": h.get("fingerprint"),
                "ioc_value": val[:256], "ioc_value_text": val,
                "line_no": h.get("line_no"),
                "confidence": h.get("confidence"),
                "evidence": "%s hit in %s line %s (%s)" % (
                    h.get("fingerprint"), h.get("file"), h.get("line_no"),
                    h.get("note", "")),
                "published_at": pub_lookup.get((gem, ver)),
                "retrieved_at": NOW,
            }
            hid = "hit:%s:%s:%s:%s:%s" % (
                gem, ver, h.get("fingerprint"),
                (h.get("file") or "").replace("/", "_"), h.get("line_no"))
            put(hid, doc)
    return docs


def ensure_index():
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
    try:
        req("PUT", "/" + INDEX, {"mappings": mapping})
        print("index created:", INDEX)
    except Exception as e:
        if "resource_already_exists_exception" in str(e):
            print("index already exists:", INDEX)
        else:
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
    s = req("POST", "/%s/_search" % INDEX,
            {"size": 3, "sort": [{"retrieved_at": "desc"}],
             "_source": ["record_kind", "gem", "version", "ioc_fingerprint",
                         "file", "published_at"]})
    for h in s["hits"]["hits"]:
        print(json.dumps(h["_source"]))


def main():
    if "--verify" in sys.argv:
        verify()
        return
    ensure_index()
    docs = load_docs()
    print("docs to ingest (deduped):", len(docs))
    ok, fail = bulk_load(docs)
    print("ingest done: ok=%d fail=%d" % (ok, fail))
    verify()


if __name__ == "__main__":
    main()
