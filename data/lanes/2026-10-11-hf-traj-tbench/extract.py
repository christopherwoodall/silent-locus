#!/usr/bin/env python3
"""Extract behavioral indicators from yoonholee terminalbench trajectories.

Lane: 2026-10-11-hf-traj-tbench
Stages:
  1. model x agent matrix (column reads, both files)
  2. r.jina.ai instances with model reasoning (file 00001 steps)
  3. shell command frequency per model (file 00001 steps)
  4. URL inventory (file 00001 steps)
Progress is checkpointed to .work/progress.json so the run is resumable.
"""
import json, os, re, sys
from collections import Counter, defaultdict

import pyarrow.parquet as pq

LANE_DIR = os.path.expanduser(
    "~/workspace/silent-locus/data/lanes/2026-10-11-hf-traj-tbench")
WORK = os.path.join(LANE_DIR, ".work")
os.makedirs(WORK, exist_ok=True)
RAW_DIR = os.path.expanduser(
    "~/workspace/silent-locus/evidence/hf-trajectories/raw/"
    "yoonholee-terminalbench-trajectories/data")
F0 = os.path.join(RAW_DIR, "train-00000-of-00002.parquet")
F1 = os.path.join(RAW_DIR, "train-00001-of-00002.parquet")

PROG = os.path.join(WORK, "progress.json")

def load_prog():
    if os.path.exists(PROG):
        with open(PROG) as f:
            return json.load(f)
    return {}

def save_prog(p):
    tmp = PROG + ".tmp"
    with open(tmp, "w") as f:
        json.dump(p, f, indent=1)
    os.replace(tmp, PROG)

URL_RE = re.compile(r'https?://[^\s<>"\'\])}\]]+')
BASH_BLOCK_RE = re.compile(r'```(?:bash|sh|shell|console)?[ \t]*\n(.*?)```',
                            re.DOTALL | re.IGNORECASE)
BYPASS_WORDS = ("bypass", "blocked", "403", "401", "access denied",
                "access issue", "unauthorized", "forbidden", "denied",
                "without authentication", "paywall", "rate limit")

prog = load_prog()
log = prog.setdefault("log", [])

def note(msg):
    print(msg, flush=True)
    log.append(msg)
    save_prog(prog)

# ---------------- Stage 1: model x agent matrix ----------------
if "matrix" not in prog:
    matrix = Counter()
    for path in (F0, F1):
        pf = pq.ParquetFile(path)
        for batch in pf.iter_batches(columns=["model", "agent"],
                                     batch_size=100000):
            df = batch.to_pandas()
            for m, a in zip(df["model"], df["agent"]):
                matrix[(str(m), str(a))] += 1
    matrix_out = [{"model": m, "agent": a, "trajectories": c}
                  for (m, a), c in sorted(matrix.items(),
                                          key=lambda kv: -kv[1])]
    with open(os.path.join(WORK, "matrix.json"), "w") as f:
        json.dump(matrix_out, f, indent=1)
    prog["matrix"] = {"distinct_pairs": len(matrix_out),
                      "total_rows": sum(matrix.values())}
    note(f"matrix: {len(matrix_out)} pairs, {sum(matrix.values())} rows")
else:
    matrix_out = json.load(open(os.path.join(WORK, "matrix.json")))
    note(f"matrix: resumed ({prog['matrix']})")

