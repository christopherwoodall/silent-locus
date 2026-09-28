#!/usr/bin/env python3
"""Ingest the IowaCollab pastebin cluster into its own `iowacollab-pastes` Elastic index.

Conforms to the canonical shared schema (notes/gems-es-mapping.json); paste
concepts map onto existing fields; paste-specific detail lives in `labels`
(flattened) + `tags`. Zero new top-level fields.
event.dataset.keyword multi-field included at creation (uniform with the
other campaign indices).

Docs: data/iowacollab-pastes/<pasteid>.txt + dataset manifest dataset.jsonl
Usage: python3 es_ingest_iowacollab.py
"""
import json, sys, urllib.request, glob, os
from datetime import datetime, timezone

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = "/home/hatch/workspace/muse-home/projects/swarmtraces-hf-corpus"
PDIR = BASE + "/data/iowacollab-pastes"
INDEX = "iowacollab-pastes"
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "iowacollab-paste-ingest", "vendor": "nightingale-collective",
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
        elif isinstance(d, (list, tuple)) or isinstance(v, (list, tuple)):
            out[k] = ", ".join(str(x) for x in (v if isinstance(v, (list, tuple)) else [v])[:20])
        else:
            out[k] = str(v)
    return out


def epoch_to_iso(e):
    try:
        f = float(str(e).split(".")[0])
        if 10 ** 9 < f < 2 * 10 ** 9:
            return datetime.fromtimestamp(f, timezone.utc).isoformat()
    except Exception:
        return None
    return None


def build_docs():
    docs = {}
    man = {}
    for line in open(PDIR + "/dataset.jsonl"):
        r = json.loads(line)
        man[r["id"]] = r
    for txt_path in sorted(glob.glob(PDIR + "/*.txt")):
        pid = os.path.basename(txt_path).replace(".txt", "")
        body = open(txt_path).read()
        m = man.get(pid, {})
        title = m.get("title") or ""
        ts = None
        for d in m.get("source_date_literals", []):
            iso = epoch_to_iso(d)
            if iso and (ts is None or iso < ts):
                ts = iso
        if not ts and m.get("created_at_iso"):
            ts = m["created_at_iso"]
        doc = {
            "record_kind": "paste_text",
            "event": {"dataset": INDEX, "created": NOW},
            "observer": dict(OBSERVER),
            "retrieved_via": m.get("retrieved_via", "wayback-machine"),
            "source_url": (m.get("source_urls") or [""])[0],
            "file": pid + ".txt",
            "description": body,
            "sha256": m.get("body_sha256"),
            "size_bytes": m.get("body_bytes"),
            "tags": ["source:paste-linuxiarz", "cluster:iowacollab-relay"],
            "labels": {"annotated_by": "es_ingest_iowacollab"},
        }
        if ts:
            doc["@timestamp"] = ts
            doc["published_at"] = ts
        if m.get("wayback_snapshot"):
            doc["tags"].append("archived:wayback")
        if m.get("live_status"):
            doc["tags"].append("status:" + m["live_status"])
        fam = "iowa" if title.startswith("Iowa") else ("ref" if title.startswith("Ref") else "other")
        doc["tags"].append("family:" + fam)
        doc["labels"].update(flat({
            "paste_id": pid,
            "title": title,
            "handle": m.get("handle"),
            "views_at_capture": m.get("views_at_capture"),
            "capture_ts": m.get("capture_ts"),
            "created_reported": m.get("created_reported"),
            "expire": m.get("expire"),
            "relay_cluster": m.get("relay_cluster"),
            "contamination_caveat": m.get("contamination_caveat"),
            "origin_kinds": m.get("origin_kinds"),
            "corpus_record_ids": m.get("corpus_record_ids"),
        }))
        docs["paste:" + pid] = doc
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
    ensure_index()
    docs = build_docs()
    print("docs built:", len(docs))
    ok, fail = bulk_load(docs)
    print("bulk ok:", ok, "fail:", fail)
    print("verified count in index:", verify())
