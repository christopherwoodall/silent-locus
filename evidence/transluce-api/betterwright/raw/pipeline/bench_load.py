"""Agent-shaped load test: C concurrent multi-turn sessions against an OpenAI-compatible server.
Each session = unique ~PROMPT_TOK-token context, then TURNS turns that each append ~1.5k tokens of
"tool output" and ask for ~OUT tokens. Reports aggregate completion tok/s over wall time."""
import json, sys, time, random, threading, urllib.request
url, model, C, TURNS, PROMPT_WORDS, OUT = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
extra = json.loads(sys.argv[7]) if len(sys.argv) > 7 else {}
WORDS = "page link button table row price search filter result item article title author date list menu form input select option review rating cart login account settings".split()
def blob(rnd, n): return " ".join(rnd.choice(WORDS) + str(rnd.randint(0, 9999)) for _ in range(n))
stats = {"comp": 0, "prompt": 0, "cached": 0, "reqs": 0, "errs": 0}; lock = threading.Lock(); lat = []
def session(i):
    rnd = random.Random(1000 + i + int(time.time()))
    msgs = [{"role": "system", "content": "You are a browser agent analysing page dumps. Think, then answer in detail."},
            {"role": "user", "content": "Page dump:\n" + blob(rnd, PROMPT_WORDS) + "\n\nDescribe in detail a plan with at least 12 numbered steps for extracting every price from this page, and explain each step thoroughly."}]
    for t in range(TURNS):
        body = {"model": model, "messages": msgs, "max_tokens": OUT, **extra}
        req = urllib.request.Request(url + "/v1/chat/completions", data=json.dumps(body).encode(), headers={"content-type": "application/json"})
        t0 = time.time()
        try:
            d = json.load(urllib.request.urlopen(req, timeout=1800))
        except Exception as e:
            with lock: stats["errs"] += 1
            print("ERR", i, t, repr(e)[:200], flush=True); return
        u = d.get("usage", {}); m = d["choices"][0]["message"]
        with lock:
            stats["comp"] += u.get("completion_tokens", 0); stats["prompt"] += u.get("prompt_tokens", 0)
            stats["cached"] += (u.get("prompt_tokens_details") or {}).get("cached_tokens", 0) or 0
            stats["reqs"] += 1; lat.append(time.time() - t0)
        msgs.append({"role": "assistant", "content": (m.get("content") or "ok")[:4000]})
        msgs.append({"role": "user", "content": "Tool output:\n" + blob(rnd, 500) + "\n\nContinue: refine the plan given this new output, in detail."})
t0 = time.time(); th = [threading.Thread(target=session, args=(i,)) for i in range(C)]
[x.start() for x in th]; [x.join() for x in th]; wall = time.time() - t0
lat.sort()
print(json.dumps({"C": C, "turns": TURNS, "wall_s": round(wall, 1), **stats, "agg_completion_tok_s": round(stats["comp"] / wall, 1),
                  "agg_total_tok_s": round((stats["comp"] + stats["prompt"] - stats["cached"]) / wall, 1), "p50_lat": round(lat[len(lat)//2], 1) if lat else None}))
