#!/usr/bin/env python3
"""HUNT LANE 12 rev4 — rubydoc.info gem pages + urlkey-filter mechanism sweep.
Resilient: retries, cooldowns on backend outage. Durable state."""
import json, time, urllib.request, urllib.parse, os

BASE = os.path.dirname(os.path.abspath(__file__))
NAMES = [l.strip() for l in open(os.path.join(BASE, 'gemnames.txt')) if l.strip()]
CRAWLS = ['CC-MAIN-2026-30', 'CC-MAIN-2026-25']
OUT = os.path.join(BASE, 'rubydoc_results.jsonl')
STATE = os.path.join(BASE, 'state4.json')
FILTERS = {
    'go-import': 'rubygems.org/gems/*',
    'web_hooks': 'rubygems.org/*',
    'A000': 'rubygems.org/*',
    'ZZEND': 'rubygems.org/*',
    'go-import-rd': 'rubydoc.info/*',
    'web_hooks-rd': 'rubydoc.info/*',
    'A000-rd': 'rubydoc.info/*',
}

def load_state():
    try:
        return json.load(open(STATE))
    except Exception:
        return {'done': []}

def save_state(s):
    json.dump(s, open(STATE, 'w'))

def query(params):
    q = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        f'https://index.commoncrawl.org/CC-MAIN-X-index?{q}'.replace('CC-MAIN-X', params.pop('_crawl')),
        headers={'User-Agent': 'research-bot/1.0'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read().decode('utf-8', 'replace')
            if 'Gateway Time-out' in body:
                raise RuntimeError('504-html')
            return ('ok', body)
        except Exception:
            time.sleep(4 * (attempt + 1))
    return ('fail', '')

def main():
    state = load_state()
    done = set(state['done'])
    deadline = time.time() + 2 * 3600
    out = open(OUT, 'a')
    consec = 0
    jobs = []
    for crawl in CRAWLS:
        for name in NAMES:
            jobs.append(('rubydoc', crawl, f'rubydoc.info/gems/{name}', None))
    # NOTE: prefix+filter (urlkey regex) queries removed — prior lane run found
    # the CC backend 504s on all range scans even when healthy; exact-URL only.
    total = len(jobs)
    for i, (kind, crawl, target, marker) in enumerate(jobs):
        key = f'{kind}|{crawl}|{target}|{marker}'
        if key in done:
            continue
        if time.time() > deadline:
            print('DEADLINE reached', flush=True)
            break
        params = {'_crawl': crawl, 'output': 'json'}
        if kind == 'rubydoc':
            params['url'] = target
        else:
            params['url'] = target
            params['matchType'] = 'prefix'
            params['filter'] = f'urlkey:.*{marker}.*'
            params['limit'] = '200'
        st, body = query(params)
        if st == 'fail':
            consec += 1
            if consec >= 6:
                print(f'backend down, cooling 10 min ({i}/{total})', flush=True)
                time.sleep(600); consec = 0
            continue
        consec = 0
        try:
            recs = [json.loads(l) for l in body.strip().splitlines() if l.strip()]
        except Exception:
            recs = []
        hits = [r for r in recs if isinstance(r, dict) and r.get('url')]
        if hits:
            out.write(json.dumps({'kind': kind, 'crawl': crawl, 'target': target,
                                  'marker': marker, 'captures': hits}) + '\n')
            out.flush()
            print(f'HIT [{kind}] {crawl} {target} {marker} n={len(hits)}', flush=True)
        done.add(key)
        if len(done) % 40 == 0:
            state['done'] = list(done); save_state(state)
            print(f'progress {len(done)}/{total}', flush=True)
        time.sleep(2)
    state['done'] = list(done); save_state(state)
    out.close()
    print('DONE sweep4', flush=True)

main()
