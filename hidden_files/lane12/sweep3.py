#!/usr/bin/env python3
"""HUNT LANE 12 rev3 — resilient Common Crawl sweep.
Survives backend outages: per-query retries with backoff, plus a global
cooldown loop (up to ~2h) when the CDX backend is broadly failing.
Writes durably to the project hidden_files dir."""
import json, time, urllib.request, urllib.parse, sys, os

BASE = os.path.expanduser('~/workspace/muse-home/projects/swarmtraces-hf-corpus/hidden_files/lane12')
NAMES = [l.strip() for l in open(os.path.join(BASE, 'gemnames.txt')) if l.strip()]
CRAWLS = ['CC-MAIN-2026-21', 'CC-MAIN-2026-25', 'CC-MAIN-2026-30']
OUT = os.path.join(BASE, 'results.jsonl')
STATE = os.path.join(BASE, 'state.json')

def load_state():
    try:
        return json.load(open(STATE))
    except Exception:
        return {'done': []}  # list of "crawl|name"

def save_state(s):
    json.dump(s, open(STATE, 'w'))

def query(crawl, url):
    q = urllib.parse.urlencode({'url': url, 'output': 'json'})
    req = urllib.request.Request(
        f'https://index.commoncrawl.org/{crawl}-index?{q}',
        headers={'User-Agent': 'research-bot/1.0'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read().decode('utf-8', 'replace')
            if 'Gateway Time-out' in body:
                raise RuntimeError('504-html')
            return ('ok', body)
        except Exception as e:
            time.sleep(4 * (attempt + 1))
    return ('fail', 'backend-error')

def main():
    state = load_state()
    done = set(state['done'])
    deadline = time.time() + 2 * 3600
    out = open(OUT, 'a')
    total = len(NAMES) * len(CRAWLS)
    consec_fail = 0
    for crawl in CRAWLS:
        for name in NAMES:
            key = f'{crawl}|{name}'
            if key in done:
                continue
            if time.time() > deadline:
                print('DEADLINE reached', flush=True)
                out.close(); save_state(state); return
            st, body = query(crawl, f'rubygems.org/gems/{name}')
            if st == 'fail':
                consec_fail += 1
                if consec_fail >= 6:
                    print(f'backend down, cooling 10 min ({len(done)}/{total} done)', flush=True)
                    time.sleep(600)
                    consec_fail = 0
                continue  # do not mark done; retry later
            consec_fail = 0
            try:
                recs = [json.loads(l) for l in body.strip().splitlines() if l.strip()]
            except Exception:
                recs = []
            hits = [r for r in recs if isinstance(r, dict) and r.get('url')]
            if hits:
                out.write(json.dumps({'crawl': crawl, 'name': name, 'captures': hits}) + '\n')
                out.flush()
                print(f'HIT {crawl} {name}', flush=True)
            done.add(key)
            if len(done) % 40 == 0:
                save_state(state)
                print(f'progress {len(done)}/{total}', flush=True)
            time.sleep(2)
    save_state(state)
    out.close()
    print('DONE all crawls', flush=True)

main()
