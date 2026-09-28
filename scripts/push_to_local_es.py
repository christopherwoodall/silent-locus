#!/usr/bin/env python3
"""Push the swarmtraces-hf-corpus datasets into a LOCAL Elasticsearch instance.

You run this on your own machine against your own ES (no vault, no cloud):

    # start local ES first, then from the repo root:
    python3 scripts/push_to_local_es.py --all
    python3 scripts/push_to_local_es.py --index university-shorteners --reset
    python3 scripts/push_to_local_es.py --dry-run   # preview only

Env:
    ES_URL               target cluster (default http://localhost:9200)
    ES_USER / ES_PASS    basic auth if your local instance has security on

Two tracks (see scripts/local_es_manifest.json):
  staged      verified final shared-schema JSONL -> bulk-loaded directly here.
  via_script  docs are built by a transform inside the ingest script -> the
              driver runs that script as a subprocess with SWARMTRACES_ES_URL
              pointed at your local instance. The ingest scripts honor that
              env var and skip vault auth for localhost.

Reruns are idempotent: every doc gets a deterministic _id (doc's own _id when
present, else sha256 of the canonical JSON), so re-pushing the same files is a
no-op. Use --reset to drop and rebuild an index whose staged files changed
shape (e.g. university-shorteners after the explicit-events re-explosion).

Stdlib only.
"""
import argparse, base64, hashlib, json, os, subprocess, sys, urllib.request, urllib.error

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(BASE, "scripts", "local_es_manifest.json")
BATCH = 500


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
        if not os.path.exists(path):
            print(f"  !! missing staged file: {rel}")
            return None
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    staged += 1
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
                try:
                    doc = json.loads(line)
                except ValueError:
                    fail_total += 1
                    continue
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


def run_script(es, script_rel, dry=False):
    """Run an ingest script against the local ES, picking its CLI convention."""
    path = os.path.join(BASE, script_rel)
    src = open(path).read()
    if "def main():" in src:
        cmds = [[sys.executable, path]]                      # main() loads by default
    else:
        cmds = [[sys.executable, path, "--create"],          # --create/--load/--verify style
                [sys.executable, path, "--load"]]
    env = dict(os.environ, SWARMTRACES_ES_URL=es)
    for cmd in cmds:
        label = " ".join([os.path.basename(cmd[1])] + cmd[2:])
        if dry:
            print(f"  would run: SWARMTRACES_ES_URL={es} {label}")
            continue
        print(f"  run: {label}")
        p = subprocess.run(cmd, cwd=BASE, env=env, capture_output=True, text=True, timeout=1800)
        out = (p.stdout or "") + (p.stderr or "")
        if p.returncode != 0 and "already exists" in out.replace("_", " "):
            print(f"  note: {label} -- index already exists, continuing")
            continue
        tail = (p.stdout or "").strip().splitlines()[-4:]
        for t in tail:
            print(f"    | {t[:160]}")
        if p.returncode != 0:
            print(f"  !! exit {p.returncode}: {(p.stderr or '').strip().splitlines()[-1:]}")
            return False
    return True


def main():
    global BATCH
    ap = argparse.ArgumentParser()
    ap.add_argument("--es", default=os.environ.get("ES_URL", "http://localhost:9200"))
    ap.add_argument("--index", help="only this index")
    ap.add_argument("--all", action="store_true", help="all indices in the manifest")
    ap.add_argument("--reset", action="store_true", help="drop each index before loading")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--skip-scripts", action="store_true", help="staged JSONL only")
    ap.add_argument("--batch-size", type=int, default=BATCH)
    a = ap.parse_args()
    BATCH = a.batch_size

    es = a.es.rstrip("/")
    auth = None
    if os.environ.get("ES_USER"):
        auth = f"{os.environ['ES_USER']}:{os.environ.get('ES_PASS', '')}"

    man = json.load(open(MANIFEST))
    ok, info = ping(es, auth)
    if not ok and not a.dry_run:
        print(f"cannot reach ES at {es}: {info}")
        print("start your local instance first (e.g. docker run -p 9200:9200 elasticsearch:8.x)")
        sys.exit(2)
    if not a.dry_run:
        print(f"target: {es} (v{info})")

    if a.index:
        wanted = {a.index}
    elif a.all or not a.dry_run:
        wanted = None  # everything
    else:
        wanted = None

    rows = []
    # staged track
    for entry in man["staged"]:
        idx = entry["index"]
        if wanted and idx not in wanted:
            continue
        if a.dry_run:
            n = bulk_load(es, auth, idx, entry["files"], dry=True)
            rows.append((idx, "staged", n if n is not None else "MISSING FILES", "-", "dry-run"))
            continue
        if not ensure_index(es, auth, idx, man["mapping"], reset=a.reset):
            rows.append((idx, "staged", "-", "-", "CREATE FAILED"))
            continue
        res = bulk_load(es, auth, idx, entry["files"])
        if res is None:
            rows.append((idx, "staged", "-", "-", "MISSING FILES"))
            continue
        ok_n, fail_n, staged_n = res
        st, cnt = es_req(es, "GET", f"/{idx}/_count", auth=auth)
        live = cnt.get("count", "?") if st == 200 else f"ERR {st}"
        status = "OK" if (live == staged_n and fail_n == 0) else "CHECK"
        rows.append((idx, "staged", staged_n, live, f"{status} bulk_ok={ok_n} fail={fail_n}"))

    # via_script track
    if not a.skip_scripts:
        for entry in man["via_script"]:
            idx = entry["index"]
            if wanted and idx not in wanted:
                continue
            if a.dry_run:
                for s in entry["scripts"]:
                    run_script(es, s, dry=True)
                rows.append((idx, "via_script", "-", "-", "dry-run"))
                continue
            good = all(run_script(es, s) for s in entry["scripts"])
            st, cnt = es_req(es, "GET", f"/{idx}/_count", auth=auth)
            live = cnt.get("count", "?") if st == 200 else f"ERR {st} (index may not exist yet)"
            rows.append((idx, "via_script", "-", live, "OK" if good else "SCRIPT FAILED"))

    print(f"\n{'index':32s} {'track':10s} {'staged':>8s} {'_count':>8s}  status")
    for idx, track, staged, live, status in rows:
        print(f"{idx:32s} {track:10s} {str(staged):>8s} {str(live):>8s}  {status}")


if __name__ == "__main__":
    main()
