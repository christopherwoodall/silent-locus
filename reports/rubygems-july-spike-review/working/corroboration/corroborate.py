#!/usr/bin/env python3
"""Corroboration lane: CSV names vs v2, lane JSONLs, notes (grep), JFrog CSV.
Read-only. Outputs JSON + CSVs in same dir."""
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path.home() / "workspace/silent-locus"
OUT = Path(__file__).resolve().parent
CSV = BASE / "data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv"
V2 = BASE / "reports/ruby-sus-gems-export-v2.json"
LANE = BASE / "data/lanes/rubygems-goimport-campaign"

# --- CSV ---
rows = []
with open(CSV, newline="") as f:
    for r in csv.DictReader(f):
        rows.append(r)
print(f"csv rows: {len(rows)}")
assert len(rows) == 533, len(rows)
csv_names = [r["name"] for r in rows]
assert len(set(csv_names)) == len(csv_names), "dup names in csv"

# --- v2 ---
v2 = json.load(open(V2))["gems"]
v2map = {g["name"]: g for g in v2}
print(f"v2 rows: {len(v2)}")

# --- lane JSONLs: extract any gem-name-like string per line ---
lane_files = {
    "events.jsonl": LANE / "events.jsonl",
    "gem-graph-nodes.jsonl": LANE / "raw/gem-graph-nodes.jsonl",
    "gem-iocs-2026-09-27.jsonl": LANE / "raw/gem-iocs-2026-09-27.jsonl",
    "gem-june18-wayback.jsonl": LANE / "raw/gem-june18-wayback.jsonl",
    "gem-ioc-hits.jsonl": LANE / "raw/gem-ioc-hits.jsonl",
}
lane_hits = defaultdict(set)  # name -> set of files
for label, path in lane_files.items():
    if not path.exists():
        print(f"MISSING lane file: {path}"); continue
    text = open(path, errors="replace").read()
    for name in csv_names:
        if name in text:
            lane_hits[name].add(label)
    print(f"lane scanned: {label} ({path.stat().st_size} bytes)")

# extra lane-adjacent files (not in brief, checked for completeness, reported separately)
extra_files = {
    "raw/gemstuffer-jfrog-2026-09-27.csv": LANE / "raw/gemstuffer-jfrog-2026-09-27.csv",
    "raw/gem-pins-batch1-4.txt": None,
    "bundle.json": LANE / "bundle.json",
}
jfrog_names = set()
jf = LANE / "raw/gemstuffer-jfrog-2026-09-27.csv"
if jf.exists():
    jt = open(jf, errors="replace").read()
    for name in csv_names:
        if name in jt:
            jfrog_names.add(name)
    print(f"jfrog csv hits: {len(jfrog_names)}")
pins_text = ""
for p in sorted((LANE / "raw").glob("gem-pins-batch*.txt")):
    pins_text += open(p, errors="replace").read()
pins_hits = {n for n in csv_names if n in pins_text}
print(f"pins hits: {len(pins_hits)}")
bundle_text = open(LANE / "bundle.json", errors="replace").read() if (LANE / "bundle.json").exists() else ""
bundle_hits = {n for n in csv_names if n in bundle_text}
print(f"bundle hits: {len(bundle_hits)}")

# --- notes: exact-token grep over docs/notes/gem-*.md (+ hidden lane1 jfrog.json note) ---
import glob, subprocess
note_files = sorted(glob.glob(str(BASE / "docs/notes/gem-*.md")))
note_hits = defaultdict(set)
for nf in note_files:
    text = open(nf, errors="replace").read()
    for name in csv_names:
        if name in text:
            note_hits[name].add(Path(nf).name)
print(f"notes files scanned: {len(note_files)}; names with >=1 note hit: {len(note_hits)}")

# --- assemble ---
out_rows = []
for r in rows:
    n = r["name"]
    g = v2map.get(n)
    out_rows.append({
        "name": n,
        "csv_author": r["authors_declared"],
        "csv_first_published_utc": r["first_published_utc"],
        "csv_last_published_utc": r["last_published_utc"],
        "csv_latest_version": r["latest_version"],
        "csv_withdrawn": r["withdrawn"],
        "csv_dashboard_rule_level": r["dashboard_rule_level"],
        "csv_dashboard_rules": r["dashboard_rules"],
        "csv_haiku_level": r["haiku_level"],
        "csv_haiku_score": r["haiku_score"],
        "csv_haiku_category": r["haiku_category"],
        "csv_haiku_agent_activity": r["haiku_agent_activity"],
        "in_v2": g is not None,
        "v2_wave": g["wave"] if g else None,
        "v2_triage_verdict": g["triage_verdict"] if g else None,
        "v2_source_grade": g["source_grade"] if g else None,
        "v2_author": g["package_author"] if g else None,
        "v2_first_seen": g["first_seen"] if g else None,
        "in_lane": sorted(lane_hits.get(n, [])),
        "in_jfrog_csv": n in jfrog_names,
        "in_pins": n in pins_hits,
        "in_bundle": n in bundle_hits,
        "in_notes": sorted(note_hits.get(n, [])),
    })

with open(OUT / "corroboration-matrix.json", "w") as f:
    json.dump(out_rows, f, indent=1)
