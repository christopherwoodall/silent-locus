#!/usr/bin/env python3
"""Ingest the ludism-wikis Lane A dataset into its own `ludism-wikis` Elastic index.

Conforms to the canonical shared schema (notes/gems-es-mapping.json):
zero new top-level fields; claim/fetch metadata lives in `labels` + `tags`.
event.dataset.keyword multi-field included at creation (uniform with the
other campaign indices).

Doc kinds:
- wiki_claims: thecolony-wiki second-hand claim files (verbatim excerpts),
  verification=not_independently_verified, origin=thecolony-wiki.
- proxy_fetch: verbatim proxy fetch outcomes (body or failure record),
  verification=direct_proxy_fetch.
Pattern-battery hits (pattern-sweep.json) feed `tags` (pattern:<name>).

Usage: python3 es_ingest_ludism.py
"""
import json, os, sys, urllib.request
from datetime import datetime, timezone

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = "/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus"
PDIR = BASE + "/data/ludism-wikis"
INDEX = "ludism-wikis"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "ludism-wikis-ingest", "vendor": "nightingale-collective",
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


def load_manifest():
    out = {}
    mp = PDIR + "/manifest.jsonl"
    if os.path.exists(mp):
        for line in open(mp):
            line = line.strip()
            if line:
                m = json.loads(line)
                out[m["file"]] = m
    return out


def build_docs():
    sweep = {}
    sp = PDIR + "/pattern-sweep.json"
    if os.path.exists(sp):
        sweep = json.load(open(sp))
    manifest = load_manifest()
    docs = {}

    # --- wiki_claims docs (second-hand) ---
    claims = [
        ("thecolony-claims-ludism.md",
         "thecolony incident wiki §13 + swarm catalogue Surface #10: ludism.org claims",
         "ludism.org"),
        ("thecolony-claims-apchemwiki.md",
         "thecolony incident wiki §14 + swarm catalogue §2: ApchemWiki claims",
         "tmcleod.org"),
    ]
    for fname, desc, host in claims:
        p = PDIR + "/" + fname
        if not os.path.exists(p):
            continue
        body = open(p).read()
        m = manifest.get(fname, {})
        hits = (sweep.get(fname, {}) or {}).get("pattern_hits", {})
        doc = {
            "record_kind": "wiki_claims",
            "event": {"dataset": INDEX, "created": NOW},
            "observer": dict(OBSERVER),
            "retrieved_via": "thecolony-ai lane-I capture (third-party analysis, quoted verbatim)",
            "source_url": "https://thecolony.ai/wiki/openai-escapee-agent-incident-2026 (section varies)",
            "file": fname,
            "description": body[:60000],
            "sha256": m.get("sha256"),
            "size_bytes": m.get("bytes"),
            "tags": ["source:ludism-wikis", "verification:not_independently_verified",
                     "origin:thecolony-wiki", "target_host:" + host],
            "labels": {"annotated_by": "es_ingest_ludism",
                       "claim_topic": "ludism.org" if "ludism" in fname else "ApchemWiki",
                       "pattern_hits_json": json.dumps(hits)[:4000]},
        }
        for pn in hits:
            doc["tags"].append("pattern:" + pn)
        docs["claim:" + fname] = doc

    # --- proxy_fetch docs ---
    results = []
    for r in json.load(open(PDIR + "/raw/sweep-summary.json")):
        results.append((r, "raw/%s__%s.txt" % (r["target"], r["via"]), False))
    # include the two proxy health controls as fetch docs (kind:control)
    import glob as _glob
    for cp in sorted(_glob.glob(PDIR + "/raw/proxy_control__*.txt.meta.json")):
        cm = json.load(open(cp))
        rel = "raw/" + os.path.basename(cp).replace(".meta.json", "")
        results.append((cm, rel, True))
    for r, fname, is_control in results:
        meta = manifest.get(fname, {})
        if not r["ok"]:
            body = "FETCH FAILED via %s: %s\ntarget: %s\nproxy_url: %s" % (
                r["via"], r.get("error", "(no detail)"), r["target"], r["proxy_url"])
        else:
            fp = PDIR + "/" + fname
            raw_text = open(fp, "rb").read()
            try:
                body = raw_text.decode("utf-8", errors="replace")
            except Exception:
                body = repr(raw_text[:2000])
            if len(body) > 60000:
                body = body[:60000] + "\n...[truncated]..."
        hits = (sweep.get(fname, {}) or {}).get("pattern_hits", {})
        doc = {
            "record_kind": "proxy_fetch",
            "event": {"dataset": INDEX, "created": NOW},
            "observer": dict(OBSERVER),
            "retrieved_via": "public reader proxy: " + r["proxy_url"],
            "source_url": r["target"],
            "file": fname,
            "description": body,
            "sha256": meta.get("sha256"),
            "size_bytes": meta.get("bytes"),
            "@timestamp": r["fetched_at"],
            "tags": ["source:ludism-wikis",
                     "verification:direct_proxy_fetch",
                     "fetch_ok:" + str(r["ok"]).lower(),
                     "proxy:" + r["via"]] + (["kind:proxy_control"] if is_control else []),
            "labels": flat({
                "annotated_by": "es_ingest_ludism",
                "target_name": r["target"],
                "proxy_name": r["via"],
                "http_status": r.get("http_status"),
                "content_type": r.get("content_type"),
                "fetch_error": r.get("error"),
                "fetched_at": r["fetched_at"],
                "pattern_hits_json": json.dumps(hits)[:4000],
            }),
        }
        for pn in hits:
            doc["tags"].append("pattern:" + pn)
        docs["fetch:" + r["target"] + ":" + r["via"]] = doc
    return docs


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
