#!/usr/bin/env python3
"""Independent validator for the 2026-09-28-gem83-reconciliation bundle."""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "2026-09-28-gem83-reconciliation"
ERRORS = []


def err(msg):
    ERRORS.append(msg)
    print("FAIL:", msg)


def main():
    names, versions, xrays = set(), {}, {}
    n = 0
    with open(os.path.join(HERE, "events.jsonl")) as fh:
        for line in fh:
            d = json.loads(line)
            assert d["record_kind"] == "gem_reconciliation"
            n += 1
            L = d["labels"]
            names.add(L["gem.package"])
            versions[L["gem.package"]] = L.get("gem.versions")
            xrays[L["gem.package"]] = L.get("gem.xray_id")
    assert n == 83, n
    assert len(names) == 83, "gem names not unique"
    print("legacy: 83 rows, 83 unique gem names OK")

    bundle = json.load(open(os.path.join(HERE, "bundle.json")))
    assert bundle["bundle"] == 2
    assert bundle["idempotency_key"] == LANE + "-v1"
    recs = bundle["records"]
    refs = {r["ref"] for r in recs}
    assert len(refs) == len(recs)

    pkgs = [r for r in recs
            if r["kind"] == "observation" and
            r["body"].get("type") == "infra.package"]
    if len(pkgs) != 83:
        err("expected 83 infra.package, got %d" % len(pkgs))
    got_names = set()
    for r in pkgs:
        data = r["body"]["data"]
        if not data.get("name"):
            err("package %s missing name" % r["ref"])
        got_names.add(data["name"])
        if data.get("ecosystem") != "rubygems":
            err("package %s wrong ecosystem" % r["ref"])
        if not isinstance(data.get("versions"), list):
            err("package %s versions not a list" % r["ref"])
        if r["body"].get("data_schema") != "urn:factum:infra:package:1":
            err("package %s wrong data_schema" % r["ref"])
        if r["body"].get("observed_at") != "2026-06-18T00:00:00Z":
            err("package %s wrong observed_at" % r["ref"])
        if r.get("tags", {}).get("lane") != LANE:
            err("package %s missing tags.lane" % r["ref"])
        # verbatim: name matches legacy exactly
        if data["name"] not in names:
            err("package %s name not in legacy set" % r["ref"])
    if got_names != names:
        err("name set mismatch: missing=%d extra=%d"
            % (len(names - got_names), len(got_names - names)))

    # spot-check xray/version passthrough on 5
    checked = 0
    for r in pkgs:
        if checked >= 5:
            break
        nm = r["body"]["data"]["name"]
        if r["body"]["data"].get("xray_id") != xrays[nm]:
            err("xray mismatch on %s" % nm)
        exp_v = [versions[nm]] if versions[nm] else []
        if r["body"]["data"].get("versions") != exp_v:
            err("versions mismatch on %s" % nm)
        checked += 1
    print("spot-checks OK:", checked)

    # the overlap claim must exist and name the other lane
    claims = [r for r in recs if r["kind"] == "claim"]
    if not any("2026-09-29-gem-temporal-pivot" in json.dumps(c["body"])
               for c in claims):
        err("missing corpus_overlap claim")
    print("bundle OK: %d records (%d pkg, %d claims)"
          % (len(recs), len(pkgs), len(claims)))

    if ERRORS:
        print("VALIDATOR FAILED")
        sys.exit(1)
    print("VALIDATOR PASS")


if __name__ == "__main__":
    main()