# ---------------- Stage 2-4: steps scan (file 00001) ----------------
if "steps_scan" not in prog or prog.get("steps_scan") is None:
    pf = pq.ParquetFile(F1)
    jina_rows = []
    cmd_total = Counter()
    cmd_by_model = defaultdict(Counter)
    url_total = Counter()
    url_models = defaultdict(set)
    rows_with_steps = 0
    rows_scanned = 0
    n_batches = pf.num_row_groups
    for rg in range(n_batches):
        tbl = pf.read_row_group(rg, columns=[
            "model", "agent", "task_name", "trial_id", "started_at", "steps"])
        for row in tbl.to_pylist():
            rows_scanned += 1
            steps_s = row.get("steps")
            if not steps_s or steps_s == "null":
                continue
            try:
                steps = json.loads(steps_s)
            except Exception:
                continue
            if not isinstance(steps, list):
                continue
            rows_with_steps += 1
            model = str(row.get("model") or "")
            agent = str(row.get("agent") or "")
            msgs = []          # (src, msg, obs)
            steps_ser = []     # (src, serialized step text)
            for s in steps:
                if isinstance(s, dict):
                    src = str(s.get("src") or "")
                    msg = str(s.get("msg") or "")
                    obs = str(s.get("obs") or "")
                    msgs.append((src, msg, obs))
                    steps_ser.append((src, json.dumps(
                        s, ensure_ascii=False)))
            full = "\n".join(t for _, t in steps_ser)
            full_low = full.lower()

            # --- jina instances ---
            if "r.jina.ai" in full_low or "jina.ai/reader" in full_low:
                hits = []
                for i, (src, ser) in enumerate(steps_ser):
                    if "jina" in ser.lower():
                        bypass = [w for w in BYPASS_WORDS
                                  if w in ser.lower()]
                        hits.append({"step_index": i, "src": src,
                                     "bypass_words": bypass,
                                     "step": steps[i]})
                jina_rows.append({
                    "model": model, "agent": agent,
                    "task_name": str(row.get("task_name") or ""),
                    "trial_id": str(row.get("trial_id") or ""),
                    "started_at": str(row.get("started_at") or ""),
                    "occurrences": full_low.count("jina"),
                    "steps_with_jina": hits,
                })

            # --- commands: bash code blocks in agent msg + structured
            #     tools[].cmd shell calls ---
            for src, msg, _ in msgs:
                if not msg or src not in ("assistant", "agent"):
                    continue
                for blk in BASH_BLOCK_RE.findall(msg):
                    for line in blk.split("\n"):
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        line = re.sub(r'^[$>]\s*', '', line)
                        if not line or len(line) > 300:
                            continue
                        cmd_total[line] += 1
                        cmd_by_model[line][model] += 1
            for s in steps:
                if not isinstance(s, dict):
                    continue
                tools = s.get("tools")
                if not isinstance(tools, list):
                    continue
                for t in tools:
                    if not isinstance(t, dict):
                        continue
                    cmd = t.get("cmd")
                    if isinstance(cmd, list):
                        cmd = " ".join(str(x) for x in cmd)
                    if not cmd or not isinstance(cmd, str):
                        continue
                    cmd = cmd.strip()
                    if not cmd or len(cmd) > 300:
                        continue
                    cmd_total[cmd] += 1
                    cmd_by_model[cmd][model] += 1

            # --- urls (from DECODED step text, not raw JSON, so JSON
            #     escapes cannot glue trailing text onto the URL).
            #     Deduped per ROW: one trajectory = one sighting. ---
            def _walk(x, out):
                if isinstance(x, str):
                    out.append(x)
                elif isinstance(x, list):
                    for y in x:
                        _walk(y, out)
                elif isinstance(x, dict):
                    for y in x.values():
                        _walk(y, out)

            row_texts = []
            for s in steps:
                if isinstance(s, dict):
                    _walk([s.get("msg"), s.get("obs"), s.get("tools")],
                          row_texts)
            clean = "\n".join(t for t in row_texts if t)
            # rstrip BEFORE the set: "URL" and "URL," in one row = 1 sighting
            for u in {w.rstrip(".,;:!?") for w in URL_RE.findall(clean)}:
                if not u:
                    continue
                url_total[u] += 1
                url_models[u].add(model)

        if rg % 5 == 0 or rg == n_batches - 1:
            save_prog({"log": log, "steps_scan_partial": {
                "row_group": rg + 1, "of": n_batches,
                "jina_rows": len(jina_rows),
                "distinct_commands": len(cmd_total),
                "distinct_urls": len(url_total)}})
            print(f"rg {rg+1}/{n_batches} jina={len(jina_rows)} "
                  f"cmds={len(cmd_total)} urls={len(url_total)}", flush=True)

    with open(os.path.join(WORK, "jina_instances.jsonl"), "w") as f:
        for r in jina_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    cmd_out = [{"command": c, "count": n,
                "per_model": dict(cmd_by_model[c])}
               for c, n in cmd_total.most_common()]
    with open(os.path.join(WORK, "commands.json"), "w") as f:
        json.dump(cmd_out, f, indent=1, ensure_ascii=False)

    # per-model top commands
    model_cmds = defaultdict(list)
    for c, n in cmd_total.most_common():
        for m, k in cmd_by_model[c].most_common(5):
            model_cmds[m].append({"command": c, "count": k})
    with open(os.path.join(WORK, "commands_per_model.json"), "w") as f:
        json.dump({m: v[:60] for m, v in model_cmds.items()}, f,
                  indent=1, ensure_ascii=False)

    url_out = [{"url": u, "count": n, "models": sorted(url_models[u])}
               for u, n in url_total.most_common()]
    with open(os.path.join(WORK, "urls.json"), "w") as f:
        json.dump(url_out, f, indent=1, ensure_ascii=False)

    prog["steps_scan"] = {
        "rows_scanned": rows_scanned,
        "rows_with_steps": rows_with_steps,
        "jina_rows": len(jina_rows),
        "jina_occurrences": sum(r["occurrences"] for r in jina_rows),
        "distinct_commands": len(cmd_total),
        "distinct_urls": len(url_total),
    }
    note(f"steps scan done: {json.dumps(prog['steps_scan'])}")
else:
    note(f"steps scan: resumed ({prog['steps_scan']})")

note("EXTRACTION COMPLETE")
