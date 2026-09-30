#!/usr/bin/env python3
"""Build events.jsonl + rollup.jsonl for data/2025-05-14-hf-tampering-check.

Worker W3, 2026-09-29. Usage: python3 temp/build_events_w3_hf.py <repo_root>

Lane: Hugging Face metadata/history-only tampering check on sunblaze-ucb/cybergym
and ExploitGym-named artifacts, against the July 10-13, 2026 breach window.

Inputs (all under data/2025-05-14-hf-tampering-check/raw/):
  commits-main.json / commits-parquet.json              -> sunblaze-ucb/cybergym
  commits-shirman_exploitgym-answers.json               -> shirman/exploitgym-answers
  commits-shirman_exploitgym-results.json               -> shirman/exploitgym-results
  commits-SpeckledCerberus_exploitgym-answers.json      -> SpeckledCerberus/exploitgym-answers
  discussions-p0.json + discussion-1.json               - 1 discussion thread
  discussions-p1.json                                   - empty page (no records)
  dataset-meta-20260928T233536Z.json                    - repo metadata snapshot
  meta-shirman_exploitgym-results.json                  - repo metadata snapshot
  meta-SpeckledCerberus_exploitgym-answers.json         - repo metadata snapshot
  file-listing-summary.json                             - derived file inventory
  author-repos.json                                     - author sweep (8 repos)
  MANIFEST.sha256                                       - EXCLUDED: lane file inventory,
                                                          superseded by regenerated SHA256SUMS

Grain: one record per commit (kind=artifact_observation), one per discussion
thread (kind=artifact_observation), one per metadata snapshot file
(kind=extraction). Rollup: per-repo commit summaries (kind=repo_commit_rollup,
NEW - listed in notes/dir-triage-W3.md), including whether any commit falls in
the July 10-13, 2026 breach window.

Fingerprint identity strings (documented in PROVENANCE.md):
  commits:     sha256("hf-commit:<repo>:<sha>")
  discussions: sha256("hf-discussion:<repo>#<num>")
  snapshots:   sha256("hf-meta-snapshot:<key>")
  rollup:      sha256("hf-repo-rollup:<repo>")
"""
import json, sys, hashlib, os
from datetime import datetime, timezone

ROOT = sys.argv[1]
D = os.path.join(ROOT, "data", "2025-05-14-hf-tampering-check")
RAW = os.path.join(D, "raw")
SLUG = "2025-05-14-hf-tampering-check"
CREATED = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
LANE_TS = "2026-09-28T00:00:00Z"
BREACH_START, BREACH_END = "2026-07-10", "2026-07-13"

