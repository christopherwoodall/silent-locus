#!/usr/bin/env python3
import csv, re, collections, json
from pathlib import Path
SRC = Path.home()/"workspace/silent-locus/data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv"
OUT = Path.home()/"workspace/silent-locus/reports/rubygems-july-spike-review/working/linguist"
rows = list(csv.DictReader(open(SRC, encoding='utf-8')))

# credential-shape triage: which keyword matched, counts only, no values printed
for kw in ['api','key','secret','token','password','passwd','aws_','sk-','ghp_','github_pat_','xox']:
    c=sum(1 for r in rows for v in r.values() if v and kw in v.lower())
    print(kw, c)

# Per-author detailed naming: token-count, separator, digit position
def detail(name):
    sep = '_' if '_' in name else ('-' if '-' in name else 'none')
    parts = re.split(r'[-_]', name)
    return len(parts), sep

for a in ['Andrey78','Prvaz12_mars','tester','monib110','t','SR','Test','T','test','Tester','testingbear']:
    sub=[r for r in rows if r['authors_declared']==a]
    if not sub: continue
    print(f"\n=== {a} n={len(sub)} ===")
    print(" token-count:", collections.Counter(detail(r['name'])[0] for r in sub).most_common())
    print(" sep:", collections.Counter(detail(r['name'])[1] for r in sub).most_common())
    print(" names sample:", [r['name'] for r in sub[:12]])
    # first token vocab
    print(" first-token:", collections.Counter(re.split(r'[-_]',r['name'])[0] for r in sub).most_common(25))
    print(" last-token:", collections.Counter(re.split(r'[-_]',r['name'])[-1] for r in sub).most_common(25))
    print(" summary top:", collections.Counter(r['summary'] for r in sub).most_common(12))
    print(" haiku_cat:", collections.Counter(r['haiku_category'] for r in sub).most_common())
    print(" haiku_agent:", collections.Counter(r['haiku_agent_activity'] for r in sub).most_common())
    print(" dashboard rules:", collections.Counter(rule.strip() for r in sub for rule in r['dashboard_rules'].split(';') if rule.strip()).most_common())

# All other authors combined
big={'Andrey78','Prvaz12_mars','tester','monib110','t','SR','Test','T','test','Tester','testingbear'}
rest=[r for r in rows if r['authors_declared'] not in big]
print(f"\n=== REST n={len(rest)} distinct authors={len(set(r['authors_declared'] for r in rest))} ===")
for r in rest:
    print(f"{r['authors_declared']!r} | {r['name']} | {r['summary']!r} | {r['haiku_category']} | {r['dashboard_rules']}")

# Name templates refined: replace each token by class
def tok_class(p):
    if p.isdigit(): return 'NUM'
    if re.fullmatch(r'[a-z]+\d+', p): return 'wordNUM'
    if re.fullmatch(r'\d+[a-z]+', p): return 'NUMword'
    if re.fullmatch(r'[a-z]+', p): return 'w'
    if re.fullmatch(r'[A-Z][a-z]+', p): return 'W'
    return 'X'
for a in sorted(set(r['authors_declared'] for r in rows)):
    sub=[r for r in rows if r['authors_declared']==a]
    c=collections.Counter('-'.join(tok_class(p) for p in re.split(r'[-_]',r['name'])) for r in sub)
    print(f"TEMPLATE {a} n={len(sub)}: {c.most_common()}")

# Specific grammars: Andrey78 word lists
print("\n--- Andrey78 token vocab ---")
sub=[r for r in rows if r['authors_declared']=='Andrey78']
for pos in range(4):
    vc=collections.Counter()
    for r in sub:
        parts=re.split(r'[-_]',r['name'])
        if len(parts)>pos: vc[parts[pos]]+=1
    print(f"pos{pos}: {vc.most_common(40)}")
print("\n--- Prvaz12_mars token vocab ---")
sub=[r for r in rows if r['authors_declared']=='Prvaz12_mars']
for pos in range(5):
    vc=collections.Counter()
    for r in sub:
        parts=re.split(r'[-_]',r['name'])
        if len(parts)>pos: vc[parts[pos]]+=1
    print(f"pos{pos}: {vc.most_common(40)}")
print("\n--- monib110 token vocab ---")
sub=[r for r in rows if r['authors_declared']=='monib110']
for pos in range(5):
    vc=collections.Counter()
    for r in sub:
        parts=re.split(r'[-_]',r['name'])
        if len(parts)>pos: vc[parts[pos]]+=1
    print(f"pos{pos}: {vc.most_common(40)}")
print("\n--- tester token vocab ---")
sub=[r for r in rows if r['authors_declared']=='tester']
for pos in range(5):
    vc=collections.Counter()
    for r in sub:
        parts=re.split(r'[-_]',r['name'])
        if len(parts)>pos: vc[parts[pos]]+=1
    print(f"pos{pos}: {vc.most_common(60)}")

