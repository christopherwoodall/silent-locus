#!/usr/bin/env python3
"""Ingest the fieldnotes gem micro-dataset into its own `fieldnotes-gem` Elastic index.

Micro-dataset: RubyGems `fieldnotes` v0.1.3 (2026-09-20) — the public-board.com
agent message board's official client gem. Read-only registry metadata only;
the gem itself was never downloaded or installed.

Conforms to the canonical shared schema (notes/gems-es-mapping.json):
metadata maps onto existing fields; dataset detail lives in `labels`
(flattened) + `tags`. Zero new top-level fields.
event.dataset.keyword multi-field included at creation (uniform with the
other campaign indices).

Usage:
  python3 es_ingest_fieldnotes_gem.py --create
  python3 es_ingest_fieldnotes_gem.py --load
  python3 es_ingest_fieldnotes_gem.py --verify
"""
import sys, json, os, re, urllib.request
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
D = BASE + "/data/fieldnotes-gem"
INDEX = "fieldnotes-gem"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "fieldnotes-gem-ingest", "vendor": "swarmtraces-hunt",
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


def flat(d):
    out = {}
    for k, v in d.items():
        if v is None:
            continue
        elif isinstance(v, (dict, list)):
            out[k] = json.dumps(v)[:500]
        else:
            out[k] = str(v)
    return out


def sha256_file(p):
    import hashlib
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def base_doc(record_kind, _id):
    return {
        "record_kind": record_kind,
        "event": {"dataset": INDEX, "created": NOW},
        "observer": dict(OBSERVER),
        "tags": ["source:rubygems", "grammar:clean"],
        "labels": {"annotated_by": "es_ingest_fieldnotes_gem"},
        "_id": _id,
    }


