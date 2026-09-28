#!/usr/bin/env python3
"""Lane J — tantive.space read-only pull. GET-only, no posts/votes/accounts.
Pacing: 4s between requests. Resume-friendly via existing outputs."""
import json, time, hashlib, sys, os
from datetime import datetime, timezone
import urllib.request

UA = 'tantive-space-research/1.0 (read-only inventory sweep; no posts)'
BASE = 'https://tantive.space'
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "tantive-space")
os.makedirs(OUT, exist_ok=True)
PACE = 4.0

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.loads(r.read().decode('utf-8'))

def paged(start_url):
    """Follow next-links until has_more is False."""
    url = start_url
    seen = set()
    while url:
        if url in seen:
            print('LOOP guard, stopping', url, flush=True); break
        seen.add(url)
        d = get(url)
        yield d
        url = d.get('next') if d.get('has_more') else None
        if url:
            time.sleep(PACE)

def main():
    tpath = os.path.join(OUT, 'threads.jsonl')
    mpath = os.path.join(OUT, 'messages.jsonl')
    have_threads = set()
    if os.path.exists(tpath):
        with open(tpath) as f:
            for line in f:
                line = line.strip()
                if line:
                    have_threads.add(json.loads(line)['id'])
    new_threads = 0
    for page in paged(BASE + '/api/threads?limit=100'):
        for t in page.get('data', []):
            if t['id'] in have_threads:
                continue
            have_threads.add(t['id'])
            with open(tpath, 'a') as f:
                f.write(json.dumps(t) + '\n')
            new_threads += 1
        print(f'threads so far: {len(have_threads)} (new this run: {new_threads})', flush=True)

    # messages per thread, resume on thread ids already done
    done = set()
    dpath = os.path.join(OUT, 'threads_done.txt')
    if os.path.exists(dpath):
        with open(dpath) as f:
            done = set(x.strip() for x in f if x.strip())
    tids = sorted(have_threads - {int(x) for x in done})
    print(f'{len(tids)} threads to pull messages for', flush=True)
    nmsg = 0
    for i, tid in enumerate(tids):
        try:
            for page in paged(f'{BASE}/api/thread/{tid}?limit=50'):
                for m in page.get('data', []):
                    with open(mpath, 'a') as f:
                        f.write(json.dumps(m) + '\n')
                    nmsg += 1
        except Exception as e:
            print(f'thread {tid} FAILED: {e}', flush=True)
        with open(dpath, 'a') as f:
            f.write(f'{tid}\n')
        if i % 25 == 0:
            print(f'{i}/{len(tids)} threads, {nmsg} msgs', flush=True)

    retrieved = datetime.now(timezone.utc).isoformat()
    man = {'retrieved_at_utc': retrieved, 'threads': len(have_threads), 'messages_new_this_run': nmsg}
    for name in ('threads.jsonl', 'messages.jsonl'):
        p = os.path.join(OUT, name)
        if os.path.exists(p):
            h = hashlib.sha256()
            with open(p, 'rb') as f:
                for chunk in iter(lambda: f.read(1 << 20), b''):
                    h.update(chunk)
            man[name] = {'sha256': h.hexdigest(), 'bytes': os.path.getsize(p)}
    with open(os.path.join(OUT, 'manifest.json'), 'w') as f:
        json.dump(man, f, indent=2)
    print('DONE', json.dumps(man, indent=2), flush=True)

if __name__ == '__main__':
    main()
