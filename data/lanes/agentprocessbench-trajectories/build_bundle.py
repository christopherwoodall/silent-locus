#!/usr/bin/env python3
"""Build the Factum ingest bundle for the agentprocessbench-trajectories lane.

Reads: verified-findings.jsonl (20 verifier-passed findings),
       raw/<split>/test.jsonl (source bytes), raw/manifest.json (provenance).
Writes: bundle.json (Factum bundle v2, submittable via `add --input`).

Bundle design (full trace edges, traversable by refs):
  source (dataset file URL)
    -> dataset.snapshot observation (revision, coverage, row_count)
    -> behavior.tool_sequence observation per finding-bearing trajectory:
         trajectory locator, harness=data_source, model=unrecorded-in-source,
         steps=[{index, tool, command}] for EVERY tool call in message order,
         human step_labels preserved as [step_label=N] annotations on command
    -> intel.behavior observation per finding (cites its tool_sequence record(s))
    -> claim record per finding (OBSERVED, cites behavior + tool_sequence)

Tool-call dual serialization handled: structured message `tool_calls`
(OpenAI function-call shape) AND <tool_call>{...}</tool_call> JSON blobs
embedded in assistant message content (bfcl style).

No edges (exhibits/uses) are submitted here: edge building is a separate
pass per the standing no-edges-during-ingest rule. The chain is traversable
via cites: claim -> intel.behavior -> behavior.tool_sequence -> trajectory
locator -> raw bytes.
"""
import json, re, os, sys

LANE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(LANE_DIR, "raw")
REV = "cd81f326aece8b0a3f6359e20df370690d3a98bf"
DATASET = "LulaCola/AgentProcessBench"
LANE = "agentprocessbench-trajectories"
ACTOR = "agent:lane-ingest-agentprocessbench"
IDEMPOTENCY = "agentprocessbench-trajectories/ingest-2026-10-16"

# finding_id -> (behavior category, severity)
CATEGORIES = {
    "APB-A-001": ("injected-directive-compliance", "high"),
    "APB-A-002": ("unauthorized-irreversible-action", "high"),
    "APB-A-003": ("unverified-entitlement", "high"),
    "APB-A-004": ("unauthorized-irreversible-action", "high"),
    "APB-A-005": ("unverified-entitlement", "low"),
    "APB-A-006": ("credential-exposure", "moderate"),
    "APB-A-007": ("injected-directive-compliance", "high"),
    "APB-A-008": ("tool-protocol-misuse", "moderate"),
    "APB-A-009": ("confabulation-under-retrieval-failure", "moderate"),
    "APB-A-010": ("recovery-livelock", "moderate"),
    "APB-A-011": ("blind-tool-output-trust", "low"),
    "APB-B-001": ("unauthorized-irreversible-action", "high"),
    "APB-B-002": ("unverified-entitlement", "high"),
    "APB-B-003": ("unverified-entitlement", "high"),
    "APB-B-004": ("tool-protocol-misuse", "moderate"),
    "APB-B-005": ("unverified-entitlement", "high"),
    "APB-B-006": ("tool-protocol-misuse", "moderate"),
    "APB-B-007": ("recovery-livelock", "moderate"),
    "APB-B-008": ("recovery-livelock", "moderate"),
    "APB-B-009": ("barrier-respecting-recovery", "low"),
}

TOOLCALL_RE = re.compile(r"<tool_call>(.*?)</tool_call>", re.DOTALL)

def extract_tool_calls(record):
    """Return ordered [(msg_index, tool_name, args_json, serialization)] for
    every assistant tool invocation in the trajectory."""
    calls = []
    labels = record.get("step_labels", {}) or {}
    for i, m in enumerate(record["messages"]):
        if m.get("role") != "assistant":
            continue
        label = labels.get(str(i), labels.get(i))
        suffix = f" [step_label={label}]" if label is not None else ""
        # 1) structured tool_calls
        for tc in m.get("tool_calls") or []:
            fn = tc.get("function", {}) if isinstance(tc, dict) else {}
            name = fn.get("name", "unknown")
            args = fn.get("arguments", "")
            if isinstance(args, dict):
                args = json.dumps(args, ensure_ascii=False)
            calls.append({"index": i, "tool": name,
                          "command": str(args) + suffix,
                          "_ser": "structured"})
        # 2) <tool_call> JSON embedded in content
        content = m.get("content")
        if isinstance(content, str):
            for mm in TOOLCALL_RE.finditer(content):
                raw = mm.group(1).strip()
                try:
                    obj = json.loads(raw)
                    name = obj.get("name", "unknown")
                    args = obj.get("arguments", "")
                    if isinstance(args, dict):
                        args = json.dumps(args, ensure_ascii=False)
                    cmd = str(args)
                except Exception:
                    name = "tool_call(unparsed)"
                    cmd = raw
                calls.append({"index": i, "tool": name,
                              "command": cmd + suffix,
                              "_ser": "embedded"})
    # order by message index (already in order)
    for c in calls:
        del c["_ser"]
    return calls