with open(OUT / "corroboration-matrix.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
    w.writeheader()
    for o in out_rows:
        d = dict(o)
        d["in_lane"] = ";".join(d["in_lane"]); d["in_notes"] = ";".join(d["in_notes"])
        w.writerow(d)

# --- summaries ---
def cnt(pred):
    return sum(1 for o in out_rows if pred(o))

print("\n== OVERLAP ==")
print("in_v2:", cnt(lambda o: o["in_v2"]))
print("v2 wave dist:", Counter(o["v2_wave"] for o in out_rows if o["in_v2"]))
print("v2 source_grade dist:", Counter(o["v2_source_grade"] for o in out_rows if o["in_v2"]))
print("v2 triage dist:", Counter(o["v2_triage_verdict"] for o in out_rows if o["in_v2"]))
print("in_lane(any of 5):", cnt(lambda o: o["in_lane"]))
for lf in lane_files:
    print(f"  {lf}:", cnt(lambda o, lf=lf: lf in o["in_lane"]))
print("in_notes:", cnt(lambda o: o["in_notes"]))
print("in_jfrog_csv:", cnt(lambda o: o["in_jfrog_csv"]))
print("in_pins:", cnt(lambda o: o["in_pins"]))
print("in_bundle:", cnt(lambda o: o["in_bundle"]))
print("in_any (v2|lane|notes):", cnt(lambda o: o["in_v2"] or o["in_lane"] or o["in_notes"]))
print("in_any incl jfrog/pins/bundle:", cnt(lambda o: o["in_v2"] or o["in_lane"] or o["in_notes"] or o["in_jfrog_csv"] or o["in_pins"] or o["in_bundle"]))

print("\n== PER AUTHOR ==")
for author, grp in sorted(defaultdict(list, {a: [o for o in out_rows if o["csv_author"] == a] for a in set(o["csv_author"] for o in out_rows)}).items()):
    print(f"{author}: n={len(grp)} in_v2={sum(o['in_v2'] for o in grp)} in_lane={sum(bool(o['in_lane']) for o in grp)} in_notes={sum(bool(o['in_notes']) for o in grp)} new={sum(not (o['in_v2'] or o['in_lane'] or o['in_notes']) for o in grp)} waves={Counter(o['v2_wave'] for o in grp if o['in_v2'])}")

print("\n== PER CSV DATE ==")
for d in sorted(set(o["csv_first_published_utc"][:10] for o in out_rows)):
    grp = [o for o in out_rows if o["csv_first_published_utc"][:10] == d]
    print(f"{d}: n={len(grp)} in_v2={sum(o['in_v2'] for o in grp)} waves={Counter(o['v2_wave'] for o in grp if o['in_v2'])} authors={Counter(o['csv_author'] for o in grp).most_common(5)}")
# set-equality checks
print("\nSET CHECKS: v2==lane:", {o['name'] for o in out_rows if o['in_v2']} == {o['name'] for o in out_rows if o['in_lane']})
print("SET CHECKS: v2==jfrog:", {o['name'] for o in out_rows if o['in_v2']} == {o['name'] for o in out_rows if o['in_jfrog_csv']})
print("notes detail:")
for o in out_rows:
    if o["in_notes"]:
        print(f"  {o['name']} | author={o['csv_author']} | v2wave={o['v2_wave']} | notes={o['in_notes']}")

# NEW = absent from v2 AND lane AND notes
new = [o for o in out_rows if not o["in_v2"] and not o["in_lane"] and not o["in_notes"]]
print(f"\nNEW (absent v2+lane+notes): {len(new)}")
with open(OUT / "new-names.json", "w") as f:
    json.dump(new, f, indent=1)
with open(OUT / "new-names.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name","csv_author","csv_first_published_utc","csv_dashboard_rule_level","csv_dashboard_rules","csv_haiku_level","csv_haiku_category","csv_haiku_agent_activity"])
    w.writeheader()
    for o in new:
        w.writerow({k: o[k] for k in w.fieldnames})
print("NEW by author:", Counter(o["csv_author"] for o in new))
print("NEW by date:", Counter(o["csv_first_published_utc"][:10] for o in new))

# July-7 wave detail in v2
july7 = [g for g in v2 if g["wave"] == "july-7"]
print(f"\nv2 july-7 rows: {len(july7)}")
for g in july7:
    print("  july7:", g["name"], "| author:", g["package_author"], "| verdict:", g["triage_verdict"], "| grade:", g["source_grade"], "| in_csv:", g["name"] in set(csv_names))
# CSV rows whose first-published date is July 7
csv_jul7 = [o for o in out_rows if o["csv_first_published_utc"][:10] == "2026-07-07"]
print(f"csv rows first-published 2026-07-07: {len(csv_jul7)}; in_v2: {sum(o['in_v2'] for o in csv_jul7)}")

# Andrey78 detail
a78 = [o for o in out_rows if o["csv_author"] == "Andrey78"]
print(f"\nAndrey78 csv rows: {len(a78)}; in_v2: {sum(o['in_v2'] for o in a78)}; in_lane: {sum(bool(o['in_lane']) for o in a78)}; in_notes: {sum(bool(o['in_notes']) for o in a78)}")
print("Andrey78 in v2 as author anywhere:", sum(1 for g in v2 if g.get("package_author") == "Andrey78"))
for label, path in lane_files.items():
    t = open(path, errors="replace").read()
    print(f"  author-string Andrey78 in {label}: {'Andrey78' in t}; Prvaz12_mars: {'Prvaz12_mars' in t}; monib110: {'monib110' in t}")
for nf in note_files:
    t = open(nf, errors="replace").read()
    for a in ("Andrey78", "Prvaz12_mars", "monib110"):
        if a in t:
            print(f"  author-string {a} in note {Path(nf).name}")
print("v2 authors of overlapping rows:", Counter(o["v2_author"] for o in out_rows if o["in_v2"]).most_common(10))
