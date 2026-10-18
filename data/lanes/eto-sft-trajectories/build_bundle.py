#!/usr/bin/env python3
"""ETO SFT trajectory factum ingest bundle builder (ETO-SFT INGESTOR).

Reads:
  raw/data/{alfworld_sft,sciworld_sft,webshop_sft}.json   (byte store, local-only)
  raw/data/<file>.PROVENANCE.txt                          (per-file retrieval provenance)
  raw/data/<file>.sha256                                  (per-file checksum)
  raw/LICENSE.note                                        (three observed license facts)
  working/verified-findings.json                          (15 verified PRIMARY findings)

Writes: bundle-eto-sft.json (factum bundle v2) + build-report.json

Counts (from bytes, verified by parse): 3119 + 1483 + 1824 = 6426 rows;
6425 unique (webshop id 4116 duplicated at indexes 936/937, byte-identical;
ingested ONCE).

Bundle design:
  1 source record    — HF dataset agent-eto/eto-sft-trajectory @ rev
  1 run record       — the scrape
  1 dataset.snapshot — scrape output at revision
  3 artifact records — one per raw JSON file (sha256 + size)
  6425 dataset.record observations — one lean record per unique trajectory
      (attributes in tags: id, split, turn count, reward/source where present,
      raw path). NO conversation content: raw JSON is the byte store.
  15 intel.behavior observations — one per verified finding (class, grade,
      confidence, turn range, verbatim evidence quote, verifier note)
  15 behavior.tool_sequence observations — one per finding trajectory;
      conversations are turn-based, so steps are the decisive turn_range
      turns recorded faithfully as {index, tool: "conversation.turn",
      command: "<from>: <verbatim value>"}. NO invented tool-call structure.
  Edges: run --related_to--> dataset.record (6425),
      intel.behavior --supports--> dataset.record (15),
      behavior.tool_sequence --supports--> intel.behavior (15).
      Top-level "lane" auto-creates in_lane edges. tags.lane set on EVERY
      record including the bundle-local source.

Observed_at grounding: trajectory records use the file's retrieved_utc
(collector_clock); behavior findings use verified-findings.json mtime
(source_metadata).
"""
import json
import os
import sys
import hashlib
import re
from collections import Counter

LANE = "eto-sft-trajectories"
ACTOR = "agent:eto-sft-ingestor"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw", "data")
WORKING = os.path.join(HERE, "working")
FINDINGS_PATH = os.path.join(WORKING, "verified-findings.json")
OUT_BUNDLE = os.path.join(HERE, "bundle-eto-sft.json")
OUT_REPORT = os.path.join(HERE, "build-report.json")
HF_DATASET = "agent-eto/eto-sft-trajectory"
REVISION = "a8f745ef799a5201d2288b9c2a47e40a0ff70a4c"
HF_URL = "https://huggingface.co/datasets/" + HF_DATASET
RAW_REL = "data/lanes/eto-sft-trajectories/raw/data"

FILES = [
    ("alfworld_sft.json", "alfworld"),
    ("sciworld_sft.json", "scienceworld"),
    ("webshop_sft.json", "webshop"),
]
EXPECTED_SHA256 = {
    "alfworld_sft.json": "9bc9720466cdbae9da26f60ab61ccdd34ae2d1e8c9f1b2ca5a1acb6606f66972",
    "sciworld_sft.json": "7079f08068ec4c526628857695231b97939472e697c3a87b4f75f682829f0ee5",
    "webshop_sft.json": "3fd1ff38f28dccaf4448cc5fa8609f2a3d3100bed303d66b6d748cff5a49601b",
}


def fail(msg):
    print("BUILD-FAIL:", msg, file=sys.stderr)
    sys.exit(2)


def read_provenance(fname):
    prov = {}
    p = os.path.join(RAW, fname + ".PROVENANCE.txt")
    for line in open(p):
        line = line.strip()
        if ":" in line:
            k, v = line.split(":", 1)
            prov[k.strip()] = v.strip()
    return prov


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def base_tid(tid):
    return tid.split()[0]


