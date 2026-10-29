#!/usr/bin/env python3
"""Lane 11 — reposcout: GitHub + HuggingFace trajectory-candidate inventory.

Watches a config-held list of GitHub repos and HuggingFace datasets
(the "watchlist" in the "reposcout" block of swarm-infra-config.json).
Each run builds a file manifest per watched repo, diffs it against the
previous manifest, and reports NEWLY-APPEARED files whose extension
marks them as trajectory candidates ("candidate-trajectory"). An
extension proves file FORMAT, not content: file bodies are never
fetched. Grade is SECONDARY (manifest metadata, not observed content).

Newness = newly-appeared files in watched manifests. No watchlist
entries in config, no run.

DISABLED BY DEFAULT. The module ships inert:
- the "reposcout" config block must carry "enabled": true, AND
- every watchlist entry must carry "enabled": true.
Without both, a live scan is refused. --dry-run still lists what WOULD
be scanned, with zero network calls and zero writes.

State (fixed paths, never caller-supplied):
- scripts/scanners/state/reposcout/<sanitized-id>.json : per-repo manifest
- scripts/scanners/state/reposcout/quota.json          : GitHub quota state

Quota: the VM's egress IP shares one 60-request/hour unauthenticated
GitHub API bucket. X-RateLimit-Remaining and X-RateLimit-Reset are
recorded from every GitHub response into quota.json. A run is capped at
max_repos_per_run repos (default 5, config-overridable) and is skipped
entirely when the recorded budget cannot cover the planned calls. Never
self-DoS the shared bucket.

Failure isolation: one repo's DNS blip, 404, or GitHub's silent tree
truncation NEVER aborts the sweep. Truncation is logged as DEGRADED
coverage (report_error), not clean. Every target is wrapped; uncaught
per-target exceptions are forbidden.

HuggingFace: download URLs use the dataset's ACTUAL default branch,
resolved from the /api/datasets/<id>/refs endpoint — never a hardcoded
"main".

Politeness: GH_SLEEP between GitHub calls, HF_SLEEP between HF calls;
429/403 Retry-After is honored with backoff.

Categories:
- "candidate-trajectory": .json/.jsonl/.ndjson/.parquet/.arrow/.csv/.tsv
  (extension proves FORMAT, not that the file holds a trajectory)
- "docs", "media", "code": recognized non-trajectory files
- "unclassified": unknown extension — kept visible, never auto-skipped
- "skip": binary/archive/container blobs, with a skip_reason

Hits: one hit per newly-appeared candidate-trajectory file (seen_ids
dedup on repo+path+sha when a sha is available). Confidence LOW by
default (format match only, content unverified); MEDIUM only when the
path also matches a trajectory naming pattern from config. Grade
SECONDARY.

Read-only. No credentials, no POST, no logins.

Usage:
    reposcout.py [--dry-run] [--since-hours 24] [--json]
    reposcout.py --inventory-only   # refresh manifests, emit no hits
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    load_config, make_hit, utcnow_iso,
    is_new, mark_seen, emit, report_error,
)

LANE = "reposcout"
USER_AGENT = "silent-locus-reposcout/1.0 (+hunt: agent-trajectories)"
GH_SLEEP = 2.0   # seconds between GitHub API calls (shared 60/hr bucket)
HF_SLEEP = 1.0   # seconds between HuggingFace API calls
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
BACKOFF_CAP = 300  # longest Retry-After we will honor, in seconds
CALLS_PER_REPO = 2  # repo info + tree: worst-case GitHub calls per repo

STATE_DIR = os.path.expanduser(
    "~/workspace/silent-locus/scripts/scanners/state/reposcout")
QUOTA_PATH = os.path.join(STATE_DIR, "quota.json")

# owner/name and org/dataset ids. Validated BEFORE any URL is built.
ID_RE = re.compile(r"^[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+$")
BRANCH_RE = re.compile(r"^[A-Za-z0-9_.\-/]+$")


class EntryError(Exception):
    """A single watchlist entry failed (404, bad data, network blip)."""


class QuotaExhausted(Exception):
    """GitHub answered 403 with X-RateLimit-Remaining: 0."""


# ---------------------------------------------------------------- fetch

def _retry_after(headers: dict) -> int:
    try:
        wait = int(headers.get("retry-after", "60"))
    except (TypeError, ValueError):
        wait = 60
    return max(1, min(wait, BACKOFF_CAP))


def _record_quota(headers: dict) -> None:
    """Persist GitHub X-RateLimit state. Best effort; never raises."""
    try:
        rem = headers.get("x-ratelimit-remaining")
        reset = headers.get("x-ratelimit-reset")
        if rem is None or reset is None:
            return
        reset = int(reset)
        data = {
            "updated_at": utcnow_iso(),
            "github": {
                "remaining": int(rem),
                "reset": reset,
                "reset_iso": datetime.datetime.fromtimestamp(
                    reset, tz=datetime.timezone.utc).strftime(
                        "%Y-%m-%dT%H:%M:%SZ"),
            },
            "source": "api.github.com X-RateLimit-Remaining / "
                      "X-RateLimit-Reset response headers",
            "note": "VM egress IP shares one 60/hr unauthenticated "
                    "bucket; never self-DoS it",
        }
        os.makedirs(STATE_DIR, exist_ok=True)
        tmp = QUOTA_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        os.rename(tmp, QUOTA_PATH)
    except Exception:
        pass  # quota bookkeeping must never break a scan


def _get(url: str, *, github: bool = False) -> tuple[int, dict, bytes]:
    """GET with UA and rate-limit backoff. Returns (status, headers, body).

    headers keys are lowercased. 404 returns (404, headers, b"").
    A 403 with X-RateLimit-Remaining: 0 raises QuotaExhausted.
    Other 429/403 honor Retry-After, then raise the original error.
    """
    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req,
                                        timeout=REQUEST_TIMEOUT) as resp:
                headers = {k.lower(): v for k, v in resp.headers.items()}
                if github:
                    _record_quota(headers)
                return resp.status, headers, resp.read()
        except urllib.error.HTTPError as e:
            raw = e.headers.items() if e.headers else []
            headers = {k.lower(): v for k, v in raw}
            if github:
                _record_quota(headers)
            if e.code == 404:
                return 404, headers, b""
            if e.code in (429, 403) and attempt < MAX_RETRIES - 1:
                if (e.code == 403
                        and headers.get("x-ratelimit-remaining") == "0"):
                    raise QuotaExhausted(
                        "GitHub rate limit exhausted; resets at "
                        f"{headers.get('x-ratelimit-reset', 'unknown')}")
                wait = _retry_after(headers)
                print(f"  rate-limited ({e.code}), sleeping {wait}s",
                      file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    raise EntryError(f"GET failed after {MAX_RETRIES} attempts: {url}")


def _quote_path(path: str) -> str:
    """URL-quote a repo-relative path, keeping '/' separators."""
    return "/".join(urllib.parse.quote(seg, safe="")
                    for seg in path.split("/"))


# ---------------------------------------------------------------- categories

# Extension proves FORMAT, not content. ".jsonl" may hold benchmark
# prompts, not agent trajectories — hence "candidate-trajectory".
CANDIDATE_TRAJECTORY_EXTS = (".json", ".jsonl", ".ndjson", ".parquet",
                             ".arrow", ".csv", ".tsv")
DOC_EXTS = (".md", ".txt", ".rst", ".yaml", ".yml", ".toml", ".cfg")
MEDIA_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".webm")
CODE_EXTS = (".py", ".sh")
SKIP_EXTS = (".bin", ".img", ".iso", ".tar", ".gz", ".tgz", ".zip",
             ".7z", ".whl", ".so", ".dll", ".dylib", ".exe", ".o", ".a",
             ".pyc", ".pth", ".safetensors", ".onnx", ".gguf", ".ckpt",
             ".pt")
# Name fragments that mark Docker layers / container blobs even without
# an extension (e.g. "blobs/sha256:<hex>").
SKIP_NAME_HINTS = ("docker", "layer.tar", "sha256:", "blobs/")


def categorize(path: str) -> tuple[str, str | None]:
    """Return (category, skip_reason). Unknown extensions stay visible."""
    low = path.lower()
    if low.endswith(CANDIDATE_TRAJECTORY_EXTS):
        return "candidate-trajectory", None
    if low.endswith(DOC_EXTS):
        return "docs", None
    if low.endswith(MEDIA_EXTS):
        return "media", None
    if low.endswith(CODE_EXTS):
        return "code", None
    if any(h in low for h in SKIP_NAME_HINTS):
        return "skip", "docker-layer-or-blob"
    for ext in sorted(SKIP_EXTS, key=len, reverse=True):
        if low.endswith(ext):
            return "skip", f"binary/archive extension {ext}"
    # Unknown extension: keep visible, never auto-skip.
    return "unclassified", None


def _provenance_stub(url: str) -> dict:
    return {
        "source_url": url,
        "retrieval_method": "not-yet-retrieved",
        "retrieved_at": None,
        "sha256": None,
    }


# ---------------------------------------------------------------- state paths

def _sanitize_id(raw: str) -> str:
    """Make a state filename stem from a repo/dataset id.

    No path components from input: '/' becomes '__', every other
    unsafe char becomes '_'. The caller still joins against STATE_DIR
    and verifies the resolved path stays inside it.
    """
    s = str(raw).replace("/", "__")
    s = re.sub(r"[^A-Za-z0-9_.\-]", "_", s)
    s = s.strip("._") or "repo"
    return s[:100]


def _manifest_path(entry_id: str) -> str:
    """Fixed state-dir manifest path. Never caller-supplied."""
    stem = _sanitize_id(entry_id)
    path = os.path.realpath(os.path.join(STATE_DIR, stem + ".json"))
    base = os.path.realpath(STATE_DIR)
    if path != base and not path.startswith(base + os.sep):
        raise EntryError(f"unsafe manifest path for id {entry_id!r}")
    return path


def _load_quota() -> dict:
    """Load quota.json. Corrupt JSON or a well-formed-but-wrong-SHAPE
    dict both fail open to {} (no record), never raise downstream."""
    try:
        with open(QUOTA_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict):
        return {}
    gh = data.get("github")
    if gh is None:
        return data  # no record yet; deliberate fail-open
    if not isinstance(gh, dict):
        return {}
    rem, reset = gh.get("remaining"), gh.get("reset")
    if rem is not None and not isinstance(rem, int):
        return {}
    if reset is not None and not isinstance(reset, int):
        return {}
    return data


def _budget_ok(quota: dict, planned: int) -> tuple[bool, str]:
    """True when the recorded GitHub budget covers the planned calls.

    planned = number of repos to scan; each costs CALLS_PER_REPO
    GitHub API calls (repo info + tree) worst case.
    """
    gh = quota.get("github", {}) if isinstance(quota, dict) else {}
    rem, reset = gh.get("remaining"), gh.get("reset")
    if rem is None or reset is None:
        return True, "no quota record yet; assuming a fresh budget"
    now = time.time()
    need = planned * CALLS_PER_REPO
    if reset > now and rem < need:
        reset_iso = datetime.datetime.fromtimestamp(
            reset, tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return False, (f"GitHub quota exhausted: remaining={rem} < "
                       f"{need} calls needed for {planned} repos; "
                       f"bucket resets {reset_iso}")
    return True, f"budget ok: remaining={rem}, need={need}"


# ---------------------------------------------------------------- GitHub

def gh_repo_info(owner: str, name: str) -> dict:
    time.sleep(GH_SLEEP)
    url = f"https://api.github.com/repos/{owner}/{name}"
    status, _, body = _get(url, github=True)
    if status == 404:
        raise EntryError(f"GitHub repo not found: {owner}/{name}")
    info = json.loads(body)
    return {
        "owner": owner,
        "name": name,
        "default_branch": info.get("default_branch", "main"),
        "description": (info.get("description") or "")[:200],
        "stars": info.get("stargazers_count"),
        "html_url": info.get("html_url"),
    }


def gh_tree(owner: str, name: str, branch: str) -> tuple[list, bool]:
    """Recursive tree walk. Returns (blob entries, truncated)."""
    time.sleep(GH_SLEEP)
    url = (f"https://api.github.com/repos/{owner}/{name}/git/trees/"
           f"{branch}?recursive=1")
    status, _, body = _get(url, github=True)
    if status == 404:
        raise EntryError(f"GitHub tree not found: {owner}/{name}@{branch}")
    tree = json.loads(body)
    truncated = bool(tree.get("truncated"))
    blobs = [t for t in tree.get("tree", []) if t.get("type") == "blob"]
    return blobs, truncated


# ---------------------------------------------------------------- HuggingFace

def hf_dataset_info(ds_id: str) -> tuple[dict, list]:
    """Query the public datasets API. Returns (meta, sibling files)."""
    time.sleep(HF_SLEEP)
    url = f"https://huggingface.co/api/datasets/{ds_id}"
    status, _, body = _get(url)
    if status == 404:
        raise EntryError(f"HF dataset not found: {ds_id}")
    info = json.loads(body)
    meta = {
        "id": ds_id,
        "sha": info.get("sha"),
        "tags": (info.get("tags") or [])[:20],
        "likes": info.get("likes"),
        "downloads": info.get("downloads"),
    }
    return meta, info.get("siblings", []) or []


def hf_default_branch(ds_id: str) -> tuple[str, str]:
    """Resolve the dataset's ACTUAL default branch from the refs API.

    Returns (branch, source_note). Never hardcodes "main". A dataset
    with one branch uses it; with several, "main"/"master" is
    preferred, else the first branch alphabetically. The choice is
    recorded in the manifest so a wrong guess is visible and fixable.
    """
    time.sleep(HF_SLEEP)
    url = f"https://huggingface.co/api/datasets/{ds_id}/refs"
    status, _, body = _get(url)
    if status == 404:
        raise EntryError(f"HF refs not found: {ds_id}")
    refs = json.loads(body)
    branches = sorted({b.get("name") for b in refs.get("branches", [])
                       if b.get("name")})
    if not branches:
        raise EntryError(f"HF dataset has no branches: {ds_id}")
    if len(branches) == 1:
        return branches[0], "refs-api: single branch"
    for preferred in ("main", "master"):
        if preferred in branches:
            return (preferred,
                    f"refs-api: preferred {preferred!r} among "
                    f"{len(branches)} branches")
    return branches[0], (f"refs-api: heuristic first of "
                         f"{len(branches)} branches")


# ---------------------------------------------------------------- manifest

def _validate_entry(entry: dict) -> list[str]:
    """Fail-closed id checks. Problems listed; no URL is built on bad ids."""
    problems = []
    entry_id = entry.get("id")
    if entry_id and not ID_RE.match(str(entry_id)):
        problems.append(f"bad id {entry_id!r}: must match "
                        r"^[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+$")
    repo = entry.get("repo")
    hf = entry.get("hf_dataset")
    if not repo and not hf:
        problems.append("entry needs 'repo' and/or 'hf_dataset'")
    if repo and not ID_RE.match(str(repo)):
        problems.append(f"bad repo id {repo!r}: must match "
                        r"^[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+$")
    if hf and not ID_RE.match(str(hf)):
        problems.append(f"bad hf_dataset id {hf!r}: must match "
                        r"^[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+$")
    branch = entry.get("branch")
    if branch and not BRANCH_RE.match(str(branch)):
        problems.append(f"bad branch {branch!r}")
    return problems


def build_manifest(entry: dict) -> dict:
    """Inventory one watchlist entry. Ids are validated by the caller."""
    entry_id = (entry.get("id") or entry.get("repo")
                or entry.get("hf_dataset"))
    repo = entry.get("repo")
    hf = entry.get("hf_dataset")
    files: list[dict] = []
    repo_info = None
    hf_meta = None
    truncated = False

    if repo:
        owner, name = str(repo).split("/", 1)
        print(f"  GitHub: {owner}/{name}", file=sys.stderr)
        repo_info = gh_repo_info(owner, name)
        branch = entry.get("branch") or repo_info["default_branch"]
        repo_info["branch_scanned"] = branch
        blobs, truncated = gh_tree(owner, name, branch)
        print(f"    {len(blobs)} blobs on {branch}"
              f"{' (TRUNCATED)' if truncated else ''}",
              file=sys.stderr)
        for b in blobs:
            path = b["path"]
            url = (f"https://raw.githubusercontent.com/{owner}/{name}/"
                   f"{branch}/{_quote_path(path)}")
            cat, reason = categorize(path)
            files.append({
                "source": "github",
                "path": path,
                "size": b.get("size"),
                "sha": b.get("sha"),
                "url": url,
                "category": cat,
                "skip_reason": reason,
                "provenance": _provenance_stub(url),
            })

    if hf:
        ds_id = str(hf)
        print(f"  HuggingFace: {ds_id}", file=sys.stderr)
        hf_meta, siblings = hf_dataset_info(ds_id)
        branch, branch_source = hf_default_branch(ds_id)
        hf_meta["branch_resolved"] = branch
        hf_meta["branch_source"] = branch_source
        print(f"    {len(siblings)} siblings (branch {branch!r}: "
              f"{branch_source})", file=sys.stderr)
        for s in siblings:
            path = s["rfilename"]
            url = (f"https://huggingface.co/datasets/{ds_id}/resolve/"
                   f"{branch}/{_quote_path(path)}")
            cat, reason = categorize(path)
            files.append({
                "source": "huggingface",
                "path": path,
                "size": s.get("size"),
                "sha": None,
                "url": url,
                "category": cat,
                "skip_reason": reason,
                "provenance": _provenance_stub(url),
            })

    by_cat: dict[str, int] = {}
    total_bytes = 0
    for f in files:
        by_cat[f["category"]] = by_cat.get(f["category"], 0) + 1
        if isinstance(f["size"], int):
            total_bytes += f["size"]

    return {
        "generated_at": utcnow_iso(),
        "scout": "reposcout.py",
        "entry_id": entry_id,
        "entry_note": entry.get("note"),
        "truncated": truncated,
        "repo": repo_info,
        "hf_dataset": hf_meta,
        "files": files,
        "summary": {
            "total": len(files),
            "by_category": by_cat,
            "total_bytes": total_bytes,
            "github_files": sum(1 for f in files
                                if f["source"] == "github"),
            "hf_files": sum(1 for f in files
                            if f["source"] == "huggingface"),
        },
    }


def _write_manifest(entry_id: str, manifest: dict) -> str:
    path = _manifest_path(entry_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    os.rename(tmp, path)
    return path


def _load_manifest(entry_id: str) -> dict | None:
    path = _manifest_path(entry_id)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as e:
        report_error("reposcout", "manifest_corrupt",
                     f"stored manifest for {entry_id!r} unreadable: {e}; "
                     f"treating as first run",
                     {"entry_id": str(entry_id)[:100]})
        return None


# ---------------------------------------------------------------- patterns

def _compile_patterns(raw) -> list[tuple[str, re.Pattern]]:
    compiled = []
    for p in raw or []:
        try:
            compiled.append((str(p), re.compile(str(p), re.IGNORECASE)))
        except re.error as e:
            report_error("reposcout", "bad_pattern",
                         f"trajectory_name_patterns entry {p!r} does not "
                         f"compile: {e}")
    return compiled


def _pattern_hit(compiled, path: str) -> str | None:
    for raw, rx in compiled:
        try:
            if rx.search(path):
                return raw
        except Exception:
            continue
    return None


# ---------------------------------------------------------------- scan

def _entry_label(entry: dict) -> str:
    return str(entry.get("id") or entry.get("repo")
               or entry.get("hf_dataset") or "<unnamed>")


def scan_entry(entry: dict, seen_ids, collected_at: str,
               patterns: list, emit_hits: bool) -> list:
    """Scan one watchlist entry. Never raises except QuotaExhausted."""
    label = _entry_label(entry)
    hits = []
    try:
        problems = _validate_entry(entry)
        if problems:
            report_error("reposcout", "entry_misconfigured",
                         f"entry {label!r}: {'; '.join(problems)}; skipped, "
                         f"no URL built",
                         {"entry_id": label[:100]})
            print(f"[reposcout] {label}: misconfigured, skipped",
                  file=sys.stderr)
            return hits

        prev = _load_manifest(label)
        manifest = build_manifest(entry)
        if manifest["truncated"]:
            # Degraded coverage, not clean: GitHub caps recursive trees.
            # Missing files are false negatives, and a later full tree
            # can "discover" old files as new.
            report_error("reposcout", "tree_truncated",
                         f"{label}: GitHub truncated the recursive tree; "
                         f"manifest is partial (degraded coverage)",
                         {"entry_id": label[:100]})
        path = _write_manifest(label, manifest)
        s = manifest["summary"]
        print(f"[reposcout] {label}: manifest {s['total']} files "
              f"({s['github_files']} github + {s['hf_files']} hf) -> {path}",
              file=sys.stderr)

        if prev is None:
            print(f"[reposcout] {label}: first run, manifest stored; "
                  f"nothing is new yet", file=sys.stderr)
            return hits

        known = {(f["path"], f.get("sha") or "") for f in prev["files"]}
        new_files = [f for f in manifest["files"]
                     if (f["path"], f.get("sha") or "") not in known]
        new_traj = [f for f in new_files
                    if f["category"] == "candidate-trajectory"]
        print(f"[reposcout] {label}: {len(new_files)} new files, "
              f"{len(new_traj)} new candidate-trajectory",
              file=sys.stderr)

        if not emit_hits:
            return hits

        for f in new_traj:
            sha = f.get("sha") or "none"
            key = f"reposcout:{label}:{f['path']}:{sha}"
            if not is_new(seen_ids, key):
                continue
            pattern = _pattern_hit(patterns, f["path"])
            confidence = "MEDIUM" if pattern else "LOW"
            indicators = ["candidate-trajectory"]
            if pattern:
                indicators.append("trajectory-naming-pattern")
            size = f.get("size")
            size_str = f"{size} bytes" if isinstance(size, int) else "?"
            hits.append(make_hit(
                lane=LANE,
                source_url=f["url"],
                indicators_matched=indicators,
                confidence=confidence,
                summary=(f"[reposcout] NEW candidate-trajectory file: "
                         f"{label} {f['path']} ({size_str})"),
                provenance={
                    "method": "GitHub git/trees API (recursive) + "
                              "HuggingFace datasets API; manifest diff",
                    "repo": entry.get("repo"),
                    "hf_dataset": entry.get("hf_dataset"),
                    "branch_scanned": (manifest["repo"] or {}).get(
                        "branch_scanned")
                    if f["source"] == "github" else
                    (manifest["hf_dataset"] or {}).get("branch_resolved"),
                    "branch_source": (manifest["hf_dataset"] or {}).get(
                        "branch_source")
                    if f["source"] == "huggingface" else None,
                    "file_sha": f.get("sha"),
                    "retrieved_at": collected_at,
                    "retrieval_method": "not-yet-retrieved",
                    "sha256": None,
                    "note": "file content not fetched; category comes "
                            "from the file extension only",
                },
                extra={
                    "entry_id": label,
                    "path": f["path"],
                    "size": size,
                    "category": "candidate-trajectory",
                    "file_url": f["url"],
                    "file_sha": f.get("sha"),
                    "naming_pattern": pattern,
                    "manifest": path,
                },
                grade="SECONDARY",
            ))
            mark_seen(seen_ids, key)
    except QuotaExhausted:
        raise  # stops the whole sweep; handled in scan()
    except Exception as e:
        # Per-target failure isolation: log, continue the sweep.
        report_error("reposcout", "entry_failed",
                     f"{label}: {type(e).__name__}: {e}",
                     {"entry_id": label[:100]})
        print(f"[reposcout] {label}: failed ({type(e).__name__}); "
              f"continuing sweep", file=sys.stderr)
    return hits


def _dry_run_plan(rc: dict, watchlist: list) -> None:
    """List what WOULD be scanned. Zero network calls, zero writes."""
    enabled = rc.get("enabled", False)
    print("[dry-run] reposcout plan (no network, no writes)",
          file=sys.stderr)
    print(f"[dry-run] module enabled in config: {enabled}",
          file=sys.stderr)
    print(f"[dry-run] max_repos_per_run: {rc.get('max_repos_per_run', 5)}",
          file=sys.stderr)
    if not watchlist:
        print("[dry-run] no watchlist entries: no run", file=sys.stderr)
        return
    for e in watchlist:
        if not isinstance(e, dict):
            print("[dry-run]   (non-dict entry, would be skipped)",
                  file=sys.stderr)
            continue
        label = _entry_label(e)
        on = e.get("enabled", False) is True
        problems = _validate_entry(e)
        status = "would scan" if on and not problems else "would SKIP"
        why = ""
        if not on:
            why = " (entry not enabled:true)"
        elif problems:
            why = f" (invalid: {'; '.join(problems)})"
        try:
            mpath = _manifest_path(label)
        except EntryError:
            mpath = "<unsafe id>"
        print(f"[dry-run]   {status}: {label} "
              f"repo={e.get('repo')} hf={e.get('hf_dataset')} "
              f"manifest={mpath}{why}", file=sys.stderr)


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False,
         inventory_only: bool = False):
    """Run the repo-watchlist sweep. Returns hit dicts.

    Note: since_hours is accepted for contract compliance. Newness
    comes from manifest diffs, not a time window.
    """
    cfg = load_config()
    rc = cfg.get("reposcout", {}) or {}
    if seen_ids is None:
        seen_ids = set()
    watchlist = rc.get("watchlist", []) or []
    collected_at = utcnow_iso()

    if dry_run:
        # Zero network calls: config read only, nothing written.
        _dry_run_plan(rc, watchlist)
        return []

    # Disabled by default: refuse a live scan unless the module AND
    # each entry are explicitly enabled in config. Refusal is silent
    # in the error log by design: a disabled module must not spam the
    # shared log on every scheduled run.
    if not rc.get("enabled", False):
        print("[reposcout] live scan refused: reposcout.enabled is not "
              "true in swarm-infra-config.json (module ships disabled)",
              file=sys.stderr)
        return []

    if not watchlist:
        print("[reposcout] no watchlist entries in config 'reposcout' "
              "block: nothing to scan", file=sys.stderr)
        return []

    entries = [e for e in watchlist
               if isinstance(e, dict) and e.get("enabled", False) is True]
    if not entries:
        print("[reposcout] watchlist has entries but none carry "
              "enabled:true: nothing to scan", file=sys.stderr)
        return []

    try:
        cap = int(rc.get("max_repos_per_run", 5))
    except (TypeError, ValueError):
        cap = 5
    cap = max(1, cap)
    planned = entries[:cap]
    if len(entries) > cap:
        print(f"[reposcout] per-run cap {cap}: "
              f"{len(entries) - cap} enabled entries deferred",
              file=sys.stderr)

    ok, why = _budget_ok(_load_quota(), len(planned))
    if not ok:
        print(f"[reposcout] skipping run: {why}", file=sys.stderr)
        report_error("reposcout", "quota_exhausted", why,
                     {"planned_repos": str(len(planned))})
        return []
    print(f"[reposcout] {why}", file=sys.stderr)

    patterns = _compile_patterns(rc.get("trajectory_name_patterns", []))
    hits = []
    for i, entry in enumerate(planned):
        try:
            hits.extend(scan_entry(entry, seen_ids, collected_at,
                                   patterns,
                                   emit_hits=not inventory_only))
        except QuotaExhausted as e:
            report_error("reposcout", "quota_exhausted", str(e))
            print("[reposcout] GitHub quota exhausted mid-run; "
                  "stopping sweep", file=sys.stderr)
            break
        if i < len(planned) - 1:
            time.sleep(GH_SLEEP)  # spacing between repo targets
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    return hits


def main():
    ap = argparse.ArgumentParser(
        description="Lane 11 — reposcout: GitHub/HF trajectory-candidate "
                    "inventory")
    ap.add_argument("--dry-run", action="store_true",
                    help="List what WOULD be scanned. Zero network calls, "
                         "writes nothing.")
    ap.add_argument("--since-hours", type=float, default=24,
                    help="Look-back window in hours (default: 24). Accepted "
                         "for contract compliance; newness comes from "
                         "manifest diffs, not time.")
    ap.add_argument("--json", action="store_true",
                    help="Print hits as JSON array.")
    ap.add_argument("--inventory-only", action="store_true",
                    help="Refresh manifests via a live scan but emit no "
                         "hits. Distinct from --dry-run: this DOES use the "
                         "network.")
    args = ap.parse_args()
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run,
                inventory_only=args.inventory_only)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
