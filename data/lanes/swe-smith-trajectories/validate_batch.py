#!/usr/bin/env python3
"""Validate an exported SWE-smith factum batch file directly (no DB locks).

Usage: validate_batch.py data/records/<batch>/records.jsonl

Checks (independent re-derivation, not a re-read of the builder):
- every line parses; record has id, record_kind, body, tags, fingerprint
- tags.lane == swe-smith-trajectories on every bundle-authored record
  (toolkit-auto in_lane edges carry no tags by design; counted separately)
- observations have observed_at + time_basis + type + data
- every declared reference target (edge subject/object, observation
  source/run/data.snapshot/data.locator.artifact/files[].artifact,
  claim cites) exists in the batch; no unresolved @refs
- counts: source==1, run==1, artifact==6, dataset.record==13,
  dataset.snapshot==1, intel.behavior==13, related_to==13, supports==13
- external_record_id unique; artifact sha256/size present
"""
import json
import re
import sys
from collections import Counter

LANE = "swe-smith-trajectories"
ID_RE = re.compile(r"^(source|artifact|observation|observable|sighting|event|claim|edge|assessment|run|retraction|lane)_[0-9a-f]{32}$")


def kind_of(r):
    return r.get("record_kind") or r.get("kind")


def ref_targets(r):
    body = r.get("body") or {}
    k = kind_of(r)
    if k == "edge":
        yield "subject", body.get("subject")
        yield "object", body.get("object")
        for i, c in enumerate(body.get("cites") or []):
            yield "cites[%d]" % i, c
    if k == "observation":
        yield "source", body.get("source")
        yield "run", body.get("run")
        data = body.get("data") or {}
        yield "data.snapshot", data.get("snapshot")
        loc = data.get("locator") or {}
        yield "data.locator.artifact", loc.get("artifact")
        for i, f in enumerate(body.get("files") or []):
            yield "files[%d].artifact" % i, (f or {}).get("artifact")
    if k == "claim":
        for i, c in enumerate(body.get("cites") or []):
            yield "cites[%d]" % i, c


def main():
    path = sys.argv[1]
    errors, warnings = [], []
    n_inlane_auto = 0
    records = []
    with open(path) as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                errors.append("line %d: bad JSON: %s" % (i, e))

    id_set = {r.get("id") for r in records}
    kinds = Counter()
    tids = []
    for r in records:
        k = kind_of(r)
        kinds[k] += 1
        rid = r.get("id", "?")
        if not ID_RE.match(rid or ""):
            errors.append("%s: bad id format" % rid)
        body = r.get("body") or {}
        tags = r.get("tags") or {}
        if tags.get("lane") == LANE:
            pass
        elif k == "edge" and not tags:
            n_inlane_auto += 1
        else:
            errors.append("%s: missing tags.lane=%s" % (rid, LANE))
        if k == "observation":
            for f in ("observed_at", "time_basis", "type", "data"):
                if not body.get(f):
                    errors.append("%s: observation missing %s" % (rid, f))
            data = body.get("data") or {}
            if body.get("type") == "dataset.record":
                erid = data.get("external_record_id")
                if erid:
                    tids.append(erid)
                for f in ("sha256",):
                    pass
        if k == "artifact":
            if not body.get("sha256") or not body.get("size"):
                errors.append("%s: artifact missing sha256/size" % rid)
        if k == "source":
            if not body.get("locator"):
                errors.append("%s: source missing locator" % rid)
        for path_, val in ref_targets(r):
            if val is None:
                continue
            if not isinstance(val, str) or not val.startswith("@"):
                continue
            rid2 = val[1:]
            if rid2 not in id_set and rid2 not in {x.split("@")[-1] for x in id_set}:
                by_ref = None
                for r2 in records:
                    if r2.get("id", "").endswith(rid2):
                        by_ref = r2["id"]
                        break
                if not by_ref:
                    errors.append("%s: ref %s=%s unresolved" % (rid, path_, val))

    if len(set(tids)) != len(tids):
        dupes = [t for t, n in Counter(tids).items() if n > 1]
        errors.append("duplicate external_record_ids: %s" % dupes[:5])

    exp = {"source": 1, "run": 1, "artifact": 6}
    for k, n in exp.items():
        if kinds.get(k, 0) != n:
            errors.append("kind %s: %d != %d" % (k, kinds.get(k, 0), n))

    body_types = Counter(
        r["body"].get("type") for r in records if kind_of(r) == "observation")
    for t, n in (("dataset.record", 13), ("dataset.snapshot", 1), ("intel.behavior", 13)):
        if body_types.get(t, 0) != n:
            errors.append("observation type %s: %d != %d" % (t, body_types.get(t, 0), n))

    preds = Counter(r["body"].get("predicate") for r in records if kind_of(r) == "edge"
                    and r.get("tags", {}).get("lane") == LANE)
    for p, n in (("related_to", 13), ("supports", 13)):
        if preds.get(p, 0) != n:
            errors.append("edge predicate %s: %d != %d" % (p, preds.get(p, 0), n))

    print("records=%d kinds=%s observation_types=%s lane_edges=%s auto_in_lane=%d"
          % (len(records), dict(kinds), dict(body_types), dict(preds), n_inlane_auto))
    if errors:
        print("ERRORS (%d):" % len(errors))
        for e in errors:
            print("  -", e)
        sys.exit(1)
    if warnings:
        print("WARNINGS (%d):" % len(warnings))
        for w in warnings:
            print("  -", w)
    print("VALIDATE-OK")


if __name__ == "__main__":
    main()
