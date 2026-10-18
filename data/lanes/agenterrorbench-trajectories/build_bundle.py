#!/usr/bin/env python3
"""Build the factum bundle for the 23 verified AgentErrorBench findings.

Per finding: dataset.record observation (trajectory file) + behavior.tool_sequence
observation (cited steps) + intel.behavior observation, with explicit edge records
(tool_sequence --derived_from--> trajectory --part_of--> snapshot;
intel.behavior --derived_from--> tool_sequence), all via bundle-local @refs.

Reads: review/verified-findings.json, review/reviewer-a-findings.json,
       review/reviewer-b-findings.json, raw/MANIFEST.json, trajectory files.
Writes: bundle.json in this directory.
"""
import json, os, re

LANE = os.path.dirname(os.path.abspath(__file__))
LANE_TAG = "agenterrorbench-trajectories"
ACTOR = "agent:agenterrorbench-ingestor"
IDEMPOTENCY = "agenterrorbench-ingest-20261016-v1"
DATASET_FOLDER = "https://drive.google.com/drive/folders/1bQe6dQA85pktT63YnKIKJDTVaH3O3Vpu?usp=drive_link"

CATEGORY = {
    "A-001": "tool-protocol-misuse",
    "A-002": "tool-protocol-misuse",
    "A-003": "confabulation-under-retrieval-failure",
    "A-004": "blocker-deception",
    "A-005": "blocker-deception",
    "A-006": "blocker-deception",
    "A-007": "tool-protocol-misuse",
    "A-008": "tool-protocol-misuse",
    "A-009": "confabulation-under-retrieval-failure",
    "A-010": "confabulation-under-retrieval-failure",
    "A-011": "confabulation-under-retrieval-failure",
    "A-013": "confabulation-under-retrieval-failure",
    "A-014": "tool-protocol-misuse",
    "A-015": "tool-protocol-misuse",
    "A-017": "blocker-deception",
    "B-001": "confabulation-under-retrieval-failure",
    "B-002": "confabulation-under-retrieval-failure",
    "B-003": "confabulation-under-retrieval-failure",
    "B-004": "unauthorized-irreversible-action",
    "B-005": "unauthorized-irreversible-action",
    "B-006": "unauthorized-irreversible-action",
    "B-007": "unauthorized-irreversible-action",
    "B-008": "unauthorized-irreversible-action",
}

SEVERITY = {k: ("high" if k.startswith("B-004") or k in
            {"B-004", "B-005", "B-006", "B-007", "B-008"} else "moderate")
            for k in CATEGORY}


def expand_steps(s):
    steps = []
    for part in s.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            steps += list(range(int(a), int(b) + 1))
        else:
            steps.append(int(part))
    return steps


def channel_entries(content):
    """Yield (channel, body) for each <action>/<answer> span, verbatim."""
    entries = []
    for m in re.finditer(r"<(action|answer)>(.*?)</\1>", content, re.S):
        entries.append((m.group(1), m.group(2)))
    if not entries:
        m = re.search(r"<(action|answer)>(.*)$", content, re.S)
        if m:
            entries.append((m.group(1), m.group(2) + " [UNTERMINATED: no closing tag]"))
    return entries


def parse_gaia_tool(body):
    m = re.search(r"^tool:\s*(\S+)\s*$", body, re.M)
    tool = m.group(1) if m else "unknown"
    m2 = re.search(r"^parameters:\s*(\{.*\})\s*$", body, re.S | re.M)
    cmd = m2.group(1) if m2 else body.strip()
    return tool, cmd


def first_observed(ts):
    if not ts:
        return "2025-09 (trajectory metadata timestamp missing)"
    m = re.match(r"^(\d{4})(\d{2})(\d{2})", str(ts))
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return str(ts)


ver = {f["id"]: f for f in json.load(open(os.path.join(LANE, "review/verified-findings.json")))}
keep = sorted([k for k, v in ver.items() if v["verdict"] == "KEEP"])
assert len(keep) == 23, keep
rev = {}
for fn in ("review/reviewer-a-findings.json", "review/reviewer-b-findings.json"):
    for f in json.load(open(os.path.join(LANE, fn))):
        rev[f["id"]] = f

man = {e["path"].split("/")[-1]: e for e in json.load(open(os.path.join(LANE, "raw/MANIFEST.json")))["files"]}

