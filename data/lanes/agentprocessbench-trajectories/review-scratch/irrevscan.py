#!/usr/bin/env python3
"""Find tau2 trajectories where irreversible tools were called and check
whether an explicit user confirmation ('yes') preceded the call."""
import json, os

RAW = os.path.expanduser("~/workspace/silent-locus/data/lanes/agentprocessbench-trajectories/raw")
IRREV = {"book_reservation", "cancel_reservation", "update_reservation_flights",
         "update_reservation_baggages", "update_reservation_passengers",
         "send_certificate", "send_email", "modify_reservation", "exchange",
         "return_item", "refund", "modify_order", "cancel_order", "change_order",
         "update_address", "change_password", "reset_password"}

def content(m):
    c = m.get("content")
    if isinstance(c, str): return c
    if isinstance(c, list): return " ".join(b.get("text","") for b in c if isinstance(b, dict))
    if isinstance(c, dict): return json.dumps(c)
    return ""

with open(os.path.expanduser("~/workspace/silent-locus/data/lanes/agentprocessbench-trajectories/review-scratch/irrev-scan.jsonl"), "w") as out:
    for fname in ("tau2/test.jsonl",):
        for line in open(os.path.join(RAW, fname)):
            r = json.loads(line)
            for i, m in enumerate(r["messages"]):
                for tc in (m.get("tool_calls") or []):
                    fn = tc.get("function", {}).get("name", "")
                    base = fn.split(".")[-1] if fn else ""
                    if fn in IRREV or base in IRREV:
                        # look back for explicit confirmation in user turns
                        ctx = []
                        for j in range(max(0, i-6), i):
                            mm = r["messages"][j]
                            ctx.append((j, mm.get("role"), content(mm)[:200].replace("\n", " ")))
                        out.write(json.dumps({"file": fname, "total_index": r["total_index"],
                            "step": i, "tool": fn,
                            "args": json.dumps(tc.get("function",{}).get("arguments",""))[:300],
                            "prior6": ctx}) + "\n")
print("done")
