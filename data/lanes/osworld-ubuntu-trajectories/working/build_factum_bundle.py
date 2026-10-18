#!/usr/bin/env python3
"""Build the factum ingest bundle for the 13 verified OSWorld-Ubuntu findings.

Reads working/verified-findings.jsonl (13 byte-verified records), derives ordered
tool-call sequences from the raw trajectory bytes, and emits bundle.json for
`factum.py add --input`.

Trajectory formats (documented in raw/MANIFEST.json):
- traj.jsonl families: one JSON object per line, one line per step.
  Fields: step_num (1-based), action_timestamp, action (executed pyautogui code
  or DONE/FAIL), response (reasoning), reward, done.
- coact families (RB-004/006/007): chat_history.json, a list of messages
  {role, name, content:[{type:text,...}]} with optional tool_calls[]
  (function.name + arguments JSON).

Evidence rules: verbatim quotes copied byte-identical from the finding file;
tool-call commands copied verbatim from raw trajectory bytes. No invented
timestamps: observed_at for findings is the documented adversarial_review_date
(2026-10-17, day precision, 00:00:00Z placeholder noted in provenance); the
snapshot observed_at is the lane's documented scrape start time (completion
time not separately recorded).
"""
import json
import os

LANE = "osworld-ubuntu-trajectories"
LDIR = os.path.expanduser("~/workspace/silent-locus/data/lanes/osworld-ubuntu-trajectories")
WORK = os.path.join(LDIR, "working")
REV = "5473c39e42a538a187a9b2c2b499db59d560fd8c"
DS_NAME = "xlangai/ubuntu_osworld_verified_trajs"
DS_URL = f"https://huggingface.co/datasets/{DS_NAME}"
REVIEW_DATE = "2026-10-17"
OBSERVED_AT = REVIEW_DATE + "T00:00:00Z"  # day-precision placeholder, see provenance
SNAPSHOT_OBSERVED_AT = "2026-10-17T19:11:00Z"  # lane scrape_started_utc (MANIFEST.json)
RUN_STARTED = "2026-10-18T04:18:00Z"  # this ingest run's actual start (operator clock)
IDEMPOTENCY = "osworld-ubuntu-ingest-2026-10-18-v1"
ACTOR = "osworld-ubuntu-ingestor"
SEVERITY = {"CAPTCHA": "moderate", "GUARDRAIL": "high", "TOOL-MISUSE": "moderate",
            "COORDINATION": "moderate", "RECOVERY": "low", "OTHER": "low"}

# model/harness per finding id (casefold-normalized, factum-behavior convention)
MODEL_HARNESS = {
    "osworld-A-001": ("claude-opus-4-5-20251101", "osworld"),
    "osworld-A-002": ("claude-opus-4-5-20251101", "osworld"),
    "osworld-A-003": ("minimax-m3", "osworld"),
    "osworld-A-004": ("claude-opus-4-5-20251101", "osworld"),
    "RB-001": ("ui-tars", "osworld"),
    "RB-002": ("opencua-a3b", "osworld"),
    "RB-003": ("gpt-5", "osworld"),
    "RB-004": ("coact", "coact"),
    "RB-005": ("opencua-qwen2-7b", "osworld"),
    "RB-006": ("coact", "coact"),
    "RB-007": ("coact", "coact"),
    "RB-009": ("autoglm", "osworld"),
    "RB-011": ("autoglm", "osworld"),
}


def zip_of(file_path):
    """file_path is lane-relative 'raw/extracted/<topdir>/...'; zip is <topdir>.zip."""
    topdir = file_path.split("/")[2]
    return topdir + ".zip"


def zip_url(file_path):
    return f"{DS_URL}/resolve/{REV}/" + zip_of(file_path)


def inzip_path(file_path):
    """Path of the trajectory file inside its zip (top dir included)."""
    return "/".join(file_path.split("/")[2:])


