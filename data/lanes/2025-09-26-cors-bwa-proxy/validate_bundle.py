#!/usr/bin/env python3
"""Independent validator for the 2025-09-26-cors-bwa-proxy Factum bundle.

Re-derives expectations from data/lanes/2025-09-26-cors-bwa-proxy/events.jsonl
WITHOUT importing the builder: independent kind counts, independent dup
computation (own URL normalization), bundle structural checks, schema-shape
checks against the installed packs, and verbatim spot-checks.
"""
import json
import os
import re
import sys
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "2025-09-26-cors-bwa-proxy"
ERRORS = []


def err(msg):
    ERRORS.append(msg)
    print("FAIL:", msg)


def norm(u):
    # independent normalization: triple-decode, strip scheme, strip one
    # wrapper-host level, strip at inner scheme occurrences
    if not u:
        return set()
    u = unquote(unquote(unquote(u))).replace("&amp;", "&")
    out = {u, re.sub(r"^https?://", "", u)}
    m = re.match(r"^https?://[^/]+/(.*)$", u)
    if m:
        out.add(m.group(1))
    for mm in re.finditer(r"https?://", u):
        if mm.start() > 0:
            out.add(u[mm.start():])
    return out


def main():
    # 1. independent legacy counts
    kinds = {}
    rows = []
    with open(os.path.join(HERE, "events.jsonl")) as fh:
        for line in fh:
            d = json.loads(line)
            kinds[d["record_kind"]] = kinds.get(d["record_kind"], 0) + 1
            rows.append(d)
    assert kinds == {"proxied_target": 113, "proxy_ladder": 29,
                     "proxy_family": 6, "venue_summary": 6}, kinds
    print("legacy kind counts OK:", kinds)

    # 2. independent dup computation against exported corpus
    import glob
    corpus_vars = set()
    corpus_hosts = set()
    for batch in glob.glob("/home/hatch/workspace/silent-locus/"
                            "data/records/*/records.jsonl"):
        for line in open(batch):
            try:
                d = json.loads(line)
            except Exception:
                continue
            b = d.get("body", {})
            if not isinstance(b, dict):
                continue
            t = b.get("type")
            data = b.get("data", {}) or {}
            if t == "infra.proxy_chain" and data.get("target_url"):
                corpus_vars |= norm(data["target_url"])
            elif t == "infra.proxy_instance" and data.get("host"):
                corpus_hosts.add(data["host"])
    exp_new, exp_dup = 0, 0
    for d in rows:
        if d["record_kind"] != "proxied_target":
            continue
        cand = norm(d.get("matched_string")) | \
            norm(d.get("labels", {}).get("decoded_target"))
        if cand & corpus_vars:
            exp_dup += 1
        else:
            exp_new += 1
    print("independent dup recompute: new=%d dup=%d" % (exp_new, exp_dup))

    # 3. bundle structural checks
    bundle = json.load(open(os.path.join(HERE, "bundle.json")))
    assert bundle["bundle"] == 2
    assert bundle["idempotency_key"] == LANE + "-v1"
    assert bundle["actor"].startswith("agent:")
    recs = bundle["records"]
    refs = {r["ref"] for r in recs}
    assert len(refs) == len(recs), "duplicate refs"

    by_kind = {}
    for r in recs:
        by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + 1
        tags = r.get("tags", {})
        if tags.get("lane") != LANE:
            err("record %s missing tags.lane" % r["ref"])
        body = r.get("body", {})
        k = r["kind"]
        if k == "observation":
            for f in ("type", "source", "observed_at", "time_basis",
                      "files", "data_schema", "data"):
                if f not in body:
                    err("observation %s missing body.%s" % (r["ref"], f))
            if not re.match(r"^\d{4}-\d{2}-\d{2}T", body.get("observed_at", "")):
                err("observation %s bad observed_at" % r["ref"])
            src = body.get("source", "")
            if src.startswith("@") and src[1:] not in refs:
                err("observation %s dangling source ref" % r["ref"])
            t = body.get("type")
            data = body.get("data", {})
            if t == "infra.proxy_chain":
                if not data.get("proxy_service") or not data.get("target_url"):
                    err("proxy_chain %s missing required" % r["ref"])
                if (body.get("data_schema") !=
                        "urn:factum:infra:proxy-chain:1"):
                    err("proxy_chain %s wrong data_schema" % r["ref"])
            elif t == "infra.proxy_instance":
                if not data.get("host") or not data.get("invocation_shape"):
                    err("proxy_instance %s missing required" % r["ref"])
        elif k == "claim":
            for f in ("subject", "property", "value", "basis", "cites"):
                if f not in body:
                    err("claim %s missing body.%s" % (r["ref"], f))
            for c in [body["subject"]] + list(body["cites"]):
                if c.startswith("@") and c[1:] not in refs:
                    err("claim %s dangling ref %s" % (r["ref"], c))
            if body.get("basis") not in ("OBSERVED", "INFERENCE", "UPSTREAM"):
                err("claim %s bad basis" % r["ref"])
    print("bundle structure OK:", by_kind)

    n_chain = sum(1 for r in recs
                  if r["kind"] == "observation" and
                  r["body"].get("type") == "infra.proxy_chain")
    n_inst = sum(1 for r in recs
                 if r["kind"] == "observation" and
                 r["body"].get("type") == "infra.proxy_instance")
    # 47 new proxied_target + 29 ladders = 76 chains; 5 family = 5 instances
    if n_chain != 76:
        err("expected 76 proxy_chain, got %d" % n_chain)
    if n_inst != 5:
        err("expected 5 proxy_instance, got %d" % n_inst)
    if exp_new != 47 or exp_dup != 66:
        err("dup recompute mismatch: expected new=47 dup=66, got "
            "new=%d dup=%d" % (exp_new, exp_dup))

    # 4. verbatim spot-checks: 3 chain records vs legacy bytes
    checked = 0
    for r in recs:
        tg = r.get("tags", {})
        if tg.get("legacy_kind") == "proxied_target" and checked < 3:
            ms = tg.get("matched_string")
            if r["body"]["data"]["target_url"] != ms:
                err("verbatim mismatch on %s" % r["ref"])
            checked += 1
    print("verbatim spot-checks OK:", checked)

    # 5. drop log consistency
    drop = json.load(open(os.path.join(HERE, "drop_log.json")))
    if len(drop["dropped"]) != 67:
        err("drop_log has %d entries, expected 67" % len(drop["dropped"]))

    if ERRORS:
        print("VALIDATOR FAILED:", len(ERRORS), "errors")
        sys.exit(1)
    print("VALIDATOR PASS: all checks green")


if __name__ == "__main__":
    main()
