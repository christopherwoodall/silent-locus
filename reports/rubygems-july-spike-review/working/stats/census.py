import csv, json, re, collections, statistics
from datetime import datetime
from pathlib import Path
SRC = Path.home()/"workspace/silent-locus/data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv"
OUT = Path.home()/"workspace/silent-locus/reports/rubygems-july-spike-review/working/stats"
OUT.mkdir(parents=True, exist_ok=True)
rows = list(csv.DictReader(open(SRC, newline='', encoding='utf-8')))
cols = rows[0].keys() if rows else []
print(f"ROWS={len(rows)} COLS={list(cols)}")
def is_empty(v): return v is None or v.strip()==''
def parse_dt(s):
    try: return datetime.strptime(s.strip(), "%Y-%m-%d %H:%M:%S")
    except: return None
out={}
out['total_rows']=len(rows)
# 1 per-column
schema=[]
for c in cols:
    vals=[r[c] for r in rows]
    empty=sum(1 for v in vals if is_empty(v))
    distinct=len(set(v for v in vals if not is_empty(v)))
    distinct_all=len(set(vals))
    entry={'column':c,'distinct_nonempty':distinct,'distinct_incl_empty':distinct_all,'empty':empty,'nonempty':len(rows)-empty}
    # numeric attempt
    nums=[]
    for v in vals:
        if is_empty(v): continue
        try: nums.append(float(v))
        except: pass
    if nums and len(nums)==len(rows)-empty:
        entry['numeric']={'min':min(nums),'max':max(nums),'mean':statistics.mean(nums),'median':statistics.median(nums)}
    schema.append(entry)
    print(c, entry)
out['schema']=schema
# categorical distributions
cats=['authors_declared','withdrawn','dashboard_rule_level','dashboard_rules','haiku_level','haiku_category','haiku_agent_activity','haiku_prompt_version','latest_version','runtime_dependencies','versions_in_window']
dists={}
for c in cats:
    cnt=collections.Counter(r[c] for r in rows)
    dists[c]=cnt.most_common()
    print(f"\n== {c} ==")
    for k,v in cnt.most_common(): print(repr(k),v)
out['distributions']={k:v for k,v in dists.items()}
# numeric ranges detail
for c in ['haiku_score','versions_in_window']:
    vals=[]
    for r in rows:
        if not is_empty(r[c]):
            try: vals.append(float(r[c]))
            except: pass
    print(f"\n{c}: n={len(vals)} min={min(vals)} max={max(vals)} mean={statistics.mean(vals):.4f} median={statistics.median(vals)} stdev={statistics.pstdev(vals):.4f} empty={sum(1 for r in rows if is_empty(r[c]))}")
    # histogram for versions
    print(collections.Counter(vals).most_common())
    out[c+'_stats']={'n':len(vals),'min':min(vals),'max':max(vals),'mean':statistics.mean(vals),'median':statistics.median(vals),'stdev':statistics.pstdev(vals),'counter':{str(k):v for k,v in collections.Counter(vals).most_common()}}
# haiku_score distribution binned / exact if few
hs=[r['haiku_score'] for r in rows]
print("haiku_score raw counter:", collections.Counter(hs).most_common())
out['haiku_score_raw_counter']=collections.Counter(hs).most_common()
# other columns distinct counts + samples for free text
for c in ['name','summary','homepage_uri','source_code_uri','haiku_reason','doc_id','first_published_utc','last_published_utc']:
    vals=[r[c] for r in cols and rows] if False else [r[c] for r in rows]
    print(f"\n{c}: distinct={len(set(vals))} empty={sum(1 for v in vals if is_empty(v))}")
    if c in ('summary','homepage_uri','source_code_uri','haiku_reason'):
        print(collections.Counter(vals).most_common(20))
        out[c+'_top20']=collections.Counter(vals).most_common(20)
# 2 per-author
authors={}
for r in rows:
    authors.setdefault(r['authors_declared'],[]).append(r)
