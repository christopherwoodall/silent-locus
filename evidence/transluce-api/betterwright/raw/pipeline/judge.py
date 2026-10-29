"""Judge one finished run with the local Qwen server. Writes judge.json next to result.json."""
import json, sys, os, re, urllib.request
d = sys.argv[1]
out = os.path.join(d, "judge.json")
if os.path.exists(out): sys.exit(0)
res = json.load(open(os.path.join(d, "result.json")))
conv = json.load(open(os.path.join(d, "conversation.json")))
msgs = conv.get("messages") or []
def clip(s, n): s = str(s or ""); return s if len(s) <= n else s[: n // 2] + f"\n...[{len(s) - n} chars clipped]...\n" + s[-n // 2 :]
lines = []; step = 0
for m in msgs[1:]:
    if m["role"] == "user": lines.append("USER: " + clip(m["content"], 3000))
    elif m["role"] == "assistant":
        step += 1
        if m.get("content"): lines.append(f"[{step}] AGENT SAYS: " + clip(m["content"], 1200))
        for tc in m.get("tool_calls") or []:
            lines.append(f"[{step}] CALL {tc['function']['name']}: " + clip(tc["function"]["arguments"], 1500))
    elif m["role"] == "tool": lines.append("RESULT: " + clip(m["content"], 1400))
traj = "\n".join(lines)
if len(traj) > 150000: traj = traj[:50000] + "\n...[middle of trajectory clipped]...\n" + traj[-100000:]
task = res["task"]
prompt = f"""You are a strict evaluator of a web-browsing agent. Decide from the evidence in the trajectory whether the agent really completed the user's task on the live web.

TASK:
{task['text']}
{('FOLLOW-UP REQUEST: ' + task['followup']) if task.get('followup') else ''}

AGENT FINAL ANSWER (stop reason: {res.get('reason')}):
{clip(res.get('answer'), 6000)}

TRAJECTORY (tool calls and clipped tool results):
{traj}

Rules: every fact in the final answer must be supported by tool results in the trajectory (grounded), not by prior knowledge. Required filters/constraints must have visibly taken effect. If the site blocked the agent or the task was impossible, an honest, specific report of that is a partial success (score 3), while a fabricated answer is a failure (score 1). Wasteful-but-correct runs still succeed.

Reply with ONLY a JSON object: {{"success": true|false, "score": 1-5, "grounded": true|false, "fabricated": true|false, "blocked": true|false, "efficiency": 1-5, "failure_mode": "none|blocked|wrong_answer|incomplete|fabricated|loop|timeout|tool_misuse|other", "rationale": "<=60 words"}}"""
backend = {"name": "qwen", "endpoint": "http://127.0.0.1:30010/v1", "model": "qwen3.8-flash-next", "label": "Qwen3.8-Flash-Next (local NVFP4, low effort)",
           "extra": {"chat_template_kwargs": {"enable_thinking": True, "reasoning_effort": "low"}}}
try: backend = json.load(open(os.environ.get("JOBW", "/job/work") + "/control/judge_backend.json"))
except Exception: pass
body = {"model": backend["model"], "messages": [{"role": "user", "content": prompt}], "max_tokens": 6000, "temperature": 0.3, **backend.get("extra", {})}
headers = {"content-type": "application/json"}
if backend.get("api_key_file"): headers["authorization"] = "Bearer " + open(backend["api_key_file"].replace("/job/work", os.environ.get("JOBW", "/job/work"))).read().strip()
verdict = None; err = None; cost = 0.0
for attempt in range(4):
    try:
        req = urllib.request.Request(backend["endpoint"].rstrip("/") + "/chat/completions", data=json.dumps(body).encode(), headers=headers)
        data = json.load(urllib.request.urlopen(req, timeout=1500))
        u = data.get("usage") or {}
        if backend.get("price_in"): cost = u.get("estimated_cost") if isinstance(u.get("estimated_cost"), (int, float)) else ((u.get("prompt_tokens") or 0) * backend["price_in"] + (u.get("completion_tokens") or 0) * backend["price_out"]) / 1e6
        text = data["choices"][0]["message"].get("content") or ""
        m = re.search(r"\{.*\}", text, re.S)
        verdict = json.loads(m.group(0)); break
    except Exception as e:
        err = repr(e)[:300]; import time; time.sleep(5 * (attempt + 1))
if cost: open(os.environ.get("JOBW", "/job/work") + "/state/spend.jsonl", "a").write(json.dumps({"t": int(__import__("time").time() * 1000), "id": "judge:" + os.path.basename(d), "usd": cost}) + "\n")
json.dump({"judge_model": backend["label"], "verdict": verdict, "error": None if verdict else err, "cost_usd": cost}, open(out, "w"))
