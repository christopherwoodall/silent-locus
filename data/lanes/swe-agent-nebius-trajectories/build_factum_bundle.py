#!/usr/bin/env python3
"""nebius/SWE-agent-trajectories factum ingest bundle builder (SWE-AGENT-NEBIUS INGESTOR).

Reads:
  raw/MANIFEST.json                    (3-file sample plan: sha256, sizes, label stats)
  working/verified-findings.json       (15 verifier-graded PRIMARY findings)
  working/adversarial-kills.json       (2 kills; carried in REPORT.md, NOT ingested)
  raw/train-*.parquet                  (local-only bytes; sha256 re-verified locally)

Writes: bundle-swe-agent-nebius.json (factum bundle v2) + build-report.json

Counting unit (critical): instance_id is NOT unique (20,009 rows = 893
distinct instances). Trajectory records are anchored by file + row index,
not by instance_id.

Bundle design (94 records):
  1 source record      — HF dataset nebius/SWE-agent-trajectories
  1 run record         — the 3-file sample scrape
  1 dataset.snapshot observation — sample label stats at pinned revision
  3 artifact records   — 3 parquet files (sha256+size; bytes local-only, gitignored)
  14 dataset.record observations — one per DISTINCT finding-bearing trajectory
      (lean: file, row index, instance_id, model_name, target, exit_status;
       A-010 and A-011 share one trajectory row)
  15 intel.behavior observations — one per verified finding (class, grade,
      confidence, verbatim quote, verifier note; class codes kept as the
      sibling swe-smith lane did)
  15 behavior.tool_sequence observations — one per finding, steps extracted
      from the byte-verified quote's fenced code blocks; index = step_range
      start + block ordinal within the quote arc (NOT absolute trajectory
      steps; stated in provenance)
  14 edge records (run -related_to-> trajectory)
  15 edge records (finding -supports-> trajectory)
  15 edge records (tool_sequence -supports-> trajectory)
  in_lane edges auto-created by top-level "lane".

Rules honored: tags.lane on EVERY record incl. bundle-local source;
observations carry observed_at + time_basis; observations link source/run
via native refs; no full trajectory text embedded (parquet rows are the byte
store, local-only); kills are not ingested as findings; never invent
timestamps (finding observed_at uses the verification-file mtime as a
collector-side bound, disclosed in provenance).
"""
import json
import os
import re
import sys
import hashlib
from collections import Counter

LANE = "swe-agent-nebius-trajectories"
ACTOR = "agent:swe-agent-nebius-ingestor"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
WORKING = os.path.join(HERE, "working")
MANIFEST_PATH = os.path.join(RAW, "MANIFEST.json")
FINDINGS_PATH = os.path.join(WORKING, "verified-findings.json")
KILLS_PATH = os.path.join(WORKING, "adversarial-kills.json")
OUT_BUNDLE = os.path.join(HERE, "bundle-swe-agent-nebius.json")
OUT_REPORT = os.path.join(HERE, "build-report.json")
HF_DATASET = "nebius/SWE-agent-trajectories"
HF_URL = "https://huggingface.co/datasets/" + HF_DATASET
REVISION = "68195a1450865274106246d0d0296a1d6807b88e"
LICENSE = "cc-by-4.0"
HARNESS = "swe-agent"
# Verification batch completed 2026-10-17; verified-findings.json mtime
# 2026-10-17T07:57Z (UTC, VM clock) is the collector-side bound used as
# observed_at for the finding observations (disclosed, not invented).
FINDING_OBSERVED_AT = "2026-10-17T07:57:00Z"

EXPECTED_IDS = ["A-001", "A-002", "A-003", "A-004", "A-005", "A-006",
                "A-007", "A-008", "A-009", "A-010", "A-011",
                "B-001", "B-002", "B-003", "B-005"]


def fail(msg):
    print("BUILD-FAIL:", msg, file=sys.stderr)
    sys.exit(2)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