# Resolve trajectories; dedupe across findings.
trajs = {}   # filename -> dict
findings = []
for fid in keep:
    f = rev[fid]; v = ver[fid]
    name = f["trajectory_id"]
    if not name.endswith(".json"):
        name += ".json"
    if name not in trajs:
        sub = None
        for d in ("Original_Failure_Trajectory/ALFWorld", "Original_Failure_Trajectory/GAIA",
                  "Original_Failure_Trajectory/WebShop"):
            p = os.path.join(LANE, "raw", d, name)
            if os.path.exists(p):
                sub, path = d, p
                break
        assert sub, name
        t = json.load(open(path))
        md = t.get("metadata", {})
        assert man[name]["sha256"] == f["provenance"]["sha256"], fid
        mname = re.match(r"^(Llama3\.3-70B-Turbo|GPT-4o|Qwen3-8B)_", name)
        model = (mname.group(1).casefold() if mname
                 else (md.get("model") or "").casefold() or "unknown")
        trajs[name] = {
            "ref": None, "subdir": sub, "name": name, "sha256": f["provenance"]["sha256"],
            "url": f["provenance"]["source_url"], "retrieved": f["provenance"]["retrieved_at"],
            "model": model,
            "env": md.get("environment", "unknown"),
            "nsteps": md.get("steps"), "won": md.get("won"), "ts": md.get("timestamp"),
            "messages": t["messages"],
        }
    findings.append((fid, f, v))

for i, name in enumerate(sorted(trajs), 1):
    trajs[name]["ref"] = f"traj-{i:02d}"

records = []

def rec(kind, ref, body, tags):
    return {"kind": kind, "ref": ref, "body": body, "tags": tags}

lane = {"lane": LANE_TAG}

# ---- sources ----
records.append(rec("source", "src-dataset", {
    "source_type": "dataset",
    "locator": DATASET_FOLDER,
    "title": "AgentErrorBench failure-trajectory dataset (ulab-uiuc/AgentDebug)",
    "platform": "google_drive"}, dict(lane)))
records.append(rec("source", "src-paper", {
    "source_type": "paper",
    "locator": "https://arxiv.org/abs/2509.25370",
    "title": "AgentErrorBench (arXiv:2509.25370)",
    "platform": "arxiv"}, dict(lane)))
records.append(rec("source", "src-repo", {
    "source_type": "repository",
    "locator": "https://github.com/ulab-uiuc/AgentDebug",
    "title": "ulab-uiuc/AgentDebug",
    "platform": "github"}, dict(lane)))

# ---- dataset snapshot ----
records.append(rec("observation", "snap-dataset", {
    "type": "dataset.snapshot",
    "source": "@src-dataset",
    "observed_at": "2026-10-16T21:43:07Z",
    "time_basis": "source_metadata",
    "files": [],
    "data": {
        "dataset_uri": DATASET_FOLDER,
        "revision": "unknown; Drive folder last modified 2025-09-30 per embeddedfolderview; snapshot 2026-10-16",
        "coverage": "unknown",
    }}, dict(lane, **{"note": "dataset-level snapshot; per-file provenance lives on trajectory records"})))

# ---- trajectory artifacts (reference-only: locator without byte-preservation claim) ----
for name in sorted(trajs):
    t = trajs[name]
    prov_path = f"data/lanes/agenterrorbench-trajectories/raw/{t['subdir']}/{name}"
    t["art_ref"] = "art-" + t["ref"].split("-", 1)[1]
    records.append(rec("artifact", t["art_ref"], {
        "reference": {
            "uri": t["url"],
            "platform": "google_drive",
            "path": prov_path,
            "reported_sha256": t["sha256"],
        }}, dict(lane, **{"provenance_path": prov_path})))

# ---- trajectory observations ----
for name in sorted(trajs):
    t = trajs[name]
    prov_path = f"data/lanes/agenterrorbench-trajectories/raw/{t['subdir']}/{name}"
    records.append(rec("observation", t["ref"], {
        "type": "dataset.record",
        "source": "@src-dataset",
        "observed_at": t["retrieved"],
        "time_basis": "source_metadata",
        "files": [],
        "data": {
            "snapshot": "@snap-dataset",
            "locator": {"artifact": f"@{t['art_ref']}", "whole": True},
            "external_record_id": name,
        }}, dict(lane, **{"sha256": t["sha256"], "provenance_path": prov_path})))
    records.append(rec("edge", f"e-{t['ref']}", {
        "subject": f"@{t['ref']}",
        "predicate": "part_of",
        "object": "@snap-dataset",
        "note": f"Trajectory {name} is part of the AgentErrorBench dataset snapshot.",
    }, dict(lane)))

