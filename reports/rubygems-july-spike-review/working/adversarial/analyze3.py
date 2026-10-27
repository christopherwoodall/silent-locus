#!/usr/bin/env python3
import csv, collections, re
from pathlib import Path
SRC = Path.home()/"workspace/silent-locus/data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv"
rows = list(csv.DictReader(open(SRC, newline='', encoding='utf-8')))
out = Path.home()/"workspace/silent-locus/reports/rubygems-july-spike-review/working/adversarial"
def w(name, txt):
    (out/name).write_text(txt, encoding='utf-8'); print(name, len(txt))

# burst spans per major author
lines=[]
for a in ['Andrey78','Prvaz12_mars','tester','monib110','t','SR','T']:
    sub=sorted([r for r in rows if r['authors_declared']==a], key=lambda r: r['first_published_utc'])
    if not sub: continue
    lines.append(f"{a} n={len(sub)} first={sub[0]['first_published_utc']} last={sub[-1]['first_published_utc']} dates={dict(sorted(collections.Counter(r['first_published_utc'][:10] for r in sub).items()))} scored={sum(1 for r in sub if r['dashboard_rule_level'])} empty={sum(1 for r in sub if not r['dashboard_rule_level'])}\n")
w("burst-spans.txt","".join(lines))

# v1 medium/low rows (the exceptions)
lines=[]
for r in rows:
    if r['haiku_prompt_version']=='pkg-review-1' and r['haiku_level'] in ('medium','low'):
        lines.append(f"{r['name']} | {r['authors_declared']} | dash={r['dashboard_rule_level']} rules={r['dashboard_rules']} | haiku={r['haiku_level']}/{r['haiku_category']}/{r['haiku_agent_activity']} | {r['first_published_utc']} | summary={r['summary']!r}\n  REASON: {r['haiku_reason']}\n")
lines.append(f"\nunclear row(s):\n")
for r in rows:
    if r['haiku_category']=='unclear':
        lines.append(f"{r['name']} | {r['authors_declared']} | dash={r['dashboard_rule_level']} rules={r['dashboard_rules']} | haiku={r['haiku_level']}/{r['haiku_agent_activity']} | summary={r['summary']!r}\n  REASON: {r['haiku_reason']}\n")
w("v1-medium-low.txt","".join(lines))

# combinatorial-only Andrey78: medium vs high split by prompt/summary/source
lines=[]
for rules_label, filt in [
  ("combinatorial-only", lambda r: r['dashboard_rules']=='Group: combinatorial names'),
  ("combinatorial+shared", lambda r: r['dashboard_rules']=='Group: combinatorial names; Group: shared text'),
]:
    sub=[r for r in rows if filt(r)]
    lines.append(f"\n== {rules_label} n={len(sub)} ==\n")
    lines.append(f" haiku x prompt: {dict(collections.Counter((r['haiku_level'],r['haiku_prompt_version']) for r in sub))}\n")
    lines.append(f" haiku x author: {dict(collections.Counter((r['haiku_level'],r['authors_declared']) for r in sub))}\n")
    lines.append(f" haiku x source-empty: {dict(collections.Counter((r['haiku_level'], bool(r['source_code_uri'])) for r in sub))}\n")
    lines.append(f" haiku x version: {dict(collections.Counter((r['haiku_level'],r['latest_version']) for r in sub))}\n")
    lines.append(f" medium names: {[r['name'] for r in sub if r['haiku_level']=='medium']}\n")
    lines.append(f" low names: {[r['name'] for r in sub if r['haiku_level']=='low']}\n")
w("combinatorial-split.txt","".join(lines))

# claimed batch sizes in reasons vs file counts
lines=[]
pat=re.compile(r'(\d+)[- ]package')
claimed=collections.Counter()
for r in rows:
    for m in pat.finditer(r['haiku_reason']):
        claimed[(r['authors_declared'], int(m.group(1)))]+=1
