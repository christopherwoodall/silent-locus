#!/usr/bin/env python3
import csv
from pathlib import Path
SRC = Path.home()/"workspace/silent-locus/data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv"
OUT = Path.home()/"workspace/silent-locus/reports/rubygems-july-spike-review/working/linguist"
rows = {r['name']: r for r in csv.DictReader(open(SRC, encoding='utf-8'))}
# picks: one per class, chosen by package name so text is re-read from CSV at write time
picks = {
 'mass_generated_combinatorial': ['mini-sharp-hub','ultra-fast-box','mini-fast-rb'],
 'probe_ssrf': ['ssrf-test-1783405321'] ,
 'placeholder': ['apex-black-test-001'],
 'automated_scripted': [],
 'no_deception_v2': [],
 'mass_v2': [],
}
# find automated examples: reason contains 'automat' and category mass? print first 4 automated reasons verbatim
auto = [r for r in rows.values() if 'automat' in r['haiku_reason'].lower()][:6]
for r in auto: print(f"AUTO | {r['name']} | {r['haiku_reason']}")
print()
for k, names in picks.items():
    for n in names:
        if n in rows:
            r=rows[n]
            print(f"{k} | {n} | {r['authors_declared']} | cat={r['haiku_category']} activity={r['haiku_agent_activity']} prompt={r['haiku_prompt_version']}")
            print(r['haiku_reason'])
            print()
# v2 examples by prompt
v2 = [r for r in rows.values() if r['haiku_prompt_version']=='pkg-review-2']
for r in v2[:6]:
    print(f"V2 | {r['name']} | {r['haiku_reason']}")
print()
# template-batch / placeholder-text reasons: first reasons containing 'template' 
for r in list(rows.values()):
    if 'template' in r['haiku_reason'].lower():
        print(f"TEMPLATE-WORD | {r['name']} | {r['haiku_reason']}")
        break
# reasons containing 'placeholder' first 3
c=0
for r in rows.values():
    if 'placeholder' in r['haiku_reason'].lower() and c<3:
        print(f"PLACEHOLDER-WORD | {r['name']} | {r['haiku_reason']}"); c+=1
# reasons containing 'bot' 
for r in rows.values():
    if 'bot' in r['haiku_reason'].lower():
        print(f"BOT | {r['name']} | {r['haiku_reason']}")
# reasons containing 'script' first 3
c=0
for r in rows.values():
    if 'script' in r['haiku_reason'].lower() and c<3:
        print(f"SCRIPT | {r['name']} | {r['haiku_reason']}"); c+=1
# unclear reason already known; print it
print("UNCLEAR |", rows['giga-pure-tool']['haiku_reason'])
# mass_generated with 'generated' word
for r in rows.values():
    if 'generated' in r['haiku_reason'].lower():
        print(f"GENERATED-WORD | {r['name']} | {r['haiku_reason']}")
