#!/usr/bin/env python3
"""SWE-rebench OpenHands factum ingest bundle builder (REBENCH INGESTOR).

Reads:
  raw/trajectories.parquet          (67,074 rows, sha256-verified)
  verified-findings.jsonl           (4 verifier-surviving findings)
  kill-list.json                    (27 killed candidates, for the report)
  raw/LICENSE.note                  (cc-by-4.0, verbatim)

Writes: bundle-rebench.json (factum bundle v2) + build-report.json

Bundle design (lean — 67,074 trajectories, no per-row records):
  1 source record    — HF dataset nebius/SWE-rebench-openhands-trajectories
  1 run record       — the scrape
  1 dataset.snapshot — corpus stats (exit_status / resolved / repo distributions)
  1 artifact record  — trajectories.parquet (sha256 + size)
  10 dataset.record observations — one per finding trajectory (lean attributes)
  4 intel.behavior observations  — one per verified finding
  10 edge records (run -related_to-> trajectory)
  4 edge records (finding -supports-> trajectory)
  in_lane edges auto-created by top-level "lane".

Rules: tags.lane on EVERY record; observations carry observed_at +
time_basis; no full step content embedded (parquet is the byte store);
verbatim quotes live in finding tags (<=2000 chars).
"""
import json
import os
import sys
import hashlib
from collections import Counter

LANE = "rebench-openhands-trajectories"
ACTOR = "agent:rebench-ingestor"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
PARQUET = os.path.join(RAW, "trajectories.parquet")
FINDINGS_PATH = os.path.join(HERE, "verified-findings.jsonl")
OUT_BUNDLE = os.path.join(HERE, "bundle-rebench.json")
OUT_REPORT = os.path.join(HERE, "build-report.json")
HF_DATASET = "nebius/SWE-rebench-openhands-trajectories"
HF_URL = "https://huggingface.co/datasets/" + HF_DATASET
REVISION = "35455389ab51bf5e2306bfd436ef72d0f98bf882"
LICENSE = "cc-by-4.0"
PARQUET_SHA256 = "14048dd1fcd22ce094b6e85f8a38f223a9ef1327031aaaad052804870212efa1"
PARQUET_BYTES = 2079503354

# Distributions computed by reviewers over all 67,074 rows
EXIT_STATUS_DIST = {
    "submit": 60739,
    "max-iteration": 6003,
    "stuck-in-loop": 252,
    "litellm-timeout": 36,
    "ServiceUnavailable": 29,
    "unknown": 10,
    "AttributeError": 5,
}
RESOLVED_SPLIT = {"resolved_0": 34913, "resolved_1": 32161}
REPO_COUNT = 1823
TOP_REPOS = {"tobymao/sqlglot": 2678, "python-pillow/Pillow": 1328,
             "iterative/dvc": 846, "streamlink/streamlink": 661,
             "sqlfluff/sqlfluff": 459}

# Finding -> trajectory ids (from verified-findings.jsonl verifier notes)
FINDING_TRAJS = {
    "F-001": ["chatcmpl-f1b761c7b1526651a4185cac841f4ba5",
              "chatcmpl-24758085175aa3b9fa664097408bbcb6",
              "chatcmpl-b1edf3da5db87b4117e96a3241848539",
              "chatcmpl-21829fdd1d358c73d4a47ba73608e875",
              "chatcmpl-8d985dbff619498c32c36e40529b9e72",
              "chatcmpl-0db37c2c48803ef10ea75dad9f63bb72"],
    "F-002": ["chatcmpl-71913e037b5368b663bc4e2852928153"],
    "F-006": ["chatcmpl-49a1244191b0e6f2bd5761feb8c0b876",
              "chatcmpl-0b5bcd18d09ec2200a386f76abfbac40"],
    "F-007": ["chatcmpl-efc869b063c00a8f4973286a806d1031"],
}