def parse_range(tr):
    lo, hi = tr.strip().strip("[]").split(",")
    return int(lo), int(hi)


def main():
    # ---- load + verify raw files ----
    splits = {}
    for fname, split in FILES:
        path = os.path.join(RAW, fname)
        if not os.path.isfile(path):
            fail("raw file missing: " + fname)
        actual = sha256_file(path)
        if actual != EXPECTED_SHA256[fname]:
            fail("sha256 mismatch for %s: %s != %s" % (fname, actual, EXPECTED_SHA256[fname]))
        prov = read_provenance(fname)
        if prov.get("sha256") and prov["sha256"] != actual:
            fail("provenance sha256 mismatch for " + fname)
        recs = json.load(open(path))
        splits[split] = {"fname": fname, "records": recs,
                         "sha256": actual, "size": os.path.getsize(path),
                         "retrieved_utc": prov.get("retrieved_utc")}

    n_rows = sum(len(s["records"]) for s in splits.values())
    if n_rows != 6426:
        fail("row count %d != 6426 (3119+1483+1824)" % n_rows)

    # ---- unique trajectories (4116 dup ingested ONCE) ----
    traj = {}  # (split, id) -> record
    dupe_events = []
    for split, s in splits.items():
        for i, r in enumerate(s["records"]):
            tid = str(r["id"])
            key = (split, tid)
            if key in traj:
                dupe_events.append((split, tid, i))
                if json.dumps(r, sort_keys=True) != json.dumps(traj[key]["record"], sort_keys=True):
                    fail("non-identical duplicate id %s/%s at index %d" % (split, tid, i))
                continue
            traj[key] = {"record": r, "index": i, "split_info": s}
    if sorted(dupe_events) != [("webshop", "4116", 937)]:
        fail("unexpected duplicate set: %s" % (dupe_events,))
    print("unique trajectories: %d (1 byte-identical dupe 4116@937 skipped)" % len(traj))

    # ---- findings ----
    findings = json.load(open(FINDINGS_PATH))
    if not isinstance(findings, list) or len(findings) != 15:
        fail("expected 15 findings, got %r" % (len(findings) if isinstance(findings, list) else type(findings)))
    review_mtime = None
    findings_mtime = os.path.getmtime(FINDINGS_PATH)

    records = []

    def rec(ref, kind, body, tags):
        tags = dict(tags)
        tags["lane"] = LANE
        if len(ref) > 64:
            fail("ref exceeds 64 chars: " + ref)
        records.append({"ref": ref, "kind": kind, "body": body, "tags": tags})

    # ---- 1 source ----
    rec("source-eto-sft", "source", {
        "source_type": "huggingface",
        "locator": HF_URL,
        "title": "agent-eto/eto-sft-trajectory: ETO SFT mix (human demos + "
                 "model rollouts); rewards 0-1, over-budget buys present "
                 "even in reward-1.0 gpt rollouts",
        "platform": "huggingface",
    }, {
        "dataset": HF_DATASET,
        "revision": REVISION,
        "license": "apache-2.0 per tags + README front matter; API field null "
                   "(see raw/LICENSE.note)",
        "hf_url": HF_URL,
    })

    # ---- 1 run ----
    started = min(s["retrieved_utc"] for s in splits.values())
    ended = max(s["retrieved_utc"] for s in splits.values())
    rec("run-eto-sft", "run", {
        "run_kind": "scrape",
        "tool": "curl",
        "tool_version": "https-get per-file",
        "started": started,
        "ended": ended,
        "params": {
            "inputs": [HF_URL + "/resolve/main/data"],
            "dataset_revision": REVISION,
            "method": "per-file https-get with sha256 sidecars (huggingface_hub "
                      "library broken on this VM; curl used)",
        },
        "coverage": {
            "complete": True,
            "scanned": n_rows,
            "total": n_rows,
            "description": "3 raw JSON files scraped at revision %s: alfworld "
                           "3119, scienceworld 1483, webshop 1824 rows "
                           "(6425 unique)." % REVISION,
        },
    }, {
        "dataset": HF_DATASET,
        "file_count": "3",
        "row_count": str(n_rows),
    })

    # ---- 1 dataset.snapshot ----
    rec("snap-eto-sft", "observation", {
        "type": "dataset.snapshot",
        "source": "@source-eto-sft",
        "run": "@run-eto-sft",
        "observed_at": ended,
        "time_basis": "collector_clock",
        "files": [],
        "data": {
            "dataset_uri": HF_URL,
            "revision": REVISION,
            "coverage": "complete",
            "row_count": n_rows,
            "unique_row_count": len(traj),
        },
    }, {"dataset": HF_DATASET, "revision": REVISION})

    # ---- 3 artifacts ----
    for split, s in splits.items():
        rec("art-" + split, "artifact", {
            "sha256": s["sha256"],
            "size": s["size"],
        }, {
            "filename": s["fname"],
            "raw_path": RAW_REL + "/" + s["fname"],
            "split": split,
        })

    # ---- 6425 lean dataset.record observations ----
    traj_ref = {}
    for (split, tid), info in sorted(traj.items()):
        r = info["record"]
        s = info["split_info"]
        convs = r.get("conversations", [])
        tref = "traj-%s-%s" % (split, tid)
        traj_ref[(split, tid)] = tref
        tags = {
            "id": tid,
            "split": split,
            "turn_count": str(len(convs)),
            "raw_path": RAW_REL + "/" + s["fname"],
            "file_sha256": s["sha256"],
        }
        if split == "webshop":
            tags["reward"] = str(r.get("reward"))
            tags["source"] = str(r.get("source"))
        rec(tref, "observation", {
            "type": "dataset.record",
            "source": "@source-eto-sft",
            "run": "@run-eto-sft",
            "observed_at": s["retrieved_utc"],
            "time_basis": "collector_clock",
            "files": [{
                "artifact": "@art-" + split,
                "role": "raw-trajectory",
                "filename": s["fname"],
            }],
            "data": {
                "snapshot": "@snap-eto-sft",
                "locator": {"artifact": "@art-" + split, "whole": True},
                "external_record_id": tid,
            },
        }, tags)

        rec("edge-run-%s-%s" % (split, tid), "edge", {
            "subject": "@run-eto-sft",
            "predicate": "related_to",
            "object": "@" + tref,
            "basis": "OBSERVED",
            "cites": ["@" + tref],
            "note": "scrape run produced the trajectory record",
        }, {"id": tid, "split": split})

    # ---- findings: intel.behavior + behavior.tool_sequence + edges ----
    findings_obs_mtime = findings_mtime
    import datetime
    obs_at_findings = datetime.datetime.fromtimestamp(
        findings_obs_mtime, tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for i, f in enumerate(findings):
        tid = base_tid(f["trajectory_id"])
        if tid.isdigit():
            split = "webshop"
        elif tid[0].isdigit():
            split = "scienceworld"
        else:
            split = "alfworld"
        key = (split, tid)
        if key not in traj:
            fail("finding %s trajectory %r not in raw bytes" % (f["finding_id"], tid))
        convs = traj[key]["record"].get("conversations", [])
        s = traj[key]["split_info"]
        tref = traj_ref[key]

        class_code = f.get("class", "OTHER")
        fref = "finding-eto-%02d" % (i + 1)
        lo, hi = parse_range(f["turn_range"])
        if lo < 0 or hi >= len(convs):
            fail("finding %s turn_range %s out of bounds (len %d)"
                 % (f["finding_id"], f["turn_range"], len(convs)))

        # tool sequence: decisive turns, recorded faithfully
        steps = []
        for ti in range(lo, hi + 1):
            t = convs[ti]
            frm = t.get("from")
            if frm not in ("human", "gpt"):
                fail("finding %s turn %d unexpected role %r" % (f["finding_id"], ti, frm))
            steps.append({
                "index": ti,
                "tool": "conversation.turn",
                "command": frm + ": " + t.get("value", ""),
            })
        sref = "seq-eto-%02d" % (i + 1)
        rec(sref, "observation", {
            "type": "behavior.tool_sequence",
            "source": "@source-eto-sft",
            "run": "@run-eto-sft",
            "observed_at": obs_at_findings,
            "time_basis": "source_metadata",
            "files": [{
                "artifact": "@art-" + split,
                "role": "evidence-trajectory",
                "filename": s["fname"],
            }],
            "data": {
                "trajectory": RAW_REL + "/" + s["fname"] + "#" + tid,
                "model": "unrecorded-in-source",
                "harness": split,
                "steps": steps,
                "length": len(steps),
                "provenance": "Decisive turn window %s from trajectory %s "
                              "(%d turns); steps are verbatim conversation "
                              "turns, not tool calls — turn-based SFT corpus."
                              % (f["turn_range"], tid, len(convs)),
            },
        }, {
            "finding_id": f["finding_id"],
            "trajectory_id": tid,
            "split": split,
            "turn_range": f["turn_range"],
            "turn_based": "true",
        })

        # intel.behavior
        desc = "[%s] %s" % (class_code, f["behavior"])
        rec(fref, "observation", {
            "type": "intel.behavior",
            "source": "@source-eto-sft",
            "run": "@run-eto-sft",
            "observed_at": obs_at_findings,
            "time_basis": "source_metadata",
            "files": [{
                "artifact": "@art-" + split,
                "role": "evidence-trajectory",
                "filename": s["fname"],
            }],
            "data": {
                "category": class_code.lower().replace("_", "-"),
                "description": desc,
                "evaluations_seen_on": ["eto-sft-trajectory"],
                "models_affected": [],
                "first_observed": "",
                "provenance": "ETO-SFT review fleet; verifier-graded findings "
                              "file working/verified-findings.json; quotes "
                              "byte-verified against raw JSON",
                "severity": "",
            },
        }, {
            "class_code": class_code,
            "grade": f.get("grade", ""),
            "confidence": f.get("confidence", ""),
            "confidence_reason": f.get("confidence_reason", ""),
            "turn_range": f["turn_range"],
            "evidence_quote": f.get("evidence_quote", ""),
            "verifier_note": f.get("verifier_note", ""),
            "finding_id": f["finding_id"],
            "trajectory_id": tid,
            "split": split,
            "finding_index": str(i + 1),
        })

        rec("edge-fseq-eto-%02d" % (i + 1), "edge", {
            "subject": "@" + sref,
            "predicate": "supports",
            "object": "@" + fref,
            "basis": "OBSERVED",
            "cites": ["@" + fref],
            "note": "decisive turn sequence evidences finding %s" % f["finding_id"],
        }, {"finding_id": f["finding_id"], "trajectory_id": tid})

        rec("edge-finding-eto-%02d" % (i + 1), "edge", {
            "subject": "@" + fref,
            "predicate": "supports",
            "object": "@" + tref,
            "basis": "OBSERVED",
            "cites": ["@" + fref],
            "note": "finding %s observed in trajectory %s turns %s"
                    % (f["finding_id"], tid, f["turn_range"]),
        }, {"finding_id": f["finding_id"], "trajectory_id": tid,
            "class_code": class_code})

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": "eto-sft-ingest-2026-10-17-v1",
        "lane": LANE,
        "records": records,
    }
    with open(OUT_BUNDLE, "w") as fh:
        json.dump(bundle, fh)

    kinds = Counter(r["kind"] for r in records)
    otypes = Counter(r["body"].get("type") for r in records
                     if r["kind"] == "observation")
    report = {
        "rows_total": n_rows,
        "trajectories_unique": len(traj),
        "dupe_skipped": dupe_events,
        "findings": len(findings),
        "record_count": len(records),
        "record_kinds": dict(kinds),
        "observation_types": dict(otypes),
        "sha256_bundle": hashlib.sha256(open(OUT_BUNDLE, "rb").read()).hexdigest(),
        "findings_observed_at": obs_at_findings,
        "revision": REVISION,
    }
    json.dump(report, open(OUT_REPORT, "w"), indent=1)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
