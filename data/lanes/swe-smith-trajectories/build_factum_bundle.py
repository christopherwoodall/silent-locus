#!/usr/bin/env python3
"""SWE-smith trajectories factum ingest bundle builder (SWE-SMITH INGESTOR).

Reads:
  raw/MANIFEST.json                 (shard plan: 00003 of 00008 per scaffold)
  raw/SAMPLE-STATS.json             (9,501 rows: tool 3,013 / xml 3,260 / ticks 3,228)
  verified-findings.jsonl           (13 verifier-graded findings)
  raw/<scaffold>-00003-of-00008.parquet + .jsonl (trajectory bytes, cached)

Writes: bundle-swe-smith.json (factum bundle v2) + build-report.json

Bundle design:
  1 source record   — HF dataset SWE-bench/SWE-smith-trajectories
  1 run record      — the shard-3 scrape
  1 dataset.snapshot observation — sample stats at revision
  6 artifact records — 3 parquet + 3 JSONL (sha256+size; JSONL sha computed locally)
  13 dataset.record observations — one per finding-bearing trajectory
      (lean: traj_id, scaffold, model, resolved, step_range, raw shard path)
  13 intel.behavior observations — one per verified finding
  13 edge records (run -related_to-> trajectory)
  13 edge records (finding -supports-> trajectory)
  in_lane edges auto-created by top-level "lane".

Rules honored: tags.lane on EVERY record incl. bundle-local source;
observations carry observed_at + time_basis; observations link source/run
via native refs; no full step content embedded (JSONL shards are the byte
store); scanner metadata (model/shard/rev) in record tags, never in
web.capture data fields; findings cite trajectories via supports edges.
"""
import json
import os
import sys
import hashlib
from collections import Counter

LANE = "swe-smith-trajectories"
ACTOR = "agent:swe-smith-ingestor"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
MANIFEST_PATH = os.path.join(RAW, "MANIFEST.json")
STATS_PATH = os.path.join(RAW, "SAMPLE-STATS.json")
FINDINGS_PATH = os.path.join(HERE, "verified-findings.jsonl")
OUT_BUNDLE = os.path.join(HERE, "bundle-swe-smith.json")
OUT_REPORT = os.path.join(HERE, "build-report.json")
HF_DATASET = "SWE-bench/SWE-smith-trajectories"
HF_URL = "https://huggingface.co/datasets/" + HF_DATASET


def fail(msg):
    print("BUILD-FAIL:", msg, file=sys.stderr)
    sys.exit(2)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest():
    if not os.path.isfile(MANIFEST_PATH):
        fail("MANIFEST.json missing at " + MANIFEST_PATH)
    m = json.load(open(MANIFEST_PATH))
    if m.get("dataset") != HF_DATASET:
        fail("manifest dataset mismatch: %s" % m.get("dataset"))
    files = m.get("files", {})
    for k in ("tool-00003-of-00008.parquet", "xml-00003-of-00008.parquet",
              "ticks-00003-of-00008.parquet"):
        if k not in files:
            fail("manifest missing parquet: " + k)
        if not files[k].get("sha256"):
            fail("manifest parquet sha256 missing: " + k)
    return m


def load_findings():
    findings = []
    for line in open(FINDINGS_PATH):
        line = line.strip()
        if line:
            findings.append(json.loads(line))
    if len(findings) != 13:
        fail("finding count %d != 13" % len(findings))
    tids = [f.get("trajectory_id") for f in findings]
    if len(set(tids)) != len(tids):
        fail("duplicate trajectory_ids: %s" % [t for t, n in Counter(tids).items() if n > 1])
    return findings