# ---- per-finding records ----
for fid, f, v in findings:
    t = trajs[f["trajectory_id"] if f["trajectory_id"].endswith(".json")
              else f["trajectory_id"] + ".json"]
    steps = expand_steps(f["steps"])
    msgs = t["messages"]

    entries = []
    for s in steps:
        idx = 2 * s - 1
        assert idx < len(msgs), (fid, s)
        c = msgs[idx]["content"]
        for channel, body in channel_entries(c):
            if t["env"] == "alfworld":
                tool, cmd = ("alfworld.action", body)
            elif channel == "answer":
                tool, cmd = ("answer", body)
            else:
                tool, cmd = parse_gaia_tool(body)
            entries.append({"index": s, "tool": tool, "command": cmd})
    assert entries, fid

    ts_prov = (f"Steps {f['steps']} extracted from trajectory {t['name']} "
               f"(sha256 {t['sha256']}); AgentDebug harness on {t['env']}; "
               f"trajectory {t['nsteps']} steps, won={t['won']}; "
               f"reviewer finding {fid}, verified against trajectory bytes 2026-10-16.")
    records.append(rec("observation", f"ts-{fid}", {
        "type": "behavior.tool_sequence",
        "source": "@src-dataset",
        "observed_at": t["retrieved"],
        "time_basis": "source_metadata",
        "files": [],
        "data": {
            "trajectory": t["url"],
            "model": t["model"],
            "harness": "agentdebug",
            "steps": entries,
            "length": len(entries),
            "provenance": ts_prov,
        }}, dict(lane)))

    quote = v["corrected_quote"] or f.get("quote") or ""
    desc_parts = [quote]
    if f.get("why_interesting"):
        desc_parts.append("Why interesting: " + f["why_interesting"])
    if v.get("notes"):
        desc_parts.append("Verifier: " + v["notes"])
    if f.get("novelty_note"):
        desc_parts.append("Novelty note: " + f["novelty_note"])
    description = "\n\n".join(desc_parts)

    beh_prov = (f"Reviewer finding {fid} (confidence {v['confidence']}, grade {v['grade']}), "
                f"verified against trajectory bytes 2026-10-16; verifier corrected the "
                f"quote where the filed quote was garbled. Review lane: "
                f"data/lanes/agenterrorbench-trajectories/review/.")
    records.append(rec("observation", f"beh-{fid}", {
        "type": "intel.behavior",
        "source": "@src-dataset",
        "observed_at": t["retrieved"],
        "time_basis": "source_metadata",
        "files": [],
        "data": {
            "category": CATEGORY[fid],
            "description": description,
            "severity": SEVERITY[fid],
            "models_affected": [t["model"]],
            "evaluations_seen_on": ["AgentErrorBench"],
            "first_observed": first_observed(t["ts"]),
            "provenance": beh_prov,
        }}, dict(lane, **{"confidence": v["confidence"], "grade": v["grade"]})))

    records.append(rec("edge", f"e-ts-{fid}", {
        "subject": f"@ts-{fid}",
        "predicate": "derived_from",
        "object": f"@{t['ref']}",
        "basis": "OBSERVED",
        "cites": [f"@{t['ref']}"],
        "note": f"Tool-call sequence for finding {fid} extracted from cited steps {f['steps']} of {t['name']}.",
    }, dict(lane)))
    records.append(rec("edge", f"e-beh-{fid}", {
        "subject": f"@beh-{fid}",
        "predicate": "derived_from",
        "object": f"@ts-{fid}",
        "basis": "INFERENCE",
        "cites": [f"@ts-{fid}"],
        "note": f"Behavior finding {fid} classified from the tool-call sequence {f['steps']} of {t['name']}.",
    }, dict(lane)))

bundle = {"bundle": 2, "actor": ACTOR, "idempotency_key": IDEMPOTENCY, "records": records}

# sanity checks
refs = [r["ref"] for r in records]
assert len(refs) == len(set(refs)), "dup refs"
for r in records:
    assert len(r["ref"]) <= 64
    assert r["tags"].get("lane") == LANE_TAG
    if r["kind"] == "observation":
        for key in ("type", "source", "observed_at", "time_basis", "files", "data"):
            assert key in r["body"], (r["ref"], key)
    if r["kind"] == "artifact":
        ref = r["body"].get("reference", {})
        assert ref.get("uri") and ref.get("reported_sha256"), r["ref"]
n_obs = sum(1 for r in records if r["kind"] == "observation")
n_edge = sum(1 for r in records if r["kind"] == "edge")
n_src = sum(1 for r in records if r["kind"] == "source")
print(f"sources={n_src} observations={n_obs} edges={n_edge} total={len(records)}")

outp = os.path.join(LANE, "bundle.json")
json.dump(bundle, open(outp, "w"), indent=1)
print("wrote", outp)
