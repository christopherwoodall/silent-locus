#!/usr/bin/env python3
"""Independent validator for the swe-agent-nebius factum batch.

Re-derives every check from the ORIGINAL inputs (verified-findings.json,
adversarial-kills.json, raw/MANIFEST.json, local parquet bytes) — never
from the builder's own structures. Validates the exported batch
(data/records/<batch>/records.jsonl) OR the pre-submit bundle file.

Usage: validate_batch.py <records.jsonl-or-bundle.json>
Exit 0 = all checks pass; non-zero = first failure (message on stderr).
"""
import json
import os
import re
import sys
import hashlib

LANE = "swe-agent-nebius-trajectories"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
WORKING = os.path.join(HERE, "working")


def fail(msg):
    print("VALIDATE-FAIL:", msg, file=sys.stderr)
    sys.exit(1)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_records(path):
    txt = open(path).read()
    data = json.loads(txt)
    if isinstance(data, dict) and data.get("bundle") == 2:
        return data["records"]            # pre-submit bundle file
    return [json.loads(line) for line in txt.splitlines() if line.strip()]


def main():
    if len(sys.argv) != 2:
        fail("usage: validate_batch.py <records.jsonl-or-bundle.json>")
    records = load_records(sys.argv[1])
    print("records:", len(records))

    findings = json.load(open(os.path.join(WORKING, "verified-findings.json")))["findings"]
    kills = json.load(open(os.path.join(WORKING, "adversarial-kills.json")))
    manifest = json.load(open(os.path.join(RAW, "MANIFEST.json")))
    kill_ids = {k["id"] for k in kills["adversarial_kills"] + kills["verification_kills"]}

    # ---- 1. every record carries the lane tag ----
    for r in records:
        if r.get("tags", {}).get("lane") != LANE:
            fail("record missing tags.lane: %s" % r.get("ref"))

    # ---- 2. record kind census ----
    kinds = {}
    for r in records:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    expect = {"source": 1, "run": 1, "observation": 14 + 15 + 15 + 1,
              "artifact": 3, "edge": 14 + 15 + 15}
    if kinds != expect:
        fail("kind census %s != %s" % (kinds, expect))

    def obs_of(otype):
        return [r for r in records
                if r["kind"] == "observation" and r["body"].get("type") == otype]

    # ---- 3. finding ids: exactly the 15 survivors, no kills ----
    behaviors = obs_of("intel.behavior")
    fids = sorted(r["tags"]["finding_id"] for r in behaviors)
    expect_ids = sorted(f["id"] for f in findings)
    if fids != expect_ids:
        fail("behavior finding ids %s != %s" % (fids, expect_ids))
    if set(fids) & kill_ids:
        fail("killed id present in behavior records: %s" % (set(fids) & kill_ids))

    # ---- 4. trajectory records: 14 distinct (file, row_index) anchors ----
    trajrecs = obs_of("dataset.record")
    anchors = sorted((r["tags"]["file"], int(r["tags"]["row_index"]))
                     for r in trajrecs)
    expect_anchors = sorted({(f["file"], f["row_index"]) for f in findings})
    if anchors != expect_anchors:
        fail("trajectory anchors %s != %s" % (anchors, expect_anchors))
    for r in trajrecs:
        f = next(x for x in findings
                 if x["file"] == r["tags"]["file"]
                 and x["row_index"] == int(r["tags"]["row_index"]))
        for k in ("instance_id", "model_name", "target", "exit_status"):
            if r["tags"][k] != str(f[k]):
                fail("traj %s tag %s=%s != finding %s"
                     % (r["tags"]["row_index"], k, r["tags"][k], f[k]))
        if "anchor_note" not in r["tags"]:
            fail("traj record missing anchor_note")

    # ---- 5. tool sequences: 15, length == len(steps), blocks match quote ----
    tseqs = obs_of("behavior.tool_sequence")
    if len(tseqs) != 15:
        fail("tool_sequence count %d != 15" % len(tseqs))
    fence = re.compile(r"```\n?(.*?)```", re.DOTALL)
    for r in tseqs:
        d = r["body"]["data"]
        if d["length"] != len(d["steps"]):
            fail("toolseq %s length %d != steps %d"
                 % (r["tags"]["finding_id"], d["length"], len(d["steps"])))
        if not d["steps"]:
            fail("toolseq %s has zero steps" % r["tags"]["finding_id"])
        f = next(x for x in findings if x["id"] == r["tags"]["finding_id"])
        blocks = [m.group(1).strip("\n") for m in fence.finditer(f["verbatim_quote"])]
        blocks = [b for b in blocks if b.strip()]
        got_cmds = [s["command"] for s in d["steps"]]
        if got_cmds != blocks:
            fail("toolseq %s steps != quote code blocks" % f["id"])
        if d["model"] != f["model_name"]:
            fail("toolseq %s model mismatch" % f["id"])

    # ---- 6. verbatim bodies: quotes byte-identical to source ----
    for r in behaviors:
        f = next(x for x in findings if x["id"] == r["tags"]["finding_id"])
        q = r["tags"]["evidence_quote"]
        if f["verbatim_quote"][:2000] != q:
            fail("finding %s quote drift vs verified-findings.json" % f["id"])
        if f["behavior"] not in r["body"]["data"]["description"]:
            fail("finding %s behavior text missing from description" % f["id"])

    # ---- 7. artifacts: sha256 matches local bytes AND manifest ----
    arts = [r for r in records if r["kind"] == "artifact"]
    if len(arts) != 3:
        fail("artifact count %d != 3" % len(arts))
    for a in arts:
        name = a["tags"]["filename"]
        local = os.path.join(RAW, name)
        if sha256_file(local) != a["body"]["sha256"]:
            fail("artifact %s sha256 != local bytes" % name)
        ment = next(e for e in manifest["files"] if e["filename"] == name)
        if ment["sha256"] != a["body"]["sha256"]:
            fail("artifact %s sha256 != manifest" % name)
        if a["body"]["size"] != ment["size_bytes"]:
            fail("artifact %s size != manifest" % name)
        if a["tags"].get("storage") != "local":
            fail("artifact %s must be storage=local (raw is gitignored)" % name)

    # ---- 8. edges: 14 run edges + 15 finding edges + 15 toolseq edges ----
    edges = [r for r in records if r["kind"] == "edge"]
    preds = {}
    for e in edges:
        p = e["body"]["predicate"]
        preds[p] = preds.get(p, 0) + 1
        subj, obj = e["body"]["subject"], e["body"]["object"]
        if not (subj.startswith("@") and obj.startswith("@")):
            fail("edge %s has non-ref subject/object" % e["ref"])
        if "@" in subj[1:] or "@" in obj[1:]:
            fail("edge %s double-@ ref" % e["ref"])
    if preds != {"related_to": 14, "supports": 30}:
        fail("edge predicates %s != {related_to:14, supports:30}" % preds)

    # ---- 9. snapshot numbers re-derived from manifest ----
    snaps = obs_of("dataset.snapshot")
    if len(snaps) != 1:
        fail("snapshot count %d != 1" % len(snaps))
    if snaps[0]["body"]["data"]["row_count"] != manifest["total_rows"]:
        fail("snapshot row_count != manifest total_rows")
    if snaps[0]["body"]["data"]["distinct_instance_ids"] != 893:
        fail("distinct_instance_ids != 893")

    # ---- 10. observations have observed_at + time_basis, source ref ----
    for r in obs_of("intel.behavior") + obs_of("behavior.tool_sequence") + \
            obs_of("dataset.record") + obs_of("dataset.snapshot"):
        b = r["body"]
        if not b.get("observed_at") or not b.get("time_basis"):
            fail("observation %s missing observed_at/time_basis" % r["ref"])
        if not str(b.get("source", "")).startswith("@"):
            fail("observation %s source not a bundle ref" % r["ref"])

    print("VALIDATE-OK: %d records, 15 findings, 14 trajectories, "
          "15 tool_sequences, 44 edges" % len(records))


if __name__ == "__main__":
    main()
