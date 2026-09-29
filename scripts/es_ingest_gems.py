#!/usr/bin/env python3
"""Bulk-ingest the gem IOC corpus into the hosted `rubygems-goimport-campaign` ES index.

Independent Diffend-sourced collection (May 11-12 2026 go-import meta-tag
injection campaign). NOT part of the SwarmTraces dataset (provenance
correction 2026-09-27).

Sources (all in the project data/ dir):
  - gem-ioc-log.jsonl   : download / extraction / diffend_harvest records
  - gem-ioc-hits.jsonl  : per-file + per-metadata IOC hits (record_kind := "hit")

One index, four record flavors (mirrors the hunt's one-index-flavors pattern).
Native field names throughout: fingerprint / matched_string / note
(the schema review killed the fictional ioc_fingerprint/ioc_value/evidence).

Conventions (schema review 2026-09-27, P0):
  - @timestamp = published_at, else the harvest-date fallback constant (never now)
  - canonical provenance URL = source_url on every flavor
  - status = "dead" for yanked burst gems (+ tags ["status:dead"], labels.gem.status)
  - labels is a flattened field for native extras

Idempotent: deterministic _id per doc, so re-runs overwrite rather than duplicate.
Diffend re-harvest duplicates in the log are deduped (last wins) before ingest.

Usage:
  python3 es_ingest_gems.py            # create index (if needed) + bulk load
  python3 es_ingest_gems.py --verify  # count + 3 sample docs only
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
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTS = ["agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud"]
CRED = "custom.elastic-cloud"
BASE = REPO_ROOT
INDEX = "2025-03-04-rubygems-goimport-campaign"
NOW = datetime.now(timezone.utc).isoformat()
FALLBACK_TS = "2026-09-27T00:00:00.000Z"  # harvest date; never "now"
OBSERVER = {"product": "diffend-gem-harvest", "vendor": "independent-research",
            "type": "script"}


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


def enrich_common(doc, gem, version, published_at, ts_source, status, dataset):
    """Shared ECS/provenance block for every flavor."""
    doc["@timestamp"] = published_at or FALLBACK_TS
    wave = wave_for(published_at)
    if wave:
        doc["wave"] = wave
    doc["event"] = {"dataset": dataset, "created": NOW}
    doc["observer"] = dict(OBSERVER)
    doc["package"] = gem
    doc["status"] = status
    doc["tags"] = ["status:%s" % status] + (["wave:%s" % wave] if wave else [])
    labels = {"gem.status": status}
    if ts_source:
        labels["gem.timestamp_source"] = ts_source
        labels["gem.date_precision"] = (
            "none" if ts_source == "fallback:missing_first_seen" else "day")
    doc["labels"] = labels
    return doc


def load_docs():
    docs = {}
    pub_lookup = {}     # (gem, version) -> published_at ISO
    src_lookup = {}     # (gem, version) -> canonical source_url
    status_lookup = {}  # (gem, version) -> dead|live

    def put(_id, doc):
        docs[_id] = doc

    with open(BASE + "/data/2025-03-04-rubygems-goimport-campaign/raw/gem-ioc-log.jsonl") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except ValueError:
                continue
            rk = r.get("record_kind", "?")
            gem, ver = r.get("gem"), r.get("version")
            if rk not in ("download", "extraction", "diffend_harvest"):
                continue

            doc = dict(r)  # native fields preserved verbatim
            # canonical source_url (keep download_url/diff_url as ingested aliases)
            if rk == "diffend_harvest":
                doc["source_url"] = r.get("diff_url")
                status = "dead"  # burst gems were yanked from rubygems.org
                # published_at backfill from this version's diff_ts
                ts_source = None
                for v in r.get("diffend_versions", []) or []:
                    if v.get("version") == ver and v.get("diff_ts"):
                        iso = parse_diff_ts(v["diff_ts"])
                        if iso:
                            doc["published_at"] = iso
                            ts_source = "diffend:diff_ts"
                        break
                if not doc.get("published_at"):
                    ts_source = ts_source or "fallback:missing_first_seen"
                # nested transform for diffend_versions
                nested = []
                for v in r.get("diffend_versions", []) or []:
                    raw = v.get("diff_ts")
                    nested.append({"version": v.get("version"),
                                   "diff_ts": parse_diff_ts(raw) if raw else None,
                                   "diff_ts_raw": raw})
                doc["diffend_versions"] = nested
                doc["retrieved_at"] = r.get("retrieved_at") or NOW
            elif rk == "download":
                doc["source_url"] = r.get("download_url")
                status = "live"
                ts_source = "log:published_at" if r.get("published_at") else None
            else:  # extraction
                status = None  # resolved via lookup below
                ts_source = None

            if gem and ver:
                if doc.get("published_at"):
                    pub_lookup[(gem, ver)] = doc["published_at"]
                if doc.get("source_url"):
                    src_lookup[(gem, ver)] = doc["source_url"]

            # extraction records inherit status/source from the harvest/download
            if rk == "extraction" and gem and ver:
                if not status:
                    status = status_lookup.get((gem, ver), "unknown")
                if not doc.get("source_url"):
                    doc["source_url"] = src_lookup.get((gem, ver))
                if not ts_source:
                    ts_source = ("log:published_at" if (gem, ver) in pub_lookup
                                 else "fallback:missing_first_seen")
            if gem and ver:
                status_lookup[(gem, ver)] = status

            enrich_common(doc, gem, ver, doc.get("published_at"), ts_source,
                          status, "2025-03-04-rubygems-goimport-campaign")
            put("log:%s:%s:%s" % (rk, gem, ver), doc)

    with open(BASE + "/data/2025-03-04-rubygems-goimport-campaign/raw/gem-ioc-hits.jsonl") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                h = json.loads(line)
            except ValueError:
                continue
            gem, ver = h.get("gem"), h.get("version")
            key = (gem, ver)
            status = status_lookup.get(key, "unknown")
            pub = pub_lookup.get(key)
            ts_source = ("diffend:diff_ts" if pub
                         else "fallback:missing_first_seen")
            doc = {
                "record_kind": "hit",
                "gem": gem, "version": ver,
                "file": h.get("file"),
                "fingerprint": h.get("fingerprint"),
                "matched_string": h.get("matched_string"),
                "line_no": h.get("line_no"),
                "confidence": h.get("confidence"),
                "scan_truncated": h.get("scan_truncated"),
                "note": h.get("note", ""),
                "source_url": src_lookup.get(key),
            }
            enrich_common(doc, gem, ver, pub, ts_source, status,
                          "rubygems-goimport-campaign.ioc")
            hid = "hit:%s:%s:%s:%s:%s:%s" % (
                gem, ver, h.get("fingerprint"),
                (h.get("file") or "").replace("/", "_"), h.get("line_no"),
                hashlib.sha256(str(h.get("matched_string", "")).encode()
                              ).hexdigest()[:16])
            put(hid, doc)

    # June-18 wave: Wayback-recovered metadata records (no .gem bytes exist).
    try:
        with open(BASE + "/data/2025-03-04-rubygems-goimport-campaign/raw/gem-june18-wayback.jsonl") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                gem, ver = r.get("gem"), r.get("version")
                doc = dict(r)  # native fields preserved verbatim
                doc["source_url"] = r.get("wayback_url")
                enrich_common(doc, gem, ver, r.get("published_at"),
                              r.get("date_source"), "dead",
                              "2025-03-04-rubygems-goimport-campaign")
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


def verify():
    c = req("GET", "/%s/_count" % INDEX)
    print("doc count:", c.get("count"))
    for rk in ("diffend_harvest", "extraction", "hit"):
        r = req("POST", "/%s/_search" % INDEX,
                {"size": 0, "query": {"term": {"record_kind": rk}}})
        print("  %-15s %d" % (rk, r["hits"]["total"]["value"]))
    s = req("POST", "/%s/_search" % INDEX,
            {"size": 3, "_source": ["record_kind", "gem", "version",
                                    "fingerprint", "@timestamp", "status"]})
    for h in s["hits"]["hits"]:
        print(json.dumps(h["_source"]))


def main():
    if "--verify" in sys.argv:
        verify()
        return
    ensure_index()
    docs = load_docs()
    print("docs to ingest (deduped):", len(docs))
    ok, fail = bulk_load(docs)
    print("ingest done: ok=%d fail=%d" % (ok, fail))
    verify()


if __name__ == "__main__":
    main()
