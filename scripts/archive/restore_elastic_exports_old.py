#!/usr/bin/env python3
"""Restore the elastic-exports/ cloud snapshot into a LOCAL Elasticsearch.

elastic-exports/ holds per-index scroll-API dumps written by es_export.py:
  <index>-<UTC ts>.jsonl.gz           one {"_id": ..., "_source": {...}} per line
  <index>-<UTC ts>.jsonl.gz.meta.json sidecar: sha256 (of decompressed lines),
                                      expected/exported counts, status
When several dumps exist for an index (pass 1 vs pass 2), the NEWEST wins.

Per index this script:
  1. streams the .gz, verifying sha256 + line count against the sidecar
     (with --dry-run it stops here: verify only, zero writes)
  2. creates the index with the canonical shared mapping
     (notes/gems-es-mapping.json) if it does not exist
  3. bulk-loads preserving the original _ids (idempotent: re-runs upsert
     the same docs)
  4. asserts _count == sidecar expected_count

Env: ES_URL (default http://localhost:9200), ES_USER / ES_PASS for basic auth.
Stdlib only.
"""
import argparse, base64, glob, gzip, hashlib, json, os, sys, urllib.request, urllib.error

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORTS = os.path.join(BASE, "elastic-exports")
MAPPING = os.path.join(BASE, "notes", "gems-es-mapping.json")
BATCH = 500


def es_req(es, auth, method, path, body=None, raw=None, timeout=300):
    data = raw.encode() if raw is not None else (
        json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(es + path, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    if auth:
        r.add_header("Authorization", "Basic " + base64.b64encode(auth.encode()).decode())
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            payload = resp.read().decode()
            return resp.status, json.loads(payload) if payload else {}
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {}


def latest_exports():
    """index -> (gz path, meta path) for the newest timestamp per index."""
    best = {}
    for gz in glob.glob(os.path.join(EXPORTS, "*.jsonl.gz")):
        name = os.path.basename(gz)
        # <index>-<YYYYMMDDTHHMMSSZ>.jsonl.gz ; index itself may contain '-'
        stem = name[: -len(".jsonl.gz")]
        idx, _, ts = stem.rpartition("-")
        if not idx or not ts:
            continue
        meta = gz + ".meta.json"
        if idx not in best or ts > best[idx][0]:
            best[idx] = (ts, gz, meta)
    return {idx: (gz, meta) for idx, (ts, gz, meta) in best.items()}


def verify_and_count(gz_path, meta):
    """Stream the dump; return (lines, sha_ok). Never touches ES."""
    sha = hashlib.sha256()
    n = 0
    with gzip.open(gz_path, "rt", encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            json.loads(line)  # parse check: every line must be valid JSON
            sha.update((line + "\n").encode("utf-8"))
            n += 1
    expected_sha = (meta or {}).get("sha256")
    sha_ok = (expected_sha is None) or (sha.hexdigest() == expected_sha)
    return n, sha_ok


def ensure_index(es, auth, index):
    st, _ = es_req(es, auth, "HEAD", f"/{index}")
    if st == 200:
        return True
    mapping = json.load(open(MAPPING))
    st, resp = es_req(es, auth, "PUT", f"/{index}",
                      body={"mappings": mapping["mappings"]})
    if st not in (200, 201):
        print(f"  !! create {index} -> {st} {str(resp)[:160]}")
        return False
    return True


def load_index(es, auth, index, gz_path):
    buf, batch = [], 0
    ok_total = fail_total = 0

    def flush():
        nonlocal buf, batch, ok_total, fail_total
        if not buf:
            return
        st, resp = es_req(es, auth, "POST", "/_bulk?refresh=false",
                          raw="\n".join(buf) + "\n")
        if st != 200:
            print(f"  !! bulk -> {st} {str(resp)[:200]}")
            fail_total += batch
        else:
            for item in resp.get("items", []):
                s = item.get("index", {}).get("status", 0)
                if s in (200, 201):
                    ok_total += 1
                else:
                    fail_total += 1
                    if fail_total <= 3:
                        print(f"  !! item error: {str(item)[:200]}")
        buf, batch = [], 0

    with gzip.open(gz_path, "rt", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            _id = rec.get("_id")
            src = rec.get("_source", {})
            if not _id:
                fail_total += 1
                continue
            buf.append(json.dumps({"index": {"_index": index, "_id": _id}},
                                  ensure_ascii=False))
            buf.append(json.dumps(src, ensure_ascii=False))
            batch += 1
            if batch >= BATCH:
                flush()
    flush()
    return ok_total, fail_total


def main():
    global BATCH
    ap = argparse.ArgumentParser()
    ap.add_argument("--es", default=os.environ.get("ES_URL", "http://localhost:9200"))
    ap.add_argument("--index", help="only this index")
    ap.add_argument("--dry-run", action="store_true",
                    help="verify sha256 + counts only, no writes")
    ap.add_argument("--batch-size", type=int, default=BATCH)
    a = ap.parse_args()
    BATCH = a.batch_size

    es = a.es.rstrip("/")
    auth = None
    if os.environ.get("ES_USER"):
        auth = f"{os.environ['ES_USER']}:{os.environ.get('ES_PASS', '')}"

    exports = latest_exports()
    if a.index:
        exports = {a.index: exports[a.index]} if a.index in exports else {}
    if not exports:
        print("no exports found in elastic-exports/")
        sys.exit(2)

    if not a.dry_run:
        st, info = es_req(es, auth, "GET", "/", timeout=10)
        if st != 200:
            print(f"cannot reach ES at {es} (HTTP {st}); start it first: make up")
            sys.exit(2)
        print(f"target: {es} (v{info.get('version', {}).get('number', '?')})")

    rows = []
    for idx in sorted(exports):
        gz_path, meta_path = exports[idx]
        meta = None
        if os.path.exists(meta_path):
            meta = json.load(open(meta_path))
        n, sha_ok = verify_and_count(gz_path, meta)
        exp = (meta or {}).get("expected_count", "?")
        rel = os.path.relpath(gz_path, BASE)
        if a.dry_run:
            status = "OK" if (sha_ok and (exp == "?" or n == exp)) else "MISMATCH"
            rows.append((idx, rel, n, exp, "sha256 ok" if sha_ok else "SHA256 BAD", status))
            continue
        if not sha_ok:
            rows.append((idx, rel, n, exp, "SHA256 BAD", "SKIPPED"))
            continue
        if not ensure_index(es, auth, idx):
            rows.append((idx, rel, n, exp, "-", "CREATE FAILED"))
            continue
        ok_n, fail_n = load_index(es, auth, idx, gz_path)
        st, cnt = es_req(es, auth, "GET", f"/{idx}/_count")
        live = cnt.get("count", "?") if st == 200 else f"ERR {st}"
        status = "OK" if (live == exp and fail_n == 0) else "CHECK"
        rows.append((idx, rel, n, live, f"bulk_ok={ok_n} fail={fail_n}", status))

    print(f"\n{'index':32s} {'lines':>8s} {'expected/live':>13s}  {'verify':10s}  status")
    for idx, rel, n, exp, verify, status in rows:
        print(f"{idx:32s} {n:>8d} {str(exp):>13s}  {verify:10s}  {status}")
    if a.dry_run:
        print("\ndry-run: nothing written. Run `make ingest-snapshot` to load.")


if __name__ == "__main__":
    main()