batch=[]
for a,rs in sorted(authors.items(), key=lambda x:-len(x[1])):
    firsts=sorted(parse_dt(r['first_published_utc']) for r in rs if parse_dt(r['first_published_utc']))
    lasts=sorted(parse_dt(r['last_published_utc']) for r in rs if parse_dt(r['last_published_utc']))
    days=collections.Counter(d.strftime('%Y-%m-%d') for d in firsts)
    hours=collections.Counter(d.strftime('%Y-%m-%d %H') for d in firsts)
    # gaps between sorted firsts in seconds
    gaps=[(firsts[i+1]-firsts[i]).total_seconds() for i in range(len(firsts)-1)]
    # tightest cluster: max count in any 60min / 10min sliding window
    def maxwin(window_s):
        best=0; best_start=None; j=0
        for i, t in enumerate(firsts):
            while (t-firsts[j]).total_seconds()>window_s: j+=1
            if i-j+1>best: best=i-j+1; best_start=firsts[j]
        return best, str(best_start) if best_start else None
    w60, s60 = maxwin(3600); w10, s10 = maxwin(600); w5, s5 = maxwin(300)
    name_lens=[len(r['name']) for r in rs]
    entry={'author':a,'n':len(rs),'first':str(firsts[0]) if firsts else None,'last_first':str(firsts[-1]) if firsts else None,
           'last_published_max':str(max(lasts)) if lasts else None,'span_days':(firsts[-1]-firsts[0]).total_seconds()/86400 if firsts else None,
           'per_day':dict(sorted(days.items())),'per_hour_top':collections.Counter(d.strftime('%H') for d in firsts).most_common(),
           'per_dayhour':dict(sorted(hours.items())),
           'gap_min_s':min(gaps) if gaps else None,'gap_median_s':statistics.median(gaps) if gaps else None,'gap_mean_s':statistics.mean(gaps) if gaps else None,
           'gaps_under_60s':sum(1 for g in gaps if g<60),'gaps_under_300s':sum(1 for g in gaps if g<300),'gaps_under_3600s':sum(1 for g in gaps if g<3600),
           'max_in_60min':w60,'max_in_60min_start':s60,'max_in_10min':w10,'max_in_10min_start':s10,'max_in_5min':w5,'max_in_5min_start':s5,
           'name_len_min':min(name_lens),'name_len_max':max(name_lens),'name_len_mean':round(statistics.mean(name_lens),2),
           'single_version_rows':sum(1 for r in rs if r['versions_in_window']=='1'),'multi_version_rows':sum(1 for r in rs if r['versions_in_window']!='1'),
           'first_eq_last':sum(1 for r in rs if r['first_published_utc']==r['last_published_utc'])}
    batch.append(entry); print(entry)
out['per_author']=batch
# overall timing
allfirst=sorted(parse_dt(r['first_published_utc']) for r in rows)
print("\nOVERALL first:", allfirst[0], "last:", allfirst[-1])
print("per_day overall:", sorted(collections.Counter(d.strftime('%Y-%m-%d') for d in allfirst).items()))
print("per_hour_of_day overall:", sorted(collections.Counter(d.strftime('%H') for d in allfirst).items()))
out['overall_per_day']=dict(sorted(collections.Counter(d.strftime('%Y-%m-%d') for d in allfirst).items()))
out['overall_per_hour']=dict(sorted(collections.Counter(d.strftime('%H') for d in allfirst).items()))
# name length overall + pattern counts (counts only)
lens=[len(r['name']) for r in rows]
print(f"name len min {min(lens)} max {max(lens)} mean {statistics.mean(lens):.2f} median {statistics.median(lens)} dist {sorted(collections.Counter(lens).items())}")
out['name_len']={'min':min(lens),'max':max(lens),'mean':statistics.mean(lens),'median':statistics.median(lens),'counter':dict(sorted(collections.Counter(lens).items()))}
print("names with digits:", sum(1 for r in rows if any(ch.isdigit() for ch in r['name'])))
print("names with hyphen count dist:", collections.Counter(r['name'].count('-') for r in rows))
print("names with underscore:", sum(1 for r in rows if '_' in r['name']))
out['name_patterns']={'with_digit':sum(1 for r in rows if any(ch.isdigit() for ch in r['name'])),'hyphen_counter':dict(collections.Counter(r['name'].count('-') for r in rows)),'with_underscore':sum(1 for r in rows if '_' in r['name'])}
# 3 versions
print("\nlatest_version:", collections.Counter(r['latest_version'] for r in rows).most_common())
print("versions_in_window:", collections.Counter(r['versions_in_window'] for r in rows).most_common())
print("single-version rows:", sum(1 for r in rows if r['versions_in_window']=='1'), "multi:", sum(1 for r in rows if r['versions_in_window']!='1'))
print("first==last rows:", sum(1 for r in rows if r['first_published_utc']==r['last_published_utc']))
out['version_summary']={'latest':collections.Counter(r['latest_version'] for r in rows).most_common(),'viw':collections.Counter(r['versions_in_window'] for r in rows).most_common(),'single':sum(1 for r in rows if r['versions_in_window']=='1'),'multi':sum(1 for r in rows if r['versions_in_window']!='1'),'first_eq_last':sum(1 for r in rows if r['first_published_utc']==r['last_published_utc'])}
# 4 cross-tabs
def xt(a,b):
    c=collections.Counter((r[a],r[b]) for r in rows)
    print(f"\nXT {a} x {b}")
    for k,v in sorted(c.items()): print(k,v)
    return {f"{k[0]}||{k[1]}":v for k,v in sorted(c.items())}
