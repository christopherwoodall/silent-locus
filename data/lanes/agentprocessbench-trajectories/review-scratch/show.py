#!/usr/bin/env python3
"""Pretty-print a trajectory slice for manual review."""
import json, os, sys

RAW = os.path.expanduser("~/workspace/silent-locus/data/lanes/agentprocessbench-trajectories/raw")
FNAME, TI = sys.argv[1], int(sys.argv[2])
LO = int(sys.argv[3]) if len(sys.argv) > 3 else 0
HI = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9

def msg_text(m):
    c = m.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return " ".join(b.get("text", "") for b in c if isinstance(b, dict))
    return str(c)[:50]

for line in open(os.path.join(RAW, FNAME)):
    r = json.loads(line)
    if r["total_index"] != TI:
        continue
    print("Q:", r["question"][:250].replace("\n", " "))
    print("TOOLS:", [t.get("function", {}).get("name", "?") for t in r["tools"]])
    print("final_label:", r["final_label"], "step_labels:", r.get("step_labels"))
    for i, m in enumerate(r["messages"]):
        if i < LO or i > HI:
            continue
        t = msg_text(m)
        tc = m.get("tool_calls") or []
        call = ""
        if tc:
            parts = []
            for x in tc:
                fn = x.get("function", {})
                parts.append(f"[CALL {fn.get('name')} {json.dumps(fn.get('arguments',''))[:500]}]")
            call = " " + " ".join(parts)
        print(f"\n--- [{i}] {m.get('role')}\n{t[:1800]}{call}")
    break
