#!/usr/bin/env python3
import csv, collections
from pathlib import Path
SRC = Path.home()/"workspace/silent-locus/data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv"
rows = list(csv.DictReader(open(SRC, newline='', encoding='utf-8')))
out = Path.home()/"workspace/silent-locus/reports/rubygems-july-spike-review/working/adversarial"
def w(name, txt):
    (out/name).write_text(txt, encoding='utf-8'); print(name, len(txt))

# --- v2 rows compact
lines=[]
for r in rows:
    if r['haiku_prompt_version']=='pkg-review-2':
        lines.append(f"{r['name']} | {r['authors_declared']} | dash={r['dashboard_rule_level']} | rules={r['dashboard_rules']} | haiku={r['haiku_level']}/{r['haiku_score']}/{r['haiku_category']}/{r['haiku_agent_activity']} | {r['first_published_utc']} | summary={r['summary']!r}\n  REASON: {r['haiku_reason']}\n")
w("v2-rows.txt", "".join(lines))

# --- likely rows compact
lines=[]
for r in rows:
    if r['haiku_agent_activity']=='likely':
        lines.append(f"{r['name']} | {r['authors_declared']} | dash={r['dashboard_rule_level']} | rules={r['dashboard_rules']} | haiku={r['haiku_level']}/{r['haiku_score']}/{r['haiku_category']} | prompt={r['haiku_prompt_version']} | {r['first_published_utc']} | ver={r['latest_version']} nver={r['versions_in_window']} deps={r['runtime_dependencies']} | summary={r['summary']!r}\n  REASON: {r['haiku_reason']}\n")
w("likely-rows.txt", "".join(lines))

# --- prompt comparison compact
lines=[]
for pv in ['pkg-review-1','pkg-review-2','']:
    sub=[r for r in rows if r['haiku_prompt_version']==pv]
    lines.append(f"{pv!r} n={len(sub)}\n  dash={dict(collections.Counter(r['dashboard_rule_level'] for r in sub))}\n  haiku={dict(collections.Counter(r['haiku_level'] for r in sub))}\n  cat={dict(collections.Counter(r['haiku_category'] for r in sub))}\n  act={dict(collections.Counter(r['haiku_agent_activity'] for r in sub))}\n  authors={dict(collections.Counter(r['authors_declared'] for r in sub))}\n  dates={dict(sorted(collections.Counter(r['first_published_utc'][:10] for r in sub).items()))}\n")
w("prompt-compare.txt", "".join(lines))

# --- dashboard level vs rule-count (does more rules = higher level?)
lines=[]
for r in rows:
    pass
import statistics
for lvl in ['low','medium','high','critical']:
    sub=[r for r in rows if r['dashboard_rule_level']==lvl]
    counts=[len(r['dashboard_rules'].split(';')) if r['dashboard_rules'] else 0 for r in sub]
    lines.append(f"dash {lvl} n={len(sub)} rulecount min={min(counts)} max={max(counts)} mean={statistics.mean(counts):.2f} dist={dict(sorted(collections.Counter(counts).items()))}\n")
for lvl in ['low','medium','high','critical']:
    sub=[r for r in rows if r['haiku_level']==lvl]
    counts=[len(r['dashboard_rules'].split(';')) if r['dashboard_rules'] else 0 for r in sub]
    lines.append(f"haiku {lvl} n={len(sub)} rulecount min={min(counts)} max={max(counts)} mean={statistics.mean(counts):.2f} dist={dict(sorted(collections.Counter(counts).items()))}\n")
# same rule string, different dashboard levels
groups=collections.defaultdict(list)
for r in rows:
    if r['dashboard_rules']: groups[r['dashboard_rules']].append(r)
lines.append("\nSame dashboard_rules string -> different dashboard_rule_level:\n")
for k,v in groups.items():
    lv=set(x['dashboard_rule_level'] for x in v)
    if len(lv)>1:
        lines.append(f"  n={len(v)} levels={lv} rules={k!r} names={[x['name'] for x in v]}\n")
lines.append("\nSame dashboard_rules string -> different haiku_level (v1 only, score blank):\n")
for k,v in groups.items():
    lv=set(x['haiku_level'] for x in v)
    if len(lv)>1:
        lines.append(f"  n={len(v)} haiku_levels={lv} dash_levels={set(x['dashboard_rule_level'] for x in v)} rules={k!r} names={[x['name'] for x in v][:10]}\n")
w("rule-level-consistency.txt", "".join(lines))

