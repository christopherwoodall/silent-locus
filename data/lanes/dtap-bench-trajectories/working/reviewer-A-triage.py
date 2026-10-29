#!/usr/bin/env python3
"""Reviewer A: triage scanner for DTap-Bench malicious trajectories.
Reads the index CSV, draws a deterministic per-cell sample, and prints
a compact episode card per trajectory for human triage.
Read-only. Does not execute benchmark code.
"""
import csv, json, os, sys, re

RAW = '/home/hatch/workspace/silent-locus/data/lanes/dtap-bench-trajectories/raw'
IDX = '/home/hatch/workspace/silent-locus/data/lanes/dtap-bench-trajectories/working/reviewer-A-index.csv'
SAMPLE = '/home/hatch/workspace/silent-locus/data/lanes/dtap-bench-trajectories/working/reviewer-A-sample.jsonl'

FLAG_WORDS = [
    'delete', 'rm -rf', 'exfiltrat', 'send_email', 'transfer', 'password',
    'api_key', 'apikey', 'secret', 'token', 'credential', 'ssn', 'credit card',
    'ignored', 'refus', 'declin', 'cannot comply', 'will not', 'stop',
    'sudo', 'chmod 777', 'curl | sh', 'wget | sh', 'eval(', 'exec(',
    'unauthorized', 'bypass', 'override', 'exploit', 'inject', 'payload',
]

def card(row):
    d = os.path.join(RAW, row['dir'])
    tpath = os.path.join(d, row['traj'])
    if not row['traj'] or not os.path.exists(tpath):
        return None
    try:
        t = json.load(open(tpath))
    except Exception:
        return None
    ti = t.get('task_info', {}) or {}
    steps = t.get('trajectory', []) or []
    acts = []
    for s in steps:
        role = s.get('role')
        if role == 'agent':
            a = s.get('action', '')
            md = s.get('metadata', {}) or {}
            msg = md.get('message', '')
            acts.append(('A', (str(a) + ' | ' + str(msg)[:120]).strip(' |')))
        elif role == 'tool':
            st = s.get('state', '')
            md = s.get('metadata', {}) or {}
            acts.append(('T', (md.get('tool_name', '') + ': ' + str(st)[:160]).strip(': ')))
        elif role == 'user':
            acts.append(('U', str(s.get('state', ''))[:160]))
    body = json.dumps(t)[:400000]
    flags = sorted({w for w in FLAG_WORDS if w in body.lower()})
    # compact: first 2, last 2 steps, plus any step with a flag word
    n = len(steps)
    keep = set()
    for i, (r, txt) in enumerate(acts):
        if i < 2 or i >= len(acts) - 2 or any(w in txt.lower() for w in flags):
            keep.add(i)
    lines = [f"{i}:{acts[i][0]} {acts[i][1][:220]}" for i in sorted(keep)]
    return {
        'id': f"{row['harness']}/{row['model']}/{row['env']}/{row['attack_path']}/{row['taskdir']}",
        'attack_success': row['attack_success'], 'task_success': row['task_success'],
        'n_steps': n,
        'original': str(ti.get('original_instruction', ''))[:300],
        'malicious': str(ti.get('malicious_instruction', ''))[:300],
        'flags': flags,
        'seq': lines,
        'dir': row['dir'], 'traj': row['traj'],
    }

def main():
    rows = list(csv.DictReader(open(IDX)))
    # deterministic sample: per (harness,model,env,attack_family) cell, every Kth sorted by attack_path/taskdir
    from collections import defaultdict
    cells = defaultdict(list)
    for r in rows:
        fam = r['attack_path'].split('/')[0] if r['attack_path'] else '?'
        cells[(r['harness'], r['model'], r['env'], fam)].append(r)
    sample = []
    for key, rs in cells.items():
        rs.sort(key=lambda r: (r['attack_path'], r['taskdir']))
        # target ~2 per cell; K adapts
        K = max(1, len(rs) // 2)
        picked = [r for i, r in enumerate(rs) if i % K == 0]
        # always include at least one attack_success=true per cell when present
        if not any(p['attack_success'] == 'True' for p in picked):
            for r in rs:
                if r['attack_success'] == 'True' and r not in picked:
                    picked.append(r); break
        sample.extend(picked)
    print(f'cells={len(cells)} sampled={len(sample)}', file=sys.stderr)
    with open(SAMPLE, 'w') as f:
        for r in sample:
            c = card(r)
            if c:
                f.write(json.dumps(c) + '\n')
    print('wrote', SAMPLE, file=sys.stderr)

if __name__ == '__main__':
    main()
