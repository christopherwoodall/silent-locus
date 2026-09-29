#!/usr/bin/env python3
"""Rewrite event.dataset for N-Z half of collections (keys >= 'n').

Idempotent: lines already carrying the target dataset are rewritten
byte-for-byte identical via json round-trip only if a change is needed;
unchanged lines are passed through verbatim.
"""
import json
import os
import sys
from collections import Counter

ROOT = "/mnt/c/Users/chris/Desktop/projects/silent-locus"
TARGETS_PATH = os.path.join(ROOT, "temp", "dataset_targets.json")
PARENTS = [os.path.join(ROOT, "data"), os.path.join(ROOT, "data", "aggregates")]


def main():
    with open(TARGETS_PATH, encoding="utf-8") as f:
        targets = json.load(f)
    def slug(k):
        # strip YYYY-MM-DD- prefix; split range is on the slug
        return k[11:] if len(k) > 11 and k[4] == "-" and k[10] == "-" else k

    my_keys = sorted(k for k in targets if slug(k) >= "n")
    print(f"Scope: {len(my_keys)} collections", file=sys.stderr)

    report = {}
    for key in my_keys:
        target = targets[key]
        for parent in PARENTS:
            d = os.path.join(parent, key)
            if not os.path.isdir(d):
                continue
            jsonl_files = []
            for dirpath, dirnames, filenames in os.walk(d):
                if "raw" in os.path.relpath(dirpath, d).split(os.sep):
                    dirnames[:] = []
                    continue
                for fn in filenames:
                    if fn.endswith(".jsonl"):
                        jsonl_files.append(os.path.join(dirpath, fn))
            old_counter = Counter()
            total = 0
            missing_event = 0
            for path in sorted(jsonl_files):
                tmp = path + ".tmp_rewrite"
                changed = 0
                nlines = 0
                with open(path, encoding="utf-8") as fin, open(
                    tmp, "w", encoding="utf-8", newline=""
                ) as fout:
                    for line in fin:
                        nlines += 1
                        stripped = line.rstrip("\n")
                        if not stripped:
                            fout.write(line)
                            continue
                        try:
                            rec = json.loads(stripped)
                        except json.JSONDecodeError:
                            fout.write(line)
                            continue
                        ev = rec.get("event")
                        if ev is None:
                            ev = {}
                            rec["event"] = ev
                            missing_event += 1
                        old = ev.get("dataset")
                        old_counter[old] += 1
                        if old == target:
                            fout.write(line)
                        else:
                            ev["dataset"] = target
                            fout.write(
                                json.dumps(rec, ensure_ascii=False) + "\n"
                            )
                            changed += 1
                if changed or missing_event:
                    os.replace(tmp, path)
                else:
                    os.remove(tmp)
                total += nlines
            report[os.path.relpath(d, ROOT)] = {
                "target": target,
                "records": total,
                "old_values": {str(k): v for k, v in old_counter.items()},
                "missing_event": missing_event,
            }
            print(
                f"{key} [{os.path.relpath(parent, ROOT)}]: {total} records, "
                f"old values: {dict(old_counter)}"
                + (f"  !! {missing_event} missing event" if missing_event else ""),
                file=sys.stderr,
            )

    out = os.path.join(ROOT, "temp", "rewrite_datasets_b_report.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"Report written to {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
