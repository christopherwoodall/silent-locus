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

# hex prefix first-seen ordering for hex-labeled hosts
first = {}
for r in aw:
    sub = r['host'][:-len('.appwrite.network')]
    m = re.fullmatch(r'([0-9a-f]{12})', sub)
    if m and (sub not in first or r['date'] < first[sub]): first[sub] = r['date']
ord_ = sorted(first.items(), key=lambda kv: kv[1])
print('hex12 hosts:', len(first))
print('first 15 (chronological first-seen):')
for p, d in ord_[:15]: print(' ', d, p)
print('last 15:')
for p, d in ord_[-15:]: print(' ', d, p)
# prefix ordering check: first-seen order vs numeric order
vals = [int(p,16) for p,_ in ord_]
asc = sum(1 for a,b in zip(vals, vals[1:]) if b >= a)
print('ascending-adjacent pairs: %d / %d' % (asc, len(vals)-1))

# re-scan span for top hosts
hc = collections.Counter(r['host'] for r in aw)
print('\n--- re-scan spans for top hosts ---')
for h, n in hc.most_common(12):
    ts = sorted(r['date'] for r in aw if r['host']==h)
    print(n, h, ts[0], '->', ts[-1])