def main():
    manifest = load_manifest()
    stats = json.load(open(STATS_PATH))
    findings = load_findings()
    revision = manifest.get("revision") or ""
    license_ = manifest.get("license") or "NOT-DECLARED"
    retrieved = manifest.get("retrieval_utc")

    parquet_names = ["tool-00003-of-00008.parquet", "xml-00003-of-00008.parquet",
                     "ticks-00003-of-00008.parquet"]
    jsonl_names = ["tool-00003.jsonl", "xml-00003.jsonl", "ticks-00003.jsonl"]

    records = []

    def rec(ref, kind, body, tags):
        tags = dict(tags)
        tags["lane"] = LANE
        records.append({"ref": ref, "kind": kind, "body": body, "tags": tags})

    # ---- 1 source ----
    rec("source-swe-smith", "source", {
        "source_type": "huggingface",
        "locator": HF_URL,
        "title": "SWE-bench/SWE-smith-trajectories: SWE-agent-LM-32B training "
                 "rollouts on synthetic SWE-smith bug-injection tasks",
        "platform": "huggingface",
    }, {
        "dataset": HF_DATASET,
        "revision": revision,
        "license": license_,
    })

    # ---- 1 run ----
    total_parquet = sum(manifest["files"][n]["bytes"] for n in parquet_names)
    total_jsonl = sum(manifest["files"][n]["bytes"] for n in jsonl_names if n in manifest["files"])
    rec("run-swe-smith", "run", {
        "run_kind": "scrape",
        "tool": "curl",
        "tool_version": "https-get (range-chunked 16MB for xml/ticks)",
        "started": retrieved,
        "ended": retrieved,
        "params": {
            "inputs": [HF_URL + "/resolve/" + revision +
                       "/data/<scaffold>-00003-of-00008.parquet"],
            "dataset_revision": revision,
            "method": "single-threaded https-get; parquet -> jsonl expansion via convert.py",
            "shard_plan": manifest.get("shard_plan"),
        },
        "coverage": {
            "complete": False,
            "scanned": stats["totals"]["rows"],
            "total": 76002,
            "description": "shard 00003 of 00008 per scaffold (middle shard); "
                           "9,501 rows sampled (tool 3,013 / xml 3,260 / ticks 3,228); "
                           "resolved 2,801 / unresolved 6,700",
        },
    }, {
        "dataset": HF_DATASET,
        "file_count": "6",
        "total_parquet_bytes": str(total_parquet),
        "total_jsonl_bytes": str(total_jsonl),
    })

    # ---- 1 dataset.snapshot observation ----
    rec("snap-swe-smith", "observation", {
        "type": "dataset.snapshot",
        "source": "@source-swe-smith",
        "run": "@run-swe-smith",
        "observed_at": retrieved,
        "time_basis": "collector_clock",
        "files": [],
        "data": {
            "dataset_uri": HF_URL,
            "revision": revision,
            "coverage": "shard-00003-per-scaffold",
            "row_count": stats["totals"]["rows"],
            "resolved_true": stats["totals"]["resolved_true"],
            "resolved_false": stats["totals"]["resolved_false"],
        },
    }, {
        "dataset": HF_DATASET,
        "revision": revision,
    })

    # ---- artifact records ----
    art_refs = {}
    for n in parquet_names + jsonl_names:
        p = os.path.join(RAW, n)
        if not os.path.isfile(p):
            fail("raw file missing: " + n)
        size = os.path.getsize(p)
        sha = manifest["files"].get(n, {}).get("sha256") or sha256_file(p)
        scaffold = n.split("-")[0]
        fmt = "parquet" if n.endswith(".parquet") else "jsonl"
        aref = "art-" + n.replace(".parquet", "").replace(".jsonl", "").replace("-of-", "_of_")
        art_refs[n] = aref
        prov_side = p + ".sha256" if os.path.isfile(p + ".sha256") else ""
        rec(aref, "artifact", {
            "sha256": sha,
            "size": size,
        }, {
            "filename": n,
            "scaffold": scaffold,
            "format": fmt,
            "raw_path": "data/lanes/swe-smith-trajectories/raw/" + n,
            "manifest_sha256": manifest["files"].get(n, {}).get("sha256") or "computed-local",
            "sidecar_sha256_file": os.path.basename(prov_side) if prov_side else "",
        })

    # ---- finding-bearing trajectory records ----
    def shard_jsonl_for(scaffold):
        return scaffold + "-00003.jsonl"

    for f in findings:
        tid = str(f["trajectory_id"])
        scaffold = str(f.get("scaffold", ""))
        jname = shard_jsonl_for(scaffold)
        tref = "traj-" + tid
        rec(tref, "observation", {
            "type": "dataset.record",
            "source": "@source-swe-smith",
            "run": "@run-swe-smith",
            "observed_at": retrieved,
            "time_basis": "collector_clock",
            "files": [{
                "artifact": "@" + art_refs[jname],
                "role": "raw-trajectory-shard",
                "filename": jname,
            }],
            "data": {
                "snapshot": "@snap-swe-smith",
                "locator": {"artifact": "@" + art_refs[jname], "whole": True},
                "external_record_id": tid,
            },
        }, {
            "trajectory_id": tid,
            "scaffold": scaffold,
            "model": str(f.get("model", "")),
            "resolved": str(f.get("resolved", "")),
            "step_range": str(f.get("step_range", "")),
            "raw_path": "data/lanes/swe-smith-trajectories/raw/" + jname,
        })
        rec("edge-run-" + tid, "edge", {
            "subject": "@run-swe-smith",
            "predicate": "related_to",
            "object": "@" + tref,
            "basis": "OBSERVED",
            "cites": ["@" + tref],
            "note": "scrape run produced the trajectory record",
        }, {"trajectory_id": tid, "scaffold": scaffold})

    # ---- findings ----
    for i, f in enumerate(findings):
        tid = str(f["trajectory_id"])
        class_code = str(f.get("class", "OTHER"))
        grade = str(f.get("grade", ""))
        confidence = str(f.get("confidence", ""))
        quote = str(f.get("evidence_quote", ""))
        vnote = str(f.get("verifier_note", ""))
        fref = "finding-%s" % f.get("finding_id", "%02d" % (i + 1))
        rec(fref, "observation", {
            "type": "intel.behavior",
            "source": "@source-swe-smith",
            "run": "@run-swe-smith",
            "observed_at": f.get("verified_utc") or retrieved,
            "time_basis": "collector_clock",
            "files": [{
                "artifact": "@" + art_refs[shard_jsonl_for(str(f.get("scaffold", "")))],
                "role": "evidence-trajectory-shard",
                "filename": shard_jsonl_for(str(f.get("scaffold", ""))),
            }],
            "data": {
                "category": class_code.lower().replace("_", "-"),
                "description": "[%s] %s" % (class_code, f.get("description", "")),
                "evaluations_seen_on": ["swe-smith-trajectories"],
                "models_affected": [str(f.get("model", ""))],
                "first_observed": "",
                "provenance": "swe-smith trajectory review fleet; verifier-graded "
                              "verified-findings.jsonl, finding " + str(f.get("finding_id", "")),
                "severity": "",
            },
        }, {
            "class_code": class_code,
            "grade": grade,
            "confidence": confidence,
            "step_range": str(f.get("step_range", "")),
            "evidence_quote": quote[:2000],
            "verifier_note": vnote[:1500],
            "trajectory_id": tid,
            "finding_id": str(f.get("finding_id", "")),
            "scaffold": str(f.get("scaffold", "")),
            "model": str(f.get("model", "")),
            "resolved": str(f.get("resolved", "")),
        })
        rec("edge-finding-" + str(f.get("finding_id", i + 1)), "edge", {
            "subject": "@" + fref,
            "predicate": "supports",
            "object": "@traj-" + tid,
            "basis": "OBSERVED",
            "cites": ["@" + fref],
            "note": "finding observed in trajectory %s steps %s" % (tid, f.get("step_range", "")),
        }, {"trajectory_id": tid, "finding_id": str(f.get("finding_id", "")), "class_code": class_code})

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": "swe-smith-ingest-2026-10-17-v1",
        "lane": LANE,
        "records": records,
    }
    with open(OUT_BUNDLE, "w") as fh:
        json.dump(bundle, fh)

    report = {
        "trajectories": len(findings),
        "findings": len(findings),
        "record_count": len(records),
        "record_kinds": dict(Counter(r["kind"] for r in records)),
        "sha256_bundle": hashlib.sha256(open(OUT_BUNDLE, "rb").read()).hexdigest(),
        "revision": revision,
    }
    json.dump(report, open(OUT_REPORT, "w"), indent=1)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