def main():
    manifest = {m["filename"]: m for m in json.load(open(os.path.join(RAW, "manifest.json")))}
    findings = [json.loads(l) for l in open(os.path.join(LANE_DIR, "verified-findings.jsonl"))]
    assert len(findings) == 20, f"expected 20 findings, got {len(findings)}"

    # unique trajectories: (file, total_index)
    trajs = {}
    for f in findings:
        key = (f["file"], f["total_index"])
        trajs.setdefault(key, []).append(f["finding_id"])
    # APB-A-007 discusses all four samples of bfcl query_index 38
    # (total_index 691/692/693/694); 693 carries no standalone finding but is
    # part of A-007's evidence, so it gets its own tool_sequence.
    trajs.setdefault(("bfcl/test.jsonl", 693), []).append("APB-A-007")

    # load raw records
    raw_cache = {}
    def raw_rec(path, idx):
        if path not in raw_cache:
            raw_cache[path] = {}
            with open(os.path.join(RAW, path)) as fh:
                for line in fh:
                    r = json.loads(line)
                    raw_cache[path][r["total_index"]] = r
        return raw_cache[path][idx]

    bundle = {"bundle": 2, "actor": ACTOR, "idempotency_key": IDEMPOTENCY,
              "records": []}

    def lane_tags(extra=None):
        t = {"lane": LANE}
        if extra: t.update(extra)
        return t

    # 1) source records + 2) dataset.snapshot observations
    src_ref = {}
    for path in sorted({k[0] for k in trajs}):
        m = manifest[path]
        ref = "source-" + path.split("/")[0].replace("_", "-")
        src_ref[path] = ref
        bundle["records"].append({
            "ref": ref, "kind": "source",
            "body": {"source_type": "dataset",
                     "locator": m["source_url"],
                     "platform": "huggingface",
                     "title": f"{DATASET} {path} @ {REV}"},
            "tags": lane_tags({"sha256": m["sha256"]})})
        bundle["records"].append({
            "ref": "snapshot-" + path.split("/")[0].replace("_", "-"),
            "kind": "observation",
            "body": {"type": "dataset.snapshot",
                     "source": "@" + ref,
                     "observed_at": m["retrieved_at"],
                     "time_basis": "source_metadata",
                     "data": {"dataset_uri": f"huggingface://{DATASET}",
                              "revision": REV,
                              "coverage": "complete",
                              "row_count": m["lines"]}},
            "tags": lane_tags({"sha256": m["sha256"],
                               "bytes": m["bytes"],
                               "file": path})})

    # 3) behavior.tool_sequence per unique trajectory
    seq_ref = {}
    for (path, idx) in sorted(trajs):
        rec = raw_rec(path, idx)
        calls = extract_tool_calls(rec)
        ref = f"toolseq-{path.split('/')[0]}-{idx}"
        seq_ref[(path, idx)] = ref
        split = path.split("/")[0]
        bundle["records"].append({
            "ref": ref, "kind": "observation",
            "body": {"type": "behavior.tool_sequence",
                     "source": "@" + src_ref[path],
                     "observed_at": manifest[path]["retrieved_at"],
                     "time_basis": "source_metadata",
                     "data": {
                         "trajectory": f"huggingface://{DATASET}@{REV}/{path}#total_index={idx}",
                         "model": "unrecorded-in-source",
                         "harness": rec.get("data_source", "unknown"),
                         "steps": calls,
                         "length": len(calls),
                         "provenance": (f"AgentProcessBench {path} @ {REV} total_index={idx}; "
                                        f"query_index={rec.get('query_index')}, sample_index={rec.get('sample_index')}, "
                                        f"final_label={rec.get('final_label')}; bytes from raw/{path} "
                                        f"sha256={manifest[path]['sha256']}")}},
            "tags": lane_tags({"total_index": idx,
                               "findings": sorted(trajs[(path, idx)]),
                               "tool_call_count": len(calls)})})

    # 4) intel.behavior per finding + 5) claim per finding
    for f in findings:
        cat, sev = CATEGORIES[f["finding_id"]]
        bref = "behavior-" + f["finding_id"].lower().replace("-", "")
        seqs = []
        for idx in ([f["total_index"]] if f["finding_id"] != "APB-A-007"
                    else [691, 692, 693, 694]):
            # APB-A-007 spans all four samples of bfcl query_index 38
            key = (f["file"], idx)
            if seq_ref[key] not in seqs:
                seqs.append(seq_ref[key])
        seq_locators = "; ".join(
            f"huggingface://{DATASET}@{REV}/{f['file']}#total_index={i}"
            for i in ([f["total_index"]] if f["finding_id"] != "APB-A-007"
                      else [691, 692, 693, 694]))
        m = manifest[f["file"]]
        bundle["records"].append({
            "ref": bref, "kind": "observation",
            "body": {"type": "intel.behavior",
                     "source": "@" + src_ref[f["file"]],
                     "observed_at": m["retrieved_at"],
                     "time_basis": "source_metadata",
                     # NOTE: the observation envelope (urn:factum:core:observation:1)
                     # has additionalProperties:false and no cites field, so the
                     # behavior->tool_sequence link lives in the description text
                     # and in the claim's cites. Traversal stays intact.
                     "data": {
                         "category": cat,
                         "description": (f"Finding {f['finding_id']} (verifier: byte-verified in raw bytes). "
                                        f"Tool-sequence trajectories: {seq_locators}. "
                                        f"Evidence: {f['evidence']} "
                                        f"Why interesting: {f['why_interesting']} "
                                        f"Verifier note: {f['verifier_note']}"),
                         "evaluations_seen_on": ["AgentProcessBench"],
                         "first_observed": "2026-10",
                         "severity": sev,
                         "provenance": (f"{DATASET} {f['file']} @ {REV} total_index={f['total_index']} "
                                        f"steps {f['step_range']}; raw bytes sha256={m['sha256']}")}},
            "tags": lane_tags({"finding_id": f["finding_id"],
                               "class": f["class"],
                               "grade": f["grade"],
                               "confidence": f["confidence"],
                               "novelty": f["novelty"]})})
        bundle["records"].append({
            "ref": "claim-" + f["finding_id"].lower().replace("-", ""),
            "kind": "claim",
            "body": {"subject": "@" + bref,
                     "property": "behavior_finding",
                     "value": (f"{f['finding_id']} ({f['class']}, grade {f['grade']}, "
                               f"confidence {f['confidence']}): {f['why_interesting']}"),
                     "basis": "OBSERVED",
                     "cites": ["@" + bref] + ["@" + s for s in seqs]},
            "tags": lane_tags({"finding_id": f["finding_id"],
                               "class": f["class"],
                               "grade": f["grade"],
                               "confidence": f["confidence"]})})

    out = os.path.join(LANE_DIR, "bundle.json")
    with open(out, "w") as fh:
        json.dump(bundle, fh, ensure_ascii=False, indent=1)
    n = len(bundle["records"])
    kinds = {}
    for r in bundle["records"]:
        kinds[r["kind"] + ":" + (r["body"].get("type") if r["kind"]=="observation" else "")] = kinds.get(r["kind"] + ":" + (r["body"].get("type") if r["kind"]=="observation" else ""), 0) + 1
    print(f"wrote {out}: {n} records")
    for k in sorted(kinds): print(" ", k, kinds[k])
    # sanity: every tool_sequence has length == len(steps)
    for r in bundle["records"]:
        if r["kind"]=="observation" and r["body"]["type"]=="behavior.tool_sequence":
            d=r["body"]["data"]
            assert d["length"]==len(d["steps"]), r["ref"]
    print("tool_sequence length checks ok")

if __name__ == "__main__":
    main()
