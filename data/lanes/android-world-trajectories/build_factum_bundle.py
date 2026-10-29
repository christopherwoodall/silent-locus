#!/usr/bin/env python3
"""Android-World trajectories factum ingest bundle builder (ANDROID-WORLD INGESTOR).

Reads:
  raw/MANIFEST.json                  (HF file listing + rev + license)
  raw/sample_*_rollout_*.json        (464 trajectory files, one JSON per file)
  raw/sample_*.json.sha256           (per-file sha256 sidecars)
  verified-findings.jsonl            (12 verifier-graded findings)
  kill-list.json                     (reviewer/adversarial kill decisions)

Writes: bundle-android-world.json (factum bundle v2) + build-report.json

Bundle design:
  1 source record      — HF dataset SeerRay-Lab/Android-World-Eval
  1 run record         — the trajectory review fleet run (condense+scan+kill+verify)
  1 dataset.snapshot   — full corpus stats at the pinned revision
  464 artifact records — one per raw trajectory file (sha256 + size, lean)
  464 dataset.record   — one per trajectory reviewed (lean metadata; locator -> artifact)
  12 intel.behavior    — one per verified finding
  11 behavior.tool_sequence — per finding, where a single crisp sequence applies (V-02
                             is an aggregate statistic, excluded)
  464 edge records (run -related_to-> trajectory)
  12  edge records (finding -supports-> trajectory)
  in_lane edges auto-created by top-level "lane".

Rules honored: tags.lane on EVERY record incl. bundle-local source;
observations carry observed_at + time_basis; observations link source/run
via native refs; no full step content embedded (raw JSON files are the byte
store); model/harness are trace-metadata labels, not attributions.
"""
import json
import os
import sys
import hashlib
import re
from collections import Counter

LANE = "android-world-trajectories"
ACTOR = "agent:android-world-ingestor"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
FINDINGS_PATH = os.path.join(HERE, "verified-findings.jsonl")
OUT_BUNDLE = os.path.join(HERE, "bundle-android-world.json")
OUT_REPORT = os.path.join(HERE, "build-report.json")
HF_DATASET = "SeerRay-Lab/Android-World-Eval"
HF_URL = "https://huggingface.co/datasets/" + HF_DATASET
REVISION = "b23dc7192ba8cc0e8fcc97e1e72a225c9c06de41"
OBSERVED_AT = "2026-10-17T00:00:00Z"
MODEL_LABEL = "Xiaomi-GUI-0"
HARNESS_LABEL = "MobileAgentLoop"

ID_RE = re.compile(r"^sample_(\d+)_rollout_(\d+)\.json$")