def fp(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

out = []
commit_index = []  # (repo, sha, date) for the rollup

# --- 1. commits ---
COMMIT_FILES = {
    "commits-main.json": ("sunblaze-ucb/cybergym", "main"),
    "commits-parquet.json": ("sunblaze-ucb/cybergym", "refs/convert/parquet"),
    "commits-shirman_exploitgym-answers.json": ("shirman/exploitgym-answers", "main"),
    "commits-shirman_exploitgym-results.json": ("shirman/exploitgym-results", "main"),
    "commits-SpeckledCerberus_exploitgym-answers.json": ("SpeckledCerberus/exploitgym-answers", "main"),
}
n_commits = 0
for fn, (repo, ref) in sorted(COMMIT_FILES.items()):
    commits = json.load(open(os.path.join(RAW, fn)))
    for c in commits:
        n_commits += 1
        sha = c["id"]
        labels = {
            "commit.sha": sha,
            "commit.repo": repo,
            "commit.ref": ref,
            "commit.title": (c.get("title") or "")[:300],
            "commit.authors": str(c.get("authors"))[:300],
            "commit.date": c.get("date"),
            "timestamp_source": "labels:commit.date",
        }
        out.append({
            "@timestamp": c["date"],
            "event": {"dataset": SLUG, "created": CREATED},
            "record_kind": "artifact_observation",
            "fingerprint": fp(f"hf-commit:{repo}:{sha}"),
            "labels": labels,
            "source_url": f"https://huggingface.co/datasets/{repo}/commit/{sha}",
            "retrieved_via": "huggingface.co/api (public Hub API, JSON only)",
            "description": f"Commit {sha[:12]} on {repo} [{ref}]: {(c.get('title') or '').strip()[:150]} ({c.get('date')})",
        })
        commit_index.append((repo, sha, c["date"]))

# --- 2. discussions (p0 has the thread, p1 is an empty page) ---
p0 = json.load(open(os.path.join(RAW, "discussions-p0.json")))
detail = json.load(open(os.path.join(RAW, "discussion-1.json")))
n_disc = 0
for th in p0.get("discussions", []):
    n_disc += 1
    repo = (th.get("repo") or {}).get("name", "")
    author = (th.get("author") or {}).get("name", "")
    labels = {
        "discussion.num": th.get("num"),
        "discussion.repo": repo,
        "discussion.title": (th.get("title") or "")[:300],
        "discussion.status": th.get("status"),
        "discussion.author": author,
        "discussion.num_comments": th.get("numComments"),
        "discussion.is_pull_request": th.get("isPullRequest"),
        "timestamp_source": "labels:discussion.created_at",
    }
    out.append({
        "@timestamp": th["createdAt"],
        "event": {"dataset": SLUG, "created": CREATED},
        "record_kind": "artifact_observation",
        "fingerprint": fp(f"hf-discussion:{repo}#{th.get('num')}"),
        "labels": labels,
        "source_url": f"https://huggingface.co/datasets/{repo}/discussions/{th.get('num')}",
        "retrieved_via": "huggingface.co/api (public Hub API, JSON only)",
        "description": f"Discussion #{th.get('num')} on {repo}: {(th.get('title') or '')[:150]} ({th.get('status')})",
    })

# --- 3. metadata snapshots (one record per file) ---
def snap(key, fn, labels_extra, desc):
    me = {"snapshot.key": key, "snapshot.file": fn,
          "timestamp_source": "lane:2026-09-28 (Hub API retrieval; per-file timestamps in dataset-meta filename)"}
    me.update(labels_extra)
    out.append({
        "@timestamp": LANE_TS,
        "event": {"dataset": SLUG, "created": CREATED},
        "record_kind": "extraction",
        "fingerprint": fp(f"hf-meta-snapshot:{key}"),
        "labels": me,
        "retrieved_via": "huggingface.co/api (public Hub API, JSON only)",
        "description": desc,
    })

dm = json.load(open(os.path.join(RAW, "dataset-meta-20260928T233536Z.json")))
snap("sunblaze-ucb/cybergym", "dataset-meta-20260928T233536Z.json", {
    "snapshot.siblings": len(dm.get("siblings", [])),
    "snapshot.last_modified": dm.get("lastModified"),
    "snapshot.sha": dm.get("sha"),
    "snapshot.downloads": dm.get("downloads"),
    "snapshot.likes": dm.get("likes"),
    "snapshot.created_at": dm.get("createdAt"),
}, "Metadata snapshot of sunblaze-ucb/cybergym: 7538 siblings, lastModified 2025-05-15")

for repo, fn in [("shirman/exploitgym-results", "meta-shirman_exploitgym-results.json"),
                 ("SpeckledCerberus/exploitgym-answers", "meta-SpeckledCerberus_exploitgym-answers.json")]:
    m = json.load(open(os.path.join(RAW, fn)))
    snap(repo, fn, {
        "snapshot.last_modified": m.get("lastModified"),
        "snapshot.sha": m.get("sha"),
        "snapshot.created_at": m.get("createdAt"),
        "snapshot.downloads": m.get("downloads"),
        "snapshot.likes": m.get("likes"),
    }, f"Metadata snapshot of {repo}: lastModified {m.get('lastModified')}")

fls = json.load(open(os.path.join(RAW, "file-listing-summary.json")))
snap("sunblaze-ucb/cybergym:file-listing-summary", "file-listing-summary.json", {
    "snapshot.total_files": fls.get("total_files"),
    "snapshot.arvo_task_dirs": fls.get("arvo_task_dirs"),
    "snapshot.ossfuzz_task_dirs": fls.get("ossfuzz_task_dirs"),
    "snapshot.last_modified": fls.get("lastModified"),
    "snapshot.sha": fls.get("sha"),
}, "Derived file-listing summary of sunblaze-ucb/cybergym: 7538 files (1368 arvo + 139 ossfuzz task dirs)")

ar = json.load(open(os.path.join(RAW, "author-repos.json")))
snap("author:sunblaze-ucb", "author-repos.json", {
    "snapshot.repo_count": len(ar),
    "snapshot.repos": [r.get("id") for r in ar],
    "snapshot.last_modified_max": max((r.get("lastModified") or "") for r in ar),
}, f"Author sweep sunblaze-ucb: {len(ar)} org datasets")

with open(os.path.join(D, "events.jsonl"), "w", encoding="utf-8") as fh:
    for r in out:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

# --- rollup: per-repo commit summaries ---
by_repo = {}
for repo, sha, date in commit_index:
    by_repo.setdefault(repo, []).append((date, sha))
rollup = []
for repo in sorted(by_repo):
    dates = sorted(d for d, _ in by_repo[repo])
    in_window = sum(1 for d in dates if BREACH_START <= d[:10] <= BREACH_END)
    labels = {
        "repo": repo,
        "rollup.commits": len(dates),
        "rollup.first": dates[0],
        "rollup.last": dates[-1],
        "rollup.in_breach_window_2026_07_10_13": in_window,
        "timestamp_source": "derived:commit dates (min)",
    }
    rollup.append({
        "@timestamp": dates[0],
        "event": {"dataset": f"{SLUG}-rollup", "created": CREATED},
        "record_kind": "repo_commit_rollup",
        "fingerprint": fp(f"hf-repo-rollup:{repo}"),
        "labels": labels,
        "source_url": f"https://huggingface.co/datasets/{repo}/commits/main",
        "description": (f"{repo}: {len(dates)} commit(s), {dates[0][:10]} -> {dates[-1][:10]}; "
                        f"{in_window} in 2026-07-10/13 breach window"),
    })
with open(os.path.join(D, "rollup.jsonl"), "w", encoding="utf-8") as fh:
    for r in rollup:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"commits: {n_commits}, discussions: {n_disc}, snapshots: 5, events: {len(out)}, rollup: {len(rollup)}")
