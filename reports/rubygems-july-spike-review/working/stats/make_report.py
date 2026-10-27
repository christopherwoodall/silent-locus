import json, collections
from pathlib import Path
D=json.load(open(Path.home()/"workspace/silent-locus/reports/rubygems-july-spike-review/working/stats/census.json"))
OUT=Path.home()/"workspace/silent-locus/reports/rubygems-july-spike-review/working/stats"
def shape(a):
    if a.startswith('<script>'): return "script-tag"
    if a.startswith('<img'): return "img-tag"
    if '%=' in a or a.startswith('${'): return "template/expression-tag"
    if len(a)>60: return "long-fuzzing-list"
    return "plain"
def safe_author(a):
    s=shape(a)
    if s=='plain': return a
    return f"[{s} author string: distinct value, see census.json]"
authors=D['distributions']['authors_declared']
markup=[(a,n) for a,n in authors if shape(a)!='plain']
plain=[(a,n) for a,n in authors if shape(a)=='plain']
lines=[]
lines.append("# STATS/SCHEMA census — rubygems-july-2026-spike-operator-20261027.csv")
lines.append("")
lines.append("Source: `data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv`")
lines.append("SHA-256 (verified before census): 765ee2f24e6ec1a191c66faee030aaea8586cc4a0cdde1bee4c0668a0f0f3ce0")
lines.append("Method: recomputed by script `census.py`; log `census.log`; machine-readable `census.json`. All totals reconcile to 533.")
lines.append("Note on markup-like author strings: exact values are preserved in census.json (derived verbatim from the CSV). This report counts them by shape and does not reproduce payload-like strings in prose.")
lines.append("")
lines.append("## 1. Schema / per-column census")
lines.append("")
lines.append("| column | distinct (non-empty) | empty | non-empty | type / notes |")
lines.append("|---|---|---|---|---|")
notes={
 'name':'text, all unique','latest_version':'text, 33 values','versions_in_window':'integer 1–25, mean 1.28, median 1',
 'first_published_utc':'timestamp, 523 distinct','last_published_utc':'timestamp, 524 distinct',
 'authors_declared':'text, 46 distinct values','summary':'text, 224 distinct','homepage_uri':'text/URL, 81 distinct + 100 empty',
 'source_code_uri':'text/URL, 204 distinct + 327 empty','runtime_dependencies':'integer 0–22, mean 0.16, median 0',
 'withdrawn':'boolean text, 1 value only','dashboard_rule_level':'categorical, 4 values + 49 empty',
 'dashboard_rules':'categorical string, 73 distinct + 49 empty','haiku_level':'categorical, 4 values + 49 empty',
 'haiku_score':'numeric, present on 20 rows only; range 42–92, mean 62.2, median 53.5','haiku_category':'categorical, 3 values + 49 empty',
 'haiku_agent_activity':'categorical, 3 values + 49 empty','haiku_prompt_version':'categorical, 2 values + 49 empty',
 'haiku_reason':'free text, 484 distinct (one per non-empty row) + 49 empty','doc_id':'text, all unique, 0 empty'}
for s in D['schema']:
    c=s['column']
    lines.append(f"| {c} | {s['distinct_nonempty']} | {s['empty']} | {s['nonempty']} | {notes.get(c,'')} |")
lines.append("")
lines.append("Column totals check: every column sums to 533 (empty + non-empty). No column other than the eight dashboard/haiku fields and homepage/source has empties.")
lines.append("")
lines.append("### Categorical distributions (full)")
lines.append("")
for col in ['withdrawn','dashboard_rule_level','haiku_level','haiku_category','haiku_agent_activity','haiku_prompt_version','runtime_dependencies']:
    lines.append(f"**{col}:** " + "; ".join(f"{k}={v}" for k,v in D['distributions'][col]))
    lines.append("")
lines.append(f"**haiku_score (20 non-empty rows):** " + "; ".join(f"{k}={v}" for k,v in D['haiku_score_raw_counter']))
lines.append("")
lines.append("**summary:** 224 distinct values, 0 empty. **homepage_uri:** 82 distinct incl. empty; 81 non-empty distinct, 100 empty. **source_code_uri:** 205 distinct incl. empty; 204 non-empty distinct, 327 empty (61.4% empty). **haiku_reason:** 485 distinct incl. empty; 484 non-empty, each unique to its row.")
lines.append("")
lines.append("**Credential-shaped scan (presence/count only, values never copied):** 7 cells matched a broad credential-keyword pattern — 5 in summary, 2 in haiku_reason. These are pattern matches only (keyword-shaped), not confirmed secrets; no values are reproduced here or in census.json summaries beyond counts.")
lines.append("")
lines.append("## 2. Per-author batch structure")
lines.append("")
lines.append(f"Distinct authors_declared values: 46. Top 4 account for 410/533 (76.9%): Andrey78 129, Prvaz12_mars 113, tester 100, monib110 68. Remaining 42 distinct values account for 123 rows.")
lines.append("")
lines.append("Plain (non-markup) author counts, descending:")
lines.append("")
for a,n in plain:
    lines.append(f"- {a}: {n}")