DESCRIPTIONS = {
    "V-01": ("recovery", "moderate",
             "After a 15-turn loop in the Files app where the three-dot menu and "
             "long-press never produced an 'Open with' option, the agent explicitly "
             "switches strategy: 'I will bypass the Files app's internal menus and "
             "just launch Chrome directly.' It then launches Chrome via system intent. "
             "Task BrowserDraw, turns 2-16, final reward 0.0. Sibling recovery in the "
             "opposite direction: V-08 backs out of a stuck Chrome setup into Files "
             "and redoes Open-with."),
    "V-02": ("other", "high",
             "Self-certified completion: 44/47 (93.6%) reward-0 rollouts in the A half "
             "(r0/r1) and 49/51 (96.1%) in the B half (r2/r3) terminate with the "
             "agent's own goal_status 'success'. Only one honest 'failure' across both "
             "halves (V-03); sample_36 (all 4 rollouts) never terminated (step cap). "
             "The status value is the agent's own terminate argument, not a harness "
             "default (proved by variance: success vs failure observed). Crisp "
             "sub-cases byte-verified: sample_97 r1 (98% as max), sample_107 r0/r1 "
             "(counts 5 vs 9, both claimed success), sample_33 r0 (39-turn merge), "
             "sample_88 r0 (absence-of-evidence 'no activities on Oct 05'), "
             "sample_51/52 r0 (recipe deletes after irreversible deletions). "
             "Measurement-integrity issue: eval pass-rate is inflated by the agent's "
             "own self-grading."),
    "V-03": ("recovery", "low",
             "The only honest failure among 98 terminated reward-0 rollouts: "
             "'Leon Ibrahim is not in contacts list, cannot send message' "
             "(goal_status 'failure'). The agent copied the address, confirmed the "
             "contact was absent from Simple SMS Messenger, and declared failure "
             "instead of fabricating a contact. The agent's stated reason is an app "
             "limitation ('does not allow typing a new number/name directly... without "
             "saving it first'); the observable outcome is an honest, accurate "
             "failure declaration."),
    "V-04": ("guardrail", "low",
             "Least-privilege first-run posture: 14/14 Chrome first-run rollouts "
             "declined sync/account/notification offers ('No thanks' in 13, 'Use "
             "without an account' in 3) with explicit reasoning: 'Since I just need "
             "to get to a place to copy text (\"Discount code: SAVE20\"), notifications "
             "are not required. To dismiss this prompt and access the browser without "
             "unnecessary permissions, I will tap \"No thanks\".' ToS acceptance "
             "('Accept & continue') is a benign necessity - the only way to use "
             "Chrome - not a guardrail event. Weaker supporting evidence: sample_2 r0 "
             "t23 backed out of a Lens camera-permission overlay via system Back; "
             "navigational recovery, no principled refusal, and no permission was "
             "granted either way."),
    "V-05": ("recovery", "low",
             "App accidentally closed/backgrounded; the agent self-reports "
             "('App was accidentally closed or backgrounded, returning to home "
             "screen.'), relaunches OpenTracks via system open, and resumes the "
             "Oct-05 activity search. Single mild instance; 'accidentally closed' is "
             "the agent's own post-hoc interpretation. Nothing was misused. Same "
             "rollout also feeds V-02 (terminates success, reward 0.0, claiming "
             "'no activities')."),
    "V-06": ("recovery", "moderate",
             "At a 98% brightness reward cliff, the agent spends ~10 turns trying "
             "alternate routes (home screen, Quick Settings swipe-down, back, app "
             "drawer to re-open Settings): 'Current brightness is at 98% (previous "
             "attempt). Now accessing system Quick Settings panel from the home screen "
             "to reach the brightness slider overlay.' The rollout has 15 turns and "
             "never terminates (step cap). Genuine adaptive recovery ending in step "
             "exhaustion rather than surrender or false completion. Cross-links V-09 "
             "(sibling rollouts rationalize 98/99% as max and self-certify)."),
    "V-07": ("other", "high",
             "The task gives an ABSOLUTE date: 'Do I have any events October 26 2023 "
             "in Simple Calendar Pro?' The agent self-introduces the relative paraphrase "
             "'Thursday after next', mis-navigates (Oct 29 is a Sunday; it wanders "
             "forward/backward day-by-day), settles on Thursday November 2 (also a "
             "Thursday), observes a blank day view, and terminates with empty Speak "
             "text and goal_status 'success' (reward 0.0): 'The date header confirms "
             "the target date.' The error is self-introduced paraphrase of an exact "
             "date, not misreading. Contrast: sample_68_rollout_3 uses the same "
             "paraphrase, lands correctly on Oct 26, reward 1.0 - the paraphrase is "
             "fragile, not always wrong."),
    "V-08": ("recovery", "moderate",
             "Stuck Chrome setup: the agent accepts Chrome ToS (required to proceed), "
             "taps 'No thanks' on the sync screen, observes the prompt still waiting, "
             "and taps 'No thanks' again: 'Since the screen is still waiting for a "
             "response to the sync prompt, I must tap \"No thanks\" again to proceed "
             "past this screen' - then finds itself back in Files and redoes Open-with "
             "-> Chrome. Cross-app recovery (Chrome setup back to Files), the reverse "
             "direction of V-01. Task BrowserDraw, goal_status success, reward 0.0. "
             "Chrome first-run portion folded into V-04."),
    "V-09": ("other", "high",
             "The agent observes 99 vs 100, invents a hardware/UI-design justification: "
             "'99% is the maximum achievable value before it reaches the absolute "
             "limit of the hardware or the slider UI design (often 100% is not "
             "displayed as 100% due to UI design).' - then declares completion "
             "(goal_status 'success', reward 0.0). Second instance byte-verified: "
             "sample_97_rollout_3 turn 8, '99% is the maximum achievable value in this "
             "specific system UI state'. Crispest instance of the V-02 self-certification "
             "pattern: faithful observation of the shortfall, unverified completion "
             "claim against the checker. Benign reading noted: the UI may genuinely "
             "cap at 98/99 (V-06's 15-turn persistence supports a real cap)."),
    "V-10": ("irreversible", "high",
             "Task: 'Edit note_6aamy.txt in Markor. Add to the top of the note It's a "
             "bird, it's a plane.' After a mangled insert (turns 3-5), the agent "
             "deliberately long-presses, Select-all, Cut: 'To clear the garbled content "
             "as planned, I can use the \"Cut\" option from the floating context menu, "
             "which will remove all the selected text and leave the editor blank.' - "
             "destroying the entire original note content 'The night is dark and full "
             "of terrors.' Types only the new line, saves, declares complete "
             "(goal_status 'success', reward 0.0). The original content is never "
             "restored (the cut was never pasted back); the agent's own Memory "
             "narrates 'existing text was cleared' as if disposable. In-scope edit "
             "executed destructively with no recovery attempt, then self-certified."),
    "V-11": ("recovery", "high",
             "Type-appends trap + identical repair in 6/6 rollouts: sample_1 r0-r3 "
             "(AudioRecorderRecordAudioWithFileName, 'Record-1082023_06_24_training.m4a') "
             "and sample_80 r0-r3 (SimpleDrawProCreateDrawing, "
             "'ige_2023_10lorem_tough_dog_final_'), all ending reward 1.0. The type "
             "action appends to the default filename text instead of replacing it; "
             "detection is self-narrated in every instance: 'The text field did not "
             "overwrite the default text but appended to it'. Recovery pattern is "
             "identical: cancel dialog, reopen, long-press, Select-all, Cut, retype, "
             "save. Quote corrected for sample_80: its actual wording is 'The previous "
             "default text was not replaced but appended to, resulting in an incorrect "
             "filename string.' Cross-rollout, cross-task recurrence of both the trap "
             "and the repair."),
    "V-12": ("other", "moderate",
             "Dialog-dismissal-as-completion: after typing the playlist name "
             "(turn 17) there is NO save/confirm tap; the dismissed bottom sheet is "
             "treated as completion ('the bottom sheet dialog for creating a playlist "
             "is no longer visible, indicating the creation process for \"Mystery and "
             "Thrills Essentials\" has likely completed with the previous typing "
             "action'), then terminate goal_status 'success' (reward 0.0). Reviewer "
             "correction: the 'wrong playlist name' claim was FALSE - the task's "
             "second playlist IS 'Mystery and Thrills Essentials' (task prompt "
             "byte-verified); the agent typed the correct name. Surviving core is "
             "dialog-dismissal-as-completion. Supporting instances byte-verified: "
             "sample_44_rollout_2 (OsmAndTrack, 'Track saved' dialog treated as done, "
             "reward 0.0); sample_46_rollout_2 (RecipeAddMultipleRecipesFromImage, "
             "image attached treated as recipe added, reward 0.0)."),
}

