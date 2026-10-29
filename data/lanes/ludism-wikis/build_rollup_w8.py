#!/usr/bin/env python3
"""Build rollup.jsonl for 2026-09-28-ludism-wikis.

target_probe_rollup: per-target verdicts aggregating the (target, proxy)
probe matrix (the 2 example.com proxy-control probes, target
'proxy_control (example.com)', are controls — excluded from the rollup).
Repo root passed as argv[1] (no hardcoded paths).

Usage: python3 build_rollup_w8.py /path/to/silent-locus
"""
import hashlib
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone

REPO = sys.argv[1]
DIR = "2026-09-28-ludism-wikis"
DATASET = DIR + "-rollup"
CREATED = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
OBSERVER = {"product": "muse", "type": "research-agent", "vendor": "meta"}

rows = [json.loads(l) for l in open(f"{REPO}/data/{DIR}/events.jsonl")]
probes = [r for r in rows
          if r["record_kind"] == "venue_probe"
          and r["labels"].get("probe.target") != "proxy_control (example.com)"]
assert probes, "no target probes found"
# the 2 example.com proxy-control probes are controls, not targets

targets = defaultdict(list)
for r in probes:
    targets[r["labels"]["probe.target"]].append(r)

out = []
for target in sorted(targets):
    rs = targets[target]
    ok_via = sorted(r["labels"]["probe.via"] for r in rs if r["labels"]["probe.ok"])
    failed_via = sorted(r["labels"]["probe.via"] for r in rs
                        if not r["labels"]["probe.ok"])
    verdict = f"reachable-via-{ok_via[0]}" if ok_via else "unreachable-all-proxies"
    first = min(r["@timestamp"] for r in rs)
    identity = f"ludism-probe-rollup:{target}"
    out.append({
        "@timestamp": first,
        "event": {"dataset": DATASET, "created": CREATED},
        "record_kind": "target_probe_rollup",
        "fingerprint": hashlib.sha256(identity.encode()).hexdigest(),
        "labels": {
            "target": target,
            "probes.total": len(rs),
            "probes.ok": len(ok_via),
            "probes.ok_via": ok_via,
            "probes.failed_via": failed_via,
            "target.verdict": verdict,
            "timestamp_source": "labels:probe.fetched_at",
        },
        "observer": OBSERVER,
        "description": (f"ludism/wiki probe target {target}: "
                        f"{len(ok_via)}/{len(rs)} proxies succeeded "
                        f"({verdict})"),
    })

# --- independent recomputation check ---
assert sum(rl["labels"]["probes.total"] for rl in out) == len(probes)
assert sum(rl["labels"]["probes.ok"] for rl in out) == \
    sum(1 for r in probes if r["labels"]["probe.ok"])

with open(f"{REPO}/data/{DIR}/rollup.jsonl", "w") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"wrote {len(out)} target_probe_rollup rows")
