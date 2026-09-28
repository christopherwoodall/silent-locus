#!/usr/bin/env python3
"""Update paste-archive Elastic docs for the 66 recovered bodies.

Sets labels.body_recovered=true, labels.body_sha256 (computed from body
file), and key sweep findings in labels. Doc IDs: paste-archive:k4be:<id>
/ paste-archive:anna:<id>. Mirrors the req()/credential pattern in
es_ingest_paste_archive.py.
"""
import sys, json, pathlib
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
import urllib.request

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
ROOT = pathlib.Path("/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus")
D = ROOT / "data" / "paste-archive"
INDEX = "paste-archive"


def req(method, path, body=None):
    r = urllib.request.Request(ES + path,
                               data=json.dumps(body).encode() if body is not None else None,
                               method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=180) as resp:
        return read_json_response(resp)


def main():
    sweep = json.loads((D / "sweep_bodies.json").read_text())
    ops = []
    n = 0
    for res in sweep["results"]:
        pid = res["id"]
        host = res["host"]
        did = f"paste-archive:{'k4be' if host == 'k4be.pl' else 'anna'}:{pid}"
        labels = {
            "body_recovered": True,
            "body_sha256": res["sha256"],
            "body_bytes": res["bytes"],
            "body_structure": res["structure"],
            "sweep_tradecraft_hits": sorted(k for k, v in res["hits"].items()
                                            if k in ("zz", "oai", "epoch_nonce", "try_zz",
                                                     "proxy_wrapper", "laundering_chain",
                                                     "go_import", "web_hook", "chunk_marker")),
        }
        if res["structure"] == "link_render_probe":
            labels["probe_kind"] = "link-render"
        elif res["structure"] == "nsi_link_ref":
            labels["probe_kind"] = "nsi-reference"
        doc = {"labels": labels, "tags": ["body_recovered", f"body-structure:{res['structure']}"]}
        ops.append(json.dumps({"update": {"_index": INDEX, "_id": did}}))
        ops.append(json.dumps({"doc": doc, "doc_as_upsert": False}))
        n += 1
    payload = "\n".join(ops) + "\n"
    # raw bulk call
    req2 = urllib.request.Request(ES + "/_bulk", data=payload.encode(), method="POST")
    req2.add_header("Content-Type", "application/x-ndjson")
    add_surrogate_to_request(req2, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(req2, timeout=300) as resp:
        out = read_json_response(resp)
    fails = [i for i in out["items"] if i["update"]["status"] not in (200, 201)]
    print(f"bulk update: {n} docs, failures: {len(fails)}")
    for f in fails[:5]:
        print(json.dumps(f)[:300])


if __name__ == "__main__":
    main()
