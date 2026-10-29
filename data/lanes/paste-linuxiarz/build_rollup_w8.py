#!/usr/bin/env python3
"""Build rollup.jsonl for 2026-09-28-paste-linuxiarz.

paste_day_burst: per-day paste bursts over the 2026-05-26 -> 2026-06-17 window
(the 2026-06-16 119-paste burst is the swarm's agent-comms wave).
Repo root passed as argv[1] (no hardcoded paths).

Usage: python3 build_rollup_w8.py /path/to/silent-locus
"""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

REPO = sys.argv[1]
DIR = "2026-09-28-paste-linuxiarz"
DATASET = DIR + "-rollup"
CREATED = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
OBSERVER = {"product": "muse", "type": "research-agent", "vendor": "meta"}

rows = [json.loads(l) for l in open(f"{REPO}/data/{DIR}/events.jsonl")]
pastes = [r for r in rows if r["record_kind"] == "relay_paste"]
assert pastes, "no relay_paste events"

by_day = defaultdict(list)
for r in pastes:
    by_day[r["@timestamp"][:10]].append(r)

out = []
for day in sorted(by_day):
    drs = sorted(by_day[day], key=lambda r: r["@timestamp"])
    titles = Counter(r["labels"].get("paste.title", "") for r in drs)
    status = Counter(r["labels"].get("paste.live_status", "") for r in drs)
    identity = f"linuxiarz-paste-day:{day}"
    out.append({
        "@timestamp": drs[0]["@timestamp"],
        "event": {"dataset": DATASET, "created": CREATED},
        "record_kind": "paste_day_burst",
        "fingerprint": hashlib.sha256(identity.encode()).hexdigest(),
        "labels": {
            "day": day,
            "pastes.count": len(drs),
            "paste.first": drs[0]["@timestamp"],
            "paste.last": drs[-1]["@timestamp"],
            "titles.distinct": len(titles),
            "titles.top": titles.most_common(1)[0][0],
            "titles.top_count": titles.most_common(1)[0][1],
            "live_status.404": status.get("http_404", 0),
            "live_status.error": status.get("error", 0),
            "timestamp_source": "labels:paste.source_date_literal",
        },
        "observer": OBSERVER,
        "description": (f"linuxiarz relay pastes {day}: {len(drs)} pastes "
                        f"{drs[0]['@timestamp'][11:19]}->{drs[-1]['@timestamp'][11:19]}Z; "
                        f"top title '{titles.most_common(1)[0][0]}' "
                        f"x{titles.most_common(1)[0][1]}; "
                        f"live-check: {status.get('http_404', 0)} 404, "
                        f"{status.get('error', 0)} error"),
    })

# --- independent recomputation check ---
check = Counter(r["@timestamp"][:10] for r in pastes)
assert len(out) == len(check)
assert all(any(rl["labels"]["day"] == d and rl["labels"]["pastes.count"] == n
               for rl in out) for d, n in check.items())
assert sum(rl["labels"]["pastes.count"] for rl in out) == len(pastes)

with open(f"{REPO}/data/{DIR}/rollup.jsonl", "w") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"wrote {len(out)} paste_day_burst rows")
