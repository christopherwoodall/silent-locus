#!/usr/bin/env python3
"""Adversarial recomputation for rubygems-july-2026-spike-operator-20261027.csv
Read-only on source CSV. All outputs to stdout / analysis files in this dir.
"""
import csv, collections, re, json, statistics
from pathlib import Path
SRC = Path.home()/"workspace/silent-locus/data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv"
rows = list(csv.DictReader(open(SRC, newline='', encoding='utf-8')))
print(f"ROWS={len(rows)} COLS={list(rows[0].keys())}")
for c in rows[0].keys():
    vals = collections.Counter(r[c] for r in rows)
    print(f"\n== {c} distinct={len(vals)} ==")
    for v,n in vals.most_common(30):
        print(f"  {n:4d}  {v!r}")

# empty-49 subset
empty = [r for r in rows if not r['dashboard_rule_level'] and not r['haiku_level']]
print(f"\nEMPTY49 check: n={len(empty)} all-empty-cols? ", {c: len(set(r[c] for r in empty)) for c in ['dashboard_rule_level','dashboard_rules','haiku_level','haiku_score','haiku_category','haiku_agent_activity','haiku_prompt_version','haiku_reason']})
print("empty names sample:", [r['name'] for r in empty[:60]])
print("empty authors:", collections.Counter(r['authors_declared'] for r in empty))
print("empty dates:", collections.Counter(r['first_published_utc'][:10] for r in empty))
print("empty withdrawn:", collections.Counter(r['withdrawn'] for r in empty))

nonempty = [r for r in rows if r['dashboard_rule_level'] or r['haiku_level']]
print(f"\nNONEMPTY={len(nonempty)}")

# haiku_score numeric?
scores=[]
bad=[]
for r in rows:
    s=r['haiku_score'].strip()
    if s=='':
        continue
    try: scores.append(float(s))
    except: bad.append((r['name'],s))
print(f"haiku_score numeric n={len(scores)} bad={bad[:10]} min={min(scores) if scores else None} max={max(scores) if scores else None}")
# score by level
for lvl in sorted(set(r['haiku_level'] for r in rows)):
    ss=[float(r['haiku_score']) for r in rows if r['haiku_level']==lvl and r['haiku_score'].strip()!='']
    if ss: print(f" haiku_level={lvl!r} n={len(ss)} min={min(ss)} max={max(ss)} mean={statistics.mean(ss):.2f} median={statistics.median(ss)}")
    else: print(f" haiku_level={lvl!r} n=0 scores")
# monotonic check: sort by score, level sequence
by_score=sorted([r for r in rows if r['haiku_score'].strip()!=''], key=lambda r: float(r['haiku_score']))
print("\nScore->level boundary scan (lowest 15, highest 15):")
for r in by_score[:15]: print(f"  {r['haiku_score']} {r['haiku_level']} {r['name']} {r['haiku_category']}")
for r in by_score[-15:]: print(f"  {r['haiku_score']} {r['haiku_level']} {r['name']} {r['haiku_category']}")
# overlaps: does any score value appear under 2+ levels?
byval=collections.defaultdict(set)
for r in rows:
    if r['haiku_score'].strip(): byval[r['haiku_score']].add(r['haiku_level'])
overlap={k:v for k,v in byval.items() if len(v)>1}
print(f"\nScore values shared across levels: {len(overlap)} values, e.g. {dict(list(overlap.items())[:20])}")
# level order assumed low<medium<high<critical? check inversions
order={'low':0,'medium':1,'high':2,'critical':3}
inversions=0
for a,b in zip(by_score, by_score[1:]):
    if order.get(a['haiku_level'],99) > order.get(b['haiku_level'],99): inversions+=1
print(f"adjacent score-order inversions (level drops as score rises): {inversions} / {len(by_score)-1}")
# dashboard level vs haiku level crosstab
print("\nDashboard x Haiku crosstab:")
ct=collections.Counter((r['dashboard_rule_level'],r['haiku_level']) for r in rows)
for k in sorted(ct): print(f"  {k} {ct[k]}")
# dashboard rules breakdown (split on ';' ? inspect separators)
print("\nDashboard rules raw distinct (top 40):")
for v,n in collections.Counter(r['dashboard_rules'] for r in rows).most_common(40): print(f"  {n:4d} {v!r}")
# prompt version
print("\nPrompt x level/category/activity:")
for pv in sorted(set(r['haiku_prompt_version'] for r in rows)):
    sub=[r for r in rows if r['haiku_prompt_version']==pv]
    print(f" {pv!r} n={len(sub)} levels={collections.Counter(r['haiku_level'] for r in sub)} cat={collections.Counter(r['haiku_category'] for r in sub)} act={collections.Counter(r['haiku_agent_activity'] for r in sub)} scores={[r['haiku_score'] for r in sub][:5]}")
    print(f"   score stats: {[float(r['haiku_score']) for r in sub if r['haiku_score'].strip()!=''][:0]} min/max/mean:", end=' ')
    ss=[float(r['haiku_score']) for r in sub if r['haiku_score'].strip()!='']
    print(f"{min(ss) if ss else None}/{max(ss) if ss else None}/{round(statistics.mean(ss),2) if ss else None}")
    print(f"   authors={collections.Counter(r['authors_declared'] for r in sub)}")
    print(f"   rules={collections.Counter(r['dashboard_rules'] for r in sub)}")
