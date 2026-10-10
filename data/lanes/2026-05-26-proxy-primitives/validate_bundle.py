#!/usr/bin/env python3
"""Independent validator for the 2026-05-26-proxy-primitives Factum bundle.

Re-derives expectations from events.jsonl without importing the builder:
independent kind counts, independent dup-set recomputation (own URL
normalization over exported corpus batches, matched by legacy fingerprint),
bundle structural checks, and verbatim spot-checks.
"""
import glob
import json
import os
import re
import sys
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "2026-05-26-proxy-primitives"
ERRORS = []


def err(msg):
    ERRORS.append(msg)
    print("FAIL:", msg)


def variants(u):
    # independent re-implementation of the builder's normalization contract
    if not u:
        return set()
    for _ in range(3):
        u = unquote(u)
    u = u.replace("&amp;", "&")
    out = {u, re.sub(r"^https?://", "", u, flags=re.I)}
    m = re.match(r"^https?://[^/]+/(.*)$", u, flags=re.I)
    if m:
        out.add(m.group(1))
        out.add(re.sub(r"^https?://", "", m.group(1), flags=re.I))
    for mm in re.finditer(r"https?://", u, flags=re.I):
        if mm.start() > 0:
            out.add(u[mm.start():])
            out.add(re.sub(r"^https?://", "", u[mm.start():], flags=re.I))
    return {x for x in out if x}


def classify_url(ms):
    if not ms:
        return ("empty", None, None)
    if ms.startswith("[operational URL omitted"):
        return ("withheld", ms, None)
    clean = re.sub(r"^[\[\(]+", "", ms.strip())
    m = re.search(r"https?://[^\s'\"\]]+", clean)
    if m:
        return ("url", m.group(0), None)
    return ("other", ms, None)


