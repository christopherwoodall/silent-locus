#!/usr/bin/env python3
"""Ingest the SwarmTraces redacted dataset into a local `swarmtraces` index.

Source: data/raw/redacted.jsonl.gz (189,579 records, sha256-pinned in
data/raw/MANIFEST.json and data/swarmtraces_provenance.json).
Native record schema: id, cite, kind (payload|response|recovered_text),
parent_id, time_utc (null dataset-wide), tags, text.

Native fields are preserved verbatim and wrapped in the shared corpus schema
(notes/gems-es-mapping.json): @timestamp, event.dataset, observer,
record_kind. Deterministic _id = record id (R0000001...), so re-runs are
idempotent. Read-only against the raw file; payloads are data, never executed.

Usage:
  python3 es_ingest_swarmtraces.py --create   # create index with mapping
  python3 es_ingest_swarmtraces.py --load     # bulk-load all records
  python3 es_ingest_swarmtraces.py --verify   # count vs MANIFEST expectation
  python3 es_ingest_swarmtraces.py --dry-run  # count + kind histogram, no writes

Env: SWARMTRACES_ES_URL (default http://localhost:9200), ES_USER / ES_PASS.
Stdlib only.
"""
import sys, os, json, gzip, base64, urllib.request, urllib.error
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "data", "raw", "redacted.jsonl.gz")
PROV = os.path.join(BASE, "data", "swarmtraces_provenance.json")
MAPPING = os.path.join(BASE, "notes", "gems-es-mapping.json")
INDEX = "swarmtraces"
EXPECTED = 189579  # data/raw/MANIFEST.json: 91037 payload + 23008 response + 75534 recovered_text
ES = os.environ.get("SWARMTRACES_ES_URL",
                    os.environ.get("ES_URL", "http://localhost:9200")).rstrip("/")
BATCH = 1000
NOW = datetime.now(timezone.utc).isoformat()
OBSERVER = {"product": "swarmtraces-ingest", "vendor": "swarmtraces-hunt",
            "type": "dataset"}

# Extra fields on top of the shared mapping: the native SwarmTraces schema.
NATIVE_FIELDS = {
    "id": {"type": "keyword"},
    "cite": {"type": "keyword"},
    "kind": {"type": "keyword"},
    "parent_id": {"type": "keyword"},
    "time_utc": {"type": "date"},
    "text": {"type": "text"},
}


def req(method, path, body=None, raw=None, timeout=300):
    data = raw.encode() if raw is not None else (
        json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(ES + path, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    user = os.environ.get("ES_USER")
    if user:
        r.add_header("Authorization", "Basic " + base64.b64encode(
            f"{user}:{os.environ.get('ES_PASS', '')}".encode()).decode())
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            payload = resp.read().decode()
            return resp.status, json.loads(payload) if payload else {}
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {}


def retrieved_date():
    try:
        prov = json.load(open(PROV))
        return prov.get("retrieval_date", "2026-09-27")
    except Exception:
        return "2026-09-27"


def build_doc(rec):
    tags = rec.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    kind = rec.get("kind")
    return {
        "@timestamp": rec.get("time_utc") or retrieved_date(),
        "event": {"dataset": INDEX, "created": NOW},
        "observer": OBSERVER,
        "record_kind": kind,
        # native schema, verbatim
        "id": rec.get("id"),
        "cite": rec.get("cite"),
        "kind": kind,
        "parent_id": rec.get("parent_id"),
        "time_utc": rec.get("time_utc"),
        "tags": tags + ["dataset:swarmtraces", f"kind:{kind}"],
        "text": rec.get("text"),
    }


def cmd_create():
    mapping = json.load(open(MAPPING))
    mapping["mappings"]["properties"].update(NATIVE_FIELDS)
    st, _ = req("HEAD", f"/{INDEX}")
    if st == 200:
        print(f"index {INDEX} already exists (delete it first to recreate)")
        return
    st, resp = req("PUT", f"/{INDEX}", body={"mappings": mapping["mappings"]})
    print("created:", resp.get("acknowledged") if st in (200, 201)
          else f"FAILED {st} {str(resp)[:200]}")


def cmd_load():
    buf, batch = [], 0
    ok_total = fail_total = n = 0

    def flush():
        nonlocal buf, batch, ok_total, fail_total
        if not buf:
            return
        st, resp = req("POST", "/_bulk?refresh=false", raw="\n".join(buf) + "\n")
        if st != 200:
            print(f"!! bulk -> {st} {str(resp)[:200]}")
            fail_total += batch
        else:
            for item in resp.get("items", []):
                s = item.get("index", {}).get("status", 0)
                if s in (200, 201):
                    ok_total += 1
                else:
                    fail_total += 1
                    if fail_total <= 3:
                        print(f"!! item error: {str(item)[:200]}")
        buf, batch = [], 0

    with gzip.open(SRC, "rt", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            _id = rec.get("id")
            if not _id:
                fail_total += 1
                continue
            buf.append(json.dumps({"index": {"_index": INDEX, "_id": _id}},
                                  ensure_ascii=False))
            buf.append(json.dumps(build_doc(rec), ensure_ascii=False))
            batch += 1
            n += 1
            if batch >= BATCH:
                flush()
            if n % 20000 == 0:
                print(f"{n} records...", flush=True)
    flush()
    print(f"loaded ok={ok_total} fail={fail_total} (of {n})")


def cmd_verify():
    st, resp = req("GET", f"/{INDEX}/_count")
    count = resp.get("count", "?") if st == 200 else f"ERR {st}"
    status = "OK" if count == EXPECTED else "CHECK"
    print(f"count: {count} (expected {EXPECTED}) {status}")


def cmd_dry_run():
    kinds = {}
    n = 0
    with gzip.open(SRC, "rt", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            kinds[rec.get("kind")] = kinds.get(rec.get("kind"), 0) + 1
            n += 1
    print(f"records: {n} (expected {EXPECTED}) "
          f"{'OK' if n == EXPECTED else 'CHECK'}")
    for k, v in sorted(kinds.items()):
        print(f"  {k}: {v}")
    print("dry-run: nothing written. Load with: make ingest-swarmtraces")


if __name__ == "__main__":
    if "--create" in sys.argv:
        cmd_create()
    elif "--load" in sys.argv:
        cmd_load()
    elif "--verify" in sys.argv:
        cmd_verify()
    elif "--dry-run" in sys.argv:
        cmd_dry_run()
    else:
        print("usage: --create | --load | --verify | --dry-run")
