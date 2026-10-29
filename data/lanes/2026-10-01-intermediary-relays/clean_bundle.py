#!/usr/bin/env python3
"""Cleaner for the 2026-10-01-intermediary-relays ingest bundle.

Reads bundle.raw.json (builder output), applies structural fixes WITHOUT
touching raw evidence values (verbatim lines, target URLs, regex terms are
never altered), and writes bundle.json plus a cleaning report.

Fixes applied:
  - every record gets tags.lane = the lane (repair, never silently dropped)
  - observations: observed_at, time_basis, source, files, data_schema present
  - source/run records: required body fields present
  - intra-batch dedup re-check on (type, key) as a safety net
  - rejects placeholder terms / empty required fields (fails loudly)
"""
import json
import os
import sys

LANE = "2026-10-01-intermediary-relays"
REPO = os.path.expanduser("~/workspace/silent-locus")
LDIR = os.path.join(REPO, "data", "lanes", LANE)
IN_BUNDLE = os.path.join(LDIR, "bundle.raw.json")
OUT_BUNDLE = os.path.join(LDIR, "bundle.json")
OUT_REPORT = os.path.join(LDIR, "cleaning_report.json")

SCHEMA_BY_TYPE = {
    "infra.proxy_instance": "urn:factum:infra:proxy-instance:1",
    "infra.proxy_chain": "urn:factum:infra:proxy-chain:1",
    "infra.ioc": "urn:factum:infra:ioc:1",
    "reachability.check": "urn:factum:web:reachability-check:1",
}

PLACEHOLDERS = {"unknown-term", "TBD", "TODO", "placeholder", "N/A", "none",
                "R0000000", "xxx"}


def fail(msg):
    print("CLEANER FAIL:", msg, file=sys.stderr)
    sys.exit(1)


def main():
    with open(IN_BUNDLE, encoding="utf-8") as fh:
        bundle = json.load(fh)
    report = {"fixes": [], "dedup_removed": 0, "records_in": len(bundle["records"])}

    if bundle.get("bundle") != 2:
        fail("bundle version != 2")
    if not bundle.get("actor") or not bundle.get("idempotency_key"):
        fail("missing actor/idempotency_key")

    refs = set()
    seen_keys = {}
    out_records = []
    for r in bundle["records"]:
        kind = r.get("kind")
        ref = r.get("ref")
        body = r.get("body") or {}
        tags = r.get("tags") or {}
        if not ref:
            fail("record missing ref: %s" % json.dumps(r)[:200])
        if ref in refs:
            fail("duplicate ref in bundle: " + ref)
        refs.add(ref)

        # lane tag on EVERY record (repair if missing)
        if tags.get("lane") != LANE:
            report["fixes"].append({"ref": ref, "fix": "tags.lane set to " + LANE})
            tags["lane"] = LANE
        r["tags"] = tags

        if kind == "observation":
            data = body.get("data") or {}
            otype = body.get("type")
            if otype not in SCHEMA_BY_TYPE:
                fail("unknown observation type %r in %s" % (otype, ref))
            if body.get("data_schema") != SCHEMA_BY_TYPE[otype]:
                report["fixes"].append(
                    {"ref": ref, "fix": "data_schema corrected to " + SCHEMA_BY_TYPE[otype]})
                body["data_schema"] = SCHEMA_BY_TYPE[otype]
            for f in ("observed_at", "time_basis", "source", "files", "data"):
                if f not in body or body[f] is None:
                    fail("observation %s missing %s" % (ref, f))
            # required-field content checks per type
            if otype == "infra.proxy_instance":
                for f in ("host", "invocation_shape"):
                    if not data.get(f):
                        fail("proxy_instance %s missing %s" % (ref, f))
                key = ("proxy_instance", data["host"])
            elif otype == "infra.proxy_chain":
                for f in ("proxy_service", "target_url"):
                    if not data.get(f):
                        fail("proxy_chain %s missing %s" % (ref, f))
                if not data.get("chain"):
                    fail("proxy_chain %s has empty chain" % ref)
                key = ("proxy_chain", data["proxy_service"], data["target_url"])
            elif otype == "infra.ioc":
                if not data.get("term") or not data.get("category"):
                    fail("ioc %s missing term/category" % ref)
                if data["term"] in PLACEHOLDERS or data["term"].startswith("R000"):
                    fail("ioc %s has placeholder term" % ref)
                key = ("ioc", data["term"])
            elif otype == "reachability.check":
                for f in ("target", "method", "outcome"):
                    if not data.get(f):
                        fail("reachability %s missing %s" % (ref, f))
                key = ("reachability", data["target"], data["method"])
            if key in seen_keys:
                report["dedup_removed"] += 1
                report["fixes"].append(
                    {"ref": ref, "fix": "intra-batch duplicate of " + seen_keys[key] + "; removed"})
                continue
            seen_keys[key] = ref
            # no 1970 placeholder timestamps
            if str(body.get("observed_at", "")).startswith("1970-01-01"):
                fail("observation %s has 1970 placeholder observed_at" % ref)
        elif kind == "source":
            if not (body.get("locator") and body.get("source_type")):
                fail("source %s missing locator/source_type" % ref)
        elif kind == "run":
            if not body.get("run_kind"):
                fail("run %s missing run_kind" % ref)
        else:
            fail("unexpected kind %r in %s" % (kind, ref))
        out_records.append(r)

    # bundle-local reference integrity
    for r in out_records:
        body = r.get("body") or {}
        for fld in ("source", "run"):
            v = body.get(fld)
            if isinstance(v, str) and v.startswith("@") and v[1:] not in refs:
                fail("dangling %s reference %s in %s" % (fld, v, r["ref"]))

    bundle["records"] = out_records
    report["records_out"] = len(out_records)
    with open(OUT_BUNDLE, "w", encoding="utf-8") as fh:
        json.dump(bundle, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    with open(OUT_REPORT, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("cleaner: %d -> %d records, %d fixes, %d dedup removals" % (
        report["records_in"], report["records_out"],
        len(report["fixes"]), report["dedup_removed"]))
    print("wrote", OUT_BUNDLE)


if __name__ == "__main__":
    main()
