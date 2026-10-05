#!/usr/bin/env python3
"""Bulk-ingest the gem IOC corpus into the `2025-03-04-rubygems-goimport-campaign` ES index.

Independent Diffend-sourced collection (May 11-12 2026 go-import meta-tag
injection campaign). NOT part of the SwarmTraces dataset (provenance
correction 2026-09-27).

Sources (all in this collection's raw/ dir):
  - gem-ioc-log.jsonl      : download / extraction / diffend_harvest records
                             (2026-09-28 schema backfill: gem fields now live
                             under labels.* dotted keys, e.g. labels["gem.name"])
  - gem-ioc-hits.jsonl     : per-file + per-metadata IOC hits (NOT backfilled;
                             still flat: gem/version/file/fingerprint/...)
  - gem-june18-wayback.jsonl : Wayback-recovered metadata (flat; no .gem bytes)

Record flavors (aligned with the collection's canonical events.jsonl,
built 2026-09-29 by the normalization worker):
  download / extraction / diffend_harvest / corpus_hit / wayback_capture.

Native field names throughout. Dataset-specific extras live in `labels`
(flattened, dotted keys) per schema/record.schema.json; every emitted doc
passes scripts/validate_schema.py.

REPAIR 2026-09-29 (schema-backfill breakage): the pre-repair script read
r["gem"], r["version"], r["published_at"], r["download_url"], r["diff_url"],
r["diffend_versions"] at top level. After the 2026-09-28 backfill those
live at labels["gem.name"], labels["gem.version"], labels["published.at"],
top-level source_url, labels["diff_url"], and the parallel arrays
labels["diffend.versions.version"] / labels["diffend.versions.diff_ts"].
It also (a) overwrote the backfilled labels dict in enrich_common, wiping
gem.name etc., and (b) emitted non-schema top-level fields (package, wave,
published_at, diffend_versions) plus the raw IOC family name as
doc["fingerprint"] for hits (fails the 64-hex fingerprint rule).
All fixed: labels are merged, never replaced; extras move into labels;
hit docs get a computed 64-hex fingerprint (sha256 of the W3 identity
string) with the IOC family name kept at labels["hit.ioc_family"].

PAYLOAD NOTE (2026-09-29, schema commit 37988db): per-item payload material is
embedded in the OPTIONAL top-level `payloads` array (NOT event.payloads --
`event` has additionalProperties:false). Item shape:
{kind, content_type, content, encoding, truncated, byte_size, sha256}.
Each doc carries one payload: the byte-exact raw source record
(kind gem_ioc_log_entry / gem_ioc_hit / wayback_metadata_record,
content_type application/json, encoding text). Truncation cap is 64 KiB
(PAYLOAD_TRUNCATE_AT); no current row exceeds ~11 KiB, so every payload
here is full (truncated=false) with byte_size/sha256 of the body.
Larger artifacts are NOT duplicated: the extracted gem trees at
data/processed/gems/<name>-<version>/ are skeletal Diffend reconstructions
(1-byte placeholder gemspecs, tiny lib stubs) whose manifests already live
in labels files.path/size/sha256 -- the tree path is kept as the file
pointer (top-level `file` on extraction docs, labels["extracted.to"]
everywhere). .gem binaries (3 control downloads) and June-18 Wayback HTML
were never archived in this repo; source_url is the file pointer.

Idempotent: deterministic _id per doc, so re-runs overwrite rather than duplicate.
Diffend re-harvest duplicates in the log are deduped (last wins) before ingest.

Usage:
  python3 es_ingest_gems.py --emit /tmp/gems-docs.jsonl   # dry run to disk (no network)
  python3 es_ingest_gems.py                               # create index (if needed) + bulk load
  python3 es_ingest_gems.py --verify                      # count + sample docs only
"""
import sys, json, hashlib, urllib.request
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
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = REPO_ROOT
INDEX = "2025-03-04-rubygems-goimport-campaign"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
FALLBACK_TS = "2026-09-27T00:00:00.000Z"  # harvest date; never "now"
OBSERVER = {"product": "diffend-gem-harvest", "vendor": "independent-research",
            "type": "script"}
RAW = os.path.join(SCRIPT_DIR, "raw")
PAYLOAD_TRUNCATE_AT = 65536  # 64 KiB; no current source row exceeds ~11 KiB


