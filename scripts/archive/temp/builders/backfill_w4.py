#!/usr/bin/env python3
"""Schema backfill 2026-09-29 (worker w4): bring 5 pre-schema JSONL files
onto the shared corpus schema. Mirrors scripts/backfill_schema_2026_09_28.py.

Files:
  data/proxy-primitives/hits.jsonl                              (raw hits)
  data/university-shorteners/university-shorteners.jsonl        (near-conformant)
  data/university-shorteners-batch2/university-shorteners-batch2.jsonl
  data/university-shorteners-batch3/university-shorteners-batch3.jsonl
  data/university-shorteners-events/university-shorteners-events.jsonl

Rules: lossless (extra top-level keys -> labels, nested labels flattened with
dotted keys), additive only (existing event/@timestamp/record_kind kept
verbatim; existing event.dataset never rewritten). Idempotent: a record that
already conforms passes through unchanged.

Usage: python3 temp/backfill_w4.py [--check]
"""

import hashlib
import json
import re
import sys
import os
from datetime import datetime, timezone

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

CANONICAL_TOP = {
    "@timestamp", "event", "record_kind", "fingerprint", "labels",
    "observer", "retrieved_at", "retrieved_via", "source_url",
    "matched_string", "description", "note", "tags", "confidence",
    "sha256", "size_bytes", "file", "status", "observed_at",
}

# record_kind values in proxy-primitives that violate ^[a-z0-9_]+$ ->
# snake_case normalizations (originals preserved in labels.record_kind_original)
KIND_FIX = {"corpus-hit": "corpus_hit", "gem-name-fragment": "gem_name_fragment"}


