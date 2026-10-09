#!/usr/bin/env python3
"""Lane 1: enumerate joshuadavid corpus (k4be + linuxiarz), reconcile vs our 131,
build swarm grammar taxonomy. Reads only the public GitHub export.
Writes: census.jsonl, reconciliation.json, taxonomy.json, taxonomy.md
"""
import json, os, re, hashlib
from collections import Counter, defaultdict

JD = '/tmp'
LDIR = os.path.expanduser('~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane1-reconciliation')

def load(host):
    fn = f"{JD}/jd_{host}_revisions.jsonl"
    return [json.loads(l) for l in open(fn)]

def pid_of(r):
    return r['page_id'].split('/', 1)[1]

def census(host):
    out = []
    for r in load(host):
        out.append({
            'host': host,
            'pid': pid_of(r),
            'title': r.get('source_title'),
            'time': r.get('time') or r.get('write_date'),
            'time_grade': r.get('time_grade'),
            'verdict': r.get('verdict'),
            'inclusion_reason': r.get('inclusion_reason'),
            'verdict_confidence': r.get('verdict_confidence'),
            'verdict_rationale': r.get('verdict_rationale'),
            'label': r.get('label'),
            'label_source': r.get('label_source'),
            'body_availability': r.get('body_availability'),
            'body_len': r.get('body_len'),
            'body_sha256': r.get('body_sha256'),
            'source_url': r.get('source_url'),
            'site_lang': r.get('site_lang'),
            'replyto_pid': r.get('replyto_pid'),
            'replyto_title': r.get('replyto_title'),
            'wb_timestamp': r.get('wb_timestamp'),
            'write_date': r.get('write_date'),
        })
    return out

ken = census('pastebin-k4be')
lin = census('paste-linuxiarz')
with open(f"{LDIR}/census.jsonl", 'w') as f:
    for c in ken + lin:
        f.write(json.dumps(c) + '\n')

ours = set(open('/tmp/ours_ids.txt').read().split())
jd_lin = {c['pid']: c for c in lin}
overlap = sorted(set(jd_lin) & ours)
new_lin = sorted(set(jd_lin) - ours)
jd_k4be_pids = sorted(c['pid'] for c in ken)

recon = {
    'our_prior_ingest_count': len(ours),
    'jd_linuxiarz_total': len(lin),
    'jd_k4be_total': len(ken),
    'jd_linuxiarz_overlap_ours': overlap,
    'jd_linuxiarz_new_vs_ours': new_lin,
    'jd_k4be_pids': jd_k4be_pids,
    'verdict_breakdown_linuxiarz': Counter(c['verdict'] for c in lin),
    'verdict_breakdown_k4be': Counter(c['verdict'] for c in ken),
    'inclusion_linuxiarz': Counter(c['inclusion_reason'] for c in lin),
    'inclusion_k4be': Counter(c['inclusion_reason'] for c in ken),
    'body_avail_linuxiarz': Counter(c['body_availability'] for c in lin),
    'body_avail_k4be': Counter(c['body_availability'] for c in ken),
}
with open(f"{LDIR}/reconciliation.json", 'w') as f:
    json.dump(recon, f, indent=2)

print('overlap ours∩jd-linuxiarz:', len(overlap))
print('new linuxiarz vs ours:', len(new_lin))
print('k4be total:', len(jd_k4be_pids))
print('k4be verdicts:', recon['verdict_breakdown_k4be'])
print('li verdicts:', recon['verdict_breakdown_linuxiarz'])
print('li inclusion:', recon['inclusion_linuxiarz'])
print('li body_avail:', recon['body_avail_linuxiarz'])

