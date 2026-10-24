#!/usr/bin/env python3
"""Lane prcomment: GitHub PR and issue comment behavior scanner.

Purpose: search GitHub issues and pull requests for comments that
match behavior patterns from config. A match is text evidence only.
It is not proof of agent activity.

How it works:
- Step 1: read the "prcomment" block from swarm-infra-config.json.
- Step 2: search GitHub issues and pull requests for each query.
- Step 3: fetch issue comments and pull-request review comments
  for each candidate. The search API does not return the matching
  comment, so the comments must be fetched separately.
- Step 4: match each comment body against the config patterns.
- Step 5: emit one hit for each new matching comment.

Behavior families: each pattern in config carries a family name.
The family groups related patterns. A comment that matches two or
more distinct families is stronger evidence than a comment that
matches one family only.

Grade: SECONDARY. The source is GitHub metadata, not first-party
trajectory bytes. Confidence is LOW by default. Confidence is
MEDIUM only when one comment matches two or more distinct families.

Newness: a comment is new when its comment id is not in
state/prcomment/seen.json. The --since-hours flag is accepted for
contract compliance only. It does not filter by time.

Budget rules:
- The VM egress IP shares one 60-request-per-hour unauthenticated
  GitHub API bucket. Do not self-DoS that bucket.
- X-RateLimit-Remaining and X-RateLimit-Reset are recorded from
  every GitHub response into state/prcomment/quota.json.
- A run is skipped when the recorded budget cannot cover the
  planned calls. No quota record means a fresh budget is assumed.
- Planned calls = one search call per query, plus two comment
  calls per candidate per query (issue comments and review
  comments), times the pages needed per candidate. At the default
  of 100 comments per candidate, that is one page per candidate,
  so the formula matches the spec exactly.
- A 403 with X-RateLimit-Remaining: 0 stops the whole sweep.
- A search 422 (validation failed) is logged for that query only.
  The sweep continues with the next query.

Failure isolation: one query failure never aborts the sweep.
One raw-capture failure never aborts the sweep. One bad pattern
never aborts the sweep. Bad patterns are logged and skipped.

Disabled by default: a live scan is refused unless
prcomment.enabled is true in config. --dry-run still lists the
plan, with zero network calls and zero writes.

Read-only: GET only. No credentials. No POST. No login.

Usage:
    prcomment.py [--dry-run] [--since-hours 24] [--json]
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import math
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

LANE = "prcomment"
USER_AGENT = "silent-locus-prcomment/1.0 (+hunt: agent-behaviors)"
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
BACKOFF_CAP = 300  # longest Retry-After honored, in seconds

STATE_DIR = os.path.expanduser(
    "~/workspace/silent-locus/scripts/scanners/state/prcomment")
QUOTA_PATH = os.path.join(STATE_DIR, "quota.json")
SEEN_PATH = os.path.join(STATE_DIR, "seen.json")
RAW_BASE = os.path.expanduser(
    "~/workspace/silent-locus/data/lanes/github-pr-comments/raw")

REPO_RE = re.compile(r"^https://api\.github\.com/repos/"
                     r"([A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+)$")


class EntryError(Exception):
    """A single query or candidate failed."""


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


def _get(url: str) -> tuple[int, dict, bytes]:
    """GET with UA and rate-limit backoff. Returns (status, headers, body).

    Headers keys are lowercased. 404 and 422 return a status tuple
    so the caller can decide per query. A 403 with
    X-RateLimit-Remaining: 0 raises QuotaExhausted at once, on any
    attempt. Other 429/403 responses honor Retry-After, then raise
    the original error after the last retry.
    """
    for attempt in range(MAX_RETRIES):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req,
                                        timeout=REQUEST_TIMEOUT) as resp:
                headers = {k.lower(): v for k, v in resp.headers.items()}
                _record_quota(headers)
                return resp.status, headers, resp.read()
        except urllib.error.HTTPError as e:
            raw = e.headers.items() if e.headers else []
            headers = {k.lower(): v for k, v in raw}
            _record_quota(headers)
            if e.code in (404, 422):
                return e.code, headers, b""
            if (e.code == 403
                    and headers.get("x-ratelimit-remaining") == "0"):
                raise QuotaExhausted(
                    "GitHub rate limit exhausted; resets at "
                    f"{headers.get('x-ratelimit-reset', 'unknown')}")
            if e.code in (429, 403) and attempt < MAX_RETRIES - 1:
                wait = _retry_after(headers)
                print(f"  rate-limited ({e.code}), sleeping {wait}s",
                      file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    raise EntryError(f"GET failed after {MAX_RETRIES} attempts: {url}")


# ---------------------------------------------------------------- state

def _load_quota() -> dict:
    """Load quota.json. Bad JSON or a wrong-shape dict fails open to {}."""
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
    """True when the recorded GitHub budget covers the planned calls."""
    gh = quota.get("github", {}) if isinstance(quota, dict) else {}
    rem, reset = gh.get("remaining"), gh.get("reset")
    if rem is None or reset is None:
        return True, "no quota record yet; assuming a fresh budget"
    now = time.time()
    if reset > now and rem < planned:
        reset_iso = datetime.datetime.fromtimestamp(
            reset, tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return False, (f"GitHub quota exhausted: remaining={rem} < "
                       f"{planned} calls needed; "
                       f"bucket resets {reset_iso}")
    return True, f"budget ok: remaining={rem}, need={planned}"


def _load_seen() -> set:
    """Load seen comment keys. A missing or corrupt file means empty."""
    try:
        with open(SEEN_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return set()
    if not isinstance(data, list):
        return set()
    return {str(k) for k in data}


def _save_seen(seen_ids) -> None:
    """Write seen keys with tmp-file + rename. Never raises."""
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        tmp = SEEN_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(sorted(seen_ids), fh, indent=2)
        os.rename(tmp, SEEN_PATH)
    except OSError as e:
        report_error("prcomment", "seen_write_failed",
                     f"could not persist seen.json: {e}")


# ---------------------------------------------------------------- config

def _int_config(block: dict, key: str, default: int) -> int:
    try:
        value = int(block.get(key, default))
    except (TypeError, ValueError):
        return default
    return max(1, value)


def _float_config(block: dict, key: str, default: float) -> float:
    try:
        value = float(block.get(key, default))
    except (TypeError, ValueError):
        return default
    return max(0.0, value)


def _queries(block: dict) -> list[str]:
    """Queries as strings. A dict entry with q/query is also accepted."""
    out = []
    for q in block.get("queries", []) or []:
        if isinstance(q, str) and q.strip():
            out.append(q.strip())
        elif isinstance(q, dict):
            text = q.get("q") or q.get("query")
            if isinstance(text, str) and text.strip():
                out.append(text.strip())
    return out


def _compile_patterns(raw) -> list[dict]:
    """Compile config patterns. Failures are logged and skipped."""
    compiled = []
    for p in raw or []:
        if not isinstance(p, dict):
            report_error("prcomment", "bad_pattern",
                         f"pattern entry is not an object: {p!r}; skipped")
            continue
        name = str(p.get("name") or p.get("regex") or "")
        family = str(p.get("family") or "unknown")
        regex = p.get("regex")
        if not regex:
            report_error("prcomment", "bad_pattern",
                         f"pattern {name!r} has no regex; skipped")
            continue
        try:
            compiled.append({
                "name": name,
                "family": family,
                "regex": re.compile(str(regex), re.IGNORECASE),
            })
        except re.error as e:
            report_error("prcomment", "bad_pattern",
                         f"pattern {name!r} does not compile: {e}; skipped")
    return compiled


# ---------------------------------------------------------------- GitHub

def _search(query: str, max_candidates: int, gh_sleep: float) -> list:
    """Search issues/PRs. Returns candidate dicts. 422 returns []."""
    time.sleep(gh_sleep)
    params = urllib.parse.urlencode({
        "q": query,
        "per_page": max_candidates,
        "sort": "updated",
    })
    url = f"https://api.github.com/search/issues?{params}"
    status, _headers, body = _get(url)
    if status == 422:
        report_error("prcomment", "search_validation_failed",
                     f"search query failed validation (422): {query!r}; "
                     f"query skipped",
                     {"query": query[:200]})
        print(f"[prcomment] query {query!r}: 422 validation failed; "
              f"skipping query", file=sys.stderr)
        return []
    if status == 404:
        return []
    data = json.loads(body)
    items = data.get("items", []) if isinstance(data, dict) else []
    return items if isinstance(items, list) else []


def _fetch_comments(url: str, max_comments: int,
                    gh_sleep: float) -> list:
    """Fetch comment pages for one comments URL. 404/422 means []."""
    comments: list = []
    page = 1
    while len(comments) < max_comments:
        time.sleep(gh_sleep)
        sep = "&" if "?" in url else "?"
        page_url = f"{url}{sep}per_page=100&page={page}"
        status, _headers, body = _get(page_url)
        if status in (404, 422):
            return comments
        data = json.loads(body)
        if not isinstance(data, list):
            return comments
        comments.extend(data)
        if len(data) < 100:
            break
        page += 1
    return comments[:max_comments]


def _repo_from_candidate(candidate: dict) -> str | None:
    """Owner/repo from repository_url. None when it cannot be parsed."""
    repo_url = candidate.get("repository_url") or ""
    m = REPO_RE.match(str(repo_url))
    if m:
        return m.group(1)
    return None


# ---------------------------------------------------------------- raw capture

def _make_raw_dir(collected_at: str) -> str | None:
    """Create the per-run raw dir. None on failure; never raises."""
    stamp = collected_at.replace(":", "").replace("-", "")
    raw_dir = os.path.join(RAW_BASE, stamp)
    try:
        os.makedirs(raw_dir, exist_ok=True)
    except OSError as e:
        report_error("prcomment", "raw_dir_failed",
                     f"could not create raw dir {raw_dir}: {e}; "
                     f"raw capture disabled for this run")
        return None
    return raw_dir


def _capture_raw(raw_dir: str, comment: dict, collected_at: str) -> None:
    """Write one matching comment JSON + provenance + sha256.

    Failures are logged and never abort the sweep.
    """
    try:
        comment_id = str(comment.get("id", "unknown"))
        safe_id = re.sub(r"[^A-Za-z0-9_.\-]", "_", comment_id)
        payload = json.dumps(comment, indent=2, ensure_ascii=False).encode(
            "utf-8")
        base = os.path.join(raw_dir, safe_id)
        tmp = base + ".json.tmp"
        with open(tmp, "wb") as fh:
            fh.write(payload)
        os.rename(tmp, base + ".json")
        digest = hashlib.sha256(payload).hexdigest()
        with open(base + ".sha256", "w", encoding="utf-8") as fh:
            fh.write(digest + "\n")
        source_url = comment.get("html_url") or ""
        with open(base + ".PROVENANCE.txt", "w",
                  encoding="utf-8") as fh:
            fh.write(f"source URL: {source_url}\n")
            fh.write(f"retrieval time: {collected_at}\n")
            fh.write("method: GitHub API GET (search/issues + "
                     "issue/review comments)\n")
            fh.write(f"sha256: {digest}\n")
    except OSError as e:
        report_error("prcomment", "raw_capture_failed",
                     f"raw capture failed for comment "
                     f"{comment.get('id')}: {e}")


# ---------------------------------------------------------------- scan

def _match_comment(body: str, patterns: list) -> tuple[list, list]:
    """Return (matched pattern names, distinct families) for a body."""
    names: list = []
    families: list = []
    for p in patterns:
        try:
            if p["regex"].search(body):
                names.append(p["name"])
                if p["family"] not in families:
                    families.append(p["family"])
        except Exception:
            continue
    return names, families


def _scan_query(query: str, block: dict, patterns: list, seen_ids,
                collected_at: str, raw_dir: str | None,
                stats: dict | None = None) -> list:
    """Scan one query. Never raises except QuotaExhausted."""
    hits = []
    max_candidates = _int_config(block, "max_candidates_per_query", 5)
    max_comments = _int_config(block, "max_comments_per_candidate", 100)
    gh_sleep = _float_config(block, "gh_sleep", 2.0)
    try:
        candidates = _search(query, max_candidates, gh_sleep)
        print(f"[prcomment] query {query!r}: {len(candidates)} candidates",
              file=sys.stderr)
        for cand in candidates:
            if not isinstance(cand, dict):
                continue
            candidate_url = cand.get("html_url") or ""
            repo = _repo_from_candidate(cand) or ""
            pr_number = cand.get("number")
            comments: list = []
            comments_url = cand.get("comments_url")
            if comments_url:
                comments.extend(_fetch_comments(
                    str(comments_url), max_comments, gh_sleep))
            # Review comments exist only on pull requests.
            if isinstance(cand.get("pull_request"), dict) and repo \
                    and pr_number is not None:
                review_url = (f"https://api.github.com/repos/{repo}/"
                              f"pulls/{pr_number}/comments")
                comments.extend(_fetch_comments(
                    review_url, max_comments, gh_sleep))
            if stats is not None:
                stats["candidates"] = stats.get("candidates", 0) + 1
                stats["comments_fetched"] = (
                    stats.get("comments_fetched", 0) + len(comments))
            for comment in comments:
                if not isinstance(comment, dict):
                    continue
                comment_id = comment.get("id")
                if comment_id is None:
                    continue
                key = f"prcomment:{comment_id}"
                if not is_new(seen_ids, key):
                    continue
                body = comment.get("body") or ""
                names, families = _match_comment(str(body), patterns)
                if not names:
                    continue
                # Seen only on a match: non-matching comments are
                # re-checked on later runs, matching ones are not.
                mark_seen(seen_ids, key)
                if raw_dir is not None:
                    _capture_raw(raw_dir, comment, collected_at)
                author = comment.get("user") or {}
                author_type = ("bot" if author.get("type") == "Bot"
                               else "user")
                confidence = ("MEDIUM" if len(families) >= 2 else "LOW")
                hits.append(make_hit(
                    lane=LANE,
                    source_url=comment.get("html_url") or candidate_url,
                    indicators_matched=names,
                    confidence=confidence,
                    summary=(f"[prcomment] {repo or 'unknown-repo'} "
                             f"PR #{pr_number}: comment matches "
                             f"families {', '.join(families)}"),
                    provenance={
                        "method": "GitHub search/issues API + issue "
                                  "comments and pull-request review "
                                  "comments APIs; local regex match",
                        "query": query,
                        "candidate_url": candidate_url,
                        "comment_id": comment_id,
                        "retrieved_at": collected_at,
                    },
                    extra={
                        "repo": repo,
                        "pr_number": pr_number,
                        "comment_author_type": author_type,
                        "families": families,
                        "patterns": names,
                    },
                    grade="SECONDARY",
                ))
    except QuotaExhausted:
        raise  # stops the whole sweep; handled in scan()
    except Exception as e:
        report_error("prcomment", "query_failed",
                     f"query {query!r}: {type(e).__name__}: {e}",
                     {"query": query[:200]})
        print(f"[prcomment] query {query!r}: failed "
              f"({type(e).__name__}); continuing sweep", file=sys.stderr)
    return hits


def _dry_run_plan(block: dict | None) -> None:
    """List what WOULD be scanned. Zero network calls, zero writes."""
    print("[dry-run] prcomment plan (no network, no writes)",
          file=sys.stderr)
    if block is None:
        print("[dry-run] no prcomment block: no run", file=sys.stderr)
        return
    queries = _queries(block)
    patterns = block.get("patterns", []) or []
    max_candidates = _int_config(block, "max_candidates_per_query", 5)
    max_comments = _int_config(block, "max_comments_per_candidate", 100)
    pages = max(1, math.ceil(max_comments / 100))
    planned = len(queries) + len(queries) * max_candidates * 2 * pages
    print(f"[dry-run] module enabled in config: "
          f"{block.get('enabled', False)}", file=sys.stderr)
    print(f"[dry-run] queries ({len(queries)}):", file=sys.stderr)
    for q in queries:
        print(f"[dry-run]   {q}", file=sys.stderr)
    print(f"[dry-run] patterns ({len(patterns)}):", file=sys.stderr)
    for p in patterns:
        if isinstance(p, dict):
            print(f"[dry-run]   {p.get('name')}: family="
                  f"{p.get('family')} regex={p.get('regex')}",
                  file=sys.stderr)
        else:
            print(f"[dry-run]   {p!r} (non-dict, would be skipped)",
                  file=sys.stderr)
    print(f"[dry-run] max_candidates_per_query: {max_candidates}",
          file=sys.stderr)
    print(f"[dry-run] max_comments_per_candidate: {max_comments}",
          file=sys.stderr)
    print(f"[dry-run] planned calls (worst case): {planned}",
          file=sys.stderr)
    ok, why = _budget_ok(_load_quota(), planned)
    print(f"[dry-run] quota status: {why} (run would proceed: {ok})",
          file=sys.stderr)


def scan(since_hours: float = 24, seen_ids=None, dry_run: bool = False):
    """Run the PR-comment sweep. Returns hit dicts.

    Note: since_hours is accepted for contract compliance. Newness
    comes from seen comment ids, not a time window.
    """
    cfg = load_config()
    block = cfg.get("prcomment")
    if not isinstance(block, dict):
        block = None

    if dry_run:
        # Zero network calls: config read only, nothing written.
        _dry_run_plan(block)
        return []

    if block is None:
        print("[prcomment] no prcomment block in "
              "swarm-infra-config.json: no run", file=sys.stderr)
        return []

    # Disabled by default: refuse a live scan unless the module is
    # explicitly enabled in config. Refusal is silent in the error
    # log by design: a disabled module must not spam the shared log
    # on every scheduled run.
    if not block.get("enabled", False):
        print("[prcomment] live scan refused: prcomment.enabled is not "
              "true in swarm-infra-config.json (module ships disabled)",
              file=sys.stderr)
        return []

    queries = _queries(block)
    if not queries:
        print("[prcomment] no queries in config 'prcomment' block: "
              "nothing to scan", file=sys.stderr)
        return []

    if seen_ids is None:
        seen_ids = _load_seen()
    collected_at = utcnow_iso()
    max_candidates = _int_config(block, "max_candidates_per_query", 5)
    max_comments = _int_config(block, "max_comments_per_candidate", 100)
    pages = max(1, math.ceil(max_comments / 100))
    planned = len(queries) + len(queries) * max_candidates * 2 * pages

    ok, why = _budget_ok(_load_quota(), planned)
    if not ok:
        print(f"[prcomment] skipping run: {why}", file=sys.stderr)
        report_error("prcomment", "quota_exhausted", why,
                     {"planned_calls": str(planned)})
        return []
    print(f"[prcomment] {why}", file=sys.stderr)

    patterns = _compile_patterns(block.get("patterns", []))
    raw_capture = block.get("raw_capture", True) is True
    sleep_between = _float_config(block, "sleep_between_queries", 2.0)
    raw_dir = _make_raw_dir(collected_at) if raw_capture else None

    hits = []
    stats: dict = {"queries_run": 0, "candidates": 0,
                   "comments_fetched": 0}
    for i, query in enumerate(queries):
        stats["queries_run"] += 1
        try:
            hits.extend(_scan_query(query, block, patterns, seen_ids,
                                    collected_at, raw_dir, stats))
        except QuotaExhausted as e:
            report_error("prcomment", "quota_exhausted", str(e))
            print("[prcomment] GitHub quota exhausted mid-run; "
                  "stopping sweep", file=sys.stderr)
            break
        if i < len(queries) - 1:
            time.sleep(sleep_between)
    _save_seen(seen_ids)
    print(f"[prcomment] run totals: queries_run={stats['queries_run']} "
          f"candidates={stats['candidates']} "
          f"comments_fetched={stats['comments_fetched']} "
          f"hits={len(hits)}", file=sys.stderr)
    rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    hits.sort(key=lambda h: (rank.get(h["confidence"], 3), h["summary"]))
    return hits


def main():
    ap = argparse.ArgumentParser(
        description="Lane prcomment: GitHub PR/issue comment behavior "
                    "scanner")
    ap.add_argument("--dry-run", action="store_true",
                    help="List what WOULD be scanned. Zero network calls, "
                         "writes nothing.")
    ap.add_argument("--since-hours", type=float, default=24,
                    help="Look-back window in hours (default: 24). Accepted "
                         "for contract compliance; newness comes from "
                         "seen comment ids, not time.")
    ap.add_argument("--json", action="store_true",
                    help="Print hits as JSON array.")
    args = ap.parse_args()
    hits = scan(since_hours=args.since_hours, dry_run=args.dry_run)
    emit(hits, args.json, args.dry_run)


if __name__ == "__main__":
    main()
