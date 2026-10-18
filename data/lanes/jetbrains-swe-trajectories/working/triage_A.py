#!/usr/bin/env python3
"""Semantic triage for reviewer A (rows 0-892).
Extracts bash commands per trajectory and flags semantic candidates:
 test-write, no-test-before-submit, format violations, model routing."""
import pyarrow.parquet as pq
import re, json, os
from collections import Counter

PARQ = os.path.expanduser('~/workspace/silent-locus/data/lanes/jetbrains-swe-trajectories/raw/data/train-00000-of-00001.parquet')
OUTD = os.path.expanduser('~/workspace/silent-locus/data/lanes/jetbrains-swe-trajectories/working')

CMD_RE = re.compile(r'```bash\s*\n(.*?)```', re.DOTALL)
WRITE_TEST_RE = re.compile(r'(sed\s+-i|apply_patch|>\s*\S*test|>>\s*\S*test|tee\s+\S*test|patch\s+-p)', re.IGNORECASE)
TEST_PATH_RE = re.compile(r'(tests?/|test_\w*\.py|conftest\.py)', re.IGNORECASE)
RUN_TEST_RE = re.compile(r'(pytest|bin/test|doctest|python\s+-m\s+test)', re.IGNORECASE)
SUBMIT_RE = re.compile(r'COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT')

def main():
    t = pq.read_table(PARQ, columns=['instance_id','n_turns','exit_status','selected_models','messages'])
    rows = t.to_pylist()
    report = {'test_writes': [], 'no_test_before_submit': [], 'format_violations': [],
              'submit_without_any_command': [], 'weird': []}
    model_mix = Counter()
    for idx in range(0, 893):
        r = rows[idx]; iid = r['instance_id']
        msgs = r['messages']
        sm = r['selected_models'] or []
        model_mix[tuple(sm[:4])] += 0  # placeholder
        n_models = len(set(sm))
        asst = [m['content'] for m in msgs if m['role']=='assistant']
        cmds = []
        n_blocks_viol = 0
        for a in asst:
            blocks = CMD_RE.findall(a or '')
            if len(blocks) != 1:
                n_blocks_viol += 1
            cmds.extend(blocks)
        allcmd = '\n'.join(cmds)
        # test file writes
        for c in cmds:
            if WRITE_TEST_RE.search(c) and TEST_PATH_RE.search(c):
                report['test_writes'].append({'row': idx, 'instance_id': iid, 'cmd': c[:400]})
                break
        # no test run before submit
        if SUBMIT_RE.search(allcmd) and not RUN_TEST_RE.search(allcmd):
            report['no_test_before_submit'].append({'row': idx, 'instance_id': iid,
                'exit': r['exit_status'], 'n_cmds': len(cmds)})
        if n_blocks_viol:
            report['format_violations'].append({'row': idx, 'instance_id': iid,
                'viol_msgs': n_blocks_viol, 'n_asst': len(asst)})
    # model routing stats
    mix = Counter()
    for idx in range(0, 893):
        sm = rows[idx]['selected_models'] or []
        mix[(sm[0] if sm else None, len(set(sm)))] += 1
    print(json.dumps({k: len(v) for k, v in report.items()}, indent=1))
    print("model routing (first_model, n_distinct):", dict(mix))
    print("\n--- test_writes:", len(report['test_writes']))
    for h in report['test_writes'][:20]:
        print(h['row'], h['instance_id'], '|', h['cmd'][:200].replace('\n',' | '))
    print("\n--- no_test_before_submit sample:")
    for h in report['no_test_before_submit'][:20]:
        print(h)
    print("\n--- format_violations sample (n=%d):" % len(report['format_violations']))
    for h in report['format_violations'][:10]:
        print(h)
    json.dump(report, open(os.path.join(OUTD, 'triage_A.json'), 'w'), indent=1)

if __name__ == '__main__':
    main()
