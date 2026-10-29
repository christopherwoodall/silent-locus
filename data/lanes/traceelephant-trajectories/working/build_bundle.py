#!/usr/bin/env python3
"""Build the TraceElephant factum bundle (v2) with full trace edges.

Reads review/verified-findings.json (43 verifier-approved findings) and
emits a schema-validated bundle:
  source (run, per task) -> observable (harness/model)
  observation behavior.tool_sequence (cited steps, agent per step)
  observation intel.behavior (finding)
  edge exhibits (harness -> behavior) + edge uses (behavior -> tool_sequence)

Mirrors the wildclawbench-trajectories ingest precedent (batch
1762402022fc4d028d27c82fd92f8fc0).
"""
import json
import os
import re
import hashlib

BASE = os.path.expanduser("~/workspace/silent-locus")
LANE_DIR = os.path.join(BASE, "data/lanes/traceelephant-trajectories")
RAW_DATA = os.path.join(LANE_DIR, "raw/data")
LANE = "traceelephant-trajectories"
HF_SHA = "a78a57cdcdf74a080b1bec0f56f85228d86acbac"
HF_URL = ("https://huggingface.co/datasets/TraceElephant/TraceElephant/resolve/"
          + HF_SHA + "/data.zip")
OBSERVED_AT = "2026-10-16T00:00:00Z"

SYSTEM_HARNESS = {
    "captain-runs-assistantbench": "captain-agent",
    "captain-runs-gaia": "captain-agent",
    "magentic-runs-assistant-bench": "magentic-one",
    "magentic-runs-gaia": "magentic-one",
    "swe-agent-runs-swe-bench": "swe-agent",
}
SYSTEM_BENCH = {
    "captain-runs-assistantbench": "assistantbench",
    "captain-runs-gaia": "gaia",
    "magentic-runs-assistant-bench": "assistantbench",
    "magentic-runs-gaia": "gaia",
    "swe-agent-runs-swe-bench": "swe-bench",
}
SEV = {"HIGH": "high", "MEDIUM": "moderate", "LOW": "low"}

STEP_RE = re.compile(
    r"^([A-Za-z_][\w/]*)\s+steps?\s+([\d][\d,\-/\.\s]*?)(?:\s*\((.*)\))?\s*$")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def agent_at(task_dir, step_id):
    """True agent_name for a step_id from the raw step records."""
    p = os.path.join(RAW_DATA, task_dir, "step_records.json")
    try:
        with open(p) as f:
            steps = json.load(f)
        for s in steps:
            if s.get("step_id") == step_id:
                return s.get("agent_name", "unknown")
    except Exception:
        pass
    return "unknown"


def parse_extra_steps(entries):
    """Parse agents_steps_involved strings into (index, agent, note) triples."""
    out = []
    for e in entries:
        m = STEP_RE.match(e.strip())
        if not m:
            continue
        agent, nums, note = m.group(1), m.group(2), m.group(3) or ""
        first = re.search(r"\d+", nums)
        if not first:
            continue
        idx = int(first.group(0))
        label = "steps %s" % nums.strip()
        if note:
            label += " (%s)" % note
        out.append((idx, agent, label))
    return out


