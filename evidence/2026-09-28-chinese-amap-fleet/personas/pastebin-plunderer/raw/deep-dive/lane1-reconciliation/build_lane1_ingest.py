#!/usr/bin/env python3
"""Lane 1 ingest builder (2026-10-05).
Part A: extend data/2026-05-26-paste-linuxiarz/ with the 250 genuinely-new
        linuxiarz pids from joshuadavid/WikiAgentSwarmInvestigation.
Part B: build new dataset data/2025-10-24-pastebin-k4be/ (198 pids).
Source: /tmp/jd_<host>_revisions.jsonl (public GitHub export, fetched 2026-10-05).
No network, no ES writes. Verifies every body against jd body_sha256.
"""
import json, os, hashlib, datetime, sys
from collections import Counter

JD = '/tmp'
REPO = os.path.expanduser('~/workspace/silent-locus')
LIA = os.path.join(REPO, 'data/2026-05-26-paste-linuxiarz')
K4B = os.path.join(REPO, 'data/2025-10-24-pastebin-k4be')
JD_REPO = 'https://github.com/JoshuaDavid/WikiAgentSwarmInvestigation'
CREATED = datetime.datetime.now(datetime.timezone.utc).isoformat()

ours = set(open('/tmp/ours_ids.txt').read().split())

def load(host):
    return [json.loads(l) for l in open(f'{JD}/jd_{host}_revisions.jsonl')]

def pid_of(r):
    return r['page_id'].split('/', 1)[1]

def sha(b: bytes):
    return hashlib.sha256(b).hexdigest()

def manifest_entry(host, r, body_ok):
    p = pid_of(r)
    return {
        'id': p,
        'title': r.get('source_title'),
        'retrieval_timestamp': CREATED,
        'retrieval_method': 'extracted_from_joshuadavid_wikiagentswarminvestigation_export',
        'source_urls': [r.get('source_url')],
        'source_host': 'paste.linuxiarz.pl' if host == 'paste-linuxiarz' else 'pastebin.k4be.pl',
        'jd_inclusion_reason': r.get('inclusion_reason'),
        'jd_verdict': r.get('verdict'),
        'jd_verdict_confidence': r.get('verdict_confidence'),
        'jd_verdict_rationale': r.get('verdict_rationale'),
        'jd_label': r.get('label'),
        'jd_label_source': r.get('label_source'),
        'jd_body_availability': r.get('body_availability'),
        'jd_time': r.get('time'),
        'jd_write_date': r.get('write_date'),
        'jd_time_grade': r.get('time_grade'),
        'jd_wb_timestamp': r.get('wb_timestamp'),
        'jd_replyto_pid': r.get('replyto_pid'),
        'jd_replyto_title': r.get('replyto_title'),
        'jd_site_lang': r.get('site_lang'),
        'external_overlap': [f'{JD_REPO}/agent-logs/{host} (rev main, retrieved 2026-10-05)'],
        'jd_body_sha256': r.get('body_sha256'),
        'body_sha256': sha((r.get('body') or '').encode('utf-8')) if (r.get('body') or '') else None,
        'body_sha256_matches_jd': body_ok,
        'body_bytes': len((r.get('body') or '').encode('utf-8')),
        'live_status': 'not_checked_lane1',
    }
    return man

def event_row(host, dataset, r, body_ok, man):
    p = pid_of(r)
    t = r.get('time')
    if t:
        ts, tsrc = t, 'labels:paste.jd_time'
    else:
        ts, tsrc = '1970-01-01T00:00:00Z', 'fallback:no_recoverable_date'
    conf = 'confirmed' if (body_ok and r.get('body')) else 'medium'
    body_bytes = len((r.get('body') or '').encode('utf-8'))
    row = {
        '@timestamp': ts,
        'event': {'dataset': dataset, 'created': CREATED},
        'record_kind': 'relay_paste',
        'fingerprint': sha(f"{'linuxiarz' if host=='paste-linuxiarz' else 'k4be'}-paste:{p}".encode()),
        'labels': {
            'paste.id': p,
            'paste.title': r.get('source_title'),
            'paste.jd_time': r.get('time'),
            'paste.jd_time_grade': r.get('time_grade'),
            'paste.jd_inclusion_reason': r.get('inclusion_reason'),
            'paste.jd_verdict': r.get('verdict'),
            'paste.jd_verdict_confidence': r.get('verdict_confidence'),
            'paste.jd_body_availability': r.get('body_availability'),
            'paste.jd_label': r.get('label'),
            'paste.retrieval_method': 'extracted_from_joshuadavid_wikiagentswarminvestigation_export',
            'paste.live_status': 'not_checked_lane1',
            'paste.external_overlap': f'{JD_REPO}/agent-logs/{host}',
            'timestamp_source': tsrc,
        },
        'source_url': r.get('source_url'),
        'size_bytes': body_bytes,
        'retrieved_at': CREATED,
        'retrieved_via': 'extracted_from_joshuadavid_wikiagentswarminvestigation_export',
        'confidence': conf,
        'description': (
            f"{'paste.linuxiarz.pl' if host=='paste-linuxiarz' else 'pastebin.k4be.pl'} paste "
            f"'{r.get('source_title')}' ({body_bytes} B): joshuadavid-export copy, "
            f"verdict={r.get('verdict')}, inclusion={r.get('inclusion_reason')}, "
            f"body_availability={r.get('body_availability')}"
        ),
    }
    if man['body_sha256']:
        row['sha256'] = man['body_sha256']
    return row

