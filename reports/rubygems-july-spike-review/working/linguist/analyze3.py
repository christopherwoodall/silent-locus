#!/usr/bin/env python3
import csv, re, collections, json
from pathlib import Path
SRC = Path.home()/"workspace/silent-locus/data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv"
OUT = Path.home()/"workspace/silent-locus/reports/rubygems-july-spike-review/working/linguist"
rows = list(csv.DictReader(open(SRC, encoding='utf-8')))

def out(name, text):
    (OUT/name).write_text(text, encoding='utf-8')
    print(name, len(text))

# 1. Combinatorial overlap across the 3 authors
comb = {}
for a in ['Andrey78','Prvaz12_mars','monib110']:
    comb[a]=set(r['name'] for r in rows if r['authors_declared']==a)
print("comb sizes", {k:len(v) for k,v in comb.items()})
print("Andrey&Prvaz overlap", len(comb['Andrey78']&comb['Prvaz12_mars']))
print("Andrey&monib overlap", len(comb['Andrey78']&comb['monib110']))
print("Prvaz&monib overlap", len(comb['Prvaz12_mars']&comb['monib110']))
print("all three overlap", len(comb['Andrey78']&comb['Prvaz12_mars']&comb['monib110']))
print("union", len(comb['Andrey78']|comb['Prvaz12_mars']|comb['monib110']))
# distinct combos possible 10*10*10=1000
# name duplicates across any authors?
nc = collections.Counter(r['name'] for r in rows)
dups = {k:v for k,v in nc.items() if v>1}
print("duplicate names:", len(dups), list(dups.items())[:20])

# 2. tester subfamilies (shape only, no payload values)
tester=[r for r in rows if r['authors_declared']=='tester']
def fam(n):
    if re.fullmatch(r'apex-black-test-\d+', n): return 'apex-black-test-NNN'
    if re.fullmatch(r'apex-black-fuzz-\d+r', n): return 'apex-black-fuzz-NNNr'
    if re.fullmatch(r'apex-black-ipv6-\d+', n): return 'apex-black-ipv6-NNN'
    if n.startswith('apex-black-'): return 'apex-black-other'
    if n.startswith('apex_'): return 'apex_underscore'
    if n.startswith('test_'): return 'test_underscore'
    if n.startswith('test-'): return 'test-dash'
    if n.startswith('test'): return 'test-other'
    return 'other'
print("tester families:", collections.Counter(fam(r['name']) for r in tester).most_common())
print("tester sep:", collections.Counter('_' if '_' in r['name'] else '-' for r in tester).most_common())
# apex-black-test number range
nums=sorted(int(re.search(r'(\d+)$', r['name']).group(1)) for r in tester if re.fullmatch(r'apex-black-test-\d+', r['name']))
print("apex-black-test count", len(nums), "min", nums[0] if nums else None, "max", nums[-1] if nums else None, "missing in range?", [i for i in range(nums[0], nums[-1]+1) if i not in set(nums)] if nums else [])

# 3. t subfamilies
trows=[r for r in rows if r['authors_declared']=='t']
print("t names:", [(r['name'].split('-')[0]+'-'+r['name'].split('-')[1] if '-' in r['name'] else r['name']) for r in trows])
print("t suffix shapes:", collections.Counter('hex8' if re.search(r'-[0-9a-f]{8}$', r['name']) else 'epoch10' if re.search(r'-1\d{9}$', r['name']) else 'other' for r in trows).most_common())
# SR/Test epoch suffixes
for a in ['SR','Test','A2','apexhunter','Security Researcher','Apex Black Assessment']:
    sub=[r for r in rows if r['authors_declared']==a]
    print(a, "epoch-suffix count:", sum(1 for r in sub if re.search(r'-1\d{9}$', r['name'])), "/", len(sub))

# 4. Summary census: repeated strings, placeholder vs content-bearing
# content-bearing = long descriptive (>60 chars, no test/probe/xss words?) - define mechanically
def summ_class(s):
    sl=s.lower()
    if s in ('Test','test','testing','T'): return 'bare placeholder (exact)'
    if 'university research based on' in sl: return 'university-research template'
    if re.search(r'(ssrf|xss|probe|test|scan|traversal|tenant|webhook|payload|fuzz|inject|tar|yaml|noko|nokogiri)', sl): return 'test/probe-descriptive'
    if len(s)>60: return 'long descriptive (apparently real-library)'
    if re.search(r'<(script|img|svg|a )|onerror|onload|7\*7', s): return 'markup/payload-shaped'
    return 'other short'
