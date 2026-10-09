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
# persist full deduped list
jsonl = open('burst_report_ids.jsonl','w')
for r in sorted(aw, key=lambda x:(x['date'],x['report_id'])):
    jsonl.write(json.dumps({'report_id':r['report_id'],'date':r['date'],'url':r['url']})+'\n')
jsonl.close()
print('persisted', len(aw))

# hourly histogram
c = collections.Counter(r['date'][:13] for r in aw)
print('--- hourly ---')
for k in sorted(c): print(k, c[k])
# branch-name grammar breakdown
br = [r['host'][:-len('.appwrite.network')] for r in aw if (r['host'] or '').startswith('branch-')]
grams = collections.Counter(re.match(r'^branch-([a-z]+)', b).group(1) if re.match(r'^branch-([a-z]+)', b) else 'other' for b in br)
print('--- branch prefix grammar (unique hosts in parens) ---')
for g, n in grams.most_common():
    hosts = set(b for b in br if (re.match(r'^branch-([a-z]+)', b) or [None,'other'])[1] == g)
    print(g, n, 'reports /', len(hosts), 'unique hosts')
print('total branch-* reports', len(br), '/', len(set(br)), 'unique branch deploys')
# named (non-branch, non-hex) sample with re-scan counts
hc = collections.Counter(r['host'] for r in aw)
named = [(h,n) for h,n in hc.items() if h and not h.startswith('branch-') and not re.match(r'^[0-9a-f]{8,}', h)]
print('--- top named non-branch hosts ---')
for h,n in sorted(named, key=lambda x:-x[1])[:15]: print(n,h)