# Resolved trajectory attributes via column-projected parquet scan
TRAJ_ATTRS = {
    "chatcmpl-f1b761c7b1526651a4185cac841f4ba5": ("RadioAstronomySoftwareGroup__pyuvdata-642", "RadioAstronomySoftwareGroup/pyuvdata", "AgentStuckInLoopError: Agent got stuck in a loop", 0),
    "chatcmpl-24758085175aa3b9fa664097408bbcb6": ("zopefoundation__zope.configuration-42", "zopefoundation/zope.configuration", "AgentStuckInLoopError: Agent got stuck in a loop", 0),
    "chatcmpl-b1edf3da5db87b4117e96a3241848539": ("conan-io__conan-12397", "conan-io/conan", "AgentStuckInLoopError: Agent got stuck in a loop", 0),
    "chatcmpl-21829fdd1d358c73d4a47ba73608e875": ("pappasam__toml-sort-36", "pappasam/toml-sort", "AgentStuckInLoopError: Agent got stuck in a loop", 1),
    "chatcmpl-8d985dbff619498c32c36e40529b9e72": ("stfc__PSyclone-1603", "stfc/PSyclone", "AgentStuckInLoopError: Agent got stuck in a loop", 1),
    "chatcmpl-0db37c2c48803ef10ea75dad9f63bb72": ("Veinar__envcloak-19", "Veinar/envcloak", "AgentStuckInLoopError: Agent got stuck in a loop", 0),
    "chatcmpl-71913e037b5368b663bc4e2852928153": ("tobymao__sqlglot-2529", "tobymao/sqlglot", "submit", 1),
    "chatcmpl-49a1244191b0e6f2bd5761feb8c0b876": ("pandas-dev__pandas-61146", "pandas-dev/pandas", "submit", 0),
    "chatcmpl-0b5bcd18d09ec2200a386f76abfbac40": ("anchore__anchore-cli-107", "anchore/anchore-cli", "submit", 0),
    "chatcmpl-efc869b063c00a8f4973286a806d1031": ("pynamodb__PynamoDB-386", "pynamodb/PynamoDB", "RuntimeError: Agent reached maximum iteration. Current iteration: 100, max iteration: 100", 1),
}


def fail(msg):
    print("BUILD-FAIL:", msg, file=sys.stderr)
    sys.exit(2)


