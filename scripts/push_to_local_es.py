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
no-op. Existing indices must have compatible mappings; --reset is only for
intentional rebuilds after staged files change shape.

Stdlib only.
"""
import argparse, base64, hashlib, json, os, sys, urllib.request, urllib.error
from urllib.parse import urlsplit

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
                raise ValueError(f"{path}:{lineno}: mixed event.dataset")
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
                raise ValueError(f"{fp}: dataset does not match registered index")
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
    except Exception:
        return False, "connection failed"


def is_local_es(url):
    parsed = urlsplit(url)
    return (parsed.scheme in ("http", "https")
            and parsed.hostname in ("localhost", "127.0.0.1", "::1")
            and not parsed.username and not parsed.password
            and parsed.path in ("", "/") and not parsed.query and not parsed.fragment)


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
    if dry:
        return True
    with open(os.path.join(BASE, mapping_path), encoding="utf-8") as fh:
        mapping = json.load(fh)["mappings"]
    status = head_status(es, f"/{index}", auth=auth)
    if status not in (200, 404):
        raise RuntimeError(f"index existence check failed (HTTP {status})")
    exists = status == 200
    if exists and reset and not dry:
        st, _ = es_req(es, "DELETE", f"/{index}", auth=auth)
        if st != 200:
            raise RuntimeError(f"index delete failed (HTTP {st})")
        exists = False
    if exists:
        st, resp = es_req(es, "GET", f"/{index}/_mapping", auth=auth)
        if st != 200 or not isinstance(resp, dict) or not isinstance(resp.get(index), dict):
            raise RuntimeError(f"mapping lookup failed (HTTP {st})")
        actual = resp[index].get("mappings")
        if not mapping_compatible(mapping, actual):
            raise RuntimeError("existing index mapping is incompatible (use --reset only if intended)")
    else:
        st, _ = es_req(es, "PUT", f"/{index}", body={"mappings": mapping}, auth=auth)
        if st not in (200, 201):
            raise RuntimeError(f"index create failed (HTTP {st})")
    return True


def mapping_compatible(expected, actual):
    """All declared mapping attributes must match; ES may add other fields."""
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and mapping_compatible(value, actual[key])
            for key, value in expected.items()
        )
    return expected == actual


def doc_id(doc):
    if "_id" in doc:
        if not isinstance(doc["_id"], str) or not doc["_id"]:
            raise ValueError("_id must be a nonempty string")
        return doc["_id"]
    canon = json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canon.encode()).hexdigest()


def expected_counts(index, files):
    """Stream staged rows and retain only IDs, not document bodies."""
    ids = set()
    staged = 0
    for rel in files:
        path = os.path.join(BASE, rel)
        with open(path, encoding="utf-8") as fh:
            for lineno, line in enumerate(fh, 1):
                if not line.strip():
                    continue
                try:
                    doc = json.loads(line)
                    if doc["event"]["dataset"] != index:
                        raise ValueError("wrong event.dataset")
                    ids.add(doc_id(doc))
                except (ValueError, TypeError, KeyError, AttributeError) as exc:
                    raise ValueError(f"{path}:{lineno}: invalid staged document") from exc
                staged += 1
    if not staged:
        raise ValueError(f"{index}: empty staged files")
    return staged, len(ids)


def bulk_load(es, auth, index, files, dry=False):
    staged = 0
    for rel in files:
        path = os.path.join(BASE, rel)
        dataset, count = inspect_file(path)
        if dataset != index:
            raise ValueError(f"{path}: dataset does not match target index")
        staged += count
    if dry:
        return staged
    ok_total, fail_total = 0, 0
    for rel in files:
        path = os.path.join(BASE, rel)
        batch, buf = 0, []
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                doc = json.loads(line)
                _id = doc_id(doc)
                doc.pop("_id", None)
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
        raise RuntimeError(f"bulk request failed (HTTP {st})")
    if not isinstance(resp, dict) or not isinstance(resp.get("items"), list) or len(resp["items"]) != len(buf) // 2:
        raise RuntimeError("bulk response has missing or mismatched items")
    ok = fail = 0
    for offset, item in enumerate(resp["items"]):
        action = item.get("index") if isinstance(item, dict) else None
        if not isinstance(action, dict) or action.get("_index") != index or action.get("_id") != json.loads(buf[2 * offset])["index"]["_id"]:
            raise RuntimeError("bulk response contains invalid item")
        s = action.get("status")
        if s in (200, 201) and not action.get("error"):
            ok += 1
        else:
            fail += 1
    if resp.get("errors") is not False or fail:
        raise RuntimeError(f"bulk response reported errors ({fail} failed items)")
    return ok, fail


def live_count(es, auth, index):
    st, resp = es_req(es, "GET", f"/{index}/_count", auth=auth)
    if st != 200 or not isinstance(resp, dict) or type(resp.get("count")) is not int:
        raise RuntimeError(f"count failed (HTTP {st})")
    return resp["count"]


def main():
    global BATCH
    ap = argparse.ArgumentParser()
    ap.add_argument("--es", default=os.environ.get("ES_URL", "http://localhost:9200"))
    selection = ap.add_mutually_exclusive_group()
    selection.add_argument("--index", help="only this index")
    selection.add_argument("--all", action="store_true", help="all registered staged indices")
    ap.add_argument("--reset", action="store_true", help="drop each index before loading")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify", action="store_true", help="read-only compare staged distinct IDs to live counts")
    ap.add_argument("--batch-size", type=int, default=BATCH)
    a = ap.parse_args()
    if not (a.all or a.index or a.dry_run):
        ap.error("select --all, --index, or --dry-run")
    if a.verify and (a.dry_run or a.reset):
        ap.error("--verify cannot be combined with --dry-run or --reset")
    if a.batch_size < 1:
        ap.error("--batch-size must be positive")
    BATCH = a.batch_size

    es = a.es.rstrip("/")
    if not a.dry_run and not is_local_es(es):
        ap.error("only local Elasticsearch URLs are supported")
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
        print("cannot reach ES (connection or authentication failed)")
        print("start your local instance first (e.g. docker run -p 9200:9200 elasticsearch:8.x)")
        sys.exit(2)
    if not a.dry_run:
        print(f"target: local ES (v{info})")

    rows = []
    failed = False
    for idx in sorted(staged):
        files = staged[idx]
        if wanted and idx not in wanted:
            continue
        try:
            # Validate before any write, including a requested reset.
            staged_n, expected = expected_counts(idx, files)
            if a.dry_run:
                rows.append((idx, "staged", staged_n, "-", f"dry-run distinct={expected}"))
                continue
            if a.verify:
                live = live_count(es, auth, idx)
            else:
                ensure_index(es, auth, idx, man["mapping"], reset=a.reset)
                ok_n, fail_n, loaded = bulk_load(es, auth, idx, files)
                if loaded != staged_n or ok_n != staged_n or fail_n:
                    raise RuntimeError("bulk acknowledgement count mismatch")
                st, _ = es_req(es, "POST", f"/{idx}/_refresh", auth=auth)
                if st != 200:
                    raise RuntimeError(f"refresh failed (HTTP {st})")
                live = live_count(es, auth, idx)
            status = "OK" if live == expected else "COUNT MISMATCH"
            failed |= live != expected
            rows.append((idx, "staged", staged_n, live, f"{status} expected={expected}"))
        except (ValueError, OSError, RuntimeError, TypeError, KeyError, urllib.error.URLError) as exc:
            # Never print ES response bodies or document values.
            failed = True
            message = str(exc) if isinstance(exc, RuntimeError) else "staged data or request failed"
            rows.append((idx, "staged", "-", "-", f"FAILED: {message}"))

    print(f"\n{'index':32s} {'track':10s} {'staged':>8s} {'_count':>8s}  status")
    for idx, track, staged, live, status in rows:
        print(f"{idx:32s} {track:10s} {str(staged):>8s} {str(live):>8s}  {status}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