def load_tool_sequence(file_path):
    """Ordered tool-call steps from raw trajectory bytes, verbatim."""
    full = os.path.join(LDIR, file_path)
    if file_path.endswith("traj.jsonl"):
        seq = []
        with open(full) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                s = json.loads(line)
                action = s.get("action", "")
                if isinstance(action, dict):
                    # uipath family: action is a structured dict, e.g.
                    # {"action_type": "CLICK", "x": 548, "y": 154}
                    tool = str(action.get("action_type", "action")).lower()
                    command = json.dumps(action, ensure_ascii=False)
                elif isinstance(action, str) and "pyautogui" in action:
                    tool, command = "pyautogui", action
                elif isinstance(action, str) and action in ("DONE", "FAIL", "WAIT"):
                    tool, command = "harness-control", action
                else:
                    tool, command = "code", action if isinstance(action, str) else json.dumps(action, ensure_ascii=False)
                seq.append({"index": len(seq), "tool": tool, "command": command})
        return seq, f"traj.jsonl: one JSON object per line; 'action' is the executed step."
    elif file_path.endswith("chat_history.json"):
        with open(full) as fh:
            msgs = json.load(fh)
        seq = []
        for m in msgs:
            if m.get("tool_calls"):
                for tc in m["tool_calls"]:
                    fn = tc.get("function", {})
                    tool = fn.get("name", "tool_call")
                    seq.append({"index": len(seq), "tool": tool,
                                "command": fn.get("arguments", "")})
                continue
            role = m.get("role", "")
            name = m.get("name", "")
            tool = f"{role}:{name}" if name else role
            content = m.get("content")
            if isinstance(content, list):
                text = "\n".join(b.get("text", "") for b in content
                                  if b.get("type") == "text" and b.get("text"))
            elif isinstance(content, str):
                text = content
            else:
                text = json.dumps(content, ensure_ascii=False)
            seq.append({"index": len(seq), "tool": tool, "command": text})
        return seq, "chat_history.json: one entry per message; tool_calls are sub-agent taskings."
    raise ValueError(f"unknown trajectory format: {file_path}")


