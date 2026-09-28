#!/usr/bin/env python3
"""Merge lane-20 original results + retry results into the final file.

Final schema: 1,284 rows, original name order. Retry rows (retry_pass=True)
replace the 672 phase-1 failure rows. Rows still unconfirmed after retry keep
in_diffend=None / http_status="unconfirmed".
"""
import json
import os

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(PROJ, "data/osv/diffend_sweep_results.jsonl")
RETRY = os.path.join(PROJ, "data/osv/diffend_sweep_results_retry.jsonl")
FINAL = os.path.join(PROJ, "data/osv/diffend_sweep_results_final.jsonl")

retry = {}
for line in open(RETRY):
    r = json.loads(line)
    retry[r["name"]] = r

n_replaced = n_unconfirmed = 0
with open(FINAL, "w") as out:
    for line in open(ORIG):
        r = json.loads(line)
        if r["name"] in retry:
            r = retry[r["name"]]
            n_replaced += 1
            if r.get("in_diffend") is None:
                n_unconfirmed += 1
        out.write(json.dumps(r) + "\n")

print("final rows: 1284 expected; retry rows merged: %d; still unconfirmed: %d"
      % (n_replaced, n_unconfirmed))

# summary stats
import collections
rows = [json.loads(l) for l in open(FINAL)]
c = collections.Counter(
    "found" if r.get("in_diffend") is True
    else "absent" if r.get("in_diffend") is False else "unconfirmed"
    for r in rows)
print(dict(c))
mechs = collections.Counter()
for r in rows:
    for m in r.get("mechanism_notes", []):
        mechs[m.split(":")[0]] += 1
print("mechanism families:", dict(mechs))
gram = collections.Counter()
for r in rows:
    if r.get("in_diffend") is True:
        for g in r.get("name_grammars", []):
            gram[g] += 1
print("found-name grammars:", dict(gram))
