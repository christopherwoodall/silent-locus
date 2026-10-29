"""Assemble runs/* into a Parquet dataset + dataset card under /job/export/dataset."""
import json, os, glob, sys, collections, datetime, shutil
import pyarrow as pa, pyarrow.parquet as pq

W = os.environ.get("JOBW", "/job/work"); OUT = sys.argv[1] if len(sys.argv) > 1 else "/job/export/dataset"
os.makedirs(f"{OUT}/data", exist_ok=True)
J = lambda o: json.dumps(o, ensure_ascii=False)
def load(p, d=None):
    try: return json.load(open(p))
    except Exception: return d
def lines(p):
    out = []
    try:
        for l in open(p):
            try: out.append(json.loads(l))
            except Exception: pass
    except Exception: pass
    return out

rows = []; skipped = collections.Counter()
for d in sorted(glob.glob(f"{W}/runs/*")):
    res = load(f"{d}/result.json"); conv = load(f"{d}/conversation.json")
    if not res or not conv or not conv.get("messages") or not res.get("turns"): skipped["incomplete"] += 1; continue
    lasterr = str((res.get("segments") or [{}])[-1].get("error") or "")
    if res.get("reason") == "error" and any(x in lasterr for x in ("Unable to connect", "ECONNREFUSED", "model request failed", "socket connection", "spend cap", "fetch failed")): skipped["infrastructure_error"] += 1; continue
    task = res["task"]; judge = (load(f"{d}/judge.json") or {}).get("verdict") or {}
    turns = [t for t in lines(f"{d}/turns.jsonl")]
    good_turns = [t for t in turns if not t.get("error")]
    steps = lines(f"{d}/steps.jsonl")
    msgs = []
    for m in conv["messages"]:
        content = m.get("content")
        if isinstance(content, list): content = "".join(p.get("text", "") for p in content if isinstance(p, dict))
        msgs.append({"role": m["role"], "content": content if content is not None else "", "reasoning_content": m.get("reasoning_content") or "",
                     "tool_calls": [{"id": tc.get("id") or "", "name": tc["function"]["name"] or "", "arguments": tc["function"]["arguments"] if isinstance(tc["function"]["arguments"], str) else J(tc["function"]["arguments"])} for tc in (m.get("tool_calls") or [])],
                     "tool_call_id": m.get("tool_call_id") or ""})
    seg = res.get("segments") or [{}]
    tok = res.get("tokens") or {}
    ok = bool(res.get("ok")); reason = res.get("reason") or ""
    clean = ok and reason in ("done", "answered") and not res.get("aborted") and not res.get("length_stops")
    accepted = bool(clean and judge.get("success") is True and (judge.get("score") or 0) >= 4 and judge.get("grounded") is not False and not judge.get("fabricated"))
    n_calls = sum(len(m["tool_calls"]) for m in msgs)
    rows.append({
        "id": res["run_id"], "task_id": task["id"], "task": task["text"], "followup_task": task.get("followup") or "",
        "tier": task.get("tier") or "", "site_mode": task.get("site_mode") or "", "category": task.get("category") or "", "sites": task.get("sites") or [],
        "task_kind": task.get("kind") or "", "answer_format": task.get("answer_format") or "", "expected_steps": int(task.get("expected_steps") or 0) if str(task.get("expected_steps") or "0").lstrip("-").isdigit() else 0,
        "ask_profile": J(task.get("ask_profile")) if task.get("ask_profile") else "",
        "model": res.get("model_label") or "", "model_id": res.get("model") or "", "provider": res.get("provider") or "", "reasoning_effort": res.get("effort") or "",
        "request_params": J(res.get("body_extra") or {}), "harness": J(res.get("harness") or {}), "guardrails": J(res.get("guardrails") or {}),
        "system_prompt": msgs[0]["content"] if msgs and msgs[0]["role"] == "system" else "", "tools": J(conv.get("tools") or []),
        "messages": msgs, "transcript": J(load(f"{d}/transcript.json", [])),
        "turns": [{"turn": int(t.get("turn") or 0), "latency_ms": int(t.get("latency_ms") or 0), "finish_reason": t.get("finish_reason") or "", "served_model": t.get("served_model") or "",
                   "prompt_tokens": int((t.get("usage") or {}).get("prompt_tokens") or 0), "completion_tokens": int((t.get("usage") or {}).get("completion_tokens") or 0),
                   "reasoning_tokens": int(((t.get("usage") or {}).get("completion_tokens_details") or {}).get("reasoning_tokens") or (t.get("usage") or {}).get("reasoning_tokens") or 0),
                   "cached_tokens": int(((t.get("usage") or {}).get("prompt_tokens_details") or {}).get("cached_tokens") or 0)} for t in good_turns],
        "browser_steps": [{"step": int(s.get("step") or 0), "ok": bool(s.get("ok")), "note": s.get("note") or "", "url": s.get("url") or "", "ms": int(s.get("ms") or 0), "error": s.get("error") or ""} for s in steps if s.get("kind") == "run"],
        "ask_events": [{"question": s.get("question") or "", "options": [str(o) for o in (s.get("options") or [])], "answer": s.get("answer") or ""} for s in steps if s.get("kind") == "ask"],
        "final_answer": res.get("answer") or "", "success_reported": ok, "stop_reason": reason, "aborted": res.get("aborted") or "",
        "num_turns": len(good_turns), "num_tool_calls": n_calls, "num_browser_steps": int(res.get("browser_steps") or 0), "model_errors_retried": len(turns) - len(good_turns),
        "wall_seconds": round(sum((s.get("wall_ms") or 0) for s in seg) / 1000, 1), "final_tabs": J(res.get("final_tabs") or []),
        "prompt_tokens_total": int(tok.get("prompt") or 0), "completion_tokens_total": int(tok.get("completion") or 0), "reasoning_tokens_total": int(tok.get("reasoning") or 0),
        "max_context_tokens": int(res.get("max_prompt_tokens") or 0), "length_stops": int(res.get("length_stops") or 0), "images_omitted": int(res.get("images_omitted") or 0),
        "judge_success": bool(judge.get("success")) if judge else None, "judge_score": int(float(judge.get("score") or 0)) if judge else None, "judge_grounded": (judge.get("grounded") if isinstance(judge.get("grounded"), bool) else None) if judge else None,
        "judge_fabricated": (judge.get("fabricated") if isinstance(judge.get("fabricated"), bool) else None) if judge else None, "judge_blocked": (judge.get("blocked") if isinstance(judge.get("blocked"), bool) else None) if judge else None, "judge_efficiency": int(float(judge.get("efficiency") or 0)) if judge else None,
        "judge_failure_mode": str(judge.get("failure_mode") or "") if judge else "", "judge_rationale": str(judge.get("rationale") or "") if judge else "",
        "accepted": accepted, "finished_at": res.get("finished_at") or "",
    })

