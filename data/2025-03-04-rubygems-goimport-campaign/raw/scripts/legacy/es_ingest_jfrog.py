#!/usr/bin/env python3
"""Ingest JFrog's public GemStuffer inventory CSV into the collection index.

record_kind := "jfrog_inventory".
Source: data/2025-03-04-rubygems-goimport-campaign/raw/gemstuffer-jfrog-2026-09-27.csv
(Package, Versions, Xray ID), saved from https://research.jfrog.com/gemstuffer.csv
on 2026-09-27.
Provenance: https://research.jfrog.com/post/gemstuffer-openai-rubygems/

Wave/date attribution: the CSV carries no per-row dates, so @timestamp and the
wave label are inherited from our dated Diffend harvest log
(raw/gem-ioc-log.jsonl, record_kind="diffend_harvest") wherever the package
overlaps. The 2026-09-28 schema backfill moved the harvest fields under
labels.* dotted keys -- gem name is now labels["gem.name"] and the publish
time is labels["published.at"] (ISO), falling back to
labels["diffend.versions.diff_ts"] (old "May 12, 2026 03:32" format) and then
the log row's @timestamp. Rows with no recoverable date at all use the CSV
acquisition date 2026-09-27T00:00:00Z with an explicit
labels["gem.timestamp_source"] -- never a silent "now".

Each doc embeds its source row in the schema's top-level `payloads` array
(schema/record.schema.json, commit 37988db -- `{kind, content_type, content,
encoding, truncated, byte_size, sha256}`; complements `file`, which points at
the full repo-local artifact):
  - inventory_row: the raw CSV line, embedded fully (rows are small)
  - wave_attribution: the derived date/wave/overlap attribution as text

Docs are schema-valid per schema/record.schema.json (dataset-specific fields
live in labels.*; fingerprint = sha256("jfrog_inventory|<gem>"), identity
string documented in PROVENANCE.md).

Idempotent: deterministic _id "jfrog:<package>", re-runs overwrite.

Usage:
  python3 es_ingest_jfrog.py                 # update mapping + bulk load (network)
  python3 es_ingest_jfrog.py --verify        # count + sample docs only (network)
  python3 es_ingest_jfrog.py --build [PATH]  # build docs to disk JSONL, validate,
                                             # no network
"""
import sys, json, csv, hashlib, urllib.request, re
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
INDEX = "2025-03-04-rubygems-goimport-campaign"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
CSV_RETRIEVAL_TS = "2026-09-27T00:00:00Z"  # gemstuffer.csv saved 2026-09-27; real, never "now"
CSV_REL_PATH = "data/2025-03-04-rubygems-goimport-campaign/raw/gemstuffer-jfrog-2026-09-27.csv"
CSV_PATH = os.path.join(BASE, CSV_REL_PATH)
LOG_PATH = os.path.join(SCRIPT_DIR, "raw", "gem-ioc-log.jsonl")
SCHEMA_PATH = os.path.join(BASE, "schema", "record.schema.json")
REPORT_URL = "https://research.jfrog.com/post/gemstuffer-openai-rubygems/"
CSV_URL = "https://research.jfrog.com/gemstuffer.csv"
SENTINEL = "1970-01-01T00:00:00Z"  # schema sentinel: no recoverable date
OBSERVER = {"product": "jfrog-inventory-ingest", "vendor": "independent-research",
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


def iso_z(ts):
    """Normalize an ISO-8601 timestamp to Z-suffixed form; None on failure."""
    if not ts:
        return None
    try:
        s = ts.strip().replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    except Exception:
        return None


def parse_diff_ts(ts):
    """Old Diffend 'May 12, 2026 03:32' format, kept as a fallback read."""
    try:
        return datetime.strptime(ts.strip(), "%b %d, %Y %H:%M").replace(
            tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
    except Exception:
        return None


def wave_for(published_at):
    if not published_at:
        return None
    d = published_at[:10]
    if d == "2026-07-07":
        return "july-7"   # third JFrog wave family (July 7, 215 pkgs)
    if d == "2026-06-18":
        return "june-18"
    if d in ("2026-05-26", "2026-05-27"):
        return "may-26"
    if d.startswith("2026-05-"):
        return "may-12"
    return None


def row_published_at(labels, row_ts):
    """Best-effort publish time for a diffend_harvest log row (backfill-aware).

    Returns (iso_ts, ts_source). Reads, in order:
      1. labels["published.at"] (ISO, promoted by the 2026-09-28 backfill)
      2. labels["diffend.versions.diff_ts"] entries (original Diffend format)
      3. the log row's own @timestamp (unless the 1970 sentinel)
    """
    iso = iso_z((labels or {}).get("published.at"))
    if iso:
        return iso, "diffend:published.at"
    for raw in (labels or {}).get("diffend.versions.diff_ts") or []:
        iso = parse_diff_ts(raw or "")
        if iso:
            return iso, "diffend:diff_ts (fallback; labels:published.at unset)"
    iso = iso_z(row_ts)
    if iso and iso != SENTINEL:
        return iso, "log:@timestamp"
    return None, None


def corpus_wave_lookup():
    """gem name -> (published_at ISO, wave, ts_source) from the dated Diffend
    harvest log. Reads the backfilled labels.* dotted keys; keeps the EARLIEST
    publish time per gem across harvest rows."""
    lookup = {}
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r.get("record_kind") != "diffend_harvest":
                continue
            labels = r.get("labels") or {}
            gem = (labels.get("gem.name") or "").strip()
            if not gem:
                continue
            iso, src = row_published_at(labels, r.get("@timestamp"))
            if not iso:
                continue
            if gem not in lookup or iso < lookup[gem][0]:
                lookup[gem] = (iso, wave_for(iso), src)
    return lookup


def parse_versions(raw):
    parts = [p.strip() for p in (raw or "").replace(";", ",").split(",")]
    return [p for p in parts if p]


def fingerprint_for(gem):
    # identity string "jfrog_inventory|<gem>" documented in PROVENANCE.md
    return hashlib.sha256(("jfrog_inventory|" + gem).encode()).hexdigest()


def csv_rows():
    """Yield (raw_line, row_dict) for each CSV data row; raw_line is the exact
    source bytes for payload embedding (CSV has no quoted commas)."""
    with open(CSV_PATH, newline="") as f:
        lines = f.read().splitlines()
    if not lines:
        return
    reader = csv.DictReader(lines)
    for i, row in enumerate(reader):
        yield lines[i + 1], row


def build_docs():
    lookup = corpus_wave_lookup()
    print("corpus wave lookup: %d gems" % len(lookup))
    docs = {}
    overlap = 0
    dated = 0
    for raw_line, row in csv_rows():
        gem = (row.get("Package") or "").strip()
        if not gem:
            continue
        versions = parse_versions(row.get("Versions"))
        xray = (row.get("Xray ID") or "").strip()
        in_corpus = gem in lookup
        if in_corpus:
            overlap += 1
            published_at, wave, ts_source = lookup[gem]
        else:
            published_at, wave = CSV_RETRIEVAL_TS, None
            ts_source = "dataset:csv_retrieval_date"
        if published_at != CSV_RETRIEVAL_TS:
            dated += 1
        labels = {
            "gem.name": gem,
            "gem.versions": versions,
            "gem.version_count": len(versions),
            "gem.xray_id": xray or "unknown",
            "gem.in_diffend_corpus": "true" if in_corpus else "false",
            "gem.timestamp_source": ts_source,
            "gem.status": "dead",
        }
        if wave:
            labels["gem.wave"] = wave
        payloads = [
            {"kind": "inventory_row", "content_type": "text/csv",
             "content": raw_line, "encoding": "text", "truncated": False,
             "byte_size": len(raw_line.encode()),
             "sha256": hashlib.sha256(raw_line.encode()).hexdigest()},
            {"kind": "wave_attribution", "content_type": "text/plain",
             "content":
                 "gem=%s; xray_id=%s; versions=%s; published_at=%s; wave=%s; "
                 "in_diffend_corpus=%s; timestamp_source=%s"
                 % (gem, xray or "unknown", ",".join(versions) or "none",
                    published_at, wave or "none",
                    "true" if in_corpus else "false", ts_source),
             "encoding": "text", "truncated": False},
        ]
        payloads[1]["byte_size"] = len(payloads[1]["content"].encode())
        payloads[1]["sha256"] = hashlib.sha256(
            payloads[1]["content"].encode()).hexdigest()
        doc = {
            "@timestamp": published_at,
            "event": {"dataset": INDEX, "created": NOW},
            "record_kind": "jfrog_inventory",
            "fingerprint": fingerprint_for(gem),
            "labels": labels,
            "payloads": payloads,
            "source_url": REPORT_URL,
            "file": CSV_REL_PATH,
            "retrieved_at": CSV_RETRIEVAL_TS,
            "description": "JFrog GemStuffer inventory: %s (%s)" % (
                gem, ", ".join(versions) or "no versions listed"),
            "status": "dead",
            "tags": ["status:dead", "source:jfrog",
                     "corpus:overlap" if in_corpus else "corpus:jfrog_only"]
                    + (["wave:%s" % wave] if wave else []),
            "observer": dict(OBSERVER),
            "note": "JFrog GemStuffer inventory row; wave/date inherited from "
                    "the dated Diffend corpus where the package overlaps, "
                    "else the CSV acquisition date (never 'now').",
        }
        docs["jfrog:%s" % gem] = doc
    print("jfrog rows: %d, overlap with our corpus: %d, real dated: %d" %
          (len(docs), overlap, dated))
    return docs


def validate_against_schema(docs):
    """Check built docs against schema/record.schema.json (required fields,
    closed top-level/event shapes, labels flatness + key pattern, fingerprint
    and @timestamp formats). Returns (ok_count, [errors])."""
    schema = json.load(open(SCHEMA_PATH))
    top_allowed = set(schema["properties"].keys())
    top_required = set(schema.get("required", []))
    ev_allowed = set(schema["properties"]["event"]["properties"].keys())
    ev_required = set(schema["properties"]["event"].get("required", []))
    pay_props = schema["properties"]["payloads"]
    pay_required = set(pay_props["items"]["required"])
    pay_allowed = set(pay_props["items"]["properties"].keys())
    label_key_re = re.compile(
        schema["properties"]["labels"]["propertyNames"]["pattern"])
    kind_re = re.compile(schema["properties"]["record_kind"]["pattern"])
    fp_re = re.compile(schema["properties"]["fingerprint"]["pattern"])
    errors = []
    ok = 0
    for _id, d in docs.items():
        errs = []
        missing = top_required - set(d.keys())
        if missing:
            errs.append("missing required: %s" % sorted(missing))
        extra = set(d.keys()) - top_allowed
        if extra:
            errs.append("top-level extra: %s" % sorted(extra))
        ev = d.get("event") or {}
        if set(ev.keys()) - ev_allowed:
            errs.append("event extra: %s" % sorted(set(ev.keys()) - ev_allowed))
        if ev_required - set(ev.keys()):
            errs.append("event missing: %s" % sorted(ev_required - set(ev.keys())))
        for p in d.get("payloads", []):
            if not isinstance(p, dict) or pay_required - set(p.keys()) or \
                    set(p.keys()) - pay_allowed:
                errs.append("bad payload entry: %r" % (p,))
                break
            if not all(isinstance(p[k], str)
                       for k in ("kind", "content_type", "content")):
                errs.append("bad payload entry types: %r" % (p,))
                break
        labels = d.get("labels") or {}
        if not labels:
            errs.append("labels empty")
        for k, v in labels.items():
            if not label_key_re.match(k):
                errs.append("bad label key: %r" % k)
                break
            if isinstance(v, list):
                if not v or not all(isinstance(x, (str, int, float, bool))
                                    for x in v):
                    errs.append("bad label array: %r" % k)
                    break
            elif not isinstance(v, (str, int, float, bool)):
                errs.append("bad label value: %r" % k)
                break
        if not kind_re.match(d.get("record_kind", "")):
            errs.append("bad record_kind")
        if not fp_re.match(d.get("fingerprint", "")):
            errs.append("bad fingerprint")
        if not iso_z(d.get("@timestamp")):
            errs.append("bad @timestamp: %r" % (d.get("@timestamp"),))
        if errs:
            errors.append((_id, errs))
        else:
            ok += 1
    return ok, errors


def update_mapping():
    mapping = json.load(open(BASE + "/notes/gems-es-mapping.json"))["mappings"]
    try:
        req("PUT", "/%s/_mapping" % INDEX, mapping)
        print("mapping updated on live index")
    except Exception as e:
        body = e.read().decode() if hasattr(e, "read") else str(e)
        print("mapping PUT failed:", body[:300])
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
    r = req("POST", "/%s/_search" % INDEX,
            {"size": 0, "query": {"term": {"record_kind": "jfrog_inventory"}}})
    print("  jfrog_inventory:", r["hits"]["total"]["value"])
    r = req("POST", "/%s/_search" % INDEX,
            {"size": 0, "query": {"term": {"labels.gem.in_diffend_corpus": "true"}}})
    print("  overlap (labels.gem.in_diffend_corpus=true):", r["hits"]["total"]["value"])
    s = req("POST", "/%s/_search" % INDEX,
            {"size": 3, "_source": ["record_kind", "labels.gem.name",
                                    "labels.gem.versions", "labels.gem.xray_id",
                                    "labels.gem.wave",
                                    "labels.gem.in_diffend_corpus",
                                    "@timestamp", "event.payloads"],
             "query": {"term": {"record_kind": "jfrog_inventory"}}})
    for h in s["hits"]["hits"]:
        print(json.dumps(h["_source"]))


def main():
    if "--verify" in sys.argv:
        verify()
        return
    if "--build" in sys.argv:
        i = sys.argv.index("--build")
        out = sys.argv[i + 1] if i + 1 < len(sys.argv) and \
            not sys.argv[i + 1].startswith("-") else "/tmp/jfrog_inventory_build.jsonl"
        docs = build_docs()
        with open(out, "w") as f:
            for _id, doc in docs.items():
                f.write(json.dumps({"_id": _id, "_doc": doc}) + "\n")
        ok, errors = validate_against_schema(docs)
        print("schema validation: %d/%d ok" % (ok, len(docs)))
        for _id, errs in errors[:10]:
            print("INVALID %s: %s" % (_id, errs))
        if errors:
            sys.exit(1)
        print("build written to %s (no Elastic writes)" % out)
        return
    update_mapping()
    docs = build_docs()
    ok, fail = bulk_load(docs)
    print("ingest done: ok=%d fail=%d" % (ok, fail))
    verify()


if __name__ == "__main__":
    main()
