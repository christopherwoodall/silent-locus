#!/usr/bin/env python3
"""Schema backfill 2026-09-29 (worker 2): sweep/scan collections onto the
shared record schema. Mirrors scripts/backfill_schema_2026_09_28.py.

Lossless: every original field survives (moved to labels, never dropped).
Idempotent: records already carrying @timestamp + 64-hex fingerprint +
event.dataset are left untouched.

Usage: python3 temp/backfill_w2.py [--check]
"""

import hashlib
import json
import sys
from datetime import datetime, timezone

REPO = __file__.rsplit("/temp/", 1)[0]
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

CANONICAL_TOP = {
    "@timestamp", "event", "record_kind", "fingerprint", "labels",
    "observer", "retrieved_at", "retrieved_via", "source_url",
    "matched_string", "description", "note", "tags", "confidence",
    "sha256", "size_bytes", "file", "status", "observed_at",
}


def fp(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def new_event(dataset: str) -> dict:
    return {"dataset": dataset, "created": NOW}


def to_utc_z(ts: str) -> str:
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def loose_ts(value):
    if not value or not isinstance(value, str) or "x" in value:
        return None
    v = value.strip()
    try:
        if len(v) == 10:
            return to_utc_z(v + "T00:00:00+00:00")
        return to_utc_z(v)
    except ValueError:
        return None


def diffend_ts(value):
    """Parse 'May 12, 2026 03:18' (assumed UTC) -> ISO Z, else None."""
    if not value or not isinstance(value, str):
        return None
    try:
        dt = datetime.strptime(value.strip(), "%b %d, %Y %H:%M")
        return dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
    except ValueError:
        return None


def order(rec: dict) -> dict:
    first = ["@timestamp", "event", "record_kind", "fingerprint", "labels",
             "observer", "retrieved_at", "retrieved_via", "source_url",
             "matched_string", "description", "note", "tags", "confidence",
             "sha256", "size_bytes", "file", "status", "observed_at"]
    out = {k: rec[k] for k in first if k in rec}
    out.update({k: v for k, v in rec.items() if k not in out})
    return out


def move_to_labels(rec, fields, renames=None):
    renames = renames or {}
    labels = rec.get("labels", {})
    if not isinstance(labels, dict):
        raise ValueError("labels is not a dict")
    for f in fields:
        if f in rec:
            labels[renames.get(f, f)] = rec.pop(f)
    rec["labels"] = labels
    return rec


def flatten_labels(rec):
    """Flatten any nested dict values in labels to dotted keys (lossless)."""
    labels = rec["labels"]
    out = {}
    for k, v in labels.items():
        if isinstance(v, dict):
            for sk, sv in v.items():
                assert not isinstance(sv, (dict, list)), f"deep nesting labels.{k}.{sk}"
                out[f"{k}.{sk}"] = sv
        else:
            out[k] = v
    rec["labels"] = out
    return rec


def already_done(rec) -> bool:
    fpr = rec.get("fingerprint") or ""
    return (isinstance(rec.get("event"), dict) and rec["event"].get("dataset")
            and rec.get("@timestamp") and len(fpr) == 64
            and all(c in "0123456789abcdef" for c in fpr))


# ---------------------------------------------------------------- transforms

def t_venues(rec):
    # agent-convo-venues: near-conformant; only @timestamp missing.
    if already_done(rec):
        return rec
    rec["@timestamp"] = to_utc_z(rec["labels"]["observed_at"])
    rec["labels"]["timestamp_source"] = "labels:observed_at"
    return order(rec)


def t_relay(rec):
    # agents-relay-sweep: @timestamp missing; fingerprint is a non-hex slug.
    if already_done(rec):
        return rec
    rec["@timestamp"] = to_utc_z(rec["labels"]["observed_at"])
    rec["labels"]["timestamp_source"] = "labels:observed_at"
    old = rec.get("fingerprint", "")
    if not (len(old) == 64 and all(c in "0123456789abcdef" for c in old)):
        # lossless: keep the original slug; new fp = sha256 of the slug
        rec["labels"]["legacy_fingerprint"] = old
        rec["fingerprint"] = fp(old)
    return order(rec)


def t_commonlog(rec):
    # commonlog-scan: @timestamp missing; labels.false_positive_reasons nested.
    if already_done(rec) and not any(isinstance(v, dict) for v in rec["labels"].values()):
        return rec
    rec = flatten_labels(rec)
    if not rec.get("@timestamp"):
        ts = loose_ts(rec["labels"].get("posted_utc"))
        if ts:
            rec["@timestamp"] = ts
            rec["labels"]["timestamp_source"] = "labels:posted_utc"
        else:
            rec["@timestamp"] = "1970-01-01T00:00:00Z"
            rec["labels"]["timestamp_source"] = "fallback:no_recoverable_date"
    return order(rec)


def t_urlquery(rec):
    if already_done(rec):
        return rec
    expect = {"report_id", "report_url", "date", "marker", "location",
              "evidence_grade", "matched_string", "notes"}
    extra = set(rec) - expect - CANONICAL_TOP
    assert not extra, f"urlquery: unexpected keys {sorted(extra)}"
    rid = rec["report_id"]
    rec = move_to_labels(rec, ["report_id", "marker", "location",
                               "evidence_grade"])
    # canonical renames: report_url -> source_url, notes -> note
    rec["source_url"] = rec.pop("report_url")
    rec["note"] = rec.pop("notes")
    rec["event"] = new_event("urlquery-marker-sweep")
    rec["record_kind"] = "venue_finding"
    ts = loose_ts(rec.pop("date", None))
    if ts:
        rec["@timestamp"] = ts
        rec["labels"]["timestamp_source"] = "labels:date"
    else:
        rec["@timestamp"] = "1970-01-01T00:00:00Z"
        rec["labels"]["timestamp_source"] = "fallback:no_recoverable_date"
    rec["fingerprint"] = fp(rid)
    return order(rec)


def t_osv(pass_name):
    def fn(rec):
        if already_done(rec):
            return rec
        expect = {"name", "in_diffend", "http_status", "versions",
                  "first_publish", "mechanism_notes", "name_grammars",
                  "diff_error", "retry_pass", "fetch_client"}
        extra = set(rec) - expect - CANONICAL_TOP
        assert not extra, f"osv: unexpected keys {sorted(extra)}"
        name = rec["name"]
        # versions is a list of {version, ts} dicts; flatten into two
        # parallel scalar arrays (lossless, ECS labels rule).
        vers = rec.get("versions", [])
        rec = move_to_labels(rec, ["name", "in_diffend", "http_status",
                                   "first_publish", "mechanism_notes",
                                   "name_grammars", "diff_error",
                                   "retry_pass", "fetch_client"],
                             renames={"name": "gem.name",
                                      "first_publish": "first_publish_raw"})
        rec.pop("versions", None)
        lab = rec["labels"]
        lab["versions.version"] = [v["version"] for v in vers]
        lab["versions.ts"] = [v["ts"] for v in vers]
        rec["event"] = new_event("osv")
        rec["record_kind"] = ("diffend_harvest" if rec["labels"]["in_diffend"]
                              else "sweep_negative")
        ts = diffend_ts(lab.get("first_publish_raw"))
        if ts:
            rec["@timestamp"] = ts
            lab["timestamp_source"] = "labels:first_publish_raw"
        else:
            rec["@timestamp"] = "1970-01-01T00:00:00Z"
            lab["timestamp_source"] = "fallback:no_recoverable_date"
        rec["fingerprint"] = fp(name + "|" + pass_name)
        return order(rec)
    return fn


def t_hfspace(rec):
    if already_done(rec):
        return rec
    expect = {"id", "url", "live", "sdk", "created", "modified", "likes",
              "shape", "swarm_tie", "tie_strength"}
    extra = set(rec) - expect - CANONICAL_TOP
    assert not extra, f"hfspace: unexpected keys {sorted(extra)}"
    sid = rec["id"]
    rec = move_to_labels(rec, ["id", "live", "sdk", "created", "modified",
                               "likes", "shape", "swarm_tie", "tie_strength"],
                         renames={"id": "space.id", "live": "space.live_url",
                                  "sdk": "space.sdk",
                                  "created": "space.created",
                                  "modified": "space.modified",
                                  "likes": "space.likes"})
    rec["source_url"] = rec.pop("url")
    rec["event"] = new_event("hfspace-proxies")
    rec["record_kind"] = "venue_probe"
    ts = loose_ts(rec["labels"].get("space.created"))
    if ts:
        rec["@timestamp"] = ts
        rec["labels"]["timestamp_source"] = "labels:space.created"
    else:
        rec["@timestamp"] = "1970-01-01T00:00:00Z"
        rec["labels"]["timestamp_source"] = "fallback:no_recoverable_date"
    rec["fingerprint"] = fp(sid)
    return order(rec)


JOBS = [
    ("data/agent-convo-venues/venues.jsonl", t_venues),
    ("data/agents-relay-sweep/sweep.jsonl", t_relay),
    ("data/commonlog-scan/messages.jsonl", t_commonlog),
    ("data/urlquery-marker-sweep/hits.jsonl", t_urlquery),
    ("data/osv/diffend_sweep_results.jsonl", t_osv("initial")),
    ("data/osv/diffend_sweep_results_retry.jsonl", t_osv("retry")),
    ("data/hfspace-proxies/spaces.jsonl", t_hfspace),
]


def validate(rec, ctx):
    assert rec.get("event", {}).get("dataset"), f"{ctx}: event.dataset missing"
    assert rec.get("record_kind"), f"{ctx}: record_kind missing"
    assert rec.get("fingerprint"), f"{ctx}: fingerprint missing"
    assert isinstance(rec.get("labels"), dict) and rec["labels"], \
        f"{ctx}: labels missing/empty"
    stray = set(rec) - CANONICAL_TOP
    assert not stray, f"{ctx}: non-canonical top-level keys {sorted(stray)}"
    to_utc_z(rec["@timestamp"])


def main():
    check_only = "--check" in sys.argv
    total = 0
    for rel, fn in JOBS:
        p = f"{REPO}/{rel}"
        lines = open(p).read().splitlines()
        out = []
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            rec = fn(json.loads(line))
            validate(rec, f"{rel}:{i}")
            out.append(json.dumps(rec, ensure_ascii=False))
        total += len(out)
        if not check_only:
            open(p, "w").write("\n".join(out) + "\n")
        print(f"{'checked' if check_only else 'rewrote'} {rel}: "
              f"{len(out)} records")
    print(f"total: {total} records")


if __name__ == "__main__":
    main()
