#!/usr/bin/env python3
import csv, re, collections, json, hashlib, sys
from pathlib import Path

SRC = Path.home()/"workspace/silent-locus/data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv"
OUT = Path.home()/"workspace/silent-locus/reports/rubygems-july-spike-review/working/linguist"
OUT.mkdir(parents=True, exist_ok=True)

rows = list(csv.DictReader(open(SRC, encoding='utf-8')))
print(f"rows={len(rows)} cols={list(rows[0].keys())}")
assert len(rows)==533

# ---- credential-shaped scan: presence/count only, never copy values ----
cred_pat = re.compile(r'(?i)(api[_-]?key|secret|token|password|passwd|aws_|sk-[A-Za-z0-9]|ghp_|github_pat_|xox[baprs]-)')
cred_hits = collections.Counter()
for r in rows:
    for k,v in r.items():
        if v and cred_pat.search(v):
            cred_hits[k]+=1
print("credential-shaped field hits (counts only):", dict(cred_hits))

# ---- authors ----
auth = collections.Counter(r['authors_declared'] for r in rows)
print("authors:", auth.most_common())

# ---- naming grammar ----
# Decompose: split on - and _, detect numeric tokens, suffixes
def template(name):
    parts = re.split(r'[-_]', name)
    out=[]
    for p in parts:
        if p.isdigit(): out.append('<N>')
        elif re.fullmatch(r'[a-z]+\d+', p): out.append('<word><N>')
        elif re.fullmatch(r'\d+[a-z]+', p): out.append('<N><word>')
        else: out.append(p)
    return '-'.join(out)

# More useful: structural shape: number of tokens, presence of digits, prefix/suffix patterns
def shape(name):
    parts = re.split(r'[-_]', name)
    toks=[]
    for p in parts:
        if p.isdigit(): toks.append('NUM')
        elif re.fullmatch(r'[a-z]+\d+', p): toks.append('WORDNUM')
        elif re.fullmatch(r'\d+[a-z]+', p): toks.append('NUMWORD')
        elif re.fullmatch(r'[a-z]+', p): toks.append('word')
        else: toks.append('OTHER:'+p)
    return '-'.join(toks)

by_author_shape = collections.defaultdict(collections.Counter)
by_author_example = collections.defaultdict(dict)
for r in rows:
    a=r['authors_declared']; s=shape(r['name'])
    by_author_shape[a][s]+=1
    by_author_example[a].setdefault(s, []).append(r['name'])

# Prefix / suffix census
prefix = collections.Counter(); suffix = collections.Counter()
for r in rows:
    parts = re.split(r'[-_]', r['name'])
    prefix[parts[0]]+=1
    suffix[parts[-1]]+=1

# Numbered names: trailing digits, embedded digits
num_end = [r['name'] for r in rows if re.search(r'\d+$', r['name'])]
num_any = [r['name'] for r in rows if re.search(r'\d', r['name'])]
print(f"names with any digit: {len(num_any)}, trailing digit: {len(num_end)}")

# Token vocab
vocab = collections.Counter()
for r in rows:
    for p in re.split(r'[-_]', r['name']):
        vocab[re.sub(r'\d+','N',p)]+=1

# ---- summaries ----
summ = collections.Counter(r['summary'] for r in rows)
summ_by_author = collections.defaultdict(collections.Counter)
for r in rows:
    summ_by_author[r['authors_declared']][r['summary']]+=1

# summary shapes
def summ_shape(s):
    if s=='' : return '<EMPTY>'
    if re.fullmatch(r'[A-Za-z ]+ based on [A-Za-z0-9_\-\.]+', s): return 'University research based on X'
    if s.lower() in ('test','testing','test test','hello','hi','asdf','aaa','xxx'): return 'bare placeholder word'
    return 'other'
summ_shape_c = collections.Counter(summ_shape(r['summary']) for r in rows)
summ_shape_by_author = collections.defaultdict(collections.Counter)
for r in rows:
    summ_shape_by_author[r['authors_declared']][summ_shape(r['summary'])]+=1

# repeated summaries across authors?
summ_authors = collections.defaultdict(set)
for r in rows:
    summ_authors[r['summary']].add(r['authors_declared'])
shared_summ = {s:a for s,a in summ_authors.items() if len(a)>1}

# ---- haiku reasons ----
reasons = collections.Counter(r['haiku_reason'] for r in rows)
print(f"distinct haiku_reason strings: {len(reasons)}")
print(f"empty reasons: {sum(1 for r in rows if not r['haiku_reason'])}")
# dashboard rules
rules = collections.Counter()
for r in rows:
    for rule in r['dashboard_rules'].split(';'):
        rule=rule.strip()
        if rule: rules[rule]+=1