def build_docs():
    docs = {}
    gem = json.load(open(D + "/rubygems-gem.json"))
    versions = json.load(open(D + "/rubygems-versions.json"))
    sweep = json.load(open(D + "/grammar-sweep.json"))
    total_hits = sum(len(f["hits"]) for f in sweep["files"].values())

    # 1. gem-level metadata doc
    g = base_doc("gem_metadata", "gem:fieldnotes")
    g.update({
        "gem": "fieldnotes",
        "package": "fieldnotes",
        "version": gem["version"],
        "published_at": gem["version_created_at"],
        "@timestamp": gem["version_created_at"],
        "authors": gem["authors"],
        "meta_authors": gem["authors"],
        "meta_summary": gem["info"][:256],
        "meta_description": gem["info"],
        "meta_homepage": gem["homepage_uri"],
        "meta_licenses": gem["licenses"],
        "description": gem["info"],
        "total_downloads": str(gem["downloads"]),
        "external_links": [gem["homepage_uri"], gem["project_uri"],
                           gem["documentation_uri"]],
        "source_url": gem["project_uri"],
        "retrieved_via": "rubygems.org api v1 (read-only GETs)",
        "retrieved_at": NOW,
        "status": "live",
    })
    g["tags"] += ["status:live", "registry:rubygems.org", "agent-board-client",
                  "yanked:false", "campaign-corpus:false"]
    g["labels"].update(flat({
        "gem_uri": gem["gem_uri"],
        "sha": gem["sha"],
        "spec_sha": gem["spec_sha"],
        "platform": gem["platform"],
        "runtime_dependencies": gem["dependencies"]["runtime"],
        "development_dependencies": gem["dependencies"]["development"],
        "metadata_empty": len(gem["metadata"]) == 0,
        "grammar_hits_total": total_hits,
        "swept_at": sweep["swept_at"],
        "homepage": gem["homepage_uri"],
        "note": "official client gem of public-board.com (agent message board); NOT in go-import campaign corpus; yanked=false (live)",
    }))
    docs[g["_id"]] = {k: v for k, v in g.items() if k != "_id"}

    # 2. one doc per version
    for v in versions:
        d = base_doc("version", "version:fieldnotes:" + v["number"])
        d.update({
            "gem": "fieldnotes",
            "package": "fieldnotes",
            "version": v["number"],
            "published_at": v["created_at"],
            "@timestamp": v["created_at"],
            "authors": v["authors"],
            "meta_authors": v["authors"],
            "meta_summary": v["summary"],
            "meta_description": v["description"],
            "meta_licenses": v["licenses"],
            "sha256": v["sha"],
            "expected_sha256": v["sha"],
            "total_downloads": str(v["downloads_count"]),
            "source_url": "https://rubygems.org/api/v1/versions/fieldnotes.json",
            "retrieved_via": "rubygems.org api v1 (read-only GETs)",
            "retrieved_at": NOW,
            "status": "live",
        })
        d["tags"] += ["status:live", "registry:rubygems.org", "grammar:clean"]
        d["labels"].update(flat({
            "summary": v["summary"],
            "downloads_count": v["downloads_count"],
            "built_at": v["built_at"],
            "platform": v["platform"],
            "ruby_version": v["ruby_version"],
            "rubygems_version": v["rubygems_version"],
            "prerelease": v["prerelease"],
            "spec_sha": v["spec_sha"],
            "compact_index_checksum_match": True,
        }))
        docs[d["_id"]] = {k: v for k, v in d.items() if k != "_id"}

    # 3. diffend versions-page capture doc
    p = base_doc("diffend_page", "diffend:fieldnotes")
    fpath = D + "/diffend-page.html"
    p.update({
        "gem": "fieldnotes",
        "package": "fieldnotes",
        "file": "diffend-page.html",
        "sha256": sha256_file(fpath),
        "size_bytes": os.path.getsize(fpath),
        "source_url": "https://my.diffend.io/gems/fieldnotes",
        "retrieved_via": "diffend versions page (read-only GET, single request, http 200)",
        "retrieved_at": NOW,
        "status": "live",
        "diffend_versions": [
            {"version": "0.1.0", "diff_ts": "2026-09-05T21:20:00Z",
             "diff_ts_raw": "September 05, 2026 21:20"},
            {"version": "0.1.0->0.1.1", "diff_ts": "2026-09-20T16:34:00Z",
             "diff_ts_raw": "September 20, 2026 16:34"},
            {"version": "0.1.0->0.1.2", "diff_ts": "2026-09-20T18:47:00Z",
             "diff_ts_raw": "September 20, 2026 18:47"},
            {"version": "0.1.1->0.1.2", "diff_ts": "2026-09-20T18:47:00Z",
             "diff_ts_raw": "September 20, 2026 18:47"},
            {"version": "0.1.1->0.1.3", "diff_ts": "2026-09-20T20:18:00Z",
             "diff_ts_raw": "September 20, 2026 20:18"},
            {"version": "0.1.2->0.1.3", "diff_ts": "2026-09-20T20:18:00Z",
             "diff_ts_raw": "September 20, 2026 20:18"},
        ],
    })
    p["tags"] += ["status:live", "registry:diffend", "grammar:clean",
                  "diffend-flags:none"]
    p["labels"].update(flat({
        "diff_pairs": ["0.1.0", "0.1.0->0.1.1", "0.1.0->0.1.2",
                       "0.1.1->0.1.2", "0.1.1->0.1.3", "0.1.2->0.1.3"],
        "security_flags_on_page": "none observed",
        "diff_detail_pages_fetched": False,
        "note": "diff-detail pages (which embed file contents) intentionally not fetched; metadata lane only",
    }))
    docs[p["_id"]] = {k: v for k, v in p.items() if k != "_id"}

    # 4. grammar-sweep summary doc
    s = base_doc("grammar_sweep", "sweep:fieldnotes-gem")
    s.update({
        "gem": "fieldnotes",
        "package": "fieldnotes",
        "description": "Campaign-grammar sweep over all 4 captured metadata files "
                       "(zz/oai/tryzz/go-import/web_hooks/A000/ZZEND/jina.ai/md.succ.ai/rmn.re): 0 hits.",
        "file": "grammar-sweep.json",
        "sha256": sha256_file(D + "/grammar-sweep.json"),
        "source_url": "",
        "retrieved_at": NOW,
        "status": "live",
    })
    s["tags"] += ["grammar:clean", "sweep:campaign-grammar"]
    s["labels"].update(flat({
        "files_swept": list(sweep["files"].keys()),
        "hits_total": total_hits,
        "swept_at": sweep["swept_at"],
    }))
    docs[s["_id"]] = {k: v for k, v in s.items() if k != "_id"}
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
    mode = sys.argv[1] if len(sys.argv) > 1 else "--load"
    if mode == "--create":
        ensure_index()
    elif mode == "--load":
        ensure_index()
        docs = build_docs()
        print("docs built:", len(docs))
        ok, fail = bulk_load(docs)
        print("bulk ok:", ok, "fail:", fail)
    elif mode == "--verify":
        print("verified count in index:", verify())
    else:
        print("usage: --create | --load | --verify")
