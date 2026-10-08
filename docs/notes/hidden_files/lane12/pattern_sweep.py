#!/usr/bin/env python3
"""HUNT LANE 12 pattern sweep — grammar-enumerated candidate gem names +
r.jina.ai laundering URLs, exact-queried against CC index.
Resilient: retries, cooldowns on backend outage. Durable state."""
import json, time, urllib.request, urllib.parse, os

BASE = os.path.dirname(os.path.abspath(__file__))
CRAWL = 'CC-MAIN-2026-21'
OUT = os.path.join(BASE, 'pattern_results.jsonl')
STATE = os.path.join(BASE, 'pattern_state.json')

def load_state():
    try:
        return json.load(open(STATE))
    except Exception:
        return {'done': []}

def save_state(s):
    json.dump(s, open(STATE, 'w'))

def query(url):
    q = urllib.parse.urlencode({'url': url, 'output': 'json'})
    req = urllib.request.Request(
        f'https://index.commoncrawl.org/{CRAWL}-index?{q}',
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

def run(targets, label):
    state = load_state()
    done = set(state['done'])
    consec = 0
    out = open(OUT, 'a')
    for i, t in enumerate(targets):
        key = f'{label}|{t}'
        if key in done:
            continue
        st, body = query(t)
        if st == 'fail':
            consec += 1
            if consec >= 6:
                print(f'[{label}] backend down, cooling 10min ({i}/{len(targets)})', flush=True)
                time.sleep(600); consec = 0
            continue
        consec = 0
        try:
            recs = [json.loads(l) for l in body.strip().splitlines() if l.strip()]
        except Exception:
            recs = []
        hits = [r for r in recs if isinstance(r, dict) and r.get('url')]
        if hits:
            out.write(json.dumps({'crawl': CRAWL, 'target': t, 'label': label,
                                  'captures': hits}) + '\n')
            out.flush()
            print(f'HIT [{label}] {t}', flush=True)
        done.add(key)
        if len(done) % 50 == 0:
            state['done'] = list(done); save_state(state)
        if (i + 1) % 50 == 0:
            print(f'[{label}] {i+1}/{len(targets)}', flush=True)
        time.sleep(2)
    state['done'] = list(done); save_state(state)
    out.close()
    print(f'DONE [{label}]', flush=True)

if __name__ == '__main__':
    cands = [l.strip() for l in open(os.path.join(BASE, 'pattern_cands.txt')) if l.strip()]
    run([f'rubygems.org/gems/{c}' for c in cands], 'grammar')
    jurls = [l.strip() for l in open(os.path.join(BASE, 'jina_urls.txt')) if l.strip()
             and 'example.com' not in l]
    run(jurls, 'jina-url')
