#!/usr/bin/env python3
"""Independent validator for the swarmtraces-hf-dataset Factum bundle.

Re-derives every number straight from evidence/raw/redacted.jsonl.gz with
its own regexes and counting logic. Never reads the builder's intermediate
structures. Fails loudly on any mismatch.
"""

import gzip
import json
import re
import sys

INPUT = "evidence/raw/redacted.jsonl.gz"
BUNDLE = "data/lanes/swarmtraces-hf-dataset/bundle.json"

fails = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (" | " + str(detail) if detail and not cond else ""))
    if not cond:
        fails.append(name)


def main():
    bundle = json.load(open(BUNDLE))
    recs = bundle["records"]

    # --- envelope ---
    check("envelope.bundle==2", bundle.get("bundle") == 2)
    check("envelope.actor", isinstance(bundle.get("actor"), str) and bundle["actor"])
    check("envelope.idempotency", isinstance(bundle.get("idempotency_key"), str) and bundle["idempotency_key"])
    check("envelope.lane", bundle.get("lane") == "swarmtraces-hf-dataset")

    # --- shape rules ---
    for r in recs:
        ref = r.get("ref", "?")
        tags = r.get("tags", {})
        check("tags.strings.%s" % ref,
              all(isinstance(v, str) for v in tags.values()),
              {k: type(v).__name__ for k, v in tags.items() if not isinstance(v, str)})
        check("tags.lane.%s" % ref, tags.get("lane") == "swarmtraces-hf-dataset")
        if r["kind"] == "observation":
            check("obs.type-in-body.%s" % ref,
                  isinstance(r["body"].get("type"), str) and "type" not in r,
                  "type must live in body")
            check("obs.observed_at.%s" % ref,
                  isinstance(r["body"].get("observed_at"), str) and
                  isinstance(r["body"].get("time_basis"), str))
        if r["kind"] == "claim":
            b = r["body"]
            check("claim.basis.%s" % ref, b.get("basis") == "OBSERVED")
            check("claim.subject-str.%s" % ref, isinstance(b.get("subject"), str))
            check("claim.cites-strs.%s" % ref,
                  isinstance(b.get("cites"), list) and
                  all(isinstance(c, str) for c in b["cites"]) and
                  not any(isinstance(c, dict) for c in b["cites"]))
            check("claim.cites-no-source.%s" % ref,
                  not any(c in ("@src",) for c in b["cites"]))

    # --- independent re-derivation ---
    url_re = re.compile(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&()*+,;=%-]+")
    svc_re = re.compile(r"\[SERVICE \d+ URL \d+\]")
    dst_re = re.compile(r"\[REDACTED:destination(?::\d+)?\]")
    hf_re = re.compile(r"\[HF [^\]]*\]")
    bad = ("[", "REDACTED", "CREDENTIAL", "SERVICE")

    kinds = {}
    parent_of = {}
    ids = set()
    url_recs = {}
    dom_recs = {}
    svc = set()
    dst = set()
    hfs = set()
    art_ids = set()
    art_urls = set()
    zz = set()
    imds = []
    total = 0

    with gzip.open(INPUT, "rt", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            total += 1
            ids.add(r["id"])
            kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
            t = r["text"]
            if r.get("parent_id"):
                parent_of[r["id"]] = r["parent_id"]
            seen = set()
            for m in url_re.finditer(t):
                u = m.group(0).rstrip(".,);")
                if any(x in u for x in bad):
                    continue
                seen.add(u)
            for u in seen:
                url_recs[u] = url_recs.get(u, 0) + 1
                dm = re.match(r"https?://([^/:?#]+)", u)
                if dm:
                    d = dm.group(1).lower()
                    dom_recs[d] = dom_recs.get(d, 0) + 1
                if u.startswith("https://packages.hub.ace-research.openai.org/"):
                    art_ids.add(r["id"])
                    art_urls.add(u)
                    zm = re.search(r"zz[A-Z0-9_]+", u)
                    if zm:
                        zz.add(zm.group(0))
            for m in svc_re.finditer(t):
                svc.add(m.group(0))
            for m in dst_re.finditer(t):
                dst.add(m.group(0))
            for m in hf_re.finditer(t):
                hfs.add(m.group(0)[:80])
            if "169.254.169.254" in t:
                imds.append((r["id"], r["kind"]))

    check("total==189579", total == 189579, total)
    check("kinds", kinds == {"payload": 91037, "response": 23008,
                             "recovered_text": 75534}, kinds)

    # depth
    maxd = 0
    hist = {}
    for rid in parent_of:
        d, cur, seen = 0, rid, set()
        while cur in parent_of and cur not in seen:
            seen.add(cur)
            cur = parent_of[cur]
            d += 1
        hist[d] = hist.get(d, 0) + 1
        maxd = max(maxd, d)
    check("depth.max==1", maxd == 1, maxd)
    check("depth.all-d1", hist == {1: 61125}, hist)
    check("distinct-parents==26248", len(set(parent_of.values())) == 26248)
    check("no-dangling", all(p in ids for p in parent_of.values()))

    check("svc-distinct==4004", len(svc) == 4004, len(svc))
    check("dst-distinct==28087", len(dst) == 28087, len(dst))
    check("hf-distinct==527", len(hfs) == 527, len(hfs))

    check("art-records==1983", len(art_ids) == 1983, len(art_ids))

    # every IOC term in the bundle re-verified
    iocs = [r for r in recs if r["kind"] == "observation"
            and r["body"].get("type") == "infra.ioc"]
    check("ioc-count==37", len(iocs) == 37, len(iocs))
    for r in iocs:
        term = r["body"]["data"]["term"]
        cat = r["body"]["data"]["category"]
        claimed = int(r["tags"]["record_count"])
        if cat == "domain":
            actual = dom_recs.get(term, 0)
        elif cat == "ip":
            actual = len(imds)
        else:
            actual = url_recs.get(term, 0)
        check("ioc.%s" % term[:50], claimed == actual,
              "claimed=%d actual=%d" % (claimed, actual))
        check("ioc.term-nonempty.%s" % term[:40], len(term) > 0)
        check("ioc.status.%s" % term[:40],
              r["body"]["data"].get("status") in
              ("active", "noisy", "retired", "candidate"))

    imds_ids = sorted(i for i, _ in imds)
    check("imds-ids", imds_ids == ["R0189543", "R0189547", "R0189564",
                                   "R0189565", "R0189566"], imds_ids)
    check("imds-all-recovered_text", all(k == "recovered_text" for _, k in imds))

    # snapshot
    snaps = [r for r in recs if r["body"].get("type") == "dataset.snapshot"]
    check("snapshot-count==1", len(snaps) == 1)
    if snaps:
        d = snaps[0]["body"]["data"]
        check("snapshot.row_count", d.get("row_count") == 189579)
        check("snapshot.coverage", d.get("coverage") == "complete")
        check("snapshot.uri", d.get("dataset_uri") ==
              "https://swarmtraces.org/data/final/redacted.jsonl.gz")

    # claims: 5, all OBSERVED, subjects/cites resolve inside bundle
    claims = [r for r in recs if r["kind"] == "claim"]
    check("claims==5", len(claims) == 5, len(claims))
    refs = {r["ref"] for r in recs}
    for r in claims:
        for c in r["body"]["cites"]:
            check("cite-resolves.%s->%s" % (r["ref"], c),
                  c.lstrip("@") in {x.lstrip("@") for x in refs} or
                  c[1:] in refs, c)

    # verbatim spot-checks: terms byte-identical in source
    spot = {
        "https://packages.hub.ace-research.openai.org/artifactory/github-remote-cache/": 3,
        "https://huggingface.co/api/whoami-v2": 3,
        "https://registry-1.docker.io/v2/cybergym/arvo": 2,
    }
    with gzip.open(INPUT, "rt", encoding="utf-8") as fh:
        texts = [json.loads(line)["text"] for line in fh]
    for term, need in spot.items():
        hits = sum(1 for t in texts if term in t)
        check("verbatim.%s" % term[:45], hits >= need, hits)

    print()
    if fails:
        print("VALIDATOR FAILED: %d checks" % len(fails))
        sys.exit(1)
    print("VALIDATOR: all checks passed")


if __name__ == "__main__":
    main()
