#!/usr/bin/env python3
"""Build events.jsonl for data/2022-12-30-dse-wiki-verification.

Worker W3, 2026-09-29. Usage: python3 temp/build_events_w3_dse_wiki.py <repo_root>
Repo root is passed as argv[1] (never a hardcoded path).

Inputs (all under data/2022-12-30-dse-wiki-verification/raw/):
  reports/<uuid>.json          - 6 urlquery report JSONs cited in the Transluce
                                article / third-party DSE-wiki analyses
  provenance_cited.json       - retrieval log: bytes/sha256/live_url per report
  expansion/search_summary.json     - 12 live HTMX search queries (all HTTP 204)
  expansion/cache_indicator_hits.json - 12 frozen-cache indicator sweeps

Grain: one record per cited report (kind=download) + one record per indicator
in the union of both sweep files (15 indicators; kind=corpus_hit when the
frozen-cache sweep found hits, else corpus_grep_negative).

No rollup.jsonl: this collection is a pure event stream (report verifications
+ sweep queries); there is no burst/window/per-actor layer to aggregate.

Fingerprint identity strings (documented in PROVENANCE.md):
  reports: sha256("dse-wiki-report:<report_id>")
  sweeps:  sha256("dse-wiki-sweep:<indicator>")
"""
import json, sys, hashlib, glob, os
from datetime import datetime, timezone

ROOT = sys.argv[1]
D = os.path.join(ROOT, "data", "2022-12-30-dse-wiki-verification")
RAW = os.path.join(D, "raw")
SLUG = "2022-12-30-dse-wiki-verification"
CREATED = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def fp(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def rec(ts, kind, ident, labels, **kw):
    r = {
        "@timestamp": ts,
        "event": {"dataset": SLUG, "created": CREATED},
        "record_kind": kind,
        "fingerprint": fp(ident),
        "labels": labels,
    }
    r.update(kw)
    return r

out = []

# --- 1. cited report downloads ---
prov = json.load(open(os.path.join(RAW, "provenance_cited.json")))
retrieved_at = prov["retrieval_utc"].replace("+00:00", "Z")
for f in sorted(glob.glob(os.path.join(RAW, "reports", "*.json"))):
    d = json.load(open(f))
    rid = d["report_id"]
    p = prov["reports"][rid]
    u = d.get("url", {}) or {}
    submitted = u.get("addr") if isinstance(u, dict) else None
    labels = {
        "report.id": rid,
        "report.version": d.get("version"),
        "report.status": d.get("status"),
        "report.submitted_url": (submitted or "")[:500],
        "report.date": d.get("date"),
        "report.bytes": p["bytes"],
        "report.sha256": p["sha256"],
        "timestamp_source": "labels:report.date",
    }
    out.append(rec(
        d["date"], "download", f"dse-wiki-report:{rid}", labels,
        source_url=p["live_url"],
        sha256=p["sha256"],
        size_bytes=p["bytes"],
        retrieved_at=retrieved_at,
        retrieved_via="live urlquery.net/report/<id>/json (Chrome UA, >=20s pacing)",
        description=f"urlquery report {rid} ({d.get('date')}) cited in third-party DSE-wiki analyses: still live, JSON valid, {p['bytes']} B",
        confidence="confirmed",
    ))

# --- 2. indicator sweeps (union of both sweep files) ---
summ = json.load(open(os.path.join(RAW, "expansion", "search_summary.json")))
hits = json.load(open(os.path.join(RAW, "expansion", "cache_indicator_hits.json")))
SWEEP_TS = "2026-09-27T00:00:00Z"
for ind in sorted(set(summ) | set(hits)):
    s = summ.get(ind, {})
    h = hits.get(ind, {})
    count = h.get("count", 0)
    samples = h.get("sample", [])
    sample_ids = [x.get("report_id") for x in samples if x.get("report_id")]
    sample_dates = sorted({x.get("date") for x in samples if x.get("date")})
    kind = "corpus_hit" if count > 0 else "corpus_grep_negative"
    labels = {
        "sweep.indicator": ind,
        "sweep.query": s.get("query", ""),
        "sweep.live_http_status": s.get("http_status"),
        "sweep.live_uuids": s.get("uuids", []),
        "sweep.live_trusted": False,
        "sweep.cache_hits": count,
        "sweep.sample_report_ids": sample_ids,
        "sweep.sample_dates": sample_dates,
        "sweep.present_in": sorted([k for k, v in
            (("search_summary", ind in summ), ("cache_indicator_hits", ind in hits)) if v]),
        "timestamp_source": "lane:2026-09-27 (indicator sweep; per-query timestamps absent from raw)",
    }
    if ind in ("unm_nmdigital", "unm_tok_expt"):
        labels["sweep.note"] = "1 mention, not a probe (page title reference, not a scan)"
    out.append(rec(
        SWEEP_TS, kind, f"dse-wiki-sweep:{ind}", labels,
        description=(f"Indicator sweep '{s.get('query', ind)}': {count} frozen-cache hit(s); "
                     f"live HTMX search returned HTTP {s.get('http_status')} (untrusted as negative)"),
    ))

dest = os.path.join(D, "events.jsonl")
with open(dest, "w", encoding="utf-8") as fh:
    for r in out:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"wrote {len(out)} records -> {dest}")
print(f"  downloads: {sum(1 for r in out if r['record_kind']=='download')}")
print(f"  corpus_hit: {sum(1 for r in out if r['record_kind']=='corpus_hit')}")
print(f"  corpus_grep_negative: {sum(1 for r in out if r['record_kind']=='corpus_grep_negative')}")
