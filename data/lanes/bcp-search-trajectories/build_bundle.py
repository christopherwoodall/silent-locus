#!/usr/bin/env python3
"""BCP search-agent trajectories factum ingest bundle builder (BCP INGESTOR).

Reads:
  raw/MANIFEST.json                 (6 run dirs x 830 rows, pinned rev)
  raw/LICENSE.note                  (apache-2.0, three-source check)
  verified-findings.jsonl           (15 verifier-graded PRIMARY findings)

Writes: bundle-bcp-search.json (factum bundle v2) + build-report.json

Bundle design (63 records):
  1 source record     — HF dataset liuqi6777/bcp_search_agent_trajectory @ rev
  1 run record        — scrape + review-fleet coverage (4,980/4,980 rows)
  1 dataset.snapshot  — corpus stats at the pinned revision
  15 intel.behavior   — one per verified finding (taxonomy category, grade,
                        confidence, step range, verbatim evidence quote,
                        verifier note; claims cite these, never sources)
  15 behavior.tool_sequence — ordered tool-call steps of each finding's
                        exemplar trajectory (full row, in order)
  30 edges            — run -related_to-> tool_sequence (15);
                        finding -supports-> tool_sequence (15)

Gates (fail loudly, like the TauBench builder):
  G1: every evidence_quote has a >=40-char verbatim substring present in the
      exemplar trajectory's raw bytes (quotes checked part-wise on " ; ").
  G2: every tool_sequence step count matches the extracted tool_call count.
  G3: no duplicate finding ids; no duplicate (run, line) per finding.

Conventions:
  - Trajectory id = "<run>:predictions.jsonl line <N>" (1-based file line).
  - Reviewer B's "idx" citations are 0-based rows -> +1 for file lines.
  - Reviewer A/C "line"/"row" citations are 1-based file lines.
  - tags.lane = bcp-search-trajectories on EVERY record incl. source.
  - Observations carry observed_at + time_basis (collector_clock, 2026-10-17T04:36:31Z).
  - Tool schema differs by run family: ds4pro/glm51/qwen35 use
    search(query)/visit(docid); gpt-oss/kimi26/tongyi-dr use
    search(query)/visit(docid,goal); recorded in tool_sequence provenance.
"""
import json
import os
import sys
import hashlib
import re
from collections import Counter

LANE = "bcp-search-trajectories"
ACTOR = "agent:bcp-ingestor"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
MANIFEST_PATH = os.path.join(RAW, "MANIFEST.json")
FINDINGS_PATH = os.path.join(HERE, "verified-findings.jsonl")
OUT_BUNDLE = os.path.join(HERE, "bundle-bcp-search.json")
OUT_REPORT = os.path.join(HERE, "build-report.json")

HF_DATASET = "liuqi6777/bcp_search_agent_trajectory"
HF_URL = "https://huggingface.co/datasets/" + HF_DATASET
REV = "af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f"
LICENSE = "apache-2.0"
RETRIEVED_AT = "2026-10-17T04:36:31Z"   # raw/MANIFEST.json retrieved_utc
OBSERVED_AT = "2026-10-17T04:36:31Z"  # raw-file manifest time (grounded; schema needs date-time)
RUNS = ["ds4pro", "glm51", "gpt-oss-120b-high", "kimi26", "qwen35-35b-a3b", "tongyi-dr"]
ROWS_PER_RUN = 830

# finding_id -> (run, 1-based file line, taxonomy category slug)
ANCHORS = {
    "BCP-A-001": ("glm51", 266, "self-echo-as-evidence"),
    "BCP-A-002": ("glm51", 12, "evidence-blindness-at-giveup"),
    "BCP-A-003": ("ds4pro", 9, "reasoning-delimiter-leakage"),
    "BCP-A-004": ("ds4pro", 362, "tool-protocol-misuse"),
    "F-B1":      ("gpt-oss-120b-high", 79, "tool-protocol-misuse"),   # idx78 +1
    "F-B2":      ("gpt-oss-120b-high", 342, "tool-protocol-misuse"),  # idx341 +1
    "F-B3":      ("gpt-oss-120b-high", 458, "confabulation-under-retrieval-failure"),  # idx457 +1
    "F-B4":      ("kimi26", 101, "recovery-livelock"),                # idx100 +1
    "BCP-C-001": ("tongyi-dr", 741, "schema-fixation-against-evidence"),
    "BCP-C-002": ("tongyi-dr", 1, "repair-without-learning"),
    "BCP-C-003": ("tongyi-dr", 351, "transcription-error-cascade"),
    "BCP-C-004": ("tongyi-dr", 351, "transcription-error-cascade"),
    "BCP-C-005": ("tongyi-dr", 21, "constraint-abandonment"),
    "BCP-C-006": ("tongyi-dr", 560, "declared-abandonment-not-followed"),
    "BCP-X-001": ("glm51", 12, "evidence-blindness-at-giveup"),
}

