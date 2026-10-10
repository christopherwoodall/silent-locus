import json, re, collections
from urllib.parse import urlparse

allr = []
for off in [0,60,120,180,240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140,1200,1260,1320]:
    f = 'uq_appwrite_kw_o%d.json'%off if off else 'uq_appwrite_kw.json'
    d = json.load(open(f)); allr += d['reports']
seen = {}
for r in allr: seen[r['report_id']] = r
allr = list(seen.values())
print('UNIQUE TOTAL', len(allr))
ds = sorted(r['date'] for r in allr); print('RANGE', ds[0], ds[-1])

def host(r):
    u = r['url']
    if '://' not in u: u = 'https://' + u
    try: return urlparse(u).hostname
    except: return None

aw = [r for r in allr if (host(r) or '').endswith('.appwrite.network') or 'appwrite.network' in r['url']]
print('appwrite.network reports', len(aw))
# per-minute histogram (all)
c = collections.Counter(r['date'][:16] for r in aw)
mins = sorted(c)
print('minutes with reports:', len(mins))
# hosts
hc = collections.Counter(host(r) for r in aw)
print('unique *.appwrite.network hosts:', len(hc))
print('--- top re-scanned hosts ---')
for h, n in hc.most_common(25): print(n, h)
# naming grammar
hex_pref = collections.defaultdict(list)
branch = collections.defaultdict(list)
named = []
for h in hc:
    if not h: continue
    sub = h[:-len('.appwrite.network')]
    m = re.fullmatch(r'([0-9a-f]{6,})', sub)
    if m: hex_pref[sub].append(h)
    elif sub.startswith('branch-'): branch[sub].append(h)
    else: named.append(sub)
print('hex-labeled sites:', len(hex_pref), 'branch-deploys:', len(branch), 'named:', len(named))
print('--- named hosts ---')
for n in sorted(named): print(' ', n)
print('--- branch deploys (sample 30) ---')
for b in sorted(branch): print(' ', b, hc['%s.appwrite.network'%b])
