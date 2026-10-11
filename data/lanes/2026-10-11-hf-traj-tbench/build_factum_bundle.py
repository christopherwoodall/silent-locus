#!/usr/bin/env python3
"""Build Factum bundles from the yoonholee terminalbench trajectory extracts.

Lane: 2026-10-11-hf-traj-tbench
Inputs (.work/): matrix.json, jina_instances.jsonl, commands_per_model.json,
                 urls.json
Outputs (.work/bundles/): bundle-00.json .. bundle-NN.json, each submittable
                 via `factum add --input`.

Records:
  - 1 source (per bundle, bundle-local) + 1 run (first bundle only)
  - intel.behavior / harness-assignment : one per (model, agent) pair (109)
  - intel.behavior / fetch-proxy-abuse  : one per r.jina.ai trajectory row (20)
  - intel.behavior / shell-command-profile : one per model (49)
  - infra.ioc / other                   : one per distinct URL seen >= 5x (~500)

No edges during ingest. Every record carries tags.lane.
"""
import json
import os
import re

import pyarrow.parquet as pq

LANE = "2026-10-11-hf-traj-tbench"
WORK = os.path.expanduser(
    f"~/workspace/silent-locus/data/lanes/{LANE}/.work")
BUNDLES = os.path.join(WORK, "bundles")
os.makedirs(BUNDLES, exist_ok=True)
ACTOR = f"agent:lane-ingest-{LANE}"
RETRIEVED_AT = "2026-10-07T23:55:16Z"  # dataset acquisition, source PROVENANCE.md
DATASET = "yoonholee-terminalbench-trajectories"
RAW_LOC = ("evidence/hf-trajectories/raw/yoonholee-terminalbench-trajectories/"
           "data/")
URL_MIN_COUNT = 5
CHUNK = 150

BASE_TAGS = {
    "lane": LANE,
    "grade": "OBSERVED",
    "source_dataset": DATASET,
}

SCHEMAS = {
    "intel.behavior": "urn:factum:intel:behavior:1",
    "infra.ioc": "urn:factum:infra:ioc:1",
}


def src_record():
    return {
        "ref": "src-dataset", "kind": "source",
        "body": {
            "source_type": "submitted",
            "locator": RAW_LOC,
            "title": ("yoonholee/terminalbench-trajectories: "
                      "train-00000-of-00002.parquet + "
                      "train-00001-of-00002.parquet "
                      "(52,104 Terminal-Bench trial rows; "
                      "trajectory steps present only in 00001)"),
        },
        "tags": dict(BASE_TAGS, retrieved_via=(
            "curl from huggingface.co, " + RETRIEVED_AT)),
    }


def run_record(n_obs):
    return {
        "ref": "run-extract", "kind": "run",
        "body": {
            "run_kind": "extraction",
            "tool": "build_factum_bundle.py",
            "tool_version": "1",
            "params": {
                "lane": LANE,
                "inputs": ["matrix.json", "jina_instances.jsonl",
                           "commands_per_model.json", "urls.json"],
                "observations": n_obs,
            },
            "coverage": {
                "complete": True,
                "total": 52104,
                "scanned": 52104,
                "description": (
                    "52,104 rows across both parquet files. "
                    "Matrix from both files; jina/commands/URLs from "
                    "train-00001 steps (17,030 rows with steps; "
                    "train-00000 steps are all the literal string "
                    "'null' in this copy)."),
            },
        },
        "tags": dict(BASE_TAGS),
    }


def obs(ref, ftype, data, observed_at, time_basis, tags):
    return {
        "ref": ref, "kind": "observation",
        "body": {
            "type": ftype,
            "data_schema": SCHEMAS[ftype],
            "data": data,
            "observed_at": observed_at,
            "time_basis": time_basis,
            "source": "@src-dataset",
            "files": [],
        },
        "tags": tags,
    }


def pair_earliest_started():
    """Earliest started_at per (model, agent) and per model (both files)."""
    pair_min, model_min = {}, {}
    for fn in ("train-00000-of-00002.parquet",
               "train-00001-of-00002.parquet"):
        pf = pq.ParquetFile(os.path.join(
            os.path.expanduser("~/workspace/silent-locus"), RAW_LOC, fn))
        for batch in pf.iter_batches(
                columns=["model", "agent", "started_at"], batch_size=100000):
            df = batch.to_pandas()
            for m, a, s in zip(df["model"], df["agent"], df["started_at"]):
                if not s:
                    continue
                s = str(s)
                k = (str(m), str(a))
                if k not in pair_min or s < pair_min[k]:
                    pair_min[k] = s
                mk = str(m)
                if mk not in model_min or s < model_min[mk]:
                    model_min[mk] = s
    return pair_min, model_min


URL_ARTIFACT = re.compile(r"[\\\s]")


