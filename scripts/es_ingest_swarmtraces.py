#!/usr/bin/env python3
"""Ingest the SwarmTraces redacted dataset into a local `swarmtraces` index.

Source: data/raw/redacted.jsonl.gz (189,579 records, sha256-pinned in
data/raw/MANIFEST.json and data/raw/swarmtraces_provenance.json).
Native record schema: id, cite, kind (payload|response|recovered_text),
parent_id, time_utc (null dataset-wide), tags, text.

Native fields are preserved verbatim and wrapped in the shared corpus schema
(notes/gems-es-mapping.json): @timestamp, event.dataset, observer,
record_kind. Deterministic _id = record id (R0000001...), so re-runs are
idempotent. Read-only against the raw file; payloads are data, never executed.

Usage:
  python3 es_ingest_swarmtraces.py --create   # create index with mapping
  python3 es_ingest_swarmtraces.py --load     # bulk-load all records
  python3 es_ingest_swarmtraces.py --verify   # refresh + count vs source
  python3 es_ingest_swarmtraces.py --check-source # offline checksum/count/IDs
  python3 es_ingest_swarmtraces.py --dry-run  # count + kind histogram, no writes

Env: SWARMTRACES_ES_URL (default http://localhost:9200), ES_USER / ES_PASS.
Stdlib only.
"""
import sys, os, json, gzip, base64, hashlib, urllib.request, urllib.error
from functools import lru_cache
from urllib.parse import urlsplit

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "data", "raw", "redacted.jsonl.gz")
MANIFEST = os.path.join(BASE, "data", "raw", "MANIFEST.json")
PROV = os.path.join(BASE, "data", "raw", "swarmtraces_provenance.json")
MAPPING = os.path.join(BASE, "notes", "gems-es-mapping.json")
INDEX = "swarmtraces"
EXPECTED = 189579  # data/raw/MANIFEST.json: 91037 payload + 23008 response + 75534 recovered_text
EXPECTED_SHA256 = "7b66ab21674de52fcd3f557652f68b1801170c998e2f266862124e6edf283488"
ES = os.environ.get("SWARMTRACES_ES_URL",
                    os.environ.get("ES_URL", "http://localhost:9200")).rstrip("/")
BATCH = 1000
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


def is_local_es(url):
    parsed = urlsplit(url)
    return (parsed.scheme in ("http", "https")
            and parsed.hostname in ("localhost", "127.0.0.1", "::1")
            and not parsed.username and not parsed.password
            and parsed.path in ("", "/") and not parsed.query and not parsed.fragment)


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


@lru_cache(maxsize=1)
def retrieved_date():
    try:
        with open(PROV, encoding="utf-8") as fh:
            prov = json.load(fh)
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
        "event": {"dataset": INDEX, "created": retrieved_date()},
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


