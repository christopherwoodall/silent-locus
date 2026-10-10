#!/usr/bin/env python3
"""Rebuild the IowaCollab pastebin cluster Elastic docs for index
`2026-05-17-iowacollab-pastes`.

Repair history (2026-09-29): the original build inputs (`dataset.jsonl`
manifest in the old top-level format + `*.txt` bodies at the collection
root) were removed/moved by the 21312cf layout normalization, leaving this
script un-runnable. Nothing was actually lost:

- The paste bodies survive verbatim in `raw/<pasteid>.txt` (4 files).
- The manifest metadata survives, superset, in the staged `events.jsonl`
  (post-backfill `labels.*` form; the old `dataset.jsonl` blob was
  byte-identical to the staged `events.jsonl` blob b69982c3, i.e. it was
  absorbed, not deleted).
- The pre-backfill top-level manifest format is recoverable from git
  history (commit ad31cd4, `data/iowacollab-pastes/dataset.jsonl`) if ever
  needed.

So this script now does a TRUE RAW BUILD (not a blind re-emit of staged
events): it reads each `raw/<id>.txt` body, hard-verifies
sha256+byte-length against the staged metadata, and constructs the Elastic
docs from body + metadata. Any mismatch aborts before any doc is emitted.

Payload embedding: paste bodies are embedded in the optional top-level
`payloads` array (`schema/record.schema.json`, 2026-09-29), one
`{kind: paste_body, content_type: text/plain, ...}` entry per doc with
`byte_size`/`sha256` of the full body; `sha256`/`size_bytes` also sit
alongside at top level and full metadata is flattened in `labels`. All four
bodies are <= 270 bytes; the script enforces a 64 KiB cap per body (larger
bodies would abort the build rather than silently truncate). Empty bodies
get no payload entry.

Schema conformance: every built doc validates against
`schema/record.schema.json` (checked in-process via
`scripts/validate_schema.py::check`). Fixes vs the pre-repair version:
`fingerprint` (required) added, illegal top-level `published_at` dropped,
`@timestamp`/`event.created` are real ISO-8601 UTC values, and `labels`
keys/values obey the flat-scalars rule.

Docs built: 4 `paste_text` + 1 `live_recheck` (the workstream-C3 2026-09-28
live re-check recorded in the original script). Doc ids are deterministic:
`paste:<id>` and `recheck:2026-09-28`. Fingerprints: the staged event's
fingerprint for pastes; `sha256("iowacollab-pastes|live_recheck|2026-09-28")`
for the recheck (identity strings documented in PROVENANCE.md).

Usage:
    python3 es_ingest_iowacollab.py              # dry-run: build + validate, print summary
    python3 es_ingest_iowacollab.py --out DIR    # dry-run: write DIR/docs.jsonl, no network
    python3 es_ingest_iowacollab.py --load       # real ES bulk load (network + creds)
"""
import argparse
import glob
import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

import os
try:
    sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
    from dynamic_credentials import add_surrogate_to_request, read_json_response
except ImportError:  # local run: no vault on this machine, plain HTTP(S) instead
    def add_surrogate_to_request(request, *args, **kwargs):
        return None
    def read_json_response(response):
        import json as _json
        return _json.load(response)

ES = os.environ.get("SWARMTRACES_ES_URL", "https://agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud:443")
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = REPO_ROOT
PDIR = SCRIPT_DIR
INDEX = "2026-05-17-iowacollab-pastes"
OBSERVER = {"product": "iowacollab-paste-ingest", "vendor": "nightingale-collective",
            "type": "dataset"}

# Deterministic build constants (no wall-clock "now" in doc fields).
RECHECK_TS = "2026-09-28T11:35:00Z"          # workstream-C3 observation time
RECHECK_IDENTITY = "iowacollab-pastes|live_recheck|2026-09-28"
MAX_BODY_BYTES = 64 * 1024                  # payload cap; bodies here are <= 270 B
SENTINEL_TS = "1970-01-01T00:00:00Z"

# in-process schema validation (stdlib only)
sys.path.insert(0, BASE + "/scripts")
from validate_schema import check as schema_check  # noqa: E402