out['xt']={}
for a,b in [('authors_declared','haiku_category'),('authors_declared','haiku_agent_activity'),('authors_declared','dashboard_rule_level'),('haiku_prompt_version','haiku_category'),('haiku_prompt_version','haiku_agent_activity'),('authors_declared','haiku_prompt_version'),('authors_declared','dashboard_rules'),('dashboard_rule_level','haiku_category')]:
    out['xt'][f"{a} x {b}"]=xt(a,b)
print("\ndashboard_rules FULL:")
for k,v in collections.Counter(r['dashboard_rules'] for r in rows).most_common(): print(repr(k),v)
out['dashboard_rules_full']=collections.Counter(r['dashboard_rules'] for r in rows).most_common()
print("\nhaiku_level:", collections.Counter(r['haiku_level'] for r in rows).most_common())
print("summary distinct:", len(set(r['summary'] for r in rows)), "homepage distinct:", len(set(r['homepage_uri'] for r in rows)), "source distinct:", len(set(r['source_code_uri'] for r in rows)), "runtime_deps:", collections.Counter(r['runtime_dependencies'] for r in rows).most_common())
out['misc']={'summary_distinct':len(set(r['summary'] for r in rows)),'homepage_distinct':len(set(r['homepage_uri'] for r in rows)),'source_distinct':len(set(r['source_code_uri'] for r in rows)),'runtime_deps':collections.Counter(r['runtime_dependencies'] for r in rows).most_common(),'haiku_level':collections.Counter(r['haiku_level'] for r in rows).most_common()}
# 5 doc_id
docs=[r['doc_id'] for r in rows]
print("\ndoc_id distinct:", len(set(docs)), "empty:", sum(1 for d in docs if is_empty(d)))
pat=re.compile(r'^rubygems:([^@]+)@(.+)$')
print("doc_id matching rubygems:name@version:", sum(1 for d in docs if pat.match(d)))
print("doc_id name==row name:", sum(1 for r in rows if pat.match(r['doc_id']) and pat.match(r['doc_id']).group(1)==r['name']))
print("doc_id version==latest_version:", sum(1 for r in rows if pat.match(r['doc_id']) and pat.match(r['doc_id']).group(2)==r['latest_version']))
print("doc_id duplicates:", [k for k,v in collections.Counter(docs).items() if v>1])
out['doc_id']={'distinct':len(set(docs)),'empty':sum(1 for d in docs if is_empty(d)),'matching_format':sum(1 for d in docs if pat.match(d)),'name_matches_row':sum(1 for r in rows if pat.match(r['doc_id']) and pat.match(r['doc_id']).group(1)==r['name']),'version_matches_latest':sum(1 for r in rows if pat.match(r['doc_id']) and pat.match(r['doc_id']).group(2)==r['latest_version']),'duplicates':[k for k,v in collections.Counter(docs).items() if v>1]}
# 6 empty-field analysis
empty_rows=[r for r in rows if is_empty(r['haiku_category'])]
print(f"\nEMPTY haiku_category rows: {len(empty_rows)}")
print("their dashboard_rule_level:", collections.Counter(r['dashboard_rule_level'] for r in empty_rows))
print("their dashboard_rules:", collections.Counter(r['dashboard_rules'] for r in empty_rows))
print("their haiku_level:", collections.Counter(r['haiku_level'] for r in empty_rows))
print("their haiku_score:", collections.Counter(r['haiku_score'] for r in empty_rows))
print("their haiku_agent_activity:", collections.Counter(r['haiku_agent_activity'] for r in empty_rows))
print("their haiku_prompt_version:", collections.Counter(r['haiku_prompt_version'] for r in empty_rows))
print("their haiku_reason empty:", sum(1 for r in empty_rows if is_empty(r['haiku_reason'])))
print("their authors:", collections.Counter(r['authors_declared'] for r in empty_rows))
print("their withdrawn:", collections.Counter(r['withdrawn'] for r in empty_rows))
print("their dates:", sorted(collections.Counter(parse_dt(r['first_published_utc']).strftime('%Y-%m-%d') for r in empty_rows).items()))
print("their versions:", collections.Counter(r['versions_in_window'] for r in empty_rows), collections.Counter(r['latest_version'] for r in empty_rows))
# check overlap of empties across fields
for c in cols:
    e=set(i for i,r in enumerate(rows) if is_empty(r[c]))
    print(f"empty {c}: {len(e)}")
