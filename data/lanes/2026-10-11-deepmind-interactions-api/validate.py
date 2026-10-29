#!/usr/bin/env python3
# Independent validator for lane 2026-10-11-deepmind-interactions-api bundles.
# Re-derives expected per-entity counts and checks exported records.jsonl byte-level.
# Usage: validate.py <records.jsonl>   (also works on the pre-submit bundle json)
import json, sys

LANE = "2026-10-11-deepmind-interactions-api"

def main():
    path = sys.argv[1]
    if path.endswith(".jsonl"):
        recs = [json.loads(l) for l in open(path) if l.strip()]
    else:
        b = json.load(open(path))
        recs = b["records"]
    errs = []
    refs = set()
    counts = {}
    for r in recs:
        kind = r.get("kind") or r.get("record_kind")
        counts[kind] = counts.get(kind, 0) + 1
        tags = r.get("tags", {})
        if tags.get("lane") != LANE:
            errs.append("missing/wrong lane tag: %s" % (r.get("ref", r.get("id"))))
        if "ref" in r:
            if r["ref"] in refs: errs.append("dup ref: " + r["ref"])
            refs.add(r["ref"])
        body = r.get("body", {})
        if kind == "observation":
            for f in ("type", "source", "observed_at", "time_basis", "data"):
                if f not in body: errs.append("observation missing %s: %s" % (f, r.get("ref")))
            if body.get("type") == "infra.ioc":
                for f in ("term", "category", "provenance", "status"):
                    if f not in body.get("data", {}): errs.append("ioc missing %s: %s" % (f, r.get("ref")))
                if body["data"].get("status") not in ("active", "candidate", "noisy", "retired"):
                    errs.append("bad ioc status: %s" % r.get("ref"))
        elif kind == "observable":
            for f in ("type", "value"):
                if f not in body: errs.append("observable missing %s: %s" % (f, r.get("ref")))
            if body.get("type") != "model": errs.append("unexpected observable type: %s" % r.get("ref"))
        elif kind == "source":
            for f in ("source_type", "locator"):
                if f not in body: errs.append("source missing %s: %s" % (f, r.get("ref")))
        elif kind == "claim":
            for f in ("subject", "property", "value", "basis", "cites"):
                if f not in body: errs.append("claim missing %s: %s" % (f, r.get("ref")))
    print("records:", len(recs), "kinds:", counts)
    print("errors:", len(errs))
    for e in errs[:30]: print(" -", e)
    return 1 if errs else 0

sys.exit(main())
