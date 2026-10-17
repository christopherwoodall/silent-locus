#!/usr/bin/env python3
"""Validate the Android-World factum bundle (pre-submit) or an exported batch.

Usage:
  validate_batch.py bundle-android-world.json            (pre-submit)
  validate_batch.py data/records/<batch>/records.jsonl  (post-export)

Checks (independent re-derivation, not a re-read of the builder):
- bundle envelope: bundle==2, actor, idempotency_key; envelope lane ABSENT
  (factum add appends one in_lane edge per bundle record when envelope
  lane is set -- that would break the edge-count checks below; lane
  membership rides on tags.lane, checked per record per the standing rule)
- bundle-local refs unique; every @ref target exists
- observations have observed_at + time_basis + type + data
- counts: source==1, run==1, artifact==464, dataset.record==464,
  dataset.snapshot==1, intel.behavior==12, behavior.tool_sequence==11,
  related_to==464, supports==12
- external_record_id unique across dataset.records
- tool_sequence length == len(steps); steps have index/tool/command
- every finding id V-01..V-12 present exactly once
"""
import json
import re
import sys
from collections import Counter

LANE = "android-world-trajectories"
FINDING_IDS = ["V-%02d" % i for i in range(1, 13)]


def load(path):
    if path.endswith(".jsonl"):
        return [json.loads(l) for l in open(path) if l.strip()], None
    d = json.load(open(path))
    return d["records"], d


def main():
    path = sys.argv[1]
    records, bundle = load(path)
    errors = []
    if bundle is not None:
        for k, v in (("bundle", 2), ("actor", "agent:android-world-ingestor"),
                     ("idempotency_key", "android-world-ingest-2026-10-16-v1")):
            if bundle.get(k) != v:
                errors.append("envelope %s: %r != %r" % (k, bundle.get(k), v))
        # Envelope lane must be ABSENT: store.py's add appends one in_lane
        # edge per bundle record when envelope lane is set, which would
        # break the edge-count checks below and submit 1430 unreviewed
        # edges. Lane membership rides on tags.lane (checked per record).
        if bundle.get("lane") is not None:
            errors.append("envelope lane must be absent (got %r)" % (bundle.get("lane"),))

    refs = [r.get("ref") for r in records if r.get("ref") is not None]
    if len(set(refs)) != len(refs):
        dupes = [t for t, n in Counter(refs).items() if n > 1]
        errors.append("duplicate bundle refs: %s" % dupes[:5])
    ref_set = set(refs)

    def resolve(val):
        # bundle-local @ref -> exists?
        if isinstance(val, str) and val.startswith("@"):
            return val[1:] in ref_set
        return True

    kinds = Counter()
    otypes = Counter()
    preds = Counter()
    tids, fids, seqs = [], [], []
    for r in records:
        k = r.get("kind") or r.get("record_kind")
        kinds[k] += 1
        body = r.get("body") or {}
        tags = r.get("tags") or {}
        rid = r.get("ref") or r.get("id") or "?"
        if tags.get("lane") != LANE:
            errors.append("%s: missing tags.lane=%s" % (rid, LANE))
        if k == "observation":
            for f in ("observed_at", "time_basis", "type", "data"):
                if not body.get(f):
                    errors.append("%s: observation missing %s" % (rid, f))
            # observed_at must be a full date-time (format: date-time), not a
            # bare date -- the store rejects "2026-10-17" with SCHEMA/format
            # (found 2026-10-17; fixed via fix_observed_at_format.py).
            oa = body.get("observed_at")
            if oa and not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", oa):
                errors.append("%s: observed_at not date-time: %r" % (rid, oa))
            t = body.get("type")
            otypes[t] += 1
            data = body.get("data") or {}
            if t == "dataset.record":
                erid = data.get("external_record_id")
                if erid:
                    tids.append(erid)
                if not resolve((data.get("locator") or {}).get("artifact")):
                    errors.append("%s: locator.artifact unresolvable" % rid)
                if not resolve(data.get("snapshot")):
                    errors.append("%s: snapshot unresolvable" % rid)
                for fl in body.get("files") or []:
                    if not resolve((fl or {}).get("artifact")):
                        errors.append("%s: files[].artifact unresolvable" % rid)
            if t == "intel.behavior":
                fid = (tags.get("finding_id") or "")
                fids.append(fid)
            if t == "behavior.tool_sequence":
                steps = data.get("steps") or []
                if data.get("length") != len(steps):
                    errors.append("%s: length != len(steps)" % rid)
                for s in steps:
                    if not all(x in s for x in ("index", "tool", "command")):
                        errors.append("%s: step missing keys" % rid)
                seqs.append(tags.get("finding_id"))
            if not resolve(body.get("source")):
                errors.append("%s: source unresolvable" % rid)
            if not resolve(body.get("run")):
                errors.append("%s: run unresolvable" % rid)
        if k == "edge":
            p = body.get("predicate")
            preds[p] += 1
            if not resolve(body.get("subject")):
                errors.append("%s: edge subject unresolvable" % rid)
            if not resolve(body.get("object")):
                errors.append("%s: edge object unresolvable" % rid)

    if len(set(tids)) != len(tids):
        dupes = [t for t, n in Counter(tids).items() if n > 1]
        errors.append("duplicate external_record_ids: %s" % dupes[:5])
    if sorted(fids) != sorted(FINDING_IDS):
        errors.append("finding ids mismatch: %s" % sorted(set(FINDING_IDS) - set(fids)))
    if sorted(seqs) != sorted([x for x in FINDING_IDS if x != "V-02"]):
        errors.append("tool_sequence finding ids mismatch: %s" % sorted(seqs))

    for k, n in (("source", 1), ("run", 1), ("artifact", 464)):
        if kinds.get(k, 0) != n:
            errors.append("kind %s: %d != %d" % (k, kinds.get(k, 0), n))
    for t, n in (("dataset.record", 464), ("dataset.snapshot", 1),
                 ("intel.behavior", 12), ("behavior.tool_sequence", 11)):
        if otypes.get(t, 0) != n:
            errors.append("observation type %s: %d != %d" % (t, otypes.get(t, 0), n))
    for p, n in (("related_to", 464), ("supports", 12)):
        if preds.get(p, 0) != n:
            errors.append("edge predicate %s: %d != %d" % (p, preds.get(p, 0), n))

    print("records=%d kinds=%s observation_types=%s edges=%s"
          % (len(records), dict(kinds), dict(otypes), dict(preds)))
    if errors:
        print("ERRORS (%d):" % len(errors))
        for e in errors[:40]:
            print("  -", e)
        sys.exit(1)
    print("VALIDATE-OK")


if __name__ == "__main__":
    main()
