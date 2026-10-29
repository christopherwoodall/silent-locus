#!/usr/bin/env python3
"""AUDIT-WORKER-3: API ground-truth check for oldest in-window revision per article.
Paces at >=5s between requests to en.wikipedia.org. Progress saved incrementally.
"""
import json, subprocess, time, sys, os
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

BASE = os.path.expanduser('~/workspace/silent-locus-top500/data/2026-10-06-wikipedia-top500-infra-scan')
UA = 'silent-locus-top500-scan/1.0 (research)'
API = 'https://en.wikipedia.org/w/api.php'

def ts_parse(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00'))

def api_oldest(title):
    params = {
        'action': 'query', 'prop': 'revisions',
        'titles': title, 'rvlimit': '1', 'rvdir': 'newer',
        'rvstart': '2020-01-01T00:00:00Z',
        'rvprop': 'ids|timestamp', 'format': 'json', 'formatversion': '2',
    }
    qs = '&'.join(f'{k}={quote(v, safe="")}' for k, v in params.items())
    url = f'{API}?{qs}'
    r = subprocess.run(['curl', '-s', '--max-time', '40', '-A', UA, url],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return {'error': f'curl exit {r.returncode}', 'stderr': r.stderr[:200]}
    try:
        data = json.loads(r.stdout)
    except Exception as e:
        return {'error': f'json parse: {e}', 'raw': r.stdout[:200]}
    try:
        page = data['query']['pages'][0]
    except (KeyError, IndexError):
        return {'error': 'no pages in response', 'raw': r.stdout[:300]}
    if 'missing' in page or 'revisions' not in page:
        return {'error': 'missing page or no revisions', 'page': {k: page.get(k) for k in ('pageid','title','missing')}}
    rev = page['revisions'][0]
    return {'revid': rev['revid'], 'timestamp': rev['timestamp']}

def main():
    entries = json.load(open(f'{BASE}/workers/audit-3/local-check.json'))
    out_path = f'{BASE}/workers/audit-3/api-ground-truth.json'
    done = {}
    if os.path.exists(out_path):
        try:
            done = {e['key']: e for e in json.load(open(out_path))}
        except Exception:
            pass
    out = list(done.values())
    api_calls = 0
    for e in entries:
        key = f"{e['rank']}::{e['file']}"
        if key in done:
            continue
        time.sleep(5.0)  # pacing: <=1 req per 5s
        res = api_oldest(e['title'])
        api_calls += 1
        rec = {'key': key, 'rank': e['rank'], 'title': e['title'], 'file': e['file'],
               'file_lines': e.get('lines', 0), 'file_min_ts': e.get('min_ts'),
               'api_oldest': res}
        if 'error' in res:
            rec['verdict'] = 'API_ERROR'
        elif e.get('lines', 0) == 0:
            rec['verdict'] = 'BROKEN'  # empty file but API has revision
        else:
            fts, ats = ts_parse(e['min_ts']), ts_parse(res['timestamp'])
            delta = (fts - ats).total_seconds()
            rec['delta_seconds'] = delta
            rec['verdict'] = 'TRUNCATED' if delta > 86400 else 'OK'
        out.append(rec)
        done[key] = rec
        with open(out_path, 'w') as f:
            json.dump(out, f, indent=1)
        print(f"[{len(out)}/{len(entries)}] rank={e['rank']} {e['title'][:40]:40s} -> {rec['verdict']} api_ts={res.get('timestamp','ERR')} file_min={e.get('min_ts')}", flush=True)
    print(f'DONE api_calls_this_run={api_calls}')

if __name__ == '__main__':
    main()