# intersection: rows empty in ALL dashboard/haiku fields vs partial
fields=['dashboard_rule_level','dashboard_rules','haiku_level','haiku_score','haiku_category','haiku_agent_activity','haiku_prompt_version','haiku_reason']
for r in empty_rows:
    pass
all_empty_dashboard_haiku=[r for r in rows if all(is_empty(r[c]) for c in fields)]
print("empty in ALL 8 dashboard/haiku fields:", len(all_empty_dashboard_haiku))
print("empty haiku_reason but nonempty category:", sum(1 for r in rows if is_empty(r['haiku_reason']) and not is_empty(r['haiku_category'])))
# what do empty rows share on other fields?
print("empty rows homepage distinct:", len(set(r['homepage_uri'] for r in empty_rows)), collections.Counter(r['homepage_uri'] for r in empty_rows).most_common(5))
print("empty rows summary sample distinct:", len(set(r['summary'] for r in empty_rows)))
print("empty rows name len:", min(len(r['name']) for r in empty_rows), max(len(r['name']) for r in empty_rows))
print("empty rows runtime_deps:", collections.Counter(r['runtime_dependencies'] for r in empty_rows))
print("empty rows source distinct:", len(set(r['source_code_uri'] for r in empty_rows)))
out['empty_analysis']={'n_empty_category':len(empty_rows),'authors':collections.Counter(r['authors_declared'] for r in empty_rows).most_common(),'dashboard_rule_level':collections.Counter(r['dashboard_rule_level'] for r in empty_rows).most_common(),'dashboard_rules':collections.Counter(r['dashboard_rules'] for r in empty_rows).most_common(),'haiku_level':collections.Counter(r['haiku_level'] for r in empty_rows).most_common(),'haiku_score':collections.Counter(r['haiku_score'] for r in empty_rows).most_common(),'agent_activity':collections.Counter(r['haiku_agent_activity'] for r in empty_rows).most_common(),'prompt_version':collections.Counter(r['haiku_prompt_version'] for r in empty_rows).most_common(),'haiku_reason_empty':sum(1 for r in empty_rows if is_empty(r['haiku_reason'])),'withdrawn':collections.Counter(r['withdrawn'] for r in empty_rows).most_common(),'dates':sorted(collections.Counter(parse_dt(r['first_published_utc']).strftime('%Y-%m-%d') for r in empty_rows).items()),'versions':collections.Counter(r['versions_in_window'] for r in empty_rows).most_common(),'latest':collections.Counter(r['latest_version'] for r in empty_rows).most_common(),'all8_empty':len(all_empty_dashboard_haiku),'runtime_deps':collections.Counter(r['runtime_dependencies'] for r in empty_rows).most_common(),'name_len_range':[min(len(r['name']) for r in empty_rows), max(len(r['name']) for r in empty_rows)],'summary_distinct':len(set(r['summary'] for r in empty_rows)),'homepage_distinct':len(set(r['homepage_uri'] for r in empty_rows)),'source_distinct':len(set(r['source_code_uri'] for r in empty_rows))}
# credential-shaped scan: presence/count only, never values
cred_re=re.compile(r'(?i)(api[_-]?key|secret|token|password|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{10,})')
hits=0; hit_cols=collections.Counter()
for r in rows:
    for c in cols:
        if cred_re.search(r[c] or ''):
            hits+=1; hit_cols[c]+=1
print(f"\nCREDENTIAL-SHAPED hits (cells): {hits} by col {dict(hit_cols)}")
out['credential_shaped_cells']=hits; out['credential_shaped_by_col']=dict(hit_cols)
# name uniqueness
print("name distinct:", len(set(r['name'] for r in rows)), "dup names:", [k for k,v in collections.Counter(r['name'] for r in rows).items() if v>1])
out['name_distinct']=len(set(r['name'] for r in rows)); out['name_dups']=[k for k,v in collections.Counter(r['name'] for r in rows).items() if v>1]
json.dump(out, open(OUT/'census.json','w'), indent=2, default=str)
print("\nDONE total", len(rows))
