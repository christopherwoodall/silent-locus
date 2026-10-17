#!/usr/bin/env python3
"""InterCode-CTF trajectories factum ingest bundle builder (INTERCODE-CTF INGESTOR).

Reads:
  raw/MANIFEST.json                         (13 HF datasets, per-file sha256 + retrieval times)
  raw/DATASET.md                            (per-dataset model/template table)
  raw/<shortname>/logs/inspect_evals/gdm_intercode_ctf/benign.eval   (inspect_ai eval ZIP journal)
  verified-findings.jsonl                   (18 byte-verified PRIMARY findings V-001..V-018)
  working/verifier-kills.md                 (kill/merge record)

Writes: bundle-intercode-ctf.json (factum bundle v2) + build-report.json

Bundle design:
  13 source records                 — one HF dataset each (apache-2.0)
  13 artifact records               — one benign.eval ZIP each (sha256+size)
   1 run record                     — the scrape (min/max retrieved_utc)
   1 dataset.snapshot observation   — lane-wide snapshot, 835 rows
 835 dataset.record observations    — one per sample (lean attributes; NO step content)
  19 behavior.tool_sequence observations — one per finding-bearing trajectory
  18 intel.behavior observations    — one per verified finding
 835 edges (run -related_to-> trajectory record)
  20 edges (finding -supports-> trajectory record)  [V-002, V-003 are corpus
        aggregates with no single trajectory: no tool_sequence / no edges, documented]

Rules honored: tags.lane on EVERY record incl. bundle-local sources;
observations carry observed_at + time_basis (collector_clock, retrieval UTC);
claims cite observations only (no claims filed here); no full step content
embedded (raw ZIPs are the byte store); intel.behavior categories come from
docs/taxonomy/behavior-categories.md (6 new eval-derived categories added
there per the taxonomy's own "Adding categories" procedure).
Dedup anchor: behavior.tool_sequence + trajectory ID.
"""
import json
import os
import re
import sys
import hashlib
import zipfile
from collections import Counter

LANE = "intercode-ctf-trajectories"
ACTOR = "agent:intercode-ctf-ingestor"
IDEMPOTENCY = "intercode-ctf-ingest-2026-10-16-v1"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
MANIFEST_PATH = os.path.join(RAW, "MANIFEST.json")
FINDINGS_PATH = os.path.join(HERE, "verified-findings.jsonl")
OUT_BUNDLE = os.path.join(HERE, "bundle-intercode-ctf.json")
OUT_REPORT = os.path.join(HERE, "build-report.json")
HARNESS = "inspect_ai eval journal (task inspect_evals/gdm_intercode_ctf)"

MODELS = {
    "70B_normal_llama_33_70b_instruct_gdm_intercode_ctf": "vllm/meta-llama/Llama-3.3-70B-Instruct",
    "devstral_normal_devstral_small_2505_gdm_intercode_ctf": "vllm/mistralai/Devstral-Small-2505",
    "normal_llama_31_8b_instruct_gdm_intercode_ctf": "vllm/meta-llama/Llama-3.1-8B-Instruct",
    "odran_default_llama_33_70b_instruct_gdm_intercode_ctf": "vllm/meta-llama/Llama-3.3-70B-Instruct",
    "odran_elicitation_llama_33_70b_instruct_gdm_intercode_ctf": "vllm/meta-llama/Llama-3.3-70B-Instruct",
    "odran_default_server_llama_33_70b_instruct_gdm_intercode_ctf": "openai/meta-llama/Llama-3.3-70B-Instruct",
    "odran_elicitation_server_llama_33_70b_instruct_gdm_intercode_ctf": "openai/meta-llama/Llama-3.3-70B-Instruct",
    "odran_default_odran_gdm_intercode_ctf": "vllm/meta-llama/Llama-3.3-70B-Instruct",
    "odran_elicitation_odran_elicitation_gdm_intercode_ctf": "vllm/meta-llama/Llama-3.3-70B-Instruct",
    "odran_default_odran_llama33_70b_20250620_160734_gdm_intercode_ctf": "vllm/meta-llama/Llama-3.3-70B-Instruct",
    "odran_elicitation_odran_llama33_70b_20250620_160734_gdm_intercode_ctf": "vllm/meta-llama/Llama-3.3-70B-Instruct",
    "odran_default_odran_llama33_70b_20250622_105629_step1600_gdm_intercode_ctf": "vllm/meta-llama/Llama-3.3-70B-Instruct",
    "odran_default_odran_20250619_075549_gdm_intercode_ctf": "vllm/odran_20250619_075549",
}

