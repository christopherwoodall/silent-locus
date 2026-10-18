#!/usr/bin/env python3
"""Read full transcript(s) of given trajectory_id(s), streaming. Usage: reader.py <tid> [tid2 ...] [--max-chars N]"""
import pyarrow.parquet as pq, sys, json

PARQUET = '/home/hatch/workspace/silent-locus/data/lanes/openswe-trajectories/raw/openhands_qwen35_122b_swe-rebench-v2_train-00000-of-00017.parquet'

def main():
    tids = set(a for a in sys.argv[1:] if not a.startswith('--'))
    max_chars = 6000
    for a in sys.argv[1:]:
        if a.startswith('--max-chars'): max_chars = int(a.split('=')[1])
    f = pq.ParquetFile(PARQUET)
    found = set()
    for batch in f.iter_batches(batch_size=40, columns=['instance_id','repo','language','trajectory_id','resolved','messages','metadata']):
        for r in batch.to_pylist():
            tid = r['trajectory_id']
            if tid not in tids or tid in found: continue
            found.add(tid)
            md = r.get('metadata') or {}
            print("="*100)
            print("TRAJ:", tid, "| instance:", r['instance_id'], "| repo:", r['repo'], "| resolved:", r['resolved'])
            print("category:", md.get('category'), "| teacher:", (md.get('teacher_model') or {}).get('name'))
            rp = (md.get('reference_patch') or {}).get('patch') or ''
            mp = (md.get('model_patch') or {}).get('patch') or ''
            print("ref_patch_lines:", len(rp.splitlines()), "model_patch_lines:", len(mp.splitlines()))
            msgs = r['messages'] or []
            print("n_messages:", len(msgs))
            for i, m in enumerate(msgs):
                print("-"*100)
                print(f"[{i}] role={m['role']}")
                c = (m.get('content') or '')
                rc = (m.get('reasoning_content') or '')
                if rc: print("REASONING:", rc[:2000])
                if c: print("CONTENT:", c[:max_chars])
                for tc in (m.get('tool_calls') or []):
                    fn = (tc.get('function') or {}).get('name')
                    args = (tc.get('function') or {}).get('arguments') or ''
                    print(f"TOOL {fn} id={tc.get('id')}")
                    print("ARGS:", args[:max_chars])
            if found == tids: return

main()