def main():
    matrix = json.load(open(os.path.join(WORK, "matrix.json")))
    jina_rows = [json.loads(l)
                 for l in open(os.path.join(WORK, "jina_instances.jsonl"))]
    cmds = json.load(open(os.path.join(WORK, "commands_per_model.json")))
    urls = json.load(open(os.path.join(WORK, "urls.json")))

    pair_min, model_min = pair_earliest_started()

    obss = []

    # ---- 1. model x harness matrix ----
    for i, p in enumerate(matrix):
        m, a, n = p["model"], p["agent"], p["trajectories"]
        ts = pair_min.get((m, a))
        if ts:
            oat, tb, first = ts, "source_metadata", ts[:10]
        else:
            oat, tb, first = RETRIEVED_AT, "unknown", "unknown (no source timestamps)"
        obss.append(obs(
            f"mx-{i:03d}", "intel.behavior",
            {"category": "harness-assignment",
             "description": (
                 f"{m} ran {n} Terminal-Bench trajectories on the {a} "
                 f"scaffold (dataset {DATASET})."),
             "evaluations_seen_on": ["terminal-bench"],
             "models_affected": [m],
             "first_observed": first,
             "provenance": (
                 f"{DATASET}: {n} trial rows for model x harness pair"),
             "severity": "minimal"},
            oat, tb,
            dict(BASE_TAGS, model=m, harness=a)))

    # ---- 2. r.jina.ai proxy instances ----
    for i, r in enumerate(jina_rows):
        m, a = r["model"], r["agent"]
        reason_texts = []
        proxy_cmds = []
        seen_cmds = set()
        for s in r["steps_with_jina"]:
            st = s["step"]
            msg = str(st.get("msg") or "")
            if "r.jina.ai" in msg.lower():
                reason_texts.append(
                    f"[step {s['step_index']} src={s['src']}] {msg}")
            tools = st.get("tools")
            if isinstance(tools, list):
                for t in tools:
                    if not isinstance(t, dict):
                        continue
                    cmd = t.get("cmd")
                    if isinstance(cmd, list):
                        cmd = " ".join(str(x) for x in cmd)
                    if cmd and "r.jina.ai" in str(cmd).lower() \
                            and cmd not in seen_cmds:
                        seen_cmds.add(cmd)
                        proxy_cmds.append(str(cmd))
        desc = (
            f"Model {m} on the {a} scaffold used the r.jina.ai reader "
            f"proxy to fetch pages it could not reach directly "
            f"(Terminal-Bench task '{r['task_name']}'). "
            f"{len(proxy_cmds)} distinct proxy fetch commands, "
            f"{r['occurrences']} jina mentions in the trajectory.\n"
            "Agent reasoning and proxy commands (verbatim):\n"
            + "\n".join(reason_texts[:12])
            + ("\nProxy commands:\n" + "\n".join(proxy_cmds)
               if proxy_cmds else ""))
        obss.append(obs(
            f"jina-{i:02d}", "intel.behavior",
            {"category": "fetch-proxy-abuse",
             "description": desc,
             "evaluations_seen_on": ["terminal-bench"],
             "models_affected": [m],
             "first_observed": "2025-11 (eval window; source rows carry no timestamps)",
             "provenance": (
                 f"{DATASET} train-00001, task {r['task_name']}; "
                 f"21 explicit-bypass THOUGHT messages across the 20 rows; "
                 f"byte counts: 20 rows / 362 r.jina.ai occurrences "
                 f"(prior audit reported 37/638 - not reproduced from this copy)"),
             "severity": "low"},
            RETRIEVED_AT, "unknown",
            dict(BASE_TAGS, model=m, harness=a,
                 task=r["task_name"])))

    # ---- 3. per-model command profiles ----
    for i, m in enumerate(sorted(cmds)):
        hist = cmds[m]
        ts = model_min.get(m)
        if ts:
            oat, tb, first = ts, "source_metadata", ts[:10]
        else:
            oat, tb, first = RETRIEVED_AT, "unknown", "unknown (no source timestamps)"
        lines = [f"{h['count']:6d}  {h['command']}" for h in hist]
        obss.append(obs(
            f"cmd-{i:02d}", "intel.behavior",
            {"category": "shell-command-profile",
             "description": (
                 f"Top shell commands issued by {m} in Terminal-Bench "
                 f"trajectories (from assistant/agent bash blocks and "
                 f"structured tools[].cmd calls; first line per block). "
                 f"count = occurrences:\n" + "\n".join(lines)),
             "evaluations_seen_on": ["terminal-bench"],
             "models_affected": [m],
             "first_observed": first,
             "provenance": (
                 f"{DATASET} train-00001 steps; "
                 f"{len(hist)} top commands shown"),
             "severity": "minimal"},
            oat, tb,
            dict(BASE_TAGS, model=m)))

    # ---- 4. URL IOCs ----
    n_url = 0
    for u in urls:
        term = u["url"]
        if URL_ARTIFACT.search(term) or len(term) > 500:
            continue
        if u["count"] < URL_MIN_COUNT:
            continue
        n_url += 1
        obss.append(obs(
            f"url-{n_url:04d}", "infra.ioc",
            {"term": term, "category": "other", "status": "candidate",
             "provenance": (
                 f"{DATASET} trajectory steps; observed in "
                 f"{u['count']} trajectories by {len(u['models'])} model(s)")},
            RETRIEVED_AT, "unknown",
            dict(BASE_TAGS, fetch_count=str(u["count"]),
                 models=",".join(sorted(u["models"])[:8]))))

    # ---- chunk into bundles ----
    chunks = [obss[i:i + CHUNK] for i in range(0, len(obss), CHUNK)]
    for ci, chunk in enumerate(chunks):
        records = [src_record()]
        if ci == 0:
            records.append(run_record(len(obss)))
        records.extend(chunk)
        bundle = {
            "bundle": 2,
            "actor": ACTOR,
            "idempotency_key": f"lane-ingest-{LANE}-chunk{ci:02d}-v1",
            "records": records,
        }
        # within-bundle ref uniqueness + in-bundle dedup of URL terms
        refs = [r["ref"] for r in records]
        assert len(refs) == len(set(refs)), "dup refs"
        path = os.path.join(BUNDLES, f"bundle-{ci:02d}.json")
        with open(path, "w") as f:
            json.dump(bundle, f, ensure_ascii=False, indent=1)
        print(f"wrote {path}: {len(records)} records")

    print(f"TOTAL observations: {len(obss)} "
          f"({len(matrix)} matrix, {len(jina_rows)} jina, "
          f"{len(cmds)} cmd-profiles, {n_url} urls) "
          f"in {len(chunks)} bundles")


if __name__ == "__main__":
    main()