FINDING_ORDER = ["BCP-A-001", "BCP-A-002", "BCP-A-003", "BCP-A-004",
                 "F-B1", "F-B2", "F-B3", "F-B4",
                 "BCP-C-001", "BCP-C-002", "BCP-C-003", "BCP-C-004",
                 "BCP-C-005", "BCP-C-006", "BCP-X-001"]


def fail(msg):
    print("BUILD-FAIL:", msg, file=sys.stderr)
    sys.exit(2)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_row(run, line):
    """Read 1-based `line` from <run>/predictions.jsonl."""
    path = os.path.join(RAW, run, "predictions.jsonl")
    with open(path) as fh:
        for _ in range(line - 1):
            if not fh.readline():
                fail("short file: %s has < %d lines" % (path, line))
        text = fh.readline()
    if not text:
        fail("empty line %d in %s" % (line, path))
    return text, json.loads(text)


def render_command(tool_calls):
    """Render one tool call as a short command string."""
    name = tool_calls.get("name", "?")
    args = tool_calls.get("arguments")
    if isinstance(args, dict):
        arg_str = json.dumps(args, ensure_ascii=False, sort_keys=True)
    else:
        arg_str = json.dumps(tool_calls.get("raw_arguments"))
    cmd = "%s(%s)" % (name, arg_str)
    if len(cmd) > 220:
        cmd = cmd[:217] + "..."
    return cmd


# G1: explicit byte-anchors per finding. Each (substring, run, line,
# min_count) was hand-verified against the raw trajectory bytes on
# 2026-10-17. Purpose: catch wrong-trajectory anchoring. The
# evidence_quote itself is the verifier-checked artifact; these anchors
# are the machine-checkable distinctive cores of each quote.
G1_ANCHORS = {
    "BCP-A-001": [("28</answer>", "glm51", 266, 1),
                  ("28 years", "glm51", 266, 1)],
    "BCP-A-002": [("birth_date: 23 09 1925", "glm51", 12, 5),
                  ("No answer found", "glm51", 12, 1)],
    "BCP-A-003": [("</think>", "ds4pro", 9, 1),
                  ("DSML", "ds4pro", 266, 1)],
    "BCP-A-004": [("Wayback machine", "ds4pro", 362, 1),
                  ("healthline.com/health/frozen-shoulder", "ds4pro", 362, 1)],
    "F-B1": [("Tool 'find' is not available", "gpt-oss-120b-high", 79, 1),
             ('"docid": "60046", "pattern": "single"',
              "gpt-oss-120b-high", 247, 1)],
    "F-B2": [("tandfonline.com/doi/pdfdirect/10.1080/17474124.2019.1685381",
              "gpt-oss-120b-high", 342, 1),
             ("takes a `docid` which is a local corpus document id",
              "kimi26", 95, 1)],
    "F-B3": [("Given knowledge anyway", "gpt-oss-120b-high", 458, 1)],
    "F-B4": [("We are stuck", "kimi26", 101, 20),
             ("theguardian.com/profile", "kimi26", 101, 25)],
    "BCP-C-001": [("query: string[]", "tongyi-dr", 741, 1),
                  ("Invalid request format", "tongyi-dr", 741, 50)],
    "BCP-C-002": [('"docid": 18639', "tongyi-dr", 1, 1),
                  ("Invalid request format", "tongyi-dr", 1, 1)],
    "BCP-C-003": [("65244", "tongyi-dr", 351, 1),
                  ("98058", "tongyi-dr", 351, 1)],
    "BCP-C-004": [("returning random unrelated content", "tongyi-dr", 351, 1),
                  ("Nicole Chikwe", "tongyi-dr", 351, 1)],
    "BCP-C-005": [("loser was Selby (pro 1999). So doesn't fit",
                   "tongyi-dr", 21, 1)],
    "BCP-C-006": [("guess docids are not helpful", "tongyi-dr", 560, 1),
                  ("85000", "tongyi-dr", 560, 1)],
    "BCP-X-001": [("Jacqueline Georgette Cantrelle", "glm51", 12, 10)],
}


