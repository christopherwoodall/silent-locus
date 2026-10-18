#!/usr/bin/env python3
"""Reviewer A: print full steps of given trajectory ids. Read-only."""
import json, os, sys, csv

RAW = '/home/hatch/workspace/silent-locus/data/lanes/dtap-bench-trajectories/raw'

def load_index():
    import csv as csvm
    rows = list(csvm.DictReader(open('/home/hatch/workspace/silent-locus/data/lanes/dtap-bench-trajectories/working/reviewer-A-index.csv')))
    m = {}
    for r in rows:
        tid = f"{r['harness']}/{r['model']}/{r['env']}/{r['attack_path']}/{r['taskdir']}"
        m[tid] = r['dir']
    return m
IDXMAP = load_index()

def show(tid):
    d = os.path.join(RAW, IDXMAP[tid])
    files = [f for f in os.listdir(d) if f.endswith('.json') and f != 'judge_result.json'
             and not f.endswith('.PROVENANCE.txt') and not f.endswith('.sha256')]
    t = json.load(open(os.path.join(d, files[0])))
    ti = t.get('task_info', {}) or {}
    j = json.load(open(os.path.join(d, 'judge_result.json')))
    print('='*100)
    print('ID:', tid)
    print('attack_success=%s task_success=%s error=%s' % (j.get('attack_success'), j.get('task_success'), j.get('error')))
    print('ORIG:', str(ti.get('original_instruction',''))[:400])
    print('MAL :', str(ti.get('malicious_instruction',''))[:400])
    for s in t.get('trajectory', []):
        sid, role = s.get('step_id'), s.get('role')
        if role == 'agent':
            a = s.get('action',''); md = s.get('metadata',{}) or {}
            msg = md.get('message','')
            print(f'[{sid}] AGENT action={str(a)[:300]}')
            if msg: print(f'      msg: {str(msg)[:900]}')
        elif role == 'tool':
            md = s.get('metadata',{}) or {}
            print(f'[{sid}] TOOL {md.get("tool_name","?")}: {str(s.get("state",""))[:900]}')
        elif role == 'user':
            print(f'[{sid}] USER: {str(s.get("state",""))[:400]}')
    print()

if __name__ == '__main__':
    for tid in sys.argv[1:]:
        show(tid)
