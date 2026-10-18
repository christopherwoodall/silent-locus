#!/usr/bin/env python3
"""WebArena-Infinity trajectories factum ingest bundle builder (WEBARENA-INFINITY INGESTOR).

Reads:
  raw/MANIFEST.json              (completeness: true, 4390 files, sha256_mismatches: 0)
  raw/_absent_at_rev.json        (134 absent at rev, recorded not ingested)
  working/verified-findings.json (21 byte-verified PRIMARY findings)
  raw/<model>/<site>/<task_id>/result.json  (passed/is_done/steps, lean attributes)

Writes: bundle-webarena-infinity.json (factum bundle v2) + build-report.json

Bundle design (parent-ordered):
  1 source record            -- HF dataset webarena-x/webarena-infinity-trajectories
  1 artifact record          -- reference-only pointer at the HF dataset @ rev
                               (raw bytes stay local in raw/, not in git)
  1 run record               -- the curl download
  1 dataset.snapshot         -- collection output at rev
  2195 dataset.record observations -- lean: trajectory id, model, site, step count,
                                    result.json passed/is_done, raw path, sha256;
                                    locator points at the dataset artifact + row.
                                    NO step content.
  21 intel.behavior observations   -- one per verified finding
  2195 edge records (run -related_to-> dataset.record)
  25 edge records (finding -supports-> dataset.record)
    -- 19 findings have one trajectory; A-F007 and RB-012 cite a verified
       sibling trajectory (edge to primary only, sibling in note);
       A-F010 names 6 trajectories (edge to each); A-F009 is corpus-wide
       (no supports edge -- note explains). 19 + 6 = 25, deviation from the
       ordered 21 is flagged in the build report.
  in_lane edges auto-created by top-level "lane".

Rules honored: tags.lane on EVERY record incl. bundle-local source;
observations carry observed_at + time_basis; observations link source/run
via native refs; claims cite observations only (NO claims filed here);
verbatim quotes preserved; RB-008: ak- token value and org id withheld --
finding filed with path/error context/hash only, raw bytes untouched.
"""
import json
import os
import sys
import hashlib
from collections import Counter

LANE = "webarena-infinity-trajectories"
ACTOR = "agent:webarena-infinity-ingestor"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
WORKING = os.path.join(HERE, "working")
MANIFEST_PATH = os.path.join(RAW, "MANIFEST.json")
ABSENT_PATH = os.path.join(RAW, "_absent_at_rev.json")
FINDINGS_PATH = os.path.join(WORKING, "verified-findings.json")
OUT_BUNDLE = os.path.join(HERE, "bundle-webarena-infinity.json")
OUT_REPORT = os.path.join(HERE, "build-report.json")
HF_DATASET = "webarena-x/webarena-infinity-trajectories"
HF_REV = "73cf7f57a6ff61c95722a23bffdd9c1de4069bfe"
HF_URL = "https://huggingface.co/datasets/" + HF_DATASET
IDEMPOTENCY_KEY = "webarena-infinity-ingest-2026-10-17-v1"


def fail(msg):
    print("BUILD-FAIL:", msg, file=sys.stderr)
    sys.exit(2)


def load_manifest():
    if not os.path.isfile(MANIFEST_PATH):
        fail("MANIFEST.json missing at " + MANIFEST_PATH)
    m = json.load(open(MANIFEST_PATH))
    if m.get("dataset") != HF_DATASET:
        fail("manifest dataset mismatch: %s" % m.get("dataset"))
    if m.get("revision") != HF_REV:
        fail("manifest revision mismatch: %s" % m.get("revision"))
    if m.get("completeness") is not True:
        fail("manifest completeness flag not true")
    if m.get("sha256_mismatches"):
        fail("manifest has sha256 mismatches: %s" % m["sha256_mismatches"])
    if m.get("missing_files"):
        fail("manifest has missing files: %s" % m["missing_files"])
    return m