def main():
    findings = [json.loads(l) for l in open(FINDINGS_PATH) if l.strip()]
    if len(findings) != 4:
        fail("expected 4 verified findings, got %d" % len(findings))
    for f in findings:
        if f.get("verified") != "yes":
            fail("finding %s not verifier-confirmed" % f.get("finding_id"))

    prov = {}
    p = PARQUET + ".PROVENANCE.txt"
    if os.path.isfile(p):
        for line in open(p):
            line = line.strip()
            if "=" in line or ":" in line:
                for sep in ("=", ":"):
                    if sep in line:
                        k, v = line.split(sep, 1)
                        prov[k.strip()] = v.strip()
                        break
    observed_at = prov.get("retrieval_utc") or "2026-10-17T03:03:00Z"

    records = []

    def rec(ref, kind, body, tags):
        tags = dict(tags)
        tags["lane"] = LANE
        records.append({"ref": ref, "kind": kind, "body": body, "tags": tags})

    # ---- 1 source ----
    rec("source-rebench", "source", {
        "source_type": "huggingface",
        "locator": HF_URL,
        "title": "nebius/SWE-rebench-openhands-trajectories: 67,074 OpenHands "
                 "v0.54 rollouts (Qwen3-Coder-480B-A35B) on nebius/SWE-rebench "
                 "GitHub issues",
        "platform": "huggingface",
    }, {
        "dataset": HF_DATASET,
        "revision": REVISION,
        "license": LICENSE,
    })

    # ---- 1 run ----
    rec("run-rebench", "run", {
        "run_kind": "scrape",
        "tool": "curl",
        "tool_version": "https-get with -C - resume",
        "started": observed_at,
        "ended": observed_at,
        "params": {
            "inputs": [HF_URL + "/resolve/" + REVISION + "/trajectories.parquet"],
            "dataset_revision": REVISION,
            "method": "single curl download with resume; sha256 verified "
                      "against HF LFS oid",
        },
        "coverage": {
            "complete": True,
            "scanned": 67074,
            "total": 67074,
            "description": "trajectories.parquet: 67,074 rows, %d bytes, "
                           "sha256 %s." % (PARQUET_BYTES, PARQUET_SHA256),
        },
    }, {
        "dataset": HF_DATASET,
        "total_bytes": str(PARQUET_BYTES),
        "sha256": PARQUET_SHA256,
    })

    # ---- 1 dataset.snapshot ----
    rec("snap-rebench", "observation", {
        "type": "dataset.snapshot",
        "source": "@source-rebench",
        "run": "@run-rebench",
        "observed_at": observed_at,
        "time_basis": "collector_clock",
        "files": [],
        "data": {
            "dataset_uri": HF_URL,
            "revision": REVISION,
            "coverage": "complete",
            "row_count": 67074,
            "exit_status_distribution": EXIT_STATUS_DIST,
            "resolved_split": RESOLVED_SPLIT,
            "repo_count": REPO_COUNT,
            "top_repos": TOP_REPOS,
            "model": "Qwen3-Coder-480B-A35B",
            "harness": "OpenHands v0.54",
        },
    }, {
        "dataset": HF_DATASET,
        "revision": REVISION,
    })

    # ---- 1 artifact (the parquet) ----
    rec("art-rebench-parquet", "artifact", {
        "sha256": PARQUET_SHA256,
        "size": PARQUET_BYTES,
    }, {
        "filename": "trajectories.parquet",
        "raw_path": "data/lanes/rebench-openhands-trajectories/raw/trajectories.parquet",
    })

    # ---- trajectory records (finding trajectories only) ----
    traj_refs = {}
    for tid, (iid, repo, exit_status, resolved) in TRAJ_ATTRS.items():
        tref = "traj-" + tid[:16]
        traj_refs[tid] = tref
        rec(tref, "observation", {
            "type": "dataset.record",
            "source": "@source-rebench",
            "run": "@run-rebench",
            "observed_at": observed_at,
            "time_basis": "collector_clock",
            "files": [{
                "artifact": "@art-rebench-parquet",
                "role": "raw-trajectory",
                "filename": "trajectories.parquet",
            }],
            "data": {
                "snapshot": "@snap-rebench",
                "locator": {"artifact": "@art-rebench-parquet",
                            "row": {"trajectory_id": tid}},
                "external_record_id": tid,
            },
        }, {
            "trajectory_id": tid,
            "instance_id": iid,
            "repo": repo,
            "exit_status": exit_status,
            "resolved": str(resolved),
        })
        rec("edge-run-" + tid[:16], "edge", {
            "subject": "@run-rebench",
            "predicate": "related_to",
            "object": "@" + tref,
            "basis": "OBSERVED",
            "cites": ["@" + tref],
            "note": "scrape run produced the trajectory record",
        }, {"trajectory_id": tid})

    # ---- findings ----
    for f in findings:
        fid = f["finding_id"]
        fref = "finding-" + fid
        body = {
            "type": "intel.behavior",
            "source": "@source-rebench",
            "run": "@run-rebench",
            "observed_at": observed_at,
            "time_basis": "collector_clock",
            "files": [{"artifact": "@art-rebench-parquet",
                       "role": "evidence-trajectory",
                       "filename": "trajectories.parquet"}],
            "data": {
                "category": f["behavior_class"].lower().replace("_", "-"),
                "description": "[%s] %s" % (f["behavior_class"],
                                            f["verifier_note"][:800]),
                "evaluations_seen_on": ["swe-rebench"],
                "models_affected": ["Qwen3-Coder-480B-A35B"],
                "provenance": "rebench trajectory review fleet; "
                              "adversarial reviewer + byte-verifier; "
                              "verified-findings.jsonl",
            },
        }
        rec(fref, "observation", body, {
            "finding_id": fid,
            "class_code": f["behavior_class"],
            "grade": f["grade"],
            "confidence": f["confidence"],
            "step_range": f["step_range"],
            "evidence_quote": f["verbatim_quote"][:2000],
            "verifier_note": f["verifier_note"][:2000],
            "trajectory_id": f["trajectory_id"],
            "instance_id": f["instance_id"],
        })
        for tid in FINDING_TRAJS.get(fid, []):
            tref = traj_refs.get(tid)
            if tref:
                rec("edge-%s-%s" % (fid, tid), "edge", {
                    "subject": "@" + fref,
                    "predicate": "supports",
                    "object": "@" + tref,
                    "basis": "OBSERVED",
                    "cites": ["@" + fref],
                    "note": "finding %s observed in trajectory %s" % (fid, tid),
                }, {"finding_id": fid, "trajectory_id": tid})

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": "rebench-ingest-2026-10-17-v1",
        "lane": LANE,
        "records": records,
    }
    with open(OUT_BUNDLE, "w") as fh:
        json.dump(bundle, fh)

    report = {
        "findings": len(findings),
        "finding_trajectories": len(traj_refs),
        "record_count": len(records),
        "record_kinds": dict(Counter(r["kind"] for r in records)),
        "sha256_bundle": hashlib.sha256(
            open(OUT_BUNDLE, "rb").read()).hexdigest(),
        "revision": REVISION,
    }
    json.dump(report, open(OUT_REPORT, "w"), indent=1)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
