import json, re, collections
from urllib.parse import urlparse

allr = []
for off in [0,60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320]:
    f = 'uq_appwrite_kw_o%d.json'%off if off else 'uq_appwrite_kw.json'
    d = json.load(open(f)); allr += d['reports']
seen = {}
for r in allr: seen[r['report_id']] = r
allr = list(seen.values())
def host(r):
    u = r['url']
    if '://' not in u: u = 'https://' + u
    try: return urlparse(u).hostname
    except: return None
for r in allr: r['host'] = host(r)
aw = [r for r in allr if (r['host'] or '').endswith('.appwrite.network')]

# hex extraction: leading hex run in subdomain, and full-hex subdomains
prefixes = {}
lengths = collections.Counter()
for r in aw:
    sub = r['host'][:-len('.appwrite.network')]
    m = re.match(r'^([0-9a-f]{8,})', sub)
    if m:
        p = m.group(1); lengths[len(p)] += 1
        if p not in prefixes or r['date'] < prefixes[p]: prefixes[p] = r['date']
print('hex-prefix length distribution:', dict(lengths))
print('distinct hex prefixes:', len(prefixes))
ord_ = sorted(prefixes.items(), key=lambda kv: kv[1])
vals = [int(p,16) for p,_ in ord_]
asc = sum(1 for a,b in zip(vals, vals[1:]) if b >= a)
print('ascending-adjacent pairs: %d / %d (%.1f%%)' % (asc, len(vals)-1, 100*asc/max(1,len(vals)-1)))
print('first 10 chronologically:')
for p, d in ord_[:10]: print(' ', d, p)
print('last 10:')
for p, d in ord_[-10:]: print(' ', d, p)

# intervals for top host branch-v2-0f34728
ts = sorted(r['date'] for r in aw if r['host']=='branch-v2-0f34728.appwrite.network')
print('\nbranch-v2-0f34728 intervals (min): first 10 / last 5')
from datetime import datetime
dt = [datetime.fromisoformat(t.replace('Z','+00:00')) for t in ts]
diffs = [(b-a).total_seconds()/60 for a,b in zip(dt,dt[1:])]
print(' '.join('%.1f'%x for x in diffs[:10]))
print(' '.join('%.1f'%x for x in diffs[-5:]))

# known operator markers in URLs
markers = ['zz=','uqscan','httpbun','webhook','oai','epoch','nonce','?task','batch=','eval','harness']
print('\nmarker hits in appwrite URLs:')
for mk in markers:
    hits = [r['url'] for r in aw if mk in r['url'].lower()]
    print(' ', mk, len(hits))
# branch names containing QA/dev keywords
qa = [r['host'] for r in aw if re.search(r'routertest|e2e|validation|feat-|staging|stage|qa-|test|deploy|ci-|preview', r['host'] or '')]
print('\nQA/dev-keyword hosts (distinct):', len(set(qa)))