def req(method, path, body=None, raw=None):
    url = ES + path
    data = raw.encode() if raw is not None else (
        json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Content-Type", "application/json")
    if ES.startswith(("http://localhost", "http://127.0.0.1", "http://[::1]")):
        _es_user = os.environ.get("ES_USER")
        if _es_user:
            import base64 as _b64
            r.add_header("Authorization", "Basic " + _b64.b64encode(
                f"{_es_user}:{os.environ.get('ES_PASS', '')}".encode()).decode())
    else:
        add_surrogate_to_request(r, CRED, allowed_hosts=HOSTS)
    with urllib.request.urlopen(r, timeout=180) as resp:
        return read_json_response(resp)


def flat(d):
    """Flatten manifest metadata into schema-valid labels values.

    Scalars pass through; lists/tuples become comma-joined strings (capped
    at 20 items); None values are dropped. Dict values are rejected loudly
    rather than coerced (schema forbids nested objects in labels).
    """
    out = {}
    for k, v in d.items():
        if v is None:
            continue
        if isinstance(v, dict):
            raise ValueError(f"labels value for {k!r} is a nested object")
        if isinstance(v, (list, tuple)):
            out[k] = ", ".join(str(x) for x in v[:20])
        else:
            out[k] = v
    return out


def epoch_to_iso(e):
    try:
        f = float(str(e).split(".")[0])
        if 10 ** 9 < f < 2 * 10 ** 9:
            return datetime.fromtimestamp(f, timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return None
    return None


def load_staged_events():
    """Read the staged events.jsonl metadata (post-backfill labels.* form)."""
    events = {}
    path = PDIR + "/events.jsonl"
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            lab = rec.get("labels", {})
            pid = lab.get("id")
            if rec.get("record_kind") == "relay_paste" and pid:
                events[pid] = rec
            else:
                print(f"note: skipping non-relay_paste staged line {i} "
                      f"(kind={rec.get('record_kind')!r})", file=sys.stderr)
    return events


def read_verified_body(pid, meta_labels):
    """Read raw/<pid>.txt and hard-verify against staged metadata."""
    path = PDIR + f"/raw/{pid}.txt"
    with open(path, "r", encoding="utf-8") as f:
        body = f.read()
    raw = body.encode("utf-8")
    if len(raw) > MAX_BODY_BYTES:
        raise SystemExit(
            f"ABORT: raw/{pid}.txt is {len(raw)} bytes, over the "
            f"{MAX_BODY_BYTES}-byte payload cap")
    digest = hashlib.sha256(raw).hexdigest()
    expect_digest = meta_labels.get("body_sha256")
    expect_bytes = meta_labels.get("body_bytes")
    if expect_digest and digest != expect_digest:
        raise SystemExit(
            f"ABORT: sha256 mismatch for raw/{pid}.txt: "
            f"got {digest}, staged metadata says {expect_digest}")
    if expect_bytes is not None and len(raw) != expect_bytes:
        raise SystemExit(
            f"ABORT: byte-length mismatch for raw/{pid}.txt: "
            f"got {len(raw)}, staged metadata says {expect_bytes}")
    return body, digest, len(raw)


def event_timestamp(meta):
    """Deterministic @timestamp: staged event's own, else epoch literal,
    else the documented sentinel (schema rule)."""
    ts = meta.get("@timestamp")
    if ts:
        return ts, False
    for d in (meta.get("labels") or {}).get("source_date_literals", []):
        iso = epoch_to_iso(d)
        if iso:
            return iso, False
    return SENTINEL_TS, True


def build_paste_doc(pid, staged, body, digest, nbytes):
    lab = dict(staged.get("labels", {}))
    title = lab.get("title") or ""
    ts, used_sentinel = event_timestamp(staged)

    doc = {
        "record_kind": "paste_text",
        "fingerprint": staged.get("fingerprint"),
        "@timestamp": ts,
        "event": {"dataset": INDEX,
                  "created": staged.get("event", {}).get("created")},
        "observer": dict(OBSERVER),
        "retrieved_via": staged.get("retrieved_via", "wayback-machine"),
        "source_url": (lab.get("source_urls") or [""])[0],
        "file": "raw/" + pid + ".txt",
        "description": f"IowaCollab relay paste {pid} ({title})",
        "sha256": digest,
        "size_bytes": nbytes,
        "tags": ["source:paste-linuxiarz", "cluster:iowacollab-relay"],
        "labels": {"annotated_by": "es_ingest_iowacollab"},
    }
    if body:
        doc["payloads"] = [{
            "kind": "paste_body",
            "content_type": "text/plain",
            "content": body,
            "encoding": "text",
            "truncated": False,
            "byte_size": nbytes,
            "sha256": digest,
        }]
    if used_sentinel:
        doc["labels"]["timestamp_source"] = "fallback:no_recoverable_date"
    if lab.get("wayback_view_snapshot") or lab.get("wayback_raw_snapshot"):
        doc["tags"].append("archived:wayback")
    if lab.get("live_status"):
        doc["tags"].append("status:" + str(lab["live_status"]))
    fam = ("iowa" if title.startswith("Iowa")
           else ("ref" if title.startswith("Ref") else "other"))
    doc["tags"].append("family:" + fam)
    # staged metadata (superset): keep everything except fields promoted to
    # top level (sha256/size_bytes/source_url) or renamed (id -> paste_id).
    carry = {k: v for k, v in lab.items()
             if k not in ("id", "body_sha256", "body_bytes", "source_urls")}
    doc["labels"].update(flat({"paste_id": pid}))
    doc["labels"].update(flat(carry))
    return doc


def build_recheck_doc(created):
    """Deterministic rebuild of the workstream-C3 live re-check doc."""
    return {
        "record_kind": "live_recheck",
        "fingerprint": hashlib.sha256(
            RECHECK_IDENTITY.encode("utf-8")).hexdigest(),
        "@timestamp": RECHECK_TS,
        "event": {"dataset": INDEX, "created": created},
        "observer": dict(OBSERVER),
        "retrieved_via": "read-only HEAD/GET status check",
        "source_url": "https://paste.linuxiarz.pl/view/df40f1f1",
        "description": ("Workstream C3 live re-check (2026-09-28 ~11:35 UTC): "
                        "paste.linuxiarz.pl/view/df40f1f1 -> 404 (still pruned), "
                        "/view/raw/df40f1f1 -> 404, /api/recent -> 403 anonymous "
                        "(unchanged since lane G). Wayback availability endpoint "
                        "returned 429 (rate-limited); backed off per policy, no "
                        "retry storm. The 7 other relay IDs were deliberately "
                        "unenumerated by the source report; no new IDs surfaced. "
                        "Gap still open."),
        "tags": ["source:paste-linuxiarz", "cluster:iowacollab-relay",
                 "gap:still-open", "recovery-check"],
        "labels": {"annotated_by": "es_ingest_iowacollab",
                   "view_status": "404", "api_recent_status": "403",
                   "wayback_status": "429-rate-limited", "lane": "G",
                   "workstream": "C3"},
    }


def build_docs():
    docs = {}
    staged = load_staged_events()
    if not staged:
        raise SystemExit("ABORT: no relay_paste events in staged events.jsonl")
    created = None
    for txt_path in sorted(glob.glob(PDIR + "/raw/*.txt")):
        pid = os.path.basename(txt_path).replace(".txt", "")
        meta = staged.get(pid)
        if meta is None:
            print(f"note: raw/{pid}.txt has no staged event; skipping",
                  file=sys.stderr)
            continue
        body, digest, nbytes = read_verified_body(pid, meta.get("labels", {}))
        created = created or meta.get("event", {}).get("created")
        docs["paste:" + pid] = build_paste_doc(pid, meta, body, digest, nbytes)
    missing = sorted(set(staged) - {k.split(":", 1)[1] for k in docs})
    if missing:
        raise SystemExit(
            f"ABORT: staged events with no raw body: {missing}")
    # workstream C3 live re-check (2026-09-28): site still pruned, 7 IDs still unenumerated
    docs["recheck:2026-09-28"] = build_recheck_doc(created)
    return docs


def validate_docs(docs):
    errs = []
    for doc_id, doc in docs.items():
        for e in schema_check(doc, doc_id):
            errs.append(f"{doc_id}: {e}")
    return errs


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


def main():
    ap = argparse.ArgumentParser(
        description="Rebuild IowaCollab paste docs (dry-run by default).")
    ap.add_argument("--out", metavar="DIR",
                    help="dry-run: write docs.jsonl into DIR (no network)")
    ap.add_argument("--load", action="store_true",
                    help="bulk-load docs into Elastic (network + creds)")
    args = ap.parse_args()

    docs = build_docs()
    errs = validate_docs(docs)
    if errs:
        print("SCHEMA VALIDATION FAILED:")
        for e in errs:
            print("  " + e)
        raise SystemExit(1)
    print(f"docs built: {len(docs)} (schema-valid)")
    for doc_id, doc in docs.items():
        print(f"  {doc_id} kind={doc['record_kind']} "
              f"fp={doc['fingerprint'][:12]}… ts={doc['@timestamp']} "
              f"bytes={doc.get('size_bytes', '-')}")

    if args.out:
        os.makedirs(args.out, exist_ok=True)
        out_path = os.path.join(args.out, "docs.jsonl")
        with open(out_path, "w", encoding="utf-8") as f:
            for doc_id, doc in docs.items():
                f.write(json.dumps(doc, ensure_ascii=False,
                                   sort_keys=True) + "\n")
        print("wrote", out_path)
        return

    if args.load:
        ensure_index()
        ok, fail = bulk_load(docs)
        print("bulk ok:", ok, "fail:", fail)
        print("verified count in index:", verify())


if __name__ == "__main__":
    main()
