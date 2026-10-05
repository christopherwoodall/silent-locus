#!/usr/bin/env python3
"""SCRATCH (temp/): audit data/ collections vs records, manifest, registry.

Read-only over the repo. For every data/ entry reports:
  - which event.dataset values its JSONL records actually carry (sampled)
  - whether the dir name matches those datasets
  - registration in scripts/local_es_manifest.json and schema/collections.json
  - PROVENANCE.md / SHA256SUMS / notes presence

Run from repo root:  python3 temp/audit_collections.py
"""
import glob, gzip, json, os
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)
SAMPLE, MAXF = 400, 6


def datasets_in_file(path):
    ds, n = Counter(), 0
    op = gzip.open if path.endswith(".gz") else open
    try:
        with op(path, "rt", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                n += 1
                d = (rec.get("event") or {}).get("dataset")
                ds[d if d else "<none>"] += 1
                if n >= SAMPLE:
                    break
    except Exception:
        return None
    return ds


man = json.load(open("scripts/local_es_manifest.json"))
reg = {e["index"]: "staged" for e in man.get("staged", [])}
reg.update({e["index"]: "via_script" for e in man.get("via_script", [])})
reg.setdefault("swarmtraces", "loader")
registry = {}
if os.path.exists("schema/collections.json"):
    registry = {c["name"]: c
                for c in json.load(open("schema/collections.json"))["collections"]}

print(f"{'collection':44s} {'reg':10s} {'in-registry':11s} PSN  datasets-in-records")
unreg, mismatch, loose = [], [], []
for entry in sorted(os.listdir("data")):
    p = os.path.join("data", entry)
    if os.path.isdir(p):
        files = sorted(glob.glob(p + "/**/*.jsonl", recursive=True)
                       + glob.glob(p + "/**/*.jsonl.gz", recursive=True))
        prov = os.path.exists(p + "/PROVENANCE.md")
        sums = os.path.exists(p + "/SHA256SUMS")
    else:
        files = [p] if entry.endswith((".jsonl", ".jsonl.gz")) else []
        prov = sums = False
    ds_all = Counter()
    for f in files[:MAXF]:
        ds = datasets_in_file(f)
        if ds:
            ds_all.update(ds)
    note = bool(glob.glob(f"notes/{entry}*")) or \
        bool(glob.glob(f"notes/analyst-note-{entry}*"))
    r = reg.get(entry, "")
    inreg = "Y" if entry in registry else "-"
    ds = ",".join(f"{k}:{v}" for k, v in ds_all.items()) or "-"
    if len(ds) > 58:
        ds = ds[:55] + "..."
    flag = ""
    if ds_all and entry not in ds_all and os.path.isdir(p) \
            and entry not in ("raw", "processed", "site-captures"):
        ov = registry.get(entry, {}).get("dataset_override")
        ovs = [ov] if isinstance(ov, str) else (ov or [])
        if not any(o in ds_all for o in ovs):
            flag = " <-- dataset!=dir"
            mismatch.append(entry)
    if not os.path.isdir(p) and files:
        flag = " <-- LOOSE at data/ root"
        loose.append(entry)
    if os.path.isdir(p) and ds_all and not r and \
            entry not in ("raw", "processed", "site-captures"):
        unreg.append(entry)
    print(f"{entry:44s} {r:10s} {inreg:11s} "
          f"{'Y' if prov else '-'}{'Y' if sums else '-'}{'Y' if note else '-'}  {ds}{flag}")

print(f"\nunregistered collections WITH jsonl records: {unreg}")
print(f"dataset!=dirname (no override): {mismatch}")
print(f"loose jsonl at data/ root: {loose}")