def mk_payload(kind, text):
    """Build one top-level payloads[] item from a source-record string.

    Embeds the full body; truncates at PAYLOAD_TRUNCATE_AT with
    truncated=true. byte_size/sha256 always describe the FULL untruncated
    body (schema/record.schema.json, commit 37988db).
    """
    body = text.encode("utf-8")
    full_len = len(body)
    full_sha = hashlib.sha256(body).hexdigest()
    if full_len > PAYLOAD_TRUNCATE_AT:
        content = body[:PAYLOAD_TRUNCATE_AT].decode("utf-8", "replace")
        truncated = True
    else:
        content = text
        truncated = False
    return {"kind": kind,
            "content_type": "application/json",
            "content": content,
            "encoding": "text",
            "truncated": truncated,
            "byte_size": full_len,
            "sha256": full_sha}


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
    with urllib.request.urlopen(r, timeout=120) as resp:
        return read_json_response(resp)


def parse_diff_ts(ts):
    """'May 12, 2026 07:56' -> UTC ISO, or None."""
    try:
        return datetime.strptime(ts.strip(), "%b %d, %Y %H:%M").replace(
            tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
    except Exception:
        return None


def wave_for(published_at):
    """Campaign wave label from a published_at ISO date."""
    if not published_at:
        return None
    d = published_at[:10]
    if d == "2026-06-18":
        return "june-18"
    if d in ("2026-05-26", "2026-05-27"):
        return "may-26"
    if d.startswith("2026-05-"):
        return "may-12"
    return None


def sha64(s):
    return hashlib.sha256(s.encode()).hexdigest()


def enrich_common(doc, gem, ver, published_at, ts_source, status):
    """Shared ECS/provenance block for every flavor.

    Schema-valid only: extras go into labels (merged with, never replacing,
    the native backfilled labels). The old top-level `package` / `wave` /
    `published_at` fields were dropped (not in schema/record.schema.json).
    """
    doc["@timestamp"] = doc.get("@timestamp") or published_at or FALLBACK_TS
    doc["event"] = {"dataset": INDEX, "created": NOW}
    doc["observer"] = dict(OBSERVER)
    doc["status"] = status
    labels = doc.get("labels")
    if not isinstance(labels, dict):
        labels = {}
    labels.setdefault("gem.name", gem)
    labels.setdefault("gem.version", ver)
    labels["gem.status"] = status
    wave = wave_for(published_at)
    if wave:
        labels["wave"] = wave
    if ts_source:
        labels.setdefault("timestamp_source", ts_source)
        labels["gem.timestamp_source"] = ts_source
        labels.setdefault("gem.date_precision",
                           "none" if ts_source == "fallback:missing_first_seen" else "day")
    doc["labels"] = labels
    doc["tags"] = ["status:%s" % status] + (["wave:%s" % wave] if wave else [])
    return doc


def load_docs():
    docs = {}
    pub_lookup = {}     # (gem, version) -> published_at ISO
    src_lookup = {}     # (gem, version) -> canonical source_url
    status_lookup = {}  # (gem, version) -> dead|live

    def put(_id, doc):
        docs[_id] = doc

    def iter_jsonl(name):
        with open(os.path.join(RAW, name)) as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    yield stripped, json.loads(stripped)
                except ValueError:
                    continue

    for line, r in iter_jsonl("gem-ioc-log.jsonl"):
        rk = r.get("record_kind", "?")
        if rk not in ("download", "extraction", "diffend_harvest"):
            continue
        # --- post-backfill key map (2026-09-28): raw fields now under labels.* ---
        lab_in = r.get("labels") if isinstance(r.get("labels"), dict) else {}
        gem, ver = lab_in.get("gem.name"), lab_in.get("gem.version")
        published_at = lab_in.get("published.at")

        doc = {"record_kind": rk,
               "fingerprint": r.get("fingerprint"),
               "labels": dict(lab_in)}  # native backfilled labels kept verbatim
        for k in ("retrieved_at", "retrieved_via", "sha256", "size_bytes",
                  "note", "@timestamp"):
            if r.get(k) is not None:
                doc[k] = r[k]

        if rk == "diffend_harvest":
            if lab_in.get("diff_url"):
                doc["source_url"] = lab_in["diff_url"]
            status = "dead"  # burst gems were yanked from rubygems.org
            ts_source = (lab_in.get("published.at_source")
                         or lab_in.get("timestamp_source"))
            if not published_at:
                # fall back to parsing the raw diff_ts strings
                versions = lab_in.get("diffend.versions.version") or []
                diff_tss = lab_in.get("diffend.versions.diff_ts") or []
                for v, raw_ts in zip(versions, diff_tss):
                    if v == ver and raw_ts:
                        iso = parse_diff_ts(raw_ts)
                        if iso:
                            published_at = iso
                            doc["labels"]["published.at"] = iso
                            ts_source = "diffend:diff_ts"
                        break
            if not ts_source:
                ts_source = "fallback:missing_first_seen"
        elif rk == "download":
            doc["source_url"] = r.get("source_url")  # canonical, backfilled
            status = "live"
            ts_source = (lab_in.get("timestamp_source")
                         or ("log:published_at" if published_at else None))
        else:  # extraction
            status = None  # resolved via lookup below
            ts_source = lab_in.get("timestamp_source")

        if gem and ver:
            if published_at:
                pub_lookup[(gem, ver)] = published_at
            if doc.get("source_url"):
                src_lookup[(gem, ver)] = doc["source_url"]

        # extraction records inherit status/source from the harvest/download
        if rk == "extraction" and gem and ver:
            if not status:
                status = status_lookup.get((gem, ver), "unknown")
            if not doc.get("source_url") and src_lookup.get((gem, ver)):
                doc["source_url"] = src_lookup[(gem, ver)]
            if not ts_source:
                ts_source = ("log:published_at" if (gem, ver) in pub_lookup
                             else "fallback:missing_first_seen")
            # file pointer to the full extracted tree (repo-relative)
            tree = (doc["labels"].get("extracted.to") or "").lstrip("./")
            if tree:
                doc["file"] = tree
        if gem and ver:
            status_lookup[(gem, ver)] = status

        enrich_common(doc, gem, ver, published_at, ts_source, status)
        doc["payloads"] = [mk_payload("gem_ioc_log_entry", line)]
        put("log:%s:%s:%s" % (rk, gem, ver), doc)

    for line, h in iter_jsonl("gem-ioc-hits.jsonl"):
        # NOTE: hits file was NOT backfilled -- still the flat native format.
        # Its "fingerprint" is the IOC family name, not a doc fingerprint.
        gem, ver = h.get("gem"), h.get("version")
        key = (gem, ver)
        status = status_lookup.get(key, "unknown")
        pub = pub_lookup.get(key)
        ioc_family = h.get("fingerprint")
        doc = {
            "record_kind": "corpus_hit",
            "fingerprint": sha64("gem-ioc-hit:%s@%s:%s:%s:%s" % (
                gem, ver, ioc_family, h.get("line_no"),
                h.get("matched_string", ""))),
            "file": h.get("file"),
            "matched_string": h.get("matched_string"),
            "confidence": h.get("confidence"),
            "description": "IOC hit [%s] in %s==%s (%s, line %s)" % (
                ioc_family, gem, ver, h.get("file"), h.get("line_no")),
            "labels": {
                "gem.name": gem,
                "gem.version": ver,
                "hit.file": h.get("file"),
                "hit.ioc_family": ioc_family,
                "hit.line_no": h.get("line_no"),
                "hit.scan_truncated": h.get("scan_truncated"),
            },
        }
        ts_source = ("diffend:diff_ts" if pub
                     else "fallback:missing_first_seen")
        if h.get("note") is not None:
            doc["note"] = h["note"]
        if src_lookup.get(key):
            doc["source_url"] = src_lookup[key]
        enrich_common(doc, gem, ver, pub, ts_source, status)
        doc["payloads"] = [mk_payload("gem_ioc_hit", line)]
        hid = "hit:%s:%s:%s:%s:%s:%s" % (
            gem, ver, ioc_family,
            (h.get("file") or "").replace("/", "_"), h.get("line_no"),
            sha64(str(h.get("matched_string", "")))[:16])
        put(hid, doc)

    # June-18 wave: Wayback-recovered metadata records (no .gem bytes exist).
    try:
        for line, r in iter_jsonl("gem-june18-wayback.jsonl"):
            gem, ver = r.get("gem"), r.get("version")
            doc = {
                "record_kind": "wayback_capture",
                "fingerprint": sha64("gem-wayback:%s@%s" % (gem, ver)),
                "labels": {
                    "gem.name": gem,
                    "gem.version": ver,
                    "wave": r.get("wave") or "june-18",
                    "published.at": r.get("published_at"),
                    "published.at_source": r.get("date_source"),
                    "wayback.snapshot_ts": r.get("snapshot_ts"),
                    "wayback.recovery_status": r.get("recovery_status"),
                    "wayback.embedded_key_count": r.get("embedded_key_count"),
                    "wayback.total_downloads": r.get("total_downloads"),
                },
            }
            # drop None-valued optionals (schema types are strict)
            doc["labels"] = {k: v for k, v in doc["labels"].items()
                             if v is not None}
            if r.get("wayback_url"):
                doc["source_url"] = r["wayback_url"]
            if r.get("description"):
                doc["description"] = r["description"]
            if r.get("note"):
                doc["note"] = r["note"]
            if r.get("external_links"):
                doc["labels"]["wayback.external_links"] = r["external_links"]
            if r.get("embedded_key_prefixes"):
                doc["labels"]["wayback.embedded_key_prefixes"] = (
                    r["embedded_key_prefixes"])
            enrich_common(doc, gem, ver, r.get("published_at"),
                          r.get("date_source"), "dead")
            doc["payloads"] = [mk_payload("wayback_metadata_record", line)]
            put("wayback:%s:%s" % (gem, ver or "noversion"), doc)
    except FileNotFoundError:
        pass
    return docs


def ensure_index():
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
    try:
        req("PUT", "/" + INDEX, {"mappings": mapping})
        print("index created:", INDEX)
    except Exception as e:
        body = ""
        try:
            body = e.read().decode() if hasattr(e, "read") else str(e)
        except Exception:
            body = str(e)
        if "resource_already_exists_exception" in body or "resource_already_exists_exception" in str(e):
            print("index already exists:", INDEX)
        else:
            print("PUT index failed:", body[:300])
            raise


def bulk_load(docs):
    items = list(docs.items())
    total_ok, total_fail = 0, 0
    for i in range(0, len(items), 400):
        chunk = items[i:i + 400]
        nd = "".join(
            json.dumps({"index": {"_index": INDEX, "_id": _id}}) + "\n" +
            json.dumps(doc) + "\n" for _id, doc in chunk)
        res = req("POST", "/_bulk", raw=nd)
        for it in res.get("items", []):
            st = it.get("index", {}).get("status", 0)
            if st in (200, 201):
                total_ok += 1
            else:
                total_fail += 1
                print("BULK FAIL:", json.dumps(it)[:200])
        print("bulk progress: %d/%d ok=%d fail=%d" %
              (i + len(chunk), len(items), total_ok, total_fail))
    return total_ok, total_fail


def emit(path):
    """Dry run: build docs and write them to disk. No network, no ES."""
    docs = load_docs()
    with open(path, "w") as f:
        for _id, doc in docs.items():
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")
    print("wrote %d docs to %s" % (len(docs), path))


def verify():
    c = req("GET", "/%s/_count" % INDEX)
    print("doc count:", c.get("count"))
    for rk in ("diffend_harvest", "extraction", "corpus_hit", "wayback_capture"):
        r = req("POST", "/%s/_search" % INDEX,
                {"size": 0, "query": {"term": {"record_kind": rk}}})
        print("  %-15s %d" % (rk, r["hits"]["total"]["value"]))
    s = req("POST", "/%s/_search" % INDEX,
            {"size": 3, "_source": ["record_kind", "fingerprint",
                                    "@timestamp", "status"]})
    for h in s["hits"]["hits"]:
        print(json.dumps(h["_source"]))


def main():
    if "--verify" in sys.argv:
        verify()
        return
    if "--emit" in sys.argv:
        i = sys.argv.index("--emit")
        emit(sys.argv[i + 1] if i + 1 < len(sys.argv) else "/tmp/gems-docs.jsonl")
        return
    ensure_index()
    docs = load_docs()
    print("docs to ingest (deduped):", len(docs))
    ok, fail = bulk_load(docs)
    print("ingest done: ok=%d fail=%d" % (ok, fail))
    verify()


if __name__ == "__main__":
    main()
