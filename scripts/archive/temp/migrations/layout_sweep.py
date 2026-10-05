#!/usr/bin/env python3
"""Canonical layout migration sweep: rename event files to events.jsonl,
move root strays into raw/, move helper scripts to repo scripts/.
Moves/renames only; no content modification, nothing deleted."""
import os, re, shutil, sys, json

REPO = "/mnt/c/Users/chris/Desktop/projects/silent-locus"
DATA = os.path.join(REPO, "data")
SCRIPTS = os.path.join(REPO, "scripts")

EXCLUDED = {
    "2026-09-28-dockerhub-trojan-images", "2026-05-05-gomod-hunt",
    "2026-05-11-osv", "2026-07-07-july7-gem-forensics",
    "2026-09-29-gem-temporal-pivot", "2026-06-04-admin-deletions",
}
AGG_OK = {"2026-05-26-proxy-primitives", "2025-09-26-cors-bwa-proxy",
          "2026-09-29-overlap-analysis", "2026-09-28-gem83-reconciliation"}
ALLOWED_ROOT = {"events.jsonl", "rollup.jsonl", "PROVENANCE.md",
                "SHA256SUMS", "SHA256SUMS.txt", "raw"}

# helper scripts -> repo scripts/ (explicit old rel path -> new basename)
SCRIPT_MOVES = {
    "2016-05-06-reverse-tunnels/htmx_search.py": "reverse_tunnels_htmx_search.py",
    "2022-12-30-dse-wiki-verification/expand_search.py": "dse_wiki_verification_expand_search.py",
    "2022-12-30-dse-wiki-verification/fetch_reports.py": "dse_wiki_verification_fetch_reports.py",
    "2022-12-30-dse-wiki-verification/scan_cache.py": "dse_wiki_verification_scan_cache.py",
    "2022-12-30-dse-wiki-verification/fetch_slow.sh": "dse_wiki_verification_fetch_slow.sh",
    "2025-12-04-urlquery-marker-sweep/run_sweep.py": "urlquery_marker_sweep_run_sweep.py",
    "2025-12-04-urlquery-marker-sweep/run_sweep_v2.py": "urlquery_marker_sweep_run_sweep_v2.py",
    "2026-02-01-agent-convo-venues/build_dataset.py": "agent_convo_venues_build_dataset.py",
    "2026-08-25-commonlog-scan/build_dataset.py": "commonlog_scan_build_dataset.py",
    "2026-09-28-nsi-venue-sweep/build_dataset.py": "nsi_venue_sweep_build_dataset.py",
    "2026-09-28-open-data-api-venues/build_dataset.py": "open_data_api_venues_build_dataset.py",
    "2026-09-28-university-shorteners/build_dataset.py": "university_shorteners_build_dataset.py",
    "2026-09-28-university-shorteners-batch2/build_dataset.py": "university_shorteners_batch2_build_dataset.py",
    "2026-09-28-university-shorteners-batch3/build_dataset.py": "university_shorteners_batch3_build_dataset.py",
    "2026-09-28-worldpoverty-task-family/build_dataset.py": "worldpoverty_task_family_build_dataset.py",
    "2026-09-28-yourls-resweep/build_resweep.py": "yourls_resweep_build_resweep.py",
    "2026-09-28-yourls-resweep/diff_resweep.py": "yourls_resweep_diff_resweep.py",
    "2026-09-28-yourls-resweep/fetch_resweep.py": "yourls_resweep_fetch_resweep.py",
    "2026-09-29-forged-flag-hunt/compute_flags.py": "forged_flag_hunt_compute_flags.py",
}

renames, moved_files, moved_dirs, scripts_moved = [], [], [], []
needs_review, no_event, errors = [], [], []

def collect_dirs():
    dirs = []
    for name in sorted(os.listdir(DATA)):
        p = os.path.join(DATA, name)
        if os.path.isdir(p) and re.match(r"^\d{4}-\d{2}-\d{2}-", name) and name not in EXCLUDED:
            dirs.append((name, p))
    agg = os.path.join(DATA, "aggregates")
    for name in sorted(os.listdir(agg)):
        p = os.path.join(agg, name)
        if os.path.isdir(p) and name in AGG_OK:
            dirs.append(("aggregates/" + name, p))
    return dirs

def safe_move(src, dst):
    if os.path.exists(dst):
        errors.append(f"target exists: {dst} (from {src})")
        return False
    shutil.move(src, dst)
    return True

for rel, d in collect_dirs():
    entries = sorted(os.listdir(d))
    root_jsonl = [e for e in entries
                  if e.endswith(".jsonl") and os.path.isfile(os.path.join(d, e))
                  and e not in ("events.jsonl", "rollup.jsonl")]
    has_events = "events.jsonl" in entries
    review = False
    if has_events:
        if root_jsonl:
            needs_review.append(f"{rel}: events.jsonl present plus {root_jsonl}")
            review = True
    elif len(root_jsonl) == 1:
        src = os.path.join(d, root_jsonl[0])
        dst = os.path.join(d, "events.jsonl")
        if safe_move(src, dst):
            renames.append(f"{rel}/{root_jsonl[0]} -> {rel}/events.jsonl")
    elif len(root_jsonl) == 0:
        no_event.append(rel)
    else:
        needs_review.append(f"{rel}: multiple root .jsonl {root_jsonl}")
        review = True

    # helper scripts
    for e in entries:
        key = f"{rel}/{e}"
        if key in SCRIPT_MOVES:
            src = os.path.join(d, e)
            dst = os.path.join(SCRIPTS, SCRIPT_MOVES[key])
            if safe_move(src, dst):
                scripts_moved.append(f"data/{key} -> scripts/{SCRIPT_MOVES[key]}")

    # hygiene sweep
    for e in sorted(os.listdir(d)):
        if e in ALLOWED_ROOT:
            continue
        src = os.path.join(d, e)
        if review and e.endswith(".jsonl") and os.path.isfile(src):
            continue  # leave jsonl in needs-review dirs
        raw = os.path.join(d, "raw")
        os.makedirs(raw, exist_ok=True)
        dst = os.path.join(raw, e)
        if safe_move(src, dst):
            if os.path.isdir(dst):
                moved_dirs.append(f"data/{rel}/{e} -> data/{rel}/raw/{e}")
            else:
                moved_files.append(f"data/{rel}/{e} -> data/{rel}/raw/{e}")

report = {
    "renames": renames, "scripts_moved": scripts_moved,
    "moved_dirs": moved_dirs, "moved_files_count": len(moved_files),
    "moved_files": moved_files, "needs_review": needs_review,
    "no_event": no_event, "errors": errors,
}
with open(os.path.join(os.path.dirname(__file__), "layout_sweep_report.json"), "w") as f:
    json.dump(report, f, indent=1)
print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in report.items()}, indent=1))
for e in errors:
    print("ERROR:", e, file=sys.stderr)
