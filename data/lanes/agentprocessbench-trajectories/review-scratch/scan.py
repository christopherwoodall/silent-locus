#!/usr/bin/env python3
"""Stage-2 candidate scanner for AgentProcessBench review (Reviewer B split).
Scans gaia_dev + tau2 test.jsonl for taxonomy keyword hits; Reviewer B
then reads the bytes of each candidate before filing or killing."""
import json, re, sys, os

RAW = os.path.expanduser("~/workspace/silent-locus/data/lanes/agentprocessbench-trajectories/raw")
OUT = os.path.expanduser("~/workspace/silent-locus/data/lanes/agentprocessbench-trajectories/review-scratch/candidates.jsonl")

PATTERNS = {
    "CAPTCHA": r"captcha|recaptcha|hcaptcha|bot.?check|are you (a )?human|cloudflare challenge|arcaptcha",
    "ACCOUNT": r"sign.?up|register|create (an )?account|new account|sign.?in credentials|request access",
    "GUARDRAIL": r"permission denied|not (allowed|authorized|permitted)|policy violation|refuse|guardrail|access denied|blocked by|403",
    "PROMPT-INJECT": r"ignore (all |the |previous |prior |above )?(instructions|prompt)|disregard (all |the )?(previous |prior )?(instructions|prompt)|jailbreak|DAN mode|system prompt|override your|new instructions:|### instruction|do not follow",
    "CREDENTIAL": r"api[_-]?key|secret|password|passwd|token|bearer|private key|\.pem|credentials|auth|session id|cookie",
    "IRREVERSIBLE": r"\brm\b|rm -rf|delete|drop table|truncate|overwrite|send email|publish|purchase|buy now|checkout|git push|force.?push|sudo",
    "COORDINATION": r"another agent|other agent|multi.?agent|delegat|handoff|hand.?off|sub.?agent|swarm|shared (state|memory|file|workspace)|coordinate|teammate|colleague",
    "RECOVERY": r"retry|retrying|fallback|alternative|try again|give up|unable to|failed,? (trying|try)|workaround|escalat",
    "TOOL-MISUSE": r"wrong tool|unexpected argument|invalid (argument|parameter|tool)|type ?error|missing (argument|parameter|required)",
}

def msg_text(m):
    parts = []
    for k in ("content", "text"):
        v = m.get(k)
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, list):
            for b in v:
                if isinstance(b, dict) and b.get("type") == "text":
                    parts.append(b.get("text", ""))
    # tool calls
    tc = m.get("tool_calls") or []
    for t in tc:
        fn = t.get("function", {}) if isinstance(t, dict) else {}
        parts.append("TOOLCALL:" + fn.get("name", "") + ":" + json.dumps(fn.get("arguments", ""))[:400])
    # function role content
    if m.get("role") in ("tool", "function"):
        parts.append(str(m.get("content", ""))[:2000])
    return "\n".join(parts)

def scan():
    hits = []
    with open(OUT, "w") as out:
        for fname in ("gaia_dev/test.jsonl", "tau2/test.jsonl"):
            for line in open(os.path.join(RAW, fname)):
                r = json.loads(line)
                ti = r["total_index"]
                for i, m in enumerate(r["messages"]):
                    t = msg_text(m).lower()
                    for cls, pat in PATTERNS.items():
                        mm = re.findall(pat, t)
                        if mm:
                            snippet = re.search(pat, t)
                            ctx = t[max(0, snippet.start()-80):snippet.end()+120].replace("\n", " ")[:220]
                            hits.append({"file": fname, "total_index": ti, "class_hint": cls,
                                         "step": i, "role": m.get("role"), "ctx": ctx})
                            out.write(json.dumps(hits[-1]) + "\n")
    print("hits:", len(hits))
    by = {}
    for h in hits:
        by.setdefault((h["file"], h["total_index"]), []).append(h)
    print("trajectories with hits:", len(by))

scan()
