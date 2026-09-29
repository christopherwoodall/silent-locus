#!/usr/bin/env python3
"""Schema backfill 2026-09-29 (worker W1): data/dockerhub-trojan-images/.

Brings 42 pre-schema JSONL files onto the shared record schema
(schema/record.schema.json). Mirrors scripts/backfill_schema_2026_09_28.py.

Source shapes (all pre-schema, verified by full key-set scan):
  corpus-trojan-tag-liveness.jsonl:
      {org, repo, tag, status, retrieved, source}
      LIVE rows add {tag_last_pushed, last_updated, digest}
  final-gone-trojan-tags.jsonl:
      {org, repo, tag, tag_last_pushed, last_updated, liveness,
       retrieved, sources, note}
  final-* (other 20 files):
      {org, repo, tag, tag_last_pushed, last_updated, tag_status, digest,
       images_arch, metadata_fetched, liveness, retrieved, sources}
  hub10-* and repo-* (19 files):
      {org, repo, tag, tag_last_pushed, tag_status, last_updated, digest,
       images_arch, retrieved, source}

Mapping:
  status / liveness -> canonical `status` (liveness probe result)
  source -> source_url; sources (array) -> source_url when exactly one
    non-null entry, otherwise labels.sources (lossless)
  retrieved -> retrieved_at and @timestamp (the liveness/listing probe
    time IS the event time); labels.timestamp_source = "retrieved_at"
  note -> canonical note (already top-level, kept verbatim)
  everything else -> labels (flat, dotted where useful)
  record_kind: tag_liveness (corpus/final/gone families: per-tag liveness
    probes) or tag_listing (hub10/repo families: registry/hub tag listings)
  fingerprint = sha256(family + "|" + org + "|" + repo + "|" + tag)
    family is the filename prefix (corpus|final|gone|hub10|repo) so
    the same tag probed by different sweeps keeps distinct fingerprints.

Idempotent: records already carrying event+fingerprint pass through.
Stdlib only.
"""

import glob
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

REPO = __file__.rsplit("/temp/", 1)[0]
DIR = os.path.join(REPO, "data", "dockerhub-trojan-images")
NOW = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
DATASET = "dockerhub-trojan-images"

CANONICAL_TOP = {
    "@timestamp", "event", "record_kind", "fingerprint", "labels",
    "observer", "retrieved_at", "retrieved_via", "source_url",
    "matched_string", "description", "note", "tags", "confidence",
    "sha256", "size_bytes", "file", "status", "observed_at",
}

# per-file record_kind / family, derived from filename prefix
LIVENESS_LABEL_KEYS = ["org", "repo", "tag", "tag_last_pushed",
                       "last_updated", "tag_status", "digest",
                       "images_arch", "metadata_fetched"]


def fp(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def to_utc_z(ts: str) -> str:
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def order(rec: dict) -> dict:
    first = ["@timestamp", "event", "record_kind", "fingerprint", "labels",
             "observer", "retrieved_at", "retrieved_via", "source_url",
             "matched_string", "description", "note", "tags", "confidence",
             "sha256", "size_bytes", "file", "status", "observed_at"]
    out = {k: rec[k] for k in first if k in rec}
    out.update({k: v for k, v in rec.items() if k not in out})
    return out


def family_of(fname: str) -> str:
    for fam in ("corpus", "final", "gone", "hub10", "repo"):
        if fname.startswith(fam):
            return "gone" if fname == "final-gone-trojan-tags.jsonl" else fam
    raise ValueError(f"unknown file family: {fname}")


def transform(rec: dict, family: str) -> dict:
    if rec.get("event", {}).get("dataset") and rec.get("fingerprint"):
        return rec  # already conformant (idempotent re-run)

    kind = "tag_listing" if family in ("hub10", "repo") else "tag_liveness"
    rec = dict(rec)  # don't mutate caller

    # canonical status: `status` (corpus file) or `liveness` (final/gone)
    if "status" in rec:
        status = rec.pop("status")
    elif "liveness" in rec:
        status = rec.pop("liveness")
    else:
        status = None

    # source / sources -> source_url
    source_url = None
    if "source" in rec:
        source_url = rec.pop("source")
    if "sources" in rec:
        srcs = rec.pop("sources")
        nonnull = [s for s in srcs if s]
        if source_url is None and len(nonnull) == 1 and len(srcs) == 1:
            source_url = nonnull[0]
        else:
            rec.setdefault("labels", {})["sources"] = srcs

    # retrieved -> retrieved_at (+ @timestamp below)
    retrieved = rec.pop("retrieved", None)

    labels = rec.get("labels", {})
    for k in LIVENESS_LABEL_KEYS:
        if k in rec:
            labels[k] = rec.pop(k)
    rec["labels"] = labels
    labels["timestamp_source"] = "retrieved_at" if retrieved else "none"

    stray = set(rec) - CANONICAL_TOP
    if stray:
        raise ValueError(f"unexpected top-level keys: {sorted(stray)}")

    if status is not None:
        rec["status"] = status
    if source_url:
        rec["source_url"] = source_url
    if retrieved:
        rec["retrieved_at"] = to_utc_z(retrieved)
        rec["@timestamp"] = rec["retrieved_at"]
    else:
        rec["@timestamp"] = "1970-01-01T00:00:00Z"
    rec["event"] = {"dataset": DATASET, "created": NOW}
    rec["record_kind"] = kind
    ident = "|".join([family, str(labels.get("org")),
                      str(labels.get("repo")), str(labels.get("tag"))])
    rec["fingerprint"] = fp(ident)
    return order(rec)


def main():
    check_only = "--check" in sys.argv
    files = sorted(glob.glob(os.path.join(DIR, "*.jsonl")))
    total = 0
    for p in files:
        fname = os.path.basename(p)
        fam = family_of(fname)
        with open(p) as f:
            lines = f.read().splitlines()
        out = []
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            rec = transform(json.loads(line), fam)
            # post-transform conformance spot-asserts
            assert rec["event"]["dataset"] == DATASET
            assert rec.get("record_kind") and rec.get("fingerprint")
            assert isinstance(rec["labels"], dict) and rec["labels"]
            assert not (set(rec) - CANONICAL_TOP)
            out.append(json.dumps(rec, ensure_ascii=False))
        total += len(out)
        if not check_only:
            with open(p, "w") as f:
                f.write("\n".join(out) + "\n")
        print(f"{'checked' if check_only else 'rewrote'} {fname}: "
              f"{len(out)} records")
    print(f"total: {total} records in {len(files)} files")


if __name__ == "__main__":
    main()