# --- identical summary+author+version+deps but different haiku level (concise, names only)
lines=[]
def check(keyfn, label):
    g=collections.defaultdict(list)
    for r in rows:
        if r['dashboard_rule_level']: g[keyfn(r)].append(r)
    lines.append(f"\n== {label} ==\n")
    for k,v in g.items():
        if len(v)>1 and len(set(x['haiku_level'] for x in v))>1:
            lines.append(f"key={k!r}\n")
            for x in v: lines.append(f"  {x['name']} dash={x['dashboard_rule_level']} haiku={x['haiku_level']} cat={x['haiku_category']} act={x['haiku_agent_activity']} prompt={x['haiku_prompt_version']} rules={x['dashboard_rules']!r}\n")
check(lambda r:(r['authors_declared'],r['latest_version'],r['runtime_dependencies'],r['summary']), "author+version+deps+summary, haiku differs")
check(lambda r:(r['summary'],), "summary only, haiku differs (first 30 groups)")
w("shape-inconsistencies.txt", "".join(lines))

# --- empty49 compact table
lines=[]
for r in rows:
    if not r['dashboard_rule_level']:
        lines.append(f"{r['name']} | {r['authors_declared']} | {r['first_published_utc']} | ver={r['latest_version']} | summary={r['summary']!r}\n")
w("empty49.txt", "".join(lines))

# --- agent-activity: what distinguishes likely? word scan of likely vs possible reasons
lines=[]
likely=[r for r in rows if r['haiku_agent_activity']=='likely']
possible=[r for r in rows if r['haiku_agent_activity']=='possible']
for term in ['agent','automated','script','AI-generated','AI ','LLM','bot','tool','harness','model','Claude','GPT','autonomous','programmatic','bulk','batch','template']:
    lines.append(f"{term!r}: likely {sum(1 for r in likely if term.lower() in r['haiku_reason'].lower())}/{len(likely)}  possible {sum(1 for r in possible if term.lower() in r['haiku_reason'].lower())}/{len(possible)}\n")
lines.append(f"\nlikely by author: {dict(collections.Counter(r['authors_declared'] for r in likely))}\n")
lines.append(f"likely by category: {dict(collections.Counter(r['haiku_category'] for r in likely))}\n")
lines.append(f"likely by haiku level: {dict(collections.Counter(r['haiku_level'] for r in likely))}\n")
lines.append(f"likely by dash level: {dict(collections.Counter(r['dashboard_rule_level'] for r in likely))}\n")
lines.append(f"likely by prompt: {dict(collections.Counter(r['haiku_prompt_version'] for r in likely))}\n")
lines.append(f"likely by date: {dict(sorted(collections.Counter(r['first_published_utc'][:10] for r in likely).items()))}\n")
lines.append(f"no_sign rows: {[(r['name'],r['haiku_level'],r['haiku_category']) for r in rows if r['haiku_agent_activity']=='no_sign']}\n")
w("agent-activity-stats.txt", "".join(lines))

# --- July-7 subset (for verdict-change test) + Andrey78 + JFrog-ish terms
lines=[]
for d in ['2026-07-07']:
    sub=[r for r in rows if r['first_published_utc'][:10]==d]
    lines.append(f"July7 n={len(sub)} authors={dict(collections.Counter(r['authors_declared'] for r in sub))} dash={dict(collections.Counter(r['dashboard_rule_level'] for r in sub))} haiku={dict(collections.Counter(r['haiku_level'] for r in sub))} cat={dict(collections.Counter(r['haiku_category'] for r in sub))} act={dict(collections.Counter(r['haiku_agent_activity'] for r in sub))}\n")
    lines.append("July7 names: "+", ".join(r['name'] for r in sub)+"\n")
for a in ['Andrey78']:
    sub=[r for r in rows if r['authors_declared']==a]
    lines.append(f"\nAndrey78 n={len(sub)} dates={dict(sorted(collections.Counter(r['first_published_utc'][:10] for r in sub).items()))} dash={dict(collections.Counter(r['dashboard_rule_level'] for r in sub))} haiku={dict(collections.Counter(r['haiku_level'] for r in sub))} cat={dict(collections.Counter(r['haiku_category'] for r in sub))} act={dict(collections.Counter(r['haiku_agent_activity'] for r in sub))} rules={dict(collections.Counter(r['dashboard_rules'] for r in sub))}\n")
# JFrog / GemStuffer terms in file?
for term in ['gemstuffer','jfrog','stuffer','typosquat','malware','malicious','dependency confusion','backdoor']:
    hits=[r['name'] for r in rows if term in (r['summary']+r['haiku_reason']+r['dashboard_rules']).lower()]
    lines.append(f"term {term!r}: {len(hits)} {hits[:10]}\n")
# oob url rows: what are they?
oob=[r for r in rows if 'oob url' in r['dashboard_rules']]
lines.append(f"\noob-url rows n={len(oob)}: "+", ".join(r['name'] for r in oob)+"\n")
lines.append(f"oob homepages: {dict(collections.Counter(r['homepage_uri'] for r in oob))}\n")
w("verdict-subsets.txt", "".join(lines))
print("done")
