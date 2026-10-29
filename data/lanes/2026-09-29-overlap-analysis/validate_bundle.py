#!/usr/bin/env python3
"""Independent validator for the 2026-09-29-overlap-analysis bundle."""
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "2026-09-29-overlap-analysis"
ERRORS = []


def err(msg):
    ERRORS.append(msg)
    print("FAIL:", msg)


def main():
    # independent re-derivation
    seen = {}
    paste = []
    kinds = Counter()
    with open(os.path.join(HERE, "events.jsonl")) as fh:
        for line in fh:
            d = json.loads(line)
            kinds[d["record_kind"]] += 1
            if d["record_kind"] == "overlap_match":
                if d["fingerprint"] not in seen:
                    seen[d["fingerprint"]] = d
            else:
                paste.append(d)
    assert kinds == {"overlap_match": 17038, "paste_link": 317}, kinds
    assert len(seen) == 7982, len(seen)
    print("legacy OK: 17038 rows -> 7982 unique; 317 paste_link rows")

    bundle = json.load(open(os.path.join(HERE, "bundle.json")))
    assert bundle["bundle"] == 2
    assert bundle["idempotency_key"] == LANE + "-v1"
    recs = bundle["records"]
    refs = {r["ref"] for r in recs}
    assert len(refs) == len(recs)

    iocs = [r for r in recs if r["kind"] == "observation"]
    claims = [r for r in recs if r["kind"] == "claim"]
    if len(iocs) != 15:
        err("expected 15 iocs, got %d" % len(iocs))
    terms = [r["body"]["data"]["term"] for r in iocs]
    if len(set(terms)) != 15:
        err("ioc terms not unique")
    for must in ("httpbun.com", "OTS92", "G236",
                 "packages.hub.ace-research.openai.org"):
        if must not in terms:
            err("missing expected ioc %s" % must)
    if "github-remote-cache/zz" in terms:
        err("github-remote-cache/zz should be skipped (already in corpus)")
    for r in iocs:
        data = r["body"]["data"]
        if not data.get("term") or not data.get("category"):
            err("ioc %s missing required" % r["ref"])
        if data.get("status") != "active":
            err("ioc %s status != active" % r["ref"])
        if r.get("tags", {}).get("lane") != LANE:
            err("ioc %s missing tags.lane" % r["ref"])
    print("iocs OK: 15")

    if len(claims) != 8:
        err("expected 8 claims, got %d" % len(claims))
    for r in claims:
        body = r["body"]
        for f in ("subject", "property", "value", "basis", "cites"):
            if f not in body:
                err("claim %s missing %s" % (r["ref"], f))
        if body["subject"] != "@run" or body["cites"] != ["@run"]:
            err("claim %s must cite the run record" % r["ref"])
    cov = next(c for c in claims
               if c["body"]["property"] == "overlap_coverage")
    if cov["body"]["value"]["unique_matches"] != 7982:
        err("coverage claim unique_matches wrong")
    print("claims OK: 8")

    print("bundle OK: %d records" % len(recs))
    if ERRORS:
        print("VALIDATOR FAILED")
        sys.exit(1)
    print("VALIDATOR PASS")


if __name__ == "__main__":
    main()
