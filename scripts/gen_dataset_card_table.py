#!/usr/bin/env python3
"""Generate the collection stats tables for the HF dataset card (README.md).

Walks data/YYYY-MM-DD-*/events.jsonl (the 64 dated collections) and
data/aggregates/*/events.jsonl, counts event rows, and computes the
min/max @timestamp per collection (excluding the documented
1970-01-01T00:00:00Z sentinel). Emits two markdown tables to stdout:
the 64-collection table, then the aggregate-collections table.

Stdlib only. Run from the silent-locus repo root:

    python3 scripts/gen_dataset_card_table.py > /tmp/card_table.md
"""
import json
import glob
import os

SENTINEL = "1970-01-01T00:00:00Z"


def stats(path):
    """Return (row_count, min_non_sentinel_ts, max_non_sentinel_ts)."""
    n = 0
    mn = mx = None
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            n += 1
            ts = rec.get("@timestamp", "")
            if ts and ts != SENTINEL:
                if mn is None or ts < mn:
                    mn = ts
                if mx is None or ts > mx:
                    mx = ts
    return n, mn, mx


def fmt_range(mn, mx):
    if mn is None:
        return "all 1970-sentinel (no recoverable event time)"
    if mn == mx:
        return mn
    return f"{mn} → {mx}"


def table(dirs, heading):
    rows = []
    total = 0
    for d in dirs:
        name = os.path.basename(d.rstrip("/"))
        ev = os.path.join(d, "events.jsonl")
        if not os.path.isfile(ev):
            rows.append((name, None, None))
            continue
        n, mn, mx = stats(ev)
        total += n
        rows.append((name, n, fmt_range(mn, mx)))
    print(heading)
    print()
    print("| Collection | Event rows | @timestamp range |")
    print("|---|---|---|")
    for name, n, rng in rows:
        if n is None:
            print(f"| `{name}` | — | event layer generated at ingest (see PROVENANCE.md) |")
        else:
            print(f"| `{name}` | {n:,} | {rng} |")
    print()
    print(f"*{len(rows)} collections · {total:,} event rows*")
    print()


def main():
    dated = sorted(glob.glob("data/2[0-9][0-9][0-9]-*/"))
    aggs = sorted(glob.glob("data/aggregates/2[0-9][0-9][0-9]-*/"))
    table(dated, f"### Event collections ({len(dated)})")
    table(aggs, f"### Aggregate collections ({len(aggs)})")


if __name__ == "__main__":
    main()
