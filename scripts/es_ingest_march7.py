#!/usr/bin/env python3
"""Ingest the March-7 RCE-modality lane into its own `march7-rce-modality`
Elastic index under the canonical shared schema (notes/gems-es-mapping.json).

Record flavors: `package` (one per package, metadata + modality analysis),
`version` (one per version, diff evidence), `sweep_hit` (pattern-sweep
marker hits in Diffend-rendered diffs). Mechanism/egress detail lives in
`labels` (flattened) + `tags`. Zero new top-level fields.
event.dataset.keyword multi-field included at creation.

Usage: python3 es_ingest_march7.py [--create|--load|--verify] (default: all)
"""
import json, os, sys, urllib.request
from datetime import datetime, timezone

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
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
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=180) as resp:
        return read_json_response(resp)


def base_doc(record_kind, tag_extra=()):
    return {
        "record_kind": record_kind,
        "event": {"dataset": INDEX, "created": NOW},
        "observer": dict(OBSERVER),
        "retrieved_via": "https://my.diffend.io (read-only HTTPS GET)",
        "tags": ["source:march7-rce-modality", "lane:D"] + list(tag_extra),
        "labels": {"annotated_by": "es_ingest_march7",
                   "modality": "registry-code-execution-probe",
                   "investigator_attribution": "colonist-one via thecolony.ai incident wiki (reported, not independently re-verified)"},
    }


def build_docs():
    results = json.load(open(DIR + "/results.json"))
    sweep = json.load(open(DIR + "/sweep.json")) if os.path.exists(DIR + "/sweep.json") else {}
    docs = {}

    for name, pkg in results.items():
        # package record
        pd = base_doc("package")
        pd.update({
            "package": name,
            "gem": name,
            "status": "dead",
            "source_url": f"https://my.diffend.io/gems/{name}",
            "diff_url": f"https://my.diffend.io/gems/{name}",
            "versions": pkg.get("versions", []),
            "version_count": len(pkg.get("versions", [])),
            "meta_summary": "Registry code-execution probe (doc-builder RCE + egress test), reported by colonist-one; versions start 2026-03-07; all yanked as of 2026-09-28 (compact-index 404 / 200-empty oracle).",
            "tags": pd["tags"] + ["status:dead", "modality:rce-probe"],
            "labels": {
                **pd["labels"],
                "diffend_status": str(pkg.get("diffend_status")),
                "compact_index_status": str(pkg.get("compact_status")),
                "egress_targets": "; ".join(sweep.get("egress_targets", {}).get(name, [])),
                "mechanism_markers": "; ".join(sweep.get("mechanism_markers", {}).get(name, [])),
                "first_version": (pkg.get("versions") or [""])[0],
                "note": "; ".join(pkg.get("notes", [])),
            },
        })
        docs[f"package:{name}"] = pd

        # version records
        for v in pkg.get("versions", []):
            vd = base_doc("version")
            files = (pkg.get("files") or {}).get(v, [])
            vd.update({
                "package": name,
                "gem": name,
                "version": v,
                "status": "dead",
                "diff_url": f"https://my.diffend.io/gems/{name}/{v}",
                "source_url": f"https://my.diffend.io/gems/{name}/{v}",
                "sha256": (pkg.get("diff_sha256") or {}).get(v),
                "file_count": len(files),
                "tags": vd["tags"] + ["status:dead"],
                "labels": {
                    **vd["labels"],
                    "diff_files": "; ".join(files[:50]),
                    "egress_targets": "; ".join(sweep.get("egress_targets", {}).get(f"{name}:{v}", [])),
                    "mechanism_markers": "; ".join(sweep.get("mechanism_markers", {}).get(f"{name}:{v}", [])),
                },
            })
            docs[f"version:{name}:{v}"] = vd

        # sweep_hit records
        for hit in (sweep.get("hits", {}).get(name, [])):
            hid = f"sweep:{name}:{hit['version']}:{hit['pattern']}"
            hd = base_doc("sweep_hit")
            hd.update({
                "package": name,
                "gem": name,
                "version": hit["version"],
                "fingerprint": hit["pattern"],
                "matched_string": hit["match"],
                "file": hit.get("file", ""),
                "line_no": hit.get("line_no", 0),
                "diff_url": f"https://my.diffend.io/gems/{name}/{hit['version']}",
                "confidence": "high" if hit["pattern"] in ("egress-host", "rce-sink") else "medium",
                "tags": hd["tags"] + [f"mechanism:{hit['family']}"],
                "labels": {**hd["labels"], "pattern_family": hit["family"]},
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