def main():
    manifest = load_manifest()
    files = manifest.get("files", [])
    generated_at = manifest.get("generated_at_utc")
    absent = json.load(open(ABSENT_PATH)) if os.path.isfile(ABSENT_PATH) else {}

    findings = json.load(open(FINDINGS_PATH))
    if not isinstance(findings, list) or len(findings) != 21:
        fail("verified-findings.json must hold a list of 21 (got %s)" % type(findings))

    # ---- index manifest by trajectory: model/site/task -> {history, result} ----
    trajs = {}
    for fe in files:
        p = fe["path"]
        parts = p.split("/")
        if len(parts) != 4:
            fail("unexpected manifest path shape: %s" % p)
        model, site, task_id, fname = parts
        key = "%s/%s/%s" % (model, site, task_id)
        e = trajs.setdefault(key, {"model": model, "site": site, "task_id": task_id})
        e[fname] = fe
    if len(trajs) != 2195:
        fail("trajectory count %d != 2195" % len(trajs))
    for key, e in trajs.items():
        if "history.json" not in e or "result.json" not in e:
            fail("trajectory missing history/result pair: %s" % key)

    records = []

    def rec(ref, kind, body, tags):
        tags = dict(tags)
        tags["lane"] = LANE
        if len(ref) > 64:
            fail("ref exceeds 64 chars: %s" % ref)
        records.append({"ref": ref, "kind": kind, "body": body, "tags": tags})

    # ---- 1 source ----
    rec("source-webarena-infinity", "source", {
        "source_type": "huggingface",
        "locator": HF_URL,
        "title": "webarena-x/webarena-infinity-trajectories: WebArena-Infinity "
                 "agent trajectory dataset (gemini/qwen/kimi)",
        "platform": "huggingface",
    }, {
        "dataset": HF_DATASET,
        "revision": HF_REV,
        "license": "mit",
    })

    # ---- 1 artifact (reference-only; raw bytes stay local in raw/) ----
    rec("artifact-webarena-infinity", "artifact", {
        "reference": {
            "uri": HF_URL,
            "revision": HF_REV,
            "platform": "huggingface",
            "path": "data/",
        },
    }, {
        "dataset": HF_DATASET,
        "revision": HF_REV,
        "storage": "reference",
    })

    # ---- 1 run ----
    started = min(fe["retrieved_at"] for fe in files if fe.get("retrieved_at"))
    ended = generated_at
    total_bytes = manifest.get("total_bytes", 0)
    absent_total = manifest.get("trajectories_absent_at_rev", 0)
    rec("run-webarena-infinity", "run", {
        "run_kind": "scrape",
        "tool": "curl",
        "tool_version": "https-get per-file",
        "started": started,
        "ended": ended,
        "params": {
            "inputs": [HF_URL + "/resolve/" + HF_REV + "/data"],
            "dataset_revision": HF_REV,
            "method": "per-file https-get with sha256 sidecars",
        },
        "coverage": {
            "complete": True,
            "scanned": 2195,
            "total": 2195,
            "description": "2195 trajectory pairs (history.json + result.json) "
                           "downloaded at revision %s; 134 trajectories absent "
                           "at this revision (recorded in raw/_absent_at_rev.json); "
                           "%d bytes total." % (HF_REV, total_bytes),
        },
    }, {
        "dataset": HF_DATASET,
        "file_count": "4390",
        "trajectory_count": "2195",
        "absent_at_rev": str(absent_total),
        "total_bytes": str(total_bytes),
    })

    # ---- 1 dataset.snapshot ----
    rec("snap-webarena-infinity", "observation", {
        "type": "dataset.snapshot",
        "source": "@source-webarena-infinity",
        "run": "@run-webarena-infinity",
        "observed_at": ended,
        "time_basis": "collector_clock",
        "files": [],
        "data": {
            "dataset_uri": HF_URL,
            "revision": HF_REV,
            "coverage": "complete",
            "row_count": 2195,
        },
    }, {
        "dataset": HF_DATASET,
        "revision": HF_REV,
        "license": "mit",
    })

    # ---- per-trajectory dataset.record observations (lean) ----
    traj_refs = {}
    for i, (key, e) in enumerate(sorted(trajs.items())):
        hfe = e["history.json"]
        raw_path = os.path.join(RAW, hfe["path"])
        if not os.path.isfile(raw_path):
            fail("raw history file missing: %s" % hfe["path"])
        res_path = os.path.join(RAW, e["result.json"]["path"])
        result = {}
        if os.path.isfile(res_path):
            try:
                result = json.load(open(res_path))
            except Exception:
                result = {}
        observed_at = hfe.get("retrieved_at") or ended
        tref = "traj-" + e["model"] + "-" + e["site"] + "-" + e["task_id"]
        traj_refs[key] = tref
        rec(tref, "observation", {
            "type": "dataset.record",
            "source": "@source-webarena-infinity",
            "run": "@run-webarena-infinity",
            "observed_at": observed_at,
            "time_basis": "collector_clock",
            "files": [],
            "data": {
                "snapshot": "@snap-webarena-infinity",
                "locator": {"artifact": "@artifact-webarena-infinity",
                            "row": {"index": i, "key": key}},
                "external_record_id": key,
            },
        }, {
            "trajectory_id": key,
            "model": e["model"],
            "site": e["site"],
            "task_id": e["task_id"],
            "step_count": str(result.get("steps", "")),
            "passed": str(result.get("passed", "")),
            "is_done": str(result.get("is_done", "")),
            "raw_path": os.path.join("data/lanes", LANE, "raw", hfe["path"]),
            "sha256": hfe["sha256"],
        })

    # ---- findings ----
    n_sup_edges = 0
    for f in findings:
        fid = f["id"]
        class_code = f["class"]
        grade = f["grade"]
        confidence = f["confidence"]
        step_range = f["step_range"]
        traj_id = f["trajectory"]
        quote = f["quote"]
        vnote = f.get("verifier_note", "")
        why = f.get("why_interesting", "")
        fref = "finding-" + fid
        description = "[%s] %s" % (class_code, why or quote)
        body = {
            "type": "intel.behavior",
            "source": "@source-webarena-infinity",
            "run": "@run-webarena-infinity",
            "observed_at": ended,
            "time_basis": "collector_clock",
            "files": [],
            "data": {
                "category": class_code.lower().replace("_", "-"),
                "description": description,
                "evaluations_seen_on": ["webarena-infinity"],
                "models_affected": [f["model"]],
                "first_observed": "",
                "provenance": "webarena-infinity trajectory review fleet; "
                              "verifier-graded working/verified-findings.json "
                              "(byte-verified 2026-10-17)",
                "severity": "",
            },
        }
        tags = {
            "finding_id": fid,
            "class_code": class_code,
            "grade": grade,
            "confidence": confidence,
            "step_range": step_range,
            "trajectory_id": traj_id,
            "model": f["model"],
            "site": f["site"],
            "task_id": f["task_id"],
            "evidence_quote": quote,
            "verifier_note": vnote,
            "raw_path": os.path.join("data/lanes", LANE, "raw",
                                     str(traj_id).replace("/", os.sep), "history.json")
                         if traj_id != "aggregate" else "aggregate",
            "sha256": f["sha256"],
        }
        if fid == "RB-008":
            # Credential-like token: value and org id deliberately withheld.
            tags["secret_withheld"] = "true"
            tags["credential_note"] = ("ak- prefixed token value and org id "
                                       "present in raw result.json errors[0] "
                                       "but NOT copied here; raw bytes remain "
                                       "in raw/ untouched")
            tags["result_json_sha256"] = ("4ad3a634a9a418a0fbc67af7756ac8e0"
                                           "5222e12271eb9feb9ea0175c10a3c06e")
        rec(fref, "observation", body, tags)

        # ---- supports edges ----
        edge_targets = []
        if traj_id == "aggregate":
            if fid == "A-F010":
                # Six named trajectories in the quote; edge to each.
                edge_targets = [
                    ("gemini/gmail-accounts-and-contacts/task_e19", 1),
                    ("gemini/handshake-career-exploration/task_h6", 2),
                    ("gemini/paypal-my-wallet/task_e1", 3),
                    ("gemini/paypal-my-wallet/task_e15", 4),
                    ("gemini/xero-invoicing/task_e10", 5),
                    ("gemini/xero-invoicing/task_h5", 6),
                ]
            # A-F009 is corpus-wide: no supports edge (note in report).
        else:
            if traj_id not in traj_refs:
                fail("finding %s references unknown trajectory %s" % (fid, traj_id))
            edge_targets = [(traj_id, 1)]
        for tgt, seq in edge_targets:
            if tgt not in traj_refs:
                fail("finding %s references unknown trajectory %s" % (fid, tgt))
            tref = traj_refs[tgt]
            eref = "edge-sup-%s-%02d" % (fid, seq)
            note = "finding observed in trajectory steps %s" % step_range
            if fid == "A-F010":
                note += " (aggregate finding; 6 named trajectories)"
            if fid == "A-F007":
                note += "; verified sibling trajectory gemini/superhuman-general/task_h11 shows the same misuse"
            if fid == "RB-012":
                note += "; verified extension qwen/paypal-my-wallet/task_h84 shows the same mismatch"
            if fid == "A-F006":
                note += "; verifier confirmed cross-trajectory note in gemini/elation-patient-communication/task_m13 steps 7-14"
            if fid == "RB-005":
                note += "; reviewer's 4-trajectory extension unverified (open gap)"
            if fid == "RB-007":
                note += "; reviewer's qwen twin claim unverified (open gap)"
            if fid == "RB-011":
                note += "; confidence downgraded MEDIUM->LOW by verifier"
            rec(eref, "edge", {
                "subject": "@" + fref,
                "predicate": "supports",
                "object": "@" + tref,
                "basis": "OBSERVED",
                "cites": ["@" + fref],
                "note": note,
            }, {
                "trajectory_id": tgt,
                "class_code": class_code,
            })
            n_sup_edges += 1

    # ---- run -> trajectory related_to edges ----
    for key in sorted(trajs.keys()):
        tref = traj_refs[key]
        rec("edge-run-" + tref.replace("traj-", ""), "edge", {
            "subject": "@run-webarena-infinity",
            "predicate": "related_to",
            "object": "@" + tref,
            "basis": "OBSERVED",
            "cites": ["@" + tref],
            "note": "scrape run produced the trajectory record",
        }, {"trajectory_id": key})

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": IDEMPOTENCY_KEY,
        "lane": LANE,
        "records": records,
    }
    with open(OUT_BUNDLE, "w") as fh:
        json.dump(bundle, fh)

    kinds = dict(Counter(r["kind"] for r in records))
    types = dict(Counter(r["body"].get("type", "") for r in records if r["kind"] == "observation"))
    report = {
        "trajectories": len(trajs),
        "findings": len(findings),
        "supports_edges": n_sup_edges,
        "record_count": len(records),
        "record_kinds": kinds,
        "observation_types": types,
        "sha256_bundle": hashlib.sha256(open(OUT_BUNDLE, "rb").read()).hexdigest(),
        "total_bytes": total_bytes,
        "scrape_started": started,
        "scrape_ended": ended,
        "revision": HF_REV,
        "supports_edge_deviation": ("ordered 21 supports edges; filed %d "
                                    "(A-F010 names 6 trajectories; A-F009 is "
                                    "corpus-wide, no edge)" % n_sup_edges),
    }
    json.dump(report, open(OUT_REPORT, "w"), indent=1)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
