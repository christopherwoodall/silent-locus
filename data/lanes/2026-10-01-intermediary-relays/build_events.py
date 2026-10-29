#!/usr/bin/env python3
"""Build events.jsonl for 2026-10-01-intermediary-relays.

Records from sweep_results.json:
- `indicator_census`: per-indicator matching-line/file counts
- `relay_score`: per-relay indicator co-occurrence scores
- `relay_ts_sample`: <=40 timestamped evidence samples per relay
plus `relay_mention_sample`: one per line of sweep_samples.jsonl
(<=3000 evidence samples, <=600 chars each).
"""
import hashlib
import json
from datetime import datetime, timezone

LANE = "2026-10-01-intermediary-relays"
CREATED = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
SWEEP_TS = "2026-10-01T00:00:00Z"


def fp(*parts):
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


records = []

res = json.load(open("sweep_results.json", encoding="utf-8"))

for ind, n in res["census"].items():
    files = res.get("census_files", {}).get(ind, 0)
    records.append(
        {
            "@timestamp": SWEEP_TS,
            "event": {"dataset": LANE, "created": CREATED},
            "record_kind": "indicator_census",
            "fingerprint": fp(LANE, "indicator-census", ind),
            "labels": {
                "indicator": ind,
                "matching.lines": n,
                "files": files,
                "timestamp_source": "fallback:dir_date_prefix",
            },
            "description": (
                f"indicator census: '{ind}' matched in {n} lines across {files} "
                f"files (2026-10-01 intermediary-relays sweep)"
            ),
            "confidence": "confirmed",
        }
    )

for relay, s in res["relay_scores"].items():
    records.append(
        {
            "@timestamp": SWEEP_TS,
            "event": {"dataset": LANE, "created": CREATED},
            "record_kind": "relay_score",
            "fingerprint": fp(LANE, "relay-score", relay),
            "labels": {
                "relay": relay,
                "distinct.indicators": s["distinct_indicators"],
                "total.cooccur.hits": s["total_cooccur_hits"],
                "line.matches": s["line_matches"],
                "indicators": s["indicators"],
                "per.indicator": s["per_indicator"],
                "timestamp_source": "fallback:dir_date_prefix",
            },
            "description": (
                f"relay score: {relay} — {s['distinct_indicators']} distinct "
                f"indicators co-occur, {s['line_matches']} relay-mentioning lines, "
                f"{s['total_cooccur_hits']} total co-occurring indicator hits"
            ),
            "confidence": "confirmed",
        }
    )

for i, (relay, samples) in enumerate(res["ts_samples"].items()):
    for j, s in enumerate(samples):
        records.append(
            {
                "@timestamp": s["ts"],
                "event": {"dataset": LANE, "created": CREATED},
                "record_kind": "relay_ts_sample",
                "fingerprint": fp(LANE, "relay-ts", relay, str(i), str(j), s["snippet"]),
                "labels": {
                    "relay": relay,
                    "sample.index": f"{i}:{j}",
                    "timestamp_source": "ts_samples",
                },
                "description": f"relay timestamped sample: {relay} — {s['snippet']}",
                "confidence": "confirmed",
            }
        )

with open("sweep_samples.jsonl", encoding="utf-8") as f:
    for k, line in enumerate(f):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        records.append(
            {
                "@timestamp": SWEEP_TS,
                "event": {"dataset": LANE, "created": CREATED},
                "record_kind": "relay_mention_sample",
                "fingerprint": fp(LANE, "relay-sample", d["relay"], str(k), d["text"]),
                "labels": {
                    "relay": d["relay"],
                    "sample.line": k,
                    "timestamp_source": "fallback:dir_date_prefix",
                },
                "description": d["text"],
                "confidence": "confirmed",
            }
        )

with open("events.jsonl", "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("records:", len(records))