# v2 rows full dump
print("\n=== PROMPT V2 ROWS (full) ===")
for r in rows:
    if r['haiku_prompt_version']=='pkg-review-2':
        print(f"{r['name']} | author={r['authors_declared']} | dash={r['dashboard_rule_level']}/{r['dashboard_rules']} | haiku={r['haiku_level']}/{r['haiku_score']}/{r['haiku_category']}/{r['haiku_agent_activity']} | ver={r['latest_version']} nver={r['versions_in_window']} first={r['first_published_utc']} summary={r['summary']!r} | reason={r['haiku_reason']!r}")

# likely rows full dump
print("\n=== LIKELY ROWS (full) ===")
for r in rows:
    if r['haiku_agent_activity']=='likely':
        print(f"{r['name']} | author={r['authors_declared']} | dash={r['dashboard_rule_level']}/{r['dashboard_rules']} | haiku={r['haiku_level']}/{r['haiku_score']}/{r['haiku_category']} | prompt={r['haiku_prompt_version']} | ver={r['latest_version']} nver={r['versions_in_window']} first={r['first_published_utc']} summary={r['summary']!r} homepage={r['homepage_uri']!r} source={r['source_code_uri']!r} deps={r['runtime_dependencies']} | reason={r['haiku_reason']!r}")

# possible / no_sign
print("\nno_sign rows:")
for r in rows:
    if r['haiku_agent_activity']=='no_sign':
        print(f" {r['name']} | {r['authors_declared']} | {r['haiku_level']}/{r['haiku_score']}/{r['haiku_category']} | {r['dashboard_rules']} | reason={r['haiku_reason']!r}")

# identical-shape consistency: group by (author, summary-pattern?, version, deps, rule?) — test shape keys
def shape_keys():
    return {
      'author+version+deps+summary': lambda r:(r['authors_declared'],r['latest_version'],r['runtime_dependencies'],r['summary']),
      'author+version+deps': lambda r:(r['authors_declared'],r['latest_version'],r['runtime_dependencies']),
      'summary-only': lambda r:(r['summary'],),
      'author+rule': lambda r:(r['authors_declared'],r['dashboard_rules']),
      'rule-only': lambda r:(r['dashboard_rules'],),
    }
for kname, kf in shape_keys().items():
    groups=collections.defaultdict(list)
    for r in nonempty: groups[kf(r)].append(r)
    multi={k:v for k,v in groups.items() if len(v)>1}
    inconsistent=0; examples=[]
    for k,v in multi.items():
        lv=set(x['haiku_level'] for x in v); sc=set(x['haiku_score'] for x in v); cat=set(x['haiku_category'] for x in v); act=set(x['haiku_agent_activity'] for x in v); dl=set(x['dashboard_rule_level'] for x in v)
        if len(lv)>1 or len(cat)>1 or len(act)>1 or len(dl)>1:
            inconsistent+=1
            if len(examples)<12: examples.append((k,[(x['name'],x['dashboard_rule_level'],x['haiku_level'],x['haiku_score'],x['haiku_category'],x['haiku_agent_activity']) for x in v[:8]]))
    print(f"\nSHAPE {kname}: groups>1={len(multi)} inconsistent(level/cat/act/dash)={inconsistent}")
    for k,ex in examples: print(f"  key={k!r} -> {ex}")

# identical names? duplicate names?
print("\nDuplicate names:", [k for k,n in collections.Counter(r['name'] for r in rows).items() if n>1])
# versions_in_window, withdrawn, deps, versions
print("\nversions_in_window:", collections.Counter(r['versions_in_window'] for r in rows))
print("withdrawn:", collections.Counter(r['withdrawn'] for r in rows))
print("latest_version:", collections.Counter(r['latest_version'] for r in rows).most_common(10))
print("deps:", collections.Counter(r['runtime_dependencies'] for r in rows).most_common(10))
print("authors x dashboard level:")
for a in sorted(set(r['authors_declared'] for r in rows)):
    sub=[r for r in rows if r['authors_declared']==a]
    print(f" {a!r} n={len(sub)} dash={dict(collections.Counter(r['dashboard_rule_level'] for r in sub))} haiku={dict(collections.Counter(r['haiku_level'] for r in sub))} cat={dict(collections.Counter(r['haiku_category'] for r in sub))} act={dict(collections.Counter(r['haiku_agent_activity'] for r in sub))} prompt={dict(collections.Counter(r['haiku_prompt_version'] for r in sub))}")