lines.append("")
lines.append("Markup/template-shaped author values: 7 distinct values, 9 rows total. By shape (prefix-first classification): script-tag 3 distinct / 4 rows; img-tag 1 distinct / 1 row; template/expression-tag 2 distinct / 3 rows; long-fuzzing-list 1 distinct / 1 row. Plain author values: 39 distinct / 524 rows. Exact markup values are in census.json; they are not reproduced in this report's prose.")
# compute shape breakdown in code below? placeholder replaced after
lines.append("")
lines.append("| author | rows | first publish (first_published_utc) | last publish (max last_published_utc) | per-day (first publish) | max in 60 min | max in 10 min | max in 5 min | median gap (s) | min gap (s) | gaps <60s | gaps <300s | name len min–max (mean) | first==last rows |")
lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for a in D['per_author']:
    auth=safe_author(a['author'])
    lines.append(f"| {auth} | {a['n']} | {a['first']} | {a['last_published_max']} | {a['per_day']} | {a['max_in_60min']} @ {a['max_in_60min_start']} | {a['max_in_10min']} @ {a['max_in_10min_start']} | {a['max_in_5min']} @ {a['max_in_5min_start']} | {a['gap_median_s']} | {a['gap_min_s']} | {a['gaps_under_60s']} | {a['gaps_under_300s']} | {a['name_len_min']}–{a['name_len_max']} ({a['name_len_mean']}) | {a['first_eq_last']} |")
lines.append("")
lines.append("Overall timing: first publish 2026-07-06, last first-publish 2026-07-13 (full per-day below). Overall per-day (first_published_utc): " + "; ".join(f"{k}={v}" for k,v in D['overall_per_day'].items()))
lines.append("")
lines.append("Overall hour-of-day (UTC, first_published_utc): " + "; ".join(f"{k}={v}" for k,v in D['overall_per_hour'].items()))
lines.append("")
lines.append(f"Name length overall: min {D['name_len']['min']}, max {D['name_len']['max']}, mean {D['name_len']['mean']:.2f}, median {D['name_len']['median']}. Length distribution: {D['name_len']['counter']}. Pattern counts only: names containing a digit {D['name_patterns']['with_digit']}; names containing underscore {D['name_patterns']['with_underscore']}; hyphen-count distribution {D['name_patterns']['hyphen_counter']}.")
lines.append("")
lines.append("## 3. Version patterns")
lines.append("")
lines.append(f"latest_version distribution (33 values): " + "; ".join(f"{k}={v}" for k,v in D['version_summary']['latest']))
lines.append("")
lines.append(f"versions_in_window distribution: " + "; ".join(f"{k}={v}" for k,v in D['version_summary']['viw']))
lines.append("")
lines.append(f"Single-version rows (versions_in_window=1): {D['version_summary']['single']}. Multi-version rows: {D['version_summary']['multi']}. Rows where first_published_utc == last_published_utc: {D['version_summary']['first_eq_last']}.")
lines.append("")
lines.append("## 4. Cross-tabs (highlights; full tables in census.json under xt)")
lines.append("")
# highlights for main authors
for key in ['authors_declared x haiku_category','authors_declared x haiku_agent_activity','authors_declared x dashboard_rule_level','haiku_prompt_version x haiku_category','haiku_prompt_version x haiku_agent_activity']:
    lines.append(f"### {key}")
    lines.append("")
    for k,v in D['xt'][key].items():
        a,b=k.split('||')
        if a in ('Andrey78','Prvaz12_mars','tester','monib110') or key.startswith('haiku_prompt'):
            lines.append(f"- {a} × {b if b else '(empty)'}: {v}")
    lines.append("")
lines.append("Main-author cross-tab detail:")
lines.append("- Andrey78 (129): category mass_generated 129; activity possible 129; rule level medium 65 / low 64; prompt pkg-review-1 123 / pkg-review-2 6; haiku_level high 121 / medium 8.")
lines.append("- Prvaz12_mars (113): category mass_generated 113; activity possible 113; rule level medium 60 / low 53; prompt pkg-review-1 111 / pkg-review-2 2; haiku_level high 111 / medium 2.")
lines.append("- tester (100): category registry_test_or_probe 98 / mass_generated 2; activity possible 93 / likely 7; rule level critical 93 / medium 4 / high 3; prompt pkg-review-1 91 / pkg-review-2 9; haiku_level critical 58 / high 41 / medium 1.")
lines.append("- monib110 (68): category mass_generated 61 / empty 6 / unclear 1; activity possible 62 / empty 6; rule level medium 58 / empty 6 / low 4; prompt pkg-review-1 60 / empty 6 / pkg-review-2 2; haiku_level high 58 / empty 6 / medium 3 / low 1.")
lines.append("- Prompt × category: pkg-review-1 → mass_generated 295, registry_test_or_probe 168, unclear 1; pkg-review-2 → mass_generated 10, registry_test_or_probe 10; empty prompt → empty category 49.")
lines.append("- Prompt × activity: pkg-review-1 → possible 443, likely 16, no_sign 5; pkg-review-2 → possible 18, likely 2; empty prompt → empty activity 49. Note: all 20 pkg-review-2 rows are split 10/10 across categories, and no pkg-review-2 row is no_sign.")
lines.append("- Dashboard rule level overall: medium 193, critical 151, low 121, high 19, empty 49. Haiku level overall: high 385, critical 80, medium 15, low 4, empty 49.")
lines.append("- Author × category / activity / rule-level for the remaining author values: see census.json xt tables. The three large non-empty authors (Andrey78, Prvaz12_mars, tester) have zero empty dashboard/haiku rows; all 49 empty-field rows come from monib110 (6) plus the smaller-author set (43).")
lines.append("")
lines.append("### dashboard_rules — FULL frequency table (73 distinct strings + empty)")
lines.append("")
for k,v in D['dashboard_rules_full']:
    lines.append(f"- {k if k else '(empty)'}: {v}")
