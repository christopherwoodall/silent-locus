#!/usr/bin/env python3
"""Build the factum ingest bundle for the SWE-smith-mini trajectory lane.

Regenerates bundle-swe-smith-mini.json from:
  - verified-findings.jsonl (7 byte-verified PRIMARY findings)
  - raw/*.parquet (40 sampled shards; byte checks per finding trajectory)

Graph: run -related_to-> dataset.record (trajectory) <-supports- intel.behavior (finding).
in_lane edges are auto-created by the top-level "lane" key (longrca pattern),
which requires the factum lane record to exist (see working/lane-new.log).
Without the lane record, submit WITHOUT the top-level "lane" key (wildclaw
pattern: tags.lane on every record carries the grouping).

Idempotency key: swe-smith-mini-ingest-2026-10-17-v1
Actor: agent:swe-smith-mini-ingestor

Validation gates (fail loudly):
  - every (shard,row) resolves to the expected instance_id (byte check)
  - every finding-level verbatim quote is a byte substring of the cited message
  - tags.lane on every record; ref uniqueness; ref <= 64 chars
  - no duplicate (shard,row) in the batch
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

import pyarrow.parquet as pq

LANE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(LANE_DIR, "raw")
FINDINGS = os.path.join(LANE_DIR, "verified-findings.jsonl")

LANE = "swe-smith-mini-trajectories"
DATASET = "Kwai-Klear/SWE-smith-mini_swe_agent_plus-trajectories-66k"
REVISION = "750b2c11239fd5e32f97e6cfb9bf80fb9a9a2983"
ACTOR = "agent:swe-smith-mini-ingestor"
IDEMPOTENCY_KEY = "swe-smith-mini-ingest-2026-10-17-v1"
RUN_STARTED = "2026-10-17T03:30:55Z"  # first shard GET in raw/download.log (real)

# Outcome-heuristic regexes (same as raw/outcome_heuristic.py)
RC_RE = re.compile(r"<returncode>(-?\d+)</returncode>")
MARKER_RE = re.compile(r"MINI_SWE_AGENT_FINAL_OUTPUT")
STUCK_RE = re.compile(
    r"(?i)\b(unable to|cannot|could not|failed to|give up|giving up|stuck|"
    r"exhausted|out of (steps|time|ideas)|no (further |more )?progress|"
    r"limit reached|max\w* steps)\b"
)
HEX_RE = re.compile(r"^[0-9a-f]{7,40}$")


def parse_bug_family(instance_id):
    """instance_id: <org>__<repo>.<commit>.<bug_type>[__<nonce>].

    Returns (org, repo, commit, bug_family). commit is the first all-hex
    token; repo may itself contain dots (e.g. pdfminer.six).
    """
    head, _, _nonce = instance_id.partition("__")  # org | rest...
    # careful: org itself has no '__'; the FIRST '__' separates org from rest
    first, sep, rest = instance_id.partition("__")
    org = first
    if sep:
        # rest = "<repo>.<commit>.<bug_type>[__<nonce>]"; strip trailing __nonce
        core = rest.split("__")[0]
    else:
        core = instance_id
    toks = core.split(".")
    commit_idx = None
    for i, t in enumerate(toks):
        if HEX_RE.match(t):
            commit_idx = i
            break
    assert commit_idx is not None, f"no commit token in {instance_id}"
    repo = ".".join(toks[:commit_idx])
    commit = toks[commit_idx]
    bug_family = ".".join(toks[commit_idx + 1 :])
    return org, repo, commit, bug_family


def outcome_proxy(messages):
    """Heuristic outcome classes (proxies, NOT ground truth)."""
    last_rc = None
    for x in messages:
        if x["role"] == "user":
            rcs = RC_RE.findall(x["content"])
            if rcs:
                last_rc = rcs[-1]
    last_a = ""
    for x in reversed(messages):
        if x["role"] == "assistant":
            last_a = x["content"]
            break
    classes = []
    if last_rc == "0":
        classes.append("C1")
    elif last_rc is None:
        classes.append("C2-no-rc")
    else:
        classes.append("C2")
    if STUCK_RE.search(last_a):
        classes.append("C3")
    return "+".join(classes)


def shard_file(num):
    return f"train-{int(num):05d}-of-00047.parquet"


def load_findings():
    out = []
    with open(FINDINGS) as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def collect_trajectories(findings):
    """Return list of dicts: finding_id, shard, row, iid, step_range,
    quote_step, verbatim_quote, cls, is_exemplar."""
    trajs = []
    for f in findings:
        fid = f["finding_id"]
        if fid in ("F-A-001", "F-A-002", "F-A-003", "F-A-004"):
            trajs.append({
                "finding_id": fid, "shard": f["shard"], "row": f["row"],
                "iid": f["trajectory_id"],
                "step_range": tuple(f["step_range"]),
                "quote_step": f["quote_step"],
                "verbatim_quote": f["verbatim_quote"],
                "cls": f["behavior_class"], "role": "primary",
            })
        elif fid == "F-B-001":
            for key in f["trajectory_keys"]:
                left, iid = key.split("=", 1)
                snum, rownum = left.split(",")
                trajs.append({
                    "finding_id": fid, "shard": shard_file(snum),
                    "row": int(rownum), "iid": iid,
                    "step_range": (46, 52) if (snum == "24" and rownum == "299") else None,
                    "quote_step": 48 if (snum == "24" and rownum == "299") else None,
                    "verbatim_quote": f["verbatim_quote"] if (snum == "24" and rownum == "299") else None,
                    "cls": f["behavior_class"],
                    "role": "exemplar" if (snum == "24" and rownum == "299") else "member",
                })
        elif fid == "F-B-002":
            for sc in f["sub_cases"]:
                trajs.append({
                    "finding_id": fid, "shard": sc["shard"], "row": sc["row"],
                    "iid": sc["iid"], "step_range": tuple(sc["steps"]),
                    "quote_step": None, "verbatim_quote": None,
                    "cls": f["behavior_class"], "role": "subcase",
                    "subclass": sc["class"],
                })
            # finding-level quote lives on the bleach trajectory
            for t in trajs:
                if t["finding_id"] == "F-B-002" and t["iid"] == f["trajectory_id"]:
                    t["quote_step"] = f["quote_step"]
                    t["verbatim_quote"] = f["verbatim_quote"]
                    t["role"] = "primary"
        elif fid == "F-B-004":
            for inst in f["instances"]:
                trajs.append({
                    "finding_id": fid, "shard": inst["shard"], "row": inst["row"],
                    "iid": inst["iid"], "step_range": tuple(inst["steps"]),
                    "quote_step": None, "verbatim_quote": None,
                    "cls": f["behavior_class"], "role": "subcase",
                })
            for t in trajs:
                if t["finding_id"] == "F-B-004" and t["iid"] == f["trajectory_id"]:
                    t["quote_step"] = f["quote_step"]
                    t["verbatim_quote"] = f["verbatim_quote"]
                    t["role"] = "primary"
    return trajs


def main():
    build_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    findings = load_findings()
    assert len(findings) == 7, f"expected 7 findings, got {len(findings)}"
    trajs = collect_trajectories(findings)

    # Dedup (shard,row): cantools r2b03pps is in F-B-002 and F-B-004.
    seen = {}
    for t in trajs:
        key = (t["shard"], t["row"])
        seen.setdefault(key, []).append(t)
    dupes = {k: v for k, v in seen.items() if len(v) > 1}
    assert set(dupes.keys()) == {("train-00044-of-00047.parquet", 1100)}, \
        f"unexpected duplicate trajectories: {list(dupes.keys())}"
    print(f"trajectory entries: {len(trajs)}, unique (shard,row): {len(seen)}",
          file=sys.stderr)

    # Byte checks: read each touched shard once, verify iid per row,
    # compute bug family + outcome proxy, byte-check the 7 quotes.
    # One shard at a time; release before the next (no cache: 24 shards
    # do not fit in RAM together under sibling contention).
    by_shard = {}
    for key, members in seen.items():
        by_shard.setdefault(key[0], []).append(key[1])

    def row_data(shard, rows):
        path = os.path.join(RAW, shard)
        tbl = pq.read_table(path, columns=["instance_id", "messages"])
        iids = tbl.column("instance_id").to_pylist()
        msgs = tbl.column("messages")
        out = {}
        for r in rows:
            out[r] = (iids[r], msgs[r].as_py())
        del tbl, iids, msgs
        return out

    for shard, rows in sorted(by_shard.items()):
        data = row_data(shard, rows)
        for row in rows:
            key = (shard, row)
            actual_iid, messages = data[row]
            for m in seen[key]:
                assert actual_iid == m["iid"], \
                    f"iid mismatch at {shard} row {row}: {actual_iid} != {m['iid']}"
            org, repo, commit, bug = parse_bug_family(actual_iid)
            oc = outcome_proxy(messages)
            for m in seen[key]:
                m["bug_family"] = bug
                m["outcome_proxy"] = oc
                m["n_msgs"] = len(messages)
                if m["verbatim_quote"]:
                    content = messages[m["quote_step"]]["content"]
                    assert m["verbatim_quote"] in content, \
                        f"QUOTE MISMATCH {m['finding_id']} {shard} row {row} step {m['quote_step']}"
        del data
        print(f"  shard {shard}: {len(rows)} rows checked", file=sys.stderr)
    print("byte checks passed: iid x%d, quotes x7" % len(seen), file=sys.stderr)

    # Shard sha256 + size for artifacts.
    shards = sorted({t["shard"] for t in trajs})
    shard_meta = {}
    for s in shards:
        sha_path = os.path.join(RAW, s + ".sha256")
        with open(sha_path) as fh:
            sha = fh.read().strip().split()[0]
        size = os.path.getsize(os.path.join(RAW, s))
        shard_meta[s] = {"sha256": sha, "size": size}
    print(f"artifacts: {len(shards)} shards", file=sys.stderr)

    records = []

    def add(rec):
        assert rec["tags"].get("lane") == LANE, \
            f"missing tags.lane on {rec.get('ref')}"
        assert len(rec["ref"]) <= 64, f"ref too long: {rec['ref']}"
        records.append(rec)

    # ---- source ----
    add({
        "ref": "source-swesmith-mini",
        "kind": "source",
        "body": {
            "source_type": "dataset",
            "locator": f"https://huggingface.co/datasets/{DATASET}",
            "platform": "huggingface",
            "title": f"{DATASET} @ {REVISION}",
        },
        "tags": {
            "lane": LANE,
            "license": "mit",
            "revision": REVISION,
            "sampling": ("stratified whole-shard drop (seed 151): dropped shards "
                         "13,18,22,23,26,40,45; kept 40/47 shards, 56166/65994 "
                         "trajectories (85.1%), 1.331GB of 1.58GB compressed"),
        },
    })

    # ---- run ----
    add({
        "ref": "run-swesmith-mini",
        "kind": "run",
        "body": {
            "run_kind": "scrape",
            "tool": "curl",
            "tool_version": "https-get",
            "started": RUN_STARTED,
            "ended": build_time,
            "params": {
                "inputs": [f"https://huggingface.co/datasets/{DATASET}/resolve/{REVISION}/<shard>.parquet"],
                "dataset_revision": REVISION,
                "method": ("curl -L -C - per-shard HTTPS GET with per-shard "
                           ".PROVENANCE.txt + .sha256 sidecars; stratified whole-shard "
                           "sampling (seed 151, worst org kept-share 77%); outcome "
                           "heuristic C1/C2/C3/C4 proxies over trajectory text; review "
                           "fleet (A/B) + adversarial reviewer + byte verifier"),
                "review": ("7 PRIMARY findings survive byte verification; kills in "
                           "data/lanes/swe-smith-mini-trajectories/working/verifier-kills.md"),
                "edge_scheme": ("run -related_to-> dataset.record; intel.behavior "
                                "-supports-> dataset.record; in_lane via top-level lane key"),
            },
            "coverage": {
                "complete": False,
                "scanned": 56166,
                "total": 65994,
                "description": ("56,166/65,994 trajectories (85.1%) across 40/47 shards; "
                                "7 verified PRIMARY findings filed over 93 finding-bearing trajectories"),
            },
        },
        "tags": {
            "lane": LANE,
            "dataset": DATASET,
            "revision": REVISION,
        },
    })

    # ---- snapshot ----
    add({
        "ref": "snapshot-swesmith-mini",
        "kind": "observation",
        "body": {
            "type": "dataset.snapshot",
            "source": "@source-swesmith-mini",
            "observed_at": RUN_STARTED,
            "time_basis": "source_metadata",
            "data": {
                "dataset_uri": f"huggingface://{DATASET}",
                "revision": REVISION,
                "coverage": "partial",
                "row_count": 56166,
            },
        },
        "tags": {
            "lane": LANE,
            "license": "mit",
            "outcome_mix": ("heuristic proxies, not ground truth: C1 clean-finish 98.65%, "
                            "C2 error-finish 1.35%, C3 give-up-language 3.13%"),
        },
    })

    # ---- artifacts (one per touched shard) ----
    art_ref = {}
    for s in shards:
        num = s.split("-")[1]
        ref = f"art-ssm-{num}"
        art_ref[s] = ref
        add({
            "ref": ref,
            "kind": "artifact",
            "body": {
                "sha256": shard_meta[s]["sha256"],
                "size": shard_meta[s]["size"],
            },
            "tags": {
                "lane": LANE,
                "filename": s,
                "format": "parquet",
                "raw_path": f"data/lanes/{LANE}/raw/{s}",
                "sidecar_sha256_file": s + ".sha256",
                "dataset_revision": REVISION,
            },
        })

    # ---- trajectory observations (dataset.record, one per unique shard,row) ----
    traj_ref = {}
    order = sorted(seen.keys())
    for n, key in enumerate(order, 1):
        shard, row = key
        members = seen[key]
        m0 = members[0]
        fids = sorted({m["finding_id"] for m in members})
        ref = f"traj-ssm-{n:03d}"
        traj_ref[key] = ref
        step_ranges = sorted({f"{m['step_range'][0]}-{m['step_range'][1]}"
                              for m in members if m["step_range"]})
        tags = {
            "lane": LANE,
            "trajectory_id": m0["iid"],
            "shard": shard,
            "row": str(row),
            "bug_family": m0["bug_family"],
            "outcome_proxy": m0["outcome_proxy"],
            "n_messages": str(m0["n_msgs"]),
            "finding_id": ",".join(fids),
            "anchor_note": ("instance_id is not a row key (many rollouts share ids); "
                            "anchored by shard+row"),
        }
        if step_ranges:
            tags["step_range"] = ",".join(step_ranges)
        add({
            "ref": ref,
            "kind": "observation",
            "body": {
                "type": "dataset.record",
                "source": "@source-swesmith-mini",
                "run": "@run-swesmith-mini",
                "observed_at": RUN_STARTED,
                "time_basis": "source_metadata",
                "files": [{
                    "artifact": f"@{art_ref[shard]}",
                    "role": "raw-trajectory-shard",
                    "filename": shard,
                }],
                "data": {
                    "snapshot": "@snapshot-swesmith-mini",
                    "locator": {"artifact": f"@{art_ref[shard]}", "whole": True},
                    "external_record_id": m0["iid"],
                },
            },
            "tags": tags,
        })

    # ---- intel.behavior (one per finding) ----
    CATEGORY = {
        "F-A-001": "test-expectation-rewriting",
        "F-A-002": "test-expectation-rewriting",
        "F-A-003": "test-expectation-rewriting",
        "F-A-004": "test-expectation-rewriting",
        "F-B-001": "test-addition-against-instruction",
        "F-B-002": "test-expectation-rewriting",
        "F-B-004": "submit-with-test-declared-wrong",
    }
    SEV = {"HIGH": "high", "MEDIUM": "moderate", "LOW": "low",
           "CRITICAL": "critical", "MINIMAL": "minimal"}
    beh_ref = {}
    for f in findings:
        fid = f["finding_id"]
        ref = "beh-ssm-" + fid.lower().replace("-", "")
        beh_ref[fid] = ref
        desc = build_description(f)
        add({
            "ref": ref,
            "kind": "observation",
            "body": {
                "type": "intel.behavior",
                "source": "@source-swesmith-mini",
                "observed_at": build_time,
                "time_basis": "collector_clock",
                "data": {
                    "category": CATEGORY[fid],
                    "description": desc,
                    "evaluations_seen_on": [DATASET],
                    "first_observed": "2026-10",
                    "models_affected": ["unrecorded-in-source"],
                    "severity": SEV[f["severity"]],
                    "provenance": build_provenance(f),
                },
            },
            "tags": {
                "lane": LANE,
                "finding_id": fid,
                "class": f["behavior_class"],
                "grade": f["grade"],
                "confidence": f["confidence"],
            },
        })

    # ---- edges ----
    en = 0
    for key in order:
        en += 1
        tref = traj_ref[key]
        members = seen[key]
        fids = sorted({m["finding_id"] for m in members})
        add({
            "ref": f"edge-run-ssm-{en:03d}",
            "kind": "edge",
            "body": {
                "subject": "@run-swesmith-mini",
                "predicate": "related_to",
                "object": f"@{tref}",
                "basis": "OBSERVED",
                "cites": [f"@{tref}"],
                "note": "acquire/review run produced the trajectory record",
            },
            "tags": {"lane": LANE, "finding_id": ",".join(fids),
                     "trajectory_id": members[0]["iid"]},
        })
    fn = 0
    for t in trajs:
        fn += 1
        key = (t["shard"], t["row"])
        add({
            "ref": f"edge-find-ssm-{fn:03d}",
            "kind": "edge",
            "body": {
                "subject": f"@{beh_ref[t['finding_id']]}",
                "predicate": "supports",
                "object": f"@{traj_ref[key]}",
                "basis": "OBSERVED",
                "cites": [f"@{beh_ref[t['finding_id']]}", f"@{traj_ref[key]}"],
                "note": f"finding {t['finding_id']} observed in trajectory {t['iid']}",
            },
            "tags": {"lane": LANE, "finding_id": t["finding_id"],
                     "trajectory_id": t["iid"]},
        })

    # ref uniqueness
    refs = [r["ref"] for r in records]
    assert len(refs) == len(set(refs)), "duplicate refs in bundle"

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": IDEMPOTENCY_KEY,
        "records": records,
    }
    out_path = os.path.join(LANE_DIR, "bundle-swe-smith-mini.json")
    with open(out_path, "w") as fh:
        json.dump(bundle, fh, indent=1)
        fh.write("\n")
    print(f"wrote {out_path}: {len(records)} records", file=sys.stderr)
    from collections import Counter
    print(Counter((r["kind"], r.get("body", {}).get("type", r.get("body", {}).get("predicate", "?")))
                  for r in records), file=sys.stderr)


def build_provenance(f):
    fid = f["finding_id"]
    if fid in ("F-A-001", "F-A-002", "F-A-003", "F-A-004"):
        loc = (f"{f['shard']} row {f['row']}, steps {f['step_range'][0]}-{f['step_range'][1]}; "
               f"raw bytes sha256={f['source_sha256']}")
    elif fid == "F-B-001":
        loc = (f"69 trajectories / 61 instance_ids across 20 shards (full key list in "
               f"verified-findings.jsonl); exemplar {f['trajectory_id']} {f['shard']} row {f['row']} "
               f"steps 46-52, raw bytes sha256={f['source_sha256']}")
    elif fid == "F-B-002":
        loc = (f"15 sub-cases across shards 14,25,29,32,33,34,35,37,39,43,44 "
               f"(iid/shard/row/steps per sub-case in verified-findings.jsonl); "
               f"primary {f['trajectory_id']} {f['shard']} row {f['row']}, "
               f"raw bytes sha256={f['source_sha256']}")
    else:
        loc = (f"6 instances across shards 24,29,31,36,44 "
               f"(iid/shard/row/steps per instance in verified-findings.jsonl); "
               f"primary {f['trajectory_id']} {f['shard']} row {f['row']}, "
               f"raw bytes sha256={f['source_sha256']}")
    return (f"{DATASET} @ {REVISION}; {loc}; "
            f"lane raw dir data/lanes/{LANE}/raw/")


def build_description(f):
    """Finding description: class/grade/confidence, verbatim quote, verifier notes."""
    fid = f["finding_id"]
    parts = [f"{fid} ({f['behavior_class']}, grade {f['grade']}, confidence {f['confidence']}):"]
    if fid in ("F-A-001", "F-A-002", "F-A-003", "F-A-004"):
        parts.append(f"Trajectory {f['trajectory_id']} ({f['shard']} row {f['row']}, "
                     f"steps {f['step_range'][0]}-{f['step_range'][1]}).")
        parts.append(f"Verbatim (step {f['quote_step']}): \"{f['verbatim_quote']}\"")
        parts.append(f"Verifier: {f['verifier_notes']}")
    elif fid == "F-B-001":
        parts.append(f"69 distinct (shard,row) trajectories / 61 distinct instance_ids "
                     f"append tests into the repo tree against the msg-1 boundary "
                     f"('DO NOT MODIFY: Tests'). Split: (a) appends to existing repo test "
                     f"files: 43 trajectories / 42 instance_ids; (b) new files inside the "
                     f"tree: 27 trajectories / 22 instance_ids (conan pr_15763 does both). "
                     f"Exemplar: {f['trajectory_id']} ({f['shard']} row {f['row']}, steps 46-52).")
        parts.append(f"Verbatim (exemplar, step {f['quote_step']}): \"{f['verbatim_quote']}\"")
        parts.append(f"Verifier: {f['verifier_notes']}")
    elif fid == "F-B-002":
        parts.append("15 sub-cases of expectation/fixture rewriting (11 confirmed incl. 5 "
                     "new from the byte-verifier's cp/mv scan; 4 boundary-by-letter weaker cases). "
                     f"Primary: {f['trajectory_id']} ({f['shard']} row {f['row']}, steps 68-69).")
        parts.append(f"Verbatim (primary, step {f['quote_step']}): \"{f['verbatim_quote']}\"")
        for sc in f["sub_cases"]:
            parts.append(f"- {sc['iid']} ({sc['shard']} row {sc['row']}, steps "
                         f"{sc['steps'][0]}-{sc['steps'][1]}, {sc['class']}): {sc['note']}")
        parts.append(f"Verifier: {f['verifier_notes']}")
    else:  # F-B-004
        parts.append("6 instances of submit-red-with-test-declared-wrong (5 + cantools cross-ref). "
                     f"Primary: {f['trajectory_id']} ({f['shard']} row {f['row']}, steps 71-76).")
        parts.append(f"Verbatim (primary, step {f['quote_step']}): \"{f['verbatim_quote']}\"")
        for inst in f["instances"]:
            parts.append(f"- {inst['iid']} ({inst['shard']} row {inst['row']}, steps "
                         f"{inst['steps'][0]}-{inst['steps'][1]}, {inst['severity']}): {inst['note']}")
        parts.append(f"Verifier: {f['verifier_notes']}")
    return "\n".join(parts)


if __name__ == "__main__":
    main()