S = pa.string(); I = pa.int64(); B = pa.bool_()
SCHEMA = pa.schema([("id", S), ("task_id", S), ("task", S), ("followup_task", S), ("tier", S), ("site_mode", S), ("category", S), ("sites", pa.list_(S)),
  ("task_kind", S), ("answer_format", S), ("expected_steps", I), ("ask_profile", S), ("model", S), ("model_id", S), ("provider", S), ("reasoning_effort", S),
  ("request_params", S), ("harness", S), ("guardrails", S), ("system_prompt", S), ("tools", S),
  ("messages", pa.list_(pa.struct([("role", S), ("content", S), ("reasoning_content", S), ("tool_calls", pa.list_(pa.struct([("id", S), ("name", S), ("arguments", S)]))), ("tool_call_id", S)]))),
  ("transcript", S),
  ("turns", pa.list_(pa.struct([("turn", I), ("latency_ms", I), ("finish_reason", S), ("served_model", S), ("prompt_tokens", I), ("completion_tokens", I), ("reasoning_tokens", I), ("cached_tokens", I)]))),
  ("browser_steps", pa.list_(pa.struct([("step", I), ("ok", B), ("note", S), ("url", S), ("ms", I), ("error", S)]))),
  ("ask_events", pa.list_(pa.struct([("question", S), ("options", pa.list_(S)), ("answer", S)]))),
  ("final_answer", S), ("success_reported", B), ("stop_reason", S), ("aborted", S), ("num_turns", I), ("num_tool_calls", I), ("num_browser_steps", I), ("model_errors_retried", I),
  ("wall_seconds", pa.float64()), ("final_tabs", S), ("prompt_tokens_total", I), ("completion_tokens_total", I), ("reasoning_tokens_total", I), ("max_context_tokens", I),
  ("length_stops", I), ("images_omitted", I), ("judge_success", B), ("judge_score", I), ("judge_grounded", B), ("judge_fabricated", B), ("judge_blocked", B), ("judge_efficiency", I),
  ("judge_failure_mode", S), ("judge_rationale", S), ("accepted", B), ("finished_at", S)])