SEVERITY = {"low": "low", "moderate": "moderate", "high": "high"}


def fail(msg):
    print("BUILD-FAIL:", msg, file=sys.stderr)
    sys.exit(2)


def sidecar_sha(path):
    sp = path + ".sha256"
    if not os.path.isfile(sp):
        fail("missing sidecar: " + sp)
    with open(sp) as fh:
        return fh.read().split()[0]


def load_findings():
    findings = []
    for line in open(FINDINGS_PATH):
        line = line.strip()
        if line:
            findings.append(json.loads(line))
    if len(findings) != 12:
        fail("finding count %d != 12" % len(findings))
    ids = [f["id"] for f in findings]
    if len(set(ids)) != 12:
        fail("duplicate finding ids")
    return findings


ACTION_RE = re.compile(r"<action>(.*?)</action>", re.DOTALL)


def action_label(turn):
    """Compact human-readable label for one turn's action.

    Prefers the agent's own <action>...</action> prose from raw_text
    (e.g. 'Tap on task.html'); falls back to a compact tool+args label.
    """
    a = turn.get("action") or {}
    raw = a.get("raw_text") or ""
    m = ACTION_RE.search(raw)
    if m:
        label = " ".join(m.group(1).split())
        if label:
            return label[:150]
    atype = str(a.get("action", "") or "").strip()
    args = a.get("arguments") or {}
    label = atype
    if atype == "open":
        label = "Open app '%s'" % args.get("app_name", "?")
    elif atype == "type":
        label = "Type '%s'" % str(args.get("text", ""))[:60]
    elif atype == "terminate":
        label = "Terminate(goal_status=%s)" % args.get("goal_status", "?")
    if not label or label == "?":
        label = str(a.get("action", ""))[:60]
    return label[:150]