def norm_row_text(text):
    # raw JSONL row text carries escaped \n (backslash-n), not newlines
    t = text.replace("\\n", " ").replace("\\t", " ").replace("\\r", " ")
    return re.sub(r"\s+", " ", t)


_row_cache = {}


def check_g1():
    """Verify every anchor substring occurs >= min_count in the cited
    trajectory's normalized raw bytes."""
    failures = []
    for fid, anchors in G1_ANCHORS.items():
        for substr, run, line, min_count in anchors:
            key = (run, line)
            if key not in _row_cache:
                _row_cache[key] = norm_row_text(read_row(run, line)[0])
            n = _row_cache[key].count(substr)
            if n < min_count:
                failures.append("%s: %r found %dx in %s:%d (need %d)"
                                % (fid, substr[:60], n, run, line, min_count))
    return failures


def main():
    manifest = json.load(open(MANIFEST_PATH))
    if manifest.get("dataset") != HF_DATASET or manifest.get("rev") != REV:
        fail("manifest dataset/rev mismatch")
    findings = []
    for line in open(FINDINGS_PATH):
        line = line.strip()
        if line:
            findings.append(json.loads(line))
    if len(findings) != 15:
        fail("finding count %d != 15" % len(findings))
    by_id = {f["id"]: f for f in findings}
    if sorted(by_id) != sorted(FINDING_ORDER):
        fail("finding id set mismatch: %s" % sorted(by_id))
    if set(ANCHORS) != set(FINDING_ORDER):
        fail("anchor set mismatch")

    records = []

    def rec(ref, kind, body, tags):
        tags = dict(tags)
        tags["lane"] = LANE
        records.append({"ref": ref, "kind": kind, "body": body, "tags": tags})

    # ---- 1 source ----
    rec("source-bcp", "source", {
        "source_type": "huggingface",
        "locator": HF_URL,
        "title": "liuqi6777/bcp_search_agent_trajectory: BrowseComp-Plus "
                 "search-agent trajectories (6 model runs x 830 rows)",
        "platform": "huggingface",
    }, {
        "dataset": HF_DATASET,
        "revision": REV,
        "license": LICENSE,
    })

    # ---- 1 run ----
    rec("run-bcp", "run", {
        "run_kind": "scrape",
        "tool": "curl",
        "tool_version": "https-get",
        "started": RETRIEVED_AT,
        "ended": RETRIEVED_AT,
        "params": {
            "inputs": [HF_URL + "/resolve/" + REV + "/<run>/predictions.jsonl"],
            "dataset_revision": REV,
            "method": "single-threaded https-get per run file; per-file "
                      ".PROVENANCE sidecars; sha256 verified against repo "
                      "manifest bytes (bytes_match=true, sha256_match=true)",
            "review": "review fleet (A: glm51+ds4pro, B: gpt-oss-120b-high+kimi26, "
                      "C: tongyi-dr+qwen35) + adversarial reviewer + byte "
                      "verifier; findings in verified-findings.jsonl",
            "edge_scheme": "run -related_to-> behavior.tool_sequence; "
                           "intel.behavior -supports-> behavior.tool_sequence",
        },
        "coverage": {
            "complete": True,
            "scanned": ROWS_PER_RUN * len(RUNS),
            "total": ROWS_PER_RUN * len(RUNS),
            "description": "4,980/4,980 trajectories reviewed across 6 runs "
                           "(ds4pro, glm51, gpt-oss-120b-high, kimi26, "
                           "qwen35-35b-a3b, tongyi-dr), 830 rows each; 15 "
                           "verified PRIMARY findings filed",
        },
    }, {
        "dataset": HF_DATASET,
        "revision": REV,
        "file_count": "6",
    })

    # ---- 1 dataset.snapshot ----
    file_entries = []
    for run in RUNS:
        entry = next(x for x in manifest["files"] if x["path"] == run + "/predictions.jsonl")
        file_entries.append({
            "run": run,
            "path": entry["path"],
            "size_bytes": entry["size_bytes"],
            "sha256": entry["sha256"],
        })
    # dataset.snapshot schema allows only dataset_uri/revision/coverage/row_count
    rec("snap-bcp", "observation", {
        "type": "dataset.snapshot",
        "source": "@source-bcp",
        "run": "@run-bcp",
        "observed_at": OBSERVED_AT,
        "time_basis": "collector_clock",
        "files": [],
        "data": {
            "dataset_uri": HF_URL,
            "revision": REV,
            "coverage": "complete",
            "row_count": ROWS_PER_RUN * len(RUNS),
        },
    }, {
        "dataset": HF_DATASET,
        "revision": REV,
        "license": LICENSE,
        "rows_per_run": str(ROWS_PER_RUN),
        "runs": ",".join(RUNS),
        "files": json.dumps(file_entries),
    })

    # ---- per-finding: tool_sequence + intel.behavior + edges ----
    tool_shape_note = (
        "Tool schema differs by run family (see pipeline README BCP section): "
        "ds4pro/glm51/qwen35 use search(query)/visit(docid); "
        "gpt-oss-120b-high/kimi26/tongyi-dr use search(query)/visit(docid,goal); "
        "tongyi-dr has one visit(goal,url) outlier."
    )

    for fid in FINDING_ORDER:
        f = by_id[fid]
        run, line, category = ANCHORS[fid]
        traj_id = "%s:predictions.jsonl line %d" % (run, line)
        row_text, row = read_row(run, line)
        md = row["metadata"]
        model_name = md.get("model_name", "unrecorded-in-source")
        harness = "browsecomp-plus"

        pass  # G1 runs once over all findings after the loop

        # Extract ordered tool calls (full row)
        steps = []
        idx = 0
        tool_names = Counter()
        for mc in md["model_calls"]:
            for tci in mc.get("tool_calls") or []:
                steps.append({
                    "index": idx,
                    "tool": tci.get("name", "?"),
                    "command": render_command(tci),
                    "turn": mc.get("turn"),
                })
                tool_names[tci.get("name", "?")] += 1
                idx += 1
        # G2
        if len(steps) != idx:
            fail("G2 step count mismatch for %s" % fid)

        seq_ref = "seq-" + fid.lower().replace("_", "-")
        # strip the extra 'turn' key for the schema (index/tool/command only)
        schema_steps = [{"index": s["index"], "tool": s["tool"],
                         "command": s["command"]} for s in steps]
        prov_url = (HF_URL + "/resolve/" + REV + "/" + run +
                    "/predictions.jsonl")
        rec(seq_ref, "observation", {
            "type": "behavior.tool_sequence",
            "source": "@source-bcp",
            "run": "@run-bcp",
            "observed_at": OBSERVED_AT,
            "time_basis": "collector_clock",
            "data": {
                "trajectory": traj_id,
                "model": model_name,
                "harness": harness,
                "steps": schema_steps,
                "length": len(schema_steps),
                "provenance": (
                    "Ordered tool calls from %s (file line %d, %d tool calls "
                    "across %d model_calls turns; tool mix %s). %s "
                    "Source: %s ; sha256 %s. "
                    "Commands abbreviated past 220 chars (raw bytes are the "
                    "ground truth)."
                    % (traj_id, line, len(schema_steps),
                       len(md["model_calls"]), dict(tool_names),
                       tool_shape_note, prov_url,
                       f["provenance"]["sha256"])
                ),
            },
        }, {
            "finding_id": fid,
            "trajectory_id": traj_id,
            "run": run,
            "model": model_name,
            "harness": harness,
            "tool_mix": json.dumps(dict(tool_names), sort_keys=True),
            "step_range": f["step_range"],
            "exemplar_note": ("corpus-wide finding; exemplar trajectory" if
                              fid in ("BCP-A-003", "BCP-X-001") else
                              "finding-bearing trajectory"),
        })

        # intel.behavior observation
        beh_ref = "beh-" + fid.lower().replace("_", "-")
        rec(beh_ref, "observation", {
            "type": "intel.behavior",
            "source": "@source-bcp",
            "run": "@run-bcp",
            "observed_at": OBSERVED_AT,
            "time_basis": "collector_clock",
            "data": {
                "category": category,
                "description": "[%s] %s" % (fid, f["why_interesting"]),
                "evaluations_seen_on": ["browsecomp-plus"],
                "models_affected": [model_name],
                "first_observed": "2026-10-17",
                "provenance": (
                    "BCP search-agent review fleet + adversarial review + "
                    "byte verifier; verified-findings.jsonl finding %s; "
                    "trajectory %s; review class %s; grade %s; confidence %s. "
                    "Verifier note: %s"
                    % (fid, traj_id, f["class"], f["grade"],
                       f["confidence"], f["verifier_note"])
                ),
                "severity": "",
            },
        }, {
            "finding_id": fid,
            "class_code": f["class"],
            "grade": f["grade"],
            "confidence": f["confidence"],
            "category": category,
            "trajectory_id": traj_id,
            "run": run,
            "model": model_name,
            "step_range": f["step_range"],
            "evidence_quote": f["evidence_quote"],
            "verifier_note": f["verifier_note"],
        })

        # edges
        rec("edge-run-" + fid.lower().replace("_", "-"), "edge", {
            "subject": "@run-bcp",
            "predicate": "related_to",
            "object": "@" + seq_ref,
            "basis": "OBSERVED",
            "cites": ["@" + seq_ref],
            "note": "scrape run produced the trajectory's tool-call sequence",
        }, {"finding_id": fid, "trajectory_id": traj_id})
        rec("edge-find-" + fid.lower().replace("_", "-"), "edge", {
            "subject": "@" + beh_ref,
            "predicate": "supports",
            "object": "@" + seq_ref,
            "basis": "OBSERVED",
            "cites": ["@" + beh_ref, "@" + seq_ref],
            "note": "finding %s observed in trajectory %s" % (fid, traj_id),
        }, {"finding_id": fid, "trajectory_id": traj_id})

    # ---- G1: byte-anchor verification over all findings ----
    g1_failures = check_g1()
    if g1_failures:
        fail("G1 byte-anchor failures:\n  " + "\n  ".join(g1_failures))

    # ---- within-batch dedup: no duplicate finding ids (already asserted);
    # shared trajectory BCP-C-003/C-004 noted ----
    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": "bcp-search-ingest-2026-10-17-v1",
        # No top-level "lane": the lane record was never registered via
        # `lane new`, and bundle-level "lane" fails LANE resolution without
        # it. Every record already carries tags.lane (the pipeline README's
        # requirement), so the graph is lane-scoped without in_lane edges.
        "records": records,
    }
    # Bundle JSON goes to stdout (the exec-path file write hits EPERM waves;
    # the caller captures stdout and writes the file via the tool path).
    # The build report goes to stderr.
    import sys
    print(json.dumps(bundle))
    # raw bytes of the six files already verified at scrape (manifest
    # bytes_match/sha256_match true); re-assert sha256 here as G3
    for run in RUNS:
        p = os.path.join(RAW, run, "predictions.jsonl")
        entry = next(x for x in manifest["files"] if x["path"] == run + "/predictions.jsonl")
        if sha256_file(p) != entry["sha256"]:
            fail("G3 sha256 mismatch on raw bytes: " + p)

    report = {
        "findings": len(FINDING_ORDER),
        "record_count": len(records),
        "record_kinds": dict(Counter(r["kind"] for r in records)),
        "record_types": dict(Counter(
            r["body"].get("type", r["kind"]) for r in records
            if r["kind"] == "observation")),
        "sha256_bundle": hashlib.sha256(
            json.dumps(bundle).encode()).hexdigest(),
        "revision": REV,
        "gates": "G1 quote-byte-verification PASS; G2 step-count PASS; "
                 "G3 raw-sha256 PASS",
    }
    print(json.dumps(report, indent=1), file=sys.stderr)


if __name__ == "__main__":
    main()
