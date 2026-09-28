#!/usr/bin/env python3
"""Full-index export via the scroll API. Writes <index>-<ts>.jsonl.gz.
Each line: {"_id": ..., "_source": {...}} — restore by converting lines
to _bulk action pairs (see MANIFEST.md). Read-only against ES.
Usage: python3 es_export.py <index> <outdir> [scroll_size]
"""
import sys, os, json, gzip, hashlib, datetime, urllib.request
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

ES = "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443"
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"

def req(method, path, body=None, timeout=120):
    url = ES + path
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        return read_json_response(resp)

def main():
    index, outdir = sys.argv[1], sys.argv[2]
    size = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    os.makedirs(outdir, exist_ok=True)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fname = f"{index}-{ts}.jsonl.gz"
    fpath = os.path.join(outdir, fname)

    expected = req("GET", f"/{index}/_count")["count"]
    print(f"[{index}] expected count: {expected}", flush=True)

    page = req("POST", f"/{index}/_search?scroll=10m",
               {"size": size, "sort": ["_doc"], "_source": True})
    scroll_id = page["_scroll_id"]
    n = 0
    sha = hashlib.sha256()
    with gzip.open(fpath, "wt", encoding="utf-8") as fh:
        while True:
            hits = page["hits"]["hits"]
            if not hits:
                break
            for h in hits:
                line = json.dumps({"_id": h["_id"], "_source": h["_source"]},
                                  ensure_ascii=False)
                fh.write(line + "\n")
                sha.update((line + "\n").encode("utf-8"))
                n += 1
            if n % 10000 == 0:
                print(f"[{index}] {n} docs...", flush=True)
            page = req("POST", "/_search/scroll",
                       {"scroll": "10m", "scroll_id": scroll_id})
            scroll_id = page["_scroll_id"]
    try:
        req("DELETE", "/_search/scroll", {"scroll_id": scroll_id})
    except Exception:
        pass

    print(f"[{index}] exported {n} docs to {fpath}", flush=True)
    print(f"[{index}] sha256={sha.hexdigest()}", flush=True)
    status = "OK" if n == expected else f"MISMATCH (expected {expected})"
    print(f"[{index}] {status}", flush=True)
    meta = {"index": index, "file": fname, "ts_utc": ts,
            "expected_count": expected, "exported_count": n,
            "sha256": sha.hexdigest(), "status": status}
    with open(fpath + ".meta.json", "w") as fh:
        json.dump(meta, fh, indent=2)

if __name__ == "__main__":
    main()
