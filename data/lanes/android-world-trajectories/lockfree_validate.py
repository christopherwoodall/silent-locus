#!/usr/bin/env python3
"""Lock-free full validation of the Android-World bundle against factum schemas.

Replicates the add path (add_bundle in store.py) without the writer lock:
  - CORE bundle envelope schema on the submitted bundle
  - per record: deepcopy body, assign(kind, body)  [fills data_schema],
    validate_body(kind, body)                      [body + per-type data]
Collects ALL errors instead of failing fast, so one run surfaces every
remaining schema blocker before the next lock acquisition.
"""
import copy
import json
import os
import sys

REPO = os.path.expanduser("~/workspace/silent-locus")
HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLE = os.path.join(HERE, "bundle-android-world.json")
sys.path.insert(0, os.path.join(REPO, "skills", "factum", "scripts"))

from factum_lib.store import State  # noqa: E402
from factum_lib.schemas import Catalog, CORE  # noqa: E402


def main():
    state = State(REPO)
    state.lock = state.json("data/schema-lock.json")
    state.catalog = Catalog(state.read, state.lock)
    catalog = state.catalog

    errors = []
    with open(BUNDLE) as f:
        submitted = json.load(f)
    try:
        catalog.validate(CORE["bundle"], submitted)
    except Exception as e:  # noqa: BLE001
        errors.append("envelope: %s: %s" % (type(e).__name__, e))

    # Replicate add_bundle ref registration + resolution.
    from factum_lib.store import new_id  # noqa: E402

    ids = {}
    for entry in submitted["records"]:
        if "ref" in entry:
            if entry["ref"] in ids:
                errors.append("DUPLICATE_REF: %s" % entry["ref"])
            ids[entry["ref"]] = new_id(entry["kind"])

    def resolve(value, kinds):
        if isinstance(value, str) and value.startswith("@"):
            name = value[1:]
            if name not in ids:
                raise ValueError("UNKNOWN_REF: %s" % value)
            return ids[name]
        return value

    n = 0
    for entry in submitted["records"]:
        n += 1
        kind = entry["kind"]
        ref = entry.get("ref", "?")
        body = copy.deepcopy(entry["body"])
        try:
            if kind == "observation":
                body.setdefault("files", [])
            catalog.assign(kind, body)
            catalog.body_references(kind, body, resolve)
            catalog.validate_body(kind, body)
        except Exception as e:  # noqa: BLE001
            errors.append("%s (%s): %s: %s" % (ref, kind, type(e).__name__, e))

    print("records checked: %d" % n)
    if errors:
        print("ERRORS (%d):" % len(errors))
        for e in errors[:20]:
            print("  - %s" % e)
        sys.exit(1)
    print("STORE-VALIDATE-OK")


if __name__ == "__main__":
    main()
