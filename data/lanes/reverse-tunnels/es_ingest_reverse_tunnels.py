#!/usr/bin/env python3
"""Build the reverse-tunnels collection's canonical event stream from raw/.

Reads the lane-C raw captures (2026-09-28) and (re)builds the
schema-conformant `events.jsonl` (107 rows) + `rollup.jsonl` (6 rows) for
collection `2026-06-17-reverse-tunnels`, faithfully reproducing the
2026-09-29 normalization (fingerprint identity strings unchanged).

Repair 2026-09-29:
  - Repointed from the pre-rename dir `data/2016-05-06-reverse-tunnels`
    (the old date label was wrong; min @timestamp is 2026-06-17T07:52:49Z).
    Collection dir is resolved dynamically via the `*-reverse-tunnels` slug
    glob, so the next rename does not break the build.
  - Co-located with the collection (single-collection build-script
    convention, schema/collections.md); listed in the collection's
    PROVENANCE.md and covered by its SHA256SUMS.
  - Reads are against the post-backfill layout (raw inputs consumed
    directly; dataset-specific fields land under `labels.*`, flat dotted
    keys per the ECS labels rule).
  - Per-item payload material is embedded in the top-level `payloads`
    array (schema/record.schema.json, commit 37988db): each item is
    {kind, content_type, content, encoding, truncated, byte_size, sha256}
    with content capped at PAYLOAD_TEXT_CAP chars (byte_size/sha256
    describe the full untruncated body), plus a top-level `file` pointer
    to the full raw artifact. See the PROVENANCE.md repair note.

Pure build: no network, no Elastic writes. Loading is generic via
`scripts/push_to_local_es.py` auto-discovery of events.jsonl/rollup.jsonl.

Usage:
  python3 es_ingest_reverse_tunnels.py                  # dry-run: build in memory, print counts
  python3 es_ingest_reverse_tunnels.py --out-dir /tmp/x # write events.jsonl/rollup.jsonl to DIR
  python3 es_ingest_reverse_tunnels.py --build-events   # overwrite the collection's own files
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))


def resolve_collection_dir():
    """Dynamic slug-glob resolution: survive the next rename."""
    base = os.path.basename(SCRIPT_DIR)
    if base.endswith("-reverse-tunnels") and os.path.isdir(SCRIPT_DIR):
        return SCRIPT_DIR
    cands = sorted(glob.glob(os.path.join(REPO_ROOT, "data", "*-reverse-tunnels")))
    if not cands:
        sys.exit("no data/*-reverse-tunnels collection dir found under " + REPO_ROOT)
    return cands[-1]


DIR = resolve_collection_dir()
RAW = os.path.join(DIR, "raw")
SLUG = os.path.basename(DIR)
INDEX = SLUG
ROLLUP_INDEX = SLUG + "-rollup"
LANE_DATE = "2026-09-28"
LANE_TS = LANE_DATE + "T00:00:00Z"
OBSERVER = {"product": "muse", "type": "research-agent", "vendor": "meta"}
RETRIEVED_VIA = "urlquery public API (read-only GET)"

PAYLOAD_TEXT_CAP = 4000  # chars; full bytes stay in raw/, reachable via `file`
EXCLUDED_NAMES = ("myxworm", "petisse", "inohm-sh",
                  "serviceupdatevalidator", "webmailadminhelpdesk")


def fp(identity):
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def base_doc(record_kind, ts, dataset=INDEX):
    return {
        "@timestamp": ts,
        "event": {"dataset": dataset,
                  "created": datetime.now(timezone.utc).isoformat()},
        "record_kind": record_kind,
        "observer": dict(OBSERVER),
    }


def rel(path):
    """Repo-root-relative file pointer for the `file` field."""
    return os.path.relpath(path, REPO_ROOT)


def payload_item(kind, content_type, text):
    """One top-level `payloads` item per the schema: {kind, content_type,
    content, encoding, truncated, byte_size, sha256}.

    `text` is the per-item material (scan log, tunnel record, report JSON).
    Content is capped at PAYLOAD_TEXT_CAP chars; `truncated` marks the cut
    and `byte_size`/`sha256` describe the full untruncated body. The full
    artifact is reachable via the record's top-level `file` pointer.
    """
    raw = text if isinstance(text, bytes) else text.encode("utf-8")
    truncated = len(raw) > PAYLOAD_TEXT_CAP
    head = raw[:PAYLOAD_TEXT_CAP].decode("utf-8", "replace")
    return {
        "kind": kind,
        "content_type": content_type,
        "content": head,
        "encoding": "text",
        "truncated": truncated,
        "byte_size": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def get(d, *path, default=None):
    for k in path:
        if not isinstance(d, dict):
            return default
        d = d.get(k)
        if d is None:
            return default
    return d


def report_labels(query_or_fetch, r):
    """Shared urlquery-report label block (keyword hits + overviews)."""
    lab = {}
    if query_or_fetch[0] == "query":
        lab["uq.query"] = query_or_fetch[1]
    else:
        lab["uq.fetch"] = query_or_fetch[1]
    lab["uq.report_id"] = r["report_id"]
    lab["uq.date"] = r["date"]
    lab["uq.submitted_url"] = get(r, "url", "addr")
    lab["uq.fqdn"] = get(r, "url", "fqdn")
    lab["uq.target_ip"] = get(r, "ip", "addr")
    asn = get(r, "ip", "asn")
    if asn is not None:
        lab["uq.target_asn"] = asn
    as_org = get(r, "ip", "as")
    if as_org is not None:
        lab["uq.target_as_org"] = as_org
    cc = get(r, "ip", "country_code")
    if cc is not None:
        lab["uq.target_country"] = cc
    lab["uq.tags"] = r.get("tags") or []
    if query_or_fetch[0] == "query":
        # canonical normalization carries candidate_excluded on keyword
        # reports only (absent on the single-report overview fetches)
        fqdn = lab["uq.fqdn"] or ""
        lab["uq.candidate_excluded"] = any(n in fqdn for n in EXCLUDED_NAMES)
    lab["timestamp_source"] = "labels:uq.date"
    return lab


def build_events():
    events = []

    # 1. corpus rows -> corpus_hit (29)
    corpus_path = os.path.join(RAW, "corpus_tunnel_records.json")
    corpus = json.load(open(corpus_path))
    for e in corpus:
        doc = base_doc("corpus_hit", e["time"])
        doc["fingerprint"] = fp("%s|%s|%s|%s" % (
            e["time"], e["label"], e["page_id"], ",".join(e["tunnels"])))
        doc["labels"] = {
            "tunnel.label": e["label"],
            "tunnel.page_id": e["page_id"],
            "tunnel.urls": e["tunnels"],
            "record.time": e["time"],
            "timestamp_source": "labels:record.time",
        }
        doc["payloads"] = [payload_item(
            "tunnel-record", "application/json", json.dumps(e, indent=1))]
        doc["file"] = rel(corpus_path)
        doc["description"] = ("corpus revision carrying tunnel URL(s): " +
                              ", ".join(e["tunnels"]))
        events.append(doc)

    # 2. hostname candidates -> tunnel_candidate (12)
    hosts_path = os.path.join(RAW, "tunnel_hostnames.json")
    hosts = json.load(open(hosts_path))["hostnames"]
    for h in hosts:
        doc = base_doc("tunnel_candidate", h["first_seen_utc"])
        doc["fingerprint"] = fp(h["hostname"])
        doc["labels"] = {
            "tunnel.hostname": h["hostname"],
            "tunnel.provider": h["provider"],
            "tunnel.embedded_ip": h["embedded_ip"],
            "tunnel.classification": h["classification"],
            "tunnel.label": h["label"],
            "tunnel.pages": h["pages"],
            "tunnel.evidence": h["evidence"],
            "tunnel.first_seen": h["first_seen_utc"],
            "timestamp_source": "labels:tunnel.first_seen",
        }
        doc["payloads"] = [payload_item(
            "tunnel-candidate", "application/json", json.dumps(h, indent=1))]
        doc["file"] = rel(hosts_path)
        doc["description"] = ("tunnel hostname candidate (%s): %s" %
                              (h["classification"], h["hostname"]))
        events.append(doc)

    # 3. urlquery keyword responses -> per-report corpus_hit / zero-hit negative
    uq_files = sorted(
        f for f in glob.glob(os.path.join(RAW, "uq_*.json"))
        if "overview" not in f and "summary" not in f)
    for qf in uq_files:
        q = json.load(open(qf))
        query, reps = q["query"], q.get("reports") or []
        if not reps:
            doc = base_doc("corpus_grep_negative", LANE_TS)
            doc["fingerprint"] = fp("urlquery:" + query)
            doc["labels"] = {
                "uq.query": query,
                "uq.total_hits": q.get("total_hits", 0),
                "lane.date": LANE_DATE,
                "timestamp_source": "labels:lane.date",
            }
            doc["payloads"] = [payload_item(
                "urlquery-query-response", "application/json",
                json.dumps(q, indent=1))]
            doc["file"] = rel(qf)
            doc["matched_string"] = query
            doc["description"] = "urlquery keyword '%s': 0 hits" % query
            events.append(doc)
            continue
        for r in reps:
            doc = base_doc("corpus_hit", r["date"])
            doc["fingerprint"] = fp("urlquery:%s:%s" % (query, r["report_id"]))
            doc["labels"] = report_labels(("query", query), r)
            doc["payloads"] = [payload_item(
                "urlquery-report", "application/json",
                json.dumps(r, indent=1))]
            doc["file"] = rel(qf)
            doc["source_url"] = "https://urlquery.net/report/" + r["report_id"]
            doc["retrieved_via"] = RETRIEVED_VIA
            doc["description"] = ("urlquery hit for '%s': %s" %
                                  (query, doc["labels"]["uq.fqdn"]))[:96]
            events.append(doc)

    # 4. single-report overview fetches -> corpus_hit (2)
    for ovf in sorted(glob.glob(os.path.join(RAW, "uq_overview_*.json"))):
        r = json.load(open(ovf))
        doc = base_doc("corpus_hit", r["date"])
        doc["fingerprint"] = fp("urlquery:overview:" + r["report_id"])
        doc["labels"] = report_labels(("fetch", "report_overview"), r)
        doc["payloads"] = [payload_item(
            "urlquery-report-overview", "application/json",
            json.dumps(r, indent=1))]
        doc["file"] = rel(ovf)
        doc["source_url"] = "https://urlquery.net/report/" + r["report_id"]
        doc["retrieved_via"] = RETRIEVED_VIA
        doc["description"] = ("urlquery single-report overview: " +
                              doc["labels"]["uq.fqdn"])[:96]
        events.append(doc)

    # 5. HTMX 204s -> sweep_negative (7); bodies are 0-byte 204s, nothing to embed
    htmx_path = os.path.join(RAW, "htmx_summary.json")
    htmx = json.load(open(htmx_path))
    for key, blk in htmx.items():
        doc = base_doc("sweep_negative", LANE_TS)
        doc["fingerprint"] = fp("htmx_read_path:" + key)
        doc["labels"] = {
            "htmx.query": blk["query"],
            "htmx.http_status": blk["http_status"],
            "htmx.html_bytes": blk["html_bytes"],
            "lane.date": LANE_DATE,
            "timestamp_source": "labels:lane.date",
        }
        doc["file"] = rel(htmx_path)
        doc["description"] = ("urlquery HTMX read path for '%s': HTTP %d "
                              "(endpoint non-functional)" %
                              (blk["query"], blk["http_status"]))
        events.append(doc)

    # 6. DNS scan logs -> dns_probe (2); full text embedded (small files)
    for fn in sorted(os.listdir(RAW)):
        if not (fn.startswith("dns_") and fn.endswith(".txt")):
            continue
        path = os.path.join(RAW, fn)
        text = open(path).read()
        m = re.search(r"(\d{8}T\d{6})Z", fn)
        at = ("%s-%s-%sT%s:%s:%sZ" % (m.group(1)[:4], m.group(1)[4:6],
                                      m.group(1)[6:8], m.group(1)[9:11],
                                      m.group(1)[11:13], m.group(1)[13:15]))
        kind = "authoritative" if "auth" in fn else "resolution"
        hosts_list = [ln[3:].strip() for ln in text.splitlines()
                      if ln.startswith("== ")]
        doc = base_doc("dns_probe", at)
        doc["fingerprint"] = fp("dns:" + fn)
        doc["labels"] = {
            "probe.at": at,
            "probe.kind": kind,
            "probe.hosts": hosts_list,
            "probe.result": ("inconclusive: VM resolver sinkholes every query; "
                             "direct UDP/53 silent"),
            "timestamp_source": "labels:probe.at",
        }
        doc["payloads"] = [payload_item(
            "dns-scan-log", "text/plain", text)]
        doc["file"] = rel(path)
        doc["description"] = ("DNS %s check (%d names/zones); "
                              "no tunnel connections made" %
                              (kind, len(hosts_list)))
        events.append(doc)

    return events


def build_rollup():
    rows = []
    uq_files = sorted(
        f for f in glob.glob(os.path.join(RAW, "uq_*.json"))
        if "overview" not in f and "summary" not in f)
    for qf in uq_files:
        q = json.load(open(qf))
        query, reps = q["query"], q.get("reports") or []
        doc = base_doc("urlquery_rollup", LANE_TS, dataset=ROLLUP_INDEX)
        doc["fingerprint"] = fp("urlquery_rollup:" + query)
        doc["labels"] = {
            "uq.query": query,
            "uq.total_hits": q.get("total_hits", 0),
            "uq.reports_retrieved": len(reps),
            "lane.date": LANE_DATE,
            "timestamp_source": "labels:lane.date",
        }
        doc["file"] = rel(qf)
        doc["description"] = ("urlquery rollup '%s': %d total hits, "
                              "%d reports retrieved" %
                              (query, q.get("total_hits", 0), len(reps)))
        rows.append(doc)
    return rows


def write_jsonl(path, docs):
    with open(path, "w") as fh:
        for d in docs:
            fh.write(json.dumps(d, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=None,
                    help="write events.jsonl/rollup.jsonl to DIR (dry-run to disk)")
    ap.add_argument("--build-events", action="store_true",
                    help="overwrite the collection's own events.jsonl/rollup.jsonl")
    args = ap.parse_args()

    events = build_events()
    rollup = build_rollup()
    print("collection dir:", DIR)
    print("events built:", len(events), "| rollup built:", len(rollup))

    out = args.out_dir
    if args.build_events:
        out = DIR
    if out:
        os.makedirs(out, exist_ok=True)
        write_jsonl(os.path.join(out, "events.jsonl"), events)
        write_jsonl(os.path.join(out, "rollup.jsonl"), rollup)
        print("wrote:", os.path.join(out, "events.jsonl"),
              os.path.join(out, "rollup.jsonl"))


if __name__ == "__main__":
    main()
