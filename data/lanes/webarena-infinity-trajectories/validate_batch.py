#!/usr/bin/env python3
"""Validate the exported webarena-infinity factum batch directly (no DB locks).

Usage: validate_batch.py data/records/<batch>/records.jsonl

Independent re-derivation checks:
- every line parses; record has id, record_kind, body, tags, fingerprint
- tags.lane == webarena-infinity-trajectories on every bundle-authored record
  (toolkit-auto in_lane edges carry no tags by design; counted separately)
- observations have observed_at + time_basis + type + data
- every declared reference target (edge subject/object, observation
  source/run/data.snapshot/files[].artifact, claim cites) exists in the
  batch; no dangling references
- counts: source==1, run==1, dataset.record==2195, dataset.snapshot==1,
  related_to edges==2195, supports edges==25
- external_record_id unique; sha256 present on every dataset.record
"""
import json
import re
import sys
from collections import Counter

LANE = "webarena-infinity-trajectories"
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
    obs_types = Counter()
    ext_ids = []
    traj_edge_targets = set()
    sup_edges = 0
    for r in records:
        k = kind_of(r)
        kinds[k] += 1
        rid = r.get("id", "?")
        if not ID_RE.match(rid or ""):
            errors.append("%s: bad id format" % rid)
        body = r.get("body") or {}
        tags = r.get("tags") or {}
        if not r.get("fingerprint"):
            errors.append("%s: missing fingerprint" % rid)
        if k == "observation":
            t = body.get("type", "")
            obs_types[t] += 1
            if not body.get("observed_at") or not body.get("time_basis"):
                errors.append("%s (%s): missing observed_at/time_basis" % (rid, t))
            if not body.get("data"):
                errors.append("%s (%s): missing data" % (rid, t))
            if t == "dataset.record":
                ext_ids.append((body.get("data") or {}).get("external_record_id"))
                if not tags.get("sha256"):
                    errors.append("%s: dataset.record missing sha256 tag" % rid)
                if not tags.get("raw_path"):
                    errors.append("%s: dataset.record missing raw_path tag" % rid)
            if t == "intel.behavior":
                if tags.get("finding_id") == "RB-008":
                    rb8_body = json.dumps(r)
                    if re.search(r"ak-[A-Za-z0-9]{10,}", rb8_body):
                        errors.append("%s: possible token value in RB-008 record" % rid)
        if k == "edge":
            pred = body.get("predicate")
            if pred == "related_to" and body.get("subject", "").endswith("_webarena") is False:
                traj_edge_targets.add(body.get("object"))
            if pred == "supports":
                sup_edges += 1
        if tags.get("lane") != LANE:
            if k == "edge" and body.get("predicate") == "in_lane" and not tags.get("lane"):
                n_inlane_auto += 1  # toolkit-auto in_lane edges carry only
                                    # factum.author, no lane tag
            else:
                errors.append("%s (%s): tags.lane != %s (tags=%s)" % (rid, k, LANE, tags))

    if len(set(ext_ids)) != len(ext_ids):
        dupes = [x for x, n in Counter(ext_ids).items() if n > 1]
        errors.append("duplicate external_record_id: %s" % dupes[:5])
    if len(ext_ids) != 2195:
        errors.append("dataset.record count %d != 2195" % len(ext_ids))
    if kinds.get("source") != 1:
        errors.append("source count %s != 1" % kinds.get("source"))
    if kinds.get("run") != 1:
        errors.append("run count %s != 1" % kinds.get("run"))
    if obs_types.get("dataset.snapshot") != 1:
        errors.append("dataset.snapshot count != 1: %s" % obs_types.get("dataset.snapshot"))
    if obs_types.get("intel.behavior") != 21:
        errors.append("intel.behavior count != 21: %s" % obs_types.get("intel.behavior"))
    if sup_edges != 25:
        errors.append("supports edges %d != 25" % sup_edges)
    n_related = sum(1 for r in records
                    if kind_of(r) == "edge" and (r.get("body") or {}).get("predicate") == "related_to")
    if n_related != 2195:
        errors.append("related_to edges %d != 2195" % n_related)

    for r in records:
        for path_, v in ref_targets(r):
            if v is None:
                continue
            if v.startswith("lane_"):
                continue  # lane record lives in the corpus (lane new), not the batch
            if v not in id_set:
                errors.append("%s: dangling ref %s=%s" % (r.get("id"), path_, v))

    print("records:", len(records))
    print("kinds:", dict(kinds))
    print("obs_types:", dict(obs_types))
    print("toolkit-auto in_lane edges (untagged):", n_inlane_auto)
    print("warnings:", len(warnings))
    for w in warnings[:20]:
        print("WARN:", w)
    if errors:
        print("ERRORS:", len(errors))
        for e in errors[:40]:
            print("ERR:", e)
        sys.exit(2)
    print("VALIDATE-OK")


if __name__ == "__main__":
    main()
