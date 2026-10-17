#!/usr/bin/env python3
"""Batch dump of message ranges for verifier. Loads table once."""
import json, sys
import pyarrow.parquet as pq

PQ = "data/lanes/jetbrains-swe-trajectories/raw/data/train-00000-of-00001.parquet"

PLAN = {
    "FA-001": (97, 8, 20),
    "FA-002": (548, 38, 50),
    "FA-003": (157, 0, None),   # full; triage check needs whole tail
    "F-001": (894, 18, 40),
    "F-002": (1774, 18, 30),
    "F-003": (1510, 22, 42),
    "F-004": (1471, 46, 66),
}

def main():
    tbl = pq.read_table(PQ)
    for tag, (idx, lo, hi) in PLAN.items():
        row = tbl.slice(idx, 1).to_pylist()[0]
        msgs = row["messages"]
        hi = hi if hi is not None else len(msgs)
        out = f"/tmp/vdump-{tag}.jsonl"
        with open(out, "w") as f:
            f.write(json.dumps({"row": idx, "instance": row["instance_id"],
                                "n_msgs": len(msgs), "n_turns": row["n_turns"],
                                "exit": row["exit_status"],
                                "models_head": (row["selected_models"] or [])[:8]}) + "\n")
            for i in range(lo, min(hi, len(msgs))):
                m = msgs[i]
                f.write(json.dumps({"i": i, "role": m.get("role"), "content": m.get("content")}) + "\n")
        print(tag, "->", out, "msgs", lo, "-", min(hi, len(msgs)))

main()
