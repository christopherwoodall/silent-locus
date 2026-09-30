#!/usr/bin/env python3
"""Schema backfill 2026-09-29 (wave 6): overlap-analysis aggregate final outputs.

Brings the six script-written, regenerable final-output JSONL files of
data/aggregates/overlap-analysis/ onto the shared event schema, following the
2026-09-28 pattern (scripts/backfill_schema_2026_09_28.py):

  @timestamp, event {dataset, created}, record_kind, fingerprint,
  labels {dataset-specific fields, dotted keys}, canonical top-level kept.

Rules:
  - Lossless: every original field survives (moved into labels, never dropped).
  - Original top-level "fingerprint" field was the hunt-finding FAMILY label
    (F1, F3, F6, ntfy-topic, ...), NOT a hash -> moved to labels.match.family;
    a real sha256 fingerprint is computed per record.
  - No date fields exist in these records -> sentinel
    @timestamp 1970-01-01T00:00:00Z + labels.timestamp_source =
    "fallback:no_recoverable_date".
  - event.dataset = "overlap-analysis"; event.created = backfill run time.
  - Fails loudly on unexpected top-level keys.

Fingerprint identity strings (documented in PROVENANCE.md):
  - overlap_match records: sha256("overlap-analysis|overlap_match|"
                                  "<match_id>|<evidence-or-swarmtraces_evidence>")
    (match_id alone collides on exact-duplicate rows in matches-f5f6 /
    overlap-matches; identical content rows intentionally share a fingerprint)
  - paste_link records:      sha256("overlap-analysis|paste_link|"
                                  "<link_type>|<paste_id>|<wiki_side>")

Idempotent: records already carrying event.dataset == "overlap-analysis" and a
64-hex fingerprint are passed through unchanged.

Usage: python3 temp/backfill_w6.py [--check]
"""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone

REPO = __file__.rsplit("/temp/", 1)[0]
BASE = REPO + "/data/aggregates/overlap-analysis"
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
DATASET = "overlap-analysis"
SENTINEL = "1970-01-01T00:00:00Z"
FP_RE = re.compile(r"^[0-9a-f]{64}$")

CANONICAL_TOP = {
    "@timestamp", "event", "record_kind", "fingerprint", "labels",
    "observer", "retrieved_at", "retrieved_via", "source_url",
    "matched_string", "description", "note", "tags", "confidence",
    "sha256", "size_bytes", "file", "status", "observed_at",
}

MATCH_KEYS = {"match_id", "fingerprint", "match_kind", "confidence",
              "hunt_ioc", "hunt_ioc_type", "hunt_reference",
              "swarmtraces_id", "swarmtraces_payload_id",
              "swarmtraces_field", "swarmtraces_evidence",
              "evidence", "notes"}
PASTE_KEYS = {"link_type", "paste_id", "paste_title", "wiki_side",
              "wiki_agents", "wiki_wikis", "note"}

MATCH_RENAMES = {
    "match_id": "match.id",
    "fingerprint": "match.family",  # was hunt-finding family, not a hash
    "match_kind": "match.kind",
    "hunt_ioc": "hunt.ioc",
    "hunt_ioc_type": "hunt.ioc_type",
    "hunt_reference": "hunt.reference",
    "swarmtraces_id": "swarmtraces.id",
    "swarmtraces_payload_id": "swarmtraces.payload_id",
    "swarmtraces_field": "swarmtraces.field",
    "swarmtraces_evidence": "swarmtraces.evidence",
    "evidence": "evidence",
    "notes": "notes",
}
PASTE_RENAMES = {
    "link_type": "link.type",
    "paste_id": "paste.id",
    "paste_title": "paste.title",
    "wiki_side": "wiki_side",
    "wiki_agents": "wiki_agents",
    "wiki_wikis": "wiki_wikis",
}

FIRST = ["@timestamp", "event", "record_kind", "fingerprint", "labels",
         "observer", "retrieved_at", "retrieved_via", "source_url",
         "matched_string", "description", "note", "tags", "confidence",
         "sha256", "size_bytes", "file", "status", "observed_at"]