def write(name, subset, shard=400):
    os.makedirs(f"{OUT}/data/{name}", exist_ok=True)
    n = max(1, -(-len(subset) // shard))
    for i in range(n):
        part = subset[i * shard:(i + 1) * shard]
        if not part: continue
        t = pa.Table.from_pylist(part, schema=SCHEMA)
        pq.write_table(t, f"{OUT}/data/{name}/train-{i:05d}-of-{n:05d}.parquet", compression="zstd")
for d in glob.glob(f"{OUT}/data/*"): shutil.rmtree(d)
write("accepted", [r for r in rows if r["accepted"]])  # published config: accepted only (user decision 2026-09-22)

# ---- stats + card ----
def table(keyf, title):
    c = collections.defaultdict(lambda: [0, 0, 0, 0])
    for r in rows:
        k = keyf(r); c[k][0] += 1; c[k][1] += r["accepted"]; c[k][2] += r["num_turns"]; c[k][3] += r["max_context_tokens"]
    out = [f"| {title} | traces | accepted | mean turns | mean max context (tok) |", "|---|---:|---:|---:|---:|"]
    for k in sorted(c): n, a, t, m = c[k]; out.append(f"| {k} | {n} | {a} | {t / n:.1f} | {m / n:,.0f} |")
    return "\n".join(out)
stats = {"traces": len(rows), "accepted": sum(r["accepted"] for r in rows), "unique_tasks": len({r["task_id"] for r in rows}), "turns": sum(r["num_turns"] for r in rows),
         "tool_calls": sum(r["num_tool_calls"] for r in rows), "completion_tokens": sum(r["completion_tokens_total"] for r in rows), "reasoning_tokens": sum(r["reasoning_tokens_total"] for r in rows),
         "max_context_tokens": max([r["max_context_tokens"] for r in rows] or [0]), "length_stops": sum(r["length_stops"] for r in rows), "skipped": dict(skipped), "built": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
json.dump(stats, open(f"{OUT}/stats.json", "w"), indent=1)
card = open(f"{W}/CARD.md").read()
card = card.replace("{{STATS}}", "\n".join(f"- **{k.replace('_', ' ')}**: {v:,}" if isinstance(v, int) else f"- **{k.replace('_', ' ')}**: {v}" for k, v in stats.items() if k not in ("skipped",)))
card = card.replace("{{BY_MODEL}}", table(lambda r: f"{r['model']} / {r['reasoning_effort']}", "model / effort")).replace("{{BY_TIER}}", table(lambda r: r["tier"], "tier")).replace("{{BY_MODE}}", table(lambda r: r["site_mode"], "site mode"))
open(f"{OUT}/README.md", "w").write(card)
os.makedirs(f"{OUT}/pipeline", exist_ok=True)
for f in ["gen-task.mjs", "dispatcher.mjs", "make_tasks.py", "judge.py", "build_dataset.py", "run.sh", "sglang-loop.sh", "dispatch-loop.sh", "bench_load.py"]:
    if os.path.exists(f"{W}/{f}"): shutil.copy(f"{W}/{f}", f"{OUT}/pipeline/{f}")
shutil.copy(f"{W}/tasks/pool.jsonl", f"{OUT}/pipeline/task_pool.jsonl")
shutil.copy(f"{W}/control/sglang_args.txt", f"{OUT}/pipeline/sglang_args.txt")
print(json.dumps(stats))