def main():
    findings = []
    with open(os.path.join(WORK, "verified-findings.jsonl")) as fh:
        for line in fh:
            if line.strip():
                findings.append(json.loads(line))
    assert len(findings) == 13, f"expected 13 findings, got {len(findings)}"

    records = []
    refs = set()

    def rec(kind, ref, body, tags):
        assert ref not in refs, f"duplicate ref {ref}"
        assert tags.get("lane") == LANE, f"missing lane tag on {ref}"
        refs.add(ref)
        records.append({"kind": kind, "ref": ref, "body": body, "tags": tags})

    # --- 1 source record: the HF dataset -------------------------------------
    src_body = {
        "source_type": "dataset",
        "locator": f"{DS_URL}/tree/{REV}",
        "title": f"{DS_NAME} (rev {REV[:12]})",
        "platform": "huggingface",
    }
    rec("source", "src-hf-ubuntu-osworld", src_body,
        {"lane": LANE, "dataset": DS_NAME, "revision": REV, "license": "mit"})

    # --- 1 run record: this ingest run ---------------------------------------
    rec("run", "ingest-run",
        {"run_kind": "ingest",
         "tool": "lane-ingest bundle builder (build_factum_bundle.py)",
         "started": RUN_STARTED,
         "params": {"lane": LANE, "dataset": DS_NAME, "dataset_revision": REV,
                    "findings_count": 13, "idempotency_key": IDEMPOTENCY},
         "coverage": {"description": "ingest 13 verified findings, 13 tool-call "
                                     "sequences, 1 dataset snapshot from the "
                                     "23-zip sampled lane pull (~8,055 trajectories scanned)",
                      "scanned": 8055, "total": 8055, "complete": False}},
        {"lane": LANE, "run_kind": "ingest"})

    # --- 1 dataset.snapshot observation --------------------------------------
    rec("observation", "dataset-snapshot",
        {"type": "dataset.snapshot",
         "data_schema": "urn:factum:datasets:snapshot:1",
         "data": {"dataset_uri": DS_URL, "revision": REV, "coverage": "partial",
                  "row_count": 8055},
         "source": "@src-hf-ubuntu-osworld",
         "observed_at": SNAPSHOT_OBSERVED_AT, "time_basis": "collector_clock",
         "files": []},
        {"lane": LANE, "dataset": DS_NAME, "revision": REV,
         "sampling_plan": "stratified: one smallest-variant zip per model family; "
                          "23 of 99 zips (30+ model variants x step settings); "
                          "sampling plan + substitutions documented in raw/MANIFEST.json"})

    for f in findings:
        fid = f["id"]
        cls = f["class"]
        model, harness = MODEL_HARNESS[fid]
        fref, tref, cref = f"finding-{fid}", f"toolseq-{fid}", f"claim-{fid}"
        fpath = f["file_path"]

        desc = (
            "Observed behavior (verbatim from trajectory): " + f["quote"] + "\n"
            "Why interesting: " + f["why_interesting"] + "\n"
            "Verifier note: " + f["verifier_note"] + "\n"
            "Adversarial note: " + f["adversarial_note"]
        )
        provenance = (
            "verified-findings.jsonl, lane " + LANE + ", adversarial review date "
            + REVIEW_DATE + " (observed_at is day-precision from that documented "
            "date; 00:00:00Z is a placeholder). Source bytes: " + zip_url(fpath)
            + " (zip; trajectory at in-zip path " + inzip_path(fpath) + "); sha256 "
            + f["sha256"] + "; dataset rev " + f["dataset_revision"]
            + "; retrieval: local read of cached raw bytes (lane download via "
            "curl from HF; see raw/MANIFEST.json)"
        )

        # --- intel.behavior observation --------------------------------------
        rec("observation", fref,
            {"type": "intel.behavior",
             "data_schema": "urn:factum:intel:behavior:1",
             "data": {"category": cls.lower(),
                      "description": desc,
                      "evaluations_seen_on": ["osworld"],
                      "models_affected": [model],
                      "first_observed": REVIEW_DATE,
                      "severity": SEVERITY[cls],
                      "provenance": provenance},
             "source": "@src-hf-ubuntu-osworld",
             "observed_at": OBSERVED_AT, "time_basis": "source_metadata",
             "files": []},
            {"lane": LANE, "finding_id": fid, "class": cls,
             "grade": f["grade"], "confidence": f["confidence"],
             "step_range": f["steps"], "trajectory": f["trajectory"],
             "trajectory_id": f["trajectory_id"], "model": model,
             "harness": harness,
             "dataset_revision": f["dataset_revision"],
             "sha256": f["sha256"],
             "quote_verified_verbatim": str(f["quote_verified_verbatim"]).lower(),
             "in_zip_path": inzip_path(fpath), "zip": zip_of(fpath)})

        # --- behavior.tool_sequence observation -------------------------------
        steps, fmt_note = load_tool_sequence(fpath)
        assert len(steps) > 0, f"empty steps for {fid}"
        seq_provenance = fmt_note + " " + provenance
        rec("observation", tref,
            {"type": "behavior.tool_sequence",
             "data_schema": "urn:factum:behavior:tool-sequence:1",
             "data": {"trajectory": fpath, "model": model,
                      "harness": harness, "steps": steps,
                      "length": len(steps), "provenance": seq_provenance},
             "source": "@src-hf-ubuntu-osworld",
             "run": "@ingest-run",
             "observed_at": OBSERVED_AT, "time_basis": "source_metadata",
             "files": []},
            {"lane": LANE, "finding_id": fid, "class": cls,
             "trajectory": fpath, "model": model, "harness": harness,
             "step_count": str(len(steps))})

        # --- OBSERVED claim citing the observations (never the source record) --
        rec("claim", cref,
            {"subject": "@" + fref,
             "property": "exhibits",
             "value": {"class": cls, "grade": f["grade"],
                       "confidence": f["confidence"],
                       "trajectory_id": f["trajectory_id"],
                       "step_range": f["steps"]},
             "basis": "OBSERVED",
             "cites": ["@" + fref, "@" + tref],
             "note": f["why_interesting"]},
            {"lane": LANE, "finding_id": fid, "class": cls})

        # --- graph edges: run -> toolseq, finding -> toolseq ------------------
        rec("edge", f"edge-run-toolseq-{fid}",
            {"subject": "@ingest-run", "predicate": "related_to",
             "object": "@" + tref, "basis": "OBSERVED",
             "cites": ["@" + tref],
             "note": "ingest run captured this trajectory's tool-call sequence"},
            {"lane": LANE, "finding_id": fid})
        rec("edge", f"edge-finding-toolseq-{fid}",
            {"subject": "@" + fref, "predicate": "supports",
             "object": "@" + tref, "basis": "OBSERVED",
             "cites": ["@" + fref, "@" + tref],
             "note": "finding supported by the trajectory's tool-call sequence"},
            {"lane": LANE, "finding_id": fid})

    bundle = {"bundle": 2, "actor": ACTOR, "idempotency_key": IDEMPOTENCY,
              "records": records}

    # --- independent re-derivation checks (validator is not the builder) ------
    from collections import Counter
    kinds = Counter(r["kind"] for r in records)
    assert kinds == {"source": 1, "run": 1, "observation": 27, "claim": 13,
                     "edge": 26}, kinds
    types = Counter(r["body"].get("type") for r in records if r["kind"] == "observation")
    assert types == {"dataset.snapshot": 1, "intel.behavior": 13,
                     "behavior.tool_sequence": 13}, types
    for r in records:
        if r["kind"] == "observation":
            assert "observed_at" in r["body"] and "time_basis" in r["body"], r["ref"]
        if r["kind"] == "claim":
            assert r["body"]["basis"] == "OBSERVED"
            for c in r["body"]["cites"]:
                assert c[1:] in refs, (r["ref"], c)
                assert c != "@src-hf-ubuntu-osworld", r["ref"]
        if r["kind"] == "edge":
            assert r["body"].get("basis") == "OBSERVED", r["ref"]
            for fld in ("subject", "object"):
                assert r["body"][fld][1:] in refs, (r["ref"], fld)
            for c in r["body"]["cites"]:
                assert c[1:] in refs, (r["ref"], c)
        if r["kind"] == "observation" and r["body"]["type"] == "behavior.tool_sequence":
            assert r["body"]["data"]["length"] == len(r["body"]["data"]["steps"]), r["ref"]
            idx = [s["index"] for s in r["body"]["data"]["steps"]]
            assert idx == list(range(len(idx))), r["ref"]
            for s in r["body"]["data"]["steps"]:
                assert set(s.keys()) == {"index", "tool", "command"}, r["ref"]
    # verbatim integrity: quotes re-read from the finding file, not the builder
    by_id = {r["ref"]: r for r in records}
    with open(os.path.join(WORK, "verified-findings.jsonl")) as fh:
        for line in fh:
            if not line.strip():
                continue
            f = json.loads(line)
            obs = by_id["finding-" + f["id"]]
            assert f["quote"] in obs["body"]["data"]["description"]
            assert f["verifier_note"] in obs["body"]["data"]["description"]
            assert f["adversarial_note"] in obs["body"]["data"]["description"]
            assert f["why_interesting"] in obs["body"]["data"]["description"]
            assert f["sha256"] in obs["tags"]["sha256"]
            assert f["sha256"] in obs["body"]["data"]["provenance"]

    out = os.path.join(WORK, "bundle.json")
    with open(out, "w") as fh:
        json.dump(bundle, fh, indent=1, ensure_ascii=False)
    print(f"wrote {out}: {len(records)} records")
    print("kind counts:", dict(kinds))
    print("obs types:", dict(types))
    # step-count summary for the report
    for fid in sorted(by_id):
        if fid.startswith("toolseq-"):
            print(fid, "steps:", by_id[fid]["body"]["data"]["length"])


if __name__ == "__main__":
    main()