def fp(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def order(rec: dict) -> dict:
    out = {k: rec[k] for k in FIRST if k in rec}
    out.update({k: v for k, v in rec.items() if k not in out})
    return out


def already_done(rec: dict) -> bool:
    return (isinstance(rec.get("event"), dict)
            and rec["event"].get("dataset") == DATASET
            and FP_RE.match(str(rec.get("fingerprint") or "")) is not None
            and rec.get("record_kind")
            and isinstance(rec.get("labels"), dict))


def t_overlap_match(rec: dict, ctx: str) -> dict:
    extra = set(rec) - MATCH_KEYS
    if extra:
        raise ValueError(f"{ctx}: unexpected top-level keys {sorted(extra)}")
    confidence = rec.pop("confidence")
    labels = {MATCH_RENAMES[k]: v for k, v in rec.items()}
    labels["timestamp_source"] = "fallback:no_recoverable_date"
    ev = labels.get("evidence") or labels.get("swarmtraces.evidence") or ""
    identity = f"{DATASET}|overlap_match|{labels['match.id']}|{ev}"
    return order({
        "@timestamp": SENTINEL,
        "event": {"dataset": DATASET, "created": NOW},
        "record_kind": "overlap_match",
        "fingerprint": fp(identity),
        "labels": labels,
        "confidence": confidence,
    })


def t_paste_link(rec: dict, ctx: str) -> dict:
    extra = set(rec) - PASTE_KEYS
    if extra:
        raise ValueError(f"{ctx}: unexpected top-level keys {sorted(extra)}")
    note = rec.pop("note")  # canonical top-level
    labels = {PASTE_RENAMES[k]: v for k, v in rec.items()}
    labels["timestamp_source"] = "fallback:no_recoverable_date"
    identity = (f"{DATASET}|paste_link|{labels['link.type']}|"
                f"{labels['paste.id']}|{labels['wiki_side']}")
    return order({
        "@timestamp": SENTINEL,
        "event": {"dataset": DATASET, "created": NOW},
        "record_kind": "paste_link",
        "fingerprint": fp(identity),
        "labels": labels,
        "note": note,
    })


JOBS = [
    ("matches-f1f2.jsonl", t_overlap_match),
    ("matches-f3.jsonl", t_overlap_match),
    ("matches-f4f7f8f10f11f12.jsonl", t_overlap_match),
    ("matches-f5f6.jsonl", t_overlap_match),
    ("overlap-matches.jsonl", t_overlap_match),
    ("wiki_paste_links.jsonl", t_paste_link),
]


def validate(rec: dict, ctx: str):
    assert rec.get("event", {}).get("dataset") == DATASET, ctx
    assert rec.get("record_kind"), ctx
    assert FP_RE.match(rec.get("fingerprint", "")), ctx
    assert isinstance(rec.get("labels"), dict) and rec["labels"], ctx
    stray = set(rec) - CANONICAL_TOP
    assert not stray, f"{ctx}: non-canonical top-level keys {sorted(stray)}"
    assert rec["@timestamp"] == SENTINEL, ctx


def main():
    check_only = "--check" in sys.argv
    for name, fn in JOBS:
        p = f"{BASE}/{name}"
        lines = open(p).read().splitlines()
        out, skipped = [], 0
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            rec = json.loads(line)
            if already_done(rec):
                skipped += 1
            else:
                rec = fn(rec, f"{name}:{i}")
            validate(rec, f"{name}:{i}")
            out.append(json.dumps(rec, ensure_ascii=False))
        assert len(out) == sum(1 for l in lines if l.strip()), name
        if not check_only:
            open(p, "w").write("\n".join(out) + "\n")
        print(f"{'checked' if check_only else 'rewrote'} {name}: "
              f"{len(out)} records ({skipped} already conforming)")
    print("done")


if __name__ == "__main__":
    main()
