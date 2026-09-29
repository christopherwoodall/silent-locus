#!/usr/bin/env python3
"""Build rollup.jsonl for 2022-08-09-github-forensics.

Aggregates the fork event stream into per-day fork-burst rows plus one
issue-activity summary row. Repo root passed as argv[1] (no hardcoded paths).

Usage: python3 build_rollup_w8.py /path/to/silent-locus
"""
import hashlib
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone

REPO = sys.argv[1]
DIR = "2022-08-09-github-forensics"
DATASET = DIR + "-rollup"
CREATED = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
OBSERVER = {"product": "muse", "type": "research-agent", "vendor": "meta"}

rows = [json.loads(l) for l in open(f"{REPO}/data/{DIR}/events.jsonl")]
forks = [r for r in rows if r["record_kind"] == "repo_fork"]
issues = [r for r in rows if r["record_kind"] == "repo_issue"]
assert forks, "no fork events found"
for r in forks:
    assert r["labels"].get("fork.created_at"), "fork missing created_at"
    assert r["labels"].get("fork.owner"), "fork missing owner"

out = []

# --- per-day fork bursts ---
by_day = defaultdict(list)
for r in forks:
    by_day[r["@timestamp"][:10]].append(r)
cumulative = 0
for day in sorted(by_day):
    frs = sorted(by_day[day], key=lambda r: r["@timestamp"])
    cumulative += len(frs)
    owners = [r["labels"]["fork.owner"] for r in frs]
    identity = f"{DIR}|fork-day|{day}"
    out.append({
        "@timestamp": frs[0]["@timestamp"],
        "event": {"dataset": DATASET, "created": CREATED},
        "record_kind": "fork_day_rollup",
        "fingerprint": hashlib.sha256(identity.encode()).hexdigest(),
        "labels": {
            "day": day,
            "forks.new": len(frs),
            "forks.cumulative": cumulative,
            "fork.first": frs[0]["@timestamp"],
            "fork.last": frs[-1]["@timestamp"],
            "fork.owners": owners,
            "timestamp_source": "labels:rollup.day",
        },
        "observer": OBSERVER,
        "description": (f"exploitgym forks {day}: +{len(frs)} new, "
                        f"{cumulative} cumulative; "
                        f"{frs[0]['@timestamp'][11:19]}->{frs[-1]['@timestamp'][11:19]}Z"),
    })

# --- issue activity summary ---
ist = [r for r in issues]
opens = sum(1 for r in ist if r["labels"]["issue.state"] == "open")
closed = sum(1 for r in ist if r["labels"]["issue.state"] == "closed")
prs = sum(1 for r in ist if str(r["labels"]["issue.is_pr"]).lower() == "true")
c_at = [r["labels"]["issue.created_at"] for r in ist]
identity = f"{DIR}|issue-summary"
out.append({
    "@timestamp": max(c_at),
    "event": {"dataset": DATASET, "created": CREATED},
    "record_kind": "issue_summary_rollup",
    "fingerprint": hashlib.sha256(identity.encode()).hexdigest(),
    "labels": {
        "issues.total": len(ist),
        "issues.open": opens,
        "issues.closed": closed,
        "issues.prs": prs,
        "issues.plain": len(ist) - prs,
        "issue.window_first": min(c_at),
        "issue.window_last": max(c_at),
        "timestamp_source": "labels:issue.created_at(max)",
    },
    "observer": OBSERVER,
    "description": (f"exploitgym issue/PR activity summary: {len(ist)} rows "
                    f"({opens} open, {closed} closed; {prs} PRs), "
                    f"{min(c_at)[:10]}->{max(c_at)[:10]}"),
})

# --- independent recomputation check ---
check = defaultdict(int)
for r in forks:
    check[r["@timestamp"][:10]] += 1
assert len(out) - 1 == len(check), "day count mismatch"
assert all(any(rl["labels"]["day"] == d and rl["labels"]["forks.new"] == n
               for rl in out) for d, n in check.items()), "per-day counts mismatch"
assert sum(rl["labels"]["forks.new"] for rl in out
           if rl["record_kind"] == "fork_day_rollup") == len(forks)
assert [rl["labels"]["forks.cumulative"] for rl in out
        if rl["record_kind"] == "fork_day_rollup"][-1] == len(forks)

with open(f"{REPO}/data/{DIR}/rollup.jsonl", "w") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"wrote {len(out)} rollup rows "
      f"({len(check)} fork-day + 1 issue-summary)")