# Summary: 'University research based on X' distinct X
uni=[r['summary'] for r in rows if r['summary'].startswith('University research based on ')]
print(f"\nUniversity-research summaries: {len(uni)} distinct X: {len(set(uni))}")
print(collections.Counter(uni).most_common(10))
# other summary templates: normalize numbers / names
def norm_summary(s):
    s=re.sub(r'\d+','N',s)
    return s
print("normalized summary top:", collections.Counter(norm_summary(r['summary']) for r in rows).most_common(40))
print("empty summary by author:", collections.Counter(r['authors_declared'] for r in rows if not r['summary']).most_common())
print("empty summary total:", sum(1 for r in rows if not r['summary']))
# placeholder-like summaries: short / generic
short=[r for r in rows if r['summary'] and len(r['summary'])<=12]
print(f"short summaries (<=12 chars): {len(short)}")
print(collections.Counter(r['summary'] for r in short).most_common(30))

# Haiku reason keyword census (counts only, for clustering)
keywords=['agent','automated','bot','script','mass','batch','template','combinatorial','generated','generate','probe','test','placeholder','empty','no code','no real','university','research','MFA','0.0.1','burst','series','numbered','single author','one author','same author','withdrawn','registry']
for kw in keywords:
    c=sum(1 for r in rows if kw.lower() in r['haiku_reason'].lower())
    print(f"reason contains {kw!r}: {c}")
# reasons mentioning agent explicitly vs automated/script
agent_rows=[r for r in rows if 'agent' in r['haiku_reason'].lower()]
print(f"reasons containing 'agent': {len(agent_rows)}; by category: {collections.Counter(r['haiku_category'] for r in agent_rows).most_common()} by agent_activity: {collections.Counter(r['haiku_agent_activity'] for r in agent_rows).most_common()}")
auto_rows=[r for r in rows if 'automat' in r['haiku_reason'].lower()]
print(f"reasons containing 'automat*': {len(auto_rows)}")
print(f"agent_activity=likely rows: {sum(1 for r in rows if r['haiku_agent_activity']=='likely')}, of those reason contains agent: {sum(1 for r in rows if r['haiku_agent_activity']=='likely' and 'agent' in r['haiku_reason'].lower())}")
print(f"agent_activity=possible rows: {sum(1 for r in rows if r['haiku_agent_activity']=='possible')}, of those reason contains agent: {sum(1 for r in rows if r['haiku_agent_activity']=='possible' and 'agent' in r['haiku_reason'].lower())}")
print(f"agent_activity=no_sign rows: {sum(1 for r in rows if r['haiku_agent_activity']=='no_sign')}")
# prompt v2 reasons
v2=[r for r in rows if r['haiku_prompt_version']=='pkg-review-2']
print(f"\n--- pkg-review-2 n={len(v2)} authors: {collections.Counter(r['authors_declared'] for r in v2).most_common()} cat: {collections.Counter(r['haiku_category'] for r in v2).most_common()} agent: {collections.Counter(r['haiku_agent_activity'] for r in v2).most_common()} level: {collections.Counter(r['haiku_level'] for r in v2).most_common()} ---")
for r in v2: print(repr(r['haiku_reason']))
# unclear + no_sign rows
print("\n--- unclear / no_sign rows ---")
for r in rows:
    if r['haiku_category']=='unclear' or r['haiku_agent_activity']=='no_sign':
        print(f"{r['name']} | {r['authors_declared']} | cat={r['haiku_category']} agent={r['haiku_agent_activity']} level={r['haiku_level']} reason={r['haiku_reason']!r}")
# empty haiku rows: which authors?
print("\nempty-haiku by author:", collections.Counter(r['authors_declared'] for r in rows if not r['haiku_category']).most_common())
print("empty-haiku names sample:", [r['name'] for r in rows if not r['haiku_category']][:60])
# dashboard vs haiku disagreement: dashboard low but haiku high etc
print("\ncross-tab dashboard_rule_level x haiku_level:")
ct=collections.Counter((r['dashboard_rule_level'],r['haiku_level']) for r in rows)
for k in sorted(ct): print(k, ct[k])
print("\ncross-tab haiku_category x dashboard rules (top):")
for cat in ['mass_generated','registry_test_or_probe','unclear','']:
    sub=[r for r in rows if r['haiku_category']==cat]
    print(cat, len(sub), collections.Counter(rule.strip() for r in sub for rule in r['dashboard_rules'].split(';') if rule.strip()).most_common(8))
# URI: homepage empty by author, source empty by author
print("\nhomepage empty by author:", collections.Counter(r['authors_declared'] for r in rows if not r['homepage_uri']).most_common())
print("source empty by author:", collections.Counter(r['authors_declared'] for r in rows if not r['source_code_uri']).most_common())
print("homepage==source? ", sum(1 for r in rows if r['homepage_uri'] and r['homepage_uri']==r['source_code_uri']))
# deps >0 rows
print("\ndeps>0 rows:")
for r in rows:
    if r['runtime_dependencies']!='0':
        print(f"{r['name']} | {r['authors_declared']} | deps={r['runtime_dependencies']} | {r['summary']!r}")
# versions_in_window >1
print("\nmulti-version rows:", sum(1 for r in rows if r['versions_in_window']!='1'))