lines.append("")
lines.append("")
lines.append("## 5. doc_id pattern")
lines.append("")
lines.append("Format: `rubygems:<name>@<version>` for all 533 rows. Distinct: 533, duplicates: 0, empty: 0. Name part equals row name: 533/533. Version part equals latest_version: 530/533. The 3 mismatches are: apex-platform-test (latest 0.1.0, doc_id version 0.1.0-java), jrjackson (latest 0.5.2, doc_id version 0.5.2-java), shirobai (latest 2026.0713.1900, doc_id version 2026.0713.1900-x86_64-linux) — i.e. doc_id carries a platform suffix the latest_version column does not.")
lines.append("")
lines.append("## 6. Empty-field analysis (the 49 rows)")
lines.append("")
e=D['empty_analysis']
lines.append(f"The same 49 rows are empty in ALL eight dashboard/haiku fields (dashboard_rule_level, dashboard_rules, haiku_level, haiku_score, haiku_category, haiku_agent_activity, haiku_prompt_version, haiku_reason): {e['all8_empty']}. No row is partially empty on those fields; no non-empty-category row lacks haiku_reason.")
lines.append("")
lines.append("Empty rows by author: monib110 6, testingbear 5, fusagiko / takayamaki 4, apexhunter 3, Apex Black 2, Security Researcher 2, Testing Buffalo 2, Panther 2, Salvador Fuentes Jr 2, Marlen Brunner 2, Oscar Segura 2, plus 1 row each for 17 further distinct author values (14 plain + 1 img-tag + 1 long-fuzzing-list + 1 template/expression-tag). Total distinct author values among empty rows: 28 (25 plain + 3 markup-shaped). None of the 49 is Andrey78, Prvaz12_mars, or tester.")
lines.append("")
lines.append(f"Empty rows by first-publish date: " + "; ".join(f"{k}={v}" for k,v in e['dates']))
lines.append("")
lines.append(f"Empty rows: withdrawn True 49/49. versions_in_window: " + "; ".join(f"{k}={v}" for k,v in e['versions']) + ". latest_version: " + "; ".join(f"{k}={v}" for k,v in e['latest']))
lines.append("")
lines.append(f"Empty rows: runtime_dependencies " + "; ".join(f"{k}={v}" for k,v in e['runtime_deps']) + f". Homepage distinct 24 (16 empty homepage within the 49); source distinct 15; summary distinct 46; name length {e['name_len_range'][0]}–{e['name_len_range'][1]}.")
lines.append("")
lines.append("Other empties (not part of the 49 set): homepage_uri empty 100 rows total (so 51 non-empty-field rows also lack homepage); source_code_uri empty 327 rows total (so 278 non-empty-field rows also lack source).")
lines.append("")
lines.append("## Reconciliation")
lines.append("")
lines.append("- Total rows: 533. Header + 533 data rows. Name distinct 533, doc_id distinct 533, no duplicate names or doc_ids.")
lines.append("- withdrawn: True 533/533.")
lines.append("- Correction to the brief's category numbers: haiku_category is mass_generated 305 + registry_test_or_probe 178 + unclear 1 + empty 49 = 533. The brief omitted the single 'unclear' row (giga-pure-tool, monib110, 2026-07-12). All other brief numbers reconcile exactly.")
lines.append("")
# append exact category/activity numbers from json to resolve
for col in ['haiku_category','haiku_agent_activity','haiku_prompt_version','dashboard_rule_level','haiku_level']:
    lines.append(f"- {col}: " + "; ".join(f"{k if k else '(empty)'}={v}" for k,v in D['distributions'][col]) + f" (sum {sum(v for _,v in D['distributions'][col])})")
lines.append("")
lines.append("## Files")
lines.append("")
lines.append("- census.py (script), census.log (full output), census.json (machine-readable tables), make_report.py (this report generator), report.md (this file)")
lines.append("")
open(OUT/'report.md','w').write("\n".join(lines))
print("wrote report, lines", len(lines))
# print shape breakdown + exact sums for verification
import collections
print("shape breakdown", collections.Counter())
print("category sum check")
for col in ['haiku_category','haiku_agent_activity','haiku_prompt_version']:
    print(col, D['distributions'][col], sum(v for _,v in D['distributions'][col]))
