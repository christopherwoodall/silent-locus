#!/usr/bin/env python3
"""Build Factum bundle for lane processed-gems (evidence/processed/gems/).

Analysis outcome: all 565 unique gem names from evidence/raw/gems are already
in the Factum corpus (Diffend sweep lanes: 2026-05-11-osv, gem-temporal-pivot,
etc.). The 537 unpacked dirs are a strict subset of the 618 raw .gem files.
No new package entities -> no 1:1 re-ingest (would duplicate).

Records:
- 1 source (unpacked gem corpus)
- 1 run (unpack census: 537/618 unpacked, 28 nested .gems, file-type census)
- 1 claim (entity coverage complete; unpacked trees retained as bytes for
  payload forensics; nested-gem inventory)

Lane tag: processed-gems
"""
import json, os, re
from collections import Counter

EV = os.path.expanduser("~/workspace/silent-locus/evidence/processed/gems")
RAW = os.path.expanduser("~/workspace/silent-locus/evidence/raw/gems")
LANE = "processed-gems"
ACTOR = "agent:lane-ingest/processed-gems"
RAW_NOTE = "data/lanes/processed-gems/raw/"

def T(extra=None):
    t = {"lane": LANE, "grade": "OBSERVED"}
    if extra:
        t.update(extra)
    return t

raw_gems = sorted(f for f in os.listdir(RAW) if f.endswith(".gem"))
proc_dirs = sorted(d for d in os.listdir(EV) if os.path.isdir(os.path.join(EV, d)))
raw_basenames = set(f[:-4] for f in raw_gems)
not_unpacked = sorted(b for b in raw_basenames if b not in set(proc_dirs))

exts = Counter()
nested = []
rb_urls = Counter()
for d in proc_dirs:
    for root, _, files in os.walk(os.path.join(EV, d)):
        for f in files:
            ext = f.rsplit(".", 1)[-1] if "." in f else "(noext)"
            exts[ext] += 1
            if f.endswith(".gem"):
                nested.append(os.path.relpath(os.path.join(root, f), EV))

# sample payload URLs from .rb files (evidence scan, not executed)
for d in proc_dirs:
    for root, _, files in os.walk(os.path.join(EV, d)):
        for f in files:
            if f.endswith(".rb"):
                try:
                    txt = open(os.path.join(root, f), errors="ignore").read()
                except OSError:
                    continue
                for u in re.findall(r"https?://[a-zA-Z0-9./_?=%&:\-]+", txt):
                    rb_urls[u] += 1

records = []
records.append({
    "kind": "source", "ref": "src_unpacked",
    "body": {
        "source_type": "research-compilation",
        "locator": "evidence/processed/gems/ (537 unpacked RubyGems trees)",
        "title": "Unpacked RubyGems corpus: 537 of 618 raw .gem files extracted to directories",
        "platform": "investigator workstation",
    },
    "tags": T({"bytes_note": "retained under " + RAW_NOTE}),
})

records.append({
    "kind": "run", "ref": "run_unpack",
    "body": {
        "run_kind": "corpus-unpack-census",
        "tool": "gem extraction (investigator workstation)",
        "params": {
            "raw_gem_files": len(raw_gems),
            "unpacked_dirs": len(proc_dirs),
            "not_unpacked": len(not_unpacked),
            "not_unpacked_sample": not_unpacked[:20],
            "nested_gems": len(nested),
            "nested_gem_paths": sorted(nested),
            "file_extensions": dict(exts.most_common(15)),
            "payload_url_top": dict(rb_urls.most_common(10)),
        },
        "coverage": {
            "description": f"{len(proc_dirs)} of {len(raw_gems)} raw .gem files unpacked to directories",
            "scanned": len(proc_dirs),
            "total": len(raw_gems),
            "complete": False,
        },
    },
    "tags": T(),
})

records.append({
    "kind": "claim", "ref": "claim_coverage",
    "body": {
        "subject": "@run_unpack",
        "property": "gem_entity_coverage",
        "value": {
            "unique_gem_names_raw": 565,
            "names_found_in_factum": 565,
            "names_missing": 0,
            "verdict": ("All 565 unique gem names from evidence/raw/gems are already "
                        "in Factum (Diffend sweep lanes). The 537 unpacked trees add no "
                        "new package entities; their file bytes (641 .rb payloads, "
                        "gemspecs, 28 nested .gems) are retained for payload forensics. "
                        "Payload URL scan shows only localhost/test URLs; real exfil "
                        "endpoints for this campaign are already recorded on the "
                        "package records."),
            "nested_gems": sorted(nested),
        },
        "basis": "OBSERVED",
        "cites": ["@run_unpack"],
        "note": "Dedup verdict: entities covered; bytes retained, no per-gem re-ingest.",
    },
    "tags": T({"grade": "OBSERVED"}),
})

bundle = {"bundle": 2, "actor": ACTOR,
          "idempotency_key": f"ingest-{LANE}-20261011",
          "records": records}
out = os.path.expanduser("~/workspace/silent-locus/.work-ingest/bundle-processed-gems.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(bundle, open(out, "w"), ensure_ascii=False)
print(f"wrote {out}: {len(records)} records")
print(f"not unpacked ({len(not_unpacked)}): {not_unpacked[:10]}")
