import json, datetime, urllib.request, os, time
from concurrent.futures import ThreadPoolExecutor

feeds = {
    'tf':      ('tf_manifest.json',      'https://threatfox.abuse.ch/downloads/misp/'),
    'urlhaus': ('urlhaus_manifest.json', 'https://urlhaus.abuse.ch/downloads/misp/'),
    'bazaar':  ('bazaar_manifest.json',  'https://bazaar.abuse.ch/downloads/misp/'),
}
lo = datetime.date(2026,4,1); hi = datetime.date(2026,9,1)
jobs = []
for tag,(mf,base) in feeds.items():
    m = json.load(open(mf))
    os.makedirs(f'misp_{tag}', exist_ok=True)
    for uuid, v in m.items():
        t = v.get('timestamp')
        if not t: continue
        d = datetime.datetime.fromtimestamp(int(t), datetime.UTC).date()
        if lo <= d <= hi:
            out = f'misp_{tag}/{uuid}.json'
            if not os.path.exists(out) or os.path.getsize(out) < 100:
                jobs.append((base+uuid+'.json', out))
print('to download:', len(jobs))

def fetch(job):
    url, out = job
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'threat-research-lane15b/1.0'})
        with urllib.request.urlopen(req, timeout=40) as r, open(out,'wb') as f:
            f.write(r.read())
        return True
    except Exception as e:
        return f'{url}: {e}'

with ThreadPoolExecutor(max_workers=4) as ex:
    res = list(ex.map(fetch, jobs))
ok = sum(1 for r in res if r is True)
print('downloaded ok:', ok, 'of', len(jobs))
for r in res:
    if r is not True: print('FAIL', r)
