#!/usr/bin/env python3
"""Concat the 6 overlap-analysis event files -> events.jsonl (labels.file_origin)."""
import json, os
D = "data/aggregates/2026-09-29-overlap-analysis"
files = sorted(f for f in os.listdir(D) if f.endswith(".jsonl"))
total_in = 0
tmp = os.path.join(D, "events.jsonl.tmp")
with open(tmp, "w") as out:
    for fn in files:
        n = 0
        with open(os.path.join(D, fn)) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                rec.setdefault("labels", {})["file_origin"] = fn
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                n += 1
        print(f"  {fn}: {n}")
        total_in += n
os.replace(tmp, os.path.join(D, "events.jsonl"))
got = sum(1 for _ in open(os.path.join(D, "events.jsonl")))
assert got == total_in, (got, total_in)
for fn in files:
    os.remove(os.path.join(D, fn))
print(f"events.jsonl: {got} records (== {total_in} inputs); 6 sources removed")
