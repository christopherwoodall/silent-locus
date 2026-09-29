#!/usr/bin/env python3
"""Ingest the termina.digital / swarm.termina.digital Wayback-recovered incident
database into its own `termina-digital` index.

The live /db/ is gone (404/503 as of 2026-09-28); Wayback holds 115 captures of
swarm.termina.digital (Sept 5-18, 2026) including the full incident DB
(incidents x campaigns x clusters x venues x actors x trackers). One ES doc per
recovered artifact. Conforms to the shared schema (notes/gems-es-mapping.json):
dataset detail lives in `labels` (flattened) + `tags`. No new top-level fields.

Usage:
  python3 es_ingest_termina.py --create   # create index with canonical mapping
  python3 es_ingest_termina.py --load     # bulk-load the docs
  python3 es_ingest_termina.py --verify   # count + kind breakdown
"""
import sys, json, os, re, html, hashlib, glob, urllib.request
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
# Resolve the data dir by slug so date-prefix renames don't break the path.
_SLUG = "termina-digital"
_matches = sorted(glob.glob(BASE + "/data/*-" + _SLUG))
assert _matches, f"no data dir matches slug {_SLUG}"
D = _matches[-1]
INDEX = os.path.basename(D)
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "termina-digital-ingest", "vendor": "swarmtraces-hunt",
            "type": "dataset"}

MAPPING_URL = (f"{BASE}/notes/gems-es-mapping.json")


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


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def text_of(p):
    raw = open(p, encoding="utf-8", errors="replace").read()
    t = re.sub(r"<script.*?</script>", "", raw, flags=re.S)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(re.sub(r"\s+", " ", t)).strip()


def kind_for(rel):
    for k in ("incident", "cluster", "campaign", "venue", "actor", "tracker"):
        if f"/db/{k}/" in rel or rel.startswith(f"db/{k}/"):
            return f"db_{k}"
    if "llms.txt" in rel:
        return "db_llms"
    if "search-config" in rel or "graph.json" in rel or "search/index" in rel:
        return "db_search_artifact"
    if "/db/page/" in rel:
        return "db_page"
    if rel.startswith("db/"):
        return "db_doc"
    if "swarmchasing" in rel:
        return "blog_post"
    if "rss" in rel:
        return "rss_feed"
    return "site_asset"


