#!/usr/bin/env python3
"""Fix dataset.snapshot observation data to fit urn:factum:datasets:snapshot:1.

Submit blocker found 2026-10-17: the snapshot data carried
  coverage: "116 tasks x 4 rollouts (full corpus)"   (not in the enum)
  license:  "mit"                                    (additionalProperties: false)
The schema allows only dataset_uri, revision, coverage (enum
complete/partial/metadata_only/unknown), row_count.

Repair (no values lost, semantics preserved):
  data.coverage = "complete"   (full-corpus snapshot: 464/464 files)
  tags["coverage_detail"] = "116 tasks x 4 rollouts (full corpus)"
  drop data.license            (already in the source record's tags and
                                raw/LICENSE.note)

Writes via unique tmp name + atomic rename; prints before/after sha256.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLE = os.path.join(HERE, "bundle-android-world.json")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
        return h.hexdigest()


def main():
    before = sha256(BUNDLE)
    with open(BUNDLE) as f:
        bundle = json.load(f)
    snaps = [r for r in bundle["records"]
             if r.get("kind") == "observation"
             and r["body"].get("type") == "dataset.snapshot"]
    if len(snaps) != 1:
        print("expected exactly 1 dataset.snapshot, found %d" % len(snaps))
        sys.exit(2)
    snap = snaps[0]
    data = snap["body"]["data"]
    detail = data.get("coverage")
    assert data.get("license") == "mit", data
    snap.setdefault("tags", {})["coverage_detail"] = detail
    data["coverage"] = "complete"
    del data["license"]
    tmp = "%s.fix-%d.tmp" % (BUNDLE, os.getpid())
    with open(tmp, "w") as f:
        json.dump(bundle, f, indent=1)
        f.write("\n")
    os.rename(tmp, BUNDLE)
    print("snapshot fixed: coverage='complete', coverage_detail moved to tags, "
          "license dropped from data (kept in source tags + raw/LICENSE.note)")
    print("sha256 before: %s" % before)
    print("sha256 after:  %s" % sha256(BUNDLE))


if __name__ == "__main__":
    main()
