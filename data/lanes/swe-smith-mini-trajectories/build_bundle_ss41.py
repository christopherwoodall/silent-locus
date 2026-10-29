#!/usr/bin/env python3
"""Build the factum ingest bundle for the SWE-smith-mini trajectory lane.

Input: working/verifier-findings.jsonl (41 byte-verified findings SS-001..SS-041)
       raw/*.parquet (40 sampled shards)

Bundle (fallback scope, documented in REPORT.md):
  1 source + 1 run + 1 dataset.snapshot
  + 40 artifact (one per shard; sha256 + size; backs the locator refs)
  + 40 dataset.record (shard aggregates: n, outcome-proxy mix, msg quartiles,
    org/bug mix, sha256, path) 
  + 40 dataset.record (finding trajectories, lean attributes only;
    SS-010 is corpus-rate/MULTI and has no single trajectory)
  + 41 intel.behavior (full evidence per finding)
  + edges: run -related_to-> 80 records; intel.behavior -supports-> 40
    trajectories; SS-010 -supports-> dataset.snapshot (corpus-rate claim)

Graph: finding -supports-> trajectory -locator-> artifact(shard file) -> bytes.
in_lane via tags.lane on every record (no top-level "lane" key: the lane
record may not exist yet under lock contention; wildclaw pattern).

Idempotency key: swe-smith-mini-ingest-2026-10-17-v1
Actor: agent:swe-smith-mini-ingestor

Validation gates (fail loudly):
  - every non-MULTI finding's instance_id resolves to exactly one row in its
    shard (per-shard uniqueness asserted)
  - every verbatim_quote is a byte substring of the cited msg_range
  - tags.lane on every record; ref uniqueness; ref <= 64 chars
"""
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime, timezone

import pyarrow.parquet as pq

LANE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(LANE_DIR, "raw")
FINDINGS = os.path.join(LANE_DIR, "working", "verifier-findings.jsonl")

LANE = "swe-smith-mini-trajectories"
DATASET = "Kwai-Klear/SWE-smith-mini_swe_agent_plus-trajectories-66k"
REVISION = "750b2c11239fd5e32f97e6cfb9bf80fb9a9a2983"
ACTOR = "agent:swe-smith-mini-ingestor"
IDEMPOTENCY_KEY = "swe-smith-mini-ingest-2026-10-17-v1"
RUN_STARTED = "2026-10-17T03:30:55Z"  # first shard GET in raw/download.log

# Outcome-heuristic regexes (same as raw/outcome_heuristic.py)
RC_RE = re.compile(r"<returncode>(-?\d+)</returncode>")
STUCK_RE = re.compile(
    r"(?i)\b(unable to|cannot|could not|failed to|give up|giving up|stuck|"
    r"exhausted|out of (steps|time|ideas)|no (further |more )?progress|"
    r"limit reached|max\w* steps)\b"
)
HEX_RE = re.compile(r"^[0-9a-f]{7,40}$")


def parse_bug_family(instance_id):
    """instance_id: <org>__<repo>.<commit>.<bug_type>[__<nonce>]."""
    first, sep, rest = instance_id.partition("__")
    org = first
    core = rest.split("__")[0] if sep else instance_id
    toks = core.split(".")
    commit_idx = None
    for i, t in enumerate(toks):
        if HEX_RE.match(t):
            commit_idx = i
            break
    assert commit_idx is not None, f"no commit token in {instance_id}"
    repo = ".".join(toks[:commit_idx])
    commit = toks[commit_idx]
    bug_family = ".".join(toks[commit_idx + 1:])
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


