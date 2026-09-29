#!/usr/bin/env python3
"""Build rollup.jsonl for 2026-09-27-rmn-re.

Monthly link_growth_rollup (new/cumulative) derived from the per-link
YOURLS created dates — same shape as data/2016-12-28-rmn-re-history/rollup.jsonl.
Repo root passed as argv[1] (no hardcoded paths).

Usage: python3 build_rollup_w8.py /path/to/silent-locus
"""
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone

REPO = sys.argv[1]
DIR = "2026-09-27-rmn-re"
DATASET = DIR + "-rollup"
CREATED = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
OBSERVER = {"product": "muse", "type": "research-agent", "vendor": "meta"}

rows = [json.loads(l) for l in open(f"{REPO}/data/{DIR}/events.jsonl")]
links = [r for r in rows if r["record_kind"] == "shortener_link"]
assert links, "no shortener_link events"
months = Counter()
for r in links:
    c = r["labels"].get("link.created")
    assert c, "missing link.created"
    dt = datetime.strptime(c, "%b %d, %Y %H:%M")
    months[dt.strftime("%Y-%m")] += 1

out = []
cumulative = 0
for m in sorted(months):
    cumulative += months[m]
    identity = f"growth_curve:{m}"
    out.append({
        "@timestamp": f"{m}-01T00:00:00Z",
        "event": {"dataset": DATASET, "created": CREATED},
        "record_kind": "link_growth_rollup",
        "fingerprint": hashlib.sha256(identity.encode()).hexdigest(),
        "labels": {
            "curve.month": m,
            "curve.new": months[m],
            "curve.cumulative": cumulative,
            "timestamp_source": "labels:curve.month",
        },
        "observer": OBSERVER,
        "description": (f"rmn.re link-table growth {m}: "
                        f"+{months[m]} new, {cumulative} cumulative"),
    })

# --- independent recomputation check ---
check = Counter()
for r in links:
    dt = datetime.strptime(r["labels"]["link.created"], "%b %d, %Y %H:%M")
    check[dt.strftime("%Y-%m")] += 1
assert len(out) == len(check)
cum = 0
for rl, m in zip(out, sorted(check)):
    cum += check[m]
    assert rl["labels"]["curve.month"] == m
    assert rl["labels"]["curve.new"] == check[m]
    assert rl["labels"]["curve.cumulative"] == cum
assert cum == len(links)

with open(f"{REPO}/data/{DIR}/rollup.jsonl", "w") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"wrote {len(out)} link_growth_rollup rows")
