#!/usr/bin/env python3
"""Fix observed_at date-only values in the Android-World bundle.

Submit blocker found 2026-10-17: factum's add rejected the bundle with
SCHEMA / observed_at validation failed (format). All 488 observation bodies
carry "observed_at": "2026-10-17" (bare date); the core observation schema
requires "format": "date-time". Every observation has time_basis
"collector_clock" (the collector's own clock: ingest day), so the minimal
format-only repair is "2026-10-17" -> "2026-10-17T00:00:00Z" (midnight UTC
of the ingest day). No evidence value changes; semantic preserved.

Rewrites only observation bodies' observed_at; writes via unique tmp name +
atomic rename; prints before/after sha256 for provenance.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLE = os.path.join(HERE, "bundle-android-world.json")
BARE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATETIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")


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
    changed = 0
    unexpected = []
    for r in bundle["records"]:
        if r.get("kind") != "observation":
            continue
        oa = r["body"].get("observed_at")
        if oa is None:
            continue
        if BARE_DATE.match(oa):
            r["body"]["observed_at"] = oa + "T00:00:00Z"
            changed += 1
        elif not DATETIME.match(oa):
            unexpected.append((r.get("ref"), oa))
    if unexpected:
        print("UNEXPECTED observed_at values (not bare date, not datetime):")
        for ref, oa in unexpected:
            print("  %s: %r" % (ref, oa))
        sys.exit(2)
    tmp = "%s.fix-%d.tmp" % (BUNDLE, os.getpid())
    with open(tmp, "w") as f:
        json.dump(bundle, f, indent=1)
        f.write("\n")
    os.rename(tmp, BUNDLE)
    after = sha256(BUNDLE)
    print("observations repaired: %d" % changed)
    print("sha256 before: %s" % before)
    print("sha256 after:  %s" % after)


if __name__ == "__main__":
    main()