# ============ Part A: extend linuxiarz ============
lin = load('paste-linuxiarz')
new_lin = [r for r in lin if pid_of(r) not in ours]
assert len(new_lin) == 250, len(new_lin)

rawdir = os.path.join(LIA, 'raw')
os.makedirs(rawdir, exist_ok=True)

LIA_MANIFEST = os.path.join(rawdir, 'manifest.jsonl')
LIA_EVENTS = os.path.join(LIA, 'events.jsonl')
have_man = {json.loads(l)['id'] for l in open(LIA_MANIFEST)}
have_evt = {json.loads(l)['labels']['paste.id'] for l in open(LIA_EVENTS)}
already = have_man | have_evt
n_body = n_viewonly = n_mismatch = 0
man_lines = []
evt_lines = []
for r in new_lin:
    p = pid_of(r)
    if p in already:
        print('skip (already present):', p)
        continue
    body = r.get('body') or ''
    body_ok = (sha(body.encode('utf-8')) == r.get('body_sha256')) if body else False
    if r.get('body_availability') == 'full_source' and body:
        with open(os.path.join(rawdir, f'{p}.txt'), 'w', encoding='utf-8') as f:
            f.write(body)
        n_body += 1
    else:
        n_viewonly += 1
    if body and not body_ok:
        n_mismatch += 1
    man = manifest_entry('paste-linuxiarz', r, body_ok)
    man_lines.append(json.dumps(man))
    evt_lines.append(json.dumps(event_row('paste-linuxiarz', '2026-05-26-paste-linuxiarz', r, body_ok, man)))

with open(LIA_MANIFEST, 'a') as f:
    if man_lines:
        f.write('\n'.join(man_lines) + '\n')
with open(LIA_EVENTS, 'a') as f:
    if evt_lines:
        f.write('\n'.join(evt_lines) + '\n')

# regenerate SHA256SUMS (events.jsonl + all raw/ contents)
def tree_sums(coll):
    out = []
    for root, dirs, files in os.walk(coll):
        dirs.sort()
        for name in sorted(files):
            if name == 'SHA256SUMS':
                continue
            full = os.path.join(root, name)
            out.append(f"{sha(open(full,'rb').read())}  {os.path.relpath(full, coll)}")
    with open(os.path.join(coll, 'SHA256SUMS'), 'w') as f:
        f.write('\n'.join(out) + '\n')
    return len(out)

n = tree_sums(LIA)
print(f'Part A done: +250 linuxiarz (bodies={n_body}, view-only={n_viewonly}, sha-mismatch={n_mismatch}); SHA256SUMS={n} files')

# ============ Part B: new k4be dataset ============
k4b = load('pastebin-k4be')
os.makedirs(os.path.join(K4B, 'raw'), exist_ok=True)
man_lines, evt_lines = [], []
n_mismatch = 0
for r in k4b:
    p = pid_of(r)
    body = r.get('body') or ''
    body_ok = bool(body) and sha(body.encode('utf-8')) == r.get('body_sha256')
    if not body_ok:
        n_mismatch += 1
    with open(os.path.join(K4B, 'raw', f'{p}.txt'), 'w', encoding='utf-8') as f:
        f.write(body)
    man = manifest_entry('pastebin-k4be', r, body_ok)
    man_lines.append(json.dumps(man))
    evt_lines.append(json.dumps(event_row('pastebin-k4be', '2025-10-24-pastebin-k4be', r, body_ok, man)))

with open(os.path.join(K4B, 'raw', 'manifest.jsonl'), 'w') as f:
    f.write('\n'.join(man_lines) + '\n')
with open(os.path.join(K4B, 'events.jsonl'), 'w') as f:
    f.write('\n'.join(evt_lines) + '\n')

# rollup: per-day bursts
days = Counter((json.loads(l)['@timestamp'] or '')[:10] for l in evt_lines)
roll = []
for day in sorted(days):
    ts = f'{day}T00:00:00Z'
    roll.append(json.dumps({
        '@timestamp': ts,
        'event': {'dataset': '2025-10-24-pastebin-k4be-rollup', 'created': CREATED},
        'record_kind': 'paste_day_burst',
        'fingerprint': sha(f'k4be-paste-day:{day}'.encode()),
        'labels': {'paste.day': day, 'paste.count': days[day],
                   'timestamp_source': 'labels:paste.jd_time',
                   'record_layer': 'rollup'},
        'confidence': 'confirmed',
        'description': f'pastebin.k4be.pl day burst {day}: {days[day]} swarm-surface pastes',
    }))
with open(os.path.join(K4B, 'rollup.jsonl'), 'w') as f:
    f.write('\n'.join(roll) + '\n')

n = tree_sums(K4B)
print(f'Part B done: {len(k4b)} k4be pastes, sha-mismatch={n_mismatch}, days={len(roll)}, SHA256SUMS={n} files')

# final verify
for path in [os.path.join(LIA,'events.jsonl'), os.path.join(K4B,'events.jsonl'), os.path.join(K4B,'rollup.jsonl')]:
    n = sum(1 for _ in open(path))
    print(path, n)