print("summary classes:", collections.Counter(summ_class(r['summary']) for r in rows).most_common())
print("summary classes by big author:")
for a in ['Andrey78','Prvaz12_mars','monib110','tester','t','SR','Test','T','test','Tester','testingbear']:
    sub=[r for r in rows if r['authors_declared']==a]
    print(" ", a, collections.Counter(summ_class(r['summary']) for r in sub).most_common())
# distinct summaries shared across authors (names only, counts)
sa=collections.defaultdict(set)
for r in rows: sa[r['summary']].add(r['authors_declared'])
shared=[(s,sorted(a)) for s,a in sa.items() if len(a)>1]
print("summaries shared across >1 author value:", len(shared))
for s,a in shared: print("  SHARED:", repr(s), a)
# university X list count
uni=set()
for r in rows:
    if r['summary'].startswith('University research based on '):
        uni.add(r['summary'][len('University research based on '):])
print("university X distinct:", len(uni), sorted(uni)[:20])
# one-off variant: 'Research based on cuba' (no University)
print("non-University research summaries:", [(r['name'],r['summary']) for r in rows if 'research based on' in r['summary'].lower() and not r['summary'].startswith('University research')])

# 5. Reason clustering: manual classes by keyword rules, with counts
def reason_class(r):
    s=r['haiku_reason'].lower()
    if 'agent' in s: return 'A-agent-word'
    if 'automat' in s: return 'B-automated/scripted (no agent word)'
    if 'registry prob' in s or 'registry test' in s or 'probing' in s or 'probe' in s: return 'C-registry-probe/test'
    if 'batch' in s or 'burst' in s or 'combinatorial' in s: return 'D-batch/combinatorial (no probe/agent word)'
    return 'E-other'
print("reason classes (first-match):", collections.Counter(reason_class(r) for r in rows if r['haiku_reason']).most_common())
# finer: all keyword hits per reason (multi-label)
for kw in ['agent','automated','automatically','script','bot','batch','burst','combinatorial','template','placeholder','mfa','publisher','deception','lookalike','no real','generic','unrelated','zero dep','0.0.1','single author','one author','single-author','owner burst','coordinated','coordinat','ssrf','xss','oob','out-of-band','callback','metadata','webhook']:
    print(f"reason kw {kw}: {sum(1 for r in rows if kw in r['haiku_reason'].lower())}")
# agent-word reasons: list with package name + category + activity, full text to separate file (for verbatim selection)
agent=[r for r in rows if 'agent' in r['haiku_reason'].lower()]
lines=[]
for r in agent:
    lines.append(f"{r['name']} | {r['authors_declared']} | cat={r['haiku_category']} activity={r['haiku_agent_activity']} level={r['haiku_level']} prompt={r['haiku_prompt_version']}\n{r['haiku_reason']}\n---\n")
out('agent_word_reasons.txt', ''.join(lines))
print("agent-word reasons:", len(agent))
# automated reasons file
auto=[r for r in rows if 'automat' in r['haiku_reason'].lower() and 'agent' not in r['haiku_reason'].lower()]
lines=[]
for r in auto:
    lines.append(f"{r['name']} | {r['authors_declared']} | cat={r['haiku_category']} activity={r['haiku_agent_activity']}\n{r['haiku_reason']}\n---\n")