def build_docs():
    docs = {}
    ts = "2026-09-28T03:30:00Z"
    manifest = json.load(open(f"{D}/wayback_manifest.json"))
    url_by_file = {}
    for m in manifest:
        f = m.get("file")
        if f and m.get("status") == "ok":
            url_by_file[f] = m
    for root, _, files in os.walk(f"{D}/wayback"):
        for fn in sorted(files):
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, D)
            if fn.endswith(".tar.gz"):
                continue
            m = url_by_file.get(p, {})
            kind = kind_for(rel)
            labels = {
                "file": rel,
                "sha256": sha256_file(p),
                "byte_size": str(os.path.getsize(p)),
                "section": kind,
                "wayback_capture_ts": str(m.get("capture_ts", "")),
                "wayback_url": str(m.get("wayback_url", "")),
            }
            desc = ""
            if fn.endswith((".html", ".txt")):
                t = text_of(p)
                desc = t[:600]
                labels["text_chars"] = str(len(t))
            elif fn.endswith(".json"):
                desc = f"JSON artifact: {rel}"
            src = m.get("url", f"https://swarm.termina.digital/{rel.replace('wayback/','')}")
            tags = [f"kind:{kind}", "surface:termina-digital",
                    "provenance:wayback"]
            if "/db/incident/" in rel:
                tags.append("topic:incident-docket")
            if "/db/cluster/" in rel:
                tags.append("topic:task-family-cluster")
            if "/db/venue/" in rel:
                tags.append("topic:venue")
            if "/db/actor/" in rel:
                tags.append("topic:agent-handle")
            docs[f"termina:{rel}"] = {
                "@timestamp": ts,
                "event": {"dataset": INDEX, "created": NOW},
                "record_kind": kind,
                "description": desc,
                "source_url": src,
                "observer": OBSERVER,
                "tags": tags,
                "labels": labels,
            }
    # auxiliary captures (main-domain blog posts, rss, live probes)
    aux = [
        ("swarmchasing-i_20260907.html",
         "https://termina.digital/blog/swarmchasing-i",
         "Swarmchasing I (2026-09-05, via archived WASM strings): edit-war "
         "fingerprinting (~100 edit-revert cycles vs <=4 human), usemod/prowiki "
         "GET-mutation quirk, incident DB front page at swarm.termina.digital/db.",
         "blog_post"),
        ("swarmchasing-ii_20260907.html",
         "https://termina.digital/blog/swarmchasing-ii",
         "Swarmchasing II (2026-09-06): threat-model discussion (xor+gz+base64 "
         "vs grep monitoring), dsewiki docket link "
         "swarm.termina.digital/db/incident/dsewiki-2026-05.html.",
         "blog_post"),
        ("rss_live_2026-09-27.xml",
         "https://termina.digital/rss.xml",
         "Live RSS (2026-09-27): 10 items incl. Swarmchasing I/II/III "
         "(Sept 5/6/7); descriptions only — full text embedded in WASM.",
         "rss_feed"),
        ("swarm_live_home_2026-09-27.html",
         "https://swarm.termina.digital/",
         "Live swarm.termina.digital homepage (2026-09-27): WASM 'Swarm map' "
         "app shell; /db/ -> 404, /db/llms.txt -> 503 'public exports are "
         "temporarily unavailable'.",
         "site_probe"),
        ("sanctuary-df8ee5ab7c0cfec7_bg_20260907.wasm",
         "https://web.archive.org/web/20260907003610id_/https://termina.digital/sanctuary-df8ee5ab7c0cfec7_bg.wasm",
         "Archived WASM (818KB, 2026-09-07): full blog-post markdown embedded "
         "as strings; static strings extraction recovered Swarmchasing I/II "
         "full text (db moved to swarm.termina.digital subdomain).",
         "binary"),
    ]
    for fname, url, desc, kind in aux:
        p = f"{D}/{fname}"
        if not os.path.exists(p):
            continue
        docs[f"termina:aux:{fname}"] = {
            "@timestamp": ts,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": kind,
            "description": desc,
            "source_url": url,
            "observer": OBSERVER,
            "tags": [f"kind:{kind}", "surface:termina-digital"],
            "labels": {"file": fname, "sha256": sha256_file(p),
                       "byte_size": str(os.path.getsize(p))},
        }
    # recorded negatives
    negs = [
        ("neg_db_jsonl", "termina.digital /db/ incident JSONL: zero Wayback "
         "captures (CDX empty for termina.digital/db*); live /db* 404 as of "
         "2026-09-28. Recovered instead from swarm.termina.digital captures."),
        ("neg_tarball", "agent-pastes-2026-09-08.tar.gz: 503 'public exports "
         "are temporarily unavailable' both live and in Wayback; unrecoverable "
         "via these paths."),
        ("neg_archivetoday", "archive.today unreachable from this network "
         "(connection timeout); Wayback-only verification."),
    ]
    for nid, desc in negs:
        docs[f"termina:{nid}"] = {
            "@timestamp": ts,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "collection_negative",
            "description": desc,
            "source_url": "https://swarm.termina.digital/",
            "observer": OBSERVER,
            "tags": ["kind:negative", "surface:termina-digital"],
            "labels": {"negative_id": nid},
        }
    return docs


def cmd_create():
    m = json.load(open(MAPPING_URL))
    try:
        req("DELETE", f"/{INDEX}")
        print("deleted existing index")
    except Exception as e:
        print("no existing index:", str(e)[:80])
    r = req("PUT", f"/{INDEX}", {"mappings": m["mappings"]})
    print("created:", r.get("acknowledged"))


def cmd_load():
    docs = build_docs()
    print(f"built {len(docs)} docs")
    items = list(docs.items())
    ok = fail = 0
    for i in range(0, len(items), 200):
        chunk = items[i:i + 200]
        ndjson = "".join(
            json.dumps({"index": {"_index": INDEX, "_id": k}}) + "\n"
            + json.dumps(v) + "\n" for k, v in chunk)
        r = req("POST", "/_bulk", raw=ndjson)
        for it in r.get("items", []):
            if it.get("index", {}).get("status") in (200, 201):
                ok += 1
            else:
                fail += 1
                print("FAIL:", json.dumps(it)[:200])
    print(f"bulk: ok={ok} failed={fail}")


def cmd_verify():
    r = req("GET", f"/{INDEX}/_count")
    print("count:", r.get("count"))
    r = req("POST", f"/{INDEX}/_search",
            {"size": 0, "aggs": {"kinds": {"terms": {"field": "record_kind", "size": 40}}}})
    for b in r["aggregations"]["kinds"]["buckets"]:
        print(f"  {b['key']}: {b['doc_count']}")


if __name__ == "__main__":
    if "--create" in sys.argv:
        cmd_create()
    elif "--load" in sys.argv:
        cmd_load()
    elif "--verify" in sys.argv:
        cmd_verify()
    else:
        print("usage: --create | --load | --verify")
