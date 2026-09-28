#!/usr/bin/env python3
"""Ingest the March-7 RCE-modality lane into its own `march7-rce-modality`
Elastic index under the canonical shared schema (notes/gems-es-mapping.json).

Record flavors: `package` (one per gem: oracle status + investigator-reported
modality), `version` (one per Diffend version, when present), `sweep_hit`
(pattern-sweep hits; investigator-reported hits carry confidence=medium and
explicit provenance). Mechanism/egress detail lives in `labels` (flattened) +
`tags`. Zero new top-level fields. event.dataset.keyword multi-field included
at creation.

Usage: python3 es_ingest_march7.py [--create|--load|--verify] (default: all)
"""
import json, os, sys, urllib.request
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
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = "/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus"
DIR = BASE + "/data/march7-rce-modality"
INDEX = "march7-rce-modality"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "march7-rce-ingest", "vendor": "nightingale-collective",
            "type": "dataset"}


def req(method, path, body=None, raw=None):
    url = ES + path
    data = raw.encode() if raw is not None else (
        json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    if ES.startswith(("http://localhost", "http://127.0.0.1", "http://[::1]")):
        pass  # local instance: no vault auth
    else:
        add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=180) as resp:
        return read_json_response(resp)


def base_doc(record_kind, tag_extra=()):
    return {
        "record_kind": record_kind,
        "event": {"dataset": INDEX, "created": NOW},
        "observer": dict(OBSERVER),
        "retrieved_via": "https://my.diffend.io + https://index.rubygems.org (read-only HTTPS GET)",
        "tags": ["source:march7-rce-modality", "lane:D"] + list(tag_extra),
        "labels": {
            "annotated_by": "es_ingest_march7",
            "modality": "registry-code-execution-probe",
            "investigator_attribution": "colonist-one post dfac3a74 (thecolony.ai, 2026-09-05); claims cited as reported, not independently re-verified",
        },
    }


def build_docs():
    results = json.load(open(DIR + "/results.json"))
    sweep = json.load(open(DIR + "/sweep.json"))
    docs = {}

    for name, pkg in results["gems"].items():
        acct = pkg.get("account", "")
        diffend = pkg.get("diffend", {})
        compact = pkg.get("compact", {})
        present = diffend.get("present", False)
        versions = diffend.get("versions", [])
        markers = sweep.get("mechanism_markers", {}).get(name, [])
        egress = sweep.get("egress_targets", {}).get(name, [])

        pd = base_doc("package")
        pd.update({
            "package": name,
            "gem": name,
            "status": "dead",
            "source_url": f"https://my.diffend.io/gems/{name}",
            "diff_url": f"https://my.diffend.io/gems/{name}",
            "download_url": "",
            "versions": versions,
            "version_count": len(versions),
            "meta_summary": ("Registry code-execution probe (doc-builder RCE + egress test), reported by colonist-one; "
                             "all versions yanked from rubygems.org (compact-index 404) and absent from Diffend."),
            "tags": pd["tags"] + ["status:dead", "modality:rce-probe",
                                  f"diffend:{'present' if present else 'absent'}",
                                  f"account:{acct}"],
            "labels": {
                **pd["labels"],
                "owner_account": acct,
                "diffend_page_status": str(diffend.get("page_status")),
                "diffend_page_redirect": diffend.get("page_redirect", ""),
                "diffend_note": diffend.get("note", ""),
                "compact_index_status": str(compact.get("status")),
                "egress_targets": "; ".join(egress),
                "mechanism_markers": "; ".join(markers),
            },
        })
        docs[f"package:{name}"] = pd

        for v in versions:
            ts = (diffend.get("version_diff_ts") or {}).get(v)
            vd = base_doc("version")
            vd.update({
                "package": name,
                "gem": name,
                "version": v,
                "status": "dead",
                "diff_url": f"https://my.diffend.io/gems/{name}/{v}",
                "source_url": f"https://my.diffend.io/gems/{name}/{v}",
                "tags": vd["tags"] + ["status:dead", f"account:{acct}"],
                "labels": {**vd["labels"],
                           "diffend_diff_ts": ts or ""},
            })
            if ts:
                vd["snapshot_ts"] = ts
            docs[f"version:{name}:{v}"] = vd

        for hit in sweep.get("hits", {}).get(name, []):
            hid = f"sweep:{name}:{hit['version']}:{hit['pattern']}"
            hd = base_doc("sweep_hit")
            hd.update({
                "package": name,
                "gem": name,
                "version": hit["version"],
                "fingerprint": hit["pattern"],
                "matched_string": hit["match"],
                "line_no": hit.get("line_no", 0),
                "diff_url": f"https://my.diffend.io/gems/{name}/{hit['version']}",
                "confidence": "medium",
                "tags": hd["tags"] + [f"mechanism:{hit['family']}",
                                      f"account:{acct}"],
                "labels": {**hd["labels"],
                           "pattern_family": hit["family"],
                           "hit_provenance": hit.get("provenance", ""),
                           "line": hit.get("line", "")[:500]},
            })
            docs[hid] = hd
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
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("all", "--create", "create"):
        ensure_index()
    if mode in ("all", "--load", "load"):
        docs = build_docs()
        print("docs built:", len(docs))
        ok, fail = bulk_load(docs)
        print("bulk ok:", ok, "fail:", fail)
    if mode in ("all", "--verify", "verify"):
        print("verified count in index:", verify())
