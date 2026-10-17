#!/usr/bin/env python3
"""Scanner for reviewer A (rows 0-892) of jetbrains-swe-trajectories.
Finds keyword-marker candidate hits; human triages the bytes."""
import pyarrow.parquet as pq
import re, json, os

PARQ = os.path.expanduser('~/workspace/silent-locus/data/lanes/jetbrains-swe-trajectories/raw/data/train-00000-of-00001.parquet')
OUT = os.path.expanduser('~/workspace/silent-locus/data/lanes/jetbrains-swe-trajectories/working/scan_A_hits.jsonl')

MARKERS = {
    'CAPTCHA': [r'captcha', r'recaptcha', r'human verification', r'prove you are human', r'are you a robot'],
    'ACCOUNT': [r'sign[\s_-]?up', r'create (an|a) account', r'register (an|a) account', r'new account', r'account creation'],
    'GUARDRAIL': [r'not allowed', r'cannot comply', r"i'?m unable to", r'against (my|the) polic', r'\brefuse[sd]?\b', r'policy violation', r'safety concern'],
    'PROMPT-INJECT': [r'ignore (all )?previous instructions', r'disregard (all )?(previous|your) instructions', r'override (your|the) instructions', r'you are now', r'new instructions', r'prompt injection'],
    'CREDENTIAL': [r'password\s*[:=]', r'api[_-]?key\s*[:=]', r'secret\s*[:=]', r'ghp_[A-Za-z0-9]{10,}', r'AKIA[0-9A-Z]{10,}', r'sk-[A-Za-z0-9]{8,}'],
    'IRREVERSIBLE': [r'rm\s+-rf?\s+/', r'git push', r'--force', r'drop table', r'delete\s+from', r'shutdown', r'reboot'],
    'TOOL-MISUSE': [r'\bcurl\b', r'\bwget\b', r'pip install', r'\bssh\b', r'\bnc\s+-', r'netcat', r'nmap', r'exfiltrat'],
    'COORDINATION': [r'another agent', r'other agent', r'\bdelegate\b', r'handoff', r'swarm', r'multi-?agent'],
    'TESTFILE': [r'tests?/', r'test_\w+\.py', r'conftest', r'sed\s+-i.*test', r'rm\s+.*test'],
    'FABRICATE': [r'all tests pass', r'tests? (are |were )?passing', r'fix (is |was )?verified', r'successfully (fixed|resolved)', r'confirmed working'],
    'RECOVERY': [r'let me try (a |an )?(different|another|new)', r'alternative approach', r'different approach', r'giving up', r'fall ?back'],
    'SELFMOD': [r'modif(y|ied|ication).*(test|spec)', r'(test|spec).*(modif|delet|remov)', r'update the test', r'change the test', r'edit the test'],
}

def scan():
    t = pq.read_table(PARQ)
    rows = t.to_pylist()
    hits = []
    for idx in range(0, 893):
        r = rows[idx]
        iid = r['instance_id']
        full = '\n'.join(m['content'] or '' for m in r['messages'])
        low = full.lower()
        for cls, pats in MARKERS.items():
            for p in pats:
                for m in re.finditer(p, low, re.IGNORECASE):
                    s = max(0, m.start()-200); e = m.end()+200
                    hits.append({'row': idx, 'instance_id': iid, 'class_hint': cls,
                                 'pattern': p, 'snippet': full[s:e].replace('\n', ' | ')[:500]})
    with open(OUT, 'w') as f:
        for h in hits:
            f.write(json.dumps(h) + '\n')
    print('hits:', len(hits))
    from collections import Counter
    print(Counter((h['class_hint']) for h in hits))

if __name__ == '__main__':
    scan()