# finding_id -> (taxonomy category, severity, list of (shortname, sample_id, step_range))
FINDING_TRAJS = {
    "V-001": ("guardrail-erosion", "high", [("devstral_normal_devstral_small_2505_gdm_intercode_ctf", 30, "2-14")]),
    "V-002": ("refusal-absence", "high", []),          # corpus aggregate: no single trajectory
    "V-003": ("tool-protocol-misuse", "moderate", []), # corpus aggregate: no single trajectory
    "V-004": ("tool-protocol-misuse", "moderate", [("odran_default_llama_33_70b_instruct_gdm_intercode_ctf", 0, "4-22")]),
    "V-005": ("tool-output-confabulation", "high", [("odran_default_odran_20250619_075549_gdm_intercode_ctf", 17, "2-22")]),
    "V-006": ("tool-protocol-misuse", "moderate", [
        ("odran_default_odran_20250619_075549_gdm_intercode_ctf", 11, "4-6"),
        ("odran_elicitation_odran_elicitation_gdm_intercode_ctf", 45, "17")]),
    "V-007": ("generation-silence", "moderate", [("odran_default_odran_20250619_075549_gdm_intercode_ctf", 0, "2-22")]),
    "V-008": ("generation-stall", "moderate", [
        ("odran_default_odran_20250619_075549_gdm_intercode_ctf", 13, "0-1"),
        ("odran_default_odran_20250619_075549_gdm_intercode_ctf", 83, "0-1")]),
    "V-009": ("tool-protocol-misuse", "moderate", [("odran_default_odran_gdm_intercode_ctf", 56, "17-20")]),
    "V-010": ("confabulation-under-retrieval-failure", "high", [
        ("70B_normal_llama_33_70b_instruct_gdm_intercode_ctf", 56, "17-22"),
        ("odran_default_odran_gdm_intercode_ctf", 56, "14-21")]),
    "V-011": ("unapproved-edits", "high", [("odran_elicitation_odran_llama33_70b_20250620_160734_gdm_intercode_ctf", 61, "9-12")]),
    "V-012": ("recovery-livelock", "moderate", [("odran_default_odran_20250619_075549_gdm_intercode_ctf", 51, "6-21")]),
    "V-013": ("tool-protocol-misuse", "moderate", [("devstral_normal_devstral_small_2505_gdm_intercode_ctf", 53, "4-6")]),
    "V-014": ("confabulation-under-retrieval-failure", "moderate", [("odran_default_llama_33_70b_instruct_gdm_intercode_ctf", 64, "4-6")]),
    "V-015": ("false-capability-denial", "moderate", [("devstral_normal_devstral_small_2505_gdm_intercode_ctf", 38, "2-22")]),
    "V-016": ("tool-protocol-misuse", "moderate", [("normal_llama_31_8b_instruct_gdm_intercode_ctf", 65, "2-4")]),
    "V-017": ("recovery-livelock", "low", [("70B_normal_llama_33_70b_instruct_gdm_intercode_ctf", 69, "6-14")]),
    "V-018": ("recovery-livelock", "moderate", [("odran_default_odran_gdm_intercode_ctf", 15, "10-24")]),
}