print("dashboard_rules:", rules.most_common())
print("haiku_category:", collections.Counter(r['haiku_category'] for r in rows).most_common())
print("haiku_agent_activity:", collections.Counter(r['haiku_agent_activity'] for r in rows).most_common())
print("haiku_prompt_version:", collections.Counter(r['haiku_prompt_version'] for r in rows).most_common())
print("haiku_level:", collections.Counter(r['haiku_level'] for r in rows).most_common())
print("dashboard_rule_level:", collections.Counter(r['dashboard_rule_level'] for r in rows).most_common())
print("withdrawn:", collections.Counter(r['withdrawn'] for r in rows).most_common())
print("latest_version:", collections.Counter(r['latest_version'] for r in rows).most_common())
print("versions_in_window:", collections.Counter(r['versions_in_window'] for r in rows).most_common())
print("date range:", min(r['first_published_utc'] for r in rows), max(r['last_published_utc'] for r in rows))

# URI shapes
def uri_shape(u):
    if not u: return '<EMPTY>'
    u=re.sub(r'https?://','',u)
    parts=u.split('/')
    return '/'.join(parts[:2]) + ('/<...>' if len(parts)>2 else '')
hp = collections.Counter(uri_shape(r['homepage_uri']) for r in rows)
sc = collections.Counter(uri_shape(r['source_code_uri']) for r in rows)
# does source repo name match package name?
match = sum(1 for r in rows if r['source_code_uri'].rstrip('/').split('/')[-1]==r['name'])
hp_match_profile = sum(1 for r in rows if r['homepage_uri'].rstrip('/').split('/')[-1]==r['authors_declared'])
print("source repo == pkg name:", match, "homepage profile == author:", hp_match_profile)
print("homepage shapes:", hp.most_common(20))
print("source shapes:", sc.most_common(20))
print("runtime_dependencies:", collections.Counter(r['runtime_dependencies'] for r in rows).most_common(20))

# save raw tallies
data = {
 'rows': len(rows),
 'authors': auth.most_common(),
 'by_author_shape': {a: c.most_common() for a,c in by_author_shape.items()},
 'by_author_examples': {a: {s: v[:8] for s,v in d.items()} for a,d in by_author_example.items()},
 'prefix_top': prefix.most_common(60),
 'suffix_top': suffix.most_common(60),
 'vocab_top': vocab.most_common(120),
 'num_any': len(num_any), 'num_trailing': len(num_end),
 'summary_distinct': len(summ),
 'summary_top': summ.most_common(60),
 'summary_by_author_top': {a: c.most_common(25) for a,c in summ_by_author.items()},
 'summary_shapes': summ_shape_c.most_common(),
 'summary_shapes_by_author': {a: c.most_common() for a,c in summ_shape_by_author.items()},
 'shared_summaries_across_authors': {s: sorted(a) for s,a in shared_summ.items()},
 'empty_summaries': sum(1 for r in rows if not r['summary']),
 'distinct_reasons': len(reasons),
 'reason_top': reasons.most_common(40),
 'dashboard_rules': rules.most_common(),
 'haiku_category': collections.Counter(r['haiku_category'] for r in rows).most_common(),
 'haiku_agent_activity': collections.Counter(r['haiku_agent_activity'] for r in rows).most_common(),
 'haiku_prompt_version': collections.Counter(r['haiku_prompt_version'] for r in rows).most_common(),
 'haiku_level': collections.Counter(r['haiku_level'] for r in rows).most_common(),
 'dashboard_rule_level': collections.Counter(r['dashboard_rule_level'] for r in rows).most_common(),
 'credential_shaped_field_counts': dict(cred_hits),
 'homepage_shapes': hp.most_common(20),
 'source_shapes': sc.most_common(20),
 'source_repo_eq_name': match,
 'homepage_profile_eq_author': hp_match_profile,
 'runtime_deps': collections.Counter(r['runtime_dependencies'] for r in rows).most_common(20),
 'latest_version': collections.Counter(r['latest_version'] for r in rows).most_common(),
 'versions_in_window': collections.Counter(r['versions_in_window'] for r in rows).most_common(),
 'date_min': min(r['first_published_utc'] for r in rows),
 'date_max': max(r['last_published_utc'] for r in rows),
}
json.dump(data, open(OUT/'tallies.json','w'), indent=1, ensure_ascii=False)
# dump all distinct reasons + summaries to files for verbatim quoting
with open(OUT/'distinct_reasons.txt','w') as f:
    for reason,c in reasons.most_common():
        f.write(f"[{c}x] {reason}\n---\n")
with open(OUT/'distinct_summaries.txt','w') as f:
    for s,c in summ.most_common():
        f.write(f"[{c}x] {s!r}\n")
with open(OUT/'all_names_by_author.txt','w') as f:
    for a in sorted(auth):
        f.write(f"\n== {a} ({auth[a]}) ==\n")
        for r in rows:
            if r['authors_declared']==a:
                f.write(f"{r['name']}\t{r['summary']}\t{r['haiku_category']}\n")
print("written tallies + distinct lists")
