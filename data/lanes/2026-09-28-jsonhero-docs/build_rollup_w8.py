#!/usr/bin/env python3
"""Build rollup.jsonl for 2026-09-28-jsonhero-docs.

doc_family_rollup: the 12 live doc artifacts cluster into byte-size/top-key
families (dedupe groups). Repo root passed as argv[1] (no hardcoded paths).

Usage: python3 build_rollup_w8.py /path/to/silent-locus
"""
import hashlib
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone

REPO = sys.argv[1]
DIR = "2026-09-28-jsonhero-docs"
DATASET = DIR + "-rollup"
CREATED = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
OBSERVER = {"product": "muse", "type": "research-agent", "vendor": "meta"}

rows = [json.loads(l) for l in open(f"{REPO}/data/{DIR}/events.jsonl")]
docs = [r for r in rows if r["record_kind"] == "artifact_observation"]
assert len(docs) == 12, f"expected 12 docs, got {len(docs)}"

fams = defaultdict(list)
for r in docs:
    keys = r["labels"].get("doc.top_level_keys", [])
    fam_key = f"{keys[0] if keys else 'unkeyed'}:{r['labels']['doc.byte_size']}"
    fams[fam_key].append(r)

out = []
for fam_key in sorted(fams):
    members = sorted(fams[fam_key], key=lambda r: r["labels"]["doc.id"])
    ids = [r["labels"]["doc.id"] for r in members]
    total = sum(r["labels"]["doc.byte_size"] for r in members)
    identity = f"{DIR}|doc-family|{fam_key}"
    out.append({
        "@timestamp": "2026-09-28T00:00:00Z",
        "event": {"dataset": DATASET, "created": CREATED},
        "record_kind": "doc_family_rollup",
        "fingerprint": hashlib.sha256(identity.encode()).hexdigest(),
        "labels": {
            "family.key": fam_key,
            "family.first_top_key": fam_key.rsplit(":", 1)[0],
            "family.byte_size": members[0]["labels"]["doc.byte_size"],
            "docs.count": len(members),
            "docs.total_bytes": total,
            "docs.ids": ids,
            "timestamp_source": "fallback:dir_date_prefix",
        },
        "observer": OBSERVER,
        "description": (f"jsonhero doc family {fam_key}: {len(members)} docs, "
                        f"{total} B total ({', '.join(ids)})"),
    })

# --- independent recomputation check ---
assert sum(rl["labels"]["docs.count"] for rl in out) == 12
assert sum(rl["labels"]["docs.total_bytes"] for rl in out) == \
    sum(r["labels"]["doc.byte_size"] for r in docs)
seen = sorted(i for rl in out for i in rl["labels"]["docs.ids"])
assert seen == sorted(r["labels"]["doc.id"] for r in docs)

with open(f"{REPO}/data/{DIR}/rollup.jsonl", "w") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"wrote {len(out)} doc_family_rollup rows")