def fp(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def to_utc_z(ts: str) -> str:
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


KEY_OK = re.compile(r"^[a-z0-9_.]+$")


def sanitize_key(key: str) -> str:
    """Labels keys must match ^[a-z0-9_.]+$. Replace any other char with '_'.
    Callers record the original under labels._keymap.<sanitized> when the
    key changed (lossless)."""
    return re.sub(r"[^a-z0-9_.]", "_", key)


def flatten_labels(labels: dict) -> dict:
    """Flatten nested dicts one level deep with dotted keys.
    - dict value -> parent.child dotted keys (recursively)
    - empty dict -> JSON string "{}" (lossless, documented)
    - array containing dicts/lists -> each element JSON-encoded to a string
    - scalars / arrays of scalars pass through unchanged
    - keys outside ^[a-z0-9_.]+$ are sanitized ('-' etc. -> '_'); the
      original key string is kept at labels._keymap.<sanitized>
    """
    out = {}

    def put(key, value):
        if isinstance(value, dict):
            if not value:
                out[key] = "{}"
            else:
                for ck, cv in value.items():
                    put(f"{key}.{ck}", cv)
        elif isinstance(value, list):
            if any(isinstance(i, (dict, list)) for i in value):
                out[key] = [json.dumps(i, sort_keys=True, separators=(",", ":"))
                            if isinstance(i, (dict, list)) else i
                            for i in value]
            else:
                out[key] = value
        else:
            out[key] = value

    for k, v in labels.items():
        put(k, v)
    fixed = {}
    for k, v in out.items():
        sk = sanitize_key(k)
        if sk != k:
            fixed[f"_keymap.{sk}"] = k
        fixed[sk] = v
    return fixed


def order(rec: dict) -> dict:
    first = ["@timestamp", "event", "record_kind", "fingerprint", "labels",
             "observer", "retrieved_at", "retrieved_via", "source_url",
             "matched_string", "description", "note", "tags", "confidence",
             "sha256", "size_bytes", "file", "status", "observed_at"]
    out = {k: rec[k] for k in first if k in rec}
    out.update({k: v for k, v in rec.items() if k not in out})
    return out


def conforms(rec: dict) -> bool:
    return (set(rec) <= CANONICAL_TOP
            and {"@timestamp", "event", "record_kind", "fingerprint",
                 "labels"} <= set(rec))


# ---------------------------------------------------------------- transforms

PROXY_MOVE = ["primitive", "source", "laundered_target",
              "first_seen_effective", "first_seen", "first_seen_note",
              "host", "relation", "n_record_ids", "hit_sha", "record_id",
              "selection_basis", "omitted_url_sha256", "time", "line_no",
              "context", "wikis", "n_agents", "agents_sample", "target_host",
              "doc_id", "external_links"]


def t_proxy(rec: dict) -> dict:
    if conforms(rec):
        return order(rec)
    labels = dict(rec.get("labels", {}))
    for f in PROXY_MOVE:
        if f in rec:
            labels[f] = rec.pop(f)
    extra = set(rec) - CANONICAL_TOP
    if extra:
        raise ValueError(f"proxy-primitives: unexpected keys {sorted(extra)}")
    rec["labels"] = flatten_labels(labels)
    # record_kind: keep existing; normalize the two hyphenated values
    if rec["record_kind"] in KIND_FIX:
        rec["labels"]["record_kind_original"] = rec["record_kind"]
        rec["record_kind"] = KIND_FIX[rec["record_kind"]]
    rec["event"] = {"dataset": "proxy-primitives", "created": NOW}
    # @timestamp: first_seen_effective > first_seen > time > sentinel
    ts = None
    for cand in ("first_seen_effective", "first_seen", "time"):
        v = rec["labels"].get(cand)
        if isinstance(v, str) and v.strip():
            ts = to_utc_z(v)
            rec["labels"]["timestamp_source"] = f"labels:{cand}"
            break
    rec["@timestamp"] = ts or "1970-01-01T00:00:00Z"
    if ts is None:
        rec["labels"]["timestamp_source"] = "fallback:no_recoverable_date"
    # fingerprint: adopt the pipeline-computed hit_sha verbatim (unique over
    # all 1522 rows, verified); identity string = labels.hit_sha
    rec["fingerprint"] = rec["labels"]["hit_sha"]
    return order(rec)


def t_university(rec: dict, rollup: bool) -> dict:
    """University-shorteners files: already canonical except missing
    fingerprint and nested labels (pattern_families/referrers/best_day/
    traffic_summary dicts, daily_*/referrer_urls arrays of objects).
    Existing event/@timestamp/record_kind are kept verbatim."""
    extra = set(rec) - CANONICAL_TOP
    if extra:
        raise ValueError(f"university-shorteners: unexpected keys {sorted(extra)}")
    rec["labels"] = flatten_labels(rec.get("labels", {}))
    if "fingerprint" not in rec:
        lab = rec["labels"]
        if "event_id" in lab:
            identity = lab["event_id"]              # events file
        else:
            identity = (rec["record_kind"] + "|"
                        + lab["shortener.instance"] + "|" + lab["short_url"])
        rec["fingerprint"] = fp(identity)
    return order(rec)


JOBS = [
    ("data/proxy-primitives/hits.jsonl", t_proxy),
    ("data/university-shorteners/university-shorteners.jsonl",
     lambda r: t_university(r, rollup=True)),
    ("data/university-shorteners-batch2/university-shorteners-batch2.jsonl",
     lambda r: t_university(r, rollup=True)),
    ("data/university-shorteners-batch3/university-shorteners-batch3.jsonl",
     lambda r: t_university(r, rollup=True)),
    ("data/university-shorteners-events/university-shorteners-events.jsonl",
     lambda r: t_university(r, rollup=False)),
]


def validate(rec: dict, ctx: str):
    assert rec.get("event", {}).get("dataset"), f"{ctx}: event.dataset missing"
    assert rec.get("record_kind"), f"{ctx}: record_kind missing"
    assert rec.get("fingerprint"), f"{ctx}: fingerprint missing"
    assert isinstance(rec.get("labels"), dict), f"{ctx}: labels not a dict"
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
