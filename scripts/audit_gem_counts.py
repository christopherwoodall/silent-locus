"""Read-only audit: reconcile rubygems-goimport-campaign _count vs _cat vs on-disk sources.

Usage: python3 scripts/audit_gem_counts.py
Compares:
  - ES _count (authoritative live docs)
  - ES _cat/indices docs.count / docs.deleted
  - terms aggs on record_kind / event.dataset / observer.product / wave
  - on-disk row counts with deterministic-_id dedup applied (mirrors ingest scripts)
Prints a composition table. Makes no writes.
"""
import os, sys, json, hashlib, urllib.request
from collections import Counter

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
IDX = "rubygems-goimport-campaign"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def req(method, path, body=None):
    r = urllib.request.Request(ES + path,
                               data=(json.dumps(body).encode() if body else None),
                               method=method)
    r.add_header("Content-Type", "application/json")
    add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=180) as resp:
        return read_json_response(resp)


def count_lines(path):
    try:
        with open(path) as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return None


def unique_ids_jsonl(path, id_fn, skip_blank=True):
    ids = set()
    n = 0
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line and skip_blank:
                    continue
                n += 1
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                i = id_fn(r)
                if i is not None:
                    ids.add(i)
    except FileNotFoundError:
        return None, None
    return n, len(ids)


def main():
    print("=== hosted index (read-only) ===")
    count = req("GET", f"/{IDX}/_count")["count"]
    cat = req("GET", f"/_cat/indices/{IDX}?format=json")[0]
    print(f"_count (authoritative): {count}")
    print(f"_cat docs.count: {cat['docs.count']}  docs.deleted: {cat['docs.deleted']}")
    es_kinds = {}
    for field in ["record_kind", "event.dataset", "observer.product", "wave"]:
        ag = req("POST", f"/{IDX}/_search",
                 {"size": 0, "aggs": {"by": {"terms": {"field": field, "size": 50}}}})
        es_kinds[field] = {b["key"]: b["doc_count"]
                           for b in ag["aggregations"]["by"]["buckets"]}
    print("record_kind:", es_kinds["record_kind"],
          "sum =", sum(es_kinds["record_kind"].values()))

    print("\n=== on-disk sources (with ingest _id dedup) ===")
    rows = []
    # JFROG csv: header + data rows; _id = jfrog:<package>
    csv_lines = count_lines(BASE + "/data/gemstuffer-jfrog-2026-09-27.csv")
    pkgs = set()
    with open(BASE + "/data/gemstuffer-jfrog-2026-09-27.csv") as f:
        next(f)
        for line in f:
            pkgs.add(line.split(",")[0].strip().strip('"'))
    rows.append(("gemstuffer-jfrog-2026-09-27.csv", csv_lines, len(pkgs),
                 es_kinds["record_kind"].get("jfrog_inventory")))

    # gem-ioc-hits.jsonl -> record_kind hit
    n, u = unique_ids_jsonl(
        BASE + "/data/gem-ioc-hits.jsonl",
        lambda h: "hit:%s:%s:%s:%s:%s:%s" % (
            h.get("gem"), h.get("version"), h.get("fingerprint"),
            (h.get("file") or "").replace("/", "_"), h.get("line_no"),
            hashlib.sha256(str(h.get("matched_string", "")).encode()).hexdigest()[:16]))
    rows.append(("gem-ioc-hits.jsonl", n, u, es_kinds["record_kind"].get("hit")))

    # gem-ioc-log.jsonl -> download / extraction / diffend_harvest, _id = log:<rk>:<gem>:<ver>
    per_kind = Counter()
    per_kind_u = Counter()
    seen = set()
    with open(BASE + "/data/gem-ioc-log.jsonl") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            rk = r.get("record_kind")
            if rk not in ("download", "extraction", "diffend_harvest"):
                continue
            per_kind[rk] += 1
            _id = "log:%s:%s:%s" % (rk, r.get("gem"), r.get("version"))
            if _id not in seen:
                per_kind_u[rk] += 1
            seen.add(_id)
    for rk in ("download", "extraction", "diffend_harvest"):
        rows.append((f"gem-ioc-log.jsonl [{rk}]", per_kind[rk], per_kind_u[rk],
                     es_kinds["record_kind"].get(rk)))

    # gem-june18-wayback.jsonl -> wayback_metadata
    n, u = unique_ids_jsonl(
        BASE + "/data/gem-june18-wayback.jsonl",
        lambda h: "wayback:%s:%s" % (h.get("gem"), h.get("version") or "noversion"))
    rows.append(("gem-june18-wayback.jsonl", n, u,
                 es_kinds["record_kind"].get("wayback_metadata")))

    print(f"{'source':45s} {'lines':>7} {'uniq_id':>8} {'indexed':>8}  ok?")
    disk_total = 0
    for src, lines, uniq, idxd in rows:
        ok = "OK " if uniq == idxd else "DIFF"
        print(f"{src:45s} {lines!s:>7} {uniq!s:>8} {idxd!s:>8}  {ok}")
        disk_total += uniq or 0
    print(f"\ndisk unique total: {disk_total}   index _count: {count}   "
          f"{'AGREE' if disk_total == count else 'MISMATCH'}")


if __name__ == "__main__":
    main()
