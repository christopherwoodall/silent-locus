#!/usr/bin/env python3
"""HUNT LANE 12 alt-route — Wayback Machine CDX for campaign gem pages.
index.commoncrawl.org query backend is down; web.archive.org/cdx works.
Exact-URL queries for rubygems.org/gems/<name> and rubydoc.info/gems/<name>.
Resilient: retries, durable state."""
import json, time, urllib.request, urllib.parse, os

BASE = os.path.dirname(os.path.abspath(__file__))
NAMES = [l.strip() for l in open(os.path.join(BASE, 'gemnames.txt')) if l.strip()]
OUT = os.path.join(BASE, 'wayback_results.jsonl')
STATE = os.path.join(BASE, 'state_wb.json')

def load_state():
    try:
        return json.load(open(STATE))
    except Exception:
        return {'done': []}

def save_state(s):
    json.dump(s, open(STATE, 'w'))

def query(url):
    q = urllib.parse.urlencode({'url': url, 'output': 'json', 'limit': '50',
                                'filter': 'statuscode:200'})
    req = urllib.request.Request('https://web.archive.org/cdx/search/cdx?' + q,
                                 headers={'User-Agent': 'research-bot/1.0'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                body = r.read().decode('utf-8', 'replace')
            return ('ok', body)
        except Exception:
            time.sleep(3 * (attempt + 1))
    return ('fail', '')

def main():
    state = load_state()
    done = set(state['done'])
    out = open(OUT, 'a')
    targets = []
    for name in NAMES:
        targets.append(('gem', f'rubygems.org/gems/{name}'))
        targets.append(('rubydoc', f'rubydoc.info/gems/{name}'))
    total = len(targets)
    consec = 0
    for i, (kind, target) in enumerate(targets):
        key = f'{kind}|{target}'
        if key in done:
            continue
        st, body = query(target)
        if st == 'fail':
            consec += 1
            if consec >= 8:
                print(f'wayback down, cooling 5 min ({i}/{total})', flush=True)
                time.sleep(300); consec = 0
            continue
        consec = 0
        try:
            recs = json.loads(body) if body.strip() else []
        except Exception:
            recs = []
        rows = recs[1:] if recs and recs[0][0] == 'urlkey' else recs
        if rows:
            out.write(json.dumps({'kind': kind, 'target': target,
                                  'captures': rows}) + '\n')
            out.flush()
            print(f'HIT [{kind}] {target} n={len(rows)}', flush=True)
        done.add(key)
        if len(done) % 60 == 0:
            state['done'] = list(done); save_state(state)
            print(f'progress {len(done)}/{total}', flush=True)
        time.sleep(5)  # polite pace: wayback throttles aggressive clients
    state['done'] = list(done); save_state(state)
    out.close()
    print('DONE wayback sweep', flush=True)

main()
