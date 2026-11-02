#!/usr/bin/env python3
"""Trajectory scout: inventory downloadable trajectory artifacts for a repo.

Given a GitHub repo (owner/name) and a HuggingFace dataset ID, this script
walks the repo tree via api.github.com and queries the HuggingFace datasets
API, then writes a manifest JSON listing every downloadable file with size,
category, direct download URL, and a provenance stub for the scrape step.

Read-only. Dry-run by default: never downloads file bodies, only metadata.
Slow crawl: sleeps between requests, honors 429/403 backoff.

Usage:
    python3 trajectory-scout.py --repo internlm/WildClawBench \
        --hf-dataset internlm/WildClawBench \
        --out /tmp/wildclaw-manifest.json

Manifest shape:
    {
      "generated_at": "...Z",
      "repo": {"owner": ..., "name": ..., "default_branch": ..., "sha": ...},
      "hf_dataset": {"id": ..., "sha": ..., "tags": [...]},
      "files": [
        {"source": "github"|"huggingface", "path": ..., "size": ...,
         "url": ..., "category": "trajectory"|"docs"|"media"|"code"|"skip",
         "skip_reason": ...|null,
         "provenance": {"source_url": ..., "retrieval_method": "not-yet-retrieved",
                        "retrieved_at": null, "sha256": null}}
      ],
      "summary": {"total": N, "by_category": {...}, "total_bytes": ...}
    }

Provenance stubs are filled by the scrape step (retrieved_at, sha256,
retrieval_method="https-get"), which must also write a .PROVENANCE.txt
alongside each cached file per the lane convention.
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
import time
import urllib.error
import urllib.request

USER_AGENT = "silent-locus-trajectory-scout/1.0 (+hunt: agent-trajectories)"
GH_SLEEP = 2.0   # seconds between GitHub API calls (unauthenticated: 60/hr)
HF_SLEEP = 1.0   # seconds between HuggingFace API calls


def _now_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def _get(url: str, retries: int = 3) -> tuple[int, dict, bytes]:
    """GET with UA, rate-limit backoff. Returns (status, headers, body)."""
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.status, dict(resp.headers), resp.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 403) and attempt < retries - 1:
                wait = int(e.headers.get("Retry-After", "60"))
                print(f"  rate-limited ({e.code}), sleeping {wait}s",
                      file=sys.stderr)
                time.sleep(wait)
                continue
            if e.code == 404:
                return 404, {}, b""
            raise
    raise RuntimeError(f"GET failed after {retries} attempts: {url}")


# ---------------------------------------------------------------- categories

TRAJECTORY_EXTS = {".json", ".jsonl", ".ndjson", ".parquet", ".arrow",
                   ".csv", ".tsv"}
DOC_EXTS = {".md", ".txt", ".rst", ".yaml", ".yml", ".toml", ".cfg"}
MEDIA_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".webm"}
SKIP_EXTS = {".bin", ".img", ".iso", ".tar", ".gz", ".tgz", ".zip", ".7z",
             ".whl", ".so", ".dll", ".dylib", ".exe", ".o", ".a", ".pyc",
             ".pth", ".safetensors", ".onnx", ".gguf", ".ckpt", ".pt"}
# Name fragments that mark Docker layers / container blobs even without ext.
SKIP_NAME_HINTS = ("docker", "layer.tar", "sha256:", "blobs/")


def categorize(path: str, size: int | None) -> tuple[str, str | None]:
    """Return (category, skip_reason)."""
    low = path.lower()
    # Recognized extensions decide first; name hints only catch
    # extension-less blobs (e.g. "blobs/sha256:<hex>").
    for ext in TRAJECTORY_EXTS:
        if low.endswith(ext):
            return "trajectory", None
    for ext in DOC_EXTS:
        if low.endswith(ext):
            return "docs", None
    for ext in MEDIA_EXTS:
        if low.endswith(ext):
            return "media", None
    if low.endswith(".py") or low.endswith(".sh"):
        return "code", None
    if any(h in low for h in SKIP_NAME_HINTS):
        return "skip", "docker-layer-or-blob"
    for ext in sorted(SKIP_EXTS, key=len, reverse=True):
        if low.endswith(ext):
            return "skip", f"binary/archive extension {ext}"
    # Unknown extension: keep visible, do not auto-skip.
    return "docs", None


def _provenance_stub(url: str) -> dict:
    return {
        "source_url": url,
        "retrieval_method": "not-yet-retrieved",
        "retrieved_at": None,
        "sha256": None,
    }


# ---------------------------------------------------------------- GitHub

def gh_repo_info(owner: str, name: str) -> dict:
    url = f"https://api.github.com/repos/{owner}/{name}"
    status, _, body = _get(url)
    if status == 404:
        raise SystemExit(f"GitHub repo not found: {owner}/{name}")
    info = json.loads(body)
    return {
        "owner": owner,
        "name": name,
        "default_branch": info.get("default_branch", "main"),
        "description": (info.get("description") or "")[:200],
        "stars": info.get("stargazers_count"),
        "html_url": info.get("html_url"),
    }


def gh_tree(owner: str, name: str, branch: str) -> list[dict]:
    """Recursive tree walk. Returns blob entries only."""
    time.sleep(GH_SLEEP)
    url = (f"https://api.github.com/repos/{owner}/{name}/git/trees/"
           f"{branch}?recursive=1")
    status, _, body = _get(url)
    if status == 404:
        raise SystemExit(f"GitHub tree not found: {owner}/{name}@{branch}")
    tree = json.loads(body)
    if tree.get("truncated"):
        print("  WARNING: tree truncated by GitHub; manifest is partial",
              file=sys.stderr)
    return [t for t in tree.get("tree", []) if t.get("type") == "blob"]


# ---------------------------------------------------------------- HuggingFace

def hf_dataset_info(ds_id: str) -> tuple[dict, list[dict]]:
    """Query the public datasets API. Returns (info, sibling files)."""
    time.sleep(HF_SLEEP)
    url = f"https://huggingface.co/api/datasets/{ds_id}"
    status, _, body = _get(url)
    if status == 404:
        raise SystemExit(f"HF dataset not found: {ds_id}")
    info = json.loads(body)
    siblings = info.get("siblings", []) or []
    meta = {
        "id": ds_id,
        "sha": info.get("sha"),
        "tags": info.get("tags", [])[:20],
        "likes": info.get("likes"),
        "downloads": info.get("downloads"),
    }
    return meta, siblings


# ---------------------------------------------------------------- main

def build_manifest(repo: str, hf_dataset: str | None,
                   branch: str | None) -> dict:
    owner, name = repo.split("/", 1)
    files: list[dict] = []

    print(f"GitHub: {owner}/{name}", file=sys.stderr)
    rinfo = gh_repo_info(owner, name)
    br = branch or rinfo["default_branch"]
    blobs = gh_tree(owner, name, br)
    print(f"  {len(blobs)} blobs on {br}", file=sys.stderr)
    for b in blobs:
        path = b["path"]
        size = b.get("size")
        url = (f"https://raw.githubusercontent.com/{owner}/{name}/"
               f"{br}/{path}")
        cat, reason = categorize(path, size)
        files.append({
            "source": "github",
            "path": path,
            "size": size,
            "url": url,
            "category": cat,
            "skip_reason": reason,
            "provenance": _provenance_stub(url),
        })

    hf_meta: dict | None = None
    if hf_dataset:
        print(f"HuggingFace: {hf_dataset}", file=sys.stderr)
        hf_meta, siblings = hf_dataset_info(hf_dataset)
        print(f"  {len(siblings)} siblings", file=sys.stderr)
        for s in siblings:
            path = s["rfilename"]
            size = s.get("size")
            url = f"https://huggingface.co/datasets/{hf_dataset}/resolve/main/{path}"
            cat, reason = categorize(path, size)
            files.append({
                "source": "huggingface",
                "path": path,
                "size": size,
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
        "generated_at": _now_utc(),
        "scout": "trajectory-scout.py",
        "repo": {**rinfo, "branch_scanned": br},
        "hf_dataset": hf_meta,
        "files": files,
        "summary": {
            "total": len(files),
            "by_category": by_cat,
            "total_bytes": total_bytes,
            "github_files": sum(1 for f in files if f["source"] == "github"),
            "hf_files": sum(1 for f in files if f["source"] == "huggingface"),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", required=True, help="owner/name on GitHub")
    ap.add_argument("--hf-dataset", default=None,
                    help="org/id on HuggingFace (optional)")
    ap.add_argument("--branch", default=None,
                    help="branch to scan (default: repo default)")
    ap.add_argument("--out", required=True, help="manifest JSON output path")
    ap.add_argument("--only", default=None,
                    help="comma list of categories to keep "
                         "(default: trajectory,docs,media,code)")
    args = ap.parse_args()

    manifest = build_manifest(args.repo, args.hf_dataset, args.branch)
    if args.only:
        keep = {c.strip() for c in args.only.split(",")}
        manifest["files"] = [f for f in manifest["files"]
                             if f["category"] in keep]
        # Recompute summary for the filtered set.
        by_cat: dict[str, int] = {}
        total_bytes = 0
        for f in manifest["files"]:
            by_cat[f["category"]] = by_cat.get(f["category"], 0) + 1
            if isinstance(f["size"], int):
                total_bytes += f["size"]
        manifest["summary"]["total"] = len(manifest["files"])
        manifest["summary"]["by_category"] = by_cat
        manifest["summary"]["total_bytes"] = total_bytes

    with open(args.out, "w") as fh:
        json.dump(manifest, fh, indent=2)
    s = manifest["summary"]
    print(f"manifest: {s['total']} files "
          f"({s['github_files']} github + {s['hf_files']} hf), "
          f"{s['total_bytes'] / 1e6:.1f} MB total, "
          f"categories={s['by_category']}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