def source_records():
    """Validate IDs while streaming the source; never expose record contents."""
    with gzip.open(SRC, "rt", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                raise ValueError("blank source record")
            rec = json.loads(line)
            if not isinstance(rec, dict):
                raise ValueError("source record is not an object")
            yield rec


def check_source():
    with open(MANIFEST, encoding="utf-8") as fh:
        manifest = json.load(fh)
    entries = [entry for entry in manifest["files"]
               if entry.get("name") == os.path.basename(SRC)]
    if len(entries) != 1 or (entries[0].get("sha256") != EXPECTED_SHA256
                             or entries[0].get("total_records") != EXPECTED):
        raise ValueError("source manifest does not match pinned expectations")
    digest = hashlib.sha256()
    with open(SRC, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest() != EXPECTED_SHA256:
        raise ValueError("source checksum mismatch")
    count = 0
    for count, rec in enumerate(source_records(), 1):
        if rec.get("id") != f"R{count:07d}":
            raise ValueError(f"invalid source ID at record {count}")
    if count != EXPECTED:
        raise ValueError(f"source count {count} differs from expected {EXPECTED}")
    print(f"source OK: {count} records, sha256 {EXPECTED_SHA256}")
    return count


def cmd_create():
    with open(MAPPING, encoding="utf-8") as fh:
        mapping = json.load(fh)
    mapping["mappings"]["properties"].update(NATIVE_FIELDS)
    st, _ = req("HEAD", f"/{INDEX}")
    if st == 200:
        st, existing = req("GET", f"/{INDEX}/_mapping")
        actual = existing.get(INDEX, {}).get("mappings") if isinstance(existing, dict) else None
        if st != 200 or not mapping_compatible(mapping["mappings"], actual):
            raise RuntimeError(f"existing index {INDEX} has incompatible mapping (HTTP {st})")
        print(f"index {INDEX} already exists with compatible mapping")
        return
    if st != 404:
        raise RuntimeError(f"index lookup failed (HTTP {st})")
    st, resp = req("PUT", f"/{INDEX}", body={"mappings": mapping["mappings"]})
    if st not in (200, 201) or resp.get("acknowledged") is not True:
        raise RuntimeError(f"index creation failed (HTTP {st})")
    print(f"created: {INDEX}")


def mapping_compatible(expected, actual):
    """Compare declared mappings while allowing ES-added fields and defaults."""
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and mapping_compatible(value, actual[key])
            for key, value in expected.items()
        )
    return expected == actual


def cmd_load():
    check_source()  # No writes until both compressed bytes and record IDs are checked.
    buf, batch = [], 0
    ok_total = fail_total = n = 0

    def flush():
        nonlocal buf, batch, ok_total, fail_total
        if not buf:
            return
        st, resp = req("POST", "/_bulk?refresh=false", raw="\n".join(buf) + "\n")
        if st != 200 or not isinstance(resp, dict):
            print(f"!! bulk HTTP {st}", file=sys.stderr)
            fail_total += batch
        else:
            items = resp.get("items")
            if not isinstance(items, list) or len(items) != batch:
                fail_total += batch
                print("!! bulk response item count mismatch", file=sys.stderr)
                buf, batch = [], 0
                return
            batch_failed = 0
            for item in items:
                s = item.get("index", {}).get("status", 0) if isinstance(item, dict) else 0
                if s in (200, 201):
                    ok_total += 1
                else:
                    fail_total += 1
                    batch_failed += 1
                    if fail_total <= 3:
                        print(f"!! bulk item failed (HTTP {s})", file=sys.stderr)
            if resp.get("errors") is not False and batch_failed == 0:
                fail_total += batch
                ok_total -= batch
                print("!! bulk errors flag missing or inconsistent", file=sys.stderr)
        buf, batch = [], 0

    for n, rec in enumerate(source_records(), 1):
        _id = f"R{n:07d}"
        if rec.get("id") != _id:
            raise ValueError(f"source changed at record {n}")
        buf.append(json.dumps({"index": {"_index": INDEX, "_id": _id}},
                              ensure_ascii=False))
        buf.append(json.dumps(build_doc(rec), ensure_ascii=False))
        batch += 1
        if batch >= BATCH:
            flush()
        if n % 20000 == 0:
            print(f"{n} records...", flush=True)
    flush()
    print(f"loaded ok={ok_total} fail={fail_total} (of {n})")
    if n != EXPECTED or ok_total != EXPECTED or fail_total:
        raise RuntimeError("bulk load incomplete")


def cmd_verify():
    check_source()
    st, _ = req("POST", f"/{INDEX}/_refresh")
    if st != 200:
        raise RuntimeError(f"refresh failed (HTTP {st})")
    st, resp = req("GET", f"/{INDEX}/_count")
    if st != 200 or not isinstance(resp, dict) or type(resp.get("count")) is not int:
        raise RuntimeError(f"count failed (HTTP {st})")
    count = resp["count"]
    print(f"count: {count} (expected {EXPECTED}) "
          f"{'OK' if count == EXPECTED else 'CHECK'}")
    if count != EXPECTED:
        raise RuntimeError("index count mismatch")


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


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    for mode in ("create", "load", "verify", "check-source", "dry-run"):
        modes.add_argument(f"--{mode}", action="store_true")
    args = parser.parse_args(argv)
    if not (args.check_source or args.dry_run) and not is_local_es(ES):
        parser.error("only local Elasticsearch URLs are supported")
    try:
        if args.create:
            cmd_create()
        elif args.load:
            cmd_load()
        elif args.verify:
            cmd_verify()
        elif args.check_source:
            check_source()
        else:
            cmd_dry_run()
    except (OSError, ValueError, KeyError, TypeError, RuntimeError,
            urllib.error.URLError, json.JSONDecodeError) as exc:
        # Do not print exception text: HTTP and JSON errors can contain payloads.
        print(f"failed: {type(exc).__name__}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