# Aggregate findings: which single source the observation envelope links to,
# plus the full aggregate list in tags.
AGG_SOURCE = {"V-002": "d01", "V-003": "d05"}
AGG_DATASETS = {
    "V-002": ["70B_normal_llama_33_70b_instruct_gdm_intercode_ctf",
              "normal_llama_31_8b_instruct_gdm_intercode_ctf",
              "odran_default_llama_33_70b_instruct_gdm_intercode_ctf",
              "odran_elicitation_llama_33_70b_instruct_gdm_intercode_ctf",
              "odran_default_odran_gdm_intercode_ctf",
              "odran_elicitation_odran_elicitation_gdm_intercode_ctf",
              "odran_default_odran_llama33_70b_20250620_160734_gdm_intercode_ctf",
              "odran_elicitation_odran_llama33_70b_20250620_160734_gdm_intercode_ctf",
              "odran_default_odran_llama33_70b_20250622_105629_step1600_gdm_intercode_ctf",
              "odran_default_odran_20250619_075549_gdm_intercode_ctf"],
    "V-003": ["odran_elicitation_llama_33_70b_instruct_gdm_intercode_ctf",
              "odran_default_llama_33_70b_instruct_gdm_intercode_ctf",
              "odran_elicitation_odran_elicitation_gdm_intercode_ctf",
              "odran_default_odran_gdm_intercode_ctf"],
}


def fail(msg):
    print("BUILD-FAIL:", msg, file=sys.stderr)
    sys.exit(2)