def main():
    with open(os.path.join(LANE_DIR, "review/verified-findings.json")) as f:
        findings = json.load(f)["findings"]

    records = []

    def add(rec):
        tags = rec.setdefault("tags", {})
        tags["lane"] = LANE
        records.append(rec)

    # Harness + model observables (deduped)
    harness_refs = {}
    for sysdir in sorted({f["evidence"]["file"].split("/")[2] for f in findings}):
        harness = SYSTEM_HARNESS[sysdir]
        if harness in harness_refs:
            continue
        ref = "harness-%s" % harness
        harness_refs[harness] = ref
        add({
            "ref": ref, "kind": "observable",
            "body": {"type": "harness",
                     "value_schema": "urn:factum:core:raw-string:1",
                     "value": harness},
            "tags": {"observable": "harness"},
        })
    add({
        "ref": "model-gpt-4o", "kind": "observable",
        "body": {"type": "model",
                 "value_schema": "urn:factum:core:raw-string:1",
                 "value": "gpt-4o"},
        "tags": {"observable": "model"},
    })

    prov_ts = ("TraceElephant trajectory review 2026-10-16: reviewer fleet "
               "(2 reviewers, 220 tasks) filed 44 candidates; adversarial "
               "verifier re-checked every citation against raw step bytes "
               "(43 verified, 1 killed: TE-A-16). Findings graded "
               "PRIMARY-by-observation, SECONDARY-by-source (published ACL "
               "2026 benchmark 'Seeing the Whole Elephant').")

    for i, f in enumerate(findings):
        fid = f["id"]
        parts = f["evidence"]["file"].split("/")
        sysdir, task = parts[2], parts[3]
        harness = SYSTEM_HARNESS[sysdir]
        bench = SYSTEM_BENCH[sysdir]
        task_dir = "%s/%s" % (sysdir, task)
        rel_traj = "data/lanes/traceelephant-trajectories/raw/data/%s/step_records.json" % task_dir
        step_path = os.path.join(RAW_DATA, task_dir, "step_records.json")
        fsha = sha256_file(step_path)

        # 1. source (run)
        sref = "src-%d" % i
        add({
            "ref": sref, "kind": "source",
            "body": {
                "source_type": "dataset",
                "locator": rel_traj,
                "title": task,
                "platform": ("TraceElephant trajectory corpus (HF "
                             "TraceElephant/TraceElephant, revision %s)" % HF_SHA),
            },
            "tags": {
                "record": "run", "task_id": task, "system": sysdir,
                "benchmark": bench, "sha256": fsha,
                "retrieval_method": "curl",
                "source_url": HF_URL, "license": "CC-BY-4.0",
            },
        })

        # 2. tool_sequence observation
        ev = f["evidence"]
        agent = agent_at(task_dir, ev["step"])
        steps = [{"index": ev["step"], "tool": agent,
                  "command": ev["verified_quote"]}]
        seen = {(ev["step"], agent)}
        for idx, ag, note in parse_extra_steps(f.get("agents_steps_involved", [])):
            if (idx, ag) in seen:
                continue
            seen.add((idx, ag))
            steps.append({"index": idx, "tool": ag, "command": note})
        steps.sort(key=lambda s: s["index"])
        tsref = "ts-%d" % i
        ts_prov = (prov_ts + " Session file sha256=%s. Steps are the cited "
                   "ones; full step bytes (inputs, outputs, tool logs) in the "
                   "cached file. Retrieved 2026-10-16T21:02:45Z-22:45:33Z via "
                   "curl -L from %s." % (fsha, HF_URL))
        add({
            "ref": tsref, "kind": "observation",
            "body": {
                "type": "behavior.tool_sequence",
                "data_schema": "urn:factum:behavior:tool-sequence:1",
                "source": "@" + sref,
                "observed_at": OBSERVED_AT,
                "time_basis": "collector_clock",
                "files": [],
                "data": {
                    "trajectory": rel_traj,
                    "model": "gpt-4o",
                    "harness": harness,
                    "steps": steps,
                    "length": len(steps),
                    "provenance": ts_prov,
                },
            },
            "tags": {"record": "tool_sequence", "finding.id": fid,
                     "task_id": task, "system": sysdir},
        })

        # 3. intel.behavior observation
        bref = "beh-%d" % i
        add({
            "ref": bref, "kind": "observation",
            "body": {
                "type": "intel.behavior",
                "data_schema": "urn:factum:intel:behavior:1",
                "source": "@" + sref,
                "observed_at": OBSERVED_AT,
                "time_basis": "collector_clock",
                "files": [],
                "data": {
                    "category": f["behavior_class"].lower(),
                    "description": f["description"],
                    "evaluations_seen_on": ["TraceElephant trajectory corpus"],
                    "first_observed": ("2026-10-16 (trajectory review; trace "
                                       "runs executed 2026 per step timestamps)"),
                    "models_affected": ["gpt-4o"],
                    "provenance": prov_ts,
                    "severity": SEV.get(f["confidence"], "moderate"),
                },
            },
            "tags": {
                "record": "finding", "finding.id": fid,
                "behavior.class": f["behavior_class"],
                "confidence": f["confidence"], "grade": f["grade"],
                "task_id": task, "trajectory": rel_traj, "system": sysdir,
            },
        })

        # 4. edges: exhibits (harness -> behavior) + uses (behavior -> sequence)
        add({
            "ref": "edge-ex-%d" % i, "kind": "edge",
            "body": {
                "predicate": "exhibits",
                "subject": "@" + harness_refs[harness],
                "object": "@" + bref,
                "basis": "OBSERVED",
                "cites": ["@" + tsref],
                "note": ("Harness %s exhibited this behavior in "
                         "TraceElephant task %s." % (harness, task)),
            },
            "tags": {"record": "edge", "predicate": "exhibits",
                     "finding.id": fid},
        })
        add({
            "ref": "edge-us-%d" % i, "kind": "edge",
            "body": {
                "predicate": "uses",
                "subject": "@" + bref,
                "object": "@" + tsref,
                "basis": "INFERENCE",
                "cites": ["@" + tsref],
                "note": "The behavior finding rests on the run's cited tool-call sequence.",
            },
            "tags": {"record": "edge", "predicate": "uses",
                     "finding.id": fid},
        })

    bundle = {
        "bundle": 2,
        "idempotency_key": "traceelephant-ingest/20261017",
        "actor": "agent:traceelephant-ingestor",
        "tags": {"lane": LANE, "ingest": "traceelephant-trajectories"},
        "records": records,
    }
    out = os.path.join(LANE_DIR, "working", "bundle-traceelephant.json")
    with open(out, "w") as f:
        json.dump(bundle, f, indent=1)
    kinds = {}
    for r in records:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    print("wrote %s" % out)
    print("records: %d %s" % (len(records), kinds))


if __name__ == "__main__":
    main()
