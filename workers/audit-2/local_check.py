#!/usr/bin/env python3
"""LOCAL ground-truth check for audit-2 chunk: valid JSONL, article match, timestamps non-increasing."""
import json, os, sys

BASE = os.path.expanduser("~/workspace/silent-locus-top500")
CHUNK = os.path.join(BASE, "data/2026-10-06-wikipedia-top500-infra-scan/raw/audit-chunks/audit-2.tsv")
REVDIR = os.path.join(BASE, "data/2026-10-06-wikipedia-top500-infra-scan/raw/revisions")

def check_file(path, expected_title, expected_rank):
    issues = []
    lines, min_ts, max_ts = 0, None, None
    prev_ts = None
    prev_revid = None
    try:
        with open(path, encoding="utf-8") as f:
            for i, raw in enumerate(f, 1):
                s = raw.strip()
                if not s:
                    issues.append(f"line {i}: empty line")
                    continue
                try:
                    rec = json.loads(s)
                except Exception as e:
                    issues.append(f"line {i}: JSON parse error: {e}")
                    continue
                lines += 1
                if rec.get("article") != expected_title:
                    issues.append(f"line {i}: article mismatch {rec.get('article')!r}")
                if rec.get("rank") != expected_rank:
                    issues.append(f"line {i}: rank mismatch {rec.get('rank')!r}")
                ts = rec.get("timestamp")
                if not ts:
                    issues.append(f"line {i}: missing timestamp")
                else:
                    if min_ts is None or ts < min_ts: min_ts = ts
                    if max_ts is None or ts > max_ts: max_ts = ts
                    if prev_ts is not None and ts > prev_ts:
                        issues.append(f"line {i}: timestamp increasing {prev_ts} -> {ts}")
                    prev_ts = ts
                rv = rec.get("revid")
                if prev_revid is not None and rv is not None and rv >= prev_revid:
                    issues.append(f"line {i}: revid not decreasing {prev_revid} -> {rv}")
                prev_revid = rv
    except FileNotFoundError:
        issues.append("FILE MISSING")
    except Exception as e:
        issues.append(f"read error: {e}")
    return lines, min_ts, max_ts, issues

results = []
for line in open(CHUNK, encoding="utf-8"):
    line = line.rstrip("\n")
    if not line:
        continue
    rank_s, title = line.split("\t", 1)
    rank = int(rank_s)
    path = os.path.join(REVDIR, f"{rank}.jsonl")
    n, mn, mx, issues = check_file(path, title, rank)
    results.append({
        "rank": rank, "title": title, "file": f"{rank}.jsonl",
        "lines": n, "min_ts": mn, "max_ts": mx, "issues": issues,
    })

json.dump(results, open(os.path.join(BASE, "workers/audit-2/local_results.json"), "w"), indent=1)
n_bad = sum(1 for r in results if r["issues"] or r["lines"] == 0)
print(f"checked {len(results)}, with issues or empty: {n_bad}")
for r in results:
    if r["issues"] or r["lines"] == 0:
        print(r["rank"], repr(r["title"]), r["lines"], r["min_ts"], r["issues"][:3])