def main():
    manifest = json.load(open(MANIFEST_PATH))
    shortnames = list(manifest.keys())
    if len(shortnames) != 13:
        fail("manifest dataset count %d != 13" % len(shortnames))
    dnum = {s: "d%02d" % (i + 1) for i, s in enumerate(shortnames)}

    findings = [json.loads(l) for l in open(FINDINGS_PATH)]
    if len(findings) != 18:
        fail("finding count %d != 18" % len(findings))
    fmap = {f["id"]: f for f in findings}
    for fid in FINDING_TRAJS:
        if fid not in fmap:
            fail("finding %s missing from verified-findings.jsonl" % fid)

    # ---- per-dataset ZIP facts + sample enumeration ----
    ds = {}
    zip_cache = {}
    started, ended = None, None
    total_samples = 0
    for s in shortnames:
        meta = manifest[s]
        entry = next(f for f in meta["files"] if f["path"].endswith("benign.eval"))
        zpath = os.path.join(RAW, s, "logs/inspect_evals/gdm_intercode_ctf/benign.eval")
        if not os.path.isfile(zpath):
            fail("ZIP missing: " + zpath)
        z = zipfile.ZipFile(zpath)
        zip_cache[s] = z
        samples = sorted(
            (int(re.search(r"samples/(\d+)_epoch_1\.json", n).group(1)), n)
            for n in z.namelist()
            if re.fullmatch(r"samples/\d+_epoch_1\.json", n))
        ds[s] = {"dataset_id": meta["dataset_id"], "rev": meta["rev"],
                 "sha256": entry["sha256"], "size": entry["size_bytes"],
                 "url": entry["url"], "retrieved": entry["retrieved_utc"],
                 "samples": samples}
        r = entry["retrieved_utc"]
        started = r if started is None or r < started else started
        ended = r if ended is None or r > ended else ended
        total_samples += len(samples)
    if total_samples != 835:
        fail("sample count %d != 835" % total_samples)

    records = []

    def rec(ref, kind, body, tags):
        tags = dict(tags)
        tags["lane"] = LANE
        records.append({"ref": ref, "kind": kind, "body": body, "tags": tags})

    # ---- 13 sources ----
    for s in shortnames:
        n = dnum[s]
        info = ds[s]
        rec("src-" + n, "source", {
            "source_type": "dataset",
            "locator": "https://huggingface.co/datasets/" + info["dataset_id"],
            "title": info["dataset_id"] + ": InterCode-CTF agent trajectories "
                     "(inspect_ai eval journal, task inspect_evals/gdm_intercode_ctf)",
            "platform": "huggingface",
        }, {
            "dataset_id": info["dataset_id"],
            "revision": info["rev"],
            "license": "apache-2.0",
            "model": MODELS[s],
            "sample_count": str(len(info["samples"])),
            "eval_zip_sha256": info["sha256"],
        })

    # ---- 13 artifacts (the eval ZIP journals) ----
    for s in shortnames:
        n = dnum[s]
        info = ds[s]
        rec("art-" + n, "artifact", {
            "sha256": info["sha256"],
            "size": info["size"],
        }, {
            "dataset_shortname": s,
            "filename": "benign.eval",
            "rel_path": "data/lanes/intercode-ctf-trajectories/raw/%s/"
                        "logs/inspect_evals/gdm_intercode_ctf/benign.eval" % s,
            "retrieval_url": info["url"],
        })

    # ---- 1 run ----
    inputs = [ds[s]["url"] for s in shortnames]
    rec("run-scrape", "run", {
        "run_kind": "scrape",
        "tool": "curl",
        "tool_version": "https-get per-file",
        "started": started,
        "ended": ended,
        "params": {
            "inputs": inputs,
            "dataset_ids": [ds[s]["dataset_id"] for s in shortnames],
            "method": "per-file https-get with sha256 sidecars; "
                      "13 InterCode-CTF eval datasets, apache-2.0",
        },
        "coverage": {
            "complete": True,
            "scanned": total_samples,
            "total": total_samples,
            "description": "13 InterCode-CTF trajectory datasets scraped from "
                           "HuggingFace; 835 benign.eval journal samples.",
        },
    }, {"dataset_count": "13", "sample_count": str(total_samples)})

    # ---- 1 dataset.snapshot ----
    rec("snap-lane", "observation", {
        "type": "dataset.snapshot",
        "source": "@src-d01",
        "run": "@run-scrape",
        "observed_at": ended,
        "time_basis": "collector_clock",
        "files": [],
        "data": {
            "dataset_uri": "huggingface://jordan-taylor-aisi (13 "
                           "intercode-ctf eval datasets; per-dataset "
                           "revisions in source tags)",
            "coverage": "complete",
            "row_count": total_samples,
        },
    }, {"dataset_count": "13", "anchor_source": "src-d01"})

    # ---- 835 lean dataset.record observations + run->trajectory edges ----
    sample_cache = {}

    def get_sample(s, sid):
        key = (s, sid)
        if key not in sample_cache:
            n = dict((i, nm) for i, nm in ds[s]["samples"])[sid]
            sample_cache[key] = json.loads(zip_cache[s].read(n))
        return sample_cache[key]

    n_rec_edges = 0
    for s in shortnames:
        n = dnum[s]
        info = ds[s]
        for sid, nm in info["samples"]:
            rec_obj = get_sample(s, sid)
            msgs = rec_obj.get("messages", []) or []
            tc_count = sum(len(m.get("tool_calls") or []) for m in msgs
                           if isinstance(m, dict))
            score = ""
            try:
                score = str((rec_obj.get("scores") or {}).get("includes",
                            {}).get("value", ""))
            except Exception:
                pass
            tref = "traj-%s-s%03d" % (n, sid)
            rec(tref, "observation", {
                "type": "dataset.record",
                "source": "@src-" + n,
                "run": "@run-scrape",
                "observed_at": info["retrieved"],
                "time_basis": "collector_clock",
                "files": [{
                    "artifact": "@art-" + n,
                    "role": "eval-journal-zip",
                    "filename": "benign.eval",
                }],
                "data": {
                    "snapshot": "@snap-lane",
                    "locator": {"artifact": "@art-" + n,
                                "row": {"index": sid,
                                        "key": "samples/%d_epoch_1.json" % sid}},
                    "external_record_id": "sample %d" % sid,
                },
            }, {
                "dataset_shortname": s,
                "sample_id": str(sid),
                "message_count": str(len(msgs)),
                "tool_call_count": str(tc_count),
                "score": score,
            })
            rec("edge-run-%s-s%03d" % (n, sid), "edge", {
                "subject": "@run-scrape",
                "predicate": "related_to",
                "object": "@" + tref,
                "basis": "OBSERVED",
                "cites": ["@" + tref],
                "note": "scrape run acquired the trajectory sample",
            }, {"dataset_shortname": s, "sample_id": str(sid)})
            n_rec_edges += 1

    # ---- behavior.tool_sequence per UNIQUE finding trajectory (parsed from ZIP bytes) ----
    def extract_tool_calls(s, sid):
        rec_obj = get_sample(s, sid)
        steps = []
        for i, m in enumerate(rec_obj.get("messages", []) or []):
            if not isinstance(m, dict) or m.get("role") != "assistant":
                continue
            for tc in m.get("tool_calls") or []:
                fn = tc.get("function", "?")
                args = json.dumps(tc.get("arguments", {}), sort_keys=True,
                                  ensure_ascii=False)
                if len(args) > 300:
                    args = args[:300] + "...[truncated]"
                steps.append({"index": i, "tool": fn, "command": "%s(%s)" % (fn, args)})
        return steps

    # unique trajectories across all findings (V-009 and V-010 both use d8 sample 56)
    uniq_trajs = []
    for fid, (cat, sev, trajs) in FINDING_TRAJS.items():
        for (s, sid, step_range) in trajs:
            if (s, sid) not in uniq_trajs:
                uniq_trajs.append((s, sid))
    finding_step_range = {}
    for fid, (cat, sev, trajs) in FINDING_TRAJS.items():
        for (s, sid, step_range) in trajs:
            finding_step_range[(fid, s, sid)] = step_range

    seq_ref_of = {}
    for (s, sid) in uniq_trajs:
        n = dnum[s]
        info = ds[s]
        steps = extract_tool_calls(s, sid)
        tref = "traj-%s-s%03d" % (n, sid)
        locator = ("huggingface://%s@%s/"
                   "logs/inspect_evals/gdm_intercode_ctf/benign.eval"
                   "#samples/%d_epoch_1.json") % (info["dataset_id"], info["rev"], sid)
        sref = "seq-%s-s%03d" % (n, sid)
        seq_ref_of[(s, sid)] = sref
        fid_list = sorted(fid for (fid, ts, tsid) in finding_step_range if (ts, tsid) == (s, sid))
        rec(sref, "observation", {
            "type": "behavior.tool_sequence",
            "source": "@src-" + n,
            "run": "@run-scrape",
            "observed_at": info["retrieved"],
            "time_basis": "collector_clock",
            "files": [{
                "artifact": "@art-" + n,
                "role": "eval-journal-zip",
                "filename": "benign.eval",
            }],
            "data": {
                "trajectory": locator,
                "model": MODELS[s],
                "harness": HARNESS,
                "steps": steps,
                "length": len(steps),
                "provenance": ("InterCode-CTF lane: tool calls extracted "
                               "from assistant messages of %s in %s "
                               "(benign.eval sha256=%s); trajectory "
                               "record @%s; findings %s")
                              % (locator.split("#")[1], s,
                                 info["sha256"][:16], tref, ",".join(fid_list)),
            },
        }, {
            "finding_ids": ",".join(fid_list),
            "trajectory": "%s#sample %d" % (s, sid),
            "length": str(len(steps)),
        })

    # ---- intel.behavior per finding ----
    n_finding_edges = 0
    for fid, (cat, sev, trajs) in FINDING_TRAJS.items():
        f = fmap[fid]
        if trajs:
            s = trajs[0][0]
            n = dnum[s]
            info = ds[s]
            seq_locators = []
            for (ts, tsid, trange) in trajs:
                tn = dnum[ts]
                tinfo = ds[ts]
                seq_locators.append(
                    ("huggingface://%s@%s/logs/inspect_evals/gdm_intercode_ctf/"
                     "benign.eval#samples/%d_epoch_1.json (tool_sequence @%s)")
                    % (tinfo["dataset_id"], tinfo["rev"], tsid,
                       seq_ref_of[(ts, tsid)]))
            src_ref = "@src-" + n
            src_tag = {"primary_dataset": s}
            models = sorted({MODELS[t[0]] for t in trajs})
        else:
            agg = AGG_DATASETS[fid]
            n = AGG_SOURCE[fid]
            info = ds[[s for s in shortnames if dnum[s] == n][0]]
            seq_locators = []
            src_ref = "@src-" + n
            src_tag = {"aggregate_datasets": ";".join(agg)}
            models = sorted({MODELS[a] for a in agg})
        description = (
            "[%s] Finding %s (reviewer class %s; verifier: byte-verified in "
            "raw bytes, grade %s, confidence %s). %s "
            "Evidence quote (verbatim): %s "
            "Verifier note: %s"
            % (cat, fid, f["class"], f["grade"], f["confidence"],
               f["why_interesting"], f["quote"], f["verifier_note"]))
        if seq_locators:
            description += " Tool-sequence trajectories: " + "; ".join(seq_locators) + "."
        bref = "behavior-" + fid.lower().replace("-", "")
        body = {
            "type": "intel.behavior",
            "source": src_ref,
            "run": "@run-scrape",
            "observed_at": info["retrieved"],
            "time_basis": "collector_clock",
            "files": [],
            "data": {
                "category": cat,
                "description": description,
                "evaluations_seen_on": ["gdm_intercode_ctf"],
                "models_affected": models,
                "first_observed": "2025-06",
                "provenance": ("InterCode-CTF trajectory review lane; "
                               "verified-findings.jsonl %s; source_file %s; "
                               "eval-ZIP sha256 %s")
                              % (fid, f["source_file"], f["sha256"]),
                "severity": sev,
            },
        }
        tags = {
            "finding_id": fid,
            "class": f["class"],
            "grade": f["grade"],
            "confidence": f["confidence"],
            "category": cat,
            "step_range": f["steps"],
            "trajectory_id": f["trajectory_id"],
            "dataset": f["dataset"][:400],
            "evidence_quote": f["quote"][:2000],
        }
        tags.update(src_tag)
        rec(bref, "observation", body, tags)
        for j, (ts, tsid, trange) in enumerate(trajs):
            tn = dnum[ts]
            tref = "traj-%s-s%03d" % (tn, tsid)
            eref = "edge-finding-%s%s" % (fid.lower().replace("-", ""),
                                          chr(97 + j) if len(trajs) > 1 else "")
            rec(eref, "edge", {
                "subject": "@" + bref,
                "predicate": "supports",
                "object": "@" + tref,
                "basis": "OBSERVED",
                "cites": ["@" + bref],
                "note": "finding %s observed in trajectory steps %s" % (fid, trange),
            }, {"finding_id": fid, "trajectory": "%s#sample %d" % (ts, tsid)})
            n_finding_edges += 1

    # ---- sanity: every tool_sequence has length == len(steps) ----
    for r in records:
        if r["kind"] == "observation" and r["body"].get("type") == "behavior.tool_sequence":
            assert r["body"]["data"]["length"] == len(r["body"]["data"]["steps"]), r["ref"]
    print("tool_sequence length checks ok")

    # ---- sanity: dedup anchor uniqueness (tool_sequence + trajectory) ----
    anchors = [(tuple((st["index"], st["tool"]) for st in
                      r["body"]["data"]["steps"]),
                r["body"]["data"]["trajectory"]) for r in records
               if r["kind"] == "observation"
               and r["body"].get("type") == "behavior.tool_sequence"]
    if len(set(anchors)) != len(anchors):
        fail("duplicate behavior.tool_sequence+trajectory anchor in batch")

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": IDEMPOTENCY,
        "lane": LANE,
        "records": records,
    }
    with open(OUT_BUNDLE, "w") as fh:
        json.dump(bundle, fh)

    kinds = Counter(
        r["kind"] + (":" + r["body"].get("type") if r["kind"] == "observation" else "")
        for r in records)
    report = {
        "datasets": len(shortnames),
        "samples": total_samples,
        "findings": len(findings),
        "tool_sequences": len(anchors),
        "finding_edges": n_finding_edges,
        "run_traj_edges": n_rec_edges,
        "record_count": len(records),
        "record_kinds": dict(kinds),
        "sha256_bundle": hashlib.sha256(open(OUT_BUNDLE, "rb").read()).hexdigest(),
        "aggregates_without_trajectory": ["V-002", "V-003"],
        "retrieval_started": started,
        "retrieval_ended": ended,
    }
    json.dump(report, open(OUT_REPORT, "w"), indent=1)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
