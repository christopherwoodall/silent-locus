import json, os, re, sys

LANE = os.path.expanduser('~/workspace/silent-locus/data/lanes/agenterrorbench-trajectories')
out = json.load(open('/tmp/aeb_findings.json'))

def expand(s):
    steps = []
    for part in s.split(','):
        part = part.strip()
        if '-' in part:
            a, b = part.split('-', 1)
            steps += list(range(int(a), int(b) + 1))
        else:
            steps.append(int(part))
    return steps

def action_spans(content):
    spans = []
    for m in re.finditer(r'<action>(.*?)</action>', content, re.S):
        spans.append(m.group(1))
    if not spans:
        m = re.search(r'<action>(.*)$', content, re.S)
        if m:
            spans.append(m.group(1) + ' [UNTERMINATED: no </action>]')
    return spans

issues = []
for f in out:
    path = os.path.join(LANE, 'raw', f['subdir'], f['traj'])
    t = json.load(open(path))
    msgs = t['messages']
    nsteps = (len(msgs) - 1) // 2
    steps = expand(f['steps'])
    md = t.get('metadata', {})
    f['meta'] = {'model': md.get('model'), 'env': md.get('environment'),
                 'nsteps': md.get('steps'), 'won': md.get('won'),
                 'ts': md.get('timestamp'), 'msgcount': len(msgs)}
    for s in steps:
        idx = 2 * s - 1
        if idx >= len(msgs):
            issues.append((f['id'], s, 'STEP-OUT-OF-RANGE'))
            continue
        c = msgs[idx]['content']
        if msgs[idx]['role'] != 'assistant':
            issues.append((f['id'], s, 'NOT-ASSISTANT'))
        sp = action_spans(c)
        if not sp:
            issues.append((f['id'], s, 'NO-ACTION-TAG', c[:160].replace('\n', ' ')))
json.dump(out, open('/tmp/aeb_findings_meta.json', 'w'), indent=1)
print('issues:')
for i in issues:
    print(' ', i[0], i[1], i[2], i[3][:100] if len(i) > 3 else '')
print('total issues:', len(issues))
