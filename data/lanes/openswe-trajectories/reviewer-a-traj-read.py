#!/usr/bin/env python3
"""Dump one trajectory's messages compactly. Usage: traj_read.py <trajectory_id> [max_msg]"""
import sys, json
import pyarrow.parquet as pq

PARQUET = "/home/hatch/workspace/silent-locus/data/lanes/openswe-trajectories/raw/sweagent_minimax_m25_swe-rebench-v2_train-00000-of-00019.parquet"

def main():
    tid, maxm = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 400
    pf = pq.ParquetFile(PARQUET)
    found = None
    for batch in pf.iter_batches(batch_size=200, columns=["trajectory_id", "instance_id", "repo", "resolved", "messages"]):
        tids = batch.column("trajectory_id").to_pylist()
        if tid in tids:
            i = tids.index(tid)
            found = {
                "instance_id": batch.column("instance_id")[i].as_py(),
                "repo": batch.column("repo")[i].as_py(),
                "resolved": batch.column("resolved")[i].as_py(),
                "messages": batch.column("messages")[i].as_py(),
            }
            break
    if not found:
        print("NOT FOUND"); return
    print(f"=== {tid} | {found['instance_id']} | {found['repo']} | resolved={found['resolved']}")
    msgs = found["messages"]
    print(f"total messages: {len(msgs)}")
    for n, m in enumerate(msgs[:maxm]):
        role = m.get("role")
        if role == "assistant":
            rc = (m.get("reasoning_content") or "").strip()
            if rc:
                print(f"--- [msg {n}] ASSISTANT reasoning ({len(rc)} chars):")
                print(rc[:1500])
            for tc in (m.get("tool_calls") or []):
                fn = (tc.get("function") or {}).get("name")
                args = (tc.get("function") or {}).get("arguments") or ""
                try:
                    a = json.loads(args)
                except Exception:
                    a = {"_raw": args[:400]}
                if fn == "bash":
                    print(f"--- [msg {n}] BASH: {(a.get('command') or '')[:500]}")
                elif fn == "str_replace_editor":
                    extra = ""
                    if a.get("command") == "str_replace":
                        extra = f" old[:200]={str(a.get('old_str'))[:200]!r} new[:200]={str(a.get('new_str'))[:200]!r}"
                    elif a.get("command") == "create":
                        extra = f" file_text[:200]={str(a.get('file_text'))[:200]!r}"
                    print(f"--- [msg {n}] EDITOR {a.get('command')}: {a.get('path')}{extra}")
                else:
                    print(f"--- [msg {n}] TOOL {fn}: {str(a)[:300]}")
        elif role == "tool":
            c = (m.get("content") or "")
            # show observation compactly, flag errors
            first = c[:600].replace("\n", "\\n")
            print(f"    [obs {n}] ({len(c)} chars): {first}")
        elif role == "user" and n < 3:
            print(f"--- [msg {n}] USER: {(m.get('content') or '')[:800]}")

if __name__ == "__main__":
    main()