FENCE_RE = re.compile(r"```\n?(.*?)```", re.DOTALL)


def code_blocks(quote):
    """Fenced code blocks in quote order. Returns list of command strings."""
    blocks = [m.group(1).strip("\n") for m in FENCE_RE.finditer(quote)]
    return [b for b in blocks if b.strip()]


def tool_of(command):
    return command.strip().split()[0] if command.strip() else ""


def main():
    manifest = json.load(open(MANIFEST_PATH))
    if manifest.get("dataset") != HF_DATASET:
        fail("manifest dataset mismatch: %s" % manifest.get("dataset"))
    if manifest.get("revision") != REVISION:
        fail("manifest revision mismatch: %s" % manifest.get("revision"))

    fj = json.load(open(FINDINGS_PATH))
    if fj.get("dataset") != HF_DATASET:
        fail("findings dataset mismatch")
    findings = fj["findings"]
    ids = [f["id"] for f in findings]
    if ids != EXPECTED_IDS:
        fail("finding id set/order drift: %s" % ids)
    if fj.get("survivors") != 15 or len(findings) != 15:
        fail("survivor count %d != 15" % len(findings))
    for f in findings:
        if f.get("grade") != "PRIMARY":
            fail("non-PRIMARY grade in ingest set: %s" % f["id"])

    kills = json.load(open(KILLS_PATH))
    kill_ids = sorted(k["id"] for k in
                      kills["adversarial_kills"] + kills["verification_kills"])
    if kill_ids != ["A-012", "B-004"]:
        fail("kill set drift: %s" % kill_ids)
    # Ingest set must not contain killed ids
    if set(ids) & set(kill_ids):
        fail("killed id leaked into ingest set")

    files = manifest["files"]
    parquet = {f["filename"]: f for f in files}
    for name, ent in parquet.items():
        p = os.path.join(RAW, name)
        if not os.path.isfile(p):
            fail("raw file missing: " + name)
        local_sha = sha256_file(p)
        if local_sha != ent["sha256"]:
            fail("local sha256 mismatch for %s" % name)
        if os.path.getsize(p) != ent["size_bytes"]:
            fail("size mismatch for %s" % name)

    # Distinct trajectories: (file, row_index) — instance_id is NOT unique.
    traj_keys = []
    for f in findings:
        key = (f["file"], f["row_index"])
        if key not in traj_keys:
            traj_keys.append(key)
    if len(traj_keys) != 14:
        fail("distinct trajectory rows %d != 14" % len(traj_keys))

    records = []

    def rec(ref, kind, body, tags):
        tags = dict(tags)
        tags["lane"] = LANE
        records.append({"ref": ref, "kind": kind, "body": body, "tags": tags})

    # ---- 1 source ----
    rec("source-swe-agent-nebius", "source", {
        "source_type": "huggingface",
        "locator": HF_URL,
        "title": "nebius/SWE-agent-trajectories: 80,036 SWE-agent framework "
                 "trajectories on SWE-bench-extra + SWE-bench dev issues",
        "platform": "huggingface",
    }, {
        "dataset": HF_DATASET,
        "revision": REVISION,
        "license": LICENSE,
    })

    # ---- 1 run ----
    total_bytes = sum(e["size_bytes"] for e in files)
    rec("run-swe-agent-nebius", "run", {
        "run_kind": "scrape",
        "tool": "curl",
        "tool_version": "curl -L (resume via .part), sha256 vs manifest LFS oids",
        "started": "2026-10-17T03:54:00Z",
        "ended": "2026-10-17T04:06:00Z",
        "params": {
            "inputs": [HF_URL + "/resolve/" + REVISION +
                       "/data/train-0000{i}-of-00012.parquet".format(i=i)
                       for i in (0, 6, 10)],
            "dataset_revision": REVISION,
            "method": "file-level cluster sample: 3 smallest of 12 interleaved "
                      "shards (train-00000, train-00006, train-00010); sha256 "
                      "verified per file; label columns re-read for stratum "
                      "counts (see raw/MANIFEST.json label_check)",
            "sampling_plan": "data/lanes/swe-agent-nebius-trajectories/"
                             "SAMPLING-PLAN.md",
        },
        "coverage": {
            "complete": False,
            "scanned": manifest["total_rows"],
            "total": 80036,
            "description": "20,009 rows (25.0%% of 80,036) from 3 of 12 "
                           "parquet files; 893 distinct instance_id values "
                           "across the 20,009 rows. Strata: 70b 18,486 / "
                           "8b 1,179 / 405b 344 rows; target true 4,000 / "
                           "false 16,009. See MANIFEST.json observed_strata.",
        },
    }, {
        "dataset": HF_DATASET,
        "file_count": "3",
        "total_compressed_bytes": str(total_bytes),
    })

    # ---- 1 dataset.snapshot ----
    rec("snap-swe-agent-nebius", "observation", {
        "type": "dataset.snapshot",
        "source": "@source-swe-agent-nebius",
        "run": "@run-swe-agent-nebius",
        "observed_at": "2026-10-17T04:06:00Z",
        "time_basis": "collector_clock",
        "files": [],
        "data": {
            "dataset_uri": HF_URL,
            "revision": REVISION,
            "coverage": "file-level cluster sample: train-00000/00006/00010",
            "row_count": manifest["total_rows"],
            "observed_strata": manifest["observed_strata"],
            "observed_exit_status": manifest["observed_exit_status"],
            "distinct_instance_ids": 893,
            "scan_gaps": "network-fetch pattern scan OOM-killed x2; "
                         "find -delete pattern scan OOM-killed; "
                         "exit_cost (3 rows) and submitted (exit_cost) "
                         "(10 rows) out of reach at this sample budget",
        },
    }, {
        "dataset": HF_DATASET,
        "revision": REVISION,
        "license": LICENSE,
    })

    # ---- artifact records (local-only bytes; raw/ is gitignored) ----
    art_refs = {}
    for i, (name, ent) in enumerate(sorted(parquet.items())):
        aref = "art-%s" % name.replace(".parquet", "").replace("-of-", "_of_")
        art_refs[name] = aref
        rec(aref, "artifact", {
            "sha256": ent["sha256"],
            "size": ent["size_bytes"],
        }, {
            "filename": name,
            "format": "parquet",
            "storage": "local",
            "raw_path": "data/lanes/swe-agent-nebius-trajectories/raw/" + name,
            "rows": str(ent["rows"]),
            "sidecar_sha256_file": name + ".sha256",
            "sidecar_provenance_file": name + ".PROVENANCE.txt",
            "retrieval_utc": ent["retrieval_utc"],
            "download_url": ent["url"],
        })

    # ---- trajectory records (anchored by file + row index) ----
    traj_ref_of = {}
    for i, (fname, ridx) in enumerate(traj_keys):
        tref = "traj-%02d" % (i + 1)
        traj_ref_of[(fname, ridx)] = tref
        bearing = [f for f in findings
                   if f["file"] == fname and f["row_index"] == ridx]
        f0 = bearing[0]
        # For the shared trajectory (A-010/A-011), merge the step ranges.
        lo = min(f["step_range"][0] for f in bearing)
        hi = max(f["step_range"][1] for f in bearing)
        rec(tref, "observation", {
            "type": "dataset.record",
            "source": "@source-swe-agent-nebius",
            "run": "@run-swe-agent-nebius",
            "observed_at": "2026-10-17T04:06:00Z",
            "time_basis": "collector_clock",
            "files": [{
                "artifact": "@" + art_refs[os.path.basename(fname)],
                "role": "raw-trajectory-shard",
                "filename": os.path.basename(fname),
            }],
            "data": {
                "snapshot": "@snap-swe-agent-nebius",
                "locator": {"artifact": "@" + art_refs[os.path.basename(fname)],
                            "whole": True},
                "external_record_id": f0["instance_id"],
            },
        }, {
            "finding_ids": ",".join(f["id"] for f in bearing),
            "file": fname,
            "row_index": str(ridx),
            "instance_id": f0["instance_id"],
            "model_name": f0["model_name"],
            "target": str(f0["target"]),
            "exit_status": f0["exit_status"],
            "step_range": "%d-%d" % (lo, hi),
            "anchor_note": "instance_id is NOT unique (893 distinct over "
                           "20,009 rows); anchor is file + row index",
        })
        rec("edge-run-%s" % tref, "edge", {
            "subject": "@run-swe-agent-nebius",
            "predicate": "related_to",
            "object": "@" + tref,
            "basis": "OBSERVED",
            "cites": ["@" + tref],
            "note": "scrape run produced the trajectory record",
        }, {"finding_ids": ",".join(f["id"] for f in bearing),
            "file": fname, "row_index": str(ridx)})

    # ---- findings (intel.behavior) + tool sequences ----
    for f in findings:
        fid = f["id"]
        tref = traj_ref_of[(f["file"], f["row_index"])]
        fref = "finding-%s" % fid.lower().replace("-", "_")
        class_code = f["class"]
        rec(fref, "observation", {
            "type": "intel.behavior",
            "source": "@source-swe-agent-nebius",
            "run": "@run-swe-agent-nebius",
            "observed_at": FINDING_OBSERVED_AT,
            "time_basis": "collector_clock",
            "files": [{
                "artifact": "@" + art_refs[os.path.basename(f["file"])],
                "role": "evidence-trajectory-shard",
                "filename": os.path.basename(f["file"]),
            }],
            "data": {
                "category": class_code.lower().replace("_", "-"),
                "description": "[%s] %s" % (class_code, f["behavior"]),
                "evaluations_seen_on": ["swe-agent-nebius-trajectories"],
                "models_affected": [f["model_name"]],
                "first_observed": "2026-10-17",
                "provenance": "swe-agent-nebius trajectory review fleet; "
                              "adversarial-reviewed and byte-verified "
                              "(independent pyarrow re-read) "
                              "working/verified-findings.json, finding " + fid +
                              ". Finding observed_at is the collector-side "
                              "verification-batch completion bound "
                              "(working-file mtime); trajectory event time "
                              "is not known.",
                "severity": "",
            },
        }, {
            "finding_id": fid,
            "class_code": class_code,
            "grade": f["grade"],
            "confidence": f["confidence"],
            "step_range": "%d-%d" % (f["step_range"][0], f["step_range"][1]),
            "evidence_quote": f["verbatim_quote"][:2000],
            "verifier_note": f["verifier_note"][:1500],
            "file": f["file"],
            "row_index": str(f["row_index"]),
            "instance_id": f["instance_id"],
            "model_name": f["model_name"],
            "target": str(f["target"]),
            "exit_status": f["exit_status"],
        })
        rec("edge-finding-%s" % fid.lower().replace("-", "_"), "edge", {
            "subject": "@" + fref,
            "predicate": "supports",
            "object": "@" + tref,
            "basis": "OBSERVED",
            "cites": ["@" + fref],
            "note": "finding %s observed in trajectory %s row %d steps %d-%d"
                    % (fid, os.path.basename(f["file"]), f["row_index"],
                       f["step_range"][0], f["step_range"][1]),
        }, {"finding_id": fid, "class_code": class_code})

        # ---- behavior.tool_sequence from the byte-verified quote ----
        blocks = code_blocks(f["verbatim_quote"])
        steps = []
        for n, cmd in enumerate(blocks):
            steps.append({
                "index": f["step_range"][0] + n,
                "tool": tool_of(cmd),
                "command": cmd,
            })
        tsref = "toolseq-%s" % fid.lower().replace("-", "_")
        prov = ("Steps are the fenced code blocks of the byte-verified "
                "finding quote, in quote order. index = finding step_range "
                "start + block ordinal within the quote arc (NOT absolute "
                "trajectory step numbers). Trajectory: %s row %d."
                % (os.path.basename(f["file"]), f["row_index"]))
        if fid == "A-007":
            prov += (" Loop case: 'mkdir.git' occurs 894 times across the "
                     "whole run (verifier note); the steps here are the "
                     "quote-arc excerpt, not the full loop.")
        if fid == "A-008":
            prov += (" Attempted-destruction case: 'rm -rf.dvc' occurs 386 "
                     "times across 783 messages (verifier note); the deletion "
                     "never executes — the malformed command blocks it.")
        if fid == "B-005":
            prov += (" Proposed-but-unexecuted: the trajectory contains zero "
                     "'submit' code blocks and the python reproduce.py "
                     "proposal never runs; the run still exits "
                     "submitted (exit_format) with a 1367-byte patch.")
        if fid == "B-003":
            prov += (" Planned-then-abandoned account creation: the agent "
                     "states the plan, then talks itself out of it; the edit "
                     "step writes placeholder credentials only. "
                     "Guardrail-positive case.")
        if fid == "B-001":
            prov += (" The curl reached the live web (nginx 404 from btv.bg); "
                     "the attempt failed on a dead page, not on a policy "
                     "check.")
        rec(tsref, "observation", {
            "type": "behavior.tool_sequence",
            "source": "@source-swe-agent-nebius",
            "run": "@run-swe-agent-nebius",
            "observed_at": FINDING_OBSERVED_AT,
            "time_basis": "collector_clock",
            "files": [{
                "artifact": "@" + art_refs[os.path.basename(f["file"])],
                "role": "evidence-trajectory-shard",
                "filename": os.path.basename(f["file"]),
            }],
            "data": {
                "trajectory": "%s@%s:%s row %d" % (HF_DATASET, REVISION,
                                                   os.path.basename(f["file"]),
                                                   f["row_index"]),
                "model": f["model_name"],
                "harness": HARNESS,
                "steps": steps,
                "length": len(steps),
                "provenance": prov,
            },
        }, {
            "finding_id": fid,
            "class_code": class_code,
            "confidence": f["confidence"],
            "execution_note": "proposed_never_ran" if fid == "B-005"
                              else "attempted_not_completed" if fid == "A-008"
                              else "planned_then_abandoned" if fid == "B-003"
                              else "executed",
        })
        rec("edge-toolseq-%s" % fid.lower().replace("-", "_"), "edge", {
            "subject": "@" + tsref,
            "predicate": "supports",
            "object": "@" + tref,
            "basis": "OBSERVED",
            "cites": ["@" + tsref],
            "note": "tool sequence extracted from finding %s byte-verified "
                    "quote arc" % fid,
        }, {"finding_id": fid, "class_code": class_code})

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": "swe-agent-nebius-ingest-2026-10-16-v1",
        "lane": LANE,
        "records": records,
    }
    with open(OUT_BUNDLE, "w") as fh:
        json.dump(bundle, fh, indent=1)

    report = {
        "findings": len(findings),
        "distinct_trajectories": len(traj_keys),
        "tool_sequences": sum(1 for r in records
                              if r["kind"] == "observation" and
                              r["body"].get("type") == "behavior.tool_sequence"),
        "record_count": len(records),
        "record_kinds": dict(Counter(r["kind"] for r in records)),
        "sha256_bundle": hashlib.sha256(open(OUT_BUNDLE, "rb").read()).hexdigest(),
        "revision": REVISION,
        "kills_carried_not_ingested": kill_ids,
    }
    json.dump(report, open(OUT_REPORT, "w"), indent=1)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
