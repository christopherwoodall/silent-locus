#!/usr/bin/env python3
"""Push the swarmtraces-hf-corpus datasets into a LOCAL Elasticsearch instance.

You run this on your own machine against your own ES (no vault, no cloud):

    # start local ES first, then from the repo root:
    python3 scripts/push_to_local_es.py --all
    python3 scripts/push_to_local_es.py --index 2026-05-12-university-shorteners
    python3 scripts/push_to_local_es.py --dry-run   # preview only

Env:
    ES_URL               target cluster (default http://localhost:9200)
    ES_USER / ES_PASS    basic auth if your local instance has security on

Only registered physical collections' staged events.jsonl and rollup.jsonl
are loaded. Each complete file must contain exactly one event.dataset, which
determines its index. Historical builder scripts are never executed.

Reruns are idempotent: every doc gets a deterministic _id (doc's own _id when
present, else sha256 of the canonical JSON), so re-pushing the same files is a
no-op. Use --reset to drop and rebuild an index whose staged files changed
shape (e.g. university-shorteners after the explicit-events re-explosion).

Stdlib only.
"""
import argparse, base64, hashlib, json, os, sys, urllib.request, urllib.error

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(BASE, "scripts", "local_es_manifest.json")
BATCH = 500
# canonical layout: only these filenames at a collection root are event data
EVENT_FILES = ("events.jsonl", "rollup.jsonl")
REGISTRY = os.path.join(BASE, "schema", "collections.json")