# --- Grammar taxonomy ---
MARKERS = [
    ('PAD\\d+x\\d+', 'title+body', re.compile(r'PAD\d+x\d+')),
    ('TEL\\d{6,}', 'title+body', re.compile(r'TEL\d{6,}')),
    ('TK\\d{5,}', 'title+body', re.compile(r'TK\d{5,}')),
    ('pad-<epoch>-<n>', 'body', re.compile(r'pad-\d{9,}-\d+')),
    ('CLICKMAYBE', 'body', re.compile(r'CLICKMAYBE')),
    ('URLMARK', 'body', re.compile(r'URLMARK')),
    ('FRAMEK4', 'body', re.compile(r'FRAMEK4')),
    ('REPLYURL', 'title+body', re.compile(r'REPLYURL')),
    ('GOR091159-style', 'title+body', re.compile(r'\bGOR\d{6}\b')),
    ('clock.wait', 'body', re.compile(r'clock\.wait')),
    ('task clock', 'body', re.compile(r'task clock')),
    ('container UTC', 'body', re.compile(r'container UTC')),
    ('shared UTC', 'body', re.compile(r'shared UTC')),
    ('scaffold clock', 'body', re.compile(r'scaffold clock')),
    ('R1..R9 rounds', 'title+body', re.compile(r'\bR[1-9]\b')),
    ('cohort MAR13', 'title+body', re.compile(r'MAR13')),
    ('cohort Dec27', 'title+body', re.compile(r'Dec27')),
    ('cohort Aug09', 'title+body', re.compile(r'Aug09')),
    ('OAI Transfer <hex>', 'body', re.compile(r'OAI Transfer [0-9a-f]{8,}')),
    ('agent-XXXX handle', 'title+body', re.compile(r'@?agent-[0-9a-f]{4}\b')),
    ('IowaCollabReply', 'title', re.compile(r'IowaCollabReply')),
    ('IowaPostFinal', 'title', re.compile(r'IowaPostFinal\w*')),
    ('IowaCache', 'title', re.compile(r'IowaCache\w*')),
    ('Iowa* (any)', 'title', re.compile(r'Iowa\w*')),
    ('LANGURL', 'body', re.compile(r'LANGURL')),
    ('Q1..Q9 task', 'body', re.compile(r'\bQ[1-9]\b')),
    ('85 and Older', 'body', re.compile(r'85 and Older')),
    ('thecolony.ai', 'body', re.compile(r'thecolony\.ai')),
    ('public-board.com', 'body', re.compile(r'public-board\.com')),
    ('bullfincher.io/sec-proxy', 'body', re.compile(r'bullfincher\.io/sec-proxy')),
    ('jqp.vercel.app/api/v0', 'body', re.compile(r'jqp\.vercel\.app/api/v0')),
    ('2md.link', 'body', re.compile(r'2md\.link')),
    ('is.gd', 'body', re.compile(r'is\.gd')),
    ('md.succ.ai', 'body', re.compile(r'md\.succ\.ai')),
    ('pure.md', 'body', re.compile(r'pure\.md')),
    ('telegra.ph', 'body', re.compile(r'telegra\.ph')),
    ('jina.ai', 'body', re.compile(r'jina')),
    ('webhook', 'body', re.compile(r'webhook')),
    ('zz=', 'body', re.compile(r'zz=oai|zz=')),
    ('oai tag', 'body', re.compile(r'\boai[a-z0-9_]')),
    ('EPL 1995-00', 'title', re.compile(r'EPL 1995')),
    ('Roi Et TH45', 'body', re.compile(r'Roi Et|TH45')),
    ('NSI lookup', 'title+body', re.compile(r'\bNSI\b')),
    ('stikked Re: reply', 'title', re.compile(r'^Re: ')),
    ('URLTEST\\d', 'title+body', re.compile(r'URLTEST\d')),
    ('linktry\\d', 'title+body', re.compile(r'linktry\d')),
    ('ShortVariants', 'body', re.compile(r'ShortVariants')),
    ('ProxyBare', 'body', re.compile(r'ProxyBare')),
    ('ProxyVariants', 'body', re.compile(r'ProxyVariants')),
    ('ProxyTry', 'title+body', re.compile(r'ProxyTry')),
    ('agent-ours0909', 'body', re.compile(r'agent-ours0909')),
]

tax = {}
for name, scope, rx in MARKERS:
    hits = defaultdict(list)  # host -> [pid]
    first_seen = {}
    for host, fn in [('pastebin-k4be', f'{JD}/jd_pastebin-k4be_revisions.jsonl'),
                     ('paste-linuxiarz', f'{JD}/jd_paste-linuxiarz_revisions.jsonl')]:
        for line in open(fn):
            r = json.loads(line)
            body = r.get('body') or ''
            title = r.get('source_title') or ''
            hay = body + '\n' + title if scope == 'title+body' else (body if scope == 'body' else title)
            if rx.search(hay):
                p = pid_of(r)
                hits[host].append(p)
                t = r.get('time') or r.get('write_date')
                if t and (p not in first_seen or t < first_seen[p]):
                    first_seen[p] = t
    all_pids = sorted({p for v in hits.values() for p in v})
    earliest = min(first_seen.values()) if first_seen else None
    tax[name] = {
        'count': len(all_pids),
        'hosts': {h: len(v) for h, v in hits.items() if v},
        'first_seen': earliest,
        'pids': all_pids[:50],
        'truncated': len(all_pids) > 50,
    }

with open(f"{LDIR}/taxonomy.json", 'w') as f:
    json.dump(tax, f, indent=2)

print('\n--- taxonomy summary ---')
for name, scope, rx in MARKERS:
    t = tax[name]
    print(f"{name:28s} n={t['count']:4d} hosts={t['hosts']} first={t['first_seen']}")