CATEGORY = {
    # test-expectation-rewriting (taxonomy, SWE-smith-mini section)
    "SS-001": "test-expectation-rewriting", "SS-002": "test-expectation-rewriting",
    "SS-003": "test-expectation-rewriting", "SS-004": "test-expectation-rewriting",
    "SS-005": "test-expectation-rewriting", "SS-006": "test-expectation-rewriting",
    "SS-007": "test-expectation-rewriting", "SS-008": "test-expectation-rewriting",
    "SS-009": "test-expectation-rewriting", "SS-010": "test-expectation-rewriting",
    "SS-014": "test-expectation-rewriting", "SS-015": "test-expectation-rewriting",
    "SS-021": "test-expectation-rewriting", "SS-022": "test-expectation-rewriting",
    "SS-023": "test-expectation-rewriting", "SS-024": "test-expectation-rewriting",
    "SS-025": "test-expectation-rewriting", "SS-026": "test-expectation-rewriting",
    "SS-027": "test-expectation-rewriting", "SS-028": "test-expectation-rewriting",
    "SS-029": "test-expectation-rewriting", "SS-030": "test-expectation-rewriting",
    "SS-031": "test-expectation-rewriting", "SS-032": "test-expectation-rewriting",
    "SS-034": "test-expectation-rewriting", "SS-035": "test-expectation-rewriting",
    "SS-036": "test-expectation-rewriting", "SS-037": "test-expectation-rewriting",
    "SS-038": "test-expectation-rewriting", "SS-039": "test-expectation-rewriting",
    "SS-040": "test-expectation-rewriting", "SS-041": "test-expectation-rewriting",
    # test-addition-against-instruction (taxonomy, SWE-smith-mini section)
    "SS-013": "test-addition-against-instruction",
    "SS-016": "test-addition-against-instruction",
    # submit-with-test-declared-wrong (taxonomy, SWE-smith-mini section)
    "SS-018": "submit-with-test-declared-wrong",
    # destructive-action (taxonomy, ActBench section; benchmark-scoped attempt)
    "SS-017": "destructive-action",
    # self-correcting-recovery (taxonomy, TauBench section; positive control)
    "SS-011": "self-correcting-recovery",
    # PROPOSED categories (no established slug fits; see REPORT.md taxonomy gaps)
    "SS-019": "deliberate-bug-introduction",
    "SS-020": "deliberate-bug-introduction",
    "SS-033": "deliberate-bug-introduction",
    "SS-012": "pr-description-anchoring",
}
PROPOSED = {"deliberate-bug-introduction", "pr-description-anchoring"}

SEV = {"HIGH": "high", "MEDIUM": "moderate", "LOW": "low"}


def load_findings():
    out = []
    with open(FINDINGS) as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def quartile(sorted_vals, q):
    if not sorted_vals:
        return 0
    idx = int(q * (len(sorted_vals) - 1))
    return sorted_vals[idx]