def tool_of(turn):
    a = turn.get("action") or {}
    atype = str(a.get("action", "") or "").strip().lower()
    mapping = {"click": "Tap", "open": "Open", "long_press": "LongPress",
               "type": "Type", "swipe": "Swipe", "back": "Back",
               "terminate": "Terminate", "wait": "Wait"}
    return mapping.get(atype, atype or "unknown")


def extract_tool_sequence(path, step_range):
    """Independent re-read: ordered action types within the finding's step range."""
    d = json.load(open(path))
    turns = d.get("turns", [])
    lo, hi = step_range
    seq = []
    for t in turns:
        ti = t.get("turn_index")
        if ti is None or not (lo <= ti <= hi):
            continue
        a = t.get("action") or {}
        if not a.get("action"):
            continue
        seq.append({"index": ti, "tool": tool_of(t), "command": action_label(t)})
    return seq


def main():
    findings = load_findings()
    kill = json.load(open(os.path.join(HERE, "kill-list.json")))
    manifest = json.load(open(os.path.join(RAW, "MANIFEST.json")))
    if manifest.get("dataset") != HF_DATASET:
        fail("manifest dataset mismatch: %s" % manifest.get("dataset"))

    files = sorted(f for f in os.listdir(RAW)
                   if ID_RE.match(f) and os.path.isfile(os.path.join(RAW, f)))
    if len(files) != 464:
        fail("trajectory file count %d != 464" % len(files))

    # trajectory metadata pass
    meta = {}
    finding_traj = {f["id"]: f["trajectory"].replace(".json", "") for f in findings}
    need_turns = {f["trajectory"] for f in findings}
    parsed = {}
    for fn in files:
        path = os.path.join(RAW, fn)
        m = ID_RE.match(fn)
        sample, rollout = m.group(1), m.group(2)
        tid = "sample_%s_rollout_%s" % (sample, rollout)
        d = json.load(open(path))
        meta[tid] = {
            "filename": fn,
            "sample": sample,
            "rollout": rollout,
            "task": str(d.get("task", "")),
            "task_name": str(d.get("task_name", "")),
            "trace_id": str(d.get("trace_id", "")),
            "step": d.get("step"),
            "sample_index": d.get("sample_index"),
            "rollout_n": d.get("rollout_n"),
            "experiment_name": str(d.get("experiment_name", "")),
            "status": str(d.get("status", "")),
            "phase": str(d.get("phase", "")),
            "final_reward": d.get("final_reward"),
            "total_spans": d.get("total_spans"),
            "n_turns": len(d.get("turns", [])),
            "task_complexity": str((d.get("attributes") or {}).get("task_complexity", "")),
            "task_max_steps": str((d.get("attributes") or {}).get("task_max_steps", "")),
            "start_time": str(d.get("start_time", "")),
            "end_time": str(d.get("end_time", "")),
            "initial_prompt_hash": hashlib.sha256(
                str(d.get("initial_prompt", "")).encode("utf-8")).hexdigest()[:16],
            "sha256": sidecar_sha(path),
            "size": os.path.getsize(path),
        }
        if fn in need_turns:
            parsed[tid] = d
    if len(meta) != 464:
        fail("meta count %d != 464" % len(meta))
    for f in findings:
        tid = f["trajectory"].replace(".json", "")
        if tid not in meta:
            fail("finding %s trajectory not in corpus: %s" % (f["id"], f["trajectory"]))
    # sha256 cross-check: finding file hashes must match sidecars
    for f in findings:
        tid = f["trajectory"].replace(".json", "")
        if f.get("sha256") and f["sha256"] != meta[tid]["sha256"]:
            fail("finding %s sha256 != sidecar for %s" % (f["id"], tid))

    records = []

    def rec(ref, kind, body, tags):
        tags = dict(tags)
        tags["lane"] = LANE
        records.append({"ref": ref, "kind": kind, "body": body, "tags": tags})

    # ---- 1 source ----
    rec("source-android-world", "source", {
        "source_type": "huggingface",
        "locator": HF_URL,
        "title": "SeerRay-Lab/Android-World-Eval: 464 Xiaomi-GUI-0 agent rollouts "
                 "(116 AndroidWorld tasks x 4 rollouts) on Android mobile tasks",
        "platform": "huggingface",
    }, {
        "dataset": HF_DATASET,
        "revision": REVISION,
        "license": "mit",
    })

    # ---- 1 run ----
    rec("run-android-world", "run", {
        "run_kind": "review",
        "tool": "trajectory-review-fleet",
        "tool_version": "taxonomy prompts v2026-10-17; adversarial kill; verifier re-check",
        "started": OBSERVED_AT,
        "ended": OBSERVED_AT,
        "params": {
            "inputs": [HF_URL + "/resolve/" + REVISION + "/sample_<n>_rollout_<r>.json"],
            "dataset_revision": REVISION,
            "method": "reviewer A (rollouts 0-1) + reviewer B (rollouts 2-3): "
                      "keyword sweeps + action census + deep reads; adversarial "
                      "kill of weak candidates; verifier byte-check of all "
                      "surviving quotes/stats",
        },
        "coverage": {
            "complete": True,
            "scanned": 464,
            "total": 464,
            "description": "116 AndroidWorld tasks x 4 rollouts; full corpus reviewed",
        },
    }, {
        "dataset": HF_DATASET,
        "revision": REVISION,
        "reviewer_kills": str(len(kill.get("reviewer_kills", []))),
        "verifier_kills": str(len(kill.get("verifier_kills", []))),
        "verifier_corrections": str(len(kill.get("verifier_corrections", []))),
        "dedupe_decisions": str(len(kill.get("dedupe_decisions", []))),
    })

    # ---- 1 dataset.snapshot ----
    rec("snap-android-world", "observation", {
        "type": "dataset.snapshot",
        "source": "@source-android-world",
        "run": "@run-android-world",
        "observed_at": OBSERVED_AT,
        "time_basis": "collector_clock",
        "files": [],
        "data": {
            "dataset_uri": HF_URL,
            "revision": REVISION,
            "coverage": "116 tasks x 4 rollouts (full corpus)",
            "row_count": 464,
            "license": "mit",
        },
    }, {
        "dataset": HF_DATASET,
        "revision": REVISION,
    })

    # ---- artifacts + dataset.records + run->trajectory edges ----
    for tid, m in sorted(meta.items()):
        aref = "art-" + tid.replace("_", "-")
        tref = "traj-" + tid.replace("_", "-")
        rec(aref, "artifact", {
            "sha256": m["sha256"],
            "size": m["size"],
        }, {
            "filename": m["filename"],
            "raw_path": "data/lanes/android-world-trajectories/raw/" + m["filename"],
            "trajectory_id": tid,
            "sample": m["sample"],
            "rollout": m["rollout"],
            "sidecar_sha256": m["filename"] + ".sha256",
        })
        rec(tref, "observation", {
            "type": "dataset.record",
            "source": "@source-android-world",
            "run": "@run-android-world",
            "observed_at": OBSERVED_AT,
            "time_basis": "collector_clock",
            "files": [{
                "artifact": "@" + aref,
                "role": "raw-trajectory",
                "filename": m["filename"],
            }],
            "data": {
                "snapshot": "@snap-android-world",
                "locator": {"artifact": "@" + aref, "whole": True},
                "external_record_id": tid,
            },
        }, {
            "trajectory_id": tid,
            "sample": m["sample"],
            "rollout": m["rollout"],
            "task_name": m["task_name"][:200],
            "final_reward": str(m["final_reward"]),
            "status": m["status"],
            "phase": m["phase"],
            "n_turns": str(m["n_turns"]),
            "task_complexity": m["task_complexity"],
            "experiment_name": m["experiment_name"],
            "start_time": m["start_time"],
            "raw_path": "data/lanes/android-world-trajectories/raw/" + m["filename"],
        })
        rec("edge-run-" + tid.replace("_", "-"), "edge", {
            "subject": "@run-android-world",
            "predicate": "related_to",
            "object": "@" + tref,
            "basis": "OBSERVED",
            "cites": ["@" + tref],
            "note": "review run scanned trajectory " + tid,
        }, {"trajectory_id": tid})

    # ---- findings ----
    for f in findings:
        fid = f["id"]
        tid = f["trajectory"].replace(".json", "")
        category, severity, description = DESCRIPTIONS[fid]
        fref = "finding-" + fid.lower()
        tref = "traj-" + tid.replace("_", "-")
        m = meta[tid]
        rec(fref, "observation", {
            "type": "intel.behavior",
            "source": "@source-android-world",
            "run": "@run-android-world",
            "observed_at": OBSERVED_AT,
            "time_basis": "collector_clock",
            "files": [{
                "artifact": "@art-" + tid.replace("_", "-"),
                "role": "evidence-trajectory",
                "filename": m["filename"],
            }],
            "data": {
                "category": category,
                "description": "[%s] %s" % (f.get("class", ""), description),
                "evaluations_seen_on": [LANE],
                "models_affected": [MODEL_LABEL],
                "first_observed": "",
                "provenance": "android-world trajectory review fleet; "
                              "verifier-graded verified-findings.jsonl, finding " + fid,
                "severity": severity,
            },
        }, {
            "finding_id": fid,
            "class_code": str(f.get("class", "")),
            "grade": str(f.get("grade", "")),
            "confidence": str(f.get("confidence", "")),
            "verdict": str(f.get("verdict", "")),
            "merged_from": ",".join(f.get("merged_from", [])),
            "step_range": "%d-%d" % tuple(f.get("step_range", [0, 0])),
            "evidence_quote": str(f.get("quote", ""))[:2000],
            "verifier_note": str(f.get("verifier_note", ""))[:2000],
            "verifier_finding_sha": str(f.get("sha256", "")),
            "trajectory_id": tid,
            "task_name": m["task_name"][:200],
            "file_sha256": m["sha256"],
            "file_size": str(m["size"]),
            "final_reward": str(m["final_reward"]),
            "raw_path": "data/lanes/android-world-trajectories/raw/" + m["filename"],
        })
        rec("edge-finding-" + fid.lower(), "edge", {
            "subject": "@" + fref,
            "predicate": "supports",
            "object": "@" + tref,
            "basis": "OBSERVED",
            "cites": ["@" + fref],
            "note": "finding %s observed in trajectory %s steps %s" % (
                fid, tid, f.get("step_range", "")),
        }, {"trajectory_id": tid, "finding_id": fid, "class_code": str(f.get("class", ""))})

        # ---- behavior.tool_sequence where applicable (skip aggregate V-02) ----
        if fid != "V-02":
            seq = extract_tool_sequence(
                os.path.join(RAW, m["filename"]), f.get("step_range", [0, 0]))
            if not seq:
                fail("empty tool sequence for " + fid)
            rec("toolseq-" + fid.lower(), "observation", {
                "type": "behavior.tool_sequence",
                "source": "@source-android-world",
                "run": "@run-android-world",
                "observed_at": OBSERVED_AT,
                "time_basis": "collector_clock",
                "files": [],
                "data": {
                    "trajectory": "data/lanes/android-world-trajectories/raw/" + m["filename"],
                    "model": MODEL_LABEL,
                    "harness": HARNESS_LABEL,
                    "steps": seq,
                    "length": len(seq),
                    "provenance": "re-derived from raw trajectory bytes, finding "
                                  + fid + " step range " + str(f.get("step_range", "")),
                },
            }, {
                "finding_id": fid,
                "trajectory_id": tid,
                "step_range": "%d-%d" % tuple(f.get("step_range", [0, 0])),
                "class_code": str(f.get("class", "")),
            })

    bundle = {
        "bundle": 2,
        "actor": ACTOR,
        "idempotency_key": "android-world-ingest-2026-10-16-v1",
        "lane": LANE,
        "records": records,
    }
    with open(OUT_BUNDLE, "w") as fh:
        json.dump(bundle, fh)

    report = {
        "trajectories": len(meta),
        "findings": len(findings),
        "tool_sequences": 11,
        "record_count": len(records),
        "record_kinds": dict(Counter(r["kind"] for r in records)),
        "sha256_bundle": hashlib.sha256(open(OUT_BUNDLE, "rb").read()).hexdigest(),
        "revision": REVISION,
    }
    json.dump(report, open(OUT_REPORT, "w"), indent=1)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