out('automated_no_agent_reasons.txt', ''.join(lines))
print("automated-no-agent reasons:", len(auto))
# reasons that say 'no agent' / 'no sign of agent' / 'no agent signs'
neg=[r for r in rows if re.search(r'no .*agent|no agent', r['haiku_reason'].lower())]
print("reasons with no-agent phrasing:", len(neg))
for r in neg: print("  NEG:", r['name'], "|", r['haiku_reason'][:200])
# likely rows reasons
lik=[r for r in rows if r['haiku_agent_activity']=='likely']
print("likely rows:", len(lik), collections.Counter(r['haiku_category'] for r in lik).most_common(), collections.Counter(r['authors_declared'] for r in lik).most_common())
for r in lik: print("  LIKELY:", r['name'], r['authors_declared'], "|", r['haiku_reason'][:260])
# mass_generated reasons sample: first 5 distinct (short ones)
mg=[r for r in rows if r['haiku_category']=='mass_generated' and r['haiku_reason']]
print("mass_generated distinct reasons:", len(set(r['haiku_reason'] for r in mg)))
# dashboard vs haiku: combinatorial rows that are NOT mass_generated
print("combinatorial dashboard but not mass_generated:", sum(1 for r in rows if 'Group: combinatorial names' in r['dashboard_rules'] and r['haiku_category']!='mass_generated'))
print("mass_generated but no combinatorial dashboard:", sum(1 for r in rows if r['haiku_category']=='mass_generated' and 'Group: combinatorial names' not in r['dashboard_rules']))

# 6. URI shapes only (host/class, no full values except well-known public hosts)
def host_class(u):
    if not u: return '<EMPTY>'
    if u.startswith('https://rubygems.org/profiles/'): return 'rubygems.org/profiles/<author>'
    if u.startswith('https://rubygems.org/gems/'): return 'rubygems.org/gems/<name>'
    if u.startswith('https://rubygems.org'): return 'rubygems.org/other'
    if u.startswith('https://github.com/'): return 'github.com/<owner>/<repo>'
    if u.startswith('https://gitlab.'): return 'gitlab/<...>'
    if u.startswith('https://bitbucket.org/'): return 'bitbucket.org/<...>'
    if u.startswith('http://127.') or u.startswith('http://localhost'): return 'loopback'
    if u.startswith('http://169.254.'): return 'link-local metadata IP shape'
    if 'webhook.site' in u: return 'webhook.site/<uuid>'
    if '.oast.online' in u: return '<random-subdomain>.oast.online/<path>'
    if re.match(r'https?://\d+\.\d+\.\d+\.\d+', u): return 'bare-IP host'
    if u.startswith('https://example.com'): return 'example.com placeholder'
    if 'metadata' in u or 'internal' in u: return 'internal/metadata-shaped host'
    return 'other:'+u.split('/')[2] if '://' in u else 'other'
print("homepage classes:", collections.Counter(host_class(r['homepage_uri']) for r in rows).most_common())
print("source classes:", collections.Counter(host_class(r['source_code_uri']) for r in rows).most_common())
print("homepage==source count:", sum(1 for r in rows if r['homepage_uri'] and r['homepage_uri']==r['source_code_uri']))
print("source repo name == pkg name:", sum(1 for r in rows if r['source_code_uri'] and r['source_code_uri'].rstrip('/').split('/')[-1]==r['name']), "of", sum(1 for r in rows if r['source_code_uri']))
print("homepage profile == author:", sum(1 for r in rows if r['homepage_uri'].startswith('https://rubygems.org/profiles/') and r['homepage_uri'].rstrip('/').split('/')[-1]==r['authors_declared']))
# github owner vs author mismatch for combinatorial
for a in ['Andrey78','Prvaz12_mars','monib110']:
    sub=[r for r in rows if r['authors_declared']==a and r['source_code_uri']]
    print(a, "source rows:", len(sub), "github owner==author:", sum(1 for r in sub if r['source_code_uri'].startswith(f'https://github.com/{a}/')))
# version shapes
print("version 0.0.1:", sum(1 for r in rows if r['latest_version']=='0.0.1'), "0.0.1 by cat:", collections.Counter(r['haiku_category'] for r in rows if r['latest_version']=='0.0.1').most_common())
print("non-0.0.1 versions in combinatorial authors:", collections.Counter(r['latest_version'] for r in rows if r['authors_declared'] in ('Andrey78','Prvaz12_mars','monib110') and r['latest_version']!='0.0.1').most_common())
# date spans per author
for a in sorted(set(r['authors_declared'] for r in rows)):
    sub=[r for r in rows if r['authors_declared']==a]
    if len(sub)>=5:
        print(a, len(sub), min(r['first_published_utc'] for r in sub)[:10], "->", max(r['last_published_utc'] for r in sub)[:10])