def inspect_file(path):
    """Preflight every row; never route a mixed or malformed file by row one."""
    dataset, count = None, 0
    with open(path, encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                doc = json.loads(line)
                value = doc["event"]["dataset"]
            except (ValueError, TypeError, KeyError) as exc:
                raise ValueError(f"{path}:{lineno}: invalid event.dataset/JSON") from exc
            if not isinstance(value, str) or not value:
                raise ValueError(f"{path}:{lineno}: missing event.dataset")
            if dataset is not None and value != dataset:
                raise ValueError(f"{path}:{lineno}: mixed event.dataset {value!r} != {dataset!r}")
            dataset, count = value, count + 1
    if not count:
        raise ValueError(f"{path}: empty event file")
    return dataset, count


def discover_staged(registry=None):
    """Discover registered physical event files, keyed by verified dataset."""
    if registry is None:
        with open(REGISTRY, encoding="utf-8") as fh:
            registry = json.load(fh)
    found = {}
    for collection in registry["collections"]:
        if collection.get("virtual"):
            continue
        name = collection["name"]
        rel_dir = collection.get("path", os.path.join("data", name))
        path = os.path.join(BASE, rel_dir)
        if not os.path.isdir(path):
            continue
        for fn in EVENT_FILES:
            fp = os.path.join(path, fn)
            if not os.path.isfile(fp):
                continue
            idx, _ = inspect_file(fp)
            expected = collection.get("index") if fn == "events.jsonl" else name + "-rollup"
            if not expected or idx != expected:
                raise ValueError(f"{fp}: dataset {idx!r} != registered {expected!r}")
            found.setdefault(idx, []).append(os.path.relpath(fp, BASE))
    return found


def es_req(es, method, path, body=None, raw=None, auth=None, timeout=120):
    url = es + path
    data = raw.encode() if raw is not None else (json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    if auth:
        r.add_header("Authorization", "Basic " + base64.b64encode(auth.encode()).decode())
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, json.load(resp)
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {}


def ping(es, auth):
    try:
        st, info = es_req(es, "GET", "/", auth=auth, timeout=10)
        return st == 200, info.get("version", {}).get("number", "?") if isinstance(info, dict) else "?"
    except Exception as e:
        return False, str(e)


def head_status(es, path, auth=None, timeout=30):
    r = urllib.request.Request(es + path, method="HEAD")
    if auth:
        r.add_header("Authorization", "Basic " + base64.b64encode(auth.encode()).decode())
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def ensure_index(es, auth, index, mapping_path, reset=False, dry=False):
    exists = head_status(es, f"/{index}", auth=auth) == 200
    if exists and reset and not dry:
        es_req(es, "DELETE", f"/{index}", auth=auth)
        exists = False
    if not exists and not dry:
        mapping = json.load(open(os.path.join(BASE, mapping_path)))
        st, resp = es_req(es, "PUT", f"/{index}", body={"mappings": mapping["mappings"]}, auth=auth)
        if st not in (200, 201):
            print(f"  !! create {index} -> {st} {str(resp)[:160]}")
            return False
    return True


def doc_id(doc):
    if isinstance(doc.get("_id"), str) and doc["_id"]:
        return doc["_id"]
    canon = json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canon.encode()).hexdigest()


def bulk_load(es, auth, index, files, dry=False):
    staged = 0
    for rel in files:
        path = os.path.join(BASE, rel)
        dataset, count = inspect_file(path)
        if dataset != index:
            raise ValueError(f"{path}: dataset {dataset!r} != target index {index!r}")
        staged += count
    if dry:
        return staged
    ok_total, fail_total = 0, 0
    for rel in files:
        path = os.path.join(BASE, rel)
        batch, buf = 0, []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                doc = json.loads(line)
                _id = doc.pop("_id", None) or doc_id(doc)
                buf.append(json.dumps({"index": {"_index": index, "_id": _id}}, ensure_ascii=False))
                buf.append(json.dumps(doc, ensure_ascii=False))
                batch += 1
                if batch >= BATCH:
                    ok, fail = send_batch(es, auth, index, buf)
                    ok_total += ok; fail_total += fail
                    batch, buf = 0, []
        if buf:
            ok, fail = send_batch(es, auth, index, buf)
            ok_total += ok; fail_total += fail
    return ok_total, fail_total, staged


def send_batch(es, auth, index, buf):
    st, resp = es_req(es, "POST", "/_bulk?refresh=false", raw="\n".join(buf) + "\n", auth=auth, timeout=300)
    if st != 200:
        print(f"  !! bulk -> {st} {str(resp)[:200]}")
        return 0, len(buf) // 2
    ok = fail = 0
    for item in resp.get("items", []):
        s = item.get("index", {}).get("status", 0)
        if s in (200, 201):
            ok += 1
        else:
            fail += 1
            if fail <= 3:
                print(f"  !! item error: {str(item)[:200]}")
    return ok, fail


def main():
    global BATCH
    ap = argparse.ArgumentParser()
    ap.add_argument("--es", default=os.environ.get("ES_URL", "http://localhost:9200"))
    selection = ap.add_mutually_exclusive_group()
    selection.add_argument("--index", help="only this index")
    selection.add_argument("--all", action="store_true", help="all registered staged indices")
    ap.add_argument("--reset", action="store_true", help="drop each index before loading")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--batch-size", type=int, default=BATCH)
    a = ap.parse_args()
    if not (a.all or a.index or a.dry_run):
        ap.error("select --all, --index, or --dry-run")
    if a.batch_size < 1:
        ap.error("--batch-size must be positive")
    BATCH = a.batch_size

    es = a.es.rstrip("/")
    auth = None
    if os.environ.get("ES_USER"):
        auth = f"{os.environ['ES_USER']}:{os.environ.get('ES_PASS', '')}"

    with open(MANIFEST, encoding="utf-8") as fh:
        man = json.load(fh)
    with open(REGISTRY, encoding="utf-8") as fh:
        registry = json.load(fh)
    try:
        staged = discover_staged(registry)
    except (ValueError, OSError) as exc:
        ap.error(str(exc))
    via_script = {e["index"] for e in man.get("via_script", [])}
    overlap = via_script & set(staged)
    if overlap:
        ap.error(f"via_script/staged overlap: {sorted(overlap)}")
    if via_script:
        ap.error("via_script is unsupported: stage events.jsonl/rollup.jsonl instead")
    wanted = {a.index} if a.index else None
    if wanted and not wanted.intersection(staged):
        ap.error(f"index {a.index!r} has no registered staged event file")
    if not a.dry_run:
        ok, info = ping(es, auth)
    else:
        ok, info = True, "offline"
    if not ok:
        print(f"cannot reach ES at {es}: {info}")
        print("start your local instance first (e.g. docker run -p 9200:9200 elasticsearch:8.x)")
        sys.exit(2)
    if not a.dry_run:
        print(f"target: {es} (v{info})")

    rows = []
    for idx in sorted(staged):
        files = staged[idx]
        if wanted and idx not in wanted:
            continue
        if a.dry_run:
            n = bulk_load(es, auth, idx, files, dry=True)
            rows.append((idx, "staged", n, "-", "dry-run"))
            continue
        # Validate once more immediately before index creation or deletion.
        bulk_load(es, auth, idx, files, dry=True)
        if not ensure_index(es, auth, idx, man["mapping"], reset=a.reset):
            rows.append((idx, "staged", "-", "-", "CREATE FAILED"))
            continue
        res = bulk_load(es, auth, idx, files)
        ok_n, fail_n, staged_n = res
        st, cnt = es_req(es, "GET", f"/{idx}/_count", auth=auth)
        live = cnt.get("count", "?") if st == 200 else f"ERR {st}"
        status = "OK" if (live == staged_n and fail_n == 0) else "CHECK"
        rows.append((idx, "staged", staged_n, live, f"{status} bulk_ok={ok_n} fail={fail_n}"))

    print(f"\n{'index':32s} {'track':10s} {'staged':>8s} {'_count':>8s}  status")
    for idx, track, staged, live, status in rows:
        print(f"{idx:32s} {track:10s} {str(staged):>8s} {str(live):>8s}  {status}")


if __name__ == "__main__":
    main()
