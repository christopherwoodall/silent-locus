#!/usr/bin/env python3
"""Aggregate-only analysis of unmeasured-leftovers captures.
Prints counts, types, date ranges. Never prints logins (except Bot-type
commit authors, which are agent/bot accounts by authorship), emails,
URLs, titles, or message bodies."""
import json, glob, os
from collections import Counter

D = os.path.dirname(os.path.abspath(__file__))

def load(f):
    with open(os.path.join(D, f)) as fh:
        return json.load(fh)

def dates(rows, key):
    ds = sorted(r for r in (row_date(r, key) for r in rows) if r)
    return (ds[0], ds[-1]) if ds else (None, None)

def row_date(r, key):
    # commit rows: commit.author.date ; issue rows: createdAt
    if key == "commit":
        try:
            return r["commit"]["author"]["date"][:10]
        except Exception:
            return None
    return (r.get("createdAt") or "")[:10] or None

def summarize_issues(f):
    rows = load(f)
    types = Counter((r.get("author") or {}).get("type") for r in rows)
    repos = len({(r.get("repository") or {}).get("nameWithOwner") for r in rows})
    lo, hi = dates(rows, "issue")
    bots = sorted({(r.get("author") or {}).get("login") for r in rows
                   if (r.get("author") or {}).get("type") == "Bot"})
    print(f"{f}: rows={len(rows)}/30 repos={repos} dates={lo}..{hi} "
          f"author_types={dict(types)} bot_authors={bots}")

def summarize_commits(f):
    rows = load(f)
    at = Counter((r.get("author") or {}).get("type") for r in rows)
    ct = Counter((r.get("committer") or {}).get("type") for r in rows)
    ab = Counter((r.get("author") or {}).get("is_bot") for r in rows)
    da = len({(r.get("author") or {}).get("login") for r in rows})
    dc = len({(r.get("committer") or {}).get("login") for r in rows})
    lo, hi = dates(rows, "commit")
    inwin = sum(1 for r in rows if (row_date(r, "commit") or "") >= "2025-11-01")
    bots = sorted({(r.get("author") or {}).get("login") for r in rows
                   if (r.get("author") or {}).get("type") == "Bot"})
    msgs = [((r.get("commit") or {}).get("message") or "") for r in rows]
    footer = sum(1 for m in msgs if "Co-Authored-By:" in m)
    codex_footer = sum(1 for m in msgs if "Co-Authored-By: Codex" in m)
    print(f"{f}: rows={len(rows)}/30 author_types={dict(at)} "
          f"committer_types={dict(ct)} author_is_bot={dict(ab)} "
          f"distinct_authors={da} distinct_committers={dc} "
          f"dates={lo}..{hi} in_window={inwin}/30 "
          f"with_coauthor_footer={footer}/30 with_codex_footer={codex_footer}/30 "
          f"bot_authors={bots}")

print("== commits ==")
summarize_commits("gh-commits-codex.json")
print("== prs ==")
for f in ["gh-prs-claudecode.json", "gh-prs-agent-harness.json"]:
    summarize_issues(f)
print("== phrases ==")
for f in sorted(glob.glob(os.path.join(D, "phrase-*.json"))):
    summarize_issues(os.path.basename(f))
