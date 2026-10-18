#!/usr/bin/env python3
"""JetBrains SWE trajectories verifier helpers. Passive read-only."""
import sys, json
import pyarrow.parquet as pq

PQ_PATH = "data/lanes/jetbrains-swe-trajectories/raw/data/train-00000-of-00001.parquet"

def load_cols(cols, row_filter=None):
    tbl = pq.read_table(PQ_PATH, columns=cols)
    return tbl

def find_row(instance_id):
    tbl = pq.read_table(PQ_PATH, columns=["instance_id"])
    ids = tbl.column("instance_id").to_pylist()
    hits = [i for i, v in enumerate(ids) if v == instance_id]
    return hits

def get_row(idx):
    tbl = pq.read_table(PQ_PATH)
    row = tbl.slice(idx, 1)
    d = row.to_pylist()[0]
    return d

def dump_msgs(instance_id, a=None, b=None, out="/tmp/msgdump.txt", maxchars=4000):
    hits = find_row(instance_id)
    if not hits:
        print("NO ROW:", instance_id); return
    idx = hits[0]
    row = get_row(idx)
    msgs = row["messages"]
    print(f"row={idx} instance={instance_id} n_msgs={len(msgs)} n_turns={row['n_turns']} exit={row['exit_status']}")
    lo, hi = (a or 0), (b if b is not None else len(msgs))
    lines = []
    for i in range(lo, min(hi, len(msgs))):
        m = msgs[i]
        role = m.get("role")
        content = m.get("content") or ""
        lines.append(f"===== msg {i} role={role} chars={len(content)} =====")
        lines.append(content[:maxchars])
        lines.append("")
    with open(out, "w") as f:
        f.write("\n".join(lines))
    print("wrote", out)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "find":
        for i in find_row(sys.argv[2]):
            print(i)
    elif cmd == "dump":
        iid = sys.argv[2]
        a = int(sys.argv[3]) if len(sys.argv) > 3 else None
        b = int(sys.argv[4]) if len(sys.argv) > 4 else None
        dump_msgs(iid, a, b)