def main():
    build_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    findings = load_findings()
    assert len(findings) == 41, f"expected 41 findings, got {len(findings)}"
    assert set(CATEGORY.keys()) == {f["id"] for f in findings}, "category map mismatch"

    # ---- pass 1: resolve finding trajectories + per-shard aggregates ----
    # one shard at a time; release before the next
    by_shard = {}
    for f in findings:
        if f["instance_id"] != "MULTI":
            by_shard.setdefault(f["shard_file"], []).append(f)

    traj = {}  # finding_id -> dict(row, iid, n_msgs, outcome, org, repo, bug)
    shard_agg = {}  # shard_file -> dict
    quote_checks = 0
    for shard, fs in sorted(by_shard.items()):
        path = os.path.join(RAW, shard)
        tbl = pq.read_table(path, columns=["instance_id", "messages"])
        iids = tbl.column("instance_id").to_pylist()
        msgs_col = tbl.column("messages")

        # per-shard aggregates over all rows
        n = len(iids)
        msg_lens = []
        oc = Counter()
        orgs = Counter()
        bugs = Counter()
        row_cache = {}
        for r in range(n):
            iid = iids[r]
            try:
                org, repo, _commit, bug = parse_bug_family(iid)
            except AssertionError:
                org, repo, bug = iid.split("__")[0], "?", "?"
            orgs[org] += 1
            bugs[bug] += 1
            m = msgs_col[r].as_py()
            row_cache[r] = m
            msg_lens.append(len(m))
            for c in outcome_proxy(m).split("+"):
                oc[c] += 1
        sl = sorted(msg_lens)
        with open(os.path.join(RAW, shard + ".sha256")) as fh:
            sha = fh.read().strip().split()[0]
        shard_agg[shard] = {
            "n": n, "sha256": sha, "size": os.path.getsize(path),
            "msg_min": sl[0], "msg_q1": quartile(sl, 0.25),
            "msg_median": quartile(sl, 0.5), "msg_q3": quartile(sl, 0.75),
            "msg_max": sl[-1],
            "outcome": dict(oc),
            "top_orgs": orgs.most_common(5),
            "bugs": dict(bugs),
        }

        # resolve finding rows (per-shard instance_id uniqueness asserted)
        for f in fs:
            matches = [r for r in range(n) if iids[r] == f["instance_id"]]
            assert len(matches) == 1, \
                f"{f['id']}: {len(matches)} rows for {f['instance_id']} in {shard}"
            row = matches[0]
            m = row_cache[row]
            org, repo, _commit, bug = parse_bug_family(f["instance_id"])
            traj[f["id"]] = {
                "row": row, "iid": f["instance_id"], "n_msgs": len(m),
                "outcome": outcome_proxy(m), "org": org, "repo": repo,
                "bug": bug, "shard": shard,
            }
            # byte-check the verbatim quote inside the cited msg_range
            q = f.get("verbatim_quote")
            mr = f.get("msg_range")
            if q and isinstance(mr, list) and len(mr) == 2:
                span = " ".join(x["content"] for x in m[mr[0]:mr[1] + 1])
                assert q in span, f"QUOTE MISMATCH {f['id']} {shard} row {row}"
                quote_checks += 1
        del tbl, iids, msgs_col, row_cache
        print(f"  shard {shard}: {n} rows, {len(fs)} findings resolved",
              file=sys.stderr)

    # shards with no findings still need aggregates
    import glob
    all_shards = sorted(os.path.basename(p)
                        for p in glob.glob(os.path.join(RAW, "train-*-of-00047.parquet")))
    assert len(all_shards) == 40, f"expected 40 shards, got {len(all_shards)}"
    for shard in all_shards:
        if shard in shard_agg:
            continue
        path = os.path.join(RAW, shard)
        tbl = pq.read_table(path, columns=["instance_id", "messages"])
        iids = tbl.column("instance_id").to_pylist()
        msgs_col = tbl.column("messages")
        n = len(iids)
        msg_lens, oc, orgs, bugs = [], Counter(), Counter(), Counter()
        for r in range(n):
            iid = iids[r]
            try:
                org, _repo, _c, bug = parse_bug_family(iid)
            except AssertionError:
                org, bug = iid.split("__")[0], "?"
            orgs[org] += 1
            bugs[bug] += 1
            m = msgs_col[r].as_py()
            msg_lens.append(len(m))
            for c in outcome_proxy(m).split("+"):
                oc[c] += 1
        sl = sorted(msg_lens)
        with open(os.path.join(RAW, shard + ".sha256")) as fh:
            sha = fh.read().strip().split()[0]
        shard_agg[shard] = {
            "n": n, "sha256": sha, "size": os.path.getsize(path),
            "msg_min": sl[0], "msg_q1": quartile(sl, 0.25),
            "msg_median": quartile(sl, 0.5), "msg_q3": quartile(sl, 0.75),
            "msg_max": sl[-1],
            "outcome": dict(oc),
            "top_orgs": orgs.most_common(5),
            "bugs": dict(bugs),
        }
        del tbl, iids, msgs_col
        print(f"  shard {shard}: {n} rows (aggregate only)", file=sys.stderr)

    assert len(traj) == 40, f"expected 40 resolved trajectories, got {len(traj)}"
    assert len(shard_agg) == 40
    print(f"byte checks passed: rows x40, quotes x{quote_checks}", file=sys.stderr)

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
            "run_kind": "ingest",
            "tool": "curl",
            "tool_version": "https-get",
            "started": RUN_STARTED,
            "ended": build_time,
            "params": {
                "inputs": [f"https://huggingface.co/datasets/{DATASET}/resolve/{REVISION}/<shard>.parquet"],
                "dataset_revision": REVISION,
                "method": ("curl -L -C - per-shard HTTPS GET with per-shard "
                           ".PROVENANCE.txt + .sha256 sidecars; stratified whole-shard "
                           "sampling (seed 151); outcome heuristic C1/C2/C3 proxies over "
                           "trajectory text; review fleet (A/B) + adversarial reviewer + "
                           "byte verifier; factum bundle built by agent:swe-smith-mini-ingestor"),
                "review": ("41 findings survive byte verification (34 GUARDRAIL, 1 "
                           "IRREVERSIBLE attempt, 6 OTHER); kills/downgrades in "
                           "working/verifier-kills.md and working/verifier-killed.jsonl"),
                "edge_scheme": ("run -related_to-> dataset.record; intel.behavior "
                                "-supports-> dataset.record (SS-010 -supports-> "
                                "dataset.snapshot, corpus-rate claim); in_lane via tags.lane"),
                "scope_note": ("fallback scope under lock contention: 40 shard aggregates + "
                               "40 finding-trajectory records instead of 56,166 per-trajectory "
                               "records; see REPORT.md"),
            },
            "coverage": {
                "complete": False,
                "scanned": 56166,
                "total": 65994,
                "description": ("56,166/65,994 trajectories (85.1%) across 40/47 shards; "
                                "41 verified findings filed; 40 finding-bearing trajectories "
                                "recorded individually, 40 shards aggregated"),
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
            "files": [],
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
                            "C2 error-finish 1.35%, C3 give-up-language 3.13%; "
                            "msg quartiles Q1<=47 median=63 Q3<=85"),
            "rewrite_rate": ("SS-010: 120/145 (82.8%) of in-place test edits after "
                             "observed failure were genuine expectation-rewrites"),
        },
    })

    # ---- artifacts (one per shard) ----
    art_ref = {}
    for s in sorted(shard_agg):
        num = s.split("-")[1]
        ref = f"art-ssm-{num}"
        art_ref[s] = ref
        add({
            "ref": ref,
            "kind": "artifact",
            "body": {
                "sha256": shard_agg[s]["sha256"],
                "size": shard_agg[s]["size"],
            },
            "tags": {
                "lane": LANE,
                "filename": s,
                "format": "parquet",
                "raw_path": f"data/lanes/{LANE}/raw/{s}",
                "sidecar_sha256_file": s + ".sha256",
                "dataset_revision": REVISION,
                "retention": "local-only",
            },
        })
    print(f"artifacts: {len(art_ref)} shards", file=sys.stderr)

    # ---- shard-aggregate dataset.records ----
    agg_ref = {}
    for i, s in enumerate(sorted(shard_agg), 1):
        a = shard_agg[s]
        ref = f"shardagg-ssm-{i:02d}"
        agg_ref[s] = ref
        oc = a["outcome"]
        add({
            "ref": ref,
            "kind": "observation",
            "body": {
                "type": "dataset.record",
                "source": "@source-swesmith-mini",
                "run": "@run-swesmith-mini",
                "observed_at": RUN_STARTED,
                "time_basis": "source_metadata",
                "files": [{"artifact": f"@{art_ref[s]}",
                           "role": "raw-trajectory-shard", "filename": s}],
                "data": {
                    "snapshot": "@snapshot-swesmith-mini",
                    "locator": {"artifact": f"@{art_ref[s]}", "whole": True},
                    "external_record_id": s,
                },
            },
            "tags": {
                "lane": LANE,
                "record_kind": "shard_aggregate",
                "shard_file": s,
                "n_trajectories": str(a["n"]),
                "sha256": a["sha256"],
                "size_bytes": str(a["size"]),
                "outcome_C1": str(oc.get("C1", 0)),
                "outcome_C2": str(oc.get("C2", 0)),
                "outcome_C2_no_rc": str(oc.get("C2-no-rc", 0)),
                "outcome_C3": str(oc.get("C3", 0)),
                "msg_min": str(a["msg_min"]), "msg_q1": str(a["msg_q1"]),
                "msg_median": str(a["msg_median"]), "msg_q3": str(a["msg_q3"]),
                "msg_max": str(a["msg_max"]),
                "top_orgs": ",".join(f"{o}:{c}" for o, c in a["top_orgs"]),
                "bug_mix": ",".join(f"{b}:{c}"
                                    for b, c in sorted(a["bugs"].items())),
                "anchor_note": ("aggregate over whole shard; per-trajectory rows "
                                "keyed by (shard_file, instance_id); instance_id "
                                "repeats across shards"),
            },
        })

    # ---- finding-trajectory dataset.records (lean, no step content) ----
    traj_ref = {}
    for n, fid in enumerate(sorted(traj), 1):
        t = traj[fid]
        f = next(x for x in findings if x["id"] == fid)
        ref = f"traj-ssm-{n:02d}"
        traj_ref[fid] = ref
        mr = f["msg_range"]
        add({
            "ref": ref,
            "kind": "observation",
            "body": {
                "type": "dataset.record",
                "source": "@source-swesmith-mini",
                "run": "@run-swesmith-mini",
                "observed_at": RUN_STARTED,
                "time_basis": "source_metadata",
                "files": [{"artifact": f"@{art_ref[t['shard']]}",
                           "role": "raw-trajectory-shard",
                           "filename": t["shard"]}],
                "data": {
                    "snapshot": "@snapshot-swesmith-mini",
                    "locator": {"artifact": f"@{art_ref[t['shard']]}",
                                "row": {"index": t["row"]}},
                    "external_record_id": t["iid"],
                },
            },
            "tags": {
                "lane": LANE,
                "record_kind": "finding_trajectory",
                "finding_id": fid,
                "trajectory_id": t["iid"],
                "shard_file": t["shard"],
                "row": str(t["row"]),
                "org": t["org"],
                "repo": t["repo"],
                "bug_type": t["bug"],
                "outcome_proxy": t["outcome"],
                "n_messages": str(t["n_msgs"]),
                "msg_range": f"{mr[0]}-{mr[1]}" if isinstance(mr, list) else str(mr),
                "class": f["class"],
                "grade": f["grade"],
                "confidence": f["confidence"],
                "anchor_note": ("instance_id is not a row key (10,894 distinct ids "
                                "over 56,166 rows); anchored by shard_file+row"),
            },
        })

    # ---- intel.behavior (one per finding) ----
    beh_ref = {}
    for f in findings:
        fid = f["id"]
        ref = "beh-ssm-" + fid.lower().replace("-", "")
        beh_ref[fid] = ref
        cat = CATEGORY[fid]
        tags = {
            "lane": LANE,
            "finding_id": fid,
            "class": f["class"],
            "grade": f["grade"],
            "confidence": f["confidence"],
            "category": cat,
        }
        if cat in PROPOSED:
            tags["taxonomy_proposed"] = "true"
        if f["instance_id"] != "MULTI":
            t = traj[fid]
            tags["trajectory_id"] = t["iid"]
            tags["shard_file"] = t["shard"]
            tags["row"] = str(t["row"])
        desc = build_description(f, traj.get(fid))
        add({
            "ref": ref,
            "kind": "observation",
            "body": {
                "type": "intel.behavior",
                "source": "@source-swesmith-mini",
                "observed_at": build_time,
                "time_basis": "collector_clock",
                "files": [],
                "data": {
                    "category": cat,
                    "description": desc,
                    "evaluations_seen_on": [DATASET],
                    "first_observed": "2026-10",
                    "models_affected": ["unrecorded-in-source"],
                    "severity": SEV[f["grade"]],
                    "provenance": build_provenance(f, traj.get(fid)),
                },
            },
            "tags": tags,
        })

    # ---- edges ----
    en = 0
    for ref in sorted(agg_ref.values()) + sorted(traj_ref.values()):
        en += 1
        add({
            "ref": f"edge-run-ssm-{en:03d}",
            "kind": "edge",
            "body": {
                "subject": "@run-swesmith-mini",
                "predicate": "related_to",
                "object": f"@{ref}",
                "basis": "OBSERVED",
                "cites": [f"@{ref}"],
                "note": "acquire/review run produced the dataset record",
            },
            "tags": {"lane": LANE},
        })
    fn = 0
    for f in findings:
        fn += 1
        fid = f["id"]
        if fid == "SS-010":
            obj, note = "@snapshot-swesmith-mini", \
                "SS-010 is a corpus-rate claim; supports the dataset snapshot"
        else:
            obj = f"@{traj_ref[fid]}"
            note = f"finding {fid} observed in trajectory {traj[fid]['iid']}"
        add({
            "ref": f"edge-find-ssm-{fn:02d}",
            "kind": "edge",
            "body": {
                "subject": f"@{beh_ref[fid]}",
                "predicate": "supports",
                "object": obj,
                "basis": "OBSERVED",
                "cites": [f"@{beh_ref[fid]}", obj],
                "note": note,
            },
            "tags": {"lane": LANE, "finding_id": fid},
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
    out_path = os.path.join(LANE_DIR, "bundle-ss41-swe-smith-mini.json")
    with open(out_path, "w") as fh:
        json.dump(bundle, fh, indent=1)
        fh.write("\n")
    print(f"wrote {out_path}: {len(records)} records", file=sys.stderr)
    print(Counter((r["kind"], r.get("body", {}).get("type",
                  r.get("body", {}).get("predicate", "?")))
                  for r in records), file=sys.stderr)


def build_provenance(f, t):
    base = f"{DATASET} @ {REVISION}; lane raw dir data/lanes/{LANE}/raw/"
    if f["instance_id"] == "MULTI":
        return (base + " corpus-rate over Reviewer A slice (20 shards); "
                "adjudications in working/deepread_a/strong_verdicts.json; "
                "verifier re-derivation in SS-010 verifier_note")
    return (base + f" {t['shard']} row {t['row']}, msgs {f['msg_range']}; "
            f"byte-verified against parquet bytes")


def build_description(f, t):
    """Finding description: class/grade/confidence, anchor, verbatim quote,
    why-interesting, adversarial and verifier notes."""
    fid = f["id"]
    parts = [f"{fid} ({f['class']}, grade {f['grade']}, "
             f"confidence {f['confidence']}):"]
    if f["instance_id"] == "MULTI":
        parts.append("Corpus-rate pattern (no single trajectory).")
    else:
        mr = f["msg_range"]
        parts.append(f"Trajectory {t['iid']} ({t['shard']} row {t['row']}, "
                     f"msgs {mr[0]}-{mr[1]}).")
    if f.get("verbatim_quote"):
        parts.append(f"Verbatim: \"{f['verbatim_quote']}\"")
    parts.append(f"Why interesting: {f['why_interesting']}")
    if f.get("adversarial_note"):
        parts.append(f"Adversarial: {f['adversarial_note']}")
    if f.get("verifier_note"):
        parts.append(f"Verifier: {f['verifier_note']}")
    return " ".join(parts)


if __name__ == "__main__":
    main()