def main():
    kinds = {}
    rows = []
    with open(os.path.join(HERE, "events.jsonl")) as fh:
        for line in fh:
            d = json.loads(line)
            kinds[d["record_kind"]] = kinds.get(d["record_kind"], 0) + 1
            rows.append(d)
    expected_kinds = {"wiki_link": 553, "wiki_record_annotation": 128,
                      "corpus_hit": 3, "wiki_ioc_pivot": 827,
                      "wiki_shortener": 4, "wiki_revision": 1,
                      "gem_name_fragment": 6}
    assert kinds == expected_kinds, kinds
    print("legacy kind counts OK")

    # independent corpus scan
    corpus_vars = set()
    corpus_ioc = set()
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
                corpus_vars |= variants(data["target_url"])
            elif t == "infra.ioc" and data.get("term"):
                corpus_ioc.add(data["term"])

    # independent dup-set recomputation, keyed by legacy fingerprint.
    # Only 'url'-kind rows can be corpus dupes; withheld/hostfrag/other
    # rows become proxy_instance records and are never dupes.
    exp_dup_fps = set()
    exp_terms = set()
    for d in rows:
        kind = d["record_kind"]
        fp = d["fingerprint"]
        ms = d.get("matched_string")
        urlkind, clean_url, _ = classify_url(ms)
        if kind in ("wiki_link", "wiki_record_annotation", "wiki_shortener",
                    "wiki_ioc_pivot"):
            if urlkind == "url" and \
                    any(v in corpus_vars for v in variants(clean_url)):
                exp_dup_fps.add(fp)
        elif kind == "corpus_hit":
            if ms in corpus_ioc or \
                    any(v in corpus_vars for v in variants(ms)):
                exp_dup_fps.add(fp)
        elif kind == "gem_name_fragment":
            if ms in exp_terms:
                exp_dup_fps.add(fp)  # batch-duplicate
            else:
                exp_terms.add(ms)
                if ms in corpus_ioc:
                    exp_dup_fps.add(fp)
    print("independent dup recompute: %d dup fingerprints" % len(exp_dup_fps))

    bundle = json.load(open(os.path.join(HERE, "bundle.json")))
    assert bundle["bundle"] == 2
    assert bundle["idempotency_key"] == LANE + "-v1"
    recs = bundle["records"]
    refs = {r["ref"] for r in recs}
    assert len(refs) == len(recs), "duplicate refs"

    by_type = {}
    for r in recs:
        by_type[r["kind"]] = by_type.get(r["kind"], 0) + 1
        if r.get("tags", {}).get("lane") != LANE:
            err("record %s missing tags.lane" % r["ref"])
        body = r.get("body", {})
        if r["kind"] == "observation":
            for f in ("type", "source", "observed_at", "time_basis",
                      "files", "data_schema", "data"):
                if f not in body:
                    err("observation %s missing body.%s" % (r["ref"], f))
            if not re.match(r"^\d{4}-\d{2}-\d{2}T",
                            body.get("observed_at", "")):
                err("observation %s bad observed_at" % r["ref"])
            t = body["type"]
            data = body["data"]
            if t == "infra.proxy_chain":
                if not data.get("proxy_service") or not data.get("target_url"):
                    err("chain %s missing required" % r["ref"])
            elif t == "infra.proxy_instance":
                if not data.get("host") or not data.get("invocation_shape"):
                    err("instance %s missing required" % r["ref"])
            elif t == "infra.ioc":
                if not data.get("term") or not data.get("category"):
                    err("ioc %s missing required" % r["ref"])
                if data.get("status") not in ("active", "noisy", "retired",
                                              "candidate"):
                    err("ioc %s bad status" % r["ref"])
            for v in r["tags"].values():
                if not isinstance(v, str):
                    err("record %s has non-string tag" % r["ref"])
                    break
        elif r["kind"] == "claim":
            for f in ("subject", "property", "value", "basis", "cites"):
                if f not in body:
                    err("claim %s missing %s" % (r["ref"], f))
    print("bundle structure OK:", by_type)

    # drop-log cross-check: every dropped fp must be in the independent set
    # and vice versa (exact set equality)
    drop = json.load(open(os.path.join(HERE, "drop_log.json")))
    drop_fps = {e["legacy_fingerprint"] for e in drop["dropped"]
                if e.get("legacy_fingerprint")}
    # batch-duplicate gemfrag rows share fingerprints? no - distinct rows
    if drop_fps != exp_dup_fps:
        only_drop = drop_fps - exp_dup_fps
        only_exp = exp_dup_fps - drop_fps
        err("dup-set mismatch: only in drop_log=%d, only in recompute=%d"
            % (len(only_drop), len(only_exp)))

    # type-count cross-check + proxy_service sanity
    n_chain = n_inst = n_ioc = 0
    for r in recs:
        if r["kind"] != "observation":
            continue
        t = r["body"].get("type")
        if t == "infra.proxy_chain":
            n_chain += 1
            ps = r["body"]["data"].get("proxy_service", "")
            if any(c in ps for c in ("[", " ", "&", ";")) or \
                    ps.endswith(".") or not ps:
                err("garbage proxy_service on %s: %r" % (r["ref"], ps[:60]))
        elif t == "infra.proxy_instance":
            n_inst += 1
        elif t == "infra.ioc":
            n_ioc += 1
    print("type counts: chain=%d instance=%d ioc=%d"
          % (n_chain, n_inst, n_ioc))

    # verbatim spot-checks on 5 chain records: target_url == decoded
    # cleaned matched_string
    checked = 0
    for r in recs:
        if r["kind"] == "observation" and \
                r["body"].get("type") == "infra.proxy_chain" and checked < 5:
            tg = r["tags"]
            urlkind, clean_url, _ = classify_url(tg.get("matched_string"))
            if urlkind != "url":
                err("chain %s has non-url matched_string" % r["ref"])
                continue
            dec = clean_url
            for _ in range(3):
                dec = unquote(dec)
            dec = dec.replace("&amp;", "&")
            if r["body"]["data"]["target_url"] != dec:
                err("verbatim mismatch on %s" % r["ref"])
            checked += 1
    print("verbatim spot-checks OK:", checked)

    if ERRORS:
        print("VALIDATOR FAILED:", len(ERRORS))
        sys.exit(1)
    print("VALIDATOR PASS")


if __name__ == "__main__":
    main()