# dates
print("\nBy date:", collections.Counter(r['first_published_utc'][:10] for r in rows))
print("By date x author (top):")
for d in sorted(set(r['first_published_utc'][:10] for r in rows)):
    sub=[r for r in rows if r['first_published_utc'][:10]==d]
    print(f" {d} n={len(sub)} {dict(collections.Counter(r['authors_declared'] for r in sub))}")
# MFA / publisher claims inside reasons: count mentions (dashboard prose claims not in columns)
for term in ['MFA','publisher handle','no MFA','zero dep','0 dep','placeholder','template','agent','AI','LLM','Claude','GPT','script','automated','bot']:
    hits=[r['name'] for r in rows if term.lower() in r['haiku_reason'].lower()]
    print(f" reason-mentions {term!r}: {len(hits)} e.g. {hits[:5]}")
# summaries patterns
print("\nSummary distinct top 30:")
for v,n in collections.Counter(r['summary'] for r in rows).most_common(30): print(f"  {n:4d} {v!r}")
print("\nSummary prefixes:")
for v,n in collections.Counter(r['summary'].split(' based on ')[0] if ' based on ' in r['summary'] else r['summary'][:40] for r in rows).most_common(20): print(f"  {n:4d} {v!r}")
# homepage/source patterns
print("\nHomepage distinct top:", collections.Counter(r['homepage_uri'] for r in rows).most_common(10))
print("Source host patterns:", collections.Counter(r['source_code_uri'].split('/')[2] if '://' in r['source_code_uri'] else r['source_code_uri'] for r in rows).most_common(10))
# credential-shaped scan: report counts only, no values
cred_re = re.compile(r'(?i)(api[_-]?key|secret|token|password|passwd|pwd|aws_|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,})')
hits=[]
for r in rows:
    for c in ['name','summary','homepage_uri','source_code_uri','haiku_reason','dashboard_rules']:
        if cred_re.search(r[c] or ''): hits.append((r['name'],c))
print(f"\nCredential-shaped regex hits (count only): {len(hits)} {hits[:10]}")
# Also generic high-entropy token-ish in summary/reason? just count long alnum tokens
tok_re=re.compile(r'[A-Za-z0-9_\-]{32,}')
th=[r['name'] for r in rows if tok_re.search(r['summary'] or '') or tok_re.search(r['haiku_reason'] or '')]
print(f"Long-token (>=32 chars) in summary/reason: {len(th)} {th[:10]}")
# reason length / emptiness / templating: identical reasons?
print("\nIdentical haiku_reason values:", [(n, v[:80]) for v,n in collections.Counter(r['haiku_reason'] for r in rows).most_common(10)])
print("Reason word-count stats nonempty:", end=' ')
rc=[len(r['haiku_reason'].split()) for r in nonempty]
print(f"min={min(rc)} max={max(rc)} mean={statistics.mean(rc):.1f}")
# v1 vs v2 reason style: does v2 mention agent evidence differently?
# Check dashboard critical rows: what rules drive critical?
print("\nDashboard critical by rule:")
for v,n in collections.Counter(r['dashboard_rules'] for r in rows if r['dashboard_rule_level']=='critical').most_common(20): print(f"  {n:4d} {v!r}")
print("\nDashboard high by rule:")
for v,n in collections.Counter(r['dashboard_rules'] for r in rows if r['dashboard_rule_level']=='high').most_common(20): print(f"  {n:4d} {v!r}")
print("\nHaiku critical by category/rule:")
for v,n in collections.Counter((r['haiku_category'],r['dashboard_rules']) for r in rows if r['haiku_level']=='critical').most_common(20): print(f"  {n:4d} {v!r}")
print("\nHaiku high by category:")
print(collections.Counter(r['haiku_category'] for r in rows if r['haiku_level']=='high'))
print("Haiku medium/low by category:")
print(" medium:", collections.Counter(r['haiku_category'] for r in rows if r['haiku_level']=='medium'))
print(" low:", collections.Counter(r['haiku_category'] for r in rows if r['haiku_level']=='low'))
# name-pattern analysis for FP: numbered names, probe names
numre=re.compile(r'-\d+$|_\d+$|\d{2,}$')
print(f"\nNumbered-name pattern rows: {sum(1 for r in rows if numre.search(r['name']))}")
print("Probe-like names (probe/test/demo/sample/hello/example):", [r['name'] for r in rows if re.search(r'probe|test|demo|sample|hello|example', r['name'])][:40])