lines.append("Claimed '<N>-package' batch sizes by declared author (from haiku_reason):\n")
for k in sorted(claimed): lines.append(f"  {k} x{claimed[k]}\n")
lines.append("\nFile totals by author: "+str(dict(collections.Counter(r['authors_declared'] for r in rows)))+"\n")
lines.append("File July-7 totals by author: "+str(dict(collections.Counter(r['authors_declared'] for r in rows if r['first_published_utc'][:10]=='2026-07-07')))+"\n")
lines.append("Tester-family July-7 (tester+Testing+Test+T+t): ")
fam=[r for r in rows if r['first_published_utc'][:10]=='2026-07-07' and r['authors_declared'] in ('tester','Testing','Test','T','t')]
lines.append(f"{len(fam)} (tester={sum(1 for r in fam if r['authors_declared']=='tester')}, Testing={sum(1 for r in fam if r['authors_declared']=='Testing')}, Test={sum(1 for r in fam if r['authors_declared']=='Test')}, T={sum(1 for r in fam if r['authors_declared']=='T')}, t={sum(1 for r in fam if r['authors_declared']=='t')})\n")
w("batch-claims.txt","".join(lines))

# likely-row column verification: homepage/source actually in CSV vs reason claims
lines=[]
for r in rows:
    if r['haiku_agent_activity']=='likely':
        lines.append(f"{r['name']} | homepage={r['homepage_uri']!r} | source={r['source_code_uri']!r} | summary={r['summary']!r}\n")
w("likely-columns.txt","".join(lines))

# source presence by author; homepage empty by author
lines=[]
for a in sorted(set(r['authors_declared'] for r in rows)):
    sub=[r for r in rows if r['authors_declared']==a]
    lines.append(f"{a!r} n={len(sub)} source_present={sum(1 for r in sub if r['source_code_uri'])} homepage_empty={sum(1 for r in sub if not r['homepage_uri'])} deps0={sum(1 for r in sub if r['runtime_dependencies']=='0')} ver001={sum(1 for r in sub if r['latest_version']=='0.0.1')}\n")
w("source-presence.txt","".join(lines))

# FP rule examples: one row per rule token with name+summary
lines=[]
tokens=['Group: combinatorial names','Group: shared text','Group: name series','Group: owner burst','Group: template batch','Package: numbered name','Package: placeholder author','Package: placeholder text','Package: probe name','Package: oob url','Package: short author','Package: test name','Package: markup','Package: placeholder link']
for tok in tokens:
    sub=[r for r in rows if tok in r['dashboard_rules'].split('; ')]
    lines.append(f"\n{tok} n={len(sub)} dash={dict(collections.Counter(r['dashboard_rule_level'] for r in sub))} haiku={dict(collections.Counter(r['haiku_level'] for r in sub))} cat={dict(collections.Counter(r['haiku_category'] for r in sub))}\n")
    for r in sub[:4]:
        lines.append(f"  e.g. {r['name']} ({r['authors_declared']}, {r['first_published_utc'][:10]}) summary={r['summary']!r} homepage={r['homepage_uri']!r}\n")
w("rule-examples.txt","".join(lines))

# verdict-subset numbers already in verdict-subsets.txt; add JFrog/GemStuffer/malware counts here compact
lines=[]
for term in ['gemstuffer','jfrog','stuffer','typosquat','malware','malicious','backdoor','dependency confusion','lookalike','deception']:
    hits=[r['name'] for r in rows if term in (r['summary']+' '+r['haiku_reason']+' '+r['dashboard_rules']).lower()]
    lines.append(f"{term!r}: {len(hits)}\n")
lines.append(f"reasons saying 'no lookalike'/'no clear deception'/'no deception': {sum(1 for r in rows if 'no lookalike' in r['haiku_reason'] or 'no clear deception' in r['haiku_reason'] or 'no deception' in r['haiku_reason'])}\n")
lines.append(f"reasons saying 'no MFA' or 'MFA off' or 'no publisher': {sum(1 for r in rows if 'no MFA' in r['haiku_reason'] or 'MFA off' in r['haiku_reason'] or 'no publisher' in r['haiku_reason'] or 'null publisher' in r['haiku_reason'])}\n")
lines.append("Columns present: "+",".join(rows[0].keys())+"\n")
lines.append("Columns for MFA/publisher/code/downloads/victims: NONE (no such column exists in the CSV header)\n")
w("verdict-terms.txt","".join(lines))
print("done")
