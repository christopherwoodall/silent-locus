#!/usr/bin/env python3
"""SCRATCH (temp/): Phase 4 — apply the date-prefix rename to every reference.

Uses temp/slug_map.json (old dir relpath -> new) and temp/index_map.json
(old index/dataset slug -> new dated slug).

- scripts/*.py: path literals (data/<slug>[/..."']) and exact quoted slug
  strings (INDEX = "...", index lists, dataset filters, docstrings).
- scripts/local_es_manifest.json: index names + file paths.
- schema/collections.json: name -> dated slug, add series+date, fix
  dataset_override (rollup feeders keep overrides; legacy ones dropped).
- kibana-exports/*.ndjson: exact quoted slug strings.
- README.md: path/slug mentions.

Boundary-safe: quoted strings match quote-to-quote; path segments match
segment-to-segment. Prints a full change log. Run from repo root.
"""
import glob
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

slug_map = json.load(open("temp/slug_map.json"))     # data/<old> -> data/<new>
index_map = json.load(open("temp/index_map.json"))   # <old idx> -> <new idx>
meta = json.load(open("temp/slug_map_meta.json"))

# --- build pair lists -----------------------------------------------------
# path pairs: "data/<oldslug>" -> "data/<newslug>" (segment boundary aware)
path_pairs = []
for old, new in slug_map.items():
    path_pairs.append((old, new))
path_pairs.sort(key=lambda p: len(p[0]), reverse=True)

# quoted-slug pairs: exact "old" -> "new" (longest first)
quoted = sorted(index_map.items(), key=lambda p: len(p[0]), reverse=True)
# legacy dataset values found inside records/prose that map to dated slugs
quoted.append(("yourls-resweep", "2026-09-28-yourls-resweep"))  # series value
# NOTE: "university-shorteners" NOT globally quoted-replaced: ambiguous
# (index vs dir series). Handled per path segment + INDEX= lines only.

def patch_text(src, path):
    out = src
    hits = []
    # 1) path segments: data/.../<oldslug> bounded by / or quote or EOL
    for old, new in path_pairs:
        pat = re.compile(re.escape(old) + r'(?=[/"\'])')
        if pat.search(out):
            out = pat.sub(new, out)
            hits.append(old)
    # 2) exact quoted slugs: "old" / 'old'
    for old, new in quoted:
        for q in ('"', "'"):
            needle = q + old + q
            if needle in out:
                out = out.replace(needle, q + new + q)
                hits.append(needle)
    return out, hits

# --- scripts --------------------------------------------------------------
for path in sorted(glob.glob("scripts/*.py")):
    src = open(path).read()
    out, hits = patch_text(src, path)
    if out != src:
        open(path, "w").write(out)
        print(f"patched {path} ({len(hits)} ref kinds)")

# --- kibana exports -------------------------------------------------------
for path in sorted(glob.glob("kibana-exports/*.ndjson")):
    src = open(path).read()
    out = src
    n = 0
    for old, new in quoted:
        esc_old = old.replace('"', '\\"')
        esc_new = new.replace('"', '\\"')
        # NDJSON has escaped quotes inside JSON strings: \"slug\"
        for needle, repl in ((f'\\"{esc_old}\\"', f'\\"{esc_new}\\"'),
                             (f'"{esc_old}"', f'"{esc_new}"')):
            if needle in out:
                out = out.replace(needle, repl)
                n += 1
    if out != src:
        open(path, "w").write(out)
        print(f"patched {path} ({n} slug strings)")

# --- manifest -------------------------------------------------------------
mp = "scripts/local_es_manifest.json"
man = json.load(open(mp))
for section in ("staged", "via_script"):
    for e in man[section]:
        e["index"] = index_map.get(e["index"], e["index"])
        if "files" in e:
            e["files"] = [slug_map.get(os.path.dirname(f), os.path.dirname(f))
                          + "/" + os.path.basename(f) for f in e["files"]]
json.dump(man, open(mp, "w"), indent=1)
open(mp, "a").write("\n")
print("patched scripts/local_es_manifest.json")

# --- registry -------------------------------------------------------------
rp = "schema/collections.json"
reg = json.load(open(rp))
OVERRIDES = {  # new dir slug -> dated rollup/index slug it feeds
    "2026-09-28-university-shorteners": "2026-09-28-university-shorteners-rollup",
    "2026-09-28-university-shorteners-batch2": "2026-09-28-university-shorteners-rollup",
    "2026-09-28-university-shorteners-batch3": "2026-09-28-university-shorteners-rollup",
    "2026-05-12-university-shorteners-events": "2026-05-12-university-shorteners",
}
dirmeta = {}  # old basename -> meta
for old_dir, m in meta.items():
    dirmeta[old_dir.split("/")[-1]] = m

for c in reg["collections"]:
    m = dirmeta.get(c["name"])
    if m:
        c["series"] = m["series"]
        c["date"] = m["date"]
        c["name"] = m["new"].split("/")[-1]
        if "path" in c:
            c["path"] = m["new"]
        c.pop("dataset_override", None)
        if c["name"] in OVERRIDES:
            c["dataset_override"] = OVERRIDES[c["name"]]
        idx = c.get("index")
        if idx:
            c["index"] = index_map.get(idx, idx)
    elif c.get("virtual"):
        # virtual entries (no dir): date by their index mapping
        idx = c.get("index")
        if idx and idx in index_map:
            new_idx = index_map[idx]
            c["series"] = c["name"]
            c["date"] = new_idx[:10]
            c["name"] = new_idx
            c["index"] = new_idx
            c.pop("dataset_override", None)
json.dump(reg, open(rp, "w"), indent=2)
open(rp, "a").write("\n")
print("patched schema/collections.json")
print("done")
